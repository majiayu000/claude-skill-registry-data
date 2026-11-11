---
name: scaffold-python
description: Scaffold a new plain runnable Python application in an already-created directory. Use for new non-framework Python applications; do not use for publish-first libraries, existing configured Python projects, web frameworks, monorepos/workspaces, or projects with substantial Python configuration.
---

# Scaffold Python Application

Create a small packaged application using `scripts/scaffold.py` and the canonical
files in `assets/`. The agent handles eligibility, runtime and dependency
selection, installation, and diagnosis. The script owns baseline file contents.
Do not independently recreate or customise the baseline.

## 1. Inspect and prepare

- Work in the requested existing directory, or the current directory if unspecified.
  Inspect before writing and preserve unrelated files.
- Stop if `pyproject.toml` or substantial Python configuration already exists.
  Do not use this skill for publish-first libraries, frameworks, or workspaces.
  If an ancestor defines a uv workspace, stop and request a standalone location;
  do not modify the parent workspace or silently join it.
- Require installed uv. Do not install or upgrade uv automatically. Use uv for
  Python selection, environments, dependencies, and builds.
- Select the newest **locally installed final CPython** using
  `uv python list --only-installed --output-format json`. Consider only entries
  whose implementation is `cpython`, variant is `default`, path exists, and
  version is exactly three numeric components. Compare version components
  numerically. Do not infer the runtime from the calendar or a release schedule.
- Require CPython 3.11 or newer. Resolve the selected exact version through uv and
  confirm its actual version, CPython implementation, and final release status.
  Python has no LTS designation. Never select alpha, beta, release-candidate,
  free-threaded, or other implementation variants for this baseline.
- Set `UV_PYTHON_DOWNLOADS=never` throughout. Do not download Python or install it
  into a temporary directory. Stop if no suitable installed interpreter exists.
  Keep any explicit interpreter selection consistent across commands.
- If the default uv cache is unwritable, set `UV_CACHE_DIR` to a writable temporary
  location and keep it set through all checks. Do not disable TLS verification.
- If Git is available, detect an existing repository using Git rather than just
  a local `.git` entry. Reuse it without changing parent configuration, or run
  `git init` when outside a repository. Stop before generation if Git preparation
  is blocked. If Git is unavailable, continue and report it as unavailable.
  Never create a nested repository, commit, push, merge, rebase, or create remotes.

## 2. Resolve development dependencies

Resolve exact latest stable mutually compatible releases of `ruff`, `mypy`,
`pytest`, and the `uv_build` build backend for the selected Python. Use uv's
resolver and inspect metadata as needed. A temporary requirements file outside
the project can be resolved with `uv pip compile --python-version <exact-version>`.
Do not add application runtime dependencies, pytest plugins, or extra tooling.
Report any compatibility fallback instead of silently weakening checks.

Write a temporary JSON input file outside the project with exactly these fields:

| Field          | Value                                                                          |
| -------------- | ------------------------------------------------------------------------------ |
| `python`       | Selected exact final version, such as `3.14.6`                                 |
| `uv_build`     | Resolved exact stable backend version                                          |
| `dependencies` | Object with exactly `mypy`, `pytest`, and `ruff`, each an exact stable version |

Version numbers are resolved inputs, not defaults to copy from this document.

## 3. Generate and install

Resolve paths relative to this skill's directory, then run through uv:

```text
uv run --no-project --python <exact-version> <skill-directory>/scripts/scaffold.py create <project-directory> <inputs.json>
```

The script derives the distribution, import package, and CLI names from the
existing directory without renaming it. It handles punctuation, numeric prefixes,
and Python keywords. It pins the Python minor line and exact tool/backend
versions, and creates a packaged `src/` application with typed entry points,
Ruff, strict mypy, pytest importlib mode, executable `check.sh`, and VS Code
module debugging using the project `.venv` on POSIX and Windows.

Existing destination files block generation except `.gitignore`, whose existing
contents are preserved and missing baseline entries appended. Unsafe paths and
symlink destinations are refused before baseline writes. Do not delete conflicts,
bypass the generator, or overwrite existing files to proceed. A partial write
failure must be reported; do not rerun over partial output.

Do not use `uv init` to produce a second baseline, add project guidance or README
files, or let uv initialize Git. Run `uv lock` and `uv sync --locked` using the
selected Python, and retain `uv.lock`. Keep uv's editable project installation.
Do not pass `--no-install-project`, `--no-editable`, or bypass lock verification.
If resolution fails, diagnose within the stated constraints. If changing resolved
inputs after generation is necessary, report the scaffold as incomplete rather
than editing canonical files around the generator's preservation rule.

In pyproject.toml under [tool.mypy], set `python_version = ""` to the major.minor
version of the Python interpreter used in this scaffold (for example "3.14").

## 4. Verify and report

Run every check and inspect its own exit status; stop on an unresolved failure:

1. `uv run --locked ruff format .`
2. `uv run --no-project --python <exact-version> <skill-directory>/scripts/scaffold.py verify <project-directory> <inputs.json>`
3. `./check.sh`
4. `uv run --locked <cli-name>`
5. `uv run --locked python -m <import_package>`
6. `uv build`

Both entry points must print `Application is running.` and exit successfully.
Confirm that a wheel and source archive exist in `dist/`. Inspect the editable
installation using `importlib.metadata`: the distribution's `direct_url.json`
must mark it editable, and the imported package must resolve under this project's
`src/`. Inspect `git status --short` when Git is available.

Completion requires canonical verification and every required check to pass.
Report Python and uv versions, derived distribution/package/CLI names, Git outcome,
compatibility fallbacks, temporary cache use, and check results. Distinguish
passed, failed, blocked before execution, and not attempted; never report an
unexecuted operation as a failure. Fix scaffold defects without changing the
canonical baseline merely to make a check pass.

## Boundaries

Do not add project guidance, ADRs, specifications, README files, licenses, CI/CD,
Docker, environment files, Git hooks, publishing or release tooling, frameworks,
databases, workspace configuration, coverage tooling, or extra task runners.
Use Ruff for formatting and linting, mypy for typing, and pytest for tests.
Do not substitute another checker or add Black, isort, Flake8, tox, nox, Make,
or just. Create only `.vscode/launch.json` for editor integration; do not add
settings, extension recommendations, source maps, or a project debugpy dependency.
The root executable `check.sh` remains the project's visible quality gate.
