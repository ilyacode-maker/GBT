from flask import Flask, render_template, request, Response, send_file
import time

app = Flask(__name__)

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
    AudioFiles = ['./out002.mp3','./out003.mp3','./out004.mp3','./out005.mp3','./out006.mp3','./out007.mp3']
    def generate():
        time.sleep(1)
        i = 0
        while i < len(AudioFiles):
            file = open(AudioFiles[i],'rb');
            i += 1
            while True:
                file_chunk = file.read(CHUNK_SIZE)
                if not file_chunk:
                    yield END_SIGNATURE
                    time.sleep(.2)
                    break;
                yield file_chunk
            file.close();

    
    return Response(generate(), mimetype="application/octet-stream")


if __name__ == '__main__':
    app.run(debug=True)