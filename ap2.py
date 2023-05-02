from flask import Flask, render_template, send_from_directory
import os
import time

app = Flask(__name__, template_folder='images')

def get_all_files(path):
    all_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append((file_path, os.path.getmtime(file_path)))
    return all_files

@app.route('/images/<path:filename>')
def send_image(filename):
    images_dir = 'your_images_directory'
    return send_from_directory(images_dir, filename)

@app.route('/')
def list_files():
    webroot_dir = 'your_webroot_directory'
    files = get_all_files(webroot_dir)
    files.sort(key=lambda x: x[1], reverse=True)
    return render_template('index.html', files=files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
