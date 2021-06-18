import os
import wave

from multiprocessing import Pool
from google.cloud import storage
from google.cloud import speech

from constants import BUCKET, AUDIO_DIR, TEXT_DIR

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './credentials.json'

speech_client = speech.SpeechClient()
storage_client = storage.Client()


def upload_blob(local_file_path, file_name):
    """ Upload file """
    bucket = storage_client.get_bucket(BUCKET)
    blob = bucket.blob(file_name)
    blob.upload_from_filename(local_file_path)


def delete_blob(file_name):
    """ Deletes a blob from the bucket. """
    bucket = storage_client.get_bucket(BUCKET)
    blob = bucket.blob(file_name)
    blob.delete()


def framerate_and_channels(local_file_path):
    """ Get the frame rate and number of channels """
    with wave.open(local_file_path, "rb") as wave_file:
        framerate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return framerate, channels


def transcribe(local_file_path, file_name):
    framerate, channels = framerate_and_channels(local_file_path)

    if channels > 1:
        raise Exception("Too many channels")

    gcs_uri = f'gs://{BUCKET}/{file_name}'

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=framerate,
        language_code='en-US',
        model='video'
    )

    operation = speech_client.long_running_recognize(
        {"config": config, "audio": audio})
    response = operation.result()

    sentences = [
        result.alternatives[0].transcript.lstrip() for result in response.results]

    return sentences


def transcribe_wrapper(i, local_file_path, file_name):
    print(f'Started Transcribing File #{i}: {file_name}')

    try:
        sentences = transcribe(local_file_path, file_name)
        file_name = file_name.split('.')[0]

        file = open(f'{TEXT_DIR}/{file_name}.txt', 'w')
        file.write(file_name + '\n\n')

        for sentence in sentences:
            file.write(sentence + '\n\n')

        file.close()

    except Exception as e:
        print(f'FAILED {file_name}')
        print(e)

    print(f'Finished Transcribing File #{i}: {file_name}')


def merge(output_file_name='output.txt'):
    """ Create a single output file using TEXT_DIR """
    output = open(output_file_name, 'w')

    for file_name in os.listdir(TEXT_DIR):
        text_file = open(f'{TEXT_DIR}/{file_name}', 'r')
        text = text_file.read()
        text_file.close()

        output.write(text)

    output.close()


def audio_upload_cloud():
    """ Upload audio to GCP """
    for i, audio in enumerate(os.listdir(AUDIO_DIR)):
        print(f'Uploading File #{i} to GCP: {audio}')
        upload_blob(f'{AUDIO_DIR}/{audio}', audio)


def audio_delete_cloud():
    """ Delete audio in GCP """
    for i, audio in enumerate(os.listdir(AUDIO_DIR)):
        print(f'Removing File #{i} from GCP: {audio}')
        upload_blob(f'{AUDIO_DIR}/{audio}', audio)


def audio_to_text():
    """ Transcribes audio to text """
    print('------------ UPLOADING AUDIO TO GCP ------------')
    audio_upload_cloud()

    print('------------ CONVERTING AUDIO TO TEXT ------------')
    # Transcription
    with Pool(8) as p:
        files = [(i+1, f'{AUDIO_DIR}/{audio}', audio)
                 for i, audio in enumerate(os.listdir(AUDIO_DIR))]

        p.starmap(transcribe_wrapper, files)

    merge()
