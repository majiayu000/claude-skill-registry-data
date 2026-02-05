---
name: refactoring-07-documentation-usage
description: Use when documenting Python research code usage, setup, and experiment reproduction.
---

# Refactoring 07: Documentation and Usage

## Goal

Make the project understandable and runnable by a new contributor.

## Sequence

- Order: 07
- Previous: refactoring-06-static-analysis-style
- Next: refactoring-08-experiment-tracking

## Workflow

- Update `README.md` with purpose, setup, data expectations, and run commands.
  - Success: README includes accurate setup and run instructions.
- Add docstrings for public modules and functions that are reused.
  - Success: Public APIs have concise docstrings.
- Provide a minimal example command or notebook that reproduces results.
  - Success: A minimal example reproduces expected output.
- Document output artifacts and how to interpret them.
  - Success: Outputs and metrics are explained in docs.
- Keep docs synced with the current entrypoints and config fields.
  - Success: Docs match current entrypoints and config options.

## Guardrails

- Avoid duplicating API docs already generated elsewhere.
- Keep examples small and fast to run.
- Prefer concrete commands over narrative text.
