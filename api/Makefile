# Variables
PYTHON=python3
FLASK_DEBUG=development

# Targets
.PHONY: install run test lint clean

install: ## Install dependencies
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install -r requirements.txt

run: ## Run the Flask application
	@echo "Starting Flask application..."
	FLASK_DEBUG=$(FLASK_DEBUG) $(PYTHON) api.py

test: ## Run tests
	@echo "Running tests..."
	$(PYTHON) -m unittest tests/*/*.py

lint: ## Run linters
	@echo "Running linters..."
	$(PYTHON) -m isort \
		*.py \
		controllers/*.py \
		schemas/*.py \
		services/*.py \
		tests/services/*.py
	$(PYTHON) -m pylint --rcfile=.pylintrc \
		*.py \
		controllers/*.py \
		schemas/*.py \
		services/*.py \
		tests/services/*.py

clean: ## Clean up the project
	@echo "Cleaning up..."
	find . | grep -E "(/__pycache__$$|\.pyc$$|\.pyo$$)" | xargs rm -rf
