import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# Convert MP4 --> MP3: https://www.freeconvert.com/mp4-to-mp3
# Compress MP3: https://www.freeconvert.com/mp3-compressor

classNum = 21
part = 2

audio_file_path = os.path.join("audio_files", f"class{classNum}", f"part{part}.mp3")
transcript_file_path = os.path.join("text_output", f"class{classNum}", f"part{part}-transcript.txt")
formatted_file_path = os.path.join("text_output", f"class{classNum}", f"part{part}-formatted.txt")

audio_file= open(audio_file_path, "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)

with open(transcript_file_path, "w", encoding='utf-8') as file:
    file.write(transcription.text)

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f"""
    I have a chunk of text from a lecture can you format and group the text with relevant bullet points useful for studying.
     Keep as much of the text needed to maintain all information.
     Here is the text. In the response only include relevant text without any extra text.
     
     {transcription.text}
    """}
  ]
)

with open(formatted_file_path, "w", encoding='utf-8') as file:
    file.write(response.choices[0].message.content)