"""
This module takes the specified voice recording - turns it into text 
- summarizes the text into specifed format - then saves it into my notes folder
"""
import os
from datetime import datetime
from openai import OpenAI

# API setup
api_key = os.environ.get('YOUR_API_KEY')
client = OpenAI(api_key=api_key)

# Extraction
audio = open("Recordings\\New Recording 11.mp3", "rb") 

# Transformation
# Convert voice to text
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio
)

# print(transcription.text)

# Summarize text file 

prompt = """
Context: The text being parsed to you is a transcription of an audio file. Audio files can be rambly and lack coherent flow.

Task: I want you to create a few key ideas from the text, keep it simple. I also want you to create a summary of the text, which will most likely have a lot of repeated ideas and words, as transcriptions are rambly in nature. I want you to remove this fluff, clean it up, while still keeping the essence in how I said it.

output: I want you to format your repsonse in markdown. Your should format it like the example below. Include the relevant information under the correct header. Also I want the header to be your best guess at the main theme or main themes of the text

# Header 

## Key Ideas 
-

## Summary 

## Original Transcript


also if I say chatgpt find this quote (or similar), I want you to do your best to find the quote or link to a similar idea that I was talking about. 
If I indicate some kind of structure, eg title of a section or point numbers - do your best to inlcude that formated well in the summary.
"""

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "developer",
            "content": f"{prompt}"
        },
        {
            "role": "user",
            "content": f"{transcription.text}"
        }
    ]
)

print(completion.choices[0].message.content)


# Load
date = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')

md_file = open(f"C:\\Users\\caleb\\OneDrive - Flinders\\Obsidian Vault\\Caleb\\Transcriptions\\{date}.md", "a")
md_file.write(completion.choices[0].message.content)
md_file.close()