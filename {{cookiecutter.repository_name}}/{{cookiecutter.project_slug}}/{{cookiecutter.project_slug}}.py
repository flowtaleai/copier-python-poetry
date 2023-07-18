"""Main module."""
from {{cookiecutter.project_slug}} import logs

logger = logs.get_logger(__name__)


def a_function():
    logger.debug("Generating hello world string")
    return "Hello World!"
