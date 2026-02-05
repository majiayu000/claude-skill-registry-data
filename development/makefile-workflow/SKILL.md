---
name: makefile-workflow
description: Makefile best practices for project automation and build systems. Covers command usage, target organization (PHONY vs file targets), variable management (:=, ?=, =), platform detection, common development targets (clean, test, lint, format, run), DevContainer integration, version management with semantic versioning, Docker integration, output control, error handling, and advanced patterns. Activate when working with Makefiles, make commands, .PHONY targets, build automation, or development workflows.
---

# Makefile Workflow Guidelines

Makefiles provide consistent command interfaces across development, testing, and deployment. They abstract complex commands into simple, memorable targets and enable reproducible builds across platforms.

---

## Overview and Purpose

Makefiles serve as a unified interface for project automation:

- **Consistency**: Same commands work across different environments
- **Documentation**: Help text via grep parsing of `##` comments
- **Dependency Management**: Automatic rebuild only when dependencies change
- **Platform Abstraction**: Handle OS-specific commands in one place
- **Workflow Orchestration**: Chain targets for complex processes (test → lint → deploy)

A well-designed Makefile replaces scattered shell scripts and tribal knowledge with explicit, executable documentation.

---

## Basic Structure

### Template Makefile

```makefile
# Project Makefile
.DEFAULT_GOAL := help

# Variables
PYTHON := python
UV := uv
PROJECT_DIR := $(shell pwd)

# Phony targets (not files)
.PHONY: help install test lint format clean run

help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

install: ## Install dependencies
	$(UV) sync --extra dev

test: ## Run tests
	$(UV) run pytest -v

lint: ## Run linters
	$(UV) run ruff check .
	$(UV) run mypy src/

format: ## Format code
	$(UV) run ruff format .

clean: ## Remove generated files
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache htmlcov .coverage build dist *.egg-info

run: ## Run application
	$(UV) run python run.py
```

---

## Command Usage Principles

### Avoid Unnecessary Flags

**Only include flags that change behavior or add information:**

```makefile
# ✅ Good: Minimal, clear flags
test:
	$(UV) run pytest tests/ -v

# ❌ Poor: Redundant flags that add no value
test:
	$(UV) run pytest tests/ -v --tb=short --strict-markers --durations=0

# ✅ Good: Flag only when needed for specific use case
test-verbose: ## Run tests with detailed output
	$(UV) run pytest tests/ -vv
```

**Principle:** Add flags only when they provide value. Keep default commands simple.

---

## Target Organization

### PHONY Targets (Commands)

Use `.PHONY` for targets that don't produce files. These are action targets, not build targets:

```makefile
.PHONY: test clean install deploy help

# PHONY targets don't create files - they run commands
test:
	pytest tests/

clean:
	rm -rf build/

install:
	pip install -r requirements.txt

help:
	@echo "Available commands"
```

**Why `.PHONY` matters:** Without it, `make test` fails if a file named `test` exists in your directory.

### File Targets (Dependencies)

Use real file targets when building artifacts. Make automatically tracks dependencies and rebuilds only when sources change:

```makefile
# Real file target - only rebuilds if source changes
build/app: src/main.py src/utils.py
	mkdir -p build
	python -m PyInstaller src/main.py -o build/

# Dependency chain
dist/app.tar.gz: build/app
	tar -czf dist/app.tar.gz -C build app

# Declaration order: prerequisites first, then target
docs/index.html: docs/source/*.md
	mkdocs build -d docs/index.html
```

**Best Practice:** Use file targets for actual build artifacts, PHONY for development workflows.

---

## Variable Management

### Three Assignment Types

Makefiles support three variable assignment styles with different evaluation models:

#### Immediate Assignment (`:=`)

Evaluated **once**, at definition time. Use for values that never change:

```makefile
# Evaluated immediately
PYTHON := python
UV := uv
SRC_DIR := $(shell pwd)/src
BUILD_DATE := $(shell date +%Y-%m-%d)

# Variables available before next line
FULL_PATH := $(SRC_DIR)/main.py
```

**When to use:** Constants, paths that won't change, one-time shell evaluations.

#### Conditional Assignment (`?=`)

Set value **only if not already set**. Enables environment variable overrides:

```makefile
# Default values - can override via CLI or environment
ENVIRONMENT ?= development
LOG_LEVEL ?= info
DATABASE_URL ?= postgresql://localhost/testdb

# Usage:
# make test ENVIRONMENT=production  # Override at CLI
# ENVIRONMENT=staging make test      # Override via environment
```

**When to use:** Configuration that users might override, sensible defaults.

#### Recursive Assignment (`=`)

Evaluated **on every use** (late binding). Creates dynamic variables:

```makefile
# Evaluated each time it's referenced
TIMESTAMP = $(shell date +%Y%m%d-%H%M%S)

# This evaluates to current time each time it's used
log-target: ## Create timestamped log file
	@echo "Creating log-$(TIMESTAMP).log"
	@touch log-$(TIMESTAMP).log
```

**When to use:** Values that change over time, dynamic computations.

### Environment Variables

Export variables to subprocesses for tools to access:

```makefile
# Export specific variables
export DATABASE_URL := postgresql://localhost/testdb
export FLASK_ENV := development
export PYTHONPATH := $(SRC_DIR)

# Or export all variables at once
.EXPORT_ALL_VARIABLES:

# Now all Make variables available to commands
test:
	$(UV) run pytest tests/  # pytest sees DATABASE_URL, etc.
```

---

## Platform and Runtime Detection

### Detecting Operating System

Make scripts must work across Linux, macOS, and Windows. Use conditional logic:

```makefile
# Detect OS
UNAME_S := $(shell uname -s)

ifeq ($(UNAME_S),Linux)
    PLATFORM := linux
    OPEN := xdg-open
    RM := rm -rf
endif

ifeq ($(UNAME_S),Darwin)
    PLATFORM := macos
    OPEN := open
    RM := rm -rf
endif

ifeq ($(OS),Windows_NT)
    PLATFORM := windows
    OPEN := start
    RM := rmdir /s /q
endif

# Use platform-specific variables
show-docs: ## Open documentation in browser
	$(OPEN) htmlcov/index.html
```

### Detecting Tool Availability

Check if required tools exist before using them:

```makefile
# Check if command exists
HAS_UV := $(shell command -v uv 2>/dev/null)
HAS_POETRY := $(shell command -v poetry 2>/dev/null)
HAS_DOCKER := $(shell command -v docker 2>/dev/null)

install:
ifdef HAS_UV
	uv sync --extra dev
else ifdef HAS_POETRY
	poetry install --with dev
else
	pip install -r requirements-dev.txt
endif
```

---

## Common Development Targets

### Installation and Setup

```makefile
.PHONY: install install-dev initialize

install: ## Install production dependencies
	$(UV) sync

install-dev: ## Install development dependencies
	$(UV) sync --extra dev

initialize: install-dev ## Initialize development environment
	mkdir -p logs tmp
	test -f .env || cp .env.example .env
	@echo "Development environment initialized!"
```

### Testing Targets

```makefile
.PHONY: test test-unit test-integration test-coverage

test: ## Run all tests
	$(UV) run pytest tests/ -v

test-unit: ## Run unit tests only
	$(UV) run pytest tests/unit/ -v

test-integration: ## Run integration tests only
	$(UV) run pytest tests/integration/ -v

test-coverage: ## Run tests with coverage report
	$(UV) run pytest --cov=app --cov-report=html --cov-report=term
	@echo "Coverage report: htmlcov/index.html"
```

### Code Quality Targets

```makefile
.PHONY: lint format check

lint: ## Run linters
	$(UV) run ruff check .
	$(UV) run mypy src/

format: ## Format code
	$(UV) run ruff format .
	$(UV) run ruff check --fix .

check: format lint test ## Run all quality checks
	@echo "All checks passed!"
```

### Cleanup Targets

```makefile
.PHONY: clean clean-pyc clean-test clean-build

clean: clean-pyc clean-test clean-build ## Remove all generated files

clean-pyc: ## Remove Python file artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*~" -delete

clean-test: ## Remove test and coverage artifacts
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf .mypy_cache
	rm -rf .ruff_cache

clean-build: ## Remove build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
```

---

## DevContainer Integration

### Separate DevContainer Makefile

Keep DevContainer-specific targets separate in `.devcontainer/Makefile`:

```makefile
# Main Makefile
-include .devcontainer/Makefile
```

```makefile
# .devcontainer/Makefile
.PHONY: dev-setup dev-test dev-lint

dev-setup: ## DevContainer-specific setup
	@echo "Running devcontainer setup..."
	uv sync --extra dev
	pre-commit install || true

dev-test: ## Run tests in devcontainer context
	uv run pytest tests/ -v --log-cli-level=DEBUG

dev-lint: ## Run linters with devcontainer-specific settings
	uv run ruff check .
	uv run mypy src/ --strict
```

**Pattern:** Use `-include` to optionally include environment-specific makefiles without errors if missing.

---

## Version Management with Semantic Versioning

### Automatic Version Detection

Extract version from canonical source (package metadata, git tags, or VERSION file):

```makefile
# Option 1: From pyproject.toml
VERSION := $(shell grep -m1 version pyproject.toml | cut -d'"' -f2)

# Option 2: From VERSION file
VERSION := $(shell cat VERSION)

# Option 3: From git tags
VERSION := $(shell git describe --tags --always)

# Use version in targets
build: ## Build version-stamped release
	@echo "Building version $(VERSION)"
	python -m build

docker-build: ## Build Docker image with version tag
	docker build -t myapp:$(VERSION) .
```

### Version Bumping

Create targets to increment semantic versions:

```makefile
.PHONY: version-patch version-minor version-major

version-patch: ## Increment patch version (x.y.Z)
	@bash -c ' \
		VERSION=$$(grep -m1 version pyproject.toml | cut -d'"' -f2); \
		PARTS=($${VERSION//./ }); \
		PARTS[2]=$$(($${PARTS[2]} + 1)); \
		NEW_VERSION=$${PARTS[0]}.$${PARTS[1]}.$${PARTS[2]}; \
		sed -i "s/version = \"$$VERSION\"/version = \"$$NEW_VERSION\"/" pyproject.toml; \
		git add pyproject.toml; \
		git commit -m "Bump version to $$NEW_VERSION"; \
		git tag -a v$$NEW_VERSION -m "Release $$NEW_VERSION"; \
	'

version-minor: ## Increment minor version (x.Y.0)
	@bash -c ' \
		VERSION=$$(grep -m1 version pyproject.toml | cut -d'"' -f2); \
		PARTS=($${VERSION//./ }); \
		PARTS[1]=$$(($${PARTS[1]} + 1)); \
		PARTS[2]=0; \
		NEW_VERSION=$${PARTS[0]}.$${PARTS[1]}.$${PARTS[2]}; \
		sed -i "s/version = \"$$VERSION\"/version = \"$$NEW_VERSION\"/" pyproject.toml; \
		git add pyproject.toml; \
		git commit -m "Bump version to $$NEW_VERSION"; \
		git tag -a v$$NEW_VERSION -m "Release $$NEW_VERSION"; \
	'

version-major: ## Increment major version (X.0.0)
	@bash -c ' \
		VERSION=$$(grep -m1 version pyproject.toml | cut -d'"' -f2); \
		PARTS=($${VERSION//./ }); \
		PARTS[0]=$$(($${PARTS[0]} + 1)); \
		PARTS[1]=0; \
		PARTS[2]=0; \
		NEW_VERSION=$${PARTS[0]}.$${PARTS[1]}.$${PARTS[2]}; \
		sed -i "s/version = \"$$VERSION\"/version = \"$$NEW_VERSION\"/" pyproject.toml; \
		git add pyproject.toml; \
		git commit -m "Bump version to $$NEW_VERSION"; \
		git tag -a v$$NEW_VERSION -m "Release $$NEW_VERSION"; \
	'
```

---

## Docker Integration

### Docker Build and Run Targets

```makefile
.PHONY: docker-build docker-run docker-stop docker-clean

DOCKER_IMAGE := myapp
DOCKER_TAG := latest

docker-build: ## Build Docker image
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

docker-run: ## Run Docker container
	docker run -d --name $(DOCKER_IMAGE) -p 8000:8000 $(DOCKER_IMAGE):$(DOCKER_TAG)

docker-stop: ## Stop Docker container
	docker stop $(DOCKER_IMAGE) || true
	docker rm $(DOCKER_IMAGE) || true

docker-clean: docker-stop ## Remove Docker images
	docker rmi $(DOCKER_IMAGE):$(DOCKER_TAG) || true

docker-compose-up: ## Start services with docker-compose
	docker compose up -d

docker-compose-down: ## Stop services with docker-compose
	docker compose down
```

### Version-Tagged Docker Images

```makefile
docker-build-versioned: ## Build and tag Docker image with version
	docker build -t $(DOCKER_IMAGE):$(VERSION) .
	docker tag $(DOCKER_IMAGE):$(VERSION) $(DOCKER_IMAGE):latest

docker-push: docker-build-versioned ## Push Docker image to registry
	docker push $(DOCKER_IMAGE):$(VERSION)
	docker push $(DOCKER_IMAGE):latest
```

---

## Output Control

### Silent vs. Verbose Commands

The `@` prefix suppresses command echoing (shows only output, not the command itself):

```makefile
# @ suppresses command echo - clean output
install:
	@echo "Installing dependencies..."
	@uv sync --extra dev
	@echo "Done!"

# Without @, shows command being executed
install-verbose:
	echo "Installing dependencies..."  # Shows this line
	uv sync --extra dev              # Shows this line
```

### Verbose and Quiet Modes

Use variables to control output verbosity:

```makefile
VERBOSE ?= 0

test:
ifeq ($(VERBOSE),1)
	$(UV) run pytest tests/ -vv
else
	$(UV) run pytest tests/ -q
endif

# Usage:
# make test          # Quiet
# make test VERBOSE=1  # Verbose
```

### Formatted Output with Colors

```makefile
COLOR_RESET := \033[0m
COLOR_INFO := \033[36m
COLOR_SUCCESS := \033[32m
COLOR_ERROR := \033[31m

help: ## Show this help message
	@echo "$(COLOR_INFO)Available targets:$(COLOR_RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_SUCCESS)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'

test: ## Run tests
	@echo "$(COLOR_INFO)Running tests...$(COLOR_RESET)"
	@$(UV) run pytest tests/ -v
	@echo "$(COLOR_SUCCESS)Tests passed!$(COLOR_RESET)"
```

### Output Discipline

**One line in, one line out.** Most targets need at most two echo statements:

```makefile
# ❌ Play-by-play narration
start:
	@echo "Starting platform services..."
	$(COMPOSE_CMD) up -d
	@echo "Starting frontend..."
	@cd frontend && bun run dev &
	@echo ""
	@echo "Platform running:"
	@echo "  Frontend: https://example.com"
	@echo "  API:      https://api.example.com"
	@echo ""
	@echo "Done!"

# ✅ One in, one out
start:
	@echo "Starting at https://example.com ..."
	$(COMPOSE_CMD) up -d
	@cd frontend && bun run dev > ../logs/frontend.log 2>&1 &
	@echo "Logs: tail -f logs/frontend.log"
```

**Opening echo:** What's happening + key URL/info (optional - skip if obvious)
**Closing echo:** Actionable next step (where logs are, what command to run next)

**Skip echoes entirely for:**
- Simple commands where output is self-evident (`test`, `lint`, `format`)
- Intermediate steps ("Starting X...", "Now doing Y...")
- Blank lines for formatting
- Info already in the `## comment`

---

## Error Handling

### Default Behavior (Stop on Error)

By default, Make stops on errors. Explicitly set this:

```makefile
.SHELLFLAGS := -ec

# -e: Exit on first error
# -c: Execute string
```

### Ignore Specific Errors

Some operations fail safely (e.g., removing non-existent files). Use `-` prefix to ignore errors:

```makefile
clean:
	-rm -rf build/      # Ignore error if build/ doesn't exist
	-rm -rf dist/       # Ignore error if dist/ doesn't exist
	@echo "Cleanup complete"
```

### Per-Target Error Handling

```makefile
.IGNORE: cleanup-legacy
cleanup-legacy:
	rm -rf old_build_dir/  # Won't fail if missing

cleanup: cleanup-legacy
	rm -rf build/
```

### Check Command Existence

```makefile
require-docker: ## Check Docker is installed
	@command -v docker >/dev/null 2>&1 || \
		(echo "Error: Docker is not installed" && exit 1)

docker-deploy: require-docker ## Deploy (only if Docker available)
	docker compose up -d
```

---

## Advanced Patterns

### Parallel Execution

Run independent tasks simultaneously (requires GNU Make 4.0+):

```makefile
.PHONY: parallel-checks

parallel-checks: ## Run lint, format check, and type check in parallel
	$(MAKE) -j4 lint type-check format-check

# Equivalent to running:
# make lint & make type-check & make format-check & wait
```

**When to use:** Combine independent quality checks that don't share state.

### Dynamic Targets

Generate targets from file listings:

```makefile
# Generate test targets from test files
TEST_FILES := $(wildcard tests/test_*.py)
TEST_TARGETS := $(TEST_FILES:tests/test_%.py=test-%)

# Pattern rule: test-users runs tests/test_users.py
$(TEST_TARGETS): test-%:
	$(UV) run pytest tests/test_$*.py -v

# Usage: make test-users, make test-auth, etc.
# List all test targets: make -n test-*
```

### Multi-line Commands with Continuation

Use `&&` to chain commands; use `\` for line continuation:

```makefile
deploy:
	@echo "Starting deployment..." && \
		docker build -t myapp . && \
		docker push myapp:latest && \
		kubectl apply -f k8s/ && \
		echo "Deployment complete!"

# Alternative with shell script for complex logic
initialize:
	@bash -c ' \
		if [ ! -f .env ]; then \
			echo "Creating .env from template..."; \
			cp .env.example .env; \
		fi; \
		mkdir -p logs tmp; \
		echo "Initialization complete!"; \
	'
```

### Dependency Chains

Build complex workflows by chaining targets:

```makefile
# Build depends on all tests passing
build: test lint
	@echo "Building application..."
	python -m build

# Deploy depends on build succeeding
deploy: build
	@echo "Deploying application..."
	# Deployment commands

# Pre-commit hook: run all checks before allowing commit
pre-commit: format lint test
	@echo "Ready to commit!"
```

---

## Best Practices Summary

### Documentation
Every target must have a help comment:

```makefile
# Format: target: ## Brief description
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST)
```

### Consistency
- Use consistent naming: `test`, `test-unit`, `test-coverage` (no `unittest` or `tests`)
- Prefer verbs: `clean`, `format`, `deploy` (not `cleanup`, `fmt`, `deployment`)
- Group related targets with dashes: `docker-build`, `docker-run`, `docker-stop`

### Simplicity
- Keep default targets simple and fast
- Avoid unnecessary flags (add flags only when they change behavior)
- Use variables for repeated values
- Keep recipes short; move complex logic to scripts

### Robustness
- Always define `.PHONY` for non-file targets
- Use `$(MAKE)` to call Make recursively
- Check for required commands before using them
- Handle platform differences with conditionals
- Clean up properly in error cases

---

## Complete Working Example

Here's a production-ready Makefile combining all concepts:

```makefile
# Project Makefile
.DEFAULT_GOAL := help

# Variables
UV := uv
PYTHON := python
SRC_DIR := src
TEST_DIR := tests
PROJECT_NAME := myapp

# Version from pyproject.toml
VERSION := $(shell grep -m1 version pyproject.toml | cut -d'"' -f2)

# Platform detection
UNAME_S := $(shell uname -s)
ifeq ($(OS),Windows_NT)
    RM := del /q
else
    RM := rm -f
endif

# Configuration (can be overridden)
ENVIRONMENT ?= development
LOG_LEVEL ?= info

# Colors
COLOR_RESET := \033[0m
COLOR_INFO := \033[36m
COLOR_SUCCESS := \033[32m

# Export environment variables
export PYTHONPATH := $(SRC_DIR)
export LOG_LEVEL := $(LOG_LEVEL)

# Phony targets
.PHONY: help install install-dev test test-unit test-coverage lint format \
        check clean clean-pyc clean-test clean-build run docker-build \
        docker-run docker-stop docker-clean deploy show-docs

help: ## Show this help message
	@echo "$(COLOR_INFO)$(PROJECT_NAME) - Available targets:$(COLOR_RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_SUCCESS)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'

install: ## Install production dependencies
	@echo "$(COLOR_INFO)Installing dependencies (version $(VERSION))...$(COLOR_RESET)"
	@$(UV) sync
	@echo "$(COLOR_SUCCESS)Installation complete!$(COLOR_RESET)"

install-dev: ## Install development dependencies
	@echo "$(COLOR_INFO)Installing dev dependencies...$(COLOR_RESET)"
	@$(UV) sync --extra dev
	@echo "$(COLOR_SUCCESS)Dev setup complete!$(COLOR_RESET)"

test: ## Run all tests
	@echo "$(COLOR_INFO)Running tests...$(COLOR_RESET)"
	@$(UV) run pytest $(TEST_DIR)/ -v

test-unit: ## Run unit tests only
	@$(UV) run pytest $(TEST_DIR)/unit/ -v

test-coverage: ## Run tests with coverage report
	@echo "$(COLOR_INFO)Running tests with coverage...$(COLOR_RESET)"
	@$(UV) run pytest --cov=$(SRC_DIR) --cov-report=html --cov-report=term
	@echo "$(COLOR_SUCCESS)Coverage report: htmlcov/index.html$(COLOR_RESET)"

lint: ## Run linters
	@echo "$(COLOR_INFO)Running linters...$(COLOR_RESET)"
	@$(UV) run ruff check .
	@$(UV) run mypy $(SRC_DIR)/
	@echo "$(COLOR_SUCCESS)Linting passed!$(COLOR_RESET)"

format: ## Format code
	@echo "$(COLOR_INFO)Formatting code...$(COLOR_RESET)"
	@$(UV) run ruff format .
	@$(UV) run ruff check --fix .

check: format lint test ## Run all quality checks
	@echo "$(COLOR_SUCCESS)All checks passed!$(COLOR_RESET)"

clean: clean-pyc clean-test clean-build ## Remove all generated files
	@echo "$(COLOR_SUCCESS)Cleanup complete!$(COLOR_RESET)"

clean-pyc: ## Remove Python file artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

clean-test: ## Remove test and coverage artifacts
	rm -rf .pytest_cache htmlcov .coverage .mypy_cache .ruff_cache

clean-build: ## Remove build artifacts
	rm -rf build/ dist/ *.egg-info

run: ## Run application
	@echo "$(COLOR_INFO)Starting application ($(ENVIRONMENT) mode)...$(COLOR_RESET)"
	@$(UV) run $(PYTHON) -m $(PROJECT_NAME).cli

docker-build: ## Build Docker image (version $(VERSION))
	docker build -t $(PROJECT_NAME):$(VERSION) .

docker-run: docker-build ## Build and run Docker container
	docker run -d --name $(PROJECT_NAME) -p 8000:8000 $(PROJECT_NAME):$(VERSION)

docker-stop: ## Stop Docker container
	docker stop $(PROJECT_NAME) || true
	docker rm $(PROJECT_NAME) || true

docker-clean: docker-stop ## Remove Docker image
	docker rmi $(PROJECT_NAME):$(VERSION) || true

deploy: test lint ## Deploy application
	@echo "$(COLOR_INFO)Deploying version $(VERSION)...$(COLOR_RESET)"
	docker push $(PROJECT_NAME):$(VERSION)
	@echo "$(COLOR_SUCCESS)Deployment complete!$(COLOR_RESET)"

show-docs: ## Open documentation in browser
	@command -v open >/dev/null && open htmlcov/index.html || \
	 command -v xdg-open >/dev/null && xdg-open htmlcov/index.html || \
	 command -v start >/dev/null && start htmlcov/index.html || \
	 echo "Please open htmlcov/index.html manually"
```

---

## Quick Reference

| Concept | Syntax | When to Use |
|---------|--------|------------|
| **Immediate** | `VAR := value` | Constants, one-time evaluations |
| **Conditional** | `VAR ?= value` | Defaults, overrideable settings |
| **Recursive** | `VAR = value` | Dynamic values, time-dependent |
| **Phony** | `.PHONY: target` | Commands that don't create files |
| **File target** | `file: source` | Build artifacts with dependencies |
| **Silent** | `@command` | Cleaner output |
| **Error ignore** | `-command` | Safe failures (rm non-existent files) |
| **Parallel** | `$(MAKE) -j4 task1 task2` | Independent tasks |

---

## Common Pitfalls

1. **Forgetting `.PHONY`**: `make test` fails if a `test` file exists
2. **Tab indentation required**: Recipe lines must start with actual tab, not spaces
3. **Variable expansion timing**: `=` evaluates late, `:=` early
4. **Platform-specific commands**: Check OS before using `rm -rf` vs. `rmdir /s`
5. **Complex logic in recipes**: Move shell scripts to separate files for maintainability
6. **Mixing recursive and immediate**: Use `:=` for clarity unless you need late binding
7. **Not exporting variables**: Subprocesses won't see Make variables unless exported
8. **Echo spam**: Avoid play-by-play ("Starting...", "Now doing...", "Done!"). One line in, one line out.
