---
name: uv
description: Python package manager and project tooling using uv. Use when working with Python projects, managing dependencies, creating virtual environments, running Python scripts, configuring workspaces/monorepos, or troubleshooting uv issues. Triggers on pyproject.toml projects, uv commands, pip replacement workflows, Python version management, workspace configuration, or CI/CD Python setup.
---

# uv Field Manual

*Assumption: `uv` is already installed and available on `PATH`.*

## Sanity Check

```bash
uv --version               # verify installation; exits 0
```

If the command fails, halt and report to the user.

## Project ("cargo-style") Flow

```bash
uv init myproj                     # create pyproject.toml + .venv
cd myproj
uv add ruff pytest httpx           # fast resolver + lock update
uv run pytest -q                   # run tests in project venv
uv lock                            # refresh uv.lock (if needed)
uv sync --locked                   # reproducible install (CI-safe)
```

## Workspaces (Monorepo)

Workspaces organize large codebases by splitting them into multiple packages with shared dependencies and a single lockfile.

**Workspace root pyproject.toml:**
```toml
[project]
name = "myapp"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["shared-lib", "requests"]

[tool.uv.sources]
shared-lib = { workspace = true }    # resolve from workspace

[tool.uv.workspace]
members = ["packages/*"]             # glob patterns supported
exclude = ["packages/experimental"]  # optional exclusions
```

**Workspace member (packages/shared-lib/pyproject.toml):**
```toml
[project]
name = "shared-lib"
version = "0.1.0"
dependencies = ["pydantic"]
```

**Key commands:**
```bash
uv init mylib --package             # add new member to existing workspace
uv lock                             # locks entire workspace
uv sync                             # syncs workspace root by default
uv run --package shared-lib pytest  # run in specific member
uv sync --all-packages              # sync all members into .venv
uv sync --no-install-workspace      # deps only (good for Docker layers)
```

**Behaviors:**
- `uv lock` operates on entire workspace
- `uv run`/`uv sync` default to workspace root; use `--package` for members
- Root `tool.uv.sources` apply to all members unless overridden
- Member dependencies are always editable

## Script-Centric Flow (PEP 723)

```bash
uv run hello.py                    # zero-dep script, auto-env
uv add --script hello.py rich      # embeds dep metadata
uv run --with rich hello.py        # transient deps, no state
```

## CLI Tools (pipx Replacement)

```bash
uvx ruff check .                   # ephemeral run
uv tool install ruff               # user-wide persistent install
uv tool list                       # audit installed CLIs
uv tool update --all               # keep them fresh
```

## Python Version Management

```bash
uv python install 3.10 3.11 3.12
uv python pin 3.12                 # writes .python-version
uv run --python 3.10 script.py
```

## Legacy Pip Interface

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
uv pip sync -r requirements.txt    # deterministic install
```

## Performance Tuning

| Env Var                   | Purpose                 | Typical Value |
| ------------------------- | ----------------------- | ------------- |
| `UV_CONCURRENT_DOWNLOADS` | saturate fat pipes      | `16` or `32`  |
| `UV_CONCURRENT_INSTALLS`  | parallel wheel installs | `CPU_CORES`   |
| `UV_OFFLINE`              | enforce cache-only mode | `1`           |
| `UV_INDEX_URL`            | internal mirror         | `https://…`   |
| `UV_PYTHON`               | pin interpreter in CI   | `3.11`        |

```bash
uv cache dir && uv cache info      # show path + stats
uv cache clean                     # wipe wheels & sources
```

## Migration Matrix

| Legacy Tool         | uv Replacement              |
| ------------------- | --------------------------- |
| `python -m venv`    | `uv venv`                   |
| `pip install`       | `uv pip install`            |
| `pip-tools compile` | `uv lock`                   |
| `pipx run`          | `uvx` / `uv tool run`       |
| `poetry add`        | `uv add`                    |
| `pyenv install`     | `uv python install`         |

## Troubleshooting

| Symptom                    | Resolution                                                     |
| -------------------------- | -------------------------------------------------------------- |
| `Python X.Y not found`     | `uv python install X.Y` or set `UV_PYTHON`                     |
| Proxy throttling downloads | `UV_HTTP_TIMEOUT=120 UV_INDEX_URL=https://mirror.local/simple` |
| C-extension build errors   | `unset UV_NO_BUILD_ISOLATION`                                  |
| Need fresh env             | `uv cache clean && rm -rf .venv && uv sync`                    |
| Still stuck?               | `RUST_LOG=debug uv ...` and open a GitHub issue                |
