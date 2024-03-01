# Copier template for python

Opinionated copier template for Flowtale python projects.

## Features

| Task                   | Tool                                                                |
|------------------------|---------------------------------------------------------------------|
| Testing framework      | pytest, unittest                                                    |
| Test mocking           | pytest-mock                                                         |
| Pre-commit hooks       | pre-commit                                                          |
| Version management     | bump2version                                                        |
| Environment management | direnv                                                              |
| Common style           | EditorConfig                                                        |
| Editor configuration   | vscode with suggested extensions                                    |
| Autoformatters         | black with experimental string processing (`--preview`), pydocstyle |
| Linters                | flake8, pydocstyle                                                  |
| Test and packaging     | gitlab-ci                                                           |
| Run common commands    | make                                                                |

### Automatisms

#### On save (vscode)

- Code formatted with `black`
- Import sorted with `isort`

#### On commit

pre-commit is executed automatically before each commit in order to prevent code that does not follow the project
guidelines. Depending on the user configuration either only the standard checks or all the checks are run on commit.

Some pre-commit hooks modify the files. Re-stage them after the modification.

Standard checks:

- Check for big file added to commit
- Check for committed secrets

Strict checks:

- Trailing whitespaces removed
- Add newline at the end of the file
- `flake8` linter executed
- `black` formatter executed
- `isort` import sorted executed
- `pydocstyle` docstring checker executed

#### Linter plugins

| Name                | Description                                                                                    | strict |
|---------------------|------------------------------------------------------------------------------------------------|--------|
| flake8-builtins     | Check for python builtins being used as variables or parameters.                               |        |
| pep8-naming         | Check your code against [PEP 8](https://www.python.org/dev/peps/pep-0008/) naming conventions. |        |
| flake8-pytest-style | Check for common style issues or inconsistencies with `pytest`-based tests.                    |        |
| flake8-print        | Forbids print in the code besides `cli.py` (use `logging`!)                                    | x      |
| flake8-eradicate    | Find commented out (or so called "dead") code.                                                 | x      |
| flake8-bugbear      | Find likely bugs and design problems in your program                                           | x      |
| flake8-annotations  | Find missing type annotations                                                                  | x      |

#### On push

- Tests and run all the pre-commit checks on all files executed on the CI

## Setup

### Dependencies

Dependencies to create the project template with copier

- python (suggested install method: system)
- copier (suggested install method: pipx)

Dependencies for the project

- [poetry](https://python-poetry.org/docs#installation)
- [pyenv](https://github.com/pyenv/pyenv#getting-pyenv) (recommended)

### Development environment configuration

These configurations are required to setup the development environment and need to be performed only once.

#### poetry

(Recommended) To make poetry use the python interpreter of pyenv (defined in the `.python-version` file inside the
project)

```bash
poetry config virtualenvs.prefer-active-python true
```

This setting allows to easier to rename the project folder without having to recreated the virtual environment. It
also makes vscode automatically detected the poetry virtual environment (see [VScode](#vscode))

#### pyenv (recommended)

This step can be skipped if the system python version always matches the version specified in the `.python-version` of
the project (very unlikely).

Add the following to `~/.bashrc` or `~/.zshrc` to initialize `pyenv`

```
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

#### direnv (recommended)

direnv is a tool that enables automatic loading and unloading of directory-specific environment variables. It is useful
to automatically activate the virtual environment and load any project specific environment variables when entering a
project folder. Because this template expects the use of poetry, the `.envrc` file accompanying the template includes a
function to automatically load a poetry virtual environment, and will also load project specific environment variables
from any present `.env` file with the dotenv command.

To make use of direnv, make sure it is installed. Go to the project root directory (where the `.envrc` file is located)
and run `direnv allow`.

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
   git commit -m "Initial commit"
   ```

4. Generate the poetry lock file

   ```bash
   poetry install
   ```

5. Commit the lock file

   ```bash
   git add poetry.lock
   git commit -m "Poetry lock file regenerated"
   ```

   (Opinion) It is always better to commit the lock file by itself given that reverting a commit with an update to the
   lock file is complicated.

6. Follow the project `README` to configure the project development environment

### Project update

1. From within a project folder that has already been initialized with the template run

   ```bash
   copier update --skip-answered
   ```

   This will update our project with the version corresponding to the most recent tag of the template. It will perform a
   three way merge between out project and the newest changes introduced by the template.

   Do not provide the `--skip-answered` flag if you want to change some of the original answers.

2. Run `poetry lock` to regenerate the poetry lock file given that the `pyproject.toml` may have been updated
3. Run `poetry install --sync`  to update the project dependencies

### Copier parameters

| Name                      | Example                     | Description                                                                                                                                      |
|---------------------------|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| author_name               | Team Faboulous              |                                                                                                                                                  |
| author_email              | teamfaboulous@mycompany.com |                                                                                                                                                  |
| distribution_name         | awsome-project              | Used to define the name of the python distribution                                                                                               |
| package_name              | awsome_project              | Used to define the name of the python package                                                                                                    |
| project_name              | Awsome Project              | Name of the project                                                                                                                              |
| repository_name           | awsome-project              | Name of the project repository                                                                                                                   |
| project_short_description | A fantastic new project     | Description of the project. Also used in the CLI help.                                                                                           |
| version                   | 0.1.0                       | SemVer 2.0 version                                                                                                                               |
| license                   | MIT                         | Project license                                                                                                                                  |
| package_type              | cli                         | If `cli` generate cli module with argument parser and  cli entrypoint                                                                            |
| python_version            | 3.10                        | Define the python version to use for `pyenv` and the CI pipelines                                                                                |
| testing_framework         | pytest                      | Python testing framework                                                                                                                         |
| max_line_length           | 88                          | Code max line length                                                                                                                             |
| use_flake8_strict_plugins | true                        | If `true` install flake8 plugins that allow to catch bugs, security vulnerabilities and apply more strict rules. They can be a bit overwhelming. |
| ide                       | vscode                      | Define the IDE(s) used by the developers.                                                                                                        |
| git_hosting               | gitlab                      | Define GIT hosting that will be used.                                                                                                            |

### Project usage

### python dependencies

- Do not manually change the [dependency specification](https://python-poetry.org/docs/dependency-specification/) of the
  python packages related to the copier template (i.e. do not change the version in pyproject.toml). These will be
  automatically updated when we apply an update of the copier template.

#### VSCode

- VSCode should automatically detect the virtual environment if poetry is configured to store the venv in a subfolder of
  the project (it is by default).
- Otherwise manually select the interpreter with `Python: Select interpreter`
  - Run `poetry run poetry env info -p` to discover where it is located

#### Shell

- To perform actions in the shell

  - explicitly activate the virtual environment

      ```bash
      poetry shell
      ```

  - Or run commands in the virtual environment

    ```bash
    poetry run COMMAND
    ```

## Style suggestions

- Docstrings convention is `google` without types (types are specified using standard python typing)
- Use `pathlib.Path` instead of `str` for file names
- Use `pathlib.Path` to process files instead of `os`

## Contributing

- The python dependencies in the template should be update periodically
  - Updating the major version of black may require reformatting large portions of a project codebase to make the CI
    lint stage pass

- A note to the [Rationale][#rationale] section should be added if it helps explaining non-obvious choices

### Versioning

- This project is tagged with versions according to [SemVer](https://semver.org/).

- The version has a format `MAJOR.MINOR.PATCH`, which in the context of this project means:

  - Major: Changes that modify the generated project structure or components significantly in a way that is not
    backward-compatible.
    - e.g. updating the black major version
    - e.g. add a required flake8 plugin that may cause the CI pipeline of an existing project to fail
  - Minor: Additions or enhancements to the template that do not alter the existing structure in a backward-incompatible
    way.
    - e.g. add support for generating the documentation
  - Patch: Fixes to issues or bugs in the template that do not affect the generated project's structure or
    compatibility.

- To bump the project version:

```bash
make bump
```

​ and select the part of the version to bump

## Rationale

- [2023-10-10] We pass the `--preview` flag to black 23.x in particular to format long strings. The effects
  of `--preview` should be re-evaluated at each major version update of black.

  ```python
  # before formatting
  myvar = "Loooong ... string"

  # after formatting
  myvar = (
      "Loooong ..."
      "... string"
  )
  ```

- The versions of python dependencies of the tools (black, flake, ...) are managed by the copier template and should not
  be changed manually in the generated projects. This allows to keep the various projects aligned and have a consistent
  behavior when we develop on multiple projects. Sometimes a newer copier template version may be applied to a project
  before the others, so there is a period where there is a disalignment, but at least is a controlled one.

- typing annotations are not checked in the tests because tests do not need to be perfect and we want to be able to
  write them fast.
