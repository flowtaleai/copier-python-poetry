import pytest
from prompt_toolkit.validation import ValidationError


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


def test_bake_with_defaults(copier):
    project = copier.copy()

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


def test_bake_and_run_tests_with_pytest_framework(copier):
    custom_answers = {"testing_framework": "pytest"}
    project = copier.copy(**custom_answers)

    project.run("pytest")


def test_bake_and_run_tests_with_unittest_framework(copier):
    custom_answers = {"testing_framework": "unittest"}
    project = copier.copy(**custom_answers)

    found_toplevel_files = [f.name for f in project.path.glob("*")]
    assert ".vscode" in found_toplevel_files
    assert ".idea" not in found_toplevel_files


def test_bake_with_proprietary_license(copier):
    custom_answers = {"license": "Proprietary"}
    project = copier.copy(**custom_answers)

    found_toplevel_files = [f.name for f in project.path.glob("*")]
    assert "LICENSE" not in found_toplevel_files


def test_bake_with_invalid_package_name(copier):
    custom_answers = {"package_name": "1invalid"}
    with pytest.raises(ValidationError):
        copier.copy(**custom_answers)


def test_bake_cli_application(copier):
    custom_answers = {"package_type": "cli"}
    project = copier.copy(**custom_answers)

    found_cli_script = [f.name for f in project.path.glob("**/cli.py")]
    assert found_cli_script


def test_bake_library(copier):
    custom_answers = {"package_type": "library"}
    project = copier.copy(**custom_answers)

    found_cli_script = [f.name for f in project.path.glob("**/cli.py")]
    assert not found_cli_script


def test_bake_app_and_check_cli_scripts(copier):
    custom_answers = {"package_type": "cli"}
    project = copier.copy(**custom_answers)

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
def test_bake_and_run_cli(copier):
    custom_answers = {"package_type": "cli"}
    project = copier.copy(**custom_answers)

    project.run("poetry install --only main")
    project.run("poetry run pythonboilerplate")


@pytest.mark.slow()
def test_bake_and_run_pre_commit(copier):
    custom_answers = {"package_type": "cli"}
    project = copier.copy(**custom_answers)

    project.run("git init")
    project.run("git add .")
    project.run("git commit -m init")

    project.run("pre-commit run --all-files")
