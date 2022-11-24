import google_custom_search
import os, logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)
google = google_custom_search.CustomSearch(
    apikey=os.environ["GCS_DEVELOPER_KEY"], engine_id=os.environ["GCS_CX"])


def search(text: str):
    if len(text.split()) > 30:
        text = " ".join(text.split()[:30])
    try:
        results = google.search(text)
        logging.info(f'google_search    : {len(results)} Pages with matching images found:')

        for page in results:
            logging.info(f'google_search    : Page url   : {page.url}')
        return ["\n".join([r.title, r.url]) for r in results]
    except:
        logging.info('google_search     : Without pages with matching images found.')
        return ["Sem resultados na pesquisa por texto."]
