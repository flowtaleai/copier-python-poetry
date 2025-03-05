# Contributing to {{ project_name if project_name else distribution_name }}

Thank you for considering contributing to {{ project_name if project_name else distribution_name }}! This document provides guidelines and instructions for setting up your development environment and contributing to the project.

## Development Environment Setup

### Requirements

- Python {{ python_version }}
- [Poetry](https://python-poetry.org/docs/#installation)
- Make (optional, for using Makefile commands)
- Git (for version control)
- [direnv](https://direnv.net/) (optional, for environment management)
- [pyenv](https://github.com/pyenv/pyenv) (optional, for Python version management)
{% if generate_dockerfile %}
- [Docker](https://docs.docker.com/get-docker/) (for containerized development/deployment)
{% endif %}

### Setting Up Your Environment

1. Set up Python environment:

   If you have pyenv installed, the correct Python version ({{ python_version }}) will be automatically installed and used thanks to the `.python-version` file.

2. Install dependencies and set up the development environment:
   ```bash
   make setup
   ```

   Or for a stricter development environment with additional checks:
   ```bash
   make setup-strict
   ```

   If you don't have Make available, you can run these commands directly:
   ```bash
   poetry install
   poetry run pre-commit install
   ```

3. Configure direnv (optional but recommended):
   ```bash
   # After installing direnv
   direnv allow
   ```
   This will:
   - Automatically load environment variables from `.env`
   - Activate the poetry virtual environment using the `layout_poetry` directive in `.envrc`

{% if ide == 'vscode' %}
### IDE Configuration

When using Visual Studio Code, open the project folder and install the recommended extensions when prompted. These extensions are configured in the `.vscode/extensions.json` file to provide a consistent development experience.
{% endif %}

{% if use_jupyter_notebooks %}
### Jupyter Notebook Setup

To work with Jupyter notebooks in this project:

```bash
poetry install --with jupyterlab
poetry run jupyter lab
```

{% if strip_jupyter_outputs %}
Note: The pre-commit hooks will automatically strip output from notebooks before committing to keep the repository clean.
{% endif %}
{% endif %}

{% if generate_dockerfile %}
### Docker Development Environment

The project includes a Dockerfile for containerized development and deployment:

1. Build the Docker image:
   ```bash
   docker build -t {{ distribution_name }}:dev .
   ```

2. Run the Docker container:
   ```bash
   docker run -it --rm {{ distribution_name }}:dev
   ```

For development with mounted source code:
   ```bash
   docker run -it --rm -v $(pwd):/app {{ distribution_name }}:dev
   ```

See the [Dockerfile](./Dockerfile) for more details on the container setup.
{% endif %}

## Development Workflow

### Available Make Commands

This project includes a Makefile with various commands to help with development tasks. To see all available commands:

```bash
make help
```

This will display a list of all available commands with their descriptions.

### Environment Variables

We follow a structured approach to environment variable management:

#### `.env` File - Application Configuration

The `.env` file contains application-specific configuration that can be used in both development and production:
- Database connection strings
- API keys and secrets
- Feature flags
- External service URLs

This file should:
- Have a corresponding `.env.example` template in version control with dummy values
- Be usable in both development and production environments

Example `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
API_KEY=your_api_key_here
FEATURE_FLAG_NEW_UI=true
```

#### `.envrc` File - Development Environment Only

The `.envrc` file (used by direnv) contains development-specific settings:
- PATH adjustments
- Tool configurations
- Development convenience settings
- Poetry virtual environment activation (via `layout_poetry`)

This file should:
- Be committed to version control (without sensitive information)
- NEVER be used in production environments
- Focus only on development workflow optimization

Example `.envrc` file:
```
# Automatically activate poetry environment
layout poetry

# Development-specific settings
export DEBUG=true
export PYTHONBREAKPOINT=ipdb.set_trace
export PYTHONPATH=$PWD:$PYTHONPATH
```

#### Using Environment Variables

With direnv properly configured:
1. Environment variables from both `.env` and `.envrc` will be automatically loaded when you enter the project directory
2. The Poetry virtual environment will be automatically activated
3. All settings will be unloaded when you leave the directory

#### Production Environment

For production deployments:
- Use the `.env` file for application-specific configuration
- Load environment variables using a proper environment variable management system for your deployment platform
- Do NOT use direnv or `.envrc` files in production
- Consider using a secrets management service for sensitive credentials

### Running Tests

To run the test suite:

```bash
make test
```

Or without Make:
```bash
poetry run pytest
```

### Code Formatting and Linting

To format and lint your code:

```bash
make lint
```

This will run all configured linters and formatters using pre-commit hooks, including both standard and strict rules.

{% if generate_docs != 'none' %}
### Documentation

To build documentation:

```bash
make docs
```

To serve documentation locally for development:

```bash
make serve-docs
```
{% endif %}

## Working with Private Python Packages

### Adding Python Package Registry Credentials

If you need to use private Python packages, configure authentication with Poetry:

```bash
poetry config http-basic.my_registry your_username your_personal_access_token
poetry source add my_registry https://gitlab.mycompany.com/api/v4/projects/1234/packages/pypi/simple
poetry add private-package@0.1.0 --source my_registry
```

{% if generate_dockerfile %}
### Adding Python Package Registry Credentials for Docker Builds

When building the Docker image with private dependencies:

```bash
docker build \
  --build-arg PYTHON_REGISTRY_NAME=your_private_registry_name \
  --build-arg PYTHON_REGISTRY_USERNAME=your_username \
  --build-arg PYTHON_REGISTRY_PASSWORD=your_personal_access_token \
  -t your_image_name:tag .
```
{% endif %}

## Release Process

### Versioning

This project follows [Semantic Versioning](https://semver.org/) (SemVer).

To bump the project version:

```bash
make bump
# or specify the version part explicitly
make bump VERSION_PART=minor
```

Valid VERSION_PART values are: major, minor, or patch.

This will:
1. Update the version in the project metadata
2. Create a commit with the version change
3. Create a version tag

After bumping the version, you need to push both the commit and the tag to the remote repository:

```bash
git push  # Push the version bump commit
git push --tags  # Push the new version tag
```

## Submitting Changes

1. Create a new branch for your changes
2. Make your changes and commit them with clear, descriptive messages
3. Push your branch and create a pull/merge request
4. Ensure all CI checks pass on your changes

Thank you for contributing to {{ project_name if project_name else distribution_name }}!
