---
name: migrating-legacy-etl
description: Plan and execute migrations of legacy ETL and data warehouses — stored procedures, SSIS/Informatica, or on-prem warehouses to modern stacks (dbt, Spark, cloud warehouses) — using strangler-fig phasing, parallel runs, and row/aggregate reconciliation. Use when migrating legacy pipelines or warehouses, rewriting stored procedures into dbt/Spark, or validating a migration against the source system.
---

# Migrating Legacy ETL

## When to use

- Moving legacy ETL (stored procs, SSIS, Informatica, hand-rolled jobs) or an
  on-prem warehouse to a modern stack (dbt, Spark, cloud warehouse).
- Rewriting procedural transformations into set-based SQL/models.
- Validating that the new system matches the old before cutover.
- Do NOT use for greenfield pipelines (use the building/authoring skills).

## Workflow

```
- [ ] Inventory jobs, dependencies, and consumers; find what is actually used
- [ ] Migrate incrementally (strangler fig), not big-bang
- [ ] Rewrite procedural logic into set-based, idempotent transformations
- [ ] Run old and new in parallel; reconcile outputs
- [ ] Cut over per domain once reconciliation passes; decommission the old path
```

1. **Inventory and triage.** Map every job, its dependencies, and its downstream
   consumers. Many legacy jobs are dead or duplicated — don't migrate what nobody
   uses.
2. **Strangler-fig phasing.** Migrate one domain/table at a time, redirecting
   consumers as each piece is proven. Big-bang cutovers fail.
3. **Rewrite, don't transliterate.** Convert row-by-row cursors/procedures into
   set-based, idempotent SQL/models — a literal port keeps the old bottlenecks.
4. **Parallel run + reconcile.** Run old and new side by side and compare row
   counts, key sets, and aggregate sums until they match within tolerance.
5. **Cut over gradually** and decommission the legacy path only after
   reconciliation holds.

## Patterns

**Reconciliation harness** — compare old vs new for the same window:

```sql
SELECT 'row_count' metric, (SELECT COUNT(*) FROM legacy.fct_orders) legacy,
                           (SELECT COUNT(*) FROM new.fct_orders)    new_
UNION ALL
SELECT 'sum_amount', (SELECT SUM(amount) FROM legacy.fct_orders),
                     (SELECT SUM(amount) FROM new.fct_orders);
```

Investigate every non-matching metric; differences are usually NULL handling,
timezone, rounding, or dedup logic that the legacy system did implicitly.

**Capture business rules** buried in procedures as tested dbt models with
descriptions, so tribal logic becomes documented and version-controlled.

## Common pitfalls

- **Big-bang cutover** — high risk, no rollback; migrate domain by domain.
- **Literal transliteration** — porting cursors/temp-table hops keeps legacy
  inefficiency; re-express as set-based logic.
- **No parallel-run reconciliation** — subtle logic differences ship as data bugs;
  compare counts/sums before trusting the new path.
- **Migrating dead jobs** — wasted effort; verify each job has real consumers.
- **Losing implicit rules** — legacy handling of NULLs/timezones/dedup is often
  undocumented; reconcile to surface and encode it.
- **No decommission step** — old and new both run forever, doubling cost and
  confusion.
