help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

code-check: ## Check code
	clear
	@echo "\nRunning isort ..."
	isort .

	@echo "\nRunning black ..."
	black .

	@echo "\nRunning flake ..."
	flake8 .

	@echo "\nRunning safety check ..."
	safety check -r requirements.txt

install: ## Install requirements
	pip install -r requirements.txt && pip install .

install-dev: ## Install development requirements
	pip install -r requirements_dev.txt

test: ## Run tests
	pytest -s --mypy --cov --cov-report=html --verbose
