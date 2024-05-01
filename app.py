from flask import Flask, render_template, request, Response, jsonify
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
    #Response can be of type File or Text depending on the content
    if (request.form.get("Type") == "File"):
        #---Getting The Ebook
        #-------Checking For Parameter/Existence Of File
        if 'Content' not in request.files:
            return jsonify({'error': 'No file parameter in the request'}), 400
        
        file = request.files['Content']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        #-------Saving File in ./uploads/
        save_path = './uploads/'
        file.save(save_path + file.filename)

        #---Ebook Treatment



    else : 

        #---Title Treatment

        print(request.form.get("Content"))

    #Reformulating the text
    #...
    #time.sleep(5)
    #...

    #Sending Data Back
    CHUNK_SIZE = 1024
    END_SIGNATURE = b'\x01\x02\x03\x04\x05\x06\x07\x08'
    AudioFiles = ['./out002.mp3','./out003.mp3','./out004.mp3','./out005.mp3','./out006.mp3','./out007.mp3']
    
    #------Returns Chunks of The Audios
    def generate():
        #Simulating late Response
        # time.sleep(3)
        i = 0
        while i < len(AudioFiles):
            #Simulating different cases of Late Response
            # if (i == 1) :
            #     time.sleep(10)
            # if (i == 4):
            #     time.sleep(10)
            file = open(AudioFiles[i],'rb');
            i += 1
            while True:
                file_chunk = file.read(CHUNK_SIZE)
                if not file_chunk:
                    yield END_SIGNATURE
                    #Time To Split the requests in the client-side
                    time.sleep(.1)
                    break;
                yield file_chunk
            file.close();

    
    return Response(generate(), mimetype="application/octet-stream")


if __name__ == '__main__':
    app.run(debug=True)