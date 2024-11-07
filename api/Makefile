PYTHON=python3.9
FLASK_DEBUG=development
FOLDERS = *.py \
	controllers/*.py \
	schemas/*.py \
	services/*.py

TESTS_FOLDERS = tests/services/*.py \
	tests/controllers/*.py \
	tests/schemas/*.py

# Targets
.PHONY: install run test lint clean todo

install: ## Install dependencies
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install -r requirements.txt

run: ## Run the Flask application
	@echo "Starting Flask application..."
	FLASK_DEBUG=$(FLASK_DEBUG) $(PYTHON) api.py

test: ## Run tests
	@echo "Running tests..."
	@for folder in $(TESTS_FOLDERS); do \
		echo "Running tests in $$folder..."; \
		$(PYTHON) -m unittest $$folder -q; \
	done

lint: ## Run linters
	@echo "Running linters..."
	$(PYTHON) -m isort $(FOLDERS) $(TESTS_FOLDERS)
	$(PYTHON) -m pylint --rcfile=.pylintrc $(FOLDERS) $(TESTS_FOLDERS)

clean: ## Clean up the project
	@echo "Cleaning up..."
	find . | grep -E "(/__pycache__$$|\.pyc$$|\.pyo$$)" | xargs rm -rf

todo: ## List Todos
	@echo "List TODOs..."
	grep -r "TODO" $(FOLDERS)
