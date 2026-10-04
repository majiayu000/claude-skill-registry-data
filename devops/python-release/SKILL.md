---
name: python-release
description: Release engineering for Python projects on uv — static versioning in pyproject.toml exposed via importlib.metadata, building the sdist and wheel with uv build, publishing to PyPI with uv publish via Trusted Publishing (OIDC, no token), tag-triggered GitHub Actions releases, CI running ruff/ty (or pyright)/pytest with SHA-pinned actions, and Renovate coverage for uv and Actions. Use when releasing or publishing a Python package to PyPI, running uv build to make a wheel and sdist, running uv publish, configuring Trusted Publishing or a tag-triggered release workflow, writing a GitHub Actions CI workflow that runs ruff format/ruff check/ty (or pyright)/pytest for a uv project, versioning a package, or adding Renovate coverage for uv and GitHub Actions to a Python repo.
license: MIT
---

# Python release engineering

Tag-driven releases: pushing a `vX.Y.Z` tag builds the sdist and wheel with `uv build` and
publishes them to PyPI with `uv publish` via Trusted Publishing — no stored token. CI gates every
push; Renovate keeps dependencies and the action pins fresh. This layers on the layout and
Makefile from the `python-project` skill. For the publishing and Renovate rationale and the full
ecosystem matrix, see [reference.md](reference.md).

For a `bitwise-media-group` repo, prefer the org's centralized, SHA-pinned CI/security/release/merge
callers over the bespoke `ci.yaml`/`release.yaml` below — see the `actions-reusable-workflows`
skill. The templates here are for a Python repo outside that org infrastructure.

## 1. Version statically, read it from metadata

The `uv_build` backend takes the version from `[project] version`. Bump that line, commit, then tag
`vX.Y.Z` to match — both the tag and the artifact come from the same source, so they cannot drift.
Expose it at runtime from the installed metadata rather than re-declaring it:

```python
from importlib.metadata import version

__version__ = version("myapp")
```

(To derive the version from git tags instead, see the `hatch-vcs` note in [reference.md](reference.md).)

## 2. Build with uv

```sh
uv build          # writes the sdist + wheel to dist/
```

`make build` wraps this (see `python-project`); validate a build locally before tagging.

## 3. CI workflow

Copy [templates/ci.yaml](templates/ci.yaml) to `.github/workflows/ci.yaml`. Every push and pull
request runs `ruff format --check`, `ruff check`, `ty check`, and `pytest` — a pyright project
swaps `uv run pyright` for the `ty check` step (see `python-typing`). Conventions:

- `astral-sh/setup-uv` installs uv; `uv sync --locked` provisions the interpreter (from
  `.python-version`) and the exact locked dependencies, failing if `uv.lock` is stale.
- Every action is pinned to a full commit SHA with the tag in a trailing comment — a moved tag can
  never change what runs. Renovate keeps the pins fresh.
- `permissions: contents: read` — the default token does nothing else.

## 4. Release workflow

Copy [templates/release.yaml](templates/release.yaml) to `.github/workflows/release.yaml`. It
triggers on `v*` tags, builds, and runs `uv publish --trusted-publishing always`. Trusted
Publishing needs `permissions: id-token: write` and a one-time publisher config on PyPI (repository,
workflow filename, and the `environment:` the job pins) — no API token in secrets. Cutting a release
is exactly: bump `[project] version`, tag the matching `vX.Y.Z`, push.

## 5. Renovate

Copy [templates/renovate.json5](templates/renovate.json5) to `.github/renovate.json5`: a 7-day
cooldown before any update is proposed, minor + patch bumps grouped into one PR per manager (majors
arrive alone). The `pep621` rule covers `pyproject.toml` + `uv.lock` (runtime and dev-group
dependencies); the `github-actions` rule keeps the workflow SHA pins fresh. For the rationale and
the full ecosystem matrix (`docker`, `docker-compose`, `npm`, …), see [reference.md](reference.md).
