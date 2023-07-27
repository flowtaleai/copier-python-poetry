import shlex
import subprocess
from contextlib import contextmanager

import pytest
from cookiecutter.utils import rmtree, work_in


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        if result.project_path:
            rmtree(result.project_path)


def run_inside_dir(command, dirpath):
    """
    Run a command from inside a given directory, returning the exit status
    :param command: Command that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with work_in(dirpath):
        try:
            result = subprocess.run(
                shlex.split(command), check=True, capture_output=True
            )
        except subprocess.CalledProcessError as e:
            print(command)
            print("OUT:")
            print(e.stdout)
            print("ERR:")
            print(e.stderr)
            print("-------------")
            return -1
        return result.returncode


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.exit_code == 0
        assert result.project_path.is_dir()
        assert result.exception is None

        found_toplevel_files = [f.name for f in result.project_path.glob("*")]
        assert ".bumpversion.cfg" in found_toplevel_files
        assert ".gitignore" in found_toplevel_files
        assert "pyproject.toml" in found_toplevel_files
        assert ".python-version" in found_toplevel_files
        assert ".editorconfig" in found_toplevel_files
        assert "README.md" in found_toplevel_files
        assert "LICENSE" not in found_toplevel_files
        assert ".flake8" in found_toplevel_files
        assert ".pre-commit-config.yaml" in found_toplevel_files
        assert ".gitattributes" in found_toplevel_files
        assert "tests" in found_toplevel_files

        assert "pythonboilerplate" in found_toplevel_files
        assert ".vscode" in found_toplevel_files

        assert "Pipfile" not in found_toplevel_files


def test_bake_and_run_tests_with_pytest_framework(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"testing_framework": "pytest"}
    ) as result:
        assert result.exit_code == 0
        assert result.project_path.is_dir()
        assert run_inside_dir("pytest", result.project_path) == 0


def test_bake_and_run_tests_with_unittest_framework(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"testing_framework": "unittest"}
    ) as result:
        assert result.exit_code == 0
        assert result.project_path.is_dir()
        assert run_inside_dir("pytest", result.project_path) == 0


def test_bake_with_ide_vscode(cookies):
    with bake_in_temp_dir(cookies, extra_context={"ide": "vscode"}) as result:
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.name for f in result.project_path.glob("*")]
        assert ".vscode" in found_toplevel_files
        assert ".idea" not in found_toplevel_files


def test_bake_cli_application(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"app_or_lib": "application"}
    ) as result:
        assert result.exit_code == 0
        assert result.exception is None

        found_cli_script = [f.name for f in result.project_path.glob("**/cli.py")]
        assert found_cli_script


def test_bake_library(cookies):
    with bake_in_temp_dir(cookies, extra_context={"app_or_lib": "library"}) as result:
        assert result.exit_code == 0
        assert result.exception is None

        found_cli_script = [f.name for f in result.project_path.glob("**/cli.py")]
        assert not found_cli_script


def test_bake_app_and_check_cli_scripts(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={"app_or_lib": "application"},
    ) as result:
        assert result.exit_code == 0
        assert result.exception is None

        assert result.project_path.is_dir()
        pyproject_path = result.project_path / "pyproject.toml"
        assert (
            '''[tool.poetry.scripts]
pythonboilerplate = "pythonboilerplate.cli:cli"'''
            in pyproject_path.read_text()
        )


@pytest.mark.skip(
    "poetry is run in the poetry env of the outer project creating interferences"
)
@pytest.mark.slow()
def test_bake_and_run_cli(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.exit_code == 0
        assert result.project_path.is_dir()
        assert run_inside_dir("poetry install --only main", result.project_path) == 0
        assert run_inside_dir("poetry run pythonboilerplate", result.project_path) == 0


@pytest.mark.slow()
def test_bake_and_run_pre_commit(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.exit_code == 0
        assert result.project_path.is_dir()

        run_inside_dir("poetry install", result.project_path)
        run_inside_dir("git init", result.project_path)
        run_inside_dir("git add .", result.project_path)
        run_inside_dir("git commit -m init", result.project_path)

        assert (
            run_inside_dir("poetry run pre-commit run --all-files", result.project_path)
            == 0
        )
