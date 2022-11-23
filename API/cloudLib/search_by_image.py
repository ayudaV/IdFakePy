from google.cloud import vision
import io
client = vision.ImageAnnotatorClient()

def detect_web(uri):
    """Detects web annotations given an image."""

    image = vision.Image()
    image.source.image_uri = uri

    response = client.web_detection(image=image)
    annotations = response.web_detection
    
    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images found:'.format(
            len(annotations.pages_with_matching_images)))

        for page in annotations.pages_with_matching_images:
            print('\n\tPage url   : {}'.format(page.url))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
        
    if len(annotations.pages_with_matching_images) > 0:
        return [p.url for p in annotations.pages_with_matching_images]
    else:
        return ["Sem resultados na pesquisa por imagem."]

def detect_web_local(path):
    """Detects web annotations given an image."""
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content = content)

    response = client.web_detection(image=image)
    annotations = response.web_detection
    
    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images found:'.format(
            len(annotations.pages_with_matching_images)))

        for page in annotations.pages_with_matching_images:
            print('\n\tPage url   : {}'.format(page.url))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
        
    if len(annotations.pages_with_matching_images) > 0:
        return [p.url for p in annotations.pages_with_matching_images]
    else:
        return ["Sem resultados na pesquisa por imagem."]
