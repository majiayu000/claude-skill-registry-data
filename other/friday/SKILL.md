---
name: friday
description: Review a planned deployment or release diff for rollback feasibility, mixed-version compatibility, migrations, and configuration readiness without deploying it.
---

# Friday

> Can Monday-you undo this?

## Read Monday's incident report early

When discovery is needed, combine it with reading supplied release notes/contracts and available project instructions, then batch the discovered relevant inputs. Avoid a listing-only round trip when supplied inputs are already readable. Keep Git internals out of file discovery (for example, `rg --files --hidden -g '!.git'`); use Git commands for relevant history. Reopen files when changed, incomplete or needed for an unresolved question.

Use the release diff and documented rollout/rollback order to identify reachable states, old/new artifacts, configuration and consumers. Consult history for unresolved versions, contracts or ordering, not redundant commit metadata. Do not impose rolling deployment or zero downtime on another strategy.

For each reachable state, check active readers/writers against data and configuration, including new-version writes before rollback. Select witnesses from actual branches, representation boundaries and transitions; enumerate finite inputs only when value-dependent behavior or requested assurance warrants it. Reuse a pairing's evidence while code, inputs and relevant state remain unchanged: phase labels alone need no rerun, but changed data, configuration, effects or ordering require affected pairings to be rechecked. Include queued/external effects when their contract changes.

Combine compatible coverage obligations into representative sequences instead of multiplying every value by every version/operation. For latest-value contracts, existing representative records can undergo successive writes; retain distinct records when earlier payloads or interactions must survive. Check observations after each relevant transition and final recovery; expand combinations when branches, cross-record effects or requested assurance require them. Fewer witnesses must not mean reusing stale observations.

Code rollback is not data recovery: down migrations can lose data, and backups need restore evidence. Consider expand/migrate/contract when destructive schema changes must coexist with older consumers.

Find the first incompatible/irreversible step and last recoverable state; tie blockers to the smallest compatible ordering or prerequisite. Local SQL is not production-readiness evidence; staging requires authorization.

Choose execution from the contract: exercise actual application writers, transactions and connections when they matter. For repeated SQL-only SQLite reader checks, use the optional [in-memory matrix](references/sqlite-matrix.md); read its guide only for that path, and implementation for trust/adaptation/troubleshooting. Use existing runners for simple checks. The matrix cannot substitute for application/runtime evidence or another database engine.

## Deliver and stop

Lead with ready, ready with conditions, or blocked by evidence. Missing runtime/configuration evidence is unknown, not safe. Give each finding's step, failure, evidence and mitigation, not repeated full logs.

Stop when scoped compatibility and recovery paths are assessed; no generic infrastructure audit. Preserve user changes and requirements. Review does not authorize implementation, deployment, production migration, restore drills or publication. If asked to fix, verify the scoped correction without releasing it.
