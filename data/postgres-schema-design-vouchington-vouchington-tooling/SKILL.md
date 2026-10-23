---
name: postgres-schema-design
description: Design PostgreSQL names, relations, history, work queues, and cursors.
---

# PostgreSQL schema design

Read applicable `AGENTS.md` and the repository's local database adapter when present.
Local policy overrides these portable conventions.

- Names explain the stored thing; read [naming](references/naming.md) when naming schema objects.
- Columns say their type and FK target; finite sets use enums or lookup tables.
- Joined identities use foreign keys; read [relations](references/relations.md) before modeling references.
- Split differing shapes, share identical values, and keep history documents as JSON.
- Use canonical [table shapes](references/table-shapes.md) for revisions, changes, work, and cursors.
- Reuse parameterized trigger functions instead of copying bodies.
- Comment every table, column, and view; document reviewed exceptions explicitly.

For query shape, read [performance patterns](../postgres-node-performance-tuning/references/performance-patterns.md).
For partition lifecycle, use [UUIDv7 partitioning](../postgres-partitioning-uuid-v7/SKILL.md).
For how jobs choose, cap, and resume over work-item and cursor tables, read
[bounded iteration](../bounded-iteration/SKILL.md).
Consumer policy owns lifecycle, retention, migration strategy, and enforcement configuration.
