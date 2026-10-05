---
name: eval-gate-authoring
description: |
  Turn observed run outputs into eval-spec Artifacts, paired Gates,
  and policy bindings. Use when creating or calibrating automated,
  human, or LLM-as-judge eval gates for processkit workflows.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-eval-gate-authoring
    version: "2.0.0-alpha.1"
    created: 2026-04-30T00:00:00Z
    category: processkit
    layer: 3
    provides:
      primitives: [Artifact, Gate, Binding, LogEntry]
      mcp_tools:
        - collect_run_outputs
        - codify_eval
        - calibrate_judge
        - bind_eval_to_runs
---

# Eval Gate Authoring

## Intro

Eval gate authoring promotes repeated run observations into enforceable
checks. Capture examples, codify an `eval-spec` Artifact, create the
paired Gate, calibrate any LLM judge against human labels, then bind
the eval to the target run surface with a `policy-application` Binding.

## Overview

The workflow starts from observed run output and ends with an auditable
Gate plus bindings that describe where the evaluation applies.
LLM-as-judge evals require calibration evidence before they should be
treated as enforceable.

## Gotchas

- Do not create an eval gate from one example unless the gate is clearly
  marked exploratory.
- Do not treat an LLM judge as calibrated until human labels and a
  calibration LogEntry exist.
- Bind evals to the narrowest useful run surface so a local experiment
  does not accidentally become a global policy.

## Full reference

### MCP tools

- `collect_run_outputs`
- `codify_eval`
- `calibrate_judge`
- `bind_eval_to_runs`

### Produced entities

- `Artifact(spec.kind=eval-spec)`
- `Gate`
- `Binding(type=policy-application)`
- calibration `LogEntry` records
