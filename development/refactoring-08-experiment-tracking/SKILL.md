---
name: refactoring-08-experiment-tracking
description: Use when organizing experiment logs, results, and metadata for Python research code.
---

# Refactoring 08: Experiment Tracking

## Goal

Make runs comparable by logging results, configs, and metadata in a consistent structure.

## Sequence

- Order: 08
- Previous: refactoring-07-documentation-usage
- Next: refactoring-09-performance-profiling

## Workflow

- Define a run ID scheme and a consistent output directory layout.
  - Success: Each run has a unique ID and predictable output path.
- Log metrics and key artifacts (plots, model weights, predictions).
  - Success: Metrics and artifacts are saved per run.
- Save config snapshots and environment info with each run.
  - Success: Run outputs include config and environment details.
- Provide a simple summary index (CSV/JSON) for comparing runs.
  - Success: Runs can be compared from a single index file.
- Keep logging lightweight unless a tracking system already exists.
  - Success: Logging adds minimal overhead to runs.

## Guardrails

- Avoid adding heavy tracking frameworks unless requested.
- Do not store large raw data in run outputs.
- Keep the logging format stable once introduced.
