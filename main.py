import os
import webbrowser
import pandas as pd
from flask import Flask, render_template, jsonify, request, redirect, send_file, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'download'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return redirect(url_for('all'))

@app.route('/all')
def all():
    downloads = os.listdir('download')
    return render_template('all.html', filenames=downloads)


@app.route('/preview/<string:filename>')
def preview(filename=None):
    downloads = os.listdir('download')
    if not filename or filename not in downloads:
        return render_template('404.html'), 404
    else:
        format = filename.split('.')[1]
        if format == 'csv':
            table = pd.read_csv(f"download/{filename}", keep_default_na=False).to_html(index=False)
        elif format == 'xlsx':
            table = pd.read_excel(f"download/{filename}", keep_default_na=False).to_html(index=False)
        else:
            table = "暫時不支援此檔案類型"
        return render_template('preview.html', table=table, filename=filename)


@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('files')
    
    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return redirect(url_for('all'))


@app.route('/download/<string:filename>')
def download(filename=None):
    downloads = os.listdir('download')
    if not filename or filename not in downloads:
        return render_template('404.html'), 404
    else:
        return send_file(f"download/{filename}")


@app.route('/delete/<string:filename>')
def delete(filename=None):
    downloads = os.listdir('download')
    if filename and filename in downloads:
        os.remove(f'download/{filename}')
    return redirect(url_for('all'))


@app.route('/versions')
def versions():
    return render_template('versions.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # app.debug = True
    webbrowser.open("http://127.0.0.1:3000/all")
    app.run(port=3000)
