import json
import os

import requests
from dotenv import load_dotenv

import logger

load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')

BASIC_URL = 'https://translation.googleapis.com/language/translate/v2'
FIRST_LANG = 'en'
SECOND_LANG = 'ru'
WRONG_TEXT_ERROR = (
    'Вы ввели не текст. Для перевода вам необходимо ' +
    'ввести текст на английском или русском языке'
    )
UNSPECIFIED_ERROR = (
    'Что-то пошло не так... Кажется бот временно не работает. ' +
    'Попробуйте еще раз позже'
    )

headers = {
    'Content-Type': 'application/json'
    }


def translate_text(text, language):

    language_pair = get_language_pair(language)

    url = BASIC_URL + '?key=' + API_KEY
    payload = ({
        'q': [text],
        'target': language_pair[0],
        'source': language_pair[1],
        })

    logger.info('Делаем запрос на перевод слова')

    try:
        response = requests.post(url, json=payload, headers=headers)
    except Exception:
        logger.critical('Запрос на перевод не выполнен')

    if not response.ok:
        status_code = str(response.status_code)

        logger.critical(f'В ответе на запрос вернулась ошибка: {status_code}')

        return status_code

    try:
        translated_text = json.loads(response.text)['data']['translations'][0]['translatedText']
    except Exception:
        logger.critical('Парсинг ответа не выполнен')

    return [language_pair[0], translated_text]


def get_language_pair(text_lenguage):

    language_codes = []

    if text_lenguage == SECOND_LANG:
        language_codes = [FIRST_LANG, SECOND_LANG]
    else:
        language_codes = [SECOND_LANG, FIRST_LANG]

    return language_codes


def detect_language(text):

    language = ''

    url = BASIC_URL + '/detect' + '?key=' + API_KEY
    payload = ({
        'q': [text],
        })

    logger.info('Делаем запрос на определение языка')

    try:
        response = requests.post(url, json=payload, headers=headers)
    except Exception:
        logger.critical('Запрос на определение языка не выполнен')

    if not response.ok:
        status_code = str(response.status_code)

        logger.critical(f'В ответе на запрос вернулась ошибка: {status_code}')

        return status_code

    try:
        language = json.loads(response.text)['data']['detections'][0][0]['language']
    except Exception:
        logger.critical('Парсинг ответа не выполнен')

    return language


def detect_and_translate_text(text):

    if text == '':
        return WRONG_TEXT_ERROR

    detected_language = detect_language(text)

    if detected_language == '':
        return WRONG_TEXT_ERROR
    elif detected_language.isnumeric():
        return UNSPECIFIED_ERROR
    else:
        translated_text = translate_text(text, detected_language)

    return [[detected_language, text], translated_text]
