---
name: building-ingestion-pipelines
description: Build batch and incremental data ingestion (extract-load) pipelines — full vs incremental extraction, change data capture (CDC), watermarks and high-water marks, API pagination and rate limits, and choosing managed EL tools (Fivetran, Airbyte) vs custom code. Use when ingesting data from databases, APIs, files, or SaaS into a warehouse/lake, or designing incremental extraction and CDC.
---

# Building Ingestion Pipelines

## When to use

- Extracting from databases, APIs, files, or SaaS into a warehouse/lake.
- Designing incremental extraction, watermarks, or CDC.
- Handling API pagination, rate limits, and retries.
- Deciding managed EL (Fivetran/Airbyte) vs custom code.
- Do NOT use for transforming already-landed data (use dbt/Spark skills).

## Workflow

```
- [ ] Decide extraction mode: full snapshot vs incremental vs CDC
- [ ] Pick a reliable high-water mark (updated_at, LSN/binlog, sequence)
- [ ] Land raw immutably (append), then transform downstream
- [ ] Make the load idempotent (upsert/partition overwrite by key)
- [ ] Handle pagination, rate limits, retries, and late data
```

1. **Choose the mode.** Full reload (small/dimension tables), incremental by a
   high-water mark (most fact tables), or CDC (high-volume OLTP where you need
   deletes and every change).
2. **Pick a trustworthy watermark.** `updated_at` only works if the source always
   updates it; otherwise use DB log positions (LSN/binlog/SCN) or a monotonic
   sequence. Store the last watermark and resume from it.
3. **Land raw immutably.** Append raw extracts (bronze) with load metadata; do
   transformations downstream so you can replay without re-pulling the source.
4. **Idempotent load.** Upsert by natural key or overwrite the partition, so
   retries and overlaps don't duplicate (see
   `writing-idempotent-transformations`).
5. **Be robust** to pagination, rate limits, and late data.

## Patterns

**Incremental extract with overlap for late data:**

```sql
-- Pull a small overlap window past the last watermark to catch late updates,
-- then upsert by key so the overlap does not create duplicates.
SELECT * FROM source.orders
WHERE updated_at >= :last_watermark - INTERVAL '3 days';
```

**CDC** — read the database log (Debezium/native) to capture inserts, updates, and
**deletes** (which watermark-based extraction misses). Apply changes with MERGE,
using the change's commit position for ordering.

**API pagination + rate limits** — follow cursor/next-page tokens; back off and
retry on 429/5xx with exponential backoff and jitter; checkpoint progress so a
failure resumes mid-stream.

**Managed vs custom** — use Fivetran/Airbyte for standard connectors (they handle
schema drift, incremental state, retries); write custom only for unusual sources
or strict control/cost needs.

## Common pitfalls

- **`updated_at` watermark when the source doesn't reliably set it** — silently
  misses rows; validate or switch to log-based CDC.
- **No overlap window** — late-arriving updates are lost between runs.
- **Watermark-based extraction expecting deletes** — it can't see them; use CDC or
  periodic full reconciliation.
- **Transforming during extraction** — makes replay impossible; land raw first.
- **Ignoring rate limits/pagination edge cases** — partial pulls that look
  complete; checkpoint and verify counts.
- **Non-idempotent load** — retries and overlap windows duplicate rows.
