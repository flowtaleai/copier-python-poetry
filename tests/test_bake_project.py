import shutil

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
    assert ".gitattributes" in found_toplevel_files
    assert "tests" in found_toplevel_files

    assert ".vscode" in found_toplevel_files

    assert ".gitlab-ci.yml" not in found_toplevel_files
    assert "bitbucket-pipelines.yml" not in found_toplevel_files

    assert "Pipfile" not in found_toplevel_files
    assert "bitbucket-pipelines.yml" not in found_toplevel_files

    assert (project.path / "src" / "python_boilerplate").exists()
    assert not (project.path / "docs").exists()


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


def test_bake_namespaced_library(tmp_path, copier):
    custom_answers = {
        "package_type": "library",
        "package_name": "flowtale.copier.template",
    }
    project = copier.copy(tmp_path, **custom_answers)
    package_path = project.path / "src"

    assert list(package_path.iterdir())[0].name == "flowtale"
    assert list((package_path / "flowtale").iterdir())[0].name == "copier"
    assert list((package_path / "flowtale" / "copier").iterdir())[0].name == "template"


def test_bake_app_and_check_cli_scripts(tmp_path, copier):
    custom_answers = {"package_type": "cli"}
    project = copier.copy(tmp_path, **custom_answers)

    assert project.path.is_dir()
    pyproject_path = project.path / "pyproject.toml"
    assert_str = (
        '[tool.poetry.scripts]\npython_boilerplate = "python_boilerplate.cli:app"'
    )
    assert assert_str in pyproject_path.read_text()


def test_bake_bitbucket(tmp_path, copier):
    custom_answers = {"git_hosting": "bitbucket"}
    project = copier.copy(tmp_path, **custom_answers)

    found_toplevel_files = [f.name for f in project.path.glob("*")]
    assert "bitbucket-pipelines.yml" in found_toplevel_files
    assert ".github" not in found_toplevel_files
    assert ".gitlab-ci.yml" not in found_toplevel_files


def test_bake_gitlab(tmp_path, copier):
    custom_answers = {"git_hosting": "gitlab"}
    project = copier.copy(tmp_path, **custom_answers)

    found_toplevel_files = [f.name for f in project.path.glob("*")]
    assert "bitbucket-pipelines.yml" not in found_toplevel_files
    assert ".github" not in found_toplevel_files
    assert ".gitlab-ci.yml" in found_toplevel_files


def test_bake_github(tmp_path, copier):
    custom_answers = {"git_hosting": "github"}
    project = copier.copy(tmp_path, **custom_answers)

    found_toplevel_files = [f.name for f in project.path.glob("*")]
    assert "bitbucket-pipelines.yml" not in found_toplevel_files
    assert ".gitlab-ci.yml" not in found_toplevel_files
    github_workflow_path = project.path / ".github/workflows/ci.yml"
    assert github_workflow_path.exists()


def test_bake_gitlab_and_unittest(tmp_path, copier):
    custom_answers = {"git_hosting": "gitlab", "testing_framework": "unittest"}
    project = copier.copy(tmp_path, **custom_answers)

    gitlab_ci_path = project.path / ".gitlab-ci.yml"
    assert "poetry run python -m unittest discover" in gitlab_ci_path.read_text()


@pytest.mark.slow
@pytest.mark.venv
def test_bake_and_run_cli(tmp_path, copier):
    custom_answers = {"package_type": "cli"}
    project = copier.copy(tmp_path, **custom_answers)

    project.run("poetry install --only main")
    project.run("poetry run python_boilerplate")


@pytest.mark.venv
def test_bake_and_bump_version(tmp_path, copier):
    custom_answers = {"package_type": "cli"}
    project = copier.copy(tmp_path, **custom_answers)

    project.run("poetry run bump2version minor")


@pytest.mark.slow
@pytest.mark.venv
def test_bake_defaults_and_run_pre_commit(tmp_path, copier):
    custom_answers = {"package_type": "cli"}
    project = copier.copy(tmp_path, **custom_answers)

    project.run("git init")
    project.run("git add .")
    project.run("git config user.name 'User Name'")
    project.run("git config user.email 'user@email.org'")
    project.run("git commit -m init")

    std_pre_commit_path = project.path / ".pre-commit-config.standard.yaml"
    strict_pre_commit_path = project.path / ".pre-commit-config.addon.strict.yaml"
    dst_pre_commit_path = project.path / ".pre-commit-config.yaml"
    shutil.copy(std_pre_commit_path, dst_pre_commit_path)
    with dst_pre_commit_path.open("a") as f:
        f.write(strict_pre_commit_path.read_text())

    project.run("poetry install")
    project.run("poetry run pre-commit run --all-files")


@pytest.mark.slow
@pytest.mark.venv
def test_make_bump_updates_version_in_selected_files(tmp_path, copier):
    custom_answers = {"package_name": "mypackage"}
    project = copier.copy(tmp_path, **custom_answers)

    project.run("git init")
    project.run("git add .")
    project.run("git config user.name 'User Name'")
    project.run("git config user.email 'user@email.org'")
    project.run("git commit -m init")
    project.run("poetry run bump2version major")

    copier_answers_path = project.path / ".copier-answers.yml"
    pyproject_path = project.path / "pyproject.toml"
    project_init = project.path / "src" / "mypackage" / "__init__.py"

    assert "1.0.0" in copier_answers_path.read_text()
    assert "1.0.0" in pyproject_path.read_text()
    assert "1.0.0" in project_init.read_text()


def test_bake_with_code_examples(tmp_path, copier):
    custom_answers = {
        "use_jupyter_notebooks": True,
        "generate_example_code": True,
    }
    project = copier.copy(tmp_path, **custom_answers)

    package_name = project.answers["package_name"]
    if "." in package_name:
        package_test_name = package_name.replace(".", "_")
        package_namespace = package_name.replace(".", "/")
    else:
        package_namespace = package_name
        package_test_name = package_name
    main_module_example_path = project.path / "src" / package_namespace / "core.py"
    main_module_test_example_path = (
        project.path / "tests" / f"test_{package_test_name}.py"
    )
    jupyter_notebook_example_path = (
        project.path / "notebooks" / "example_notebook.ipynb"
    )

    assert main_module_example_path.exists() is True
    assert main_module_test_example_path.exists() is True
    assert jupyter_notebook_example_path.exists() is True


def test_bake_without_code_examples(tmp_path, copier):
    custom_answers = {"use_jupyter_notebooks": True, "generate_example_code": False}
    project = copier.copy(tmp_path, **custom_answers)

    package_name = project.answers["package_name"]
    if "." in package_name:
        package_test_name = package_name.replace(".", "_")
        package_namespace = package_name.replace(".", "/")
    else:
        package_namespace = package_name
        package_test_name = package_name
    main_module_example_path = project.path / "src" / package_namespace / "core.py"
    main_module_test_example_path = (
        project.path / "tests" / f"test_{package_test_name}.py"
    )
    jupyter_notebook_example_path = (
        project.path / "notebooks" / "example_notebook.ipynb"
    )
    assert main_module_example_path.exists() is False
    assert main_module_test_example_path.exists() is False
    assert jupyter_notebook_example_path.exists() is False


@pytest.mark.parametrize(
    ("framework", "frontpage_path"),
    [
        ("pdoc", "build/site/python_boilerplate.html"),
        ("mkdocs", "build/site/index.html"),
    ],
)
def test_bake_with_documentation(tmp_path, copier, framework, frontpage_path):
    custom_answers = {"generate_docs": framework}
    project = copier.copy(tmp_path, **custom_answers)

    project.run("git init")
    project.run("make setup")
    project.run("make docs")

    # Check that index.html exists
    frontpage_path = project.path / frontpage_path
    assert frontpage_path.exists()

    # Check that readme is displayed on frontpage
    title = project.answers["package_name"] or project.answers["distribution_name"]
    with open(frontpage_path) as index:
        front_page = "\n".join(index.readlines())
    assert title in front_page
    assert "Usage" in front_page


def test_bake_with_many_files(tmp_path, copier):
    custom_answers = {
        "use_jupyter_notebooks": True,
        "strip_jupyter_outputs": True,
        "generate_example_code": True,
        "generate_dockerfile": True,
        "generate_docs": "mkdocs",
        "type_checker": "mypy",
        "type_checker_strictness": "strict",
        "ide": "vscode",
        "package_type": "cli",
    }
    project = copier.copy(tmp_path, **custom_answers)

    package_name = project.answers["package_name"]
    if "." in package_name:
        package_test_name = package_name.replace(".", "_")
        package_namespace = package_name.replace(".", "/")
    else:
        package_namespace = package_name
        package_test_name = package_name
    main_module_example_path = project.path / "src" / package_namespace / "core.py"
    main_module_test_example_path = (
        project.path / "tests" / f"test_{package_test_name}.py"
    )
    # Jupyter
    jupyter_notebook_example_path = (
        project.path / "notebooks" / "example_notebook.ipynb"
    )
    # Docs
    mkdocs_config_filepath = project.path / "mkdocs.yml"
    mkdocs_dir_path = project.path / "docs"
    # Dockerfile
    dockerfile_path = project.path / "Dockerfile"

    assert main_module_example_path.exists() is True
    assert main_module_test_example_path.exists() is True
    assert jupyter_notebook_example_path.exists() is True
    assert mkdocs_config_filepath.exists() is True
    assert mkdocs_dir_path.exists() is True
    assert dockerfile_path.exists() is True


@pytest.mark.slow
@pytest.mark.venv
def test_bake_with_many_and_run_pre_commit(tmp_path, copier):
    custom_answers = {
        "use_jupyter_notebooks": True,
        "strip_jupyter_outputs": True,
        "generate_example_code": True,
        "generate_dockerfile": True,
        "generate_docs": "mkdocs",
        "type_checker": "mypy",
        "type_checker_strictness": "strict",
        "ide": "vscode",
        "package_type": "cli",
    }
    project = copier.copy(tmp_path, **custom_answers)

    project.run("git init")
    project.run("git add .")
    project.run("git config user.name 'User Name'")
    project.run("git config user.email 'user@email.org'")
    project.run("git commit -m init")

    std_pre_commit_path = project.path / ".pre-commit-config.standard.yaml"
    strict_pre_commit_path = project.path / ".pre-commit-config.addon.strict.yaml"
    dst_pre_commit_path = project.path / ".pre-commit-config.yaml"
    shutil.copy(std_pre_commit_path, dst_pre_commit_path)
    with dst_pre_commit_path.open("a") as f:
        f.write(strict_pre_commit_path.read_text())

    project.run("poetry install")
    project.run("poetry run pre-commit run --all-files")


def test_bake_namespaced_package_with_many_files(tmp_path, copier):
    custom_answers = {
        "package_name": "company.mypackage",
        "use_jupyter_notebooks": True,
        "strip_jupyter_outputs": True,
        "generate_example_code": True,
        "generate_dockerfile": True,
        "generate_docs": "mkdocs",
        "type_checker": "mypy",
        "type_checker_strictness": "strict",
        "ide": "vscode",
        "package_type": "cli",
    }
    project = copier.copy(tmp_path, **custom_answers)

    package_name = project.answers["package_name"]
    if "." in package_name:
        package_namespace = package_name.replace(".", "/")
        package_test_name = package_name.replace(".", "_")
    else:
        package_namespace = package_name
        package_test_name = package_name
    main_module_example_path = project.path / "src" / package_namespace / "core.py"
    main_module_test_example_path = (
        project.path / "tests" / f"test_{package_test_name}.py"
    )
    # Jupyter
    jupyter_notebook_example_path = (
        project.path / "notebooks" / "example_notebook.ipynb"
    )
    # Docs
    mkdocs_config_filepath = project.path / "mkdocs.yml"
    mkdocs_dir_path = project.path / "docs"
    # Dockerfile
    dockerfile_path = project.path / "Dockerfile"

    assert main_module_example_path.exists() is True
    assert main_module_test_example_path.exists() is True
    assert jupyter_notebook_example_path.exists() is True
    assert mkdocs_config_filepath.exists() is True
    assert mkdocs_dir_path.exists() is True
    assert dockerfile_path.exists() is True


@pytest.mark.slow
@pytest.mark.venv
def test_bake_namespaced_package_with_many_and_run_pre_commit(tmp_path, copier):
    custom_answers = {
        "package_name": "company.mypackage",
        "use_jupyter_notebooks": True,
        "strip_jupyter_outputs": True,
        "generate_example_code": True,
        "generate_dockerfile": True,
        "generate_docs": "mkdocs",
        "type_checker": "mypy",
        "type_checker_strictness": "strict",
        "ide": "vscode",
        "package_type": "cli",
    }
    project = copier.copy(tmp_path, **custom_answers)

    project.run("git init")
    project.run("git add .")
    project.run("git config user.name 'User Name'")
    project.run("git config user.email 'user@email.org'")
    project.run("git commit -m init")

    std_pre_commit_path = project.path / ".pre-commit-config.standard.yaml"
    strict_pre_commit_path = project.path / ".pre-commit-config.addon.strict.yaml"
    dst_pre_commit_path = project.path / ".pre-commit-config.yaml"
    shutil.copy(std_pre_commit_path, dst_pre_commit_path)
    with dst_pre_commit_path.open("a") as f:
        f.write(strict_pre_commit_path.read_text())

    project.run("poetry install")
    project.run("poetry run pre-commit run --all-files")


@pytest.mark.parametrize("git_hosting", ["github", "gitlab", "bitbucket"])
def test_poetry_version_consistency(tmp_path, copier, git_hosting):
    custom_answers = {
        "poetry_version": "1.8.3",
        "generate_dockerfile": True,
        "git_hosting": git_hosting,
    }
    project = copier.copy(tmp_path, **custom_answers)

    # Check Dockerfile
    dockerfile_path = project.path / "Dockerfile"
    assert "POETRY_VERSION=1.8.3" in dockerfile_path.read_text()

    # Check CI files
    if git_hosting == "github":
        ci_path = project.path / ".github" / "workflows" / "ci.yml"
        assert 'POETRY_VERSION: "1.8.3"' in ci_path.read_text()
    elif git_hosting == "gitlab":
        ci_path = project.path / ".gitlab-ci.yml"
        assert "pip install poetry==1.8.3" in ci_path.read_text()
    elif git_hosting == "bitbucket":
        ci_path = project.path / "bitbucket-pipelines.yml"
        assert "pip install poetry==1.8.3" in ci_path.read_text()

    # Check CONTRIBUTING.md
    contributing_path = project.path / "CONTRIBUTING.md"
    assert "Poetry 1.8.3" in contributing_path.read_text()

    # Check devcontainer
    devcontainer_path = project.path / ".devcontainer" / "devcontainer.json"
    assert 'poetry:2": { "version": "1.8.3" }' in devcontainer_path.read_text()


@pytest.mark.slow
@pytest.mark.venv
def test_mypy_exclude_respected_in_pre_commit(tmp_path, copier):
    """Test that mypy respects exclude patterns in pyproject.toml.

    Creates a file with type errors and verifies pre-commit passes
    when the file is explicitly excluded in mypy configuration.
    """
    custom_answers = {
        "type_checker": "mypy",
        "type_checker_strictness": "strict",
        "package_name": "mypackage",  # Specify a fixed package name
    }
    project = copier.copy(tmp_path, **custom_answers)

    project.run("git init")
    project.run("git add .")
    project.run("git config user.name 'User Name'")
    project.run("git config user.email 'user@email.org'")
    project.run("git commit -m init")

    # Create a file with type errors in src directory
    src_dir = project.path / "src" / "mypackage"
    src_file_with_error = src_dir / "exclude_me.py"
    src_file_with_error.write_text(
        "def src_function_with_type_error() -> str:\n"
        '    """Add random docstring here to avoid pre-commit error."""\n'
        "    return 999  # Type error: Incompatible return value\n"
    )

    # Modify pyproject.toml to exclude the specific file
    pyproject_path = project.path / "pyproject.toml"
    pyproject_content = pyproject_path.read_text()
    src_exclude_path = "src/mypackage/exclude_me.py"
    updated_content = pyproject_content.replace(
        'exclude = ["tests/*", "docs/*"]',
        f'exclude = ["tests/*", "docs/*", "{src_exclude_path}"]',
    )
    pyproject_path.write_text(updated_content)

    # Stage and commit the new file and changes
    project.run(f"git add {src_exclude_path} pyproject.toml")
    project.run(
        "git commit -m 'Add file with type errors in src directory and update mypy"
        " excludes'"
    )

    std_pre_commit_path = project.path / ".pre-commit-config.standard.yaml"
    strict_pre_commit_path = project.path / ".pre-commit-config.addon.strict.yaml"
    dst_pre_commit_path = project.path / ".pre-commit-config.yaml"
    shutil.copy(std_pre_commit_path, dst_pre_commit_path)
    with dst_pre_commit_path.open("a") as f:
        f.write(strict_pre_commit_path.read_text())

    project.run("poetry install")
    project.run("poetry run pre-commit run --all-files")
