from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/',methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        message  = request.form['prompt']
        return render_template('index.html', res=message)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)