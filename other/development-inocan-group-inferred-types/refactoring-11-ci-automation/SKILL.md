---
name: refactoring-11-ci-automation
description: Use when adding minimal CI automation for lint, tests, and type checks in Python research code.
---

# Refactoring 11: CI and Automation

## Goal

Automate the minimum checks to keep the codebase healthy.

## Sequence

- Order: 11
- Previous: refactoring-10-security-privacy
- Next: refactoring-12-data-versioning

## Workflow

- Check for existing CI; extend it instead of replacing.
  - Success: Existing CI remains intact with minimal additions.
- Add a simple pipeline for linting, tests, and type checks.
  - Success: CI runs lint, test, and type checks on pushes or PRs.
- Keep runtime short; split heavy jobs into optional workflows.
  - Success: Default CI completes quickly.
- Ensure commands run via `uv run` where applicable.
  - Success: CI uses `uv run` consistently for Python checks.
- Document how to run the same checks locally.
  - Success: Local check commands are documented.

## Guardrails

- Avoid complex CI matrices unless required.
- Keep CI changes isolated from refactor changes.
- Do not break existing deployment workflows.
