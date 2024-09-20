.DEFAULT_GOAL := help

VERSION_PART ?= $(shell bash -c 'read -p "Version part [major, minor, patch]: " version_part; echo $$version_part')
bump:  ## Bump the project version and create a tag
	poetry run bump2version $(VERSION_PART)
.PHONY: bump

help: ## Show this help
	@echo "Specify a command. The choices are:"
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;36m%-12s\033[m %s\n", $$1, $$2}'
	@echo ""
.PHONY: help

setup:  ## Setup the development environment
	-@pyenv install --skip-existing
	@poetry install
	@cp .pre-commit-config.standard.yaml .pre-commit-config.yaml
	@poetry run pre-commit install

setup-strict: setup  ## Setup the development environment with strict pre-commit rules
	@echo "Appending strict pre-commit rules..."
	@cat .pre-commit-config.addon.strict.yaml >> .pre-commit-config.yaml

lint:   ## Runs linting on all project files
	@tempfile=$$(mktemp) && \
	trap 'rm -f $$tempfile' EXIT && \
	cat .pre-commit-config.standard.yaml .pre-commit-config.addon.strict.yaml > $$tempfile && \
	poetry run pre-commit run --all-files -c $$tempfile
.PHONY: lint

test:  ## Run the project tests
	@poetry run pytest
.PHONY: test
{% if generate_docs == "mkdocs" %}

docs: ## Build documentation
	@mkdocs build --site-dir build/site

serve-docs: ## Build documentation and serve it locally
	@mkdocs serve
.PHONY: docs serve-docs
{% endif %}
{% if generate_docs == "pdoc" %}

docs: ## Build documentation
	@pdoc --output-directory build/site src/{{ package_name }}

serve-docs: ## Build documentation and serve it locally
	@pdoc src/{{ package_name }}
.PHONY: docs serve-docs
{% endif %}
