from flask import Flask, render_template_string
import os

app = Flask(__name__)

def get_all_files(path):
    all_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append((file_path, os.path.getmtime(file_path)))
    return all_files

@app.route('/')
def list_files():
    webroot_dir = 'your_webroot_directory'
    files = get_all_files(webroot_dir)
    files.sort(key=lambda x: x[1], reverse=True)

    template = '''
    <!doctype html>
    <html>
        <head>
            <title>ファイル一覧</title>
        </head>
        <body>
            <h1>更新日時順のファイル一覧</h1>
            <ul>
                {% for file in files %}
                    <li>
                        {% if file[0].lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')) %}
                            <img src="{{ file[0] }}" alt="{{ file[0] }}" width="100">
                        {% else %}
                            {{ file[0] }}
                        {% endif %}
                    </li>
                {% endfor %}
            </ul>
        </body>
    </html>
    '''
    return render_template_string(template, files=files)

if __name__ == '__main__':
    app.run(debug=True)
