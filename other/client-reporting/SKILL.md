---
name: client-reporting
description: Assemble recurring agency reporting workflows for client updates, KPI summaries, and performance readouts. Use when the user needs a reporting template, account-update structure, KPI narrative, or repeatable reporting process.
---

# client-reporting

## Purpose

- Standardize recurring client reporting outputs.
- Turn performance inputs into concise operational readouts.

## Triggers

- The user wants a weekly or monthly client report structure.
- The user wants KPI summaries translated into plain language.
- The user wants a reusable reporting workflow for accounts.

## Inputs

### Required

- reporting period
- KPI set or source metrics

### Optional

- benchmarks or targets
- account notes, wins, blockers, or next actions
- audience level such as operator, manager, or executive

## Outputs

- reporting outline or template
- KPI summary with narrative context
- blockers, wins, and next-step section

## Guardrails

- Do not invent metrics or imply data freshness that was not provided.
- Separate observed metrics from interpretation.
- Escalate when source data is missing, stale, or contradictory.

## Failure Modes

- metrics are missing or not normalized
- report confuses raw data with interpretation
- audience level is wrong for the output style
- next actions do not tie back to the reporting period

## QA Steps

1. Confirm the reporting period is explicit.
2. Check every KPI has a source input or is marked missing.
3. Check the narrative distinguishes fact from interpretation.
4. Check wins, blockers, and next actions are aligned.
