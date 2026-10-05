---




name: poetry
description: Manages Python project dependencies, virtual environments, building,
  and publishing using Poetry — covering dependency resolution, lockfiles, workspaces,
  plugin system, and migration from pip.
license: MIT
compatibility: opencode
metadata:
  version: "1.0.0"
  domain: coding
  triggers: poetry, python package manager, pyproject.toml, poetry lock, virtual environment, dependency management, Python publishing, PyPI upload dependency management
  archetypes:
  - tactical
  - generation
  anti_triggers:
  - brainstorming
  - vague ideation
  - code golf
  - over-engineering
  response_profile:
    verbosity: low
    directive_strength: high
    abstraction_level: operational
  role: implementation
  scope: implementation
  output-format: code
  content-types:
  - code
  - guidance
  - examples
  - do-dont
  - config
  related-skills: coding-python-uv, coding-package-ecosystem-navigator, coding-dependency-supply-chain-security




---




# Poetry — Python Package & Dependency Manager

Manages Python project dependencies, virtual environments, building, and publishing using Poetry. Covers dependency resolution strategies, lockfile management, workspace/multirepo setup, plugin architecture, and migration from pip/requirements.txt workflows.

## TL;DR Checklist

- [ ] Use `pyproject.toml` with `[tool.poetry]` section — no `setup.py`, no `requirements.txt`
- [ ] Always commit `poetry.lock` for reproducible builds in production and CI
- [ ] Use `poetry add <pkg>` to install dependencies (never pip install directly in Poetry-managed venvs)
- [ ] Pin Python version with `requires-python` in pyproject.toml
- [ ] Use named dependency groups (`group.dev.dependencies`) for dev-only packages
- [ ] Use `poetry run` or `poetry shell` to execute commands within the virtual environment
- [ ] Run `poetry lock --no-update` after manual pyproject.toml edits (never edit poetry.lock manually)

---

## When to Use

Use this skill when:

- Setting up a new Python project with structured dependency management and virtual environment isolation
- Managing complex dependency trees with version constraints across multiple packages
- Building and publishing Python packages to PyPI or private registries
- Configuring Poetry workspaces for monorepo or multi-package projects
- Migrating an existing pip/requirements.txt project to Poetry's pyproject.toml workflow
- Resolving dependency conflicts between packages with overlapping version requirements

## When NOT to Use

Avoid this skill for:

- Simple one-off scripts where a virtualenv + pip is sufficient overhead — use `python -m venv` instead
- Projects that already use `uv` or `pip-tools` and have no migration pressure — don't swap tools mid-project
- Python environments managed externally (Docker containers, system packages, conda) — Poetry's venv integration conflicts with these

---

## Core Workflow

### Phase 1: Project Initialization

1. **Create the project structure** — Run `poetry init` interactively or use `poetry new <package-name>` for a library with src/ layout. The init command creates pyproject.toml, README.md, and optionally a tests directory.
   **Checkpoint:** Verify pyproject.toml contains `[tool.poetry]`, valid name, version, Python version constraint (e.g., `requires-python = "^3.10"`), and at least one dependency or group.

2. **Configure the build backend** — Poetry uses setuptools by default but supports hatchling, flit, or pdm-backend as alternatives. Set the backend explicitly in pyproject.toml:
   ```toml
   [build-system]
   requires = ["setuptools>=61.0", "wheel"]
   build-backend = "setuptools.build_meta"

   # Or for hatchling (recommended for new projects):
   # requires = ["hatchling"]
   # build-backend = "hatchling.build"
   ```

### Phase 2: Dependency Management

3. **Add production dependencies** — Use `poetry add <package>` or `poetry add <package>@<version-spec>`. Poetry resolves the full dependency tree, picks compatible versions, and writes to both pyproject.toml and poetry.lock.
   ```bash
   # Add latest compatible version
   poetry add httpx

   # Pin to major version only
   poetry add "requests>=2.28,<3"

   # Add with extras (e.g., psycopg2 binary)
   poetry add "psycopg2-binary"

   # Add from a specific git repository
   poetry add "my-lib @ git+https://github.com/user/my-lib.git@main"

   # Add from a local path dependency
   poetry add "../shared-utils"
   ```

4. **Configure dependency groups for non-production dependencies** — Poetry supports named dependency groups (introduced in 1.2) to separate dev, test, docs, and optional features:
   ```toml
   [tool.poetry]
   name = "my-project"
   version = "0.1.0"
   requires-python = ">=3.10,<4.0"

   [tool.poetry.dependencies]
   python = "^3.10"
   httpx = "^0.27"
   pydantic = "^2.5"
   sqlalchemy = "^2.0"

   [tool.poetry.group.dev.dependencies]
   pytest = "^8.0"
   pytest-asyncio = "^0.23"
   ruff = "^0.4"
   mypy = "^1.8"
   ipython = "^8.0"

   [tool.poetry.group.test.dependencies]
   pytest-cov = "^5.0"
   hypothesis = "^6.90"

   [tool.poetry.group.docs.dependencies]
   mkdocs = "^1.5"
   mkdocstrings = {extras = ["python"], version = "^0.25"}

   # Optional dependencies (installable via extras)
   [tool.poetry.extras]
   database = ["sqlalchemy", "alembic"]
   async = ["httpx", "aiosqlite"]
   ```

5. **Install dependencies** — `poetry install` installs all dependencies defined in pyproject.toml into the virtual environment and ensures poetry.lock is up to date. Use flags for selective installation:
   ```bash
   # Install everything (default — production + all groups)
   poetry install

   # Production only, skip all dependency groups
   poetry install --only main

   # Dev group only
   poetry install --only dev

   # Specific groups
   poetry install --with dev,test

   # Sync to match lockfile exactly (removes packages not in lock)
   poetry lock && poetry install
   ```

### Phase 3: Development Workflow

6. **Execute commands within the virtual environment** — Poetry provides three mechanisms: `poetry run` for one-off execution, `poetry shell` for an interactive subshell, or `poetry env use` to select a specific Python interpreter.
   ```bash
   # Run a single command in the project's venv
   poetry run pytest tests/
   poetry run ruff check .
   poetry run mypy src/

   # Enter an interactive shell with the venv activated
   poetry shell
   (my-project-xyz) $ pytest tests/
   (my-project-xyz) $ exit

   # Run a script defined in [tool.poetry.scripts]
   poetry run my-cli --help
   ```

7. **Configure project scripts** — Define CLI entry points and convenience scripts in pyproject.toml:
   ```toml
   [tool.poetry.scripts]
   my-cli = "my_project.cli:main"
   migrate-db = "my_project.db:migrate"

   # Development convenience scripts (run via poetry run <name>)
   [tool.poetry.group.dev.scripts]
   test = "pytest tests/ --cov=src --cov-report=term-missing"
   lint = ["ruff", "check", "."]
   typecheck = "mypy src/"
   docs-serve = "mkdocs serve"
   ```

### Phase 4: Workspace (Monorepo) Setup

8. **Configure Poetry workspaces for multi-package projects** — Poetry 1.2+ supports workspaces natively. Define a root pyproject.toml that declares member packages:
   ```toml
   [tool.poetry]
   name = "my-workspace"
   version = "0.1.0"
   requires-python = ">=3.10"

   [tool.poetry.dependencies]
   python = "^3.10"

   [tool.poetry.workspaces]
   members = ["packages/*"]
   ```

   Each member package has its own pyproject.toml with its own dependencies:
   ```toml
   # packages/core/pyproject.toml
   [tool.poetry]
   name = "my-core"
   version = "0.1.0"
   requires-python = "^3.10"

   [tool.poetry.dependencies]
   python = "^3.10"
   pydantic = "^2.5"

   # packages/api/pyproject.toml
   [tool.poetry]
   name = "my-api"
   version = "0.1.0"
   requires-python = "^3.10"

   [tool.poetry.dependencies]
   python = "^3.10"
   httpx = "^0.27"
   my-core = { path = "../core", develop = true }
   ```

   **Checkpoint:** Run `poetry install` from the workspace root — it must resolve all member packages and create a unified lockfile with no dependency conflicts between workspaces.

### Phase 5: Building and Publishing

9. **Build distribution packages** — Generate wheel and/or sdist artifacts:
   ```bash
   # Build both wheel and source distribution
   poetry build

   # Output in dist/ directory
   # dist/my_project-0.1.0-py3-none-any.whl
   # dist/my_project-0.1.0.tar.gz

   # Build only wheel (faster, no source)
   poetry build --wheel

   # Build only source distribution
   poetry build --sdist
   ```

10. **Publish to PyPI or private registry** — Configure repository credentials and publish:
    ```bash
    # Publish to PyPI (requires PYPI_TOKEN env var or interactive login)
    poetry publish

    # Dry-run to validate before publishing
    poetry build && twine check dist/*

    # Publish to a custom/private repository
    poetry config repositories.my-registry https://pypi.internal.company.com/simple/
    poetry config http-basic.my-registry $USERNAME $PASSWORD
    poetry publish -r my-registry

    # Or use the upload command directly
    poetry upload -r my-registry
    ```

---

## Implementation Patterns

### Pattern 1: Complete pyproject.toml for a Production API Service

```toml
[tool.poetry]
name = "user-service"
version = "1.2.0"
description = "REST API service for user management with async database access"
authors = ["Engineering Team <eng@company.com>"]
readme = "README.md"
license = "MIT"
packages = [{ include = "user_service", from = "src" }]

[tool.poetry.dependencies]
python = "^3.11"
httpx = {version = "^0.27", extras = ["brotli"]}
pydantic = {version = "^2.5", extras = ["dotenv"]}
sqlalchemy = "^2.0"
alembic = "^1.13"
structlog = "^24.1"
prometheus-client = "^0.20"
asyncpg = {version = "^0.29", optional = true}

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-asyncio = "^0.23"
pytest-cov = "^5.0"
hypothesis = "^6.90"
ruff = "^0.4"
mypy = "^1.8"
types-requests = "^2.31"

[tool.poetry.group.lint.dependencies]
ruff = "^0.4"
mypy = "^1.8"
pre-commit = "^3.5"

[tool.poetry.scripts]
user-service = "user_service.cli:main"
db-migrate = "user_service.db:migrate"

[tool.poetry.extras]
postgresql = ["asyncpg"]

[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "RUF", "D"]
ignore = ["D100", "D104"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
filterwarnings = [
    "error::DeprecationWarning",
    "error::PendingDeprecationWarning",
]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

### Pattern 2: Dependency Resolution Strategies (BAD vs. GOOD)

```toml
# ❌ BAD — Too loose version constraints lead to non-reproducible builds
[tool.poetry.dependencies]
python = "^3.8"
requests = "*"          # Wildcard! Could pull anything including breaking changes
flask = ">=1.0"         # No upper bound — could break with any future release

# ✅ GOOD — Semantic versioning constraints balance safety and flexibility
[tool.poetry.dependencies]
python = "^3.11"        # >=3.11, <4.0 (compatible release)
httpx = ">=0.27,<1.0"   # Allow minor/patch updates within major version
pydantic = "^2.5"       # >=2.5, <3.0 — stable API guarantees within major version
sqlalchemy = "~2.0.23"  # >=2.0.23, <2.1.0 — patch-level stability for critical dep

# ❌ BAD — Conflicting constraints between groups
[tool.poetry.group.api.dependencies]
httpx = "^0.25"         # Locks to older minor version

[tool.poetry.group.test.dependencies]
pytest-httpx = "^0.28"  # Depends on httpx >=0.28 — conflict!

# ✅ GOOD — Aligned version constraints across all groups
[tool.poetry.dependencies]
httpx = "^0.27"         # Shared minimum across all groups

[tool.poetry.group.api.dependencies]
# Inherits httpx from main, no re-pinning needed

[tool.poetry.group.test.dependencies]
pytest-httpx = "^0.28"  # Compatible with httpx ^0.27
```

### Pattern 3: Poetry Plugin for Custom Build Hooks

Poetry's plugin system lets you inject custom behavior into the build and publish lifecycle. A common use case is running pre-publish validation or adding post-install hooks:

```python
# poetry_plugin.py — Register as a Poetry plugin via entry_points in your pyproject.toml
from poetry.plugins.application_plugin import ApplicationPlugin
from cleo.events.console_events import COMMAND, POST_COMMAND


class ValidationPlugin(ApplicationPlugin):
    """Run dependency and config validation before every command."""

    def activate(self, app):
        """Register event listeners when the plugin loads."""
        app.command_dispatchers[COMMAND].listen(self.on_command)
        app.command_dispatchers[POST_COMMAND].listen(self.on_post_command)

    def on_command(self, event, name, dispatcher=None):
        """Run before any Poetry command executes."""
        import os
        from pathlib import Path

        lock_path = Path("poetry.lock")
        project_path = Path("pyproject.toml")

        if (
            lock_path.exists()
            and project_path.exists()
            and lock_path.stat().st_mtime < project_path.stat().st_mtime
        ):
            print(
                "\033[91mWarning: pyproject.toml was modified more recently than poetry.lock. "
                "Run 'poetry lock' to update.\033[0m"
            )

    def on_post_command(self, event, name, dispatcher=None):
        """Run after every Poetry command completes."""
        # Auto-regenerate documentation if docs dependencies changed
        print("\033[94mDocumentation sources may have changed — consider 'poetry run mkdocs build'\033[0m")
```

Register the plugin via entry points in pyproject.toml:
```toml
[tool.poetry.plugins."poetry.application.plugin"]
validation = "poetry_plugin.ValidationPlugin"
```

### Pattern 4: Migration from pip/requirements.txt to Poetry

```bash
# Step 1: Generate an initial poetry.lock from requirements.txt
poetry import requirements requirements.txt

# Step 2: This creates pyproject.toml with dependencies extracted from requirements.txt
# Review the generated file and adjust version constraints

# Step 3: Resolve the full dependency tree
poetry lock

# Step 4: Install everything into a fresh virtual environment
poetry install

# Step 5: Verify functionality — run your test suite
poetry run pytest -x --tb=short

# Step 6: If tests pass, remove requirements.txt (Poetry manages deps via pyproject.toml + lockfile)
rm requirements.txt requirements-dev.txt

# Step 7: Update CI/CD to use poetry install instead of pip install -r requirements.txt
```

---

## Constraints

### MUST DO
- Commit `poetry.lock` to version control for deterministic, reproducible builds — never skip this
- Pin `requires-python` to a specific minimum version in pyproject.toml (e.g., `"^3.10"`)
- Use semantic version constraints (`^`, `~`) rather than wildcards (`*`) or exact pins (except in the lockfile)
- Separate dev/test dependencies from production dependencies using named groups (`[tool.poetry.group.dev.dependencies]`)
- Use `poetry run` to execute commands — never manually activate the virtual environment in scripts or CI
- Validate published packages with `twine check dist/*` before running `poetry publish`
- Run `poetry install --only main` in production deployments to skip unnecessary dev dependencies and speed up install

### MUST NOT DO
- Edit `poetry.lock` manually — always regenerate with `poetry lock`, even for single dependency changes
- Mix Poetry-managed installs with `pip install` in the same virtual environment — this corrupts the dependency tree
- Commit `pyproject.toml` without a matching `poetry.lock` — future builds will be non-deterministic
- Use `*` (wildcard) version constraints for production dependencies — this defeats reproducible builds
- Remove `poetry.lock` to "fix" dependency conflicts — instead, adjust version constraints in `pyproject.toml` and re-resolve
- Install Poetry via `pip install poetry` as the primary method — use the official installer (`install.sh`) or your package manager to avoid bootstrap issues

---

## Output Template

When configuring or auditing a Poetry-managed project, produce:

1. **Dependency Audit** — List all production and dev dependencies with resolved versions from poetry.lock, flagging any wildcard constraints or version conflicts
2. **pyproject.toml Review** — Validate structure: presence of `[tool.poetry]`, `requires-python`, dependency groups, scripts, and build-system configuration
3. **Lockfile Freshness Check** — Verify poetry.lock timestamp against pyproject.toml; report if manual edits may have drifted the lockfile from the manifest
4. **Workspace Analysis** — For monorepo setups: confirm all workspace members are declared, cross-references use `path` dependencies, and there are no inter-package version conflicts
5. **Publish Readiness** — Checklist: twine validation passed, changelog updated, version bumped, PyPI token configured, extras defined for optional features

---

## Related Skills

| Skill | Purpose |
|---|---|
| `python-uv` | uv alternative by Astral — 10-100x faster package resolution with Rust backend |
| `package-ecosystem-navigator` | General package manager ecosystem comparison (npm, pypi, cargo, etc.) |
| `dependency-supply-chain-security` | Dependency security auditing, CVE scanning, and supply chain protections |

---

## Live References

> Authoritative documentation links for this skill's domain. The model follows markdown links at load time to resolve external references and inline content.

- [Poetry Documentation](https://python-poetry.org/docs/)
- [Poetry pyproject.toml Reference](https://python-poetry.org/docs/pyproject/)
- [Poetry Workspaces (Monorepo Support)](https://python-poetry.org/docs/workspaces/)
- [Poetry Plugin Development](https://python-poetry.org/docs/plugins/)
- [PEP 621 — Storing Project Metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [Twine — PyPI Package Upload Tool](https://twine.readthedocs.io/)
- [Semantic Versioning (SemVer) Specification](https://semver.org/)
