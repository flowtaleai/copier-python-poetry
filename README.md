# Copier template for python

Opinionated copier template for Flowtale python projects.

## Features

| Task                 | Tool                                                         |
| -------------------- | ------------------------------------------------------------ |
| Testing framework    | pytest, unittest                                             |
| Test mocking         | pytest-mock                                                  |
| Pre-commit hooks     | pre-commit                                                   |
| Version management   | bump2version                                                 |
| Common style         | EditorConfig                                                 |
| Editor configuration | vscode with suggested extensions                             |
| Autoformatters       | black with experimental string processing (`--preview`), pydocstyle |
| Linters              | flake8, pydocstyle                                           |
| Test and packaging   | gitlab-ci                                                    |
| Run common commands  | make                                                         |

## Install
### Dependencies

Dependencies to create the project template with copier

- python (suggested install method: system)
- copier [suggested install method: pipx]

Dependencies for the project

- [poetry](https://python-poetry.org/docs#installation)
- [pyenv](https://github.com/pyenv/pyenv#getting-pyenv) (recommended)

### Development environment configuration

These configurations are required to setup the development environment and need to be performed only once.

#### poetry

(Recommended) To make poetry use the python interpreter of pyenv (defined in the `.python-version` file inside the project)

```bash
poetry config virtualenvs.prefer-active-python true
```

(Optional) To create the virtual envs within the project folder

```bash
poetry config virtualenvs.in-project true
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

## Usage

### Project initialization


1. Create a new project based on this copier template (it can also be applied to existing projects)

   ```bash
   copier copy https://gitlab.flowtale.ai/flowtale/cookiecutter-python project-folder
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

   (Opinion) It is always better to commit the lock file by itself given that reverting a commit with an update to the lock file is complicated.

6. Follow the project `README` to configure the project development environment

### Project update

1. From within a project folder that has already been initialized with the template run

   ```bash
   copier update --defaults
   ```

   This will update our project with the version corresponding to the most recent tag of the template. It will perform a three way merge between out project and the newest changes introduced by the template.

   Do not provide the `--defaults` flag if you want to change some of the original answers.

### Copier parameters

| Name                        | Example                     | Description                                                  |
| --------------------------- | --------------------------- | ------------------------------------------------------------ |
| author_name                 | Team Faboulous              |                                                              |
| author_email                | teamfaboulous@mycompany.com |                                                              |
| project_name                | Awsome Project              | Name of the project                                          |
| package_name                | awsomeproject               | Used to define the name of the python package                |
| repository_name             | awsome-project              | Name of the project repository                               |
| project_short_description   | A fantastic new project     | Description of the project. Also used in the CLI help.       |
| version                     | 0.1.0                       | SemVer 2.0 version                                           |
| license                     | MIT                         | Project license                                              |
| package_type                | cli                      | If `cli` generate cli module with argument parser and  cli entrypoint |
| python_version              | 3.10                        | Define the python version to use for `pyenv` and the CI pipelines |
| testing_framework           | pytest                      | Python testing framework                                     |
| max_line_length             | 88                          | Code max line length                                         |
| use_flake8_strict_plugins   | true                  | If `true` install flake8 plugins that allow to catch bugs, security vulnerabilities and apply more strict rules. They can be a bit overwhelming. |
| ide                         | vscode                      | Define the IDE(s) used by the developers.                    |
| git_hosting                 | gitlab                      | Define GIT hosting that will be used.                        |


## Usage

### VSCode

- VSCode should automatically detect the virtual environment if poetry is configured to store the venv in a subfolder of the project.
- Otherwise manually select the interpreter with `Python: Select interpreter`
    - Run `poetry run poetry env info -p` to discover where it is located

### Shell

- To perform actions in the shell

    - explicitly activate the virtual environment

        ```bash
        poetry shell
        ```

    - Or run commands in the virtual environment

      ```bash
      poetry run COMMAND
      ```

### Automatisms

#### On save (vscode)

- Code formatted with `black`
- Import sorted with `isort`

#### On commit

pre-commit is executed automatically before each commit in order to prevent code that does not follow the project guidelines.

Some pre-commit hooks modify the files. Re-stage them after the modification.

Checks

- Trailing whitespaces removed
- Add newline at the end of the file
- Check for big file added to commit
- `flake8` linter executed
- `black` formatter executed
- `isort` import sorted executed
- `pydocstyle` docstring checker executed

#### Linter plugins

| Name                | Description                                                  | strict |
| ------------------- | ------------------------------------------------------------ | ------ |
| flake8-builtins     | Check for python builtins being used as variables or parameters. |        |
| pep8-naming         | Check your code against [PEP 8](https://www.python.org/dev/peps/pep-0008/) naming conventions. |        |
| flake8-pytest-style | Check for common style issues or inconsistencies with `pytest`-based tests. |        |
| flake8-print        | Forbids print in the code besides `cli.py` (use `logging`!)  | x      |
| flake8-return       | Flake8 plugin that checks return values.                     | x      |
| flake8-eradicate    | Find commented out (or so called "dead") code.               | x      |
| flake8-bugbear      | Find likely bugs and design problems in your program         | x      |
| flake8-bandit       | Automated security testing built right into your workflow!   | x      |

#### On push

- Tests and pre-commit on all files executed on the CI

## Style suggestions

- Docstrings convention is `google` without types (types are specified using standard python typing)
- Use `pathlib.Path` instead of `str` for file names
- Use `pathlib.Path` to process files instead of `os`

## Rationale

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
