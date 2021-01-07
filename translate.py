import errors
import logger
import translate_api_handler
import utils

EN_LANGUAGE = 'en'
RU_LANGUAGE = 'ru'
TG_LANGUAGE = 'tg'


def translate_text(language_pair, text):

    logger.info('Делаем запрос на перевод слова')

    return translate_api_handler.get_translation(language_pair, text)


def get_language_pair(text_lenguage):

    language_codes = []

    if text_lenguage in [RU_LANGUAGE, TG_LANGUAGE]:
        language_codes = [EN_LANGUAGE, RU_LANGUAGE]
    else:
        language_codes = [RU_LANGUAGE, EN_LANGUAGE]

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
