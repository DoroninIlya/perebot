import os

from dotenv import load_dotenv
from telethon import TelegramClient, events

from translate import translate_word

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is issued."""
    await event.respond('Привет! Я бот-переводчик - введи слово и я его переведу)')
    raise events.StopPropagation

@bot.on(events.NewMessage)
async def echo(event):
    
    translated_word = translate_word(event.text)

    await event.respond(translated_word)


def main():
    """Start the bot."""
    bot.run_until_disconnected()


if __name__ == '__main__':
    main()
