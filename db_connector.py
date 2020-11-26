import os
import uuid

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql

import logger

load_dotenv()

DATABASE = os.getenv('DATABASE_URL')

connection = psycopg2.connect(DATABASE, sslmode='require')

cursor = connection.cursor()


def create_user_table():
    try:
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS USERS
            (USER_ID INT UNIQUE NOT NULL,
            UUID UUID UNIQUE NOT NULL,
            IS_PREMIUM_USER BOOLEAN NOT NULL DEFAULT FALSE,
            PREMIUM_EXPIRED_DATE INT,
            CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP);''')
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
            '''CREATE TABLE IF NOT EXISTS DICTIONARY
            (USER_ID INT NOT NULL,
            RU TEXT UNIQUE,
            EN TEXT UNIQUE,
            IS_LEARNED BOOLEAN,
            LEARNED_AT TIMESTAMP,
            CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP);'''
            )
    except Exception:
        logger.critical('Создание таблицы не выполнено')

    connection.commit()

def add_word_to_dictionary(user_id, translated_pair):

    first_language = translated_pair[0][0]
    second_language = translated_pair[1][0]
    first_word = translated_pair[0][1]
    second_word = translated_pair[1][1]

    query = sql.SQL(
        'INSERT INTO DICTIONARY (USER_ID, {first}, {second}) VALUES (%s, %s, %s)',
        ).format(
            first=sql.Identifier(first_language),
            second=sql.Identifier(second_language),
        )

    cursor.execute(query, (user_id, first_word, second_word))
    logger.info('Слово добавлено в словарь')

    connection.commit()


def get_word_from_dictionary():
    try:
        cursor.execute('SELECT * FROM DICTIONARY')
    except Exception:
        logger.critical('Получение данных из таблицы не выполнено')

    connection.commit()

    for row in cursor:
        print(row)
