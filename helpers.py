import os
import json
import wave
from datetime import datetime
from RealtimeSTT import AudioToTextRecorder
import pyautogui
import ollama
from pydantic import BaseModel
from prompt_library import promptDict
import re

MODEL = 'llama3.2:3b'

# Directory for storing notes
NOTES_DIR = "notes"
AUDIO_FORMAT = 2  # 2 bytes for paInt16
CHANNELS = 1
RATE = 16000

os.makedirs(NOTES_DIR, exist_ok=True)

ALL_TAGS = ['Work', 'Reflection', 'Food', 'Travel', 'Sport']

# Define your Note model
class Note(BaseModel):
    title: str
    note: str
    tags: list[str]
    transcript: str

# --- Folder Structure & File Saving ---

def create_folder_structure():
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%B")
    day = now.strftime("%d")
    timestamp = now.strftime("%H-%M-%S")

    directory = os.path.join(NOTES_DIR, year, month, day, timestamp)
    os.makedirs(directory, exist_ok=True)

    return directory, timestamp

def save_note(note: Note, chunks: list[bytes], directory: str, timestamp: str):
    filename = os.path.join(directory, f"note.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(note.dict(), f, indent=4, ensure_ascii=False)
    
    print(f"Note saved as: {filename}")

    audio_path = os.path.join(directory, f"audio.wav")

    with wave.Wave_write(open(audio_path, 'wb')) as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(AUDIO_FORMAT)
        wf.setframerate(RATE)
        wf.writeframes(b''.join(chunks))

    print(f"Audio saved as: {audio_path}")


def create_audio_callback():
    chunks = []

    def audio_callback(chunk: bytes):
        chunks.append(chunk)

    return audio_callback, chunks

# --- Ollama-based Note Formatter ---

def format_text(text, style="rant"):
    formatted_text = ollama.generate(model=MODEL, prompt=promptDict['noteTaker'].format(text=text))['response']
    title = ollama.generate(model=MODEL, prompt=promptDict['titlePrompt'].format(text=text))['response'].replace('"', '')
    tag = ollama.generate(model=MODEL, prompt=promptDict['tagPrompt'].format(text=text, tags=ALL_TAGS))['response']
    tag_list = list(set([x for x in re.findall(r'\b\w+\b', tag) if x in ALL_TAGS]))

    return Note(
        title=title,
        note=formatted_text,
        tags=tag_list,
        transcript=text
    )

# --- Interactive Voice Recording and Note Saving ---

def rant():
    while True:
        try:
            audio_callback, audio_chunks = create_audio_callback()

            # Start recorder and attach callback
            recorder = AudioToTextRecorder(
                model="tiny",
                no_log_file=True,
                post_speech_silence_duration=7,
                on_recorded_chunk=audio_callback
            )

            print("Recording... Press Enter to stop.")
            recorder.start()
            input("Press Enter to stop recording...")
            recorder.stop()

            # Get transcription
            user_text = recorder.text()
            print("Transcription: ", user_text)

            # Format and save note
            formatted_note = format_text(user_text, style="rant")
            print("\n--- Generated Note ---")
            print(f"Title: {formatted_note.title}")
            print(f"Note: {formatted_note.note}")
            print(f"Tags: {', '.join(formatted_note.tags)}\n")

            # Save note
            save = input("Do you want to save this note (yes/no)").strip().lower()
            if save=="yes" or save=="y":
                directory, timestamp = create_folder_structure()
                
                save_note(formatted_note, audio_chunks, directory, timestamp)

            # Continue or exit
            choice = input("Would you like to record another note? (yes/no): ").strip().lower()
            if not (choice == "yes" or choice=='y'):
                print("Exiting. Notes are saved in the 'notes/' folder.")
                recorder.shutdown()
                break
        
        except KeyboardInterrupt:
            print("Recording interrupted.")
        finally:
            recorder.shutdown()

def guided_rant():

    while True:
        try:
            directory, timestamp = create_folder_structure()
            audio_callback, audio_chunks = create_audio_callback()

            # Start recorder and attach callback
            recorder = AudioToTextRecorder(
                model="tiny",
                no_log_file=True,
                post_speech_silence_duration=7,
                on_recorded_chunk=audio_callback
            )

            print("Recording... Press Enter to stop.")
            recorder.start()
            input("Press Enter to stop recording...")
            recorder.stop()

            # Get transcription
            user_text = recorder.text()
            print("Transcription: ", user_text)

            # Format and save note
            formatted_note = format_text(user_text, style="rant")
            print("\n--- Generated Note ---")
            print(f"Title: {formatted_note.title}")
            print(f"Note: {formatted_note.note}")
            print(f"Tags: {', '.join(formatted_note.tags)}\n")

            # Save note
            save = input("Do you want to save this note (yes/no)").strip().lower()
            if save=="yes" or save=="y":
                save_note(formatted_note, audio_chunks, directory, timestamp)

            # Continue or exit
            choice = input("Would you like to record another note? (yes/no): ").strip().lower()
            if not (choice == "yes" or choice=='y'):
                print("Exiting. Notes are saved in the 'notes/' folder.")
                recorder.shutdown()
                break
        
        except KeyboardInterrupt:
            print("Recording interrupted.")
        finally:
            recorder.shutdown()

# --- Optional Typing Anywhere Function ---

def process_text(text):
    pyautogui.typewrite(text + " ")

def print_text(text):
    print(text)

def type_anywhere():
    try: 
        print("Wait until it says 'speak now'")
        recorder = AudioToTextRecorder()
        while True:
            recorder.text(process_text)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        recorder.shutdown()

# --- Entry Point ---

if __name__ == "__main__":
    rant()
