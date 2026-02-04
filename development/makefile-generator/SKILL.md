---
name: makefile-generator
description: Generate Makefile build automation files with targets, dependencies, and common development tasks for various project types. Triggers on "create Makefile", "generate Makefile for", "build automation", "make targets for".
---

# Makefile Generator

Generate Makefile build automation files for development workflows, CI/CD tasks, and project management.

## Output Requirements

**File Output:** `Makefile` (no extension)
**Format:** GNU Make compatible syntax
**Indentation:** Tabs only (required by Make)

## When Invoked

Immediately generate a complete Makefile with common targets for the project type. Include help target by default.

## Makefile Syntax Rules

### Basic Structure
```makefile
# Variables
VARIABLE = value

# Default target (first non-special target)
.DEFAULT_GOAL := help

# Phony targets (not real files)
.PHONY: target

# Target with dependencies
target: dependency1 dependency2
	command1
	command2
```

### Important Notes
- **Indentation must be TABS, not spaces**
- Variables: `$(VAR)` or `${VAR}`
- Shell commands: Each line is separate shell
- Continue lines: End with `\`
- Silence output: Prefix with `@`

## Project Templates

### Node.js/TypeScript Project
```makefile
# Node.js/TypeScript Project Makefile

# Variables
NODE_ENV ?= development
NPM := npm
PORT ?= 3000

# Colors for terminal output
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

.DEFAULT_GOAL := help
.PHONY: help install dev build start test lint format clean docker-build docker-run

##@ General

help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development

install: ## Install dependencies
	@echo "$(GREEN)Installing dependencies...$(NC)"
	$(NPM) ci

dev: ## Start development server
	@echo "$(GREEN)Starting development server...$(NC)"
	$(NPM) run dev

build: ## Build for production
	@echo "$(GREEN)Building for production...$(NC)"
	$(NPM) run build

start: build ## Start production server
	@echo "$(GREEN)Starting production server...$(NC)"
	NODE_ENV=production $(NPM) start

##@ Testing

test: ## Run tests
	@echo "$(GREEN)Running tests...$(NC)"
	$(NPM) test

test-watch: ## Run tests in watch mode
	$(NPM) run test:watch

test-coverage: ## Run tests with coverage
	$(NPM) run test:coverage

##@ Code Quality

lint: ## Run linter
	@echo "$(GREEN)Running linter...$(NC)"
	$(NPM) run lint

lint-fix: ## Fix linting errors
	$(NPM) run lint:fix

format: ## Format code
	$(NPM) run format

typecheck: ## Run TypeScript type checking
	$(NPM) run typecheck

check: lint typecheck test ## Run all checks

##@ Database

db-migrate: ## Run database migrations
	$(NPM) run db:migrate

db-seed: ## Seed the database
	$(NPM) run db:seed

db-reset: ## Reset and reseed database
	$(NPM) run db:reset

##@ Docker

DOCKER_IMAGE := myapp
DOCKER_TAG := latest

docker-build: ## Build Docker image
	@echo "$(GREEN)Building Docker image...$(NC)"
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

docker-run: ## Run Docker container
	docker run -p $(PORT):$(PORT) --env-file .env $(DOCKER_IMAGE):$(DOCKER_TAG)

docker-push: ## Push Docker image
	docker push $(DOCKER_IMAGE):$(DOCKER_TAG)

##@ Cleanup

clean: ## Clean build artifacts
	@echo "$(YELLOW)Cleaning build artifacts...$(NC)"
	rm -rf dist build .next out
	rm -rf coverage .nyc_output
	rm -rf node_modules/.cache

clean-all: clean ## Clean everything including node_modules
	rm -rf node_modules
```

### Python Project
```makefile
# Python Project Makefile

# Variables
PYTHON := python3
PIP := pip3
VENV := .venv
VENV_BIN := $(VENV)/bin
PYTEST := $(VENV_BIN)/pytest
PYTHON_VENV := $(VENV_BIN)/python

# Detect OS
ifeq ($(OS),Windows_NT)
    VENV_BIN := $(VENV)/Scripts
endif

.DEFAULT_GOAL := help
.PHONY: help venv install install-dev dev test lint format clean

##@ General

help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Setup

venv: ## Create virtual environment
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "Activate with: source $(VENV_BIN)/activate"

install: venv ## Install production dependencies
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -r requirements.txt

install-dev: install ## Install development dependencies
	$(VENV_BIN)/pip install -r requirements-dev.txt
	$(VENV_BIN)/pre-commit install

##@ Development

dev: ## Run development server
	$(PYTHON_VENV) -m uvicorn app.main:app --reload --port 8000

run: ## Run production server
	$(PYTHON_VENV) -m gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

shell: ## Start Python shell with app context
	$(PYTHON_VENV) -m IPython

##@ Testing

test: ## Run tests
	$(PYTEST) tests/ -v

test-cov: ## Run tests with coverage
	$(PYTEST) tests/ -v --cov=app --cov-report=html --cov-report=term

test-watch: ## Run tests in watch mode
	$(VENV_BIN)/ptw tests/

##@ Code Quality

lint: ## Run linters
	$(VENV_BIN)/ruff check .
	$(VENV_BIN)/mypy app/

lint-fix: ## Fix linting errors
	$(VENV_BIN)/ruff check . --fix

format: ## Format code
	$(VENV_BIN)/ruff format .

check: lint test ## Run all checks

##@ Database

db-migrate: ## Run database migrations
	$(PYTHON_VENV) -m alembic upgrade head

db-rollback: ## Rollback last migration
	$(PYTHON_VENV) -m alembic downgrade -1

db-revision: ## Create new migration
	$(PYTHON_VENV) -m alembic revision --autogenerate -m "$(msg)"

##@ Docker

docker-build: ## Build Docker image
	docker build -t myapp:latest .

docker-run: ## Run Docker container
	docker run -p 8000:8000 --env-file .env myapp:latest

docker-compose-up: ## Start with docker-compose
	docker-compose up -d

docker-compose-down: ## Stop docker-compose
	docker-compose down

##@ Cleanup

clean: ## Clean build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf htmlcov .coverage coverage.xml
	rm -rf dist build *.egg-info

clean-all: clean ## Clean everything including venv
	rm -rf $(VENV)
```

### Go Project
```makefile
# Go Project Makefile

# Variables
BINARY_NAME := myapp
VERSION := $(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")
BUILD_TIME := $(shell date -u '+%Y-%m-%dT%H:%M:%SZ')
LDFLAGS := -ldflags "-X main.Version=$(VERSION) -X main.BuildTime=$(BUILD_TIME) -w -s"

GO := go
GOTEST := $(GO) test
GOBUILD := $(GO) build
GORUN := $(GO) run

# Directories
BUILD_DIR := ./build
CMD_DIR := ./cmd/$(BINARY_NAME)

.DEFAULT_GOAL := help
.PHONY: help build run test lint clean

##@ General

help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development

run: ## Run the application
	$(GORUN) $(CMD_DIR)/main.go

dev: ## Run with hot reload (requires air)
	air

tidy: ## Tidy dependencies
	$(GO) mod tidy
	$(GO) mod verify

##@ Build

build: ## Build binary
	@mkdir -p $(BUILD_DIR)
	CGO_ENABLED=0 $(GOBUILD) $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME) $(CMD_DIR)

build-linux: ## Build for Linux
	@mkdir -p $(BUILD_DIR)
	GOOS=linux GOARCH=amd64 CGO_ENABLED=0 $(GOBUILD) $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME)-linux-amd64 $(CMD_DIR)

build-darwin: ## Build for macOS
	@mkdir -p $(BUILD_DIR)
	GOOS=darwin GOARCH=amd64 CGO_ENABLED=0 $(GOBUILD) $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME)-darwin-amd64 $(CMD_DIR)
	GOOS=darwin GOARCH=arm64 CGO_ENABLED=0 $(GOBUILD) $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME)-darwin-arm64 $(CMD_DIR)

build-all: build-linux build-darwin ## Build for all platforms

##@ Testing

test: ## Run tests
	$(GOTEST) -v ./...

test-race: ## Run tests with race detector
	$(GOTEST) -race -v ./...

test-coverage: ## Run tests with coverage
	$(GOTEST) -coverprofile=coverage.out ./...
	$(GO) tool cover -html=coverage.out -o coverage.html

benchmark: ## Run benchmarks
	$(GOTEST) -bench=. -benchmem ./...

##@ Code Quality

lint: ## Run linter
	golangci-lint run

lint-fix: ## Fix linting errors
	golangci-lint run --fix

fmt: ## Format code
	$(GO) fmt ./...
	goimports -w .

vet: ## Run go vet
	$(GO) vet ./...

check: fmt vet lint test ## Run all checks

##@ Docker

docker-build: ## Build Docker image
	docker build -t $(BINARY_NAME):$(VERSION) .

docker-run: ## Run Docker container
	docker run -p 8080:8080 $(BINARY_NAME):$(VERSION)

##@ Cleanup

clean: ## Clean build artifacts
	rm -rf $(BUILD_DIR)
	rm -f coverage.out coverage.html
	$(GO) clean -cache -testcache

##@ Release

release-dry: ## Dry run release
	goreleaser release --snapshot --clean

release: ## Create release
	goreleaser release --clean
```

### Generic Project (Multi-language)
```makefile
# Generic Project Makefile

PROJECT_NAME := myproject
VERSION := 1.0.0

.DEFAULT_GOAL := help
.PHONY: help setup dev build test lint clean deploy

##@ General

help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

info: ## Show project info
	@echo "Project: $(PROJECT_NAME)"
	@echo "Version: $(VERSION)"

##@ Setup

setup: ## Initial project setup
	@echo "Setting up project..."
	./scripts/setup.sh

env: ## Create environment file
	cp .env.example .env
	@echo "Created .env file - please update with your values"

##@ Development

dev: ## Start development environment
	docker-compose up -d

stop: ## Stop development environment
	docker-compose down

logs: ## View logs
	docker-compose logs -f

shell: ## Open shell in app container
	docker-compose exec app sh

##@ Build

build: ## Build the project
	docker-compose build

build-prod: ## Build for production
	docker build -t $(PROJECT_NAME):$(VERSION) -f Dockerfile.prod .

##@ Testing

test: ## Run tests
	docker-compose run --rm app npm test

test-e2e: ## Run end-to-end tests
	docker-compose -f docker-compose.test.yml up --abort-on-container-exit

##@ Deployment

deploy-staging: ## Deploy to staging
	./scripts/deploy.sh staging

deploy-prod: ## Deploy to production
	./scripts/deploy.sh production

##@ Cleanup

clean: ## Clean docker resources
	docker-compose down -v --remove-orphans
	docker system prune -f
```

## Best Practices

### Self-Documenting Help
```makefile
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
```

### Default Variables
```makefile
# Allow override from command line
PORT ?= 3000
ENV ?= development
```

## Validation Checklist

Before outputting, verify:
- [ ] Uses TABS for indentation (not spaces)
- [ ] `.PHONY` declared for non-file targets
- [ ] `help` target present and useful
- [ ] Variables use `?=` for overridable defaults
- [ ] Common targets included (build, test, clean)
- [ ] Grouped with `##@` headers
- [ ] Each target has `##` documentation

## Example Invocations

**Prompt:** "Create Makefile for a Go microservice"
**Output:** Complete `Makefile` with build, test, lint, docker targets.

**Prompt:** "Generate Makefile for Python FastAPI project"
**Output:** Complete `Makefile` with venv, test, lint, migrations.

**Prompt:** "Makefile for monorepo with multiple services"
**Output:** Complete `Makefile` with per-service and aggregate targets.
