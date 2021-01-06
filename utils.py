def is_single_word(text):
    return len(text.split()) == 1


def is_response_failed(response):
    return 'error' in response
