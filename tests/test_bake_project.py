import pytest


@pytest.fixture
def required_answers():
    return {
        "author_email": "user@example.com",
        "author_name": "The User",
        "project_name": "Python Boilerplate",
        "project_short_description": "An very nice project",
        "license": "MIT license",
        "package_type": "cli",
    }


def test_bake_with_defaults(copier, required_answers):
    project = copier.copy(**required_answers)

    found_toplevel_files = [f.name for f in project.path.glob("*")]
    assert ".bumpversion.cfg" in found_toplevel_files
    assert ".gitignore" in found_toplevel_files
    assert "pyproject.toml" in found_toplevel_files
    assert ".python-version" in found_toplevel_files
    assert ".editorconfig" in found_toplevel_files
    assert "README.md" in found_toplevel_files
    assert "LICENSE" in found_toplevel_files
    assert ".flake8" in found_toplevel_files
    assert ".pre-commit-config.yaml" in found_toplevel_files
    assert ".gitattributes" in found_toplevel_files
    assert "tests" in found_toplevel_files

    assert "pythonboilerplate" in found_toplevel_files
    assert ".vscode" in found_toplevel_files

    assert "Pipfile" not in found_toplevel_files


def test_bake_and_run_tests_with_pytest_framework(copier, required_answers):
    custom_answers = {"testing_framework": "pytest"}
    answers = {**required_answers, **custom_answers}
    project = copier.copy(**answers)

    project.run("pytest")


def test_bake_and_run_tests_with_unittest_framework(copier, required_answers):
    custom_answers = {"testing_framework": "unittest"}
    answers = {**required_answers, **custom_answers}
    project = copier.copy(**answers)

    found_toplevel_files = [f.name for f in project.path.glob("*")]
    assert ".vscode" in found_toplevel_files
    assert ".idea" not in found_toplevel_files


def test_bake_cli_application(copier, required_answers):
    custom_answers = {"package_type": "cli"}
    answers = {**required_answers, **custom_answers}
    project = copier.copy(**answers)

    found_cli_script = [f.name for f in project.path.glob("**/cli.py")]
    assert found_cli_script


def test_bake_library(copier, required_answers):
    custom_answers = {"package_type": "library"}
    answers = {**required_answers, **custom_answers}
    project = copier.copy(**answers)

    found_cli_script = [f.name for f in project.path.glob("**/cli.py")]
    assert not found_cli_script


def test_bake_app_and_check_cli_scripts(copier, required_answers):
    custom_answers = {"package_type": "cli"}
    answers = {**required_answers, **custom_answers}
    project = copier.copy(**answers)

    assert project.path.is_dir()
    pyproject_path = project.path / "pyproject.toml"
    assert (
        '''[tool.poetry.scripts]
pythonboilerplate = "pythonboilerplate.cli:cli"'''
        in pyproject_path.read_text()
    )


@pytest.mark.skip(
    "poetry is run in the poetry env of the outer project creating interferences"
)
@pytest.mark.slow()
def test_bake_and_run_cli(copier, required_answers):
    custom_answers = {"package_type": "cli"}
    answers = {**required_answers, **custom_answers}
    project = copier.copy(**answers)

    project.run("poetry install --only main")
    project.run("poetry run pythonboilerplate")


@pytest.mark.slow()
def test_bake_and_run_pre_commit(copier, required_answers):
    custom_answers = {"package_type": "cli"}
    answers = {**required_answers, **custom_answers}
    project = copier.copy(**answers)

    project.run("git init")
    project.run("git add .")
    project.run("git commit -m init")

    project.run("pre-commit run --all-files")
