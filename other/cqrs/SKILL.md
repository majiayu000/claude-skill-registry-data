---
name: cqrs
description: Pragmatic CQRS levels (separate methods, separate models, separate stores) and how to implement each in .NET with EF Core writes and Dapper/views/stored-procedure reads on SQL Server, including projections, outbox-driven read models, consistency expectations and when not to use CQRS. Use when implementing any query slice, list/report/search screens, read performance problems, read models, or when the module profile has cqrs other than none.
user-invocable: false
---
# CQRS — pragmatic levels

| Level | Write side | Read side | Consistency | Use when |
|---|---|---|---|---|
| **separate-methods** (CQS) | handler mutates, returns id/Result | handler returns data, never mutates | immediate | default for every module |
| **separate-models** | aggregates via EF Core | projections straight from the DB to response DTOs (EF `Select`/`AsNoTracking`, Dapper, views, SPs) | immediate (same DB) | domain-model modules; any list/search screen |
| **separate-stores** | aggregates + outbox | dedicated read tables/other store updated by projectors | eventual | measured read load, reporting isolation, heavy denormalization |

## Rules (all levels)
1. A query never loads an aggregate and never calls `SaveChanges`.
2. A command never returns a read model larger than an id + minimal status.
3. Read models are owned by the slice that needs them; do not build a shared "InvoiceDto".
4. Authorization filters apply to reads too (row-level: tenant, company, user scope) — inside the query.

## separate-models on SQL Server
- Simple lists/details: EF Core `AsNoTracking().Where().Select(x => new Response(...))`.
- Complex reads (many joins, aggregation, window functions): Dapper + SQL in the slice, or a module-owned
  view `{schema}.{Name}View`; SPs when execution-plan stability or security (EXECUTE-only) matter.
- Paging: keyset (`WHERE (Date, Id) < (@LastDate, @LastId)`) for large/infinite lists; OFFSET only for
  small bounded sets with a total count.
- Indexes are designed for the read queries; list them in the plan.

## separate-stores
1. Write side emits domain events → outbox (same transaction).
2. Projector (background service) reads outbox/integration events in order → upserts read tables
   (`reporting.InvoiceFacts`). Idempotent by event id; track position per projector.
3. Read handlers query only read tables.
4. **Consistency contract** is explicit in the UI/API: after a command, either return the new version
   number and poll, or read-your-writes from the write model for that one entity.
5. Rebuild procedure exists: truncate + replay from source tables or event history. Test it.

## When not to
- CRUD module with forms mirroring tables → separate-methods only.
- "We might need to scale reads" without numbers → no separate stores.
- Team cannot operate eventual consistency (support, UI patterns) → stay at separate-models.

## Review checklist
- [ ] Query handlers free of tracking, aggregates, SaveChanges
- [ ] Every read query has index support or a stated reason
- [ ] Read-side authorization applied in SQL, not after materialization
- [ ] Projectors idempotent, ordered, rebuildable (separate-stores only)
