import errors
import logger
import translate_api_handler
import utils


def translate_text(language_pair, text):

    logger.info('Делаем запрос на перевод слова')

    return translate_api_handler.get_translation(language_pair, text)


def get_language_pair(text_language, user_language_pair):

    language_codes = []
    language_pair = user_language_pair.split('-')

    if text_language in language_pair:
        if text_language == language_pair[0]:
            language_codes = [language_pair[1], language_pair[0]]
        else:
            language_codes = [language_pair[0], language_pair[1]]
    else:
        return errors.language_not_detected

    return language_codes


def detect_language(text):

    logger.info('Делаем запрос на определение языка')

    return translate_api_handler.get_language(text)


def detect_and_translate_text(text, user_language_pair):

    if text == '':
        return errors.wrong_text_error

    detected_language = detect_language(text)

    if utils.is_response_failed(detected_language):
        return detected_language

    language_pair = get_language_pair(detected_language, user_language_pair)

    if utils.is_response_failed(language_pair):
        return language_pair

    translated_text = translate_text(language_pair, text)

    if utils.is_response_failed(translated_text):
        return translated_text

    return {'language': detected_language, 'translation': translated_text}
