from telethon import TelegramClient, events, Button
import asyncio


import config
import db_connector
import logger
import translate_api_handler
import utils
from translate import detect_and_translate_text

HELLO_TEXT = (
    'Привет! Я бот-переводчик - перевожу с английского языка на ' +
    'русский или обратно. Просто напиши мне слово или фразу :)\r' +
    '[Переведено Lingvo](https://developers.lingvolive.com/) и ' +
    'Google Cloud Translation'
    )
EN_RU_PAIR = 'английский и русский'
DE_RU_PAIR = 'немецкий и русский'
FR_RU_PAIR = 'французский и русский'
ES_RU_PAIR = 'испанский и русский'

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

    await event.respond(HELLO_TEXT)

    raise events.StopPropagation


@bot.on(events.NewMessage(pattern=r'^[\/]{0}\w+'))
async def new_word(event):
    sender = await event.get_sender()

    #временный костыль, чтобы добавить в БД старых пользователей
    utils.prepare_user(sender.id)

    user_languages = db_connector.get_selected_language_pair(sender.id)

    entered_text = event.text

    translated_text = detect_and_translate_text(entered_text, user_languages)

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

    if user_languages == 'en-ru':
        localized_user_language = EN_RU_PAIR
    elif user_languages == 'de-ru':
        localized_user_language = DE_RU_PAIR
    elif user_languages == 'fr-ru':
        localized_user_language = FR_RU_PAIR
    elif user_languages == 'es-ru':
        localized_user_language = ES_RU_PAIR
    else:
        localized_user_language = 'не определена'

    message = (
        f'Текущая выбранная языковая пара - {localized_user_language}.\n\n' +
        'Для изменения выберите пару языков:'
    )

    keyboard = [
        [
            Button.inline(EN_RU_PAIR, b'en-ru'),
            Button.inline(DE_RU_PAIR, b'de-ru'),
        ],
        [
            Button.inline(FR_RU_PAIR, b'fr-ru'),
            Button.inline(ES_RU_PAIR, b'es-ru'),
        ]
    ]

    await bot.send_message(event.chat_id, (message), buttons=keyboard)


@bot.on(events.CallbackQuery)
async def callback_handler(event):
    selected_language_pair = ''

    if event.data == b'en-ru':
        selected_language_pair = 'en-ru'
        localized_user_language = EN_RU_PAIR
    elif event.data == b'de-ru':
        selected_language_pair = 'de-ru'
        localized_user_language = DE_RU_PAIR
    elif event.data == b'fr-ru':
        selected_language_pair = 'fr-ru'
        localized_user_language = FR_RU_PAIR
    else:
        selected_language_pair = 'es-ru'
        localized_user_language = ES_RU_PAIR

    sender = await event.get_sender()

    db_connector.select_language_pair(selected_language_pair, sender.id)

    await event.respond(f'Вы выбрали пару: {localized_user_language}.')


async def refresh_abbyy_token():

    logger.info('Запущена задача обновления API-токена ABBYY Lingvo')

    while True:
        if config.IS_NEED_TO_REFRESH_ABBYY_API_TOKEN == 'true':
            logger.info('Обновляю токен...')

            translate_api_handler.refresh_abbyy_api_token()

        await asyncio.sleep(int(config.SECOND_BEFORE_REFRESH_TOKEN))


def main():
    if config.TRANSLATION_SERVICE == 'abbyy':
        asyncio.get_event_loop().create_task(refresh_abbyy_token())

    bot.run_until_disconnected()


if __name__ == '__main__':
    main()
