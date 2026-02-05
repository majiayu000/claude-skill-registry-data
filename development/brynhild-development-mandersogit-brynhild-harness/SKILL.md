---
name: brynhild-development
description: Guidelines for contributing to brynhild itself - use when making changes to the brynhild codebase, running tests, or understanding project conventions
---

# Brynhild Development

This is a **project-local skill** demonstrating how to create skills specific to a project. It provides guidance for contributing to brynhild.

## Project Structure

```
brynhild/
├── src/brynhild/          # Main package
│   ├── api/               # LLM provider implementations
│   ├── cli/               # Command-line interface
│   ├── config/            # Settings and configuration
│   ├── core/              # Core conversation logic
│   ├── hooks/             # Hook system
│   ├── builtin_skills/    # Skills shipped with package
│   ├── plugins/           # Plugin system
│   ├── profiles/          # Model profiles
│   ├── session/           # Session management
│   ├── skills/            # Skill discovery and loading
│   ├── tools/             # Tool implementations
│   └── ui/                # TUI application
├── tests/                 # Test suite
├── scripts/               # Development scripts
├── workflow/              # Development documentation
└── .brynhild/skills/      # Project-local skills (like this one)
```

## Python Environment

**Always use the project venv:**

```bash
./local.venv/bin/python script.py
./local.venv/bin/pip install package
```

**Never use system Python or bare `python3`.**

## Running Tests

```bash
# All tests
make tests

# Specific test file
./local.venv/bin/python -m pytest tests/path/test_file.py -v

# Specific test
./local.venv/bin/python -m pytest tests/path/test_file.py::test_name -v
```

## Type Checking

```bash
# mypy (primary)
make typecheck

# pyright (alternative)
make typecheck-pyright
```

## Linting

```bash
make lint
```

Uses `ruff` for linting. Auto-fix with:

```bash
./local.venv/bin/python -m ruff check --fix src/ tests/
```

## Import Style

**Qualified imports only. Never import symbols directly.**

```python
# ✅ CORRECT
import pathlib as _pathlib
import typing as _typing
import brynhild.config as config

# ❌ WRONG
from pathlib import Path
from brynhild.config import Settings
```

**External imports:** underscore prefix (`_pathlib`, `_click`)
**Internal imports:** no underscore (`config`, `session`)

## Git Commits

**Never make autonomous commits.** Use the `commit-helper` skill to create commit plans, then wait for user authorization to execute.

## Testing Policy

- All tests must be honest (no mocking away the behavior being tested)
- No trivial tests (must verify meaningful behavior)
- No hacky workarounds; use `# noqa` for intentional lint ignores

## This Skill is an Example

This skill demonstrates:
- Project-local skills in `.brynhild/skills/`
- Overriding or extending builtin skills
- Project-specific conventions and guidelines

Users of brynhild can create similar skills for their own projects.

