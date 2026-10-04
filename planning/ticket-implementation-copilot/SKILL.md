---
name: ticket-implementation-copilot
description: Execute DSDS roadmap tickets using dependency-aware, acceptance-criteria-first delivery. Use when selecting the next unblocked ticket, implementing code changes, validating behavior, and reporting completion against ticket AC.
---

# Ticket Implementation Copilot

## Overview
Implement DSDS tickets in a predictable way by prioritizing unblocked work and validating acceptance criteria explicitly.

## Workflow

1. Select next unblocked ticket
- Read dependencies from `planning/TICKETS.md`.
- Pick the highest-priority ticket whose blockers are resolved.

2. Translate ticket into implementation plan
- Extract required files, interfaces, and acceptance criteria.
- Define minimal implementation scope that satisfies AC.

3. Implement with testability in mind
- Add or update code in the target files.
- Keep changes scoped to ticket intent.

4. Validate acceptance criteria
- Run relevant checks (`tsc`, tests, lint, runtime checks).
- Record AC status as pass/fail with evidence.

5. Report completion
- Summarize files changed, behavior added, test results, and remaining risks.

## Output format
1. `Selected ticket and dependency status`
2. `Implementation summary`
3. `AC verification checklist`
4. `Residual risks`

## References
- Read `references/ticket-delivery-workflow.md` for AC-first execution template.
- Use these repo sources:
- `planning/TICKETS.md`
- `planning/IMPLEMENTATION_PLAN.md`
- `docs/SYSTEM_OVERVIEW.md` (feature-to-ticket mapping)
