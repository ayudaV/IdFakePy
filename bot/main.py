from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    print(request.values)
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'frase' in incoming_msg:
        # retorne uma citação
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'Não consegui recuperar uma citação neste momento, desculpe.'
        msg.body(quote)
        responded = True
    if 'gato' in incoming_msg or 'gata' in incoming_msg:
        # retorne uma foto de gato
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body('Só conheço frases e gatos famosos, desculpe!')
    return str(resp)

@app.route('/img', methods=['POST'])
def img():
    r_msg = request.values
    resp = MessagingResponse()
    msg = resp.message()
    print(r_msg)
    responded = False
    if int(r_msg.get('NumMedia', '')) > 0:
        media_url = r_msg.get('MediaUrl0', '')
        print(media_url)
        downloadMedia(media_url)
        msg.media(media_url)
        msg.body('gostoso!')
        responded = True
    if not responded:
        msg.body('mande um gostoso!')
    return str(resp)

def downloadMedia(media_url):
    media = requests.get(media_url, stream=True)
    media_type = media.headers.get('Content-Type')
    media_type = media_type[media_type.find('/')+1:]
    if not media.ok:
        print('ocoreu um erro, status', media.status_code)
    else:
        with open('midia' + '.' + media_type, 'wb') as imagem:
            for dado in media.iter_content(1024):
                if not dado:
                    break
                
                imagem.write(dado)
        
    
        

if __name__ == '__main__':
   app.run()