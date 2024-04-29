from flask import Flask, render_template, request, url_for
from ai import create_content


app = Flask(__name__)

@app.route('/',methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        specs = request.form['specs']
        txt = create_content(specs)
        return render_template('index.html', res=txt)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)