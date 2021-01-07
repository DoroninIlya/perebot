import asyncio

from telethon import TelegramClient, events

import config
import db_connector
import logger
import translate
import translate_api_handler
import utils

HELLO_TEXT = (
    'Привет! Я бот-переводчик - перевожу с английского языка на ' +
    'русский или обратно. Просто напиши мне слово или фразу :)\r' +
    '[Переведено Lingvo](https://developers.lingvolive.com/) и ' +
    'Google Cloud Translation'
    )

bot = TelegramClient(
    'bot',
    config.API_ID,
    config.API_HASH,
    ).start(bot_token=config.BOT_TOKEN)

db_connector.create_user_table()
db_connector.create_dictionary()


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    sender = await event.get_sender()

    db_connector.add_user(sender.id)

    await event.respond(HELLO_TEXT)

    raise events.StopPropagation


@bot.on(events.NewMessage)
async def echo(event):
    entered_text = event.text
    translated_text = translate.detect_and_translate_text(entered_text)

    sender = await event.get_sender()

    translation_result = ''

    if utils.is_response_failed(translated_text):
        translation_result = translated_text['error']
    else:
        translation_result = translated_text['translation']

        if config.IS_ADD_TO_DICTIONARY == 'true' and utils.is_single_word(entered_text):
            db_connector.add_word_to_dictionary(
                sender.id,
                translated_text['language'],
                entered_text,
                )

    await event.respond(translation_result)


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
