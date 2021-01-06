import os
import uuid

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
            UUID UUID UNIQUE NOT NULL,
            IS_PREMIUM_USER BOOLEAN NOT NULL DEFAULT FALSE,
            PREMIUM_EXPIRED_DATE INT,
            CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP);""")
    except Exception:
        logger.critical('Создание таблицы не выполнено')

    connection.commit()


def add_user(user_id):

    unique_id = str(uuid.uuid4())

    try:
        cursor.execute(
            'INSERT INTO USERS (USER_ID, UUID) VALUES (%s, %s);',
            (user_id, unique_id),
            )
    except Exception:
        logger.critical('Добавление пользователя не выполнено')

    connection.commit()


def create_dictionary():

    try:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS DICTIONARY
            (USER_ID INT NOT NULL,
            RU TEXT UNIQUE,
            EN TEXT UNIQUE,
            IS_LEARNED BOOLEAN,
            LEARNED_AT TIMESTAMP,
            CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP);""")
    except Exception:
        logger.critical('Создание таблицы не выполнено')

    connection.commit()


def add_word_to_dictionary(user_id, source_language, word):

    query = sql.SQL(
        'INSERT INTO DICTIONARY (USER_ID, {language}) VALUES (%s, %s)',
        ).format(language=sql.Identifier(source_language))

    try:
        cursor.execute(query, (user_id, word.lower()))
        logger.info('Слово добавлено в словарь')
    except Exception:
        logger.critical('Добавление слова в словарь не выполнено')

    connection.commit()
