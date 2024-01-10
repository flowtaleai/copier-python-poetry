import pytest
from prompt_toolkit.validation import ValidationError


def test_bake_with_defaults(tmp_path, copier):
    project = copier.copy(tmp_path)

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

    assert ".vscode" in found_toplevel_files

    assert ".gitlab-ci.yml" not in found_toplevel_files
    assert "bitbucket-pipelines.yml" not in found_toplevel_files

    assert "Pipfile" not in found_toplevel_files
    assert "bitbucket-pipelines.yml" not in found_toplevel_files

    assert (project.path / "src" / "pythonboilerplate").exists()


def test_bake_and_run_tests_with_pytest_framework(tmp_path, copier):
    custom_answers = {"testing_framework": "pytest"}
    project = copier.copy(tmp_path, **custom_answers)

    project.run("pytest")


def test_bake_and_run_tests_with_unittest_framework(tmp_path, copier):
    custom_answers = {"testing_framework": "unittest"}
    project = copier.copy(tmp_path, **custom_answers)

    found_toplevel_files = [f.name for f in project.path.glob("*")]
    assert ".vscode" in found_toplevel_files
    assert ".idea" not in found_toplevel_files


def test_bake_with_proprietary_license(tmp_path, copier):
    custom_answers = {"license": "Proprietary"}
    project = copier.copy(tmp_path, **custom_answers)

    found_toplevel_files = [f.name for f in project.path.glob("*")]
    assert "LICENSE" not in found_toplevel_files


def test_bake_with_invalid_package_name(tmp_path, copier):
    custom_answers = {"package_name": "1invalid"}
    with pytest.raises(ValidationError):
        copier.copy(tmp_path, **custom_answers)


def test_bake_cli_application(tmp_path, copier):
    custom_answers = {"package_type": "cli"}
    project = copier.copy(tmp_path, **custom_answers)

    found_cli_script = [f.name for f in project.path.glob("**/cli.py")]
    assert found_cli_script


def test_bake_library(tmp_path, copier):
    custom_answers = {"package_type": "library"}
    project = copier.copy(tmp_path, **custom_answers)

    found_cli_script = [f.name for f in project.path.glob("**/cli.py")]
    assert not found_cli_script


def test_bake_app_and_check_cli_scripts(tmp_path, copier):
    custom_answers = {"package_type": "cli"}
    project = copier.copy(tmp_path, **custom_answers)

    assert project.path.is_dir()
    pyproject_path = project.path / "pyproject.toml"
    assert (
        '''[tool.poetry.scripts]
pythonboilerplate = "pythonboilerplate.cli:cli"'''
        in pyproject_path.read_text()
    )


def test_bake_bitbucket(tmp_path, copier):
    custom_answers = {"git_hosting": "bitbucket"}
    project = copier.copy(tmp_path, **custom_answers)

    found_toplevel_files = [f.name for f in project.path.glob("*")]
    assert "bitbucket-pipelines.yml" in found_toplevel_files
    assert ".gitlab-ci.yml" not in found_toplevel_files


@pytest.mark.slow()
@pytest.mark.venv()
def test_bake_and_run_cli(tmp_path, copier):
    custom_answers = {"package_type": "cli"}
    project = copier.copy(tmp_path, **custom_answers)

    project.run("poetry install --only main")
    project.run("poetry run pythonboilerplate")


@pytest.mark.venv()
def test_bake_and_bump_version(tmp_path, copier):
    custom_answers = {"package_type": "cli"}
    project = copier.copy(tmp_path, **custom_answers)

    project.run("poetry run bump2version minor")


@pytest.mark.slow()
def test_bake_and_run_pre_commit(tmp_path, copier):
    custom_answers = {"package_type": "cli"}
    project = copier.copy(tmp_path, **custom_answers)

    project.run("git init")
    project.run("git add .")
    project.run("git config user.name 'User Name'")
    project.run("git config user.email 'user@email.org'")
    project.run("git commit -m init")

    project.run("pre-commit run --all-files")
