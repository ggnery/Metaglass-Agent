.PHONY: proto up down restart logs db qdrant migrate build clean fmt lint typecheck test check

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

qdrant: ## Start only Qdrant
	docker compose up -d qdrant

migrate: ## Run database migrations
	docker compose run --rm migrations

build: ## Rebuild all images
	docker compose build

clean: ## Stop all services and remove volumes
	docker compose down -v

fmt: ## Auto-format and fix lint issues
	uv run ruff check --fix src && uv run ruff format src

lint: ## Run ruff linter and formatter check
	uv run ruff check src && uv run ruff format --check src

typecheck: ## Run pyright type checker
	uv run pyright src

test: ## Run tests
	uv run pytest

check: lint typecheck test ## Run all checks (lint + typecheck + tests)

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk -F ':.*## ' '{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
