---
name: setup-python-lib
description: Sets up a new Python library project using uv in the current directory. Creates project structure, installs dev dependencies, and optionally configures git remote. Use when the user wants to initialise a Python library, package, or project with uv.
user-invocable: true
allowed-tools: Bash, Write, AskUserQuestion
---

# Setting Up a Python Library with uv

## Overview

This skill scaffolds a Python library project using uv in the current working directory.

## Workflow

### Step 1: Gather Project Details

Ask the user for:
1. **Python version** - default to 3.12 if not specified
2. **Project description** (optional) - for pyproject.toml and README

### Step 2: Initialise the Project

Run from the current directory (user has already created and cd'd into it):

```bash
uv init --lib . --python <version>
```

### Step 3: Add Dev Dependencies

```bash
uv add --dev ipython jupyterlab ruff pytest pytest-cov
```

### Step 4: Create Project Structure

Create directories:

```bash
mkdir -p tests
mkdir -p nbs
mkdir -p scratch/scripts
mkdir -p scratch/nbs
touch tests/__init__.py
```

- `tests/` - test files
- `nbs/` - notebooks (tracked in git)
- `scratch/scripts/` - throwaway scripts (ignored)
- `scratch/nbs/` - throwaway notebooks (ignored)

Add `scratch/` to `.gitignore`:

```bash
echo "scratch/" >> .gitignore
```

Create a minimal test file `tests/test_placeholder.py`:

```python
def test_placeholder():
    """Placeholder test to verify pytest works."""
    assert True
```

### Step 5: Create README.md

Create a minimal README using the directory name as the project name:

```markdown
# <directory-name>

<description if provided>
```

### Step 6: Create CLAUDE.md

Create a `CLAUDE.md` with project context:

```markdown
# <project-name>

Python library using uv for dependency management.

## Commands

Run `just` to see available commands (test, lint, format, shell, jupyter).

## Project Structure

- `src/<package>/` - library source code
- `tests/` - test files
- `nbs/` - notebooks (tracked)
- `scratch/` - throwaway scripts and notebooks (gitignored)

## Dependencies

- Add runtime deps: `uv add <package>`
- Add dev deps: `uv add --dev <package>`
- Run anything: `uv run <command>`
```

### Step 7: Create justfile

Create a `justfile` with common development commands:

```just
# List available commands
default:
    @just --list

# Run tests
test *args:
    uv run pytest {{args}}

# Run tests with coverage
test-cov:
    uv run pytest --cov

# Format code
fmt:
    uv run ruff format .

# Lint code
lint:
    uv run ruff check .

# Lint and fix
lint-fix:
    uv run ruff check . --fix

# Format and lint
check: fmt lint

# Start IPython shell with autoreload
shell:
    uv run ipython -i -c "get_ipython().run_line_magic('load_ext', 'autoreload'); get_ipython().run_line_magic('autoreload', '2')"

# Start Jupyter Lab
jupyter:
    uv run jupyter lab
```

### Step 8: Git Repository Setup

**First, discover available GitHub organisations:**

```bash
gh org list
```

Then ask the user using AskUserQuestion with these options:

1. **No remote** - Keep it local only
2. **Public repository (personal)** - Create public repo in personal account
3. **Private repository (personal)** - Create private repo in personal account
4. **Organisation repository** - Show list of orgs from `gh org list` and let user pick, then ask public/private

**If user selects organisation**, present the orgs discovered and ask which one, then ask public or private.

**Creating the repository:**

For personal repos:
```bash
gh repo create <repo-name> --public|--private --source . --push
```

For organisation repos:
```bash
gh repo create <org-name>/<repo-name> --public|--private --source . --push
```

If no remote wanted:
```bash
git init
git add .
git commit -m "Initial commit: scaffold Python library with uv"
```

## Checklist

- [ ] Confirm Python version (default 3.12)
- [ ] Get optional project description
- [ ] Run `uv init --lib .`
- [ ] Add dev dependencies (ipython, jupyterlab, ruff, pytest, pytest-cov)
- [ ] Create directories (tests/, nbs/, scratch/scripts/, scratch/nbs/)
- [ ] Add scratch/ to .gitignore
- [ ] Create placeholder test
- [ ] Create README.md
- [ ] Create CLAUDE.md
- [ ] Create justfile with dev commands
- [ ] Fetch available GitHub orgs with `gh org list`
- [ ] Ask about git remote setup
- [ ] Initialise git and optionally create remote

## Notes

- Always use `uv init --lib .` for library projects (creates proper src layout)
- The project name is derived from the current directory name
- Verify uv and gh are installed before starting
- Use `gh auth status` to check GitHub authentication if needed
