from decouple import config
import requests
import json

ELEVENLABS_API_KEY = config("ELEVENLABS_API_KEY")

def send_file_to_elevenlabs(filename, file_path):
    try:
        url      = 'https://api.elevenlabs.io/v1/speech-to-text'
        files    = { 'file': (filename, open(file_path, 'rb'), 'multipart/form-data') }
        data     = { 'model_id': "scribe_v1" }
        headers  = { "xi-api-key" :  ELEVENLABS_API_KEY}
        response = requests.post(url, files = files, data = data, headers=headers)

        json_response = json.loads(response.text)

        return json_response['text']

    except Exception as e:
        print(e)
        return None