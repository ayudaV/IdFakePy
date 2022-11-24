Colégio Técnico de Campinas
Departamento de Processamento de Dados

Documento Descritivo para Execução
ID:FAKE: Ferramenta para auxílio no reconhecimento de Fake News

André Yuhji Terada
Pedro Henrique Perez Dias
Rafael Lacerda Silva

Campinas - SP

O ID:FAKE busca idealizar e desenvolver uma ferramenta que possa ser utilizada como auxílio no combate à disseminação de notícias falsas na internet, que vem afetando desde o debate político nacional e internacional, até a saúde dos brasileiros. O projeto tem como base o uso de uma inteligência artificial capaz de avaliar a probabilidade de uma notícia se enquadrar como fake news. Em cima dessa tecnologia, desenvolvemos uma aplicação para WhatsApp que recebe mensagens em diversas formas de mídia, as converte para texto, realiza a análise da mensagem e retorna qual a probabilidade da mensagem ser uma notícia falsa. As funcionalidades já desenvolvidas apresentaram uma boa acurácia na transcrição para texto, e os testes com a inteligência artificial mostraram resultados promissores. Junto com a acessibilidade e praticidade fornecida pelo WhatsApp, é possível afirmar que o projeto desenvolvido possui grande potencial no combate à desinformação na internet.

Para o desenvolvimento desse projeto, foram desenvolvidas duas partes: um ‘bot’ para respostas automáticas e uma API que fará a comunicação entre o ‘bot’ e os serviços onlines. Ambos os componentes foram desenvolvidos na linguagem Python.

Para a execução do código do bot, primeiramente é necessária a criação de uma conta na plataforma da Twilio para hospedar seu bot. Isso pode ser feito através deste link: . A plataforma permite o uso de um sandbox para desenvolvimento, sem custo. O código pode ser testado através do número de telefone do sandbox. O tutorial utilizado para criação do bot na Twilio pode ser encontrado aqui: https://www.twilio.com/blog/criar-um-chatbot-para-whatsapp-com-python-flask-e-twilio

pip install flask twilio

Após isso, execute o arquivo main.py localizado no diretório /BOT e hospede a porta 8000 na web. Este processo pode ser feito através do ngrok, ou servidores como AWS ou Heroku. O arquivo main.py aceita como paremetro a url da ID:FAKE API, caso não seja passado, ela usará a porta 5000 do localhost.

Para a execução do código da API, primeiramente acesse a pasta ‘API’ do Github. 
Em seguida será necessário fazer a instalação dos pacotes de Python utilizados. 
Para isso, rode os comandos:

pip install scikit-learn flask opencv-python moviepy ffmpeg-python 
pip install google-custom-search google-cloud-speech google-cloud-vision google-cloud-videointelligence google-cloud-storage 

Também é necessário instalar a ferramenta do ffmpeg, que fará o recorte dos keyframes dos vídeos recebidos. Para isso, rode no terminal Linux:

sudo apt install ffmpeg

Caso o sistema operacional seja Windows, siga o tutorial indicado em: https://phoenixnap.com/kb/ffmpeg-windows


Além disso, é necessário ter uma conta na Google Cloud e, posteriormente, ativar as APIs Vision AI, Custom Search e Speech-To-Text para o projeto. Para utilizar as APIs do Google, primeiro você deve criar uma conta na plataforma google cloud e após isso criar um projeto com faturamento ativado. Para mais detalhes acesse este tutorial. 

As APIs da Google precisam de identificações, para evitar colocá-las no código e causar riscos de segurança, você pode utilizar a GCloud para armazenar suas credenciais. Veja isso em: https://googleapis.dev/python/google-api-core/latest/auth.html.

Para rodar, entre no diretório “/API” e execute o arquivo ‘main.py’.

Para realizar o treinamento da I.A utilizada no projeto, rode os comandos a seguir dentro do diretório “/AI”: 

git clone https://github.com/roneysco/Fake.br-Corpus.git

python reduce.py Fake.br-Corpus/full_texts

python extract.py reduced_texts

python classify.py texts.csv

python predict.py idFake_model.pkl test
