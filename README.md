# Cookiecutter template for python

Opinionated cookiecutter for Flowtale python projects.

## Features

| Task                 | Tool                                                    |
| -------------------- | ------------------------------------------------------- |
| Testing framework    | pytest, unittest                                        |
| Test mocking         | pytest-mock                                             |
| Pre-commit hooks     | pre-commit                                              |
| Version management   | bump2version                                            |
| Common style         | EditorConfig                                            |
| Editor configuration | vscode with suggested extensions                        |
| Autoformatter        | black with experimental string processing (`--preview`) |
| Linter               | flake8                                                  |
| Test and packaging   | gitlab-ci                                               |
| Run common commands  | make                                                    |

## Dependencies

Dependencies to create the project template with cookiecutter

- python
- cookiecutter [pip]

Dependencies for the project

- [poetry](https://python-poetry.org/docs#installation)
- [pyenv](https://github.com/pyenv/pyenv#getting-pyenv) (recommended)

## Development environment configuration

These configurations are required to setup the development environment and need to be performed only once.

### poetry

To make poetry use the python interpreter of pyenv (defined in the `.python-version` file inside the project)

```bash
poetry config virtualenvs.prefer-active-python true
```

To create the virtual envs within the project folder (easier to rename the project folder and makes vscode happier)

```bash
poetry config virtualenvs.in-project true
```

### pyenv (recommended)

This step can be skipped if the system python version always matches the version specified in the `.python-version` of the project.

Add the following to `~/.bashrc` or `~/.zshrc` to initialize `pyenv`

```
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

### cookiecutter (optional)

Create `~/.cookiecutterrc` to specify customized default values for new projects:

```ini
default_context:
  full_name: "Your Name"
  email: "initials@flowtale.ai"
```

## Cookiecutter parameters

| Name                        | Example                     | Description                                                  | Depends on                  |
| --------------------------- | --------------------------- | ------------------------------------------------------------ | --------------------------- |
| full_name                   | Team Faboulous              |                                                              |                             |
| email                       | teamfaboulous@mycompany.com |                                                              |                             |
| gitlab_username             | faboulous                   | Username of the user/group owning the gitlab project         |                             |
| project_name                | Awsome Project              | Name of the project                                          |                             |
| project_slug                | awsomeproject               | Used to define the name of the python package                |                             |
| repository_name             | awsome-project              | Name of the project repository                               |                             |
| project_short_description   | A fantastic new project     | Description of the project. Also used in the CLI help.       |                             |
| version                     | 0.1.0                       | SemVer 2.0 version                                           |                             |
| license                     | MIT                         | Project license                                              |                             |
| app_or_lib                  | app                         | If `app` generate cli module with argument parser and  cli entrypoint |                             |
| python_version              | 3.10                        | Define the python version to use for `pyenv` and `gitlab-ci` |                             |
| testing_framework           | pytest                      | Python testing framework                                     |                             |
| max_line_length             | 88                          | Code max line length                                         |                             |
| use_flake8_strict_plugins   | y                           | If `y` install flake8 plugins that allow to catch bugs, security vulnerabilities and apply more strict rules. They can be a bit overwhelming. |                             |
| ide                         | vscode                      | Define the IDE(s) used by the developers.                    |                             |

## Project initialization

1. Create a new project based on this cookiecutter template

   ```bash
   cookiecutter https://gitlab.flowtale.ai/flowtale/cookiecutter-python
   ```

2. Answer all the questions to configure the project (see [cookiecutter parameters](#cookiecutter-parameters))

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
   git commit -m "Rigenerato poetry lock file"
   ```

   (Opinion) It is always better to commit the lock file by itself given that reverting a commit with an update to the lock file is complicated.

6. Follow the project `README` to configure the project development environment


## Developing

### VSCode

- VSCode should automatically detect the virtual environment if poetry is configured to store the venv in a subfolder of the project.
- Otherwise manually select the interpreter with `Select python interpreter...`
    - Run `poetry run poetry env info` to discover where it is located

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

## Automatisms

### On save (vscode)

- Code formatted with `black`
- Import sorted with `isort`

### On commit

Some pre-commit hooks modify the files. Re-stage them after the modification.

Checks

- Trailing whitespaces removed
- Add newline at the end of the file
- Check for big file added to commit
- `flake8` linter executed
- `black` formatter executed
- `isort` import sorted executed

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

### On push

- Tests executed on the CI

## Style suggestions

- TBD
