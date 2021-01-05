import logger
import translate_api_handler

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


def translate_text(text, language):

    language_pair = get_language_pair(language)

    logger.info('Делаем запрос на перевод слова')

    translated_text = translate_api_handler.get_translation(language_pair, text)

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

    logger.info('Делаем запрос на определение языка')

    response = translate_api_handler.get_language(text)

    try:
        language = translate_api_handler.parse_language_response(response.text)
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
