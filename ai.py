import google.generativeai as genai
import os
from datetime import datetime

genai.configure(api_key=os.getenv('API_KEY'))
model = genai.GenerativeModel('gemini-pro')

def get_response(book_chunk, specifications):
    res = model.generate_content(f'Give a reformulation of the {book_chunk} in a manner {specifications}')
    file = open('./test_file/test1.txt', 'w')
    t = os.getenv('TestNum')
    n = int(t) + 1
    os.environ['TestNum'] = str(n)
    file.write(f'Test{n} \t {datetime.now()} \n {book_chunk} \t {specifications}\n')
    file.write(res.text)

get_response('The idiot by fyodor desteovsky', 'short, funny and simple')

