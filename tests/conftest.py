"""Pytest-copier Plugin.

This file contains fixtures for use with pytest-copier, a pytest plugin for
testing Copier template generation. Explore the fixtures to see how to
customize Copier templates for your projects.

For more details and the source code, visit:
https://github.com/noirbizarre/pytest-copier/blob/main/src/pytest_copier/plugin.py
"""

import shutil
from pathlib import Path

import pytest
from pytest_copier.plugin import run


@pytest.fixture(scope="session")
def copier_template(
    tmp_path_factory: pytest.TempPathFactory,
    copier_template_root: Path,
) -> Path:
    """Copy temporary directories and configures git.

    This fixture is auto-used by pytest-copier.
    Overriding this fixture is necessary to avoid copying all the files in the root of
    the project, in particular .pre-commit-config.yaml that messes up the tests.

    Args:
        tmp_path_factory: Pytest fixture for creating temporary directories.
        copier_template_root: The root directory of the Copier template.

    Returns:
        Path: The path to the temporary Copier template directory.
    """
    src = tmp_path_factory.mktemp("src", False)

    shutil.copytree(
        copier_template_root / "template", src / "template", dirs_exist_ok=True
    )
    shutil.copyfile(copier_template_root / "copier.yml", src / "copier.yml")

    run("git", "config", "--global", "init.defaultBranch", "main", cwd=src)
    run("git", "config", "--global", "user.name", "'User Name'", cwd=src)
    run("git", "config", "--global", "user.email", "'user@email.org'", cwd=src)
    run("git", "init", cwd=src)
    run("git", "add", "-A", ".", cwd=src)
    run("git", "commit", "-m", "test", cwd=src)
    run("git", "tag", "99.99.99", cwd=src)

    return src


@pytest.fixture()
def copier_defaults() -> dict[str, str]:
    """Provide default Copier project configs.

    This his fixture provides a dictionary containing default configuration values
    commonly used in Copier project generation. These values can be used as a
    template for setting up a Copier configuration.

    Returns:
        dict[str, str]: A dictionary containing default configuration values.
    """
    return {
        "author_email": "user@example.com",
        "author_name": "The User",
        "project_name": "Python Boilerplate",
        "project_short_description": "An very nice project",
        "license": "MIT license",
        "package_type": "cli",
    }
