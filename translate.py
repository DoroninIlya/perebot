import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('YANDEX_TOKEN')
FOLDER_ID = os.getenv('YANDEX_FOLDER_ID')

BASIC_URL = 'https://translate.api.cloud.yandex.net/translate/v2'
HEADERS = ({
    'Content-Type': 'application/json',
    'Authorization': f'Api-Key {TOKEN}',
    })
FIRST_LANG = 'en'
SECOND_LANG = 'ru'


def translate_word(word):

    detected_language = detect_language(word)

    if detected_language == SECOND_LANG:
        language_codes = [FIRST_LANG, SECOND_LANG]
    else:
        language_codes = [SECOND_LANG, FIRST_LANG]

    url = BASIC_URL + '/translate'
    headers = HEADERS
    payload = ({
        'folder_id': FOLDER_ID,
        'texts': [word],
        'targetLanguageCode': language_codes[0],
        'sourceLanguageCode': language_codes[1],
        })

    response = requests.post(url, json=payload, headers=headers)

    resp_dict = json.loads(response.text)

    return resp_dict['translations'][0]['text']


def detect_language(word):

    url = BASIC_URL + '/detect'
    headers = HEADERS
    payload = ({
        'folder_id': FOLDER_ID,
        'languageCodeHints': ['ru', 'en'],
        'text': word,
        })

    response = requests.post(url, json=payload, headers=headers)

    resp_dict = json.loads(response.text)

    return resp_dict['languageCode']
