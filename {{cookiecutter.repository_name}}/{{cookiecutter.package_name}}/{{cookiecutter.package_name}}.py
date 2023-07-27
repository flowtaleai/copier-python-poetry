"""Main module."""
from {{cookiecutter.package_name}} import logs

logger = logs.get_logger(__name__)


def a_function():
    logger.debug("Generating hello world string")
    return "Hello World!"
