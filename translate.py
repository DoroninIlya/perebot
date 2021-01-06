import errors
import logger
import translate_api_handler
import utils

FIRST_LANG = 'en'
SECOND_LANG = 'ru'


def translate_text(language_pair, text):

    logger.info('Делаем запрос на перевод слова')

    return translate_api_handler.get_translation(language_pair, text)


def get_language_pair(text_lenguage):

    language_codes = []

    if text_lenguage == SECOND_LANG:
        language_codes = [FIRST_LANG, SECOND_LANG]
    else:
        language_codes = [SECOND_LANG, FIRST_LANG]

    return language_codes


def detect_language(text):

    logger.info('Делаем запрос на определение языка')

    return translate_api_handler.get_language(text)


def detect_and_translate_text(text):

    if text == '':
        return errors.wrong_text_error

    detected_language = detect_language(text)

    if utils.is_response_failed(detected_language):
        return detected_language

    language_pair = get_language_pair(detected_language)

    translated_text = translate_text(language_pair, text)

    if utils.is_response_failed(translated_text):
        return translated_text

    return {'language': detected_language, 'translation': translated_text}
