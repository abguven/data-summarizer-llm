.PHONY: help build demo test

LOCAL_IMAGE = data-summarizer:local

help: ## Show available commands
	@echo ""
	@echo "  Data Summarizer for LLMs — Developer commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36mmake %-10s\033[0m %s\n", $$1, $$2}'
	@echo ""

build: ## Build the Docker image locally (tagged as data-summarizer:local)
	docker build -t $(LOCAL_IMAGE) .

demo: ## Copy sample data into data/input/ and run the local image
	@cp tests/data/sample.csv data/input/sample.csv
	@cp tests/data/sample.json data/input/sample.json
	@echo "Sample files copied to data/input/"
	docker run --rm \
		-v "$(PWD)/data/input:/app/data/input" \
		-v "$(PWD)/data/output:/app/data/output" \
		-v "$(PWD)/logs:/app/logs" \
		$(LOCAL_IMAGE)
	@echo ""
	@echo "Done! Check data/output/ for the generated summaries."

test: ## Run the functional test suite against the local image
	bash tests/run_tests.sh $(LOCAL_IMAGE)
