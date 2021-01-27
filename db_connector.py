import psycopg2
from psycopg2 import sql

import config
import logger

connection = psycopg2.connect(config.DATABASE_URL, sslmode='require')

cursor = connection.cursor()


def create_table_users():
    try:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS USERS
            (USER_ID INT UNIQUE NOT NULL,
            SELECTED_LANGUAGE_PAIR TEXT,
            IS_PREMIUM_USER BOOLEAN NOT NULL DEFAULT FALSE,
            PREMIUM_EXPIRED_DATE INT,
            CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP);""")
    except Exception as error:
        logger.critical(f'Ошибка при создании таблицы пользователей.\n{error}')

    connection.commit()


def add_user(user_id):

    try:
        cursor.execute(
            'INSERT INTO users (user_id) VALUES (%s) ON CONFLICT DO NOTHING;',
            ([user_id]),
            )
    except Exception as error:
        logger.warning(
            f'Ошибка при добавлении пользователя {user_id} ' +
            f'в таблицу пользователей.\n{error}',
            )
    else:
        logger.info('Новый пользователь добавлен в таблицу')

    connection.commit()


def create_table_dictionary():

    try:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS DICTIONARY
            (USER_ID INT NOT NULL,
            RU TEXT,
            EN TEXT,
            FR TEXT,
            ES TEXT,
            DE TEXT,
            IS_LEARNED BOOLEAN,
            LEARNED_AT TIMESTAMP,
            CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            TRANSLATIONS_COUNT INT DEFAULT 1,
            CONSTRAINT unique_pair_ru UNIQUE (USER_ID, RU),
            CONSTRAINT unique_pair_en UNIQUE (USER_ID, EN),
            CONSTRAINT unique_pair_fr UNIQUE (USER_ID, FR),
            CONSTRAINT unique_pair_es UNIQUE (USER_ID, ES),
            CONSTRAINT unique_pair_de UNIQUE (USER_ID, DE));""")
    except Exception as error:
        logger.critical(f'Ошибка при создании таблицы словаря.\n{error}')

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

        increase_word_translations_count(user_id, source_language, lowered_word)
    except Exception as error:
        logger.warning(f'Ошибка при добавлении слова в словарь.\n{error}')
    else:
        logger.info('Новое слово успешно добавлено в таблицу')

    connection.commit()


def set_language_pair(language_pair, user_id):
    try:
        cursor.execute(
            'UPDATE USERS SET SELECTED_LANGUAGE_PAIR = %s WHERE USER_ID = %s;',
            (language_pair, user_id),
            )
    except Exception as error:
        logger.warning(f'Ошибка при установке языковой пары.\n{error}')
    else:
        logger.info('Выбранная языковая пара успешно добавлена в таблицу')

    connection.commit()


def increase_word_translations_count(user_id, source_language, lowered_word):
    logger.info('Слово уже добавлено в словарь')

    query = sql.SQL(
        """UPDATE dictionary
        SET translations_count = translations_count + 1
        WHERE user_id = %s AND {language} = %s;""",
        ).format(language=sql.Identifier(source_language))
    try:
        cursor.execute(query, (user_id, lowered_word))
    except Exception as error:
        logger.warning(f'Ошибка при увеличении количества переводов.\n{error}')
    else:
        logger.info('Увеличено количество переводов этого слова')
    
    connection.commit()


def get_selected_language_pair(user_id):
    try:
        cursor.execute(
            'SELECT selected_language_pair FROM users WHERE user_id = %s;',
            ([user_id]),
            )
    except Exception as error:
        logger.warning(f'Ошибка при получении языковой пары.\n{error}')

    selected_language = cursor.fetchone()

    connection.commit()

    if selected_language:
        if selected_language[0]:
            return selected_language[0]

    return 'en-ru'


def create_table_user_statistics():
    try:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS statistic
            (user_id INT UNIQUE NOT NULL,
            requests_count INT DEFAULT 0,
            symbols_count INT DEFAULT 0);""")
    except Exception as error:
        logger.critical(f'Ошибка при создании таблицы статистики.\n{error}')

    connection.commit()


def add_user_to_statistic(user_id):

    try:
        cursor.execute(
            'INSERT INTO statistic (USER_ID) VALUES (%s) ON CONFLICT DO NOTHING;',
            ([user_id])
            )
    except Exception as error:
        logger.warning(
            f'Ошибка при добавлении пользователя {user_id} ' +
            f'в таблицу статистики.\n{error}',
        )

    connection.commit()


def increase_requests_count(user_id):
    try:
        cursor.execute(
            """UPDATE statistic
            SET requests_count = requests_count + 1
            WHERE user_id = %s;""",
            ([user_id]),
            )
    except Exception as error:
        logger.warning(f'Ошибка при увеличении количества запросов.\n{error}')
    else:
        logger.info('Увеличено количество запросов')

    connection.commit()


def increase_symbols_count(user_id, symbols_number):
    try:
        cursor.execute(
            """UPDATE statistic
            SET symbols_count = symbols_count + %s
            WHERE user_id = %s;""",
            (symbols_number, user_id),
            )
    except Exception as error:
        logger.warning(f'Ошибка при увеличении количества переведенных символов.\n{error}')
    else:
        logger.info('Увеличено количество переведенных символов')

    connection.commit()
