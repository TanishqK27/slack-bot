from flask import Flask, request, jsonify
from pyngrok import ngrok
import os

app = Flask(__name__)

@app.route('/slack/slash-command', methods=['POST'])
def slash_command():
    return jsonify({
        "response_type": "in_channel",
        "text": "Hello, World!"
    }), 200

def start_ngrok():
    url = ngrok.connect(5000).public_url
    print(f' * Tunnel URL: {url}')

if __name__ == "__main__":
    start_ngrok()
    app.run(port=5000)