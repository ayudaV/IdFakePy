import google_custom_search
import os

google = google_custom_search.CustomSearch(apikey=os.environ["GCS_DEVELOPER_KEY"], engine_id=os.environ["GCS_CX"])

def search(text: str):
    if len(text.split()) > 30:
        text = " ".join(text.split()[:30])
        print(text)
    try:
        results = google.search(text)
        print([r.display_url for r in results])
        return ["\n".join([r.title, r.url]) for r in results]
    except:
        return ["Sem resultados na pesquisa por texto."]

