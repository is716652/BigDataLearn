from flask import Flask, send_from_directory
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
FRONT_DIR = os.path.join(ROOT, 'frontend')

app = Flask(__name__, static_folder=os.path.join(FRONT_DIR, 'assets'))

@app.route('/')
def index():
    return send_from_directory(FRONT_DIR, 'index.html')

@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)