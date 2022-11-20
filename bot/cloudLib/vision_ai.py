from __future__ import print_function
from google.cloud import vision
import io
client = vision.ImageAnnotatorClient()

#image_uri = 'gs://cloud-samples-data/vision/using_curl/shanghai.jpeg'

def detectText(uri):
    image = vision.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)

    return(response.text_annotations[0].description)

def detect_text_local(path):
    """Detects text in the file."""

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return(response.text_annotations[0].description)
