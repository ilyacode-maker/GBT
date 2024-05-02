from flask import Flask, render_template, request, url_for, Response, send_file
from flask_socketio import SocketIO, send
from ai import create_content, extract_text
import base64


import time
import asyncio

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/',methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        message  = request.get_json()["Chunk"]
        return render_template('index.html', res=message)
    else:
        return render_template('index.html')

@app.route("/audio", methods = ['GET','POST'])
def handleAudio():
    CHUNK_SIZE = 1024
    END_SIGNATURE = b'\x01\x02\x03\x04\x05\x06\x07\x08'
   
    AudioFiles = []
    
    def generate():
        time.sleep(1)
        i = 0
        while i < len(AudioFiles):
            file = open(AudioFiles[i],'rb')
            i += 1
            while True:
                file_chunk = file.read(CHUNK_SIZE)
                if not file_chunk:
                    yield END_SIGNATURE
                    time.sleep(.2)
                    break
                yield file_chunk
            file.close()

    
    return Response(generate(), mimetype="application/octet-stream")

#for the file upload
@socketio.on('upload_epub')
def handleFile(file, specifications):
    with open('uploaded_epub.epub', 'wb') as f:
            f.write(base64.b64decode(file['data'].split(",")[1]))
        
    # Extract text from the epub file
    text = extract_text('uploaded_epub.epub')
    for i in create_content(text,specifications):
        send(i)
    END_SIGNATURE = b'\x01\x02\x03\x04\x05\x06\x07\x08'
    send(END_SIGNATURE)

@socketio.on('message')
def handleFile(message, specifications):
    #message is the name of the book + the author
    for i in create_content(message,specifications):
        send(i)
    END_SIGNATURE = b'\x01\x02\x03\x04\x05\x06\x07\x08'
    send(END_SIGNATURE)


if __name__ == '__main__':
    socketio.run(app, debug=True)