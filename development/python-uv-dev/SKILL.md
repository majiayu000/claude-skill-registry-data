---
name: python-uv-dev
description: Python development using the `uv` package manager. Use this skill when working with Python projects that use `uv` for dependency management, when initializing new Python projects, or when the user mentions `uv`, `pyproject.toml`, or asks about Python package management best practices.
---

# Python Development with uv

## Overview

This skill provides comprehensive guidance for Python development using `uv`, an extremely fast Python package installer and resolver written in Rust. It covers project initialization, dependency management, tool execution, monorepo patterns, and integration with modern Python tooling.

## When to Use This Skill

Use this skill when:
- Working with existing Python projects that use `uv` (indicated by presence of `uv.lock` or `uv` commands in documentation)
- Initializing new Python projects
- Managing dependencies in Python projects
- Setting up pre-commit hooks with `uv`
- Configuring monorepo/workspace projects
- Adding or updating Python dependencies
- Running development tools (pytest, ruff, mypy, etc.)
- The user explicitly mentions `uv` or asks about modern Python package management

## Quick Start

### Initial Setup

To start using `uv` in a Python project:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Initialize a new project
uv init my-project
cd my-project

# Or initialize in existing directory
uv init

# Sync dependencies (creates/updates .venv and uv.lock)
uv sync
```

### Essential Commands

```bash
# Install/sync dependencies from pyproject.toml
uv sync

# Add a dependency
uv add requests pandas

# Add a development dependency
uv add --dev pytest ruff

# Remove a dependency
uv remove requests

# Run a command with the project environment
uv run python script.py
uv run pytest
uv run ruff check

# Run a tool without adding it as a dependency
uvx ruff check .
uvx mypy src/

# Update dependencies
uv lock --upgrade
uv sync
```

## Core Workflows

### 1. Tool Execution

**Critical Pattern:** All development tools defined in `pyproject.toml` must be executed as a subcommand of `uv run`.

```bash
# ❌ INCORRECT - May use wrong version or fail
ruff check file.py
pytest
mypy src/

# ✅ CORRECT - Uses project-defined tool versions
uv run ruff check file.py
uv run pytest
uv run mypy src/
```

This ensures the project's defined tool versions are used rather than any globally installed ones.

### 2. Project Initialization

When creating a new Python project:

```bash
# Create new project with structure
uv init my-project
cd my-project

# Set Python version
echo "3.12" > .python-version

# Add initial dependencies
uv add numpy pandas

# Add development tools
uv add --dev pytest pytest-cov ruff mypy

# Initialize git and pre-commit
git init
uv add --dev pre-commit
uv run pre-commit install
```

See `assets/pyproject.toml.template` for a complete starting configuration.

### 3. Dependency Management

#### Adding Dependencies

```bash
# Add runtime dependency
uv add requests

# Add multiple dependencies
uv add numpy pandas matplotlib

# Add with version constraint
uv add "fastapi>=0.100.0"

# Add from git repository
# Edit pyproject.toml to add:
# [tool.uv.sources]
# mypackage = { git = "https://github.com/user/repo", branch = "main" }
uv add mypackage
```

#### Development Dependencies

Modern `uv` projects use `dependency-groups` instead of the older `dev-dependencies`:

```toml
[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]
```

Add dev dependencies with:
```bash
uv add --dev pytest ruff mypy
```

#### Git Dependencies

For dependencies from git repositories, use `[tool.uv.sources]`:

```toml
[tool.uv.sources]
mylib = { git = "https://github.com/user/mylib", branch = "main" }
another-lib = { git = "https://github.com/user/another", tag = "v1.0.0" }
```

Then add the dependency normally:
```bash
uv add mylib another-lib
```

### 4. Monorepo/Workspace Projects

For projects with multiple packages, use workspace configuration:

**Root pyproject.toml:**
```toml
[tool.uv.workspace]
members = [
    "packages/*",
]

[tool.uv.sources]
# Internal workspace packages
mylib = { workspace = true }
another-package = { workspace = true }

# External dependencies
external-lib = { git = "https://github.com/user/repo", branch = "main" }
```

**Package pyproject.toml:**
```toml
[project]
name = "mylib"
version = "0.1.0"
dependencies = [
    "another-package",  # Can reference other workspace packages
]

[tool.uv.sources]
another-package = { workspace = true }
```

Commands work the same way from the root:
```bash
# Sync all workspace packages
uv sync

# Run tools
uv run pytest
```

See `assets/pyproject-monorepo.toml.template` for complete example.

### 5. Pre-commit Integration

Configure pre-commit hooks to use `uv run` for consistency. This ensures that all pre-commit hooks use the project's defined tool versions.

Setup:
```bash
uv add --dev pre-commit
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
```

See `assets/.pre-commit-config.yaml.template` for a complete pre-commit configuration template with ruff linting, formatting, and pytest.

## Common Patterns

### Testing Workflows

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test file
uv run pytest tests/test_api.py

# Run with markers
uv run pytest -m "not slow"

# Run in parallel
uv add --dev pytest-xdist
uv run pytest -n auto
```

### Code Quality

```bash
# Lint and fix
uv run ruff check --fix

# Format code
uv run ruff format

# Type checking
uv add --dev mypy
uv run mypy src/

# Run all quality checks
uv run ruff check --fix && uv run ruff format && uv run mypy src/ && uv run pytest
```

### Performance Testing

```bash
# Memory profiling
uv add --dev pytest-memray
uv run pytest --memray

# CPU profiling with py-spy
uvx py-spy record -o profile.svg -- uv run python script.py
```

### Building and Publishing

```bash
# Build package
uv build

# Publish to PyPI
uv publish

# Build Docker image with uv
# See Dockerfile patterns in references/docker-patterns.md
```

## Best Practices

### Always Use `uv run`

Never execute development tools directly. Always prefix with `uv run`:

```bash
# Testing
uv run pytest
uv run pytest --cov

# Linting
uv run ruff check --fix
uv run ruff format

# Type checking
uv run mypy src/

# Custom scripts
uv run python scripts/process_data.py
```

### Dependency Groups Over dev-dependencies

Use modern `[dependency-groups]` syntax instead of deprecated patterns:

```toml
# ✅ CORRECT - Modern syntax
[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.1.0",
]

# ❌ AVOID - Older syntax
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
]
```

### Lock File Hygiene

- Commit `uv.lock` to version control for reproducible builds
- Run `uv lock --upgrade` periodically to update dependencies
- Use `uv sync` after pulling changes to ensure environment matches lock file

### Platform-Specific Dependencies

Handle platform differences in `pyproject.toml`:

```toml
[project]
dependencies = [
    "jax; sys_platform == 'darwin'",
    "jax[cuda]; sys_platform == 'linux'",
]
```

### Script Entrypoints

Define CLI entrypoints in `pyproject.toml`:

```toml
[project.scripts]
my-cli = "mypackage.cli:main"
process-data = "mypackage.scripts:process"
```

Then run with:
```bash
uv run my-cli --help
```

## Code Quality Guidelines

For comprehensive code quality and refactoring guidelines specific to `uv` projects, see `references/code-quality-guidelines.md`. Key principles include:

- Prioritize architecture over implementation
- Use library-provided types for better type safety
- Refactor existing code when solving problems
- Apply DRY principle correctly
- Keep related code together
- Prefer simple solutions
- Aim to be correct rather than defensive
- Fail fast with clear errors

## Troubleshooting

### Environment Issues

```bash
# Recreate virtual environment
rm -rf .venv
uv sync

# Clear cache
uv cache clean

# Verify Python version
cat .python-version
python --version
```

### Dependency Conflicts

```bash
# See what changed
git diff uv.lock

# Force update specific package
uv add "package>=1.0.0" --upgrade

# Check dependency tree
uv pip tree
```

### Tool Not Found

```bash
# Ensure tool is added as dev dependency
uv add --dev pytest

# Use uv run prefix
uv run pytest  # not just `pytest`

# For one-off tools, use uvx
uvx ruff check .    # runs without installing
```

## Resources

### Templates (assets/)

- `pyproject.toml.template` - Template for standard Python project
- `pyproject-monorepo.toml.template` - Template for workspace/monorepo project
- `.pre-commit-config.yaml.template` - Pre-commit hook configuration
- `.python-version.template` - Python version specification

### Documentation (references/)

- `uv-commands.md` - Comprehensive command reference and usage patterns
- `code-quality-guidelines.md` - Code quality and refactoring best practices
- `pyproject-patterns.md` - Common pyproject.toml patterns and configurations
- `docker-patterns.md` - Docker integration patterns for uv projects

### Scripts (scripts/)

- `init_uv_project.py` - Initialize new uv project with best practices
- `validate_pyproject.py` - Validate pyproject.toml structure and configuration
