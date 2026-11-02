---
name: alert-noise-budget-audit
description: "Use when duplicate, flapping, or non-actionable alerts overwhelm responders; not for defining SLOs from scratch."
---

# Alert Noise Budget Audit

## Purpose

Use when duplicate, flapping, or non-actionable alerts overwhelm responders; not for defining SLOs from scratch.

## Required inputs

Inputs: alert definitions/history, incidents, ownership map, grouping keys, expected operator action.

## Workflow

1. Classify a representative alert window as actionable, duplicate, flapping, informational, misrouted, or unowned.
2. Compare thresholds, evaluation windows, grouping, missing-data behavior, and recovery hysteresis with source metrics.
3. Propose grouping/ownership/threshold changes and test both meaningful incidents and harmless variation.

## Verification checklist

Checks: each page has an owner and first action; duplicates are separated from distinct incidents; changes include positive and negative fixtures; silence rules have bounded scope.

## Required output

Output: measured noise causes, proposed rule changes, and missed-detection regression checks.

## Boundaries and failure handling

Boundary: do not silence critical alerts solely because they are noisy; document approval for risky changes.

When evidence, permission, or environment details are missing, document the limitation and do not claim unrun validation passed.

## Trigger examples

- Positive: Positive: one outage generates dozens of repeated pages.
- Negative: Negative: designing SLO targets without alert-noise symptoms.
