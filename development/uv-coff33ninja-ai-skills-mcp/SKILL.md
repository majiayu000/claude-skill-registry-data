---
name: uv
description: Use when installing Python tooling, managing Python environments, running Python scripts, or managing Python dependencies. Use command `uv` for all Python operations instead of `pip` or `python -m venv`.
---

# uv — Python Package Manager

uv is an extremely fast Python package and project manager, replacing pip, pip-tools, pipx, poetry, pyenv, and virtualenv.

## Installation (Windows)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Installs to `~/.local\bin\` (add this to PATH: `$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"`).

## Core Commands

| Command | What it does |
|---|---|
| `uv init` | Create a new Python project with `pyproject.toml` |
| `uv add <pkg>` | Add dependency to the project |
| `uv remove <pkg>` | Remove dependency from the project |
| `uv sync` | Sync environment with lockfile (like `pip install -r requirements.txt`) |
| `uv lock` | Update `uv.lock` without syncing |
| `uv run <script>` | Run a script or command in the project's environment |
| `uv venv` | Create a virtual environment in `./.venv` |
| `uv pip install <pkg>` | Pip-compatible install (for workflows not yet migrated) |
| `uv tool install <pkg>` | Install a CLI tool (replaces `pipx`) |
| `uv tool run <pkg>` | Run a tool once without installing (replaces `pipx run`) |
| `uv python install <ver>` | Download and manage Python versions (replaces `pyenv`) |
| `uv cache clean` | Clear the cache |
| `uv build` | Build source dist and wheel |
| `uv publish` | Upload to PyPI |
| `uv format` | Format Python code (uses Ruff) |
| `uv check` | Run linter checks (uses Ruff) |

## Project Workflow

```powershell
uv init my-project
cd my-project
uv add requests
uv add --dev pytest
uv sync
uv run python -c "import requests; print('ok')"
```

## Key Flags

- `--dev` — add as dev dependency
- `--group <name>` — add to a specific optional dependency group
- `-n, --no-cache` — avoid reading/writing cache
- `--offline` — no network access
- `--directory <dir>` — run as if in that directory
- `--project <path>` — scope to a specific project

## Bundled Script

A bundled script at `scripts/ensure-uv.ps1` (PowerShell) detects and installs uv:

```powershell
.\scripts\ensure-uv.ps1                          # detect only
.\scripts\ensure-uv.ps1 -InstallMissing          # install uv if missing
.\scripts\ensure-uv.ps1 -InstallMissing -ManagedPython -PythonVersion 3.12  # install uv + managed Python
.\scripts\ensure-uv.ps1 -DryRun                  # preview without changes
```

To use as a project-local tool:

```powershell
cp <skill-path>/uv/scripts/ensure-uv.ps1 .ai_scripts/
.ai_scripts\ensure-uv.ps1 -InstallMissing
```

## Environment Variables

| Variable | Purpose |
|---|---|
| `UV_CACHE_DIR` | Cache location (redirect off C: to save space) |
| `UV_PYTHON_INSTALL_DIR` | Where uv-managed Python versions live |
| `UV_MANAGED_PYTHON` | Force use of uv-managed Python (`--managed-python`) |
| `UV_NO_PYTHON_DOWNLOADS` | Disable auto-download of Python (`--no-python-downloads`) |
| `UV_OFFLINE` | Disable network (`--offline`) |

## Cross-references

- **anti-global-install** — uv is the preferred alternative to global pip installs; all Python operations should use `uv add`/`uv sync` instead of `pip install`.
- **portable-self-contained** — uv projects keep `.venv/` in the project root; cache can be redirected off C: via `UV_CACHE_DIR`.
- **project-scripts** — The ensure-uv.ps1 script is a project install script that project-scripts would discover and catalog.
- **toolchain-fallback** — uv can install and manage Python versions as a fallback toolchain.
