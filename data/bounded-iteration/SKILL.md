---
name: bounded-iteration
description: Bound the rows each run reads when writing or reviewing scheduled jobs, reconcilers, cleanups, dispatchers, backfills, exports, list endpoints, or any loop that reads rows.
---

# Bounded iteration

Read applicable `AGENTS.md` and the repository's local database adapter when present.
Local policy overrides these portable conventions.

A run's cost is the rows it reads and the work it starts, not the memory it holds. Read
[sweep patterns](references/sweep-patterns.md) for worked SQL and loop shapes.

1. **Choose work, not entities.** Read only rows that need work, through a predicate an index
   serves: a work-item or dirty-marker row, a parent id, a due timestamp with a partial index, or
   a time or UUIDv7 window past a high-water mark. Column-to-column comparisons, `OR` of unrelated
   conditions, and `EXISTS` as the only condition are not filters. (`postgres-required-predicates`)
   A per-row threshold becomes one bucket per distinct value, comparing the stored fact with a
   bound, never with another column; `timestamptz + interval` is not immutable, so it cannot be
   indexed. See [per-row interval](references/sweep-patterns.md#per-row-interval-one-bucket-per-threshold)
   and [age milestones](references/sweep-patterns.md#age-milestones-from-the-uuidv7-key).
2. **Cap every run.** Every loop has a per-run cap (batches, rows, or a deadline), reports whether
   work remains, and resumes from a persisted position. Never loop until empty, and never default
   a cap to infinity.
3. **Bound every statement.** A SELECT, UPDATE, or DELETE that can touch many rows has a `LIMIT`.
   For writes the `LIMIT` goes in a CTE, with `FOR UPDATE SKIP LOCKED` when workers compete.
   (`postgres-lock-ordering`)
4. **A stream is not a bound.** A cursor or stream bounds memory, not work. Cap the rows streamed
   per run.
5. **Resume without restarting.** Keep a keyset position on the UUIDv7 key or a
   `<verb>_through_at` time position, fix the sweep's end when it starts, and rescan an overlap
   when insert order differs from commit order. Cursor tables follow
   [table shapes](../postgres-schema-design/references/table-shapes.md).
   (`postgres-generated-column-predicates`)
6. **No unbounded fan-out.** Use `Promise.all` only over a bounded result, with bounded
   concurrency.
7. **Keyset pagination.** No `OFFSET`. Clamp the client's page size on the server. The API schema
   keeps a static ceiling; the default and the effective maximum are runtime-tunable but never
   above it. (`postgres-no-offset`)
8. **Tunables are runtime configuration.** Batch sizes, page sizes, caps, and windows come from
   the consumer's runtime configuration with a validated default and a hard maximum, and are bound
   as SQL parameters. `LIMIT 1` and an external API's page maximum are contracts, not tunables.
9. **One dispatcher per signal.** Split an `OR` of unrelated reasons into one dispatcher per
   reason, each with its own index-served predicate, position, and schedule, all enqueuing the same
   idempotent job. Writes that cause a signal enqueue directly; the sweep is the backstop. See
   [one dispatcher per signal](references/sweep-patterns.md#one-dispatcher-per-signal).
10. **Deduplicate jobs by entity and triggering event.** A job id keyed only by the entity drops a
    new trigger while the last job runs or is retained. Key it by entity and event; dedup lasts
    only while the record is retained, and a failed retained job still claims its id. See
    [queue job ids](references/sweep-patterns.md#queue-job-ids-for-deduplication).
11. **Repair through an existing reconciler.** Repeat a fire-and-forget side effect (cache fill,
    filter add, enqueue) idempotently from the reconciler that already sweeps recently changed
    rows. Do not add a sweeper. See
    [repair](references/sweep-patterns.md#repair-through-an-existing-reconciler).
12. **Membership filters are never rebuilt on a schedule.** Add on write, rebuild in full only on
    an operator action or a detected failure, and stop trusting the filter after a failed add.
    Deleted keys and growth only cost false positives. See
    [membership filters](references/sweep-patterns.md#membership-filters).
13. **Global rankings stay one periodic aggregate.** A result over every row needs every score;
    incremental per-row inputs move the cost to every write without freshening the ranking. Give
    the pass an EXPLAIN budget. See [global ranking](references/sweep-patterns.md#global-ranking).
14. **External listings carry the provider's continuation token.** Cap pages per run and enqueue a
    continuation with the token; restarting at page one lets failing front items starve the rest.
    See [external listing](references/sweep-patterns.md#external-listing-with-a-continuation-token).
15. **Verify with a plan.** EXPLAIN at representative cardinality shows no Seq Scan on an
    unbounded table, and an index that supplies the `ORDER BY`, so the scan stops at the
    `LIMIT` instead of reading and sorting every match. Compare rows read with rows returned.

For work-item, lease, and cursor tables, read [postgres-schema-design](../postgres-schema-design/SKILL.md).
For query shape and streaming, read [performance patterns](../postgres-node-performance-tuning/references/performance-patterns.md).
For UUIDv7 windows and pruning, use [UUIDv7 partitioning](../postgres-partitioning-uuid-v7/SKILL.md).
Names in parentheses are generic `jonathanong/no-mistakes` rules; check that the installed release
has one before relying on it. No generic rule checks run caps, streams, or fan-out.
Consumer policy owns run caps, tunable names and ceilings, schedules, and enforcement configuration.
