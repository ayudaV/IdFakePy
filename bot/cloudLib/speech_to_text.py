# Imports the Google Cloud client library
from google.cloud import speech
import uuid
import os
from google.cloud import storage
client = speech.SpeechClient()

# The name of the audio file to transcribe
#gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"
#gcs_uri = "https://api.twilio.com/2010-04-01/Accounts/ACfb0936b1265a6120b0b5b302c11363af/Messages/MM44f07102fcefba8cb3b0e8fee541e79a/Media/ME5529b7bf9cbfef316e7f2c693b44aef3"
#gcs_uri = "s3-external-1.amazonaws.com/media.twiliocdn.com/ACfb0936b1265a6120b0b5b302c11363af/d25e94cad9674b2dbeedb75c905930dd"

def audio_transcript(uri):
    filename = f'{str(uuid.uuid4())}.ogg'
    
    #Substituir isto posteriormente
    os.system(f'curl {uri} | gsutil cp - gs://idfake-audiofiles/{filename}')

    #upload_blob("idfake-audiofiles",uri,filename)
    # Instantiates a client

    audio = speech.RecognitionAudio(uri=f'gs://idfake-audiofiles/{filename}')

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        sample_rate_hertz=16000,
        language_code="pt-BR",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    return(response.results)

def audio_transcript_local(path):
    filename = f'{str(uuid.uuid4())}.wav'
    
    upload_blob('idfake-audiofiles', path, filename)
    audio = speech.RecognitionAudio(uri=f'gs://idfake-audiofiles/{filename}')

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        audio_channel_count=2,
        sample_rate_hertz=44100,
        language_code="pt-BR",
    )

    # Detects speech in the audio file
    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=90)

    return(response.results)


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )
