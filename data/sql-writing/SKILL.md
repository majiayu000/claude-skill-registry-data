---
model_tier: medium
name: sql-writing
description: "Use when writing raw SQL — MariaDB/MySQL syntax, parameterization, raw migrations, seeders with `DB::statement`; fires even on a pasted query asking 'why is this slow'."
domain: engineering
workspaces:
  - engineering
packs:
  - engineering-base
---

# sql


> **Grounded corpus:** tuning decisions (indexes, keyset pagination,
> N+1, trigram search, lock contention) ground via the
> [`database`](../database/SKILL.md) corpus — `./scripts-run
> <skills-root>/corpus-grounding/scripts/ground search
> --manifest <skills-root>/database/data/manifest.json "<symptom>"`.

## When to use

Use when writing or reviewing raw SQL queries, migrations with raw statements, or seeders with raw SQL.

Do NOT use when:
- Eloquent/Query Builder queries (use `eloquent` or `database` skill)
- Schema design (use `database` skill)

## Procedure: Write raw SQL

1. **Inspect call site & choose approach** — identify every dynamic value flowing into the query, then pick: query builder when possible. Raw SQL only when query builder can't express the query.
2. **Parameterize** — Every variable must use `?` binding or named `:param`. Never interpolate PHP variables into SQL strings.
3. **Read the engine, then choose the syntax** — check, in order: the project's DB config (`config/database.php` default connection, `DB_CONNECTION`), a `docker-compose.yml` service image, a migration using engine-specific syntax. MySQL and MariaDB share the query-syntax world this skill writes in; PostgreSQL and MSSQL do not. **If none of those declare an engine, say so and ask — do not assume one.** A query written for the wrong engine passes review and fails in production.
4. **Verify** — Run EXPLAIN on complex queries. Check that no PHP interpolation (`"$var"`, `'{$var}'`) appears in SQL.

```
NEVER build SQL strings with PHP variable interpolation or concatenation.
ALWAYS use parameterized queries or query builder.
```

## Conventions

→ See guideline `php/sql.md` for parameterization patterns, common mistakes, MariaDB syntax reference.

## Quick reference

```php
// ✅ Safe
DB::select('SELECT * FROM users WHERE email = ?', [$email]);

// ❌ SQL injection
DB::select("SELECT * FROM users WHERE email = '{$email}'");
```

### Validate

1. Verify every variable in SQL uses parameter binding (`?` or named `:param`).
2. Confirm MariaDB/MySQL syntax — not PostgreSQL or MSSQL.
3. Run EXPLAIN on complex queries to check index usage.
4. Check that no PHP variable interpolation (`"$var"`, `'{$var}'`) appears in SQL strings.

## Output format

1. Parameterized SQL query using MariaDB/MySQL syntax
2. EXPLAIN output for performance-critical queries

## Gotcha

**MySQL and MariaDB share a query-syntax world. They never share a migration
one.** Same principle as `database`: one engine for writing a `SELECT`, two for
online-DDL semantics, lock behavior under `ALTER`, feature availability and
`EXPLAIN` output. Never carry a claim from the second group across the two
without naming the engine and version it was measured on.

- MariaDB and MySQL have subtle syntax differences.
- The model writes `$variable` in SQL strings instead of `?` placeholders.
- `GROUP BY` with `ONLY_FULL_GROUP_BY` requires all non-aggregated columns.
- Use SQL types (`NULL`, `1/0`, `JSON_ARRAY()`) — not PHP equivalents.

## Do NOT

- Do NOT interpolate PHP variables into SQL strings — always parameterize.
- Do NOT use PHP syntax (arrays, booleans, null) in raw SQL — use SQL equivalents.
- Do NOT write raw SQL when the query builder can express the same thing clearly.

## Auto-trigger keywords

- raw SQL
- SQL query
- parameterized query
- MariaDB syntax
- SQL injection
