# Variables
PYTHON=python3
FLASK_DEBUG=development

# Targets
.PHONY: help install run test lint clean

help: ## Show this help message
	@echo "Makefile for Flask Project"
	@echo ""
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@echo "Targets:"
	@grep -E '## ' $(MAKEFILE_LIST) | sed 's/## //'

install: ## Install dependencies
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install -r requirements.txt

run: ## Run the Flask application
	@echo "Starting Flask application..."
	FLASK_DEBUG=$(FLASK_DEBUG) $(PYTHON) api.py

test: ## Run tests
	@echo "Running tests..."
	$(PYTHON) -m pytest

lint: ## Run linters
	@echo "Running linters..."
	isort *.py controllers/*.py schemas/*.py services/*.py
	$(PYTHON) -m pylint --rcfile=.pylintrc *.py controllers/*.py schemas/*.py services/*.py

clean: ## Clean up the project
	@echo "Cleaning up..."
	find . | grep -E "(/__pycache__$$|\.pyc$$|\.pyo$$)" | xargs rm -rf