---
name: python-packaging
description: >
  Package, build, distribute, and manage modern Python libraries and CLI tools.
  Use when writing or updating pyproject.toml, configuring build backends
  (hatchling, flit, setuptools), building wheels and sdists, managing dependencies
  with uv or pip, configuring CLI console_scripts entrypoints, or publishing to PyPI.
compatibility: >
  Agent Skills-compatible coding agents working on Python packaging manifests
  and distribution artifacts.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "python, packaging, pyproject, wheels, uv, pypi, build"
  topics: "programming-languages, devtools, software-development"
---

# Modern Python Packaging

Python packaging has standardized around `pyproject.toml` (PEP 517, 518, 621). Deprecated legacy files like `setup.py`, `setup.cfg`, and `requirements.txt` are replaced by declarative project metadata, standardized build backends, and fast package management via `uv` or `pip`.

## Core Rules

1. **Declarative metadata in `pyproject.toml`**: Never use executable `setup.py` scripts for static configuration.
2. **Always adopt the `src/` layout**: Placing packages inside `src/<package_name>/` prevents accidental imports of uninstalled local files during testing.
3. **Include `py.typed`**: If your library includes type annotations, place an empty `py.typed` marker file inside your package directory to inform type checkers.
4. **Pin dependencies appropriately**: Use ranges for libraries (e.g. `pydantic>=2.0,<3.0`) to avoid constraining consumers; use exact lockfiles (`uv.lock`) for applications.
5. **Never commit build artifacts**: Add `dist/`, `build/`, and `*.egg-info/` to `.gitignore`.

---

## 1. Canonical `pyproject.toml` (PEP 621)

Example using `hatchling` (the modern recommended default backend):

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "data-pipeline-core"
version = "1.2.0"
description = "High-performance streaming data parser"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
authors = [
    { name = "Michael Weiss", email = "dev@example.com" }
]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Typing :: Typed",
]
dependencies = [
    "pydantic>=2.5.0,<3.0.0",
    "httpx>=0.27.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "mypy>=1.9.0",
    "ruff>=0.4.0",
]

# Expose CLI commands
[project.scripts]
data-pipeline = "data_pipeline_core.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["src/data_pipeline_core"]
```

---

## 2. Directory Structure: The `src` Layout

```text
data-pipeline-core/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── data_pipeline_core/
│       ├── __init__.py
│       ├── cli.py
│       ├── engine.py
│       └── py.typed
└── tests/
    └── test_engine.py
```

---

## 3. Building and Inspecting Artifacts

Use modern standard tools (`build`, `twine`, or `uv`):

```bash
# 1. Build sdist (.tar.gz) and wheel (.whl)
python -m build
# Or with uv:
uv build

# 2. Inspect generated archive contents
tar -tzf dist/*.tar.gz
unzip -l dist/*.whl

# 3. Check package metadata integrity
twine check dist/*
```

---

## 4. Virtual Environments and uv Workflows

`uv` provides 10-100x faster package resolution and deterministic locking:

```bash
# Initialize a project with uv
uv init --lib my-library

# Add dependencies
uv add "httpx>=0.27"
uv add --dev pytest mypy

# Run commands within virtual environment
uv run pytest
uv run mypy src/

# Lock dependencies deterministically
uv lock
```

---

## 5. Common Packaging Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| Flat layout (`my_pkg/` in repo root) | Tests import local directory rather than built wheel | Use `src/my_pkg/` layout |
| Missing `py.typed` marker | Mypy ignores inline annotations when imported as dependency | Touch `src/my_pkg/py.typed` |
| Over-constraining dependencies (`pydantic==2.5.1`) | Causes dependency conflicts for downstream consumers | Use semver ranges: `pydantic>=2.5.0,<3.0.0` |
| Using `setup.py` for metadata | Vulnerable to arbitrary code execution at install time | Use declarative `pyproject.toml` |

---

## 6. Pre-Publish Checklist

- [ ] Version number bumped in `pyproject.toml` following SemVer.
- [ ] `README.md` and `LICENSE` exist and are correctly referenced.
- [ ] `py.typed` file present inside `src/<package>/`.
- [ ] `python -m build` generates clean `.whl` and `.tar.gz` in `dist/`.
- [ ] `twine check dist/*` reports no formatting or metadata errors.
- [ ] Installed and tested in a clean virtual environment (`python -m venv test_env && pip install dist/*.whl`).
