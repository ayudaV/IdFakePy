from cgi import print_arguments
from flask import Flask, request
import requests, time
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/idfake', methods=['POST'])
def img():
    r_msg = request.values
    resp = MessagingResponse()
    msg = resp.message()
    idf_r = {}
    url = 'https://0baf-177-194-71-96.ngrok.io/'
    
    # verifica se há algum conteúdo com a mensagem
    if int(r_msg.get('NumMedia', '')) > 0:
        media_url = r_msg.get('MediaUrl0', '')
        media = requests.get(media_url, stream=True)
        
        print(media_url)
        #time.sleep(3)
        
        if media.ok:
            media_type = media.headers.get('Content-Type')
            media_type = media_type[media_type.find('/')+1:]
            if media_type == 'jpeg':
                idf_r = requests.post(url + 'img',json = { 'img' : media_url })
            elif media_type == 'ogg':
                idf_r = requests.post(url + 'audio',json = { 'audio' : media_url })
            elif media_type == 'mp4':
                idf_r = requests.post(url + 'video',json = { 'video' : media_url })
        else:
            print('ocoreu um erro, status', media.status_code)
            msg.body('Não suportamos este tipo de mídia, tente usar jpeg, ogg e mp4')
            return str(resp)
    else:
        idf_r = requests.post(url + 'text',json = {'text': r_msg.get('Body', '')})
    
    if idf_r.status_code == 200:
        #print(idf_r.json())
        try:
            resposta = idf_r.json()
            print(resposta)
            msg.body(resposta)
        except:
            print('ocorreu um erro')
            msg.body('ocorreu um erro, tente novamente ou tente outra imagem')
    else:
        print('ocoreu um erro, status', idf_r.status_code)
        msg.body('ocorreu um erro, tente novamente')

        print(msg)
    
    #resposta twilio
    return str(resp)
                
if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)