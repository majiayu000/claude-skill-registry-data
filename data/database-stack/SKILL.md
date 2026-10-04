---
name: database-stack
description: Database implementation guidance for schema design, migrations, queries, indexing, and rollout safety.
compatibility: opencode
metadata:
  audience: database-engineers
  purpose: stack-guidance
---
## Focus areas

- Treat schema and data changes as operational changes.
- Prefer additive, phased migrations when possible.
- Watch query shape, index tradeoffs, and lock behavior.
- Design backfills and repair paths to be resumable and idempotent.
- Keep application changes and data changes sequenced safely.

## Guardrails

- Call out expensive migrations, risky rollouts, and data consistency assumptions.
- Avoid destructive changes without a clear deployment and rollback plan.
- Be explicit about coordination between code deploys and data changes.
