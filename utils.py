import requests

import logger


def is_single_word(text):
    return len(text.split()) == 1


def is_response_failed(response):
    return 'error' in response


def send_request(method, url, query_parameters, headers, payload):
    try:
        response = requests.request(
            method=method,
            url=url,
            params=query_parameters,
            headers=headers,
            json=payload,
            )
    except Exception:
        logger.critical('Запрос не выполнен')

    return response


def is_response_not_ok(response):
    if not response.ok:
        status_code = str(response.status_code)
        text = str(response.text)

        logger.critical(f'Пришел ответ с кодом {status_code} и текстом:\n{text}')

        return True

    return False
