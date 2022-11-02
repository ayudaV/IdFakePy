# Imports the Google Cloud client library
from google.cloud import speech

# The name of the audio file to transcribe
gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"
gcs_uri = "https://api.twilio.com/2010-04-01/Accounts/ACfb0936b1265a6120b0b5b302c11363af/Messages/MM44f07102fcefba8cb3b0e8fee541e79a/Media/ME5529b7bf9cbfef316e7f2c693b44aef3"
gcs_uri = "gs://idfake-audiofiles/test-sample.ogg"

def transcribeText(uri):
    # Instantiates a client
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="pt-BR",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    return(response.results)
        
print(transcribeText(gcs_uri))