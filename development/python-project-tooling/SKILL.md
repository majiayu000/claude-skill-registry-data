---
name: python-project-tooling
description: >-
  Use for creating, reviewing, debugging, or modernizing Python project
  structure and deterministic tooling with pyproject.toml, uv, dependency
  groups, lockfiles, Ruff, Pyright, pytest, build backends, wheels, sdists, or
  workspaces. Do not use for application architecture, publishing credentials,
  arbitrary pip command help, or code changes unrelated to project tooling.
argument-hint: "[project type, Python support, dependencies, checks, and packaging goal]"
---

# Reproducible Python project contract

First classify the repository:

| Project | Build system | Installation expectation |
|---|---|---|
| Application/non-package | Usually none; optionally `tool.uv.package = false` | Sync dependencies, do not invent a distributable package. |
| Library/package | Explicit `[build-system]` and package layout | Build and inspect wheel plus sdist. |
| Workspace | Root membership plus member metadata | One shared lock; run member-specific commands deliberately. |

## Workflow

1. Inspect existing `pyproject.toml`, `uv.lock`, Python constraint, source
   layout, build backend, dependency groups/extras, tool configuration, CI, and
   current commands before changing anything.
2. Preserve the declared project type. Do not add a build system merely to make
   an application look like a package.
3. Put runtime dependencies in `[project.dependencies]`, optional consumer
   features in `[project.optional-dependencies]`, and development tools in
   `[dependency-groups]`. Keep environment markers explicit.
4. Use `uv add`/`remove` or an intentional metadata edit followed by `uv lock`.
   Commit `uv.lock` for reproducible projects; never edit it manually.
5. Use `uv sync` for an exact project environment and `uv run` for commands.
   In CI or verification, use `--locked` so stale metadata fails rather than
   silently updating the lock.
6. Configure one canonical quality pipeline: Ruff check and format, Pyright,
   pytest, and build inspection when the project is distributable.
7. For a package, run `uv build`, inspect sdist/wheel contents and metadata,
   install the wheel into a clean environment, then import and exercise its
   public entry point.

## Invariants

- `pyproject.toml` declares intent; `uv.lock` records resolution; `.venv` is
  generated state and is not committed.
- A passing editable install is not proof that the built wheel contains the
  package or data files.
- Extras are consumer-selectable features; dependency groups are development
  or task environments. Do not use one as the other.
- Never invoke publishing or handle registry tokens without explicit authority.
- Preview uv features and tool schemas are version-sensitive; inspect installed
  help and current official docs before encoding them.

```text
uv lock --check
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked pyright
uv run --locked pytest
uv build
```

Use [project and dependency layout](references/projects.md), [quality and build
verification](references/verification.md), and [migration safeguards](references/migration.md).
