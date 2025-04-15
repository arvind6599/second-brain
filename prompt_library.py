
promptDict = {
            "rant":""""Below is an unedited personal transcript. Convert it into a clear, engaging, and readable journal entry. Structure it using a brief title, date placeholder, paragraphs or bullet points where necessary, and highlight key reflective insights. Preserve as much of the original voice, style, wording, repetitions, and emotional intensity as possible. Do not significantly alter the meaning or coherence; if certain parts are repetitive or unclear, keep them intact or lightly restructure only for readability, always maintaining the speaker’s original essence.
            Transcript: {text}
            Output:""",

            "base":""" You are an AI-assistant. Please follow these guidelines:
            1. Note: Make the transcript text more coherent and fix grammatical issues. Overall make it more readable.
            2. Tags: Output relevant tags for the input transcript which cover generic topics related to the transcript.
            3. Title: Generate a title for the input transcript which briefly summarizes it with a few words.

            Transcript: {text}

            Note structure: 

            json```
            Title: str
            Note: str
            Tags: List[str]
            ```
            Output:
            """,

            "noteTaker":
                        """- Reformat the user message.
                        - Structure it for effective note-taking
                        - Ensure that key-points, ideas or actions are clearly highlighted.
                        - Check for correct grammar and punctuation.
                        - Keep the tone the same as given.
                        - Use as much of the original text as possible
                        - Reply with just the reformatted text

                        User Message:
                        {text}

                        Output:
                        """,


            "titlePrompt":
                        """Respond with a short title not exceeding 8 words for the following text: {text}.""",

            "tagPrompt": 
                        """Given the following text: {text}, choose the most appropriate tags from the following list: {tags}
                        """
}


EXAMPLE1 = """
    Okay, so here we go. Today was... I don’t even know where to start. Like, I knew traveling on a budget would be tough,but Barcelona is testing me in ways I did NOT sign up for.

    First off, breakfast. I thought I was being clever, grabbing a €2 croissant and coffee combo from some corner café. But, surprise! The croissant was basically air wrapped in sadness, and the coffee? If you can even call it that. It tasted like regret. I miss my instant coffee back home. Who even am I?!

    Then I tried to do the whole "explore the city on foot" thing. I mean, who needs public transport when you’ve got legs, right? WRONG. My legs are now noodles, thank you very much. I walked from my hostel near La Rambla to Park Güell because, you know, Google Maps said it was only like 45 minutes. Lies. It felt like I was trekking to Mordor. And when I got there? Oh, the views are nice, sure, but they charge you to get into the cool part of the park. What?! Gaudí must be rolling in his grave. Or maybe he’s laughing. I wouldn’t blame him.

    Lunchtime was another saga. Found this “authentic” tapas bar, thinking I’d finally hit the jackpot. Nope. Paid €12 for three pieces of bread with random stuff on top. A bit of ham here, some kind of fish paste there, and... an olive. Just one. I think they expect you to cry into your plate to add salt to the flavor.

    Also, what’s with all the pickpocket warnings? I swear every two minutes someone’s yelling, “Watch your bag!” Like, I get it. I’m clutching my backpack like it’s my firstborn. Chill.

    Oh, and the Sagrada Família. It’s stunning, don’t get me wrong, but I thought, "Hey, I’ll just admire it from the outside, save some cash." Guess what? Even just standing there, I got roped into buying some cheesy souvenir from a street vendor. It’s a mini Sagrada Familia, made of plastic, and I already hate it. But it’s in my bag now, so... yay memories?

    Dinner. Oh, dinner. Supermarkets are my new best friend, apparently. Grabbed a baguette, some cheese, and a carton of wine because I’m that person now. Ate it sitting on some random bench while watching happy tourists at fancy restaurants. Honestly, though, the wine was okay. Cheap but okay. Silver lining?

    By the end of the day, I was so tired I didn’t even bother with the hostel social thing. Everyone’s out at clubs or whatever, and I’m here, in bed, writing this. My feet hurt, my wallet is crying, but hey, at least I’m in Barcelona, right? Ugh. Tomorrow better redeem itself."""



title_example="""
                        Title:
                        
                        Example Usage:
                        
                        Input Text:
                        "Today’s meeting was a bit chaotic. First, we discussed the budget for the new project but didn’t finalize anything. Sarah mentioned some issues with the timeline and requested an extension. Meanwhile, Mike brought up marketing strategies, but it was clear no one had prepared, so it was left for the next meeting. We also talked about hiring interns for the summer, but again, no decision was made. Overall, lots of ideas but not much progress."

                        AI Response (as Title Generator):

                        Title: Unproductive & Chaotic Meeting """


summary_example = """Example Usage 1:
                        Input Text:
                        "Today’s meeting was a bit chaotic. First, we discussed the budget for the new project but didn’t finalize anything. Sarah mentioned some issues with the timeline and requested an extension. Meanwhile, Mike brought up marketing strategies, but it was clear no one had prepared, so it was left for the next meeting. We also talked about hiring interns for the summer, but again, no decision was made. Overall, lots of ideas but not much progress."

                        AI Response (as Note-Taker):

                        Discussion Points:
                        - Budget for new project discussed but not finalized.
                        - Timeline issues raised by Sarah; extension requested.
                        - Marketing strategies brought up by Mike; deferred due to lack of preparation.
                        - Intern hiring discussed for summer; no decisions made.


                        Example Usage 2:

                        Input Text:
                        "Ah, Japan. I can still remember the trip like it was yesterday. What stood out the most—aside from the temples and all that history—was the food. Sushi, oh my goodness. The real deal over there is nothing like the stuff you get back home. I remember sitting at this tiny sushi bar, the chef slicing fish with this precision that felt almost meditative. There’s something so simple yet perfect about it—just vinegared rice, fresh seafood, and maybe a touch of wasabi. Oh, and they always serve it with pickled ginger and soy sauce; it’s like a little ritual. Honestly, I didn’t even like wasabi before, but something about the way they do it there just made it all click. I could feel how much respect they have for the craft. It’s not just food; it’s an art form. I think I even overheard someone say that people travel across the globe just for a plate of authentic sushi. Yeah, I totally get it now."

                        AI Response (as Note-Taker):

                        Cultural Significance:  
                        - Japan is renowned for its rich cultural heritage, including its traditional cuisine.

                        About Sushi:  
                        - Sushi is a popular dish made of vinegared rice paired with ingredients such as seafood, vegetables, or tropical fruits.  
                        - It is commonly served with pickled ginger, wasabi, and soy sauce.

                        Art of Sushi-Making:  
                        - Sushi preparation is considered a revered skill in Japan.  
                        - Master chefs dedicate years to perfecting the craft, elevating it to an art form.

                        Tourism Appeal:  
                        - Many travelers visit Japan specifically to experience authentic sushi made by expert chefs.
"""