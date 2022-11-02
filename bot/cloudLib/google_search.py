import google_custom_search
import os

google = google_custom_search.CustomSearch(apikey=os.environ["GCS_DEVELOPER_KEY"], engine_id=os.environ["GCS_CX"])

results = google.search("Brasil Paralelo")

for result in results:
    # get a title.
    print(result.title)
  
    # get a link.
    print(result.url)
  
    # get a displayLink.
    print(result.display_url)

    # get a htmlTitle.
    print(result.html_title)
  
    # get a snippet.
    print(result.snippet)