from cgi import print_arguments
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import argparse
import logging

# create a argparser


def prepareArgParser():
    arg_parser = argparse.ArgumentParser(
        description='A Twilio Bot for connect the ID:FAKE API and Whatsapp')
    arg_parser.add_argument(
        'url', help='Url used to conect with the ID:FAKE API', nargs='?',  const=1, default='http://127.0.0.1:5000')
    return arg_parser

# parses arguments from argparser


def parseArgs(arg_parser):
    args = arg_parser.parse_args()
    url = args.url
    if url[:-1] != '/':
        url += '/'
    logging.info(url)
    return (url)


app = Flask(__name__)
url = parseArgs(prepareArgParser())


@app.route('/', methods=['POST'])
def idfake():
    r_msg = request.values
    resp = MessagingResponse()
    msg = resp.message()
    idf_r = {}

    # verifica se há algum conteúdo com a mensagem
    if int(r_msg.get('NumMedia', '')) > 0:
        media_url = r_msg.get('MediaUrl0', '')
        media = requests.get(media_url, stream=True)

        logging.info(f"Media url: {media_url}")

        if media.ok:
            media_type = media.headers.get('Content-Type')
            media_type = media_type[media_type.find('/')+1:]
            if media_type == 'jpeg':
                idf_r = requests.post(url + 'img', json={'img': media_url})
            elif media_type == 'ogg':
                idf_r = requests.post(url + 'audio', json={'audio': media_url})
            elif media_type == 'mp4':
                idf_r = requests.post(url + 'video', json={'video': media_url})
        else:
            logging.error(f'Ocoreu um erro, status: {media.status_code}')
            msg.body(
                'Não suportamos este tipo de mídia, tente usar jpeg, ogg e mp4')
            return str(resp)
    else:
        idf_r = requests.post(
            url + 'text', json={'text': r_msg.get('Body', '')})

    if idf_r.status_code == 200:
        try:
            resposta = idf_r.json()
            logging.info(resposta)
            msg.body(resposta)
        except Exception as e:
            logging.info(f'ocorreu um erro. Erro: {e}')
            msg.body('ocorreu um erro, tente novamente ou tente outra imagem')
    else:
        logging.error(f'ocoreu um erro, status: {idf_r.status_code}')
        msg.body('ocorreu um erro, tente novamente')

        logging.info(msg)

    # resposta twilio
    return str(resp)


if __name__ == '__main__':
    logging.info("Iniciando aplicacao na porta 8000")
    app.run(host="localhost", port=8000, debug=True)
