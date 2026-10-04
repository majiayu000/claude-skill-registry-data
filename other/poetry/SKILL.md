---
name: poetry
description: Manage Python dependencies, lock files, and project environments using Poetry.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: python
  audience: developers
  workflow: automation
  since: "2026-02-25"
---

## What I do

I handle the full Poetry dependency-management lifecycle:

- **Add or remove packages** — update `pyproject.toml` and `poetry.lock` in one step
- **Sync the environment** — install exactly what the lock file specifies
- **Regenerate the lock file** — after you edit `pyproject.toml`, safely re-resolve without unintended upgrades
- **Run commands in the project environment** — no manual venv activation needed
- **Initialise a new project** — scaffold a new Poetry-managed project or migrate from pip/requirements.txt

## When to use me

- Use this skill when the project is Poetry-managed (for example, `poetry.lock` exists, or the team standard is Poetry).
- You want to add, update, or remove a dependency
- You pulled a branch and need the environment to match the updated lock file
- You edited `pyproject.toml` directly and need the lock file regenerated
- You want to run a script, test suite, or tool inside the project's virtual environment
- You are starting a new Python project with Poetry, or migrating from pip/requirements.txt

## Use Instead [if available]

- Use `uv` when the project is uv-managed (for example, `uv.lock` is the lockfile of record).
- Use `ci-fix` when your primary goal is diagnosing/remediating a failing CI run instead of general dependency work.

## Example usage

```
/poetry add requests
/poetry add --dev pytest
/poetry remove httpx
/poetry install
/poetry lock
/poetry run pytest
/poetry init
```

---

## Workflow

### Adding and removing dependencies

**Add a runtime dependency** (goes into `[tool.poetry.dependencies]` in `pyproject.toml`):

```bash
poetry add <package>           # e.g. poetry add requests
poetry add "<package>>=2.0"    # with version constraint
```

**Add a dev dependency** (goes into `[tool.poetry.group.dev.dependencies]` — Poetry 1.2+ group syntax):

```bash
poetry add --group dev <package>    # e.g. poetry add --group dev pytest ruff
```

Dev dependencies are installed in the development environment only and excluded from production installs (`poetry install --no-dev` or `poetry install --without dev`). Use `--group dev` for test runners, linters, and formatters.

**Remove a dependency**:

```bash
poetry remove <package>        # removes from pyproject.toml and updates poetry.lock
poetry remove --group dev <package>    # remove a dev dependency
```

After every `add` or `remove`, Poetry automatically:
1. Updates `pyproject.toml`
2. Resolves all constraints and regenerates `poetry.lock`
3. Installs or uninstalls the package in the active virtual environment

**Version resolution summary**: Poetry prints the resolved version and any transitive changes. If a conflict is detected, it reports the conflicting constraints — fix the version bounds in `pyproject.toml` and retry.

---

### Syncing the environment

`poetry install` installs **exactly** what `poetry.lock` specifies — no more, no less. It is the canonical way to bring an environment into alignment with the lock file.

```bash
poetry install
```

**When to use it:**

- After `git pull` when teammates updated `poetry.lock`
- After checking out a branch with different lock file state
- After cloning a repository for the first time
- After manually editing `pyproject.toml` followed by `poetry lock`

**Already in sync**: If the environment already matches the lock file, `poetry install` exits cleanly. It is safe to run on every `git pull`.

**Dev vs production install**:

```bash
poetry install --without dev    # skip dev dependency groups (production-like)
poetry install --only dev       # install only dev dependencies
```

---

### Regenerating the lock file

Use `poetry lock` after editing `pyproject.toml` directly — for example, changing a version constraint, adding a dependency entry by hand, or removing one.

**Version-aware safe regeneration**:

| Poetry version | Safe command | Notes |
|---|---|---|
| **2.x** (current) | `poetry lock` | Safe by default — existing resolved versions preserved; `--no-update` flag removed |
| **1.x** (legacy) | `poetry lock --no-update` | Required to prevent upgrading all deps; plain `poetry lock` in 1.x upgrades everything |

Check your Poetry version: `poetry --version`

**Detect which command to use**:

```bash
# Poetry 2.x — safe by default:
poetry lock

# Poetry 1.x — must pass --no-update for safe regen:
poetry lock --no-update
```

If `--no-update` is not recognised (Poetry 2.x), use plain `poetry lock`.

**Upgrade all dependencies to latest compatible versions**:

```bash
# Poetry 2.x:
poetry update --lock          # regenerate lock with all deps upgraded (no env install)
# or:
poetry lock --regenerate      # full re-resolution from scratch

# Poetry 1.x:
poetry update                 # upgrades and installs
```

**Upgrade a single package**:

```bash
poetry update <package>       # upgrade one package (both versions)
```

**When to use each variant:**

| Scenario | Poetry 2.x | Poetry 1.x |
|---|---|---|
| Edited constraint in `pyproject.toml` | `poetry lock` | `poetry lock --no-update` |
| Removed a dependency | `poetry lock` | `poetry lock --no-update` |
| Upgrade one package | `poetry update <pkg>` | `poetry update <pkg>` |
| Periodic refresh of all deps | `poetry update --lock` | `poetry update` |

After regenerating the lock file, run `poetry install` to apply the changes to your environment.

**Critical**: The skill will never run a command that silently upgrades unrelated packages. Always use the safe-default command for your Poetry version.

---

### Running commands in the project environment

`poetry run` executes any command inside the project's virtual environment — without manual activation.

```bash
poetry run <command>
```

**Examples:**

```bash
poetry run pytest                      # run tests
poetry run pytest tests/unit/ -v      # with arguments
poetry run python src/main.py         # run a script
poetry run ruff check .               # run a tool
poetry run python -m mypackage        # module invocation
```

**Replaces manual venv activation**: Use `poetry run <cmd>` instead of:
```bash
source $(poetry env info --path)/bin/activate
```

`poetry run` works consistently across platforms and CI environments without shell state side-effects.

**Tip**: To open a shell inside the venv: `poetry shell` (Poetry 1.x) or `poetry run bash` (Poetry 2.x removed `poetry shell` in favour of explicit activation).

---

### Initialising a new project

**Scaffold a new Poetry project** (creates a directory with `pyproject.toml` and src layout):

```bash
poetry new my-project
```

**Initialise in an existing directory** (interactive `pyproject.toml` wizard):

```bash
poetry init
```

This prompts for project name, version, description, Python version constraint, and initial dependencies.

**Set Python version**:

```bash
poetry env use python3.12     # pin to a specific Python for this project
```

Poetry stores the selected Python in the virtualenv metadata.

**Migrate from `requirements.txt`**:

1. Run `poetry init` if no `pyproject.toml` exists
2. Add runtime dependencies:
   ```bash
   # Add each dependency from requirements.txt:
   poetry add requests click flask
   # Or read from file:
   cat requirements.txt | xargs poetry add
   ```
3. Add dev dependencies:
   ```bash
   poetry add --group dev pytest ruff mypy
   ```
4. Verify the generated `poetry.lock` is correct: `poetry install`
5. Delete `requirements.txt` once migration is verified

---

## Tips for Success

1. **Always use `poetry run` instead of venv activation** — it works in CI without any setup steps and eliminates the risk of running commands in the wrong environment.

2. **`poetry lock` is safe by default in Poetry 2.x** — but in Poetry 1.x you must use `poetry lock --no-update` to avoid upgrading unrelated packages. Check `poetry --version` if you're unsure.

3. **Always review the lock diff after `poetry update`** — `poetry update` can pull in breaking changes. Check `git diff poetry.lock` before committing and run your test suite.

4. **Use `--group dev` for test and lint tools** — keeping pytest, ruff, mypy, and similar tools in the `dev` group ensures they are never installed in production (`poetry install --without dev`).

5. **Run `poetry install` after every `git pull`** — or make it the first step in your dev environment setup script. This ensures your environment always matches the committed lock file.

6. **Check Poetry is installed**: `poetry --version`. Install with `curl -sSL https://install.python-poetry.org | python3 -` or `brew install poetry`.

7. **Commit `poetry.lock` to version control** — the lock file is the source of truth for reproducible environments. Never add it to `.gitignore`.
