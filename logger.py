import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(asctime)s %(message)s',
    )


def critical(message):
    logging.critical(message)


def info(message):
    logging.info(message)


def critical(message):
    logging.critical(message)
