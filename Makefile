.PHONY: clean clean-test clean-pyc clean-build test
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	@rm -fr build/
	@rm -fr dist/
	@rm -fr .eggs/
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.egg' -exec rm -f {} +	

clean-pyc: ## remove Python file artifacts
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	@find . -name '*.step' -exec rm -f {} +
	@find . -name '*.stl' -exec rm -f {} +
	@find . -name '*.svg' -exec rm -f {} +
	@rm -f .coverage
	@rm -fr htmlcov/

lint: ## check style with black
	@black cqgridfinity/*.py
	@black cqgridfinity/scripts/*.py
	@black tests/*.py

lint-check: ## check if lint status is consistent between commits
	@black --diff --check cqgridfinity/*.py
	@black --diff --check cqgridfinity/scripts/*.py
	@black --diff --check tests/*.py

test: ## run tests quickly with the default Python
	@py.test -s -v --cov

test-files: ## run tests and export test files artifacts
	@export EXPORT_STEP_FILES="all" && \
	py.test -s -v
	
coverage: ## check code coverage quickly with the default Python
	coverage run --source cqgridfinity -m pytest
	coverage report -m
	coverage html
	open htmlcov/index.html

release: clean dist ## package and upload a release
	twine check dist/*
	twine upload dist/*

dist: clean ## builds source and wheel package
	@python -m build
	@twine check dist/*
	@ls -l dist

install: clean ## install the package to the active Python's site-packages
	@pip install .
