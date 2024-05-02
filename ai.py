import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

import os
import asyncio
import pyttsx3
import io
import epub
import base64
from datetime import datetime

#from log import logText

genai.configure(api_key=os.getenv('API_KEY'))
model = genai.GenerativeModel('gemini-1.5-pro-latest')


def get_response(text,specifications):
    chat = model.start_chat()
    res = chat.send_message(
        f'''
        Reformulate the following story in {specifications} manner.
        {text}
        ''',
        safety_settings={
            #Taking off all restrictions on prompts
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT       : HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH      : HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        },
        stream=True
    )
    try:
        for chunk in res:
            yield chunk.text
    except:
        print(res.candidates)

def create_content(text,Specifications):
    txt = '' #TODO must add Logging of the results, use log.py SMARTLY
    for m in get_response(text,Specifications):
        txt= txt + m
        yield text_to_audio(m)


def text_to_audio(text):
    en = pyttsx3.init()

    audio_holder = io.BytesIO()
    en.save_to_file(audio_holder, text)

    audio_holder.seek(0)
    return audio_holder

def extract_text(epub_file_path):
    try:
        book = epub.open_epub(epub_file_path)
        text = ""

        # Iterate through all the items in the EPUB
        for item_id, item in book.items():
            # Check if the item is HTML content
            if item.media_type == "application/xhtml+xml":
                # Extract text from the HTML content
                text += item.content.decode('utf-8')
        
        #TODO delete the file once it's FULLY used

        return text
    
    except Exception as e:
        return f"Error: {e}"
        