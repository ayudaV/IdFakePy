from __future__ import print_function
from google.cloud import vision
import io
import logging

client = vision.ImageAnnotatorClient()


def detect_text(uri):
    """Detects text in the file."""
    image = vision.Image()
    image.source.image_uri = uri
    response = client.text_detection(image=image)
    if response.text_annotations:
        res: str = response.text_annotations[0].description
        logging.info(f"vision_ai  : detect_text response: {res}")
        return res
    else:
        logging.info(f"vision_ai  : detect_text response: Without text")
        return ""


def detect_text_local(path):
    """Detects text in the file."""

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    if response.text_annotations:
        res: str = response.text_annotations[0].description
        logging.info(f"\nvision_ai  : detect_text_local response:\n{res}")
        return res
    else:
        logging.info(f"\nvision_ai  : detect_text_local response: Without text")
        return ""
