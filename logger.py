import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(asctime)s %(message)s',
    )


def info(message):
    logging.info(message)


def warning(message):
    logging.warning(message)


def critical(message):
    logging.critical(message)
