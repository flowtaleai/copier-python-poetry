"""Pytest-copier Plugin.

This file contains fixtures for use with pytest-copier, a pytest plugin for
testing Copier template generation. Explore the fixtures to see how to
customize Copier templates for your projects.

For more details and the source code, visit:
https://github.com/noirbizarre/pytest-copier/blob/main/src/pytest_copier/plugin.py
"""

import pytest


@pytest.fixture(scope="session")
def copier_template_paths() -> list[str]:
    return ["copier.yml", "template"]


@pytest.fixture
def copier_defaults() -> dict[str, str]:
    """Provides default Copier project configurations.

    This his fixture provides a dictionary containing default configuration values
    commonly used in Copier project generation. These values can be used as a
    template for setting up a Copier configuration.

    Returns:
        dict[str, str]: A dictionary containing default configuration values.
    """
    return {
        "author_email": "user@example.com",
        "author_name": "The User",
        "distribution_name": "python-boilerplate",
        "package_name": "python_boilerplate",
        "project_name": "Python Boilerplate",
        "project_short_description": "An very nice project",
        "license": "MIT license",
        "package_type": "cli",
        "type_checker": "none",
        "type_checker_strictness": "strict",
    }


def pytest_addoption(parser):
    parser.addoption(
        "--run-all", action="store_true", default=False, help="run all tests."
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-all"):
        return
    skip_venv = pytest.mark.skip(
        reason=(
            "Might interfere with the virtual environment. Should be run with tox. Use"
            " --run-all option to force run it."
        )
    )
    for item in items:
        if "venv" in item.keywords:
            item.add_marker(skip_venv)
