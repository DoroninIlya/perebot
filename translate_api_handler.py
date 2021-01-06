import json
import os

import requests
from dotenv import load_dotenv

import logger

load_dotenv()

TRANSLATION_SERVICE = os.getenv('TRANSLATION_SERVICE')
DETECTION_SERVICE = os.getenv('DETECTION_SERVICE')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
ABBYY_API_TOKEN = os.getenv('ABBYY_API_TOKEN')
TOKEN = os.getenv('YANDEX_TOKEN')
FOLDER_ID = os.getenv('YANDEX_FOLDER_ID')

GOOGLE_BASIC_URL = 'https://translation.googleapis.com/language/translate/v2'
YANDEX_BASIC_URL = 'https://translate.api.cloud.yandex.net/translate/v2'
ABBYY_BASIC_URL = 'https://developers.lingvolive.com/api/v1'


class Translate:
    def google(self, language_pair, text):

        url = GOOGLE_BASIC_URL + '?key=' + GOOGLE_API_KEY
        payload = ({
            'q': [text],
            'target': language_pair[0],
            'source': language_pair[1],
            'format': 'text',
            })
        headers = {
            'Content-Type': 'application/json',
            }

        response = send_post_request(url, payload, headers)

        return ParseTranslation.google(self, response.text)

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

        return send_post_request(url, payload, headers)

    def abbyy(self, language_pair, text):

        is_single_word = len(text.split()) == 1

        if is_single_word:
            logger.info('Перевод слова - используем Abbyy')

            target_language = get_abbyy_language_code(language_pair[0])
            source_language = get_abbyy_language_code(language_pair[1])

            url = ABBYY_BASIC_URL + '/Minicard'
            query_parameters = {
                'text': text,
                'srcLang': source_language,
                'dstLang': target_language,
            }
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + ABBYY_API_TOKEN,
                }

            response = send_get_request(url, query_parameters, headers)

            return ParseTranslation.abbyy(self, response.text)
        else:
            logger.info('Перевод фразы/текста - используем Google')

            return Translate.google(self, language_pair, text)


class ParseTranslation:
    def google(self, text):
        try:
            return json.loads(text)['data']['translations'][0]['translatedText']
        except Exception:
            logger.critical('Парсинг ответа не выполнен')

    def yandex(self, text):
        try:
            return json.loads(text)['translations'][0]['text']
        except Exception:
            logger.critical('Парсинг ответа не выполнен')

    def abbyy(self, text):
        try:
            return json.loads(text)['Translation']['Translation']
        except Exception:
            logger.critical('Парсинг ответа не выполнен')


class Detect:
    def google(self, text):
        url = GOOGLE_BASIC_URL + '/detect' + '?key=' + GOOGLE_API_KEY
        payload = ({
            'q': [text],
            })
        headers = {
            'Content-Type': 'application/json',
            }

        return send_post_request(url, payload, headers)

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

        return send_post_request(url, payload, headers)


class ParseLanguage:
    def google(self, text):
        return json.loads(text)['data']['detections'][0][0]['language']

    def yandex(self, text):
        return json.loads(text)['languageCode']


def send_post_request(url, payload, headers):

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


def send_get_request(url, query_parameters, headers):

    try:
        response = requests.get(url, params=query_parameters, headers=headers)
    except Exception:
        logger.critical('Запрос не выполнен')

    if not response.ok:
        status_code = str(response.status_code)
        response_text = str(response.text)

        logger.critical(f'Пришел ответ с кодом {status_code} и текстом: {response_text}')

        return status_code

    return response


def get_translation(language_pair, text):
    return getattr(Translate(), TRANSLATION_SERVICE)(language_pair, text)


def get_language(text):
    splited_text = text.split(' ')

    short_text = ' '.join(splited_text[:2])

    return getattr(Detect(), DETECTION_SERVICE)(short_text)


def parse_language_response(text):
    return getattr(ParseLanguage(), DETECTION_SERVICE)(text)


def get_abbyy_language_code(language):
    dictionaries = {
        'en': 1033,
        'ru': 1049,
    }

    return dictionaries.get(language)
