# Contributing to Copier Python Poetry

This document provides guidelines for contributing to the Copier Python Poetry template project.

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

(Recommended) To make poetry use the python interpreter of pyenv (defined in the `.python-version` file inside the project)

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

direnv is a tool that enables automatic loading and unloading of directory-specific environment variables. It is useful to automatically activate the virtual environment and load any project specific environment variables when entering a project folder. Because this template expects the use of poetry, the `.envrc` file accompanying the template includes a function to automatically load a poetry virtual environment, and will also load project specific environment variables from any present `.env` file with the dotenv command.

To make use of direnv, make sure it is installed. Go to the project root directory (where the `.envrc` file is located) and run `direnv allow`.

## Project development

### python dependencies

- Do not manually change the [dependency specification](https://python-poetry.org/docs/dependency-specification/) of the python packages related to the copier template (i.e. do not change the version in pyproject.toml). These will be automatically updated when we apply an update of the copier template.

#### VSCode

- VSCode should automatically detect the virtual environment if poetry is configured to store the venv in a subfolder of the project (it is by default).
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

#### Docker

When the Copier template has the CLI option activated (rather than the library option), there is a downstream option to generate a Dockerfile. This is useful for running the CLI in a containerized environment. The Dockerfile includes build arguments to add authentication credentials for private Python package registries configured via Poetry.

## Contributing

- The python dependencies in the template should be update periodically
  - Updating the major version of black may require reformatting large portions of a project codebase to make the CI lint stage pass

- A note to the [Rationale](README.md#rationale) section should be added if it helps explaining non-obvious choices

### Versioning

- This project is tagged with versions according to [SemVer](https://semver.org/).

- The version has a format `MAJOR.MINOR.PATCH`, which in the context of this project means:

  - Major: Changes that modify the generated project structure or components significantly in a way that is not backward-compatible.
    - e.g. updating the black major version
    - e.g. add a required flake8 plugin that may cause the CI pipeline of an existing project to fail
  - Minor: Additions or enhancements to the template that do not alter the existing structure in a backward-incompatible way.
    - e.g. add support for generating the documentation
  - Patch: Fixes to issues or bugs in the template that do not affect the generated project's structure or compatibility.

- To bump the project version:

  ```bash
  make bump
  ```

​  and select the part of the version to bump
