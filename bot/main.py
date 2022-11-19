from flask import Flask, jsonify, request
from cloudLib.vision_ai import detectText
from cloudLib.speech_to_text import transcribeText
from ai.predict import predict

app = Flask(__name__)


@app.route("/img", methods=['POST'])
def img():
    request_data = request.get_json()
    url = request_data['image']
    response = detectText(url)
    print(response)
    return jsonify(response)

@app.route("/audio", methods=['POST'])
def audio():
    request_data = request.get_json()
    url = request_data['audio']
    response = transcribeText(url)
    print(response)
    return jsonify(response)

@app.route("/text", methods=['POST'])
def text():
    request_data = request.get_json()
    text = request_data['text']
    response = predict(text)
    print(response)
    return jsonify(response)

if __name__ == '__main__':
    app.run()