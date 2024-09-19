# syntax=docker/dockerfile:1
# Keep this syntax directive! It's used to enable Docker BuildKit

# Dockerfile inspired by:
# https://github.com/orgs/python-poetry/discussions/1879
# https://github.com/orgs/python-poetry/discussions/1879#discussioncomment-216865
# https://github.com/orgs/python-poetry/discussions/1879#discussioncomment-7284113
# https://gist.github.com/usr-ein/c42d98abca3cb4632ab0c2c6aff8c88a

FROM python:{{ python_version }}-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # Poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.7.0 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # never create virtual environment automaticly, only use env prepared by us
    POETRY_VIRTUALENVS_CREATE=false \
    \
    # this is where our requirements + virtual environment will live
    VIRTUAL_ENV="/venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH"

# TODO(rj) if web server is used
ENV PORT=8000

# prepare virtual env
RUN python -m venv $VIRTUAL_ENV

# working directory and Python path
WORKDIR /work_dir
ENV PYTHONPATH="/work_dir:$PYTHONPATH"

FROM python-base as builder-base
RUN apt-get update \
    && apt-get install -y curl git
    # build-essential # if ever needed, leave it here

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
# The --mount will mount the buildx cache directory to where
# Poetry and Pip store their cache so that they can re-use it
RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python -

# used to init dependencies
WORKDIR /work_dir
COPY poetry.lock pyproject.toml ./

# install runtime deps to $VIRTUAL_ENV
ARG GIT_AUTH_METHOD=https
ARG POETRY_HTTP_BASIC_GPT_CORE_USERNAME
ARG POETRY_HTTP_BASIC_GPT_CORE_PASSWORD
ARG GIT_HOST=gitlab.company-name.com

# Setup environment for SSH or HTTPS based on the argument
RUN if [ "$GIT_AUTH_METHOD" = "ssh" ]; then \
        mkdir -p -m 0600 $HOME/.ssh && \
        ssh-keyscan -t rsa $GIT_HOST >> $HOME/.ssh/known_hosts; \
    elif [ "$GIT_AUTH_METHOD" = "https" ]; then \
        if [ -z "$POETRY_HTTP_BASIC_GPT_CORE_USERNAME" ] || [ -z "$POETRY_HTTP_BASIC_GPT_CORE_PASSWORD" ]; then \
            echo "POETRY_HTTP_BASIC_GPT_CORE_USERNAME and POETRY_HTTP_BASIC_GPT_CORE_PASSWORD are required for HTTPS method but are not set"; \
            exit 1; \
        fi; \
    else \
        echo "GIT_AUTH_METHOD must be set to 'ssh' or 'https'"; \
        exit 1; \
    fi
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=ssh \
    poetry install --no-root --only main


FROM builder-base as development

WORKDIR /work_dir

# quicker install as runtime deps are already installed
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=ssh \
    poetry install --no-root --with dev

# copy in our source code last, as it changes the most
COPY pyproject.toml poetry.lock ./
COPY ./src ./src
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=ssh \
    poetry install --only-root

# TODO(rj) if web server is used
EXPOSE $PORT

# TODO(rj) entrypoint example
# CMD uvicorn gpt_backend.main:app --host 0.0.0.0 --port $PORT --reload
CMD ["python", "-m", "my_package.cli"]

FROM python-base as production

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $VIRTUAL_ENV $VIRTUAL_ENV

WORKDIR /work_dir

# copy in our source code last, as it changes the most
COPY pyproject.toml poetry.lock ./
COPY ./src ./src
RUN --mount=type=cache,target=/root/.cache \
    poetry install --only-root


# TODO(rj) if web server is used
EXPOSE $PORT

# TODO(rj) entrypoint example
# CMD uvicorn gpt_backend.main:app --host 0.0.0.0 --port $PORT --reload
CMD ["python", "-m", "my_package.cli"]
