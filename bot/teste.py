from flask import Flask, jsonify, request
import requests
from cloudLib.vision_ai import detectText
from cloudLib.speech_to_text import transcribeText

app = Flask(__name__)


@app.route("/img", methods=['POST'])
def img():
    request_data = request.get_json()
    url = request_data['url']
    response = detectText(url)
    print(response)
    return jsonify(response)

@app.route("/audio", methods=['POST'])
def audio():
    request_data = request.get_json()
    url = request_data['url']
    response = transcribeText(url)
    print(response)
    return jsonify(response)


if __name__ == '__main__':
    app.run()