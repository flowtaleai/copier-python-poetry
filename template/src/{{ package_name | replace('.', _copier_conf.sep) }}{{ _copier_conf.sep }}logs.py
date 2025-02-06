import logging
import logging.config
import os
from enum import Enum
from typing import Optional

PACKAGE_LOGGER = __name__.split(".")[0]

LOGGING_CONFIG: dict[str, Any] = {
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
        PACKAGE_LOGGER: {
            "handlers": ["default"],
            "level": os.getenv("LOG_LEVEL", "INFO").upper(),
            "propagate": False,
        },
    },
}


class LogLevel(str, Enum):
    """Enumeration for standard log levels."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


def set_level(level: Optional[str]) -> None:
    if level is not None:
        LOGGING_CONFIG["loggers"][PACKAGE_LOGGER]["level"] = level.upper()
        logging.config.dictConfig(LOGGING_CONFIG)


def get_logger(name: str) -> logging.Logger:
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(name)
