---
name: om-prepare-issue
description: Repo-local extension of om-prepare-issue - the tenant, money and visual sections every issue here carries, the plan-stage mapping and the out-of-scope register.
---

# om-prepare-issue (money-tracker.online)

This file extends the shared `om-prepare-issue` skill installed at
`.claude/skills/om-prepare-issue/SKILL.md`. Follow its full workflow (dedupe, covering spec,
analysis, body, labels, report) with the rules below layered on top.

## Before creating

- Read `docs/agents/out-of-scope.md`. A brief that matches a row there is not filed: report the row
  and the ADR it cites, and stop.
- When the brief maps to a stage in a plan under `docs/plans/`, name it in the Summary
  (`Plan stage: 12-S3`) and carry the stage's Blockers, Tenant isolation test and Money invariant
  into the body verbatim. The plans are the backlog source (`docs/plans/README.md`).

## Body: additional sections

Append these after `## How to implement`, in this order. None is ever omitted; `n/a` needs a
reason on the same line.

- `## Tenant isolation test`: the case to add to
  `src/server/repos/__tests__/tenant-isolation.test.ts` for every new repository read or write path.
- `## Money invariant`: the arithmetic property the change must not break, and the case in
  `src/server/repos/__tests__/money-invariants.test.ts` that holds it. Never `n/a` when the change
  touches an amount, a rate, a currency or a date bucket.
- `## Visual change expected`: `none`, or the screens and states whose rendered output changes on
  purpose. Nothing in CI compares a pixel (ADR 0016), so this is the only notice a reviewer gets.

## Body: interfaces, not file paths

`## How to implement` names types, function signatures, message keys and config shapes. File paths
and line numbers go stale while the issue waits.

## Labels

- Category: a defect is `bug`; new behaviour is `feature`; the rest is `refactor`. A security
  defect is `bug` plus `security`.
- Risk: `risk-high` for anything touching auth, tenant scoping, money, the ledger, billing or a
  migration.
