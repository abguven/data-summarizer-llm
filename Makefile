.PHONY: help run demo test build

help: ## Show available commands
	@echo ""
	@echo "  Data Summarizer for LLMs - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36mmake %-10s\033[0m %s\n", $$1, $$2}'
	@echo ""

run: ## Run the summarizer on data/input/ -> results in data/output/
	docker compose up --pull always

demo: ## Run with sample data (copies CSV + JSON from tests/data/)
	@cp tests/data/sample.csv data/input/sample.csv
	@cp tests/data/sample.json data/input/sample.json
	@echo "Sample files copied to data/input/"
	docker compose up --pull always
	@echo ""
	@echo "Done! Check data/output/ for your summaries."

test: ## Run the functional test suite
	bash tests/run_tests.sh

build: ## Build the Docker image locally (for development)
	docker build -t data-summarizer:local .
