# Copier template for python

Opinionated copier template for Flowtale python projects.

## Features

| Task                   | Tool                                                         |
| ---------------------- | ------------------------------------------------------------ |
| Command line interface | Typer                                                        |
| Testing framework      | pytest, unittest                                             |
| Test mocking           | pytest-mock                                                  |
| Pre-commit hooks       | pre-commit                                                   |
| Version management     | bump2version                                                 |
| Environment management | direnv                                                       |
| Common style           | EditorConfig                                                 |
| Editor configuration   | vscode with suggested extensions                             |
| Autoformatters         | ruff  |
| Linters                | ruff  |
| Test and packaging     | gitlab-ci                                                           |
| Type Checkers          | mypy                                                                |
| Run common commands    | make                                                                |

### Automatisms

#### On save (vscode)

- Code formatted with `ruff`
- Import sorted with ruff's `isort`

#### On commit

pre-commit is executed automatically before each commit in order to prevent code that does not follow the project guidelines. Depending on the user configuration either only the standard checks or all the checks are run on commit.

Some pre-commit hooks modify the files. Re-stage them after the modification.

Standard checks:

- Check for big file added to commit
- Check for committed secrets

Strict checks:

- Trailing whitespaces removed
- Add newline at the end of the file
- `ruff` linter executed
- `ruff` formatter executed

#### On push

- Tests and run all the pre-commit checks on all files executed on the CI

## Usage

### Project initialization

1. Create a new project based on this copier template (it can also be applied to existing projects)

   ```bash
   copier copy https://github.com/flowtaleai/copier-python-poetry.git project-folder
   ```

   The template version used corresponds to the most recent tag of the template repository.

2. Answer all the questions to configure the project (see [Copier parameters](#copier-parameters))

3. Commit all the files

   ```bash
   cd pythonboilerplate
   git init
   git add .
   git commit -m "initial commit"
   ```

4. Generate the poetry lock file

   ```bash
   make setup-strict
   ```

5. Commit the lock file

   ```bash
   git add uv.lock
   git commit -m "add lock file"
   ```

   (Opinion) It is always better to commit the lock file by itself given that reverting a commit with an update to the lock file is complicated.

6. Follow the project `CONTRIBUTING.md` to configure the project development environment

### Project update

1. From within a project folder that has already been initialized with the template run

   ```bash
   copier update --skip-answered
   ```

   This will update our project with the version corresponding to the most recent tag of the template. It will perform a three way merge between out project and the newest changes introduced by the template.

   Do not provide the `--skip-answered` flag if you want to change some of the original answers.

2. Run `poetry lock` to regenerate the poetry lock file given that the `pyproject.toml` may have been updated
3. Run `poetry install --sync`  to update the project dependencies

### Copier parameters

| Name                      | Example                     | Description                                                                                                                                      |
|---------------------------|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| author_name               | Team Faboulous              |                                                                                                                                                  |
| author_email              | <teamfaboulous@mycompany.com> |                                                                                                                                                  |
| package_name              | awsomeproject               | Used to define the name of the python package. This can include "." if you need to create a namespaced package.                                                                                                    |
| distribution_name         | awsome-project              | Used to define the name of the python distribution                                                                                               |
| project_name              | Awsome Project              | Name of the project                                                                                                                              |
| repository_name           | awsome-project              | Name of the project repository                                                                                                                   |
| project_short_description | A fantastic new project     | Description of the project. Also used in the CLI help.                                                                                           |
| version                   | 0.2.0                       | SemVer 2.0 version                                                                                                                               |
| license                   | MIT                         | Project license                                                                                                                                  |
| package_type              | cli                         | If `cli` generate cli module with argument parser and  cli entrypoint                                                                            |
| python_version            | 3.10                        | Define the python version to use for `pyenv` and the CI pipelines                                                                                |
| testing_framework         | pytest                      | Python testing framework                                                                                                                         |
| max_line_length           | 88                          | Code max line length                                                                                                                             |
| type_checker | mypy | Select whether to add a type checker |
| type_checker_strictness | strict | Decide whether to support gradual typing or not  |
| ide                       | vscode                      | Define the IDE(s) used by the developers.                                                                                                        |
| git_hosting               | gitlab                      | Define GIT hosting that will be used.                                                                                                            |
| use_jupyter_notebooks     | true                        | If `true` install ipykernel dependency                                                                                                           |
| generate_example_code     | true                        | If `true` generate example files and code snippets                                                                                               |
| strip_jupyter_outputs     | true                        | If `true` strip output from Jupyter notebooks before committing                                                                                  |
| generate_docs             | mkdocs                      | Generate documentation with either `pdoc` or `mkdocs`    |

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to contribute to this project.

## Rationale

- [2024-08-19] We allow for a choice between generating documentation with either MkDocs or pdoc. The former is more powerful, using mostly additional Markdown files. The latter is more straightforward and uses only the doc-strings in the code files. For both choices, the README.md files is rendered as the front page of the documentation.

- [2023-10-10] We pass the `--preview` flag to black 23.x in particular to format long strings. The effects of `--preview` should be re-evaluated at each major version update of black.

  ```python
  # before formatting
  myvar = "Loooong ... string"

  # after formatting
  myvar = (
      "Loooong ..."
      "... string"
  )
  ```

- The versions of python dependencies of the tools (black, flake, ...) are managed by the copier template and should not be changed manually in the generated projects. This allows to keep the various projects aligned and have a consistent behavior when we develop on multiple projects. Sometimes a newer copier template version may be applied to a project before the others, so there is a period where there is a disalignment, but at least is a controlled one.

- typing annotations are not checked in the tests because tests do not need to be perfect and we want to be able to write them fast.
