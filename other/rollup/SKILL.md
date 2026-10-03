---
name: rollup
description: Coverage summary — per-scope, per-system, or per-migration-state breakdown of article + capability + functionality counts.
allowed-tools:
  - "mcp__bigweld__coverage_summary"
---

# /rollup [pivot]

Call `coverage_summary()` with the user's chosen pivot:
- `scope=<name>` for per-scope breakdown (e.g., `sfdc-internal`, `snow-target`, `migration-mapping`, `pan-hpe`)
- `system=<name>` for per-system breakdown (`sfdc`, `snow`, `manual`, `tbd`, `shared`)
- `migration_state=<name>` for per-state breakdown (`current`, `target`, `gap`, `deprecated`)

Present results as a 3-column table (Article / Capability / Functionality counts). Ask which pivot Alex wants if he didn't specify.
