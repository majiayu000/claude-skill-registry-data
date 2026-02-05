---
name: python-analyzer
description: Format and analyze Python code using ruff (formatting/linting) and ty (static type checking). Use when the user asks to format Python code, run linting, check types, fix code style issues, or analyze Python code quality.
---

# Python Code Analyzer

Format and analyze Python code using ruff and ty.

## Tools

- **ruff**: Fast Python linter and formatter (replaces black, isort, flake8)
- **ty**: Static type checker for Python

## Workflow

### 1. Format Code

Format Python files with ruff:

```bash
# Format single file
ruff format path/to/file.py

# Format directory
ruff format .

# Check formatting without applying changes
ruff format --check .
```

### 2. Lint Code

Run linter to find issues:

```bash
# Lint and show issues
ruff check .

# Auto-fix fixable issues
ruff check --fix .

# Show all fixable issues
ruff check --fix --unsafe-fixes .
```

### 3. Type Check

Run static type analysis with ty:

```bash
# Check types in current directory
ty check .

# Check specific file
ty check path/to/file.py
```

## Full Analysis Command

Run complete analysis (format + lint + type check):

```bash
ruff format . && ruff check --fix . && ty check .
```

## Common Issues and Fixes

### Ruff

- **Import sorting**: Auto-fixed with `ruff check --fix`
- **Unused imports**: Auto-fixed with `ruff check --fix`
- **Line length**: Configure in `pyproject.toml` under `[tool.ruff]`

### Ty

- **Missing type annotations**: Add type hints to function signatures
- **Type mismatches**: Review and correct variable/return types
- **Import errors**: Ensure all dependencies are installed

## Configuration

Both tools read from `pyproject.toml`:

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[tool.ty]
python-version = "3.11"
```
