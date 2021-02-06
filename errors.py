import localization
from utils import error_decorator

wrong_text_error = error_decorator(localization.WRONG_TEXT_ERROR)

unspecified_error = error_decorator(localization.UNSPECIFIED_ERROR)

language_not_detected = error_decorator(localization.LANGUAGE_NOT_DETECTED)

refresh_token_error = error_decorator(localization.REFRESH_TOKEN_ERROR)

parse_error = error_decorator(localization.PARSE_ERROR)
