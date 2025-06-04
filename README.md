# Copier Python Poetry

Opinionated copier template for python projects using poetry

## Features

| Task                   | Tool                                                    |
|------------------------|---------------------------------------------------------|
| Command line interface | Typer                                                   |
| Testing framework      | pytest, unittest                                        |
| Test mocking           | pytest-mock                                             |
| Pre-commit hooks       | pre-commit                                              |
| Version management     | bump2version                                            |
| Environment management | direnv                                                  |
| Common style           | EditorConfig                                            |
| Editor configuration   | vscode with suggested extensions                        |
| Autoformatters         | black with experimental string processing (`--preview`) |
| Linters                | ruff                                                    |
| Test and packaging     | gitlab-ci                                               |
| Type Checkers          | mypy                                                    |
| Run common commands    | make                                                    |

### Automatisms

#### On save (vscode)

- Code formatted with `black`

#### On commit

pre-commit is executed automatically before each commit in order to prevent code that does not follow the project guidelines. Depending on the user configuration either only the standard checks or all the checks are run on commit.

Some pre-commit hooks modify the files. Re-stage them after the modification.

Standard checks:

- Check for big file added to commit
- Check for committed secrets

Strict checks:

- Trailing whitespaces removed
- Add newline at the end of the file
- `black` formatter and `ruff` linter executed

#### Linter rules

| Name                           | Description                                                                  | strict |
|--------------------------------|------------------------------------------------------------------------------|--------|
| pyflakes                       | Check for syntax errors and undefined variables                              |        |
| pep8                           | Check for compliance with the PEP 8 style guide.                             |        |
| Ned Batchelder’s McCabe Script | Measure the complexity of functions and methods using cyclomatic complexity. |        |
| flake8-builtins                | Check for python builtins being used as variables or parameters.             |        |
| flake8-pytest-style            | Check for common style issues or inconsistencies with `pytest`-based tests.  |        |
| flake8-print                   | Forbids print in the code besides `cli.py` (use `logging`!)                  | x      |
| flake8-eradicate               | Find commented out (or so called "dead") code.                               | x      |
| flake8-bugbear                 | Find likely bugs and design problems in your program                         | x      |

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
   git commit -m "Initial commit"
   ```

4. Generate the poetry lock file

   ```bash
   make setup-strict
   ```

5. Commit the lock file

   ```bash
   git add poetry.lock
   git commit -m "Poetry lock file regenerated"
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
3. Run `poetry install`  to update the project dependencies

### Copier parameters

| Name                      | Example                       | Description                                                                                                                            |
|---------------------------|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| author_name               | Team Faboulous                |                                                                                                                                        |
| author_email              | <teamfaboulous@mycompany.com> |                                                                                                                                        |
| package_name              | awsomeproject                 | Used to define the name of the python package. This can include "." if you need to create a namespaced package.                        |
| distribution_name         | awsome-project                | Used to define the name of the python distribution                                                                                     |
| project_name              | Awsome Project                | Name of the project                                                                                                                    |
| repository_name           | awsome-project                | Name of the project repository                                                                                                         |
| project_short_description | A fantastic new project       | Description of the project. Also used in the CLI help.                                                                                 |
| version                   | 0.2.0                         | SemVer 2.0 version                                                                                                                     |
| license                   | MIT                           | Project license                                                                                                                        |
| package_type              | cli                           | If `cli` generate cli module with argument parser and  cli entrypoint                                                                  |
| python_version            | 3.10                          | Define the python version to use for `pyenv` and the CI pipelines                                                                      |
| testing_framework         | pytest                        | Python testing framework                                                                                                               |
| max_line_length           | 88                            | Code max line length                                                                                                                   |
| type_checker              | mypy                          | Select whether to add a type checker                                                                                                   |
| type_checker_strictness   | strict                        | Decide whether to support gradual typing or not                                                                                        |
| use_lint_strict_rules     | true                          | If `true` run linter with more rules. These could potentially catch bugs, security vulnerabilities etc. but can be a bit overwhelming. |
| ide                       | vscode                        | Define the IDE(s) used by the developers.                                                                                              |
| git_hosting               | gitlab                        | Define GIT hosting that will be used.                                                                                                  |
| use_jupyter_notebooks     | true                          | If `true` install ipykernel dependency                                                                                                 |
| generate_example_code     | true                          | If `true` generate example files and code snippets                                                                                     |
| strip_jupyter_outputs     | true                          | If `true` strip output from Jupyter notebooks before committing                                                                        |
| generate_docs             | mkdocs                        | Generate documentation with either `pdoc` or `mkdocs`                                                                                  |

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to contribute to this project.

## Rationale

- [2025-05-15] We made the following updates to the ruff configuration:
  - Moved maccabe into the strict linter rules
  - Added D105 to the list of rules to ignore. The reason was as follows:
    - D105: We decide to ignore it as we don't find it strictly necessary
  - Not ignored
    - ANN: We don't check for linter annotation errors anymore as we are using a type checker for that
    - B904: Even though this has been annoying for people, it does enforce much better behavior

- [2025-05-14] We use mypy mirror for type checking in pre-commit ([GitHub repo](https://github.com/pre-commit/mirrors-mypy)). The original solution did not respect the exclude patterns and other configuration settings in `pyproject.toml`, [see relevant issue](https://github.com/python/mypy/issues/16403#issuecomment-1812462399) that inspired us.

- [2025-03-06] We swap out isort, flake8 and pydocstring for ruff. Ruff is faster and better and we can reduce the amount of dependencies and separate config files needed to achieve the same (better) functionality.

- [2024-08-19] We allow for a choice between generating documentation with either MkDocs or pdoc. The former is more powerful, using mostly additional Markdown files. The latter is more straightforward and uses only the doc-strings in the code files. For both choices, the README.md files is rendered as the front page of the documentation.

- The versions of python dependencies of the tools (e.g. ruff) are managed by the copier template and should not be changed manually in the generated projects. This allows to keep the various projects aligned and have a consistent behavior when we develop on multiple projects. Sometimes a newer copier template version may be applied to a project before the others, so there is a period where there is a disalignment, but at least is a controlled one.

- typing annotations are not checked in the tests because tests do not need to be perfect and we want to be able to write them fast.

- [2025-04-15] We use the mypy VSCode extension by Matan Gover instead of the official Microsoft one. Matan Gover's mypy extension analyzes the entire workspace as a single unit, providing more thorough type checking across modules, while Microsoft's extension traditionally checks files individually. Gover's extension uses the mypy daemon by default for better performance, automatically respects the active Python interpreter, and offers reliable multi-root workspace support. Microsoft has added similar features, but they're still labeled as "experimental". In any case, the differences are not significant and the ratings for the non-Microsoft one seem to be better anyway.

- [2025-04-15] The mypy configuration includes `follow_imports = normal`, which makes mypy check all imported modules for type correctness ([see docs](https://mypy.readthedocs.io/en/stable/running_mypy.html#following-imports)). This has important implications:
  - For new projects: This setting provides the most comprehensive type checking and is recommended to ensure type safety across the entire codebase.
  - For existing projects with incomplete typing: This may cause many new errors for imported modules that don't have complete type annotations. In these cases, you may need to install type stubs for third-party libraries that don't include their own typing (pip install types-libraryname). For internal libraries without complete typing, consider changing this setting to `follow_imports = skip` in your mypy configuration.

- [2025-05-15] The distribution name validator ensures that the distribution name adheres to Python packaging conventions by starting with a lowercase letter or digit, allowing only lowercase letters, digits, dots, underscores, or hyphens, and limiting the name to a maximum of three dot-separated components. This aligns with [PEP 423](https://peps.python.org/pep-0423/)'s recommendations to avoid deep nesting and maintain consistent, readable package names.​
