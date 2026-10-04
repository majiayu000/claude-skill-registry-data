---
name: modeling-dimensional-data
description: Design analytics data models using dimensional modeling — star and snowflake schemas, fact and dimension tables, grain declaration, surrogate keys, and slowly changing dimensions (SCD Type 1/2/3). Use when designing a warehouse schema, building marts, choosing a table grain, tracking history, or deciding fact vs dimension.
---

# Modeling Dimensional Data

## When to use

- Designing warehouse/mart tables for analytics or BI.
- Deciding a table's grain, or whether something is a fact or a dimension.
- Tracking attribute history over time (customer moved, product re-priced).
- Do NOT use for OLTP/application schema design (normalize instead).

## Workflow

```
- [ ] Pick the business process to model
- [ ] Declare the grain (one row = ...)
- [ ] Identify the dimensions (context: who/what/where/when)
- [ ] Identify the facts (numeric measures at that grain)
- [ ] Choose SCD behavior per dimension attribute
- [ ] Add surrogate keys and relationships
```

1. **Choose the process** (orders, sessions, payments) — one star per process.
2. **Declare the grain first** and write it down: "one row per order line." Every
   fact column must be true at that grain. Never mix grains in one fact table.
3. **Dimensions** carry descriptive context and are the columns users filter/group
   by. **Facts** are additive numeric measures.
4. **Pick SCD type per attribute** (see below) based on whether history matters.
5. **Use surrogate keys** (warehouse-generated) as primary/foreign keys; keep the
   source natural key as a separate column.

## Patterns

**Star schema** — one central fact table with foreign keys to denormalized
dimensions. Prefer this default: fewer joins, faster BI, easier to understand.
**Snowflake schema** normalizes dimensions into sub-tables; use only when a
dimension is huge and shared, accepting more joins.

**Fact table types:**

- _Transaction_ — one row per event (most common).
- _Periodic snapshot_ — one row per entity per period (daily balances).
- _Accumulating snapshot_ — one row per process instance, updated as it progresses.

**SCD types (per attribute):**

- _Type 1_ — overwrite; no history. Use for corrections.
- _Type 2_ — add a new row with `valid_from`/`valid_to` + `is_current`; preserves
  full history. The default when history matters.
- _Type 3_ — add a `previous_value` column; keeps only the prior value.

```sql
-- SCD Type 2 dimension row shape
customer_key      BIGINT      -- surrogate key (unique per version)
customer_id       VARCHAR     -- natural/business key (stable across versions)
name              VARCHAR
region            VARCHAR
valid_from        TIMESTAMP
valid_to          TIMESTAMP   -- NULL or 9999-12-31 for the current version
is_current        BOOLEAN
```

Join facts to the dimension version that was current at the event time using the
surrogate key captured at load time, not the natural key.

## Common pitfalls

- **Undeclared or mixed grain** — the root cause of double-counting. Declare it
  and enforce it with a uniqueness test.
- **Joining facts on natural keys** — breaks under SCD Type 2; join on the
  surrogate key resolved at event time.
- **Non-additive measures stored as additive** (ratios, percentages) — store the
  numerator and denominator, compute the ratio at query time.
- **Overusing snowflaking** — normalizing every dimension adds joins for little
  benefit in a columnar warehouse.
- **Nulls in dimension foreign keys** — use a dedicated "unknown" dimension row
  (key = -1) instead of NULL so joins stay inner and counts stay correct.

## References

- [SCD implementation patterns](references/SCD.md)
