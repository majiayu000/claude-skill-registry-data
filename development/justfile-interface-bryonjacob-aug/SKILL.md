---
name: justfile-interface
description: Baseline justfile commands - exact comment strings, all projects implement these
---

# Justfile Standard Interface (Level 0)

All projects implement these commands. Exact comment strings required. Stub unimplemented: `@echo "⚠️ <command> not implemented"`.

## Baseline Commands

```just
set shell := ["bash", "-uc"]

# Show all available commands
default:
    @just --list

# Install dependencies and setup development environment
dev-install:
    <install deps, create venvs, download tools>

# Format code (auto-fix)
format:
    <auto-fix whitespace/style, fastest check>

# Lint code (auto-fix, complexity threshold=10)
lint:
    <auto-fix linting, complexity=10 blocks>

# Type check code
typecheck:
    <static type checking, no auto-fix>

# Run unit tests
test:
    <unit tests only (unmarked/untagged), fast, show timing>

# Run unit tests with coverage threshold (96%)
coverage:
    <unit tests with 96% threshold, blocks if below>

# Run all quality checks (format, lint, typecheck, coverage - fastest first)
check-all: format lint typecheck coverage
    @echo "✅ All checks passed"

# Remove generated files and artifacts
clean:
    <remove build artifacts, caches, generated files>
```

## Rules

**Exact comments:**
Comment strings must match exactly. Validation checks these.

**All commands present:**
Stub missing commands. Don't skip. Stubs show intent, enable validation.

**check-all order:**
format → lint → typecheck → coverage (fastest first, fail fast)

**check-all dependencies:**
Must run all four checks. Exact order matters.

**Testing philosophy:**
- Unit tests (unmarked): 96% coverage, blocks merge
- Integration tests: separate command (level 1), never blocks

## Stack Implementations

**Python:**
```just
dev-install:
    uv sync --all-extras

format:
    uv run ruff format .
    uv run ruff check --fix .

lint:
    uv run ruff check . --select C90 --config "lint.mccabe.max-complexity=10"

typecheck:
    uv run mypy .

test:
    uv run pytest -v -m "not integration" --durations=10

coverage:
    uv run pytest -m "not integration" --cov=app --cov-fail-under=96

clean:
    rm -rf .venv __pycache__ .pytest_cache .coverage htmlcov
```

**JavaScript:**
```just
dev-install:
    pnpm install

format:
    pnpm exec prettier --write .

lint:
    pnpm exec eslint . --fix --max-warnings 0

typecheck:
    pnpm exec tsc --noEmit

test:
    pnpm vitest run --project unit --reporter=verbose

coverage:
    pnpm vitest run --coverage --reporter=verbose

clean:
    rm -rf node_modules .next out dist coverage
```

**Java:**
```just
dev-install:
    mvn clean install -DskipTests

format:
    mvn spotless:apply

lint:
    mvn spotless:check pmd:check spotbugs:check

typecheck:
    @echo "⚠️ typecheck not applicable (Java is statically typed)"

test:
    mvn test -Dsurefire.printSummary=true

coverage:
    mvn verify jacoco:check -Dsurefire.printSummary=true

clean:
    mvn clean
```

## Validation

Check justfile conforms:
```bash
# All commands present
grep -q "^dev-install:" justfile
grep -q "^format:" justfile
# ... etc

# Comments exact
grep -q "# Show all available commands" justfile
grep -q "# Install dependencies and setup development environment" justfile
# ... etc

# check-all dependencies
grep -q "^check-all: format lint typecheck coverage$" justfile
```

## Stubbing Pattern

```just
# <exact comment string>
command-name:
    @echo "⚠️  command-name not implemented"
```

Example:
```just
# Type check code
typecheck:
    @echo "⚠️  typecheck not implemented"
```

## Success Criteria

Baseline complete when:
- All 9 commands present
- All comments match exactly
- check-all runs format → lint → typecheck → coverage
- Stubs or implementations for all commands
- `just check-all` exits 0 (or fails meaningfully on quality issues)
