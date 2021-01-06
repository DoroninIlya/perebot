import os

from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
TRANSLATION_SERVICE = os.getenv('TRANSLATION_SERVICE')
DETECTION_SERVICE = os.getenv('DETECTION_SERVICE')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
ABBYY_API_TOKEN = os.getenv('ABBYY_API_TOKEN')
YANDEX_API_TOKEN = os.getenv('YANDEX_TOKEN')
YANDEX_FOLDER_ID = os.getenv('YANDEX_FOLDER_ID')
DATABASE_URL = os.getenv('DATABASE_URL')
IS_ADD_TO_DICTIONARY = os.getenv('IS_ADD_TO_DICTIONARY')
