from google.cloud import vision
import io
import logging
client = vision.ImageAnnotatorClient()


def vision_detect(image):
    response = client.web_detection(image=image)
    annotations = response.web_detection

    if annotations.pages_with_matching_images:
        logging.info(
            f'search_by_image   : {len(annotations.pages_with_matching_images)} Pages with matching images found:')

        for page in annotations.pages_with_matching_images:
            logging.info(f'search_by_image   : Page url   : {page.url}')
    else:
        logging.info('search_by_image   : Without pages with matching images found.')
    if response.error.message:
        logging.error(
            'search_by_image   : {response.error.message}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors')
        return ["Ocorreu um erro na pesquisa por imagem."]

    if len(annotations.pages_with_matching_images) > 0:
        return [p.url for p in annotations.pages_with_matching_images]
    else:
        return ["Sem resultados na pesquisa por imagem."]


def detect_web(uri):
    """Detects web annotations given an image."""
    image = vision.Image()
    image.source.image_uri = uri
    return vision_detect(image)


def detect_web_local(path):
    """Detects web annotations given an image."""
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    return vision_detect(image)
