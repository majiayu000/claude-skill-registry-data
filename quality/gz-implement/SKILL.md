---
name: gz-implement
description: Use to run Gate 2 for an ADR and record the result.
category: governance-infrastructure
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
metadata:
  skill-version: "0.2.1"
model: haiku
---

# gz implement

## Overview

Run Gate 2 for one ADR and record the result in the ledger. `gz implement`:

- resolves the target ADR from `--adr` (a bare `0.1.0` gains the `ADR-` prefix
  and is canonicalized through the ledger's rename events); with no `--adr` it
  uses the single ADR pending attestation, and exits 1 when there are none or
  several;
- runs the `verification.test` command from `.gzkit/manifest.json` (default
  `uv run gz test`) and prints its output;
- appends a Gate 2 `gate_checked` event carrying the command, its exit code and
  `pass` or `fail`;
- when the tests pass, runs the eval delta: it scores `data/eval/*.json` and
  compares the scores with `data/eval/baselines/*.baseline.json` under
  `config/eval_thresholds.json`. A second Gate 2 event, command `eval-delta`,
  records the outcome, or `pass` with `skipped:` evidence when either
  directory is empty;
- exits 1 when the tests fail or the eval delta finds a regression.

It writes the ledger on every run, pass or fail. It does not run lint, docs or
BDD; `uv run gz check` is the per-change quality gate.

## Workflow

1. Name the ADR: `uv run gz implement --adr ADR-<X.Y.Z>`. Pass `--adr` whenever
   more than one ADR is pending, which is the usual state.
2. On a test failure, fix the failing tests and re-run. On an eval regression,
   the output names the surface, dimension, baseline and current score.
3. Report the ADR id, the pass/fail line and any regression lines.

## Example

```bash
uv run gz implement --adr ADR-0.1.0
```
