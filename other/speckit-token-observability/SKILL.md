---
name: "speckit-token-observability"
description: "Required token analysis workflow for Codex Spec Kit orchestration phases."
compatibility: "Requires .specify/token-analysis/ and the Spec Kit token-analyzer extension when available"
---

# Spec Kit Token Observability

Token analysis is a required observability step for every completed Spec Kit phase
and every custom orchestration phase. It is read-only with respect to product
artifacts and must not modify `spec.md`, `plan.md`, `tasks.md`, implementation
code, or contracts except for explicitly requested documentation updates outside
token capture.

## Run Labels

Use this stable format:

```text
<date>-<epic-slug>-<slice-id>-<mode>
```

Example:

```text
2026-05-18-admin-backoffice-s01-gated
```

## Artifact Locations

Each run writes under:

```text
.specify/token-analysis/runs/<run-label>/
├── metadata.json
├── steps/<phase>.json
├── summary.json
├── report.md
└── quality-notes.md
```

Shared comparison and baseline directories:

```text
.specify/token-analysis/comparisons/
.specify/token-analysis/baselines/
```

## Required Phases

Custom orchestration phases:

- intake
- slicing
- scheduling
- integration
- review
- commit
- PR creation

Spec Kit phases:

- specify
- clarify
- checklist
- plan
- tasks
- analyze
- implement

## Capture Methods

Use `exact` when runtime usage is available directly. Use `parsed` when usage is
extracted from a CLI JSON response. Use `estimated` when exact data is unavailable
but input/output artifacts allow a reasonable approximation. Use `unavailable`
only when neither exact nor estimated data can be produced; include a clear note.

For standard token-analyzer-supported phases, use the token-analyzer command or
hook when available. Supported standard phases include `specify`, `plan`, `tasks`,
and `implement`.

For unsupported or optional phases, use
`.agents/skills/speckit-guards/scripts/record-token-step.sh` to write an estimated
or unavailable step record. Do not silently skip token analysis.

## Missing Extension Behavior

Before a full workflow starts, run
`.agents/skills/speckit-guards/scripts/guard-token-analyzer-available.sh`.

If token-analyzer is missing:

- `plan-only` and `gated`: continue only after a clear warning.
- `auto-implement`, `auto-pr`, `auto-stack-pr`, or any run with `auto-commit`
  enabled: stop before automation unless the user explicitly approves
  continuing.

Recommended installation command:

```bash
specify extension add token-analyzer
```

## Token Budgets

If `.specify/token-analysis/token-budget.json` exists, report warning and blocking
threshold status. Warning thresholds never block. Blocking thresholds block only
when explicitly configured as non-null values. If no budget exists, proceed
without budget enforcement and warn on missing token data by default.

## Final Output And PR Body

Final workflow output and draft PR bodies must include:

- Run label
- Token report path
- Total tokens, exact or estimated
- Most expensive phase
- Missing token data
- Token budget status
- Notes, including any approval to continue without token-analyzer
