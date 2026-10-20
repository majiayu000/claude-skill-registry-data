---
name: publish-python-library
description: >-
  Load this skill when packaging, versioning, or publishing a Python library: build backend, src/
  layout, wheels, PyPI, the public API in __init__.py / __all__, deprecations, semver. Auto-load
  when build config or __all__ is edited, a public signature changes, or uv build runs.
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Requires Python 3.12+ and the `uv` package manager on PATH, plus network access to PyPI for
  resolving dependencies and for `uv publish`. Nothing is assumed to be installed globally: build
  and publish run through `uv`, and verifying the public surface uses the project's `mypy` and
  `pytest` dev dependencies, which `uv sync` installs.
license: Apache-2.0
---

# Publish a Python Library

A library's outward surface is three things that change together: what the package exports, what
version number that earns, and how it is built and uploaded. The public API decides the version,
and the version decides the release. Done when the wheel and sdist build, `uvx twine check` passes,
and a TestPyPI install imports the public API.

## Procedure

1. Define the public surface in `__init__.py` / `__all__` and decide the semver level the change
   earns.
2. Deprecate a public symbol before removing it.
3. Build with an explicit backend in the `src/` layout, a wheel and an sdist, with `py.typed`.
4. Publish to TestPyPI, install from it once, then publish to PyPI.

## Rules

### Define the public surface explicitly

The public API is exactly what `__init__.py` exports — nothing else is a contract.

```python
# src/your_library/__init__.py
from your_library.core import RetryPolicy, parse_duration

__all__ = ["RetryPolicy", "parse_duration"]
```

- Anything not in `__all__` (and any `_leading_underscore` name) is private — consumers must not rely on it, and you may change it freely.
- Keep the surface small. Every public symbol is a maintenance commitment.
- Re-export from a stable top-level path so internal module moves don't break consumers.

### Semantic versioning (driven by the public API)

The public API decides the level: a removed or renamed symbol, a changed signature, or changed
behavior consumers depend on is MAJOR, a new symbol or optional parameter is MINOR, anything with no
public effect is PATCH. When in doubt, bump the higher level. Never re-use or lower a version.

### Deprecation before removal

Never remove or change a public symbol without a deprecation period.

```python
import warnings


def old_name(*args, **kwargs):
    warnings.warn(
        "old_name() is deprecated; use new_name(). Removed in 3.0.",
        DeprecationWarning,
        stacklevel=2,
    )
    return new_name(*args, **kwargs)
```

- Emit `DeprecationWarning` with the replacement and the removal version.
- Keep the deprecated path working for at least one MINOR release.
- Remove it only in a MAJOR release, and document it in the changelog.

### Build system

Declare an explicit build backend in `pyproject.toml`. Default to **hatchling**; `uv_build` is fine if the project is uv-native.

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "your-library"
version = "1.2.0"
description = "One-line summary of what the library does."
readme = "README.md"
requires-python = ">=3.12"
license = "MIT"
authors = [{ name = "...", email = "..." }]
dependencies = []  # minimal — every dependency is imposed on consumers

[project.urls]
Homepage = "https://github.com/owner/your-library"
```

### src layout (mandatory)

```
your-library/
├── pyproject.toml
├── README.md
├── src/
│   └── your_library/
│       ├── __init__.py        # defines the public API (see Define the public surface above)
│       └── py.typed           # ship type information (PEP 561)
└── tests/
```

The `src/` layout prevents accidentally importing the working tree instead of the installed package —
tests run against the built/installed library, catching missing-data and packaging bugs before release.

Always ship `py.typed` so consumers get your type hints.

### Build and publish

```bash
uv build                      # produces dist/*.whl and dist/*.tar.gz (wheel + sdist)
uvx twine check dist/*        # validate metadata before upload
uv publish --publish-url https://test.pypi.org/legacy/   # TestPyPI dry run first
uv publish                    # then the real PyPI
```

- Always build **both** a wheel and an sdist: the wheel installs fast, and the sdist serves source
  builds and distro packagers.
- Publish to **TestPyPI** and install from it once before publishing to real PyPI.
- A version is published exactly once — PyPI rejects re-uploads. Bump the version to fix a bad release.

### No web dependencies

A library must not pull in application/web-server dependencies (`fastapi`, `uvicorn`, `asyncpg`, web
frameworks). If web behavior is needed, expose a clean API and let the consuming application wire the
transport. Optional integrations go under `[project.optional-dependencies]`, never the base set.
