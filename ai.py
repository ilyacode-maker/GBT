import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

import os
import asyncio
from datetime import datetime
from log import logText

import log

genai.configure(api_key=os.getenv('API_KEY'))
model = genai.GenerativeModel('gemini-1.5-pro-latest')


def get_response(specifications): #---------------------STILL TO ADD THE PARAMETER OF THE BOOK ONCE GIVEN
    #The book chunk
    bc = open('./testBooks/TheMantle.txt','r')
    txt = bc.read()
    bc.close()
    chat = model.start_chat()
    res = chat.send_message(
        f'''
        Reformulate the following story in {specifications} manner.
        {txt}
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

def create_content(Specifications):
    story = open('./testBooks/TheMantle.txt','r')
    txt = story.read()
    story.close()

    for m in get_response(Specifications):
        txt= txt + m
    logText(txt,'./Log/test_files', data={
        'source': './testBooks/TheMantle.txt',
        'prompt': f' Reformulate the following story in {Specifications} manner.'
    })
    return txt


    