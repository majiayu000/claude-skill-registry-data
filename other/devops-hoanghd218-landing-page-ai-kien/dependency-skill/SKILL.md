---
name: dependency-skill
description: Manage Python dependencies using uv package manager. Use when installing, adding, removing, or updating packages. Always prefer uv over pip.
allowed-tools: Bash, Read
---

# Dependency Skill

## Purpose
Manage Python dependencies efficiently using the `uv` package manager.

## Instructions

### Initialize a new project
```bash
uv init
```

### Add production dependencies
```bash
uv add typer rich textual pydantic tinydb questionary pyfiglet python-dateutil
```

### Add development dependencies
```bash
uv add --dev pytest pytest-cov black ruff mypy
```

### Sync dependencies (install from lock file)
```bash
uv sync
```

### Run scripts
```bash
uv run python -m package_name.main
uv run pytest
```

### Update dependencies
```bash
uv lock --upgrade
uv sync
```

### Remove a dependency
```bash
uv remove package-name
```

## Common Dependency Sets

### Todo App Dependencies
```bash
# Core
uv add typer rich textual pydantic tinydb questionary pyfiglet python-dateutil

# Development
uv add --dev pytest pytest-cov black ruff
```

### Web App Dependencies
```bash
uv add fastapi uvicorn sqlmodel httpx
```

## Examples

### Full project setup
```bash
# Initialize
uv init

# Add all dependencies at once
uv add typer[all] rich textual pydantic tinydb questionary pyfiglet python-dateutil

# Add dev dependencies
uv add --dev pytest pytest-cov

# Sync to install
uv sync

# Verify installation
uv run python -c "import rich; print(rich.__version__)"
```

## Best Practices

- Always use `uv` instead of `pip` for modern Python projects
- Lock dependencies with `uv.lock` for reproducibility
- Separate dev dependencies from production
- Run commands with `uv run` to ensure correct environment
- Update dependencies regularly with `uv lock --upgrade`
