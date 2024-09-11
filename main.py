from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

audio_file= open("audio_files\class2-part1.mp3", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)

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

with open("text_output\\transcription_output_format.txt", "w", encoding='utf-8') as file:
    file.write(response.choices[0].message.content)