---
name: database-schema-design
description: Use when designing a database from scratch, reviewing tables, an ERD, a Prisma/TypeORM/JPA/Django/SQLAlchemy schema or SQL migrations, adding indexes, normalizing data, or making a migration safe for production — Postgres, MySQL or SQLite.
---

# Database Schema Design

## Overview

A good schema makes invalid data impossible and common queries fast. Push rules into constraints, derive indexes from real access patterns, and never ship a migration that locks or loses data.

## Designing from scratch

1. **Entities and relationships.** List nouns, their cardinality (1:1, 1:N, N:M) and ownership. N:M gets a join table.
2. **Keys.** Surrogate primary key (bigint identity or UUIDv7). Natural uniqueness becomes a `UNIQUE` constraint, not the PK.
3. **Columns.** Right type, `NOT NULL` by default, defaults where sensible. See the type table.
4. **Constraints.** Foreign keys with explicit `ON DELETE`, `UNIQUE`, `CHECK`, enums or lookup tables for closed sets.
5. **Access patterns → indexes.** Write the top 5-10 queries first; index their `WHERE`, `JOIN` and `ORDER BY` columns.
6. **Lifecycle.** `created_at`, `updated_at`; soft delete only if the product needs restore or audit.
7. **Migration plan** (below).

## Reviewing an existing schema

Check every table against [checklist.md](checklist.md). Read the queries in the code too: a schema is only "wrong" relative to how it is used.

## Type choices

| Data | Use | Avoid |
|---|---|---|
| Money | `numeric(12,2)` or integer cents + currency | `float`, `double`, `real` |
| Timestamps | `timestamptz` (Postgres) / UTC `datetime` | local time without zone |
| Closed set of values | enum or FK to lookup table + `CHECK` | free-text strings |
| Email | `citext` or lower-cased + `UNIQUE` | case-sensitive unique |
| Booleans | `boolean NOT NULL DEFAULT false` | nullable tri-state by accident |
| Text | `text` with `CHECK (length(...))` if limits matter | `varchar(255)` everywhere by habit |
| JSON | `jsonb` for truly flexible attributes only | JSON for data you filter or join on |

## Safe migrations

- Add columns as nullable or with a constant default; backfill in batches; then add `NOT NULL`.
- Create indexes concurrently (`CREATE INDEX CONCURRENTLY` / online DDL).
- Renames and drops: expand (add new) → migrate code and data → contract (drop old) across releases.
- Never drop a column or table in the same release that stops writing to it.

## Output contract

```
### [Data integrity | Performance | Migration risk | Design] Title
- Where: table.column (file:line)
- Problem: the bad data or slow query this allows
- Fix: exact DDL or schema change
```

Order by risk: data loss and integrity first, then performance, then design. When designing, deliver the full DDL or ORM schema plus the index list mapped to the queries it serves.

## Common mistakes

- Missing indexes on foreign key columns (Postgres does not create them).
- Uniqueness enforced only in application code: races create duplicates.
- Polymorphic `owner_type` + `owner_id` with no referential integrity.
- Adding an index for every column instead of for actual queries.
- Reviewing the schema without reading the queries that use it.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
