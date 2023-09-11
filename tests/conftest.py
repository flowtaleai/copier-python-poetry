"""
Check out the source code of pytest-copier to understand how to use the various
fixtures.

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
    """This fixture is auto-used by pytest-copier.

    Overriding this fixture is necessary to avoid copying all the files in the root of
    the project, in particular .pre-commit-config.yaml that messes up the tests.
    """
    src = tmp_path_factory.mktemp("src", False)

    shutil.copytree(
        copier_template_root / "template", src / "template", dirs_exist_ok=True
    )
    shutil.copyfile(copier_template_root / "copier.yml", src / "copier.yml")

    run("git", "init", cwd=src)
    run("git", "add", "-A", ".", cwd=src)
    run("git", "-c", "user.name='User Name'", "-c", "user.email='user@email.org'", "commit", "-m", "test", cwd=src)
    run("git", "tag", "99.99.99", cwd=src)

    return src


@pytest.fixture()
def copier_defaults() -> dict[str, str]:
    """This fixture is auto-used by pytest-copier."""
    return {
        "author_email": "user@example.com",
        "author_name": "The User",
        "project_name": "Python Boilerplate",
        "project_short_description": "An very nice project",
        "license": "MIT license",
        "package_type": "cli",
    }
