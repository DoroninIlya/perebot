import json
import os

from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN = os.getenv('YANDEX_TOKEN')
FOLDER_ID = os.getenv('YANDEX_FOLDER_ID')


def translate_word(word):

    url = 'https://translate.api.cloud.yandex.net/translate/v2/translate'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Api-Key {TOKEN}'}
    payload = {'folder_id': FOLDER_ID, 'texts': [word], 'targetLanguageCode': 'ru'}

    response = requests.post(url, json=payload, headers=headers)

    resp_dict = json.loads(response.text)

    return resp_dict['translations'][0]['text']
