import logging

from utils import config


LEVEL = config.LOG_LEVEL
FORMAT = config.LOG_FORMAT


def setup():
    console = logging.StreamHandler()
    console.setLevel(LEVEL)
    formatter = logging.Formatter(FORMAT)
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)
