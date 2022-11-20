from flask import Flask, jsonify, request
from cloudLib.vision_ai import detectText
from cloudLib.speech_to_text import audio_transcript, audio_transcript_local
from cloudLib.search_by_image import detect_web
from cloudLib.google_search import search
from cloudLib.video_transcriptor import transcribe_video
from idfake_ai.predict import isFake
import requests
import os

app = Flask(__name__)

@app.route("/img", methods=['POST'])
def img():
    request_data = request.get_json()
    url = request_data['img']
    print(url)
    text = detectText(url)
    searchImg = detect_web(url)
    response_ai = "Texto muito pequeno para analise por inteligência artificial"
    pages = []
    if len(text.split()) > 100:
        response_ai = "Fake" if isFake(text) == 1 else "Real"
        pages = search(text)
    return jsonify("\n\n".join([response_ai] + searchImg + pages))

@app.route("/audio", methods=['POST'])
def audio():
    request_data = request.get_json()
    url = request_data['audio']
    result = audio_transcript(url)
    print(result)
    response_ai = isFake(result[0].alternatives[0].transcript)
    print(response_ai)
    return jsonify("Fake" if response_ai == 1 else "Real")

@app.route("/text", methods=['POST'])
def text():
    request_data = request.get_json()
    text = request_data['text']
    print(text)
    response_ai = "Fake" if isFake(text) == 1 else "Real"
    pages = search(text)
    return jsonify("\n\n".join([response_ai] + pages))

@app.route("/video", methods=['POST'])
def video():
    request_data = request.get_json()
    url = request_data['video']
    print(url)
    path = download(url, 'assets/video')
    print(path)
    result = transcribe_video(path)
    response_ai = "Fake" if isFake(result) == 1 else "Real"
    return jsonify(response_ai)

def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
        return file_path
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))
        return None


if __name__ == '__main__':
    app.run()