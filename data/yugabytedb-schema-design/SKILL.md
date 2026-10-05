---
name: yugabytedb-schema-design
description: >
  Best practices for designing high-performance YugabyteDB schemas from scratch or optimizing
  existing ones. Covers hash vs range sharding decisions, avoiding write hotspots on sequential
  columns, partial indexes for nullable or skewed columns, low-cardinality index design, covering
  indexes, primary key selection, foreign key index requirements, and redundant index cleanup.
  Use this skill whenever the user asks how to design a YugabyteDB schema, choose a sharding
  strategy, avoid hotspots, optimize indexes, handle NULL-heavy columns, model a table for
  distributed SQL, or asks "how should I structure this in YugabyteDB". Trigger even when the
  user mentions "YugabyteDB indexes", "YSQL schema", "tablet hotspot", "sharding key", or asks
  why their YugabyteDB writes are slow or skewed.
---

# YugabyteDB Schema Design Best Practices

This skill covers **how to design schemas well** for YugabyteDB. The design patterns that make a schema performant in a distributed SQL environment.

## Core Concepts (Read First)

YugabyteDB is an index-organized, distributed SQL database. Every design decision flows from
three foundational facts:

1. **The primary key IS the table.** Rows are stored sorted by PK. No PK = system assigns `ybrowid` (hidden, hash-sharded).
2. **Default sharding is HASH.** Data is distributed by hashing the sharding key across tablets. Great for point lookups, bad for range queries.
3. **Tablets split automatically, but hotspots happen.** Sequential values (timestamps, auto-increment IDs) written to a range-sharded index concentrate all writes on one tablet until it splits.

## Reference Files

Read only the section(s) relevant to the user's question:

- `references/sharding.md` — Hash vs range, when to use each, choosing a sharding key
- `references/hotspots.md` — Preventing write/read hotspots on timestamps and monotonic PKs
- `references/index-design.md` — Index column ordering, covering indexes, redundant indexes
- `references/partial-indexes.md` — Partial indexes for NULL-heavy and skewed-value columns
- `references/low-cardinality.md` — Avoiding poor distribution from boolean/ENUM/low-distinct sharding keys
- `references/primary-keys.md` — PK selection, explicit PKs, composite PKs for partitioned tables
- `references/foreign-keys.md` — FK type alignment, mandatory FK indexes

## Quick Decision Guide

| User's question | Go to |
|---|---|
| "Should I use hash or range sharding?" | `sharding.md` |
| "My timestamp writes are all going to one tablet" | `hotspots.md` |
| "How do I index this column?" | `index-design.md` |
| "Half my rows have NULL in this column" | `partial-indexes.md` |
| "Indexing a status/boolean column" | `low-cardinality.md` |
| "What should my primary key be?" | `primary-keys.md` |
| "FK performance is slow" | `foreign-keys.md` |
| "Can you design schema for this?" | `Refer all the files for the optimal design` |
| "Can you optimize this schema?" | `Refer all the files for the optimal design` |

## Golden Rules at a Glance

```
✅ Always define an explicit PRIMARY KEY
✅ Use ASC/DESC on index columns that are range-queried
✅ Put high-cardinality columns first in multi-column indexes
✅ Index every foreign key column in child tables
✅ Use partial indexes for nullable or skewed columns
✅ Match FK column types exactly (INT vs BIGINT matters)
✅ Drop redundant indexes (prefix-covered by another index)
✅ Use text datatype whereever possible instead of VARCHAR(n)

❌ Never use a low-cardinality column as the sole sharding key
❌ Never range-shard on a monotonically increasing column without a synthetic shard key
❌ Never leave tables without a PK if UNIQUE NOT NULL columns exist
❌ Never create multi-column GIN indexes
```
