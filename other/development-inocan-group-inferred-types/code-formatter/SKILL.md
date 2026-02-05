---
name: code-formatter
description: Format Python code using black, ruff, and isort to ensure consistent style. This skill should be used before committing code to maintain code quality standards and pass CI/CD checks.
---

# Code Formatter

Format Python code consistently using industry-standard tools (black, ruff, isort).

## Purpose

Automated code formatting eliminates style discussions and ensures consistent, readable code across the project.

## When to Use

Use this skill:
- Before every commit
- After refactoring or adding new code
- When setting up pre-commit hooks
- To fix linting errors flagged by CI

## Tools

### Black - Code Formatter

The uncompromising Python code formatter:

```bash
# Format single file
uv run black file.py

# Format directory
uv run black prism/

# Check without modifying
uv run black --check prism/

# Show what would change
uv run black --diff prism/
```

### Ruff - Fast Linter

Extremely fast Python linter:

```bash
# Lint and auto-fix
uv run ruff check prism/ --fix

# Just check
uv run ruff check prism/

# Specific rules
uv run ruff check prism/ --select E,F,W
```

### isort - Import Organizer

Sorts imports automatically:

```bash
# Sort imports
uv run isort prism/

# Check only
uv run isort --check prism/

# Show diff
uv run isort --diff prism/
```

## Configuration

### pyproject.toml

```toml
[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310']
include = '\.pyi?$'
extend-exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''

[tool.ruff]
line-length = 100
target-version = "py38"

# Select rules
select = [
    "E",  # pycodestyle errors
    "F",  # pyflakes
    "W",  # pycodestyle warnings
    "I",  # isort
    "N",  # pep8-naming
    "UP", # pyupgrade
    "B",  # flake8-bugbear
]

# Ignore specific rules
ignore = [
    "E501",  # line too long (handled by black)
    "B008",  # do not perform function calls in argument defaults
]

exclude = [
    ".git",
    ".venv",
    "build",
    "__pycache__",
]

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports in __init__.py

[tool.isort]
profile = "black"
line_length = 100
known_third_party = ["torch", "numpy", "matplotlib"]
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]
```

## Running All Formatters

### Single Command

```bash
# Format everything
uv run black prism/ && uv run isort prism/ && uv run ruff check prism/ --fix
```

### Create Formatting Script

```bash
# scripts/format.sh
#!/bin/bash
set -e

echo "Running black..."
uv run black prism/ tests/

echo "Running isort..."
uv run isort prism/ tests/

echo "Running ruff..."
uv run ruff check prism/ tests/ --fix

echo "✓ Formatting complete"
```

Make executable:
```bash
chmod +x scripts/format.sh
./scripts/format.sh
```

## Pre-commit Hooks

Automatically format on commit:

### Install pre-commit

```bash
uv add --dev pre-commit
```

### Create .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-merge-conflict
```

### Install hooks

```bash
uv run pre-commit install

# Run on all files
uv run pre-commit run --all-files
```

## Common Formatting Patterns

### Import Organization

isort organizes imports in this order:

```python
# Future imports
from __future__ import annotations

# Standard library
import os
import sys
from pathlib import Path
from typing import Optional

# Third-party
import numpy as np
import torch
from torch import nn, Tensor

# Local imports
from prism.core.telescope import Telescope
from prism.utils.transforms import fft, ifft

# Relative imports
from .grid import Grid
from ..models import ProgressiveDecoder
```

### Line Length

Black enforces 88 characters by default, but configurable:

```python
# Will be reformatted to multiple lines if too long
def very_long_function_name(
    parameter_one: str,
    parameter_two: int,
    parameter_three: float
) -> bool:
    return True
```

### String Formatting

Black normalizes quotes:

```python
# Black uses double quotes
text = "Hello"

# Except when single quotes avoid escaping
text = 'He said "Hello"'
```

## Type Checking with mypy

After formatting, validate types:

```bash
# Install mypy
uv add --dev mypy

# Run type checking
uv run mypy prism/

# Configuration
[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = "torch.*"
ignore_missing_imports = true
```

## CI Integration

### GitHub Actions

```yaml
# .github/workflows/lint.yml
name: Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install dependencies
        run: |
          pip install uv
          uv sync --extra dev

      - name: Run ruff
        run: uv run ruff check .

      - name: Run black
        run: uv run black --check .

      - name: Run isort
        run: uv run isort --check .

      - name: Run mypy
        run: uv run mypy prism/
```

## Workflow

### Before Committing

```bash
# 1. Format code
uv run black prism/ tests/
uv run isort prism/ tests/

# 2. Fix linting issues
uv run ruff check prism/ tests/ --fix

# 3. Check remaining issues
uv run ruff check prism/ tests/

# 4. Type check
uv run mypy prism/

# 5. Run tests
uv run pytest

# 6. Commit
git add .
git commit -m "feat: add new feature"
```

### With Pre-commit Hooks

```bash
# Hooks run automatically on commit
git add .
git commit -m "feat: add new feature"

# If hooks fail, fix and try again
# (some hooks auto-fix, so stage the fixes)
git add .
git commit -m "feat: add new feature"
```

## Fixing Common Issues

### Long Lines

```python
# Ruff flags E501
# Before
really_long_variable_name = some_function(arg1, arg2, arg3, arg4, arg5, arg6)

# Black auto-fixes
really_long_variable_name = some_function(
    arg1, arg2, arg3, arg4, arg5, arg6
)
```

### Unused Imports

```python
# Ruff flags F401
# Before
import torch
import numpy as np  # Not used

# Fix: Remove unused import
import torch
```

### Undefined Names

```python
# Ruff flags F821
# Before
result = undefined_variable

# Fix: Define or import
from module import undefined_variable
result = undefined_variable
```

## Ignoring Specific Rules

When needed (use sparingly):

```python
# Ignore for specific line
result = some_function()  # noqa: E501

# Ignore specific rule
result = some_function()  # noqa: F401

# Ignore file-wide
# ruff: noqa: E501

# Type ignore for mypy
result = complex_function()  # type: ignore[misc]
```

## Checklist

Before committing:
- [ ] Black formatting applied
- [ ] Imports organized with isort
- [ ] Ruff checks pass (or issues documented)
- [ ] mypy type checking passes
- [ ] Pre-commit hooks configured (optional but recommended)
- [ ] CI will pass formatting checks
