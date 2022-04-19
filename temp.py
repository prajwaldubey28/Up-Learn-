from flask import Flask, render_template, request
from werkzeug.utils import redirect, secure_filename

import os
import secrets

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploadfolder'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file_():
    if request.method == 'POST':
        for f in request.files.getlist('file'):
            name = f.filename
            extension = name.split(".")[-1]
            filename = secrets.token_hex(8) + "." + extension
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect("/upload")

if __name__ == '__main__':
    app.run(debug=True)
