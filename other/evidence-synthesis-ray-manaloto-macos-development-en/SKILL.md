---
name: evidence-synthesis
description: Synthesize discovery, repository, social, and validation evidence into DecisionRecords and AcceptanceRecords, producing a decision-complete implementation spec.
---

# Evidence Synthesis

## Overview

Use this skill in Phase D/E to convert mined evidence into executable decisions.
The output is not a summary dump; it is a plan with gates and ownership.

## Inputs

- Discovery records
- Pattern records (repo + social)
- Local validation mapping

## Required Outputs

Write:
- `reports/research-ros/<date>-decision-records.jsonl`
- `reports/research-ros/<date>-acceptance-records.jsonl`
- `reports/research-ros/<date>-research-bundle.json`
- `docs/plans/<date>-devcontainer-research-ros-spec.md`

Use schemas in `docs/research/schemas/`.

## Decision Rules

Every adopted pattern must include:
- rationale
- migration cost
- enforcement impact
- linked proof

Reject patterns with weak portability or missing implementation evidence.

## Acceptance Rules

The final spec must include machine-checkable gates for:
- devcontainer runtime state
- mise tool authority
- `mde-verify` hard-fail / hard-skip semantics
- AGENTS/skill policy enforcement
