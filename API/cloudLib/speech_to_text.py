# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud import storage
import uuid, os, logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

client = speech.SpeechClient()
config_ogg = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
    sample_rate_hertz=16000,
    language_code="pt-BR",
)

config_wav = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    audio_channel_count=2,
    sample_rate_hertz=44100,
    language_code="pt-BR",
)


def transcribe_audio(uri):
    filename = f'{str(uuid.uuid4())}.ogg'

    # Substituir isto posteriormente
    os.system(f'curl {uri} | gsutil cp - gs://idfake-audiofiles/{filename}')

    audio = speech.RecognitionAudio(uri=f'gs://idfake-audiofiles/{filename}')

    # Detects speech in the audio file
    response = client.recognize(config=config_ogg, audio=audio)
    logging.info(f"speech_to_text   : Audio trancribe done. Response: {response.results}")
    return (response.results)


def transcribe_audio_local(path):
    filename = f'{str(uuid.uuid4())}.wav'

    upload_blob('idfake-audiofiles', path, filename)
    audio = speech.RecognitionAudio(uri=f'gs://idfake-audiofiles/{filename}')

    # Detects speech in the audio file
    operation = client.long_running_recognize(config=config_wav, audio=audio)
    response = operation.result(timeout=90)
    logging.info(f"speech_to_text   : Local audio trancribe done. Response: {response.results}")
    return (response.results)

def transcribe_audio_local_ogg(path):
    filename = f'{str(uuid.uuid4())}.ogg'

    upload_blob('idfake-audiofiles', path, filename)
    audio = speech.RecognitionAudio(uri=f'gs://idfake-audiofiles/{filename}')

    # Detects speech in the audio file
    operation = client.long_running_recognize(config=config_ogg, audio=audio)
    response = operation.result(timeout=90)
    logging.info(f"speech_to_text   : Local audio ogg trancribe done. Response: {response.results}")
    return (response.results)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    logging.info(f"speech_to_text   : File {source_file_name} uploaded to {destination_blob_name}.")
