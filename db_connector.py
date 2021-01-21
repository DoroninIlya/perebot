import psycopg2
from psycopg2 import sql

import config
import logger

connection = psycopg2.connect(config.DATABASE_URL, sslmode='require')

cursor = connection.cursor()


def create_user_table():
    try:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS USERS
            (USER_ID INT UNIQUE NOT NULL,
            SELECTED_LANGUAGE_PAIR TEXT,
            IS_PREMIUM_USER BOOLEAN NOT NULL DEFAULT FALSE,
            PREMIUM_EXPIRED_DATE INT,
            CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP);""")
    except Exception as error:
        logger.critical(f'Создание таблицы users не выполнено.\n{error}')

    connection.commit()


def add_user(user_id):

    try:
        cursor.execute('INSERT INTO USERS (USER_ID) VALUES (%s);', ([user_id]))
    except Exception as error:
        logger.warning(f'Пользователь {user_id} не добавлен в таблицу.\n{error}')
    else:
        logger.info('Новый пользователь добавлен в таблицу')

    connection.commit()


def create_dictionary():

    try:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS DICTIONARY
            (USER_ID INT NOT NULL,
            RU TEXT,
            EN TEXT,
            FR TEXT,
            IS_LEARNED BOOLEAN,
            LEARNED_AT TIMESTAMP,
            CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            TRANSLATIONS_COUNT INT DEFAULT 1,
            CONSTRAINT unique_pair_ru UNIQUE (USER_ID, RU),
            CONSTRAINT unique_pair_en UNIQUE (USER_ID, EN),
            CONSTRAINT unique_pair_fr UNIQUE (USER_ID, FR));""")
    except Exception as error:
        logger.critical(f'Создание таблицы dictionary не выполнено.\n{error}')

    connection.commit()


def add_word_to_dictionary(user_id, source_language, word):

    lowered_word = word.lower()

    query = sql.SQL(
        'INSERT INTO DICTIONARY (USER_ID, {language}) VALUES (%s, %s)',
        ).format(language=sql.Identifier(source_language))
    try:
        cursor.execute(query, (user_id, lowered_word))
    except psycopg2.errors.UniqueViolation:
        connection.commit()

        increase_translations_count(user_id, source_language, lowered_word)
    except Exception as error:
        logger.warning(f'Добавление слова в словарь не выполнено.\n{error}')
    else:
        logger.info('Новое слово успешно добавлено в таблицу')

    connection.commit()


def select_language_pair(language_pair, user_id):
    try:
        cursor.execute(
            'UPDATE USERS SET SELECTED_LANGUAGE_PAIR = %s WHERE USER_ID = %s;',
            (language_pair, user_id),
            )
    except Exception as error:
        logger.warning(f'Установка языковой пары не выполнена.\n{error}')
    else:
        logger.info('Выбранная языковая пара успешно добавлена в таблицу')

    connection.commit()


def increase_translations_count(user_id, source_language, lowered_word):
    logger.info('Слово уже добавлено в словарь')

    query = sql.SQL(
        """UPDATE dictionary
        SET translations_count = translations_count + 1
        WHERE user_id = %s AND {language} = %s;""",
        ).format(language=sql.Identifier(source_language))
    try:
        cursor.execute(query, (user_id, lowered_word))
    except Exception as error:
        logger.warning(f'Увеличение количества переводов не выполнено.\n{error}')
    else:
        logger.info('Увеличено количество переводов этого слова')


def get_selected_language_pair(user_id):
    try:
        cursor.execute(
            'SELECT selected_language_pair FROM users WHERE user_id = %s;',
            ([user_id]),
            )
    except Exception as error:
        logger.warning(f'Получение языковой пары не выполнено.\n{error}')

    selected_language = cursor.fetchone()

    connection.commit()

    if selected_language:
        if selected_language[0]:
            return selected_language[0]

    return 'en-ru'
