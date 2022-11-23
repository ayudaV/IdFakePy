from flask import Flask, jsonify, request
from cloudLib.vision_ai import detectText, detect_text_local
from cloudLib.speech_to_text import audio_transcript
from cloudLib.search_by_image import detect_web, detect_web_local
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
    try:
        text:str = detectText(url)
    except:
        path = download(url, 'assets/img')
        text:str = detect_text_local(path)
    print(text)
    pages = search(text)
    print(len(text.split()))
    searchImg = []
    if len(text.split()) < 80:
        try:
            searchImg = detect_web(url)
        except:
            path = download(url, 'assets/img')
            searchImg = detect_web_local(path)
    print([response_ai(text)] + searchImg + pages)
    return jsonify("\n\n".join([response_ai(text)] + searchImg + pages))

@app.route("/audio", methods=['POST'])
def audio():
    request_data = request.get_json()
    url = request_data['audio']
    res = audio_transcript(url)
    print(res)
    return jsonify(response_ai(res))

@app.route("/text", methods=['POST'])
def text():
    request_data = request.get_json()
    text:str = request_data['text']
    print(text)
    pages = search(text)

    return jsonify("\n\n".join([response_ai(text)] + pages))

@app.route("/video", methods=['POST'])
def video():
    request_data = request.get_json()
    url = request_data['video']
    url = requests.get(url).url
    print(url)
    path = download(url, 'assets/video')
    print(path)
    res = transcribe_video(path)
    return jsonify(response_ai(res))

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

def response_ai(text: str):
    print(text)
    res = f"Texto muito pequeno para análise por inteligência artificial! Tamanho minimo: 80, tamanho atual: {len(text.split())}"
    if len(text.split()) > 80:
        res = "Essa notícia parece falsa." if isFake(text) == 1 else "Essa notícia parece verdadeira."
    print(res)
    return res

if __name__ == '__main__':
    app.run()