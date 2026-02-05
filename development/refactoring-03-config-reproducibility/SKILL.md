---
name: refactoring-03-config-reproducibility
description: Use when improving run configuration, seeding, and reproducibility for Python research code.
---

# Refactoring 03: Config and Reproducibility

## Goal

Make experiments reproducible by centralizing configuration, controlling randomness, and recording run metadata.

## Sequence

- Order: 03
- Previous: refactoring-02-dependencies-env
- Next: refactoring-04-data-io-validation

## Workflow

- Centralize runtime parameters into a config object or file (YAML/TOML/argparse).
  - Success: All run parameters are set through a single config surface.
- Seed all RNGs (Python, NumPy, framework) and make the seed a first class parameter.
  - Success: Runs are repeatable with the same seed.
- Record metadata: config snapshot, git commit hash, and environment info with outputs.
  - Success: Each run output includes config and environment metadata.
- Create a consistent output directory layout for artifacts and metrics.
  - Success: Outputs follow a documented directory structure.
- Remove hidden global state and implicit defaults where possible.
  - Success: Behavior is driven by explicit parameters.

## Guardrails

- Keep config changes backward compatible when possible.
- Do not add heavy config frameworks unless required.
- Favor explicit parameters over environment variables.
