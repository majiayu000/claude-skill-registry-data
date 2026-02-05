---
name: agilab-testing
description: Quick, targeted test strategy for AGILAB (core unit tests, app smoke tests, regression).
license: BSD-3-Clause (see repo LICENSE)
metadata:
  updated: 2026-01-09
---

# Testing Skill (AGILAB)

Use this skill when validating changes.

## Philosophy

- Start small and local: run only the tests that cover the files you changed.
- Avoid “fixing the world”: do not chase unrelated test failures.

## Common Commands

- Core tests (repo root):
  - `uv --preview-features extra-build-dependencies run --no-sync pytest src/agilab/core/agi-env/test`
  - `uv --preview-features extra-build-dependencies run --no-sync pytest src/agilab/core/test`

- Whole repo tests (if needed):
  - `uv --preview-features extra-build-dependencies run --no-sync pytest`

## Adding Coverage (Easy Wins)

- Add narrow unit tests for pure functions/helpers (path resolution, parsing, small transforms).
- Prefer tests that don’t require network, GPUs, or large datasets.

