import requests

import errors
import logger


def is_single_word(text):
    return len(text.split()) == 1


def is_response_failed(response):
    return 'error' in response


def send_post_request(url, payload, headers):

    try:
        response = requests.post(url, json=payload, headers=headers)
    except Exception:
        logger.critical('Запрос не выполнен')

    if is_response_not_ok(response):
        return errors.unspecified_error

    return response


def send_get_request(url, query_parameters, headers):

    try:
        response = requests.get(url, params=query_parameters, headers=headers)
    except Exception:
        logger.critical('Запрос не выполнен')

    if is_response_not_ok(response):
        return errors.unspecified_error

    return response


def is_response_not_ok(response):
    if not response.ok:
        status_code = str(response.status_code)
        text = str(response.text)

        logger.critical(f'Пришел ответ с кодом {status_code} и текстом:\n{text}')
