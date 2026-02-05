---
name: python-ty
description: Fast Python type checking with ty (by Astral). Use when checking Python types, running type checks in CI, or setting up type checking for Python projects. Triggers on "type check", "ty check", "python types", or type error debugging.
---

# Python Type Checking with `ty`

`ty` is an extremely fast Python type checker from Astral (makers of Ruff).

## Quick Start

```bash
# Run type checker (no install needed)
uvx ty check

# Check specific files
uvx ty check src/ tests/
```

## Installation (Optional)

```bash
# Install globally
uv tool install ty@latest

# Update
uv tool upgrade ty
```

## Common Tasks

```bash
# Watch mode - auto-recheck on file changes
ty check --watch

# Target specific Python version
ty check --python-version 3.11

# Concise output
ty check --format concise

# Exclude test files
ty check --exclude "**/test_*.py"
```

## Configuration File

Create `ty.toml` in project root (auto-discovered):

```toml
python-version = "3.11"
exclude = ["**/test_*.py", "**/__pycache__/**"]
format = "concise"
```

## CI/CD

```bash
# Strict CI check
ty check --error all --error-on-warning --no-progress
```

Exit codes: `0` = success, `1` = errors found, `2` = internal error

---

## Advanced Options

### Severity Control

```bash
ty check --error all        # All issues as errors
ty check --warn typing      # Typing issues as warnings
ty check --ignore unused    # Ignore unused imports
```

### Environment Targeting

```bash
ty check --python /path/to/python    # Specific interpreter
ty check --venv /path/to/venv        # Target virtualenv
ty check --python-platform linux     # Cross-platform check
ty check --extra-search-path ./stubs/
```

### Output Formats

```bash
ty check --format full       # Detailed (default)
ty check --format concise    # Compact
ty check --format github     # GitHub Actions annotations
ty check --format gitlab     # GitLab CI format
ty check --color never       # No colors
ty check --no-progress       # Hide progress bar
ty check -v                  # Verbose
ty check -q                  # Quiet
```

### Other Commands

```bash
ty server                              # Start LSP server
ty version                             # Show version
ty generate-shell-completion zsh       # Shell completions
```
