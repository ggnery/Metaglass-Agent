.PHONY: proto up down restart logs db migrate build clean

proto: ## Generate Python code from .proto files
	docker compose run --rm proto-gen

up: ## Start all services
	docker compose up -d

down: ## Stop all services
	docker compose down

restart: ## Restart the orchestrator service
	docker compose restart orchestrator

logs: ## Tail orchestrator logs
	docker compose logs -f orchestrator

db: ## Start only the database
	docker compose up -d db

migrate: ## Run database migrations
	docker compose run --rm migrations

build: ## Rebuild all images
	docker compose build

clean: ## Stop all services and remove volumes
	docker compose down -v

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk -F ':.*## ' '{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
