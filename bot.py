from telethon import TelegramClient, events, Button
import asyncio


import config
import db_connector
import localization
import logger
import re
import translate_api_handler
import utils
from translate import detect_and_translate_text

localized_language_pair_names = {
    'en-ru': localization.EN_RU,
    'de-ru': localization.DE_RU,
    'fr-ru': localization.FR_RU,
    'es-ru': localization.ES_RU,
}

forced_language_pattern = r'^\w{2}[:]'

bot = TelegramClient(
    'bot',
    config.API_ID,
    config.API_HASH,
    ).start(bot_token=config.BOT_TOKEN)

utils.prepare_tables()


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    sender = await event.get_sender()

    utils.prepare_user(sender.id)

    await bot.send_message(
        event.chat_id,
        localization.HELLO_TEXT,
        link_preview=False,
    )


@bot.on(events.NewMessage(pattern='/help'))
async def help_message(event):
    await bot.send_message(event.chat_id, localization.WHO_I_AM_TEXT)


@bot.on(events.NewMessage(pattern=r'^[\/]{0}\w+'))
async def new_word(event):
    sender = await event.get_sender()

    user_languages = db_connector.get_selected_language_pair(sender.id)

    entered_text = event.text

    forced_language = None

    if re.search(forced_language_pattern, entered_text):
        forced_language = entered_text[:2].lower()
        user_languages = f'{forced_language}-ru'
        entered_text = entered_text[3:]

    translated_text = detect_and_translate_text(
        entered_text,
        user_languages,
        forced_language,
        )

    translation_result = ''

    if utils.is_response_failed(translated_text):
        translation_result = translated_text['error']
    else:
        translation_result = translated_text['translation']

        utils.increase_translation_counters(sender.id, len(entered_text))

        if config.IS_ADD_TO_DICTIONARY == 'true' and utils.is_single_word(entered_text):
            db_connector.add_word_to_dictionary(
                sender.id,
                translated_text['language'],
                entered_text,
                )

    await event.respond(translation_result)


@bot.on(events.NewMessage(pattern='/language'))
async def change_language(event):
    sender = await event.get_sender()

    user_languages = db_connector.get_selected_language_pair(sender.id)

    if user_languages in localized_language_pair_names:
        message = (
            localization.CURRENT_LANG_PAIR.format(
                lang_pair=localized_language_pair_names[user_languages],
            )
        )
    else:
        message = localization.UNSUPPORTED_LANGUAGE_PAIR_MESSAGE

    keyboard = [
        [
            Button.inline(localized_language_pair_names['en-ru'], 'en-ru'),
            Button.inline(localized_language_pair_names['de-ru'], 'de-ru'),
        ],
        [
            Button.inline(localized_language_pair_names['fr-ru'], 'fr-ru'),
            Button.inline(localized_language_pair_names['es-ru'], 'es-ru'),
        ],
    ]

    await bot.send_message(
        event.chat_id,
        message + '\n\n' + localization.FOR_CHANGING_PAIR,
        buttons=keyboard,
    )


@bot.on(events.CallbackQuery)
async def callback_handler(event):
    button_data = event.data

    selected_language_pair = button_data.decode('utf-8')

    sender = await event.get_sender()

    db_connector.set_language_pair(selected_language_pair, sender.id)

    await event.respond(
        localization.YOU_HAVE_CHOSEN_A_PAIR.format(
            lang_pair=localized_language_pair_names[selected_language_pair],
        )
    )


async def refresh_abbyy_token():

    if config.IS_NEED_TO_REFRESH_ABBYY_API_TOKEN == 'true':
        logger.info('Запущена задача обновления API-токена ABBYY Lingvo')

        while True:
            logger.info('Обновляю токен...')

            translate_api_handler.refresh_abbyy_api_token()

            await asyncio.sleep(int(config.SECOND_BEFORE_REFRESH_TOKEN))


def main():
    if config.TRANSLATION_SERVICE == 'abbyy':
        asyncio.get_event_loop().create_task(refresh_abbyy_token())

    bot.run_until_disconnected()


if __name__ == '__main__':
    main()
