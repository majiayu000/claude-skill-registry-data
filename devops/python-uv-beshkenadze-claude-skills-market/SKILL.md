---
name: python-uv
description: Manage Python projects with uv. Use when creating Python projects, managing dependencies, running scripts, or installing Python versions.
version: 1.0.0
---

# Python uv

## Overview

Expert guidance for using **uv** - the extremely fast Python package and project manager by Astral. Written in Rust, 10-100x faster than pip. Replaces pip, pip-tools, pipx, poetry, pyenv, and virtualenv.

## Instructions

### 1. New Project Setup

```bash
# Create new project
uv init my-project
cd my-project

# Or initialize in current directory
uv init
```

Creates standard structure:
```
my-project/
├── .python-version
├── .gitignore
├── pyproject.toml
├── README.md
└── main.py
```

### 2. Dependency Management

```bash
# Add dependencies
uv add requests
uv add 'flask>=2.0'
uv add httpx aiofiles          # Multiple packages

# Add dev dependencies
uv add --dev pytest ruff mypy

# Add optional dependencies
uv add --optional gui pyqt6

# Remove dependencies
uv remove requests

# Sync environment with lockfile
uv sync

# Update lockfile
uv lock
uv lock --upgrade-package flask  # Upgrade specific
```

### 3. Running Code

```bash
# Run script (auto-syncs environment)
uv run main.py

# Run command in project environment
uv run pytest
uv run ruff check .

# Run with env file
uv run --env-file .env main.py

# Run with extra dependencies (not installed)
uv run --with rich main.py
```

**Key insight:** Use `uv run` instead of activating venv. It's faster and ensures sync.

### 4. Python Version Management

```bash
# Install latest Python
uv python install

# Install specific version
uv python install 3.12
uv python install 3.11 3.12    # Multiple versions

# Set as default (creates python/python3 symlinks)
uv python install --default

# List installed versions
uv python list

# Pin project to specific version
uv python pin 3.12
```

### 5. Tool Management (replaces pipx)

```bash
# Run tool without installing
uvx ruff check .
uvx black --check .

# Install tool globally
uv tool install ruff
uv tool install 'httpie>=3.0'

# Upgrade tool
uv tool upgrade ruff

# List installed tools
uv tool list
```

### 6. pip Interface (for compatibility)

```bash
# Install packages
uv pip install flask
uv pip install -r requirements.txt

# Compile requirements
uv pip compile requirements.in -o requirements.txt

# Show installed packages
uv pip list
uv pip show flask
```

## Examples

### Example: Create FastAPI Project

**Input:** "Create a new FastAPI project with testing"

```bash
uv init fastapi-app
cd fastapi-app
uv add fastapi uvicorn
uv add --dev pytest httpx pytest-asyncio
```

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

```bash
# Run development server
uv run uvicorn main:app --reload

# Run tests
uv run pytest
```

### Example: Migrate from requirements.txt

**Input:** "Migrate existing project to uv"

```bash
# In project directory
uv init

# Import existing dependencies
uv add -r requirements.txt

# Remove old requirements.txt (optional)
rm requirements.txt

# Now use uv.lock for reproducibility
git add uv.lock pyproject.toml
```

### Example: Run One-off Script

**Input:** "Run a script with dependencies not in project"

```bash
# Run with temporary dependencies
uv run --with pandas --with matplotlib script.py

# Or use inline metadata (PEP 723)
```

```python
# /// script
# dependencies = ["pandas", "matplotlib"]
# ///

import pandas as pd
import matplotlib.pyplot as plt
# ...
```

```bash
uv run script.py  # Auto-installs inline deps
```

### Example: CI/CD Setup

**Input:** "Setup GitHub Actions with uv"

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Install uv
        uses: astral-sh/setup-uv@v7

      - name: Set up Python
        run: uv python install

      - name: Install dependencies
        run: uv sync --locked --all-extras --dev

      - name: Run tests
        run: uv run pytest

      - name: Run linter
        run: uv run ruff check .
```

### Example: Docker Production

**Input:** "Create Dockerfile with uv"

```dockerfile
FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment for production
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies (no dev, locked versions)
RUN uv sync --locked --no-dev --no-install-project

# Copy application
COPY . .

# Install project
RUN uv sync --locked --no-dev

CMD ["uv", "run", "python", "-m", "myapp"]
```

## Quick Reference

| Task | Command |
|------|---------|
| New project | `uv init` |
| Add package | `uv add <pkg>` |
| Add dev dep | `uv add --dev <pkg>` |
| Remove package | `uv remove <pkg>` |
| Sync env | `uv sync` |
| Run script | `uv run <script.py>` |
| Run command | `uv run <cmd>` |
| Install Python | `uv python install 3.12` |
| Run tool (no install) | `uvx <tool>` |
| Install tool | `uv tool install <tool>` |

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `UV_COMPILE_BYTECODE=1` | Compile .pyc (faster startup) |
| `UV_NO_SYNC=1` | Skip sync in `uv run` |
| `UV_LINK_MODE=copy` | Copy files instead of hardlink |
| `UV_MANAGED_PYTHON=1` | Only use uv-managed Python |

## Guidelines

### Do

- Use `uv run` instead of activating venv
- Commit `uv.lock` for reproducible builds
- Use `--locked` in CI/CD
- Use `--dev` for test/lint dependencies
- Use `uvx` for one-off tool usage

### Don't

- Activate venv manually (use `uv run`)
- Forget to commit `uv.lock`
- Mix pip and uv in same project
- Skip `--locked` in production

## Migration Cheatsheet

| Old Tool | uv Equivalent |
|----------|---------------|
| `pip install X` | `uv add X` or `uv pip install X` |
| `pip install -r requirements.txt` | `uv add -r requirements.txt` |
| `python script.py` | `uv run script.py` |
| `pipx run ruff` | `uvx ruff` |
| `pipx install ruff` | `uv tool install ruff` |
| `pyenv install 3.12` | `uv python install 3.12` |
| `poetry add X` | `uv add X` |
| `poetry install` | `uv sync` |
| `poetry lock` | `uv lock` |
