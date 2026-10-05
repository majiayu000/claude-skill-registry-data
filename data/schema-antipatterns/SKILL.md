---
name: schema-antipatterns
description: This skill should be used when the user mentions "schema design", "database anti-pattern", "N+1", "foreign key index", "normalization", "data types", "constraints", "ORM performance", "missing primary key", "VARCHAR 255", "boolean as int", or reviewing DDL/models for design problems. It provides a relational schema design anti-pattern catalog plus a per-ORM N+1 pattern library.
---

# Schema Antipatterns

## Purpose
Provide a standardized catalog of relational schema design anti-patterns and ORM query anti-patterns, so schema reviews and N+1 hunts are consistent and grounded, statically, from DDL and source, with no database connection. These are the recurring mistakes that a DBA would flag on sight and that a team without one re-introduces every sprint.

## Schema anti-pattern catalog

| Category | Anti-pattern | Why it bites | Correct choice |
|---|---|---|---|
| Keys | No primary key | No stable row identity; replication/tooling breaks | Surrogate `bigint`/`identity` or `uuid` PK |
| Keys | UUID stored as `varchar(36)` | 2–3× storage, slow joins | `uuid` (PG) / `BINARY(16)` (MySQL) |
| Foreign keys | FK column with no index | Every parent delete/join scans the child | Index every FK column |
| Foreign keys | Relationship with no FK constraint | Orphan rows, no referential integrity | Declare the FK (+ `ON DELETE` action) |
| Types | Money as `float`/`double` | Rounding errors on cents | `numeric(12,2)` / `DECIMAL` |
| Types | `timestamp` without time zone | Ambiguous instants across zones/DST | `timestamptz` (PG) / store UTC + document |
| Types | Cargo-cult `VARCHAR(255)` | Arbitrary cap, no real meaning | `text` (PG) or a length that models a real rule |
| Types | Enum as loose `varchar` | Typos, no validation | Native `ENUM`/`CHECK`-constrained or lookup table |
| Types | Boolean as `int`/`char(1)` | `2` and `'Y'` sneak in | Native `boolean` / `TINYINT(1)` with `CHECK` |
| Constraints | Nullable-everything | NULL means "unknown" everywhere; buggy logic | `NOT NULL` on required columns |
| Constraints | Missing `UNIQUE`/`CHECK` | Duplicate/invalid data | Add the business-rule constraint |
| Indexing | Over-indexing / duplicate index | Write amplification, wasted storage | One index per access pattern; drop prefixes |
| Indexing | Index on low-selectivity boolean | Rarely used, still maintained | Partial index or none |
| Integrity | Soft-delete without partial unique | `UNIQUE(email)` blocks re-signup after delete | `UNIQUE ... WHERE deleted_at IS NULL` |

## Severity guidance
- **Critical**: data-loss/integrity, money as float, missing PK, missing FK on a real relationship.
- **High**: correctness/perf, unindexed FK, missing `NOT NULL`, wrong time type.
- **Medium**: maintainability, `VARCHAR(255)`, duplicate index, enum-as-string.
- **Low**: style/naming, inconsistent casing, non-standard plurals.

## ORM N+1 in one line
An N+1 is: a query returns N rows, then code touches a **lazy** relation once per row → 1 + N queries. The fix is always to eager-load or batch the relation before the loop. The exact call differs per ORM, see the reference.

## Additional Resources
### Reference Files
- **`references/schema-checklist.md`**: the full review checklist: types, keys, constraints, indexing FKs, normalization vs denormalization trade-offs, timestamps/time zones, soft-delete, and naming conventions.
- **`references/orm-n1-patterns.md`**: per-ORM: the exact code shape that causes an N+1 and the exact eager-loading fix for Django, SQLAlchemy, ActiveRecord, Sequelize, Prisma, TypeORM, Hibernate/JPA, GORM, and Entity Framework.
