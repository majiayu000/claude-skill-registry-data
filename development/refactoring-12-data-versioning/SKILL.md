---
name: refactoring-12-data-versioning
description: Use when adding lightweight data versioning and dataset reproducibility practices.
---

# Refactoring 12: Data Versioning

## Goal

Make input data changes explicit and reproducible.

## Sequence

- Order: 12
- Previous: refactoring-11-ci-automation
- Next: none

## Workflow

- Define dataset sources, versions, and checksums.
  - Success: Each dataset has an identifiable source and version.
- Store metadata in a manifest (CSV/JSON/TOML).
  - Success: Manifest captures dataset metadata and checksums.
- Separate raw data from derived artifacts.
  - Success: Raw and derived data live in distinct locations.
- Record dataset version alongside experiment outputs.
  - Success: Outputs reference the dataset version used.
- Prefer lightweight tracking unless DVC or similar is already in use.
  - Success: Versioning stays minimal and non-disruptive.

## Guardrails

- Do not commit large datasets to git.
- Avoid tooling changes that block current workflows.
- Keep versioning easy to maintain.
