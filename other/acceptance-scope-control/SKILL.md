---
name: acceptance-scope-control
description: Use when an AI is about to report accepted, passed, closed, ready, done, or equivalent handoff, receipt, or completion wording.
---

# Acceptance Scope Control

## Core Principle

Acceptance wording must not exceed the dimensions actually verified. `accepted`, `passed`, and `closed` are scoped receipts, not global status words.

## Scope Dimensions

Every acceptance claim must state coverage for:

- route or workflow entry,
- surface or component,
- viewport or environment,
- data source and data shape,
- role or permission assumption,
- assertion level,
- fact source,
- receipt identity,
- skipped checks.

## Procedure

1. Draft the intended acceptance sentence.
2. Break it into implied claims.
3. Map each claim to evidence.
4. Remove or downgrade any claim without evidence.
5. Add explicit uncovered scope and skipped checks.
6. Return a bounded receipt.

## Verdict Vocabulary

| Verdict | Use When |
| --- | --- |
| `accepted_scope_limited` | All stated assertions passed within the listed scope only. |
| `passed_assertions_only` | Checks passed, but acceptance authority is not established. |
| `not_ready_for_acceptance` | Required assertions are missing or failed. |
| `blocked_missing_evidence` | Verification cannot continue without a specific source or artifact. |
| `needs_same_scope_rerun` | Evidence is stale, inherited, or not aligned to the requested scope. |

## Receipt Template

```md
verdict:
covered_routes:
covered_surfaces:
covered_viewports:
covered_data:
assertions:
fact_sources:
skipped_checks:
not_covered:
remaining_risks:
next_owner:
```

## Common Mistakes

- Saying `closed` because one failing case was fixed.
- Saying `accepted` from a build, lint, or static scan alone.
- Hiding skipped checks in prose.
- Treating an upstream acceptance receipt as current evidence.
- Expanding from one viewport, route, role, or data shape to all variants.

## Red Flags

Stop and rewrite the receipt if it contains broad words such as "all", "entire", "complete", "fully", or "no issues" without matching evidence for every dimension.
