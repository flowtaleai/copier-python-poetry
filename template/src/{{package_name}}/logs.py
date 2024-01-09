import logging
import logging.config
import os
from typing import Optional

TOP_LEVEL_LOGGER = __name__.split(".")[0]

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "WARNING",
            "propagate": False,
        },  # root logger
        TOP_LEVEL_LOGGER: {
            "handlers": ["default"],
            "level": os.getenv("VERBOSITY", "INFO").upper(),
            "propagate": False,
        },
    },
}


def set_level(level: Optional[str]):
    if level is not None:
        LOGGING_CONFIG["loggers"][TOP_LEVEL_LOGGER]["level"] = level.upper()
        logging.config.dictConfig(LOGGING_CONFIG)


def get_logger(name: str):
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(name)
