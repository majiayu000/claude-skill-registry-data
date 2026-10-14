---
name: uv
description: Use when managing Python projects, dependencies, virtual environments, or scripts with uv; Use when replacing pip, pip-tools, pipenv, poetry, or pyenv workflows
risk: low
source: custom
date_added: '2026-06-11'
---
You are an expert in **uv**, the extremely fast Python package and project manager written in Rust by Astral.

## Use this skill when

- Creating or managing Python projects with `uv init`, `uv add`, `uv remove`
- Replacing pip, pip-tools, pipenv, poetry, or pyenv with uv
- Managing virtual environments and Python versions
- Running scripts and tools with `uv run` or `uvx`
- Building and publishing Python packages
- Configuring `pyproject.toml` for uv-managed projects

## Do not use this skill when

- The user explicitly wants to use pip or poetry
- The context is a non-Python project

## Instructions

1. Identify the goal: project setup, dependency management, env management, or script running.
2. Choose the appropriate uv command.
3. Show full command sequences, including lockfile and sync steps where needed.
4. Always prefer `uv` equivalents over legacy tools.

## Core Concepts

### Project Management
```bash
uv init my-project          # create a new project
uv init --lib my-lib        # create a library project
uv add requests             # add a dependency
uv add --dev pytest ruff    # add dev dependencies
uv remove requests          # remove a dependency
uv sync                     # install all deps from lockfile
uv lock                     # update uv.lock without installing
```

### Running Code
```bash
uv run python script.py     # run in project venv
uv run pytest               # run tool in project venv
uvx ruff check .            # run tool in isolated ephemeral env
uvx --from httpie http GET https://example.com
```

### Virtual Environments
```bash
uv venv                     # create .venv in current dir
uv venv --python 3.12       # with specific Python version
source .venv/bin/activate   # activate (or use uv run)
```

### Python Version Management
```bash
uv python install 3.12      # install a Python version
uv python list              # list available/installed versions
uv python pin 3.12          # pin version in .python-version
```

### Inline Script Dependencies (PEP 723)
```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "rich"]
# ///
import requests
from rich import print
```
```bash
uv run script.py            # uv auto-installs deps and runs
```

### pip Interface (drop-in replacement)
```bash
uv pip install requests     # replaces: pip install
uv pip install -r req.txt   # replaces: pip install -r
uv pip compile reqs.in      # replaces: pip-compile
uv pip sync reqs.txt        # replaces: pip-sync
```

### pyproject.toml Structure
```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["requests>=2.31"]

[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy"]

[tool.uv]
dev-dependencies = ["pytest", "ruff"]

[tool.uv.sources]
my-lib = { path = "../my-lib", editable = true }
```

## Best Practices

- Always commit `uv.lock` for applications; add it to `.gitignore` for libraries.
- Use `uv sync --frozen` in CI to ensure reproducible installs.
- Prefer `uv run <cmd>` over activating the venv manually.
- Use `uvx` for one-off tools (linters, formatters) to avoid polluting the project env.
- Use `uv add --optional dev` or `[tool.uv] dev-dependencies` for dev tools.
- Use `uv python pin` to lock the Python version per project.

## Common Workflows

### Setting up a new project
```bash
uv init my-app
cd my-app
uv add fastapi uvicorn
uv add --dev pytest ruff mypy
uv run python -m my_app
```

### CI/CD
```bash
uv sync --frozen --no-dev   # install prod deps only, no updates
uv run pytest               # run tests
```

### Migrating from pip/requirements.txt
```bash
uv init --no-readme
uv add $(cat requirements.txt | grep -v '#' | tr '\n' ' ')
uv lock
```

### Migrating from poetry
```bash
# uv can read pyproject.toml directly; run:
uv sync
# or recreate with:
uv init --no-workspace
uv add $(poetry export --without-hashes -f requirements.txt | cut -d';' -f1)
```

## Performance Notes

- uv is 10–100x faster than pip due to Rust implementation and parallel downloads.
- Global cache is shared across projects — re-installs are near-instant.
- `uv lock` uses a dependency resolver that produces fully deterministic lockfiles.
