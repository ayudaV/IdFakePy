from flask import Flask, jsonify, request
from cloudLib.vision_ai import detect_text, detect_text_local
from cloudLib.speech_to_text import transcribe_audio
from cloudLib.search_by_image import detect_web, detect_web_local
from cloudLib.google_search import search
from cloudLib.video_transcriptor import transcribe_video
from idfake_ai.predict import isFake
import requests, os, logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)


@app.route("/img", methods=['POST'])
def img():
    logging.info("Main  : Starting image process")
    request_data = request.get_json()
    url = request_data['img']
    try:
        text = detect_text(url)
    except:
        logging.warning("Main  : Redirecting to alternative text detection")
        path = download(url, 'assets/img')
        text = detect_text_local(path)

    pages = search(text) if len(text.split()) >= 5 else []
    if len(text.split()) < 80:
        try:
            search_img = detect_web(url)
        except:
            logging.warning("Main  : Redirecting to alternative image search")
            path = download(url, 'assets/img')
            search_img = detect_web_local(path)
    else:
        search_img = []
    return jsonify("\n\n".join([response_ai(text)] + search_img + pages))


@app.route("/audio", methods=['POST'])
def audio():
    logging.info("Main  : Starting audio process")
    request_data = request.get_json()
    url = request_data['audio']
    logging.info(f"Main  : Audio url: {url}")
    res = transcribe_audio(url)
    texts = [r.alternatives[0].transcript for r in res]
    return jsonify(response_ai(" ".join(texts)))


@app.route("/text", methods=['POST'])
def text():
    logging.info("Main  : Starting text process")
    request_data = request.get_json()
    text: str = request_data['text']
    logging.info(f"Main  : Text lenght: {len(text.split())}")
    pages = search(text) if len(text.split()) >= 5 else []
    return jsonify("\n\n".join([response_ai(text)] + pages))


@app.route("/video", methods=['POST'])
def video():
    logging.info("Main  : Starting video process")
    request_data = request.get_json()
    url = request_data['video']
    logging.info(f"Main  : Video url: {url}")
    path = download(url, 'assets/video')
    res = transcribe_video(path)
    return jsonify(response_ai(res))


def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    # be careful with file names
    filename = url.split('/')[-1].replace(" ", "_")
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        logging.info(f"saving to {os.path.abspath(file_path)}")
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
        return file_path
    else:  # HTTP status code 4XX/5XX
        logging.warning(f"Main   : Download failed: status code {r.status_code}\n{r.text}")
        return None


def response_ai(text: str):
    logging.info(f"Main  : AI text analysis. Text: {text[:50]}...")
    res = "Texto muito pequeno para análise por inteligência artificial! Tamanho minimo: 80 palavras."
    if len(text.split()) > 80:
        res = "Essa notícia parece falsa." if isFake(
            text) == 1 else "Essa notícia parece verdadeira."
    logging.info(f"Main  : AI text analysis. Response: {res}")
    return res


if __name__ == '__main__':
    logging.info("Main  : Starting API on port 5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
