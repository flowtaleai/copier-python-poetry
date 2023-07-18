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
        if result.project:
            rmtree(str(result.project))


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
        assert result.project.isdir()
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
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

        assert "Vagrantfile" in found_toplevel_files

        assert "ansible" in found_toplevel_files


def test_bake_and_run_tests_with_pytest_framework(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"testing_framework": "pytest"}
    ) as result:
        assert result.exit_code == 0
        assert result.project.isdir()
        assert run_inside_dir("pytest", str(result.project)) == 0


def test_bake_and_run_tests_with_unittest_framework(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"testing_framework": "unittest"}
    ) as result:
        assert result.exit_code == 0
        assert result.project.isdir()
        assert run_inside_dir("pytest", str(result.project)) == 0


def test_bake_with_ide_vscode(cookies):
    with bake_in_temp_dir(cookies, extra_context={"ide": "vscode"}) as result:
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert ".vscode" in found_toplevel_files
        assert ".idea" not in found_toplevel_files


def test_bake_with_ide_pycharm(cookies):
    with bake_in_temp_dir(cookies, extra_context={"ide": "pycharm"}) as result:
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert ".vscode" not in found_toplevel_files


def test_bake_with_ide_vscode_and_pycharm(cookies):
    with bake_in_temp_dir(cookies, extra_context={"ide": "vscode+pycharm"}) as result:
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert ".vscode" in found_toplevel_files


def test_bake_with_ide_other(cookies):
    with bake_in_temp_dir(cookies, extra_context={"ide": "other"}) as result:
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert ".vscode" not in found_toplevel_files
        assert ".idea" not in found_toplevel_files


def test_bake_app_and_check_cli_scripts(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={"app_or_lib": "application"},
    ) as result:
        assert result.exit_code == 0
        assert result.exception is None

        assert result.project.isdir()
        pyproject_path = result.project.join("pyproject.toml")
        assert '''[tool.poetry.scripts]
pythonboilerplate = "pythonboilerplate.cli:cli"''' in pyproject_path.read()


@pytest.mark.parametrize(
    ["use_ansible", "ansible_files_present"], [("y", True), ("n", False)]
)
def test_bake_without_ansible(use_ansible, ansible_files_present, cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"use_ansible": use_ansible}
    ) as result:
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert ("Vagrantfile" in found_toplevel_files) == ansible_files_present
        assert ("ansible" in found_toplevel_files) == ansible_files_present


@pytest.mark.slow
def test_bake_and_run_cli(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"use_gitlab_package_registry": False}
    ) as result:
        assert result.exit_code == 0
        assert result.project.isdir()
        assert run_inside_dir("poetry install --only-root", str(result.project)) == 0
        assert run_inside_dir("poetry run pythonboilerplate", str(result.project)) == 0


@pytest.mark.slow
def test_bake_and_run_pre_commit(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"use_gitlab_package_registry": False}
    ) as result:
        assert result.exit_code == 0
        assert result.project.isdir()

        run_inside_dir("poetry install", str(result.project))
        run_inside_dir("git init", str(result.project))
        run_inside_dir("git add .", str(result.project))
        run_inside_dir("git commit -m init", str(result.project))

        assert (
            run_inside_dir("poetry run pre-commit run --all-files", str(result.project))
            == 0
        )


@pytest.mark.parametrize(
    ["is_gitlab_auth_required", "poetry_config_present"], [("y", True), ("n", False)]
)
def test_gitlab_auth_option(is_gitlab_auth_required, poetry_config_present, cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"is_gitlab_auth_required": is_gitlab_auth_required}
    ) as result:
        assert result.exit_code == 0
        assert result.exception is None

        gitlab_ci_file = result.project / ".gitlab-ci.yml"
        assert (
            "poetry config http-basic.gitlab-flowtale" in gitlab_ci_file.read()
        ) == poetry_config_present
