import json
import os

import requests
from dotenv import load_dotenv

import logger

load_dotenv()

TRANSLATE_SERVICE = os.getenv('TRANSLATE_SERVICE')
API_KEY = os.getenv('GOOGLE_API_KEY')
TOKEN = os.getenv('YANDEX_TOKEN')
FOLDER_ID = os.getenv('YANDEX_FOLDER_ID')

GOOGLE_BASIC_URL = 'https://translation.googleapis.com/language/translate/v2'
YANDEX_BASIC_URL = 'https://translate.api.cloud.yandex.net/translate/v2'


class Translate:
    def google(self, language_pair, text):
        url = GOOGLE_BASIC_URL + '?key=' + API_KEY
        payload = ({
            'q': [text],
            'target': language_pair[0],
            'source': language_pair[1],
            'format': 'text',
            })
        headers = {
            'Content-Type': 'application/json',
            }

        return send_request(url, payload, headers)

    def yandex(self, language_pair, text):
        url = YANDEX_BASIC_URL + '/translate'
        payload = ({
            'folder_id': FOLDER_ID,
            'texts': [text],
            'targetLanguageCode': language_pair[0],
            'sourceLanguageCode': language_pair[1],
            })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Api-Key {TOKEN}',
            }

        return send_request(url, payload, headers)


class ParseTranslation:
    def google(self, text):
        return json.loads(text)['data']['translations'][0]['translatedText']

    def yandex(self, text):
        return json.loads(text)['translations'][0]['text']


class Detect:
    def google(self, text):
        url = GOOGLE_BASIC_URL + '/detect' + '?key=' + API_KEY
        payload = ({
            'q': [text],
            })
        headers = {
            'Content-Type': 'application/json',
            }

        return send_request(url, payload, headers)

    def yandex(self, text):
        url = YANDEX_BASIC_URL + '/detect'
        payload = ({
            'folder_id': FOLDER_ID,
            'languageCodeHints': ['ru', 'en'],
            'text': text,
            })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Api-Key {TOKEN}',
            }

        return send_request(url, payload, headers)


class ParseLanguage:
    def google(self, text):
        return json.loads(text)['data']['detections'][0][0]['language']

    def yandex(self, text):
        return json.loads(text)['languageCode']


def send_request(url, payload, headers):
    try:
        response = requests.post(url, json=payload, headers=headers)
    except Exception:
        logger.critical('Запрос не выполнен')

    try:
        response = requests.post(url, json=payload, headers=headers)
    except Exception:
        logger.critical('Запрос не выполнен')

    if not response.ok:
        status_code = str(response.status_code)
        response_text = str(response.text)

        logger.critical(f'Пришел ответ с кодом {status_code} и текстом: {response_text}')

        return status_code

    return response


def get_translation(language_pair, text):
    return getattr(Translate(), TRANSLATE_SERVICE)(language_pair, text)


def parse_translation_response(text):
    return getattr(ParseTranslation(), TRANSLATE_SERVICE)(text)


def get_language(text):
    return getattr(Detect(), TRANSLATE_SERVICE)(text)


def parse_language_response(text):
    return getattr(ParseLanguage(), TRANSLATE_SERVICE)(text)
