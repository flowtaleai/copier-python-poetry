import logging
import logging.config

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
            "level": "INFO",
            "propagate": False,
        },
        "__main__": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },  # if __name__ == '__main__'
    },
}


def set_level(level: int):
    LOGGING_CONFIG["loggers"]["__main__"]["level"] = level
    LOGGING_CONFIG["loggers"][TOP_LEVEL_LOGGER]["level"] = level
    logging.config.dictConfig(LOGGING_CONFIG)


def handle_log_flags(verbose: bool, quiet: bool = False):
    if verbose and quiet:
        raise ValueError("--verbose and --quiet cannot be set together.")
    elif verbose:
        set_level(logging.DEBUG)
    elif quiet:
        set_level(logging.WARNING)


def get_logger(name: str):
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(name)
