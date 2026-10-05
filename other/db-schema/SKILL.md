---
name: db-schema
description: Apply when designing database schemas, writing migrations, or reviewing table structure. Covers naming, keys, indexes, constraints, nullability, and migration safety.
license: MIT
version: 1.0.0
tokens_target: 1900
triggers:
  - database schema
  - migration
  - table design
loads_after: []
supersedes: []
---

# Sub-Skill: Database Schema Design
<!-- target: tokens_target above. Run `python tools/render_readme_table.py` to update README. -->

**Purpose:** Prevent data-integrity bugs, race conditions, and irreversible migrations by enforcing database-level constraints and safe migration patterns before code reaches production.

---

## Rules

### Naming Conventions

1. **Snake case everywhere.** Always use `snake_case` for table names, column names, and index names; never use camelCase or PascalCase in SQL identifiers.
2. **Plural table names.** Always name tables in the plural (`users`, `orders`, `line_items`); singular names cause inconsistency across ORMs and query builders.
3. **Consistent FK column naming.** Always name foreign-key columns `<referenced_table_singular>_id` (e.g., `user_id`, `order_id`) so the reference is self-documenting.

### Primary Keys

4. **Surrogate primary key.** Always define an explicit surrogate primary key (`id`) on every table; never rely on natural keys as the sole PK unless the domain guarantees immutability.
5. **UUID vs serial.** Prefer `uuid` PKs for distributed systems or public-facing IDs; prefer `bigserial` / `bigint GENERATED ALWAYS AS IDENTITY` for high-insert internal tables where sort order matters.

### Foreign Keys & Referential Integrity

6. **Declare FK constraints.** Always declare `FOREIGN KEY` constraints in the schema; never rely on application-layer join logic to enforce referential integrity.
7. **Explicit ON DELETE behaviour.** Always specify `ON DELETE` behaviour (`CASCADE`, `SET NULL`, or `RESTRICT`) on every FK; omitting it defaults to `RESTRICT`, which can cause surprising errors at runtime.
8. **Missing FK is a data-integrity bug.** Never ship a column that references another table without a corresponding FK constraint — orphaned rows accumulate silently. Reference: ERR-2026-022

### Indexes

9. **Index every FK column.** Always add an index on every foreign-key column; unindexed FKs cause full-table scans on joins and cascade operations.
10. **Covering indexes for hot queries.** Use covering indexes (include all columns in the `SELECT`) for read-heavy queries rather than adding redundant columns to the base table.
11. **Unique constraints at DB level.** Always enforce uniqueness at the database level rather than relying on application-layer deduplication; race conditions between concurrent writes bypass app checks. Reference: ERR-2026-022

### Nullability & Defaults

12. **Explicit NOT NULL.** Always mark columns `NOT NULL` unless `NULL` carries distinct semantic meaning (unknown vs. absent); nullable columns complicate query logic and ORM mapping.
13. **Meaningful defaults.** Always supply a `DEFAULT` for columns that have a sensible zero-value (`0`, `''`, `false`, `now()`); avoid forcing callers to supply values the DB can compute.

### Timestamps & Soft Delete

14. **Standard audit columns.** Always include `created_at TIMESTAMPTZ NOT NULL DEFAULT now()` and `updated_at TIMESTAMPTZ NOT NULL DEFAULT now()` on every table; omitting them makes debugging and auditing impossible.
15. **Soft delete with deleted_at.** Prefer `deleted_at TIMESTAMPTZ` over hard deletes for user-facing entities; ensure all queries filter `WHERE deleted_at IS NULL` or use a view/partial index.

### Enum Columns

16. **DB-native enum or check constraint.** Always enforce enum-like columns with a `CHECK` constraint or a native `ENUM` type; never store unconstrained strings and validate only in the application.

### Migrations

17. **Up and down migrations.** Always write both an `up` and a `down` migration; a rollback path is mandatory before any migration reaches production.
18. **Idempotent migrations.** Always guard DDL statements with `IF NOT EXISTS` / `IF EXISTS` so re-running a migration does not error; this is required for blue-green and multi-replica deployments.
19. **Non-blocking index creation.** Use `CREATE INDEX CONCURRENTLY` (Postgres) or equivalent for indexes on large tables; blocking index creation causes downtime.

### Constraints Over App Logic

20. **Check constraints for invariants.** Always encode business invariants (e.g., `price > 0`, `quantity >= 0`) as `CHECK` constraints; application-layer validation is bypassed by direct DB writes, scripts, and migrations.

---

## See also

- `skills/code-quality/SKILL.md` — general code-quality rules that apply to migration scripts
- `skills/review-deployment/SKILL.md` — deployment checklist that includes migration safety gates

---
