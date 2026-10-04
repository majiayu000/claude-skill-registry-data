---
name: jade-core-retry-router
description: >-
  Routes failed JADE migration rule tasks back into the same rule batch with
  bounded retries. Use when the orchestrator encounters VERIFICATION_FAILED
  or RULE_GATE_FAILED and the user wants automatic requeue with back-off
  before escalation. Reads verification outputs and fix results to decide
  requeue vs escalate per failed rule.
---

# JADE Retry Router

## Objective

Intercept rule-batch failures from the JADE migration pipeline, parse the
verification outputs, and either requeue the failed rule (if retries remain)
or escalate it (if the retry budget is exhausted).  This prevents a single
transient build failure from aborting the entire migration run.

## Required input

| Artifact | Purpose |
|----------|---------|
| `artifacts/06-fix-result-*.json` | Per-rule fix attempt results (one file per rule, or one aggregate file) |
| `artifacts/07-semantic-diff.json` | Post-fix semantic verification diff |
| `artifacts/07-build.log` | Build/compilation output from the verification gate |

All paths are relative to the artifacts directory configured in
`artifacts/00-run-config.json`.

## Produced artifacts

| Artifact | Purpose |
|----------|---------|
| `artifacts/08-retry-queue.json` | Rules that still have retries remaining, ordered by priority |
| `artifacts/08-escalations.json` | Rules that exhausted their retry budget, with failure trail |
| `artifacts/08-final-status.json` | Summary: requeued count, escalated count, overall status |
| `artifacts/ACTION_REQUIRED.md` | **Human-readable escalation ledger.** Written when rules are escalated. Contains per-rule failure reasons, affected files, error details, and suggested remediation steps. |

## Retry policy

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_retries` | 3 | Total fix attempts per rule (including the initial attempt) |
| `escalation_threshold` | `>= max_retries` | When `attempt >= max_retries`, the rule is escalated |
| `backoff_base_s` | 0 (no delay) | Seconds to suggest before next attempt (informational only) |

### Failure classification

| Failure type | Detected from | Priority |
|-------------|---------------|----------|
| `BUILD_ERROR` | `07-build.log` contains `error:` lines | HIGH |
| `SEMANTIC_MISMATCH` | `07-semantic-diff.json` has `mismatch_count > 0` | MEDIUM |
| `FIX_FAILED` | `06-fix-result-*.json` has `status == "FAILED"` | HIGH |
| `MISSING_ARTIFACT` | Expected artifact absent or malformed | CRITICAL (escalate immediately) |

### Escalation criteria

A rule is escalated (moved to `08-escalations.json`) when **any** of these hold:

1. `attempt >= max_retries`
2. The same failure signature repeats on 2 consecutive attempts without
   change in the fix result (stalled rule — further retries pointless)
3. A `CRITICAL` failure type is detected (missing artifact, unparseable
   output)

## Workflow

1. Discover all `artifacts/06-fix-result-*.json` files via glob.
2. Parse `artifacts/07-semantic-diff.json` for verification mismatches.
3. Parse `artifacts/07-build.log` for compilation errors.
4. Match each failure to its `rule_id` from the fix results.
5. For each failed rule:
   - Determine `attempt` number (from fix result or inferred from
     previous retry-queue.json entries).
   - Classify failure type and assign priority.
   - If eligible for retry: push to the retry queue.
   - If escalated: record the full failure trail in escalations.
6. Write `artifacts/08-retry-queue.json` (sorted by priority, then
   ascending attempt count).
7. Write `artifacts/08-escalations.json` with per-rule failure trails.
8. Write `artifacts/08-final-status.json` with aggregate counts and
   overall status (`ALL_CLEAR`, `PARTIAL_RETRY`, `PARTIAL_ESCALATION`,
   `FULL_ESCALATION`).

## Invocation

```bash
python .claude/skills/jade-retry-router/scripts/retry_router.py \
  --artifacts artifacts/ \
  --max-retries 3
```

## Constraints

1. Never modify the original rule batch (`05-rule-queue.json`).
2. Never decrement the attempt counter — it is always monotonic.
3. A `MISSING_ARTIFACT` failure type MUST escalate on first occurrence
   (no retry).
4. Log every routing decision to `phase-history.log.jsonl` if the file
   exists in the artifacts directory.
5. Atomic writes: write to `.tmp` then rename.
