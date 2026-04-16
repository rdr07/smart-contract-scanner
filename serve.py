from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def files(path):
    return send_from_directory('frontend', path)

if __name__ == '__main__':
    app.run(port=3000)