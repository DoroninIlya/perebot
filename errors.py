import localization
from utils import error_decorator

wrong_text_error = error_decorator(localization.WRONG_TEXT_ERROR)

unspecified_error = error_decorator(localization.UNSPECIFIED_ERROR)


def language_not_detected(possible_language):
    return error_decorator(
        localization.LANGUAGE_NOT_DETECTED.format(
            lang=localization.AVAILABLE_LANGUAGES_LIST[possible_language],
            available_langs=localization.AVAILABLE_LANGUAGES,
        ),
    )


refresh_token_error = error_decorator(localization.REFRESH_TOKEN_ERROR)

parse_error = error_decorator(localization.PARSE_ERROR)

unknown_language = error_decorator(localization.UNKNOWN_LANGUAGE)

unknown_forced_language = error_decorator(
    localization.UNKNOWN_FORCED_LANGUAGE.format(
        available_langs=localization.AVAILABLE_LANGUAGES,
    )
)
