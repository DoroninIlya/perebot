import os

from dotenv import load_dotenv
from telethon import TelegramClient, events

import db_connector
import translate

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

HELLO_TEXT = (
    'Привет! Я бот-переводчик - перевожу с английского языка на ' +
    'русский или обратно. Просто напиши мне слово или фразу :)'
    )

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

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
    translated_text = translate.detect_and_translate_text(event.text)

    sender = await event.get_sender()

    #db_connector.add_word_to_dictionary(sender.id, translated_text)

    await event.respond(translated_text[1][1])


def main():
    bot.run_until_disconnected()


if __name__ == '__main__':
    main()
