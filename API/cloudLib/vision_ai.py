from __future__ import print_function
from google.cloud import vision
import io
client = vision.ImageAnnotatorClient()

def detectText(uri):
    image = vision.Image()
    image.source.image_uri = uri
    response = client.text_detection(image=image)
    return response.text_annotations[0].description if response.text_annotations else ""

def detect_text_local(path):
    """Detects text in the file."""

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    return response.text_annotations[0].description if response.text_annotations else ""
