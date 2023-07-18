.DEFAULT_GOAL := help

VERSION_PART ?= $(shell bash -c 'read -p "Version part [major, minor, patch]: " version_part; echo $$version_part')
bump:  ## Bump the project version and create a tag
	poetry run bump2version $(VERSION_PART)
.PHONY: bump

TARGET ?= $(shell bash -c 'read -p "Target [production, lab, vagrant]: " target; echo $$target')
deploy:  ## Install application on the remote machine
	@./ansible/provision-deploy deploy $(TARGET)
.PHONY: deploy

help: ## Show this help
	@echo "Specify a command. The choices are:"
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;36m%-12s\033[m %s\n", $$1, $$2}'
	@echo ""
.PHONY: help

init:  ## Initialize the development environment
	@poetry install
	@poetry run pre-commit install

provision:  ## Provision the remote machine
	@./ansible/provision-deploy provision $(TARGET)
.PHONY: provision

test:  ## Run the project tests
	@poetry run pytest
.PHONY: test
