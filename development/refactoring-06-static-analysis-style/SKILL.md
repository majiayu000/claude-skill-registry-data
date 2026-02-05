---
name: refactoring-06-static-analysis-style
description: Use when adding formatting, linting, and type checking to Python research code.
---

# Refactoring 06: Static Analysis and Style

## Goal

Improve maintainability with consistent formatting, linting, and basic type checking.

## Sequence

- Order: 06
- Previous: refactoring-05-testing-regression
- Next: refactoring-07-documentation-usage

## Workflow

- Detect existing formatters and linters; extend their configs instead of replacing.
  - Success: Existing tooling remains primary with minimal config changes.
- If none exist, propose a minimal toolchain (for example: ruff + black).
  - Success: A small, documented toolchain is selected.
- Fix warnings in touched code first; avoid mass rewrites unless requested.
  - Success: Touched files are clean without broad rewrites.
- Add type hints to public functions and core data structures.
  - Success: Public APIs have basic type annotations.
- Run checks via `uv run` to use the repo environment.
  - Success: Checks execute successfully through `uv run`.

## Guardrails

- Avoid noisy lint rules that block iteration.
- Keep formatting changes separate from logic changes when possible.
- Prefer gradual typing over strict project wide enforcement.
