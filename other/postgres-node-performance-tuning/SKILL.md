---
name: postgres-node-performance-tuning
description: Measure and improve PostgreSQL queries in Node.js services.
---

# PostgreSQL and Node.js performance

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/postgres-node-performance-tuning/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Measure the query plan and the workload shape before changing code.

- Select only the required columns.
- Bound each result set. Paginate or stream a large read. A stream bounds memory, not work: cap
  the rows per run as in [bounded iteration](../bounded-iteration/SKILL.md).
- Batch writes inside an explicit transaction limit.
- Keep connection-pool usage bounded.
- Validate a query change at representative cardinality. Watch latency, memory, lock time, and
  connection pressure together.
- Cut round trips: fold dependent reads, batch per-item lookups, and overlap independent reads; see
  [round trips](references/performance-patterns.md#round-trips).
- Read the plan for hidden per-row work before trusting a change; see
  [reading plans](references/reading-plans.md).
- Read [performance patterns](references/performance-patterns.md) before changing a high-volume
  path.

Consumer wrapper owns: schema ownership, operational thresholds, pooling configuration, and rollout.
