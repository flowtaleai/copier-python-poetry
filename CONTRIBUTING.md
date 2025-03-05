# Contributing to Copier Python Poetry

This document provides guidelines for contributing to the Copier Python Poetry template project. Since this is a template generator, there are two distinct contexts to consider: the template itself and the projects generated from it.

## Template Development

### Prerequisites

- Python (suggested install method: system)
- [Copier](https://copier.readthedocs.io/) (suggested install method: pipx)
- [Poetry](https://python-poetry.org/docs#installation)
- [pyenv](https://github.com/pyenv/pyenv#getting-pyenv) (recommended)
- [direnv](https://direnv.net/) (recommended for environment management)
- Git

### Development Environment Setup

#### Installing pyenv (recommended)

This step can be skipped if your system Python version matches the one specified in the `.python-version` file.

Add the following to `~/.bashrc` or `~/.zshrc` to initialize `pyenv`:

```bash
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

#### Configuring Poetry

To make Poetry use the Python interpreter specified by pyenv:

```bash
poetry config virtualenvs.prefer-active-python true
```

This setting allows for easier project folder renaming without recreating the virtual environment, and helps VSCode detect the Poetry environment automatically.

#### Setting up direnv (recommended)

direnv automatically loads and unloads directory-specific environment variables. To use it:

1. [Install direnv](https://direnv.net/docs/installation.html)
2. At the project root (where `.envrc` is located), run:
   ```bash
   direnv allow
   ```

### Testing the Template

There are multiple approaches for testing the template to ensure it works correctly. A comprehensive testing strategy involves testing both the template itself and the projects it generates.

#### Running Template Tests

To run the automated test suite for the template:

```bash
make test
```

This runs tests using tox. If you encounter environment-related issues, you can recreate the environments:

```bash
poetry run tox -r
```

#### Generating Test Projects

1. **Using Make (Quickest Method)**:
   ```bash
   make testproject
   ```
   This creates a project in a temporary directory under `testprojects/` using the current template version.

   > **Note:** The `make testproject` command uses `--vcs-ref=HEAD` which means it will use the committed files in your repository. To test changes, you must commit them first.

2. **Basic Manual Generation**:
   ```bash
   mkdir -p /tmp/test-project
   copier copy . /tmp/test-project
   ```

   > **Important:** When using Copier with a Git repository as the source, Copier always accesses the repository content through Git, not the filesystem. This means:
   >
   > - Without a reference flag (`-r` or `--vcs-ref`), Copier uses the latest tag
   > - With `-r HEAD`, it uses the latest commit
   > - Uncommitted changes in your working directory **will not** be included in the template
   > - To test changes, you must commit them first, then use `-r HEAD`

3. **Complete Test with Git Initialization**:
   ```bash
   # First, commit your changes if needed
   git add .
   git commit -m "WIP: Testing changes"

   # Then generate a test project
   mkdir /tmp/copier-test-project && cd /tmp/copier-test-project && \
   copier copy /media/data/software/copier-python-poetry . -r HEAD \
   --data-file ~/copier-default-answers.yml && \
   git init && git add . && git commit -m "initial commit" && make setup-strict && direnv allow
   ```

   After testing, you can undo the temporary commit if needed:
   ```bash
   git reset HEAD~1  # Unstage the changes but keep them in your working directory
   ```

#### Testing Different Configurations

When making significant changes, test the template with various configurations:

1. **CLI Project**:
   ```bash
   copier copy . /tmp/test-cli --data package_type=cli
   ```

2. **Library Project**:
   ```bash
   copier copy . /tmp/test-lib --data package_type=library
   ```

3. **Documentation Variations**:
   ```bash
   copier copy . /tmp/test-mkdocs --data generate_docs=mkdocs
   copier copy . /tmp/test-pdoc --data generate_docs=pdoc
   ```

4. **Automated Testing with Predefined Answers**:
   ```bash
   copier copy . /tmp/test-automated -r HEAD --data-file ~/copier-default-answers.yml
   ```

#### Verifying Generated Projects

After generating a test project, verify it works correctly:

1. Install dependencies:
   ```bash
   cd /tmp/test-project
   poetry install
   ```

2. Run tests and linting:
   ```bash
   make test
   make lint
   ```

3. Check other features based on your configuration:
   ```bash
   # For projects with documentation
   make docs

   # For CLI projects
   poetry run your-package-name --help
   ```

#### Using a Default Answers File

To streamline testing, create a default answers YAML file:

```yaml
# ~/copier-default-answers.yml
author_name: "Test Author"
author_email: "test@example.com"
package_name: "testpackage"
distribution_name: "test-package"
project_name: "Test Project"
repository_name: "test-project"
project_short_description: "A project for testing the template"
version: "0.1.0"
license: "MIT"
package_type: "cli"
python_version: "3.10"
testing_framework: "pytest"
max_line_length: 88
type_checker: "mypy"
type_checker_strictness: "strict"
use_flake8_strict_plugins: true
ide: "vscode"
git_hosting: "gitlab"
use_jupyter_notebooks: true
generate_example_code: true
strip_jupyter_outputs: true
generate_docs: "mkdocs"
```

Adjust these values to match your testing preferences.

### Available Make Commands

The template project includes several useful commands:

- `make help`: Show all available commands with descriptions
- `make setup`: Set up the development environment
- `make setup-strict`: Set up the development environment with strict pre-commit rules
- `make lint`: Run linting on all project files
- `make test`: Run the template's tests using tox
- `make testproject`: Generate a test project in a temporary directory
- `make bump`: Bump the project version (you'll be prompted to select major, minor, or patch)

### Template Structure

The template follows this structure:

```
copier-python-poetry/
├── template/                  # Template files that will be copied
├── tests/                     # Template tests
├── copier.yml                 # Copier configuration
└── ...                        # Other repository files
```

When modifying template files:
- Use Jinja2 syntax for dynamic content: `{{ variable_name }}`
- Use conditional blocks when appropriate: `{% if condition %}...{% endif %}`
- Test thoroughly after changes

### Recursive Template Structure

Importantly, the outer project itself is based on its own template. This creates a recursive structure:

1. The `template/` directory contains files that will be copied to generated projects
2. The outer project structure mirrors what a generated project would look like

After tagging a new version, we run `copier update` on the outer project to apply the template changes to itself. This means:

- **New features should primarily be implemented in the inner `template/` directory**
- These changes will be automatically applied (except for merge conflicts) the next time the outer project template is updated
- Some changes might specifically target only the outer template (e.g., updates to the outer README.md and CONTRIBUTING.md, or other infrastructure changes that don't get copied to generated projects)

This recursive approach ensures that the template itself follows the best practices it promotes for generated projects.

## Contribution Guidelines

Before contributing to this project, please review the following internal resources:

- **Copier Guidelines** - Internal Google Drive document with detailed guidelines for running the project
- **GitLab Organization** - Internal Google Drive document with information on our GitLab workflow and organization

### Pull Request Management

Please follow the Pull Request Management Best Practices outlined in our internal GitLab Organization document, with one project-specific modification:

**Review order**: First request review from another sprint team member, then notify the product owner for final review after initial approval.

### Code Style

- Follow the style conventions evident in the existing template files
- Use consistent indentation and formatting
- Document any non-obvious template variables or logic
- Docstrings convention is `google` without types (types are specified using standard python typing)
- Use `pathlib.Path` instead of `str` for file names
- Use `pathlib.Path` to process files instead of `os`

### Python Dependencies

- Do not manually change the dependency specifications in template files without testing
- When updating dependencies in the template, ensure they are compatible across supported Python versions
- Consider the impact on generated projects when updating dependencies

#### Dependency Version Management

The template's dependencies in `template/pyproject.toml` need to be periodically updated to maintain security and incorporate new features. However, these updates require careful consideration:

- Each version update must be taken seriously as it affects all projects generated from the template
- Major version updates of formatters (like black) or linters may require reformatting entire codebases
- Test updates thoroughly across different Python versions and configurations
- Document any breaking changes or required manual steps in the release notes
- Consider creating a major template version when introducing potentially disruptive dependency updates

For example:
- Updating the formatter major version might require reformatting all code in existing projects
- Updating linter plugins might introduce new rules that existing projects need to address
- Updating type checkers might enforce stricter rules requiring code modifications

### Versioning

This project follows [Semantic Versioning](https://semver.org/).

- **MAJOR**: Breaking changes to the template structure or generated projects
  - Example: Updating to a new major version of Black that reformats code differently
  - Example: Adding required linters that may cause failures in existing projects

- **MINOR**: New features or enhancements that are backward compatible
  - Example: Adding support for new documentation generators
  - Example: New optional template features

- **PATCH**: Bug fixes that don't affect compatibility
  - Example: Fixing template syntax errors
  - Example: Correcting documentation

To bump the project version:

```bash
make bump
```

And select the version part to increment (major, minor, or patch).

## Template Rationale Documentation

When making significant changes or adding new features to the template, add an entry to the [Rationale](README.md#rationale) section of the README with:

1. Date in [YYYY-MM-DD] format
2. Clear explanation of the change and why it was made
3. Examples if applicable

This helps future contributors understand the reasoning behind design decisions.

## Release Process

1. Bump the version using `make bump` and select the appropriate version part
2. Push the changes and new tag to the repository
3. Create a release on GitHub/GitLab with release notes
4. Run `copier update` on the outer project to apply template changes to itself
5. Resolve any merge conflicts that arise from the update
6. Commit the applied changes with a message describing the update

Thank you for contributing to the Copier Python Poetry template!
