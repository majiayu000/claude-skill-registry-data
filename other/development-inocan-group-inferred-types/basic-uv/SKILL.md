---
name: basic_uv
description: Use when running or explaining uv or ty commands, managing dependencies/lockfiles/virtualenvs, or running Python in this repo.
---

# Basic uv / ty

## Overview

Use uv as the project package manager and runner; use ty for type checks. Provide command-first guidance and state what each command changes (pyproject.toml, uv.lock, or the virtual environment).

## Workflow

- Detect uv project state by checking for `pyproject.toml` and `uv.lock`.
- Sync before running tools when accuracy matters: `uv sync`.
- Run tools through uv to ensure the project environment is used: `uv run <cmd>`.
- Prefer `uv run python <script_or_module>` over plain `python` when coding or executing Python in this repo.
- Call out side effects explicitly: `uv add/remove` update `pyproject.toml` and `uv.lock`; `uv sync` changes the environment.

## Common uv Commands

- Initialize a project: `uv init`
- Add deps: `uv add <pkg>`; dev deps: `uv add --dev <pkg>`; group deps: `uv add --group <group> <pkg>`
- Remove deps: `uv remove <pkg>`
- Lock deps: `uv lock` (update `uv.lock`); `uv lock --check` (CI check); `uv lock --upgrade` (allow upgrades)
- Sync env: `uv sync`; `uv sync --frozen` (do not update `uv.lock`); `uv sync --group <group>` (include group)
- Run commands: `uv run <cmd>`; `uv run --no-sync <cmd>` (skip sync); `uv run --group <group> <cmd>`
- Inspect deps: `uv tree`
- Export lockfile: `uv export`
- Manage Python installs: `uv python list|install|find|pin`
- Tool runner: `uv tool run <pkg> <cmd>`; install: `uv tool install <pkg>`
- pip-compat mode: `uv pip install|compile|sync|list|freeze|check`

## Common ty Commands

- Type check: `uv run ty check [PATHS]`
- Watch mode: `uv run ty check --watch`
- Config override: `uv run ty check --config KEY=VALUE`
- Config file: `uv run ty check --config-file path/to/ty.toml`
- Exclude paths: `uv run ty check --exclude 'pattern'`
- Target Python: `uv run ty check --python-version 3.12`
- Specify env: `uv run ty check --python path/to/python`
- LSP server: `uv run ty server`
- Shell completion: `ty generate-shell-completion <SHELL>`

## Project Reference

- If the repo provides a local cheat sheet, consult it for project-specific conventions: `docs/ty-uv-commands.md`.
