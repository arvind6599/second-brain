# from helpers import *
import dspy
from typing import List, Optional
import os
import logging
from RealtimeSTT import AudioToTextRecorder
import os
import json
import wave
from datetime import datetime
# import pyautogui
# import ollama
import logging
from openai import OpenAI
# from pydantic import BaseModel
# from prompt_library import promptDict

# Disable LiteLLM logs
dspy.disable_litellm_logging()
logging.getLogger("litellm").setLevel(logging.ERROR)

# Set up the language model


# lm = dspy.LM('ollama_chat/llama3.2:3b', api_base='http://localhost:11434', api_key='')
lm = dspy.LM("openai/gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"), verbose=False)
dspy.configure(lm=lm)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Directory for storing notes
NOTES_DIR = "notes"
AUDIO_FORMAT = 2  # 2 bytes for paInt16
CHANNELS = 1
RATE = 16000

os.makedirs(NOTES_DIR, exist_ok=True)


# Define the signatures for each task
class NoteFormatter(dspy.Signature):
    """Format a raw spoken note into a well-structured written note."""

    text: str = dspy.InputField(desc="The raw text from speech-to-text")
    formatted_note: str = dspy.OutputField(
        desc="The formatted note with improved structure and clarity"
    )


class TitleGenerator(dspy.Signature):
    """Generate a concise, descriptive title for a note."""

    text: str = dspy.InputField(desc="The note text")
    title: str = dspy.OutputField(desc="A short, descriptive title for the note")


class TagSelector(dspy.Signature):
    """Select the most relevant tags for a note from a predefined list."""

    text: str = dspy.InputField(desc="The note text")
    available_tags: List[str] = dspy.InputField(
        desc="List of available tags to choose from"
    )
    selected_tags: List[str] = dspy.OutputField(
        desc="The most relevant tags for this note (1-3 tags)"
    )


# Implement the modules
class NoteTaker(dspy.Module):
    """
    Class to handle the input note text and parse into the file as a note
    """

    def __init__(self):
        self.formatter = dspy.Predict(NoteFormatter)
        self.title_generator = dspy.Predict(TitleGenerator)
        self.tag_selector = dspy.Predict(TagSelector)

    def format_note(self, text: str) -> str:
        """Format raw text into a structured note."""
        response = self.formatter(text=text)
        return response.formatted_note

    def generate_title(self, text: str) -> str:
        """Generate a title for the note."""
        response = self.title_generator(text=text)
        return response.title

    def select_tags(self, text: str, available_tags: List[str]) -> List[str]:
        """Select relevant tags for the note."""
        response = self.tag_selector(text=text, available_tags=available_tags)
        return response.selected_tags


# Example of how to integrate this with your existing code
def integrated_format_text(text: str, available_tags: List[str]):
    """
    Replacement for your original format_text function that uses DSPy
    with Ollama backend.
    """

    # Create note taker
    nt = NoteTaker()

    # Generate formatted content
    formatted_text = nt.format_note(text)
    title = nt.generate_title(text)
    tags = nt.select_tags(text, available_tags)

    # Create and return the Note object (adjusted for your Pydantic model)
    return {"title": title, "note": formatted_text, "tags": tags, "transcript": text}


def create_audio_callback():
    chunks = []
    is_recording = [True]  # Using list as a mutable container

    def audio_callback(chunk: bytes):
        if is_recording[0]:  # Only append chunks when recording is active
            chunks.append(chunk)

    return audio_callback, chunks, is_recording

def create_folder_structure():
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%B")
    day = now.strftime("%d")
    timestamp = now.strftime("%H-%M-%S")

    directory = os.path.join(NOTES_DIR, year, month, day, timestamp)
    os.makedirs(directory, exist_ok=True)

    return directory


class MyNote:

    def __init__(self):
        self.user_text = ""
        self.prompts = ""
        self.audio_callback, self.chunks, self.is_recording = create_audio_callback()
        self.recorder = AudioToTextRecorder(
            model="tiny",
            no_log_file=True,
            post_speech_silence_duration=7,
            on_recorded_chunk=self.audio_callback,
        )
        self.tags = [
            "Reflection",
            "Work",
            "Leisure",
            "Interests",
            "Events",
            "Reminders",
        ]
        self.note_dict = {}

    def recordingNote(self):

        ## Start the recorder, audio bytes get recorded and transcribed using the RealtTimeSTT library
        print("Starting recording .....")
        self.recorder.start()
        input("Press enter to stop recording")
        print("Stopped Recording")


        ## Stop collecting chunks before stopping the recorder
        self.is_recording[0] = False
        self.recorder.stop()


        ## Store the transcription and print it
        self.user_text = self.recorder.text()
        print("Transcript : ", self.user_text)

        if input("Do you want to process the note? (y/n)").lower() == "y":
            self.text_to_note()
        if input("Do you want to record again? (y/n)").lower() == "y":
            self.audio_callback, self.chunks, self.is_recording = create_audio_callback()
            self.recordingNote()
        else:
            ## Shutdown the recorder and end the progran cos you got nothing else to do mateeeee
            self.recorder.shutdown()
            print("Bye bye Arvind")

    def text_to_note(self):
        """
        Store the output of the DSPy pipeline to form the final note dict and store it
        """

        # Create note taker
        nt = NoteTaker()

        # Generate formatted content
        formatted_text = nt.format_note(self.user_text)
        title = nt.generate_title(self.user_text)
        tags = nt.select_tags(self.user_text, self.tags)

        # Create and return the Note object (adjusted for your Pydantic model)
        self.note_dict = {
            "title": title,
            "note": formatted_text,
            "tags": tags,
            "transcript": self.user_text,
        }

        print("Here is the formatted Note")
        print(self.note_dict)

        if input("Do you wish to save the note (y/n)").lower() == "y":
            self.save_note()

    def save_note(self):
        directory = create_folder_structure()
        filename = os.path.join(directory, "note.json")

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.note_dict, f, indent=4, ensure_ascii=False)

        print(f"Note saved as: {filename}")
        audio_path = os.path.join(directory, "audio.wav")

        with wave.Wave_write(open(audio_path, "wb")) as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(AUDIO_FORMAT)
            wf.setframerate(RATE)
            wf.writeframes(b"".join(self.chunks))
        ## reset the chunks after saving
        self.chunks = []

        ## Successs message for saving the note
        print(f"Audio saved as: {audio_path}")


# At the end of the file, add:
if __name__ == "__main__":

    if input("Do you wish to record a note? (y/n) ").lower() == "y":
        example = MyNote()
        example.recordingNote()
    else:
        query = input("What do you want then?")
        response = (
            client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant",
                    },
                    {"role": "user", "content": query},
                ],
            )
            .choices[0]
            .message.content
        )

        print(response)
