---
model_tier: medium
name: database
description: "Use when working with database architecture, MariaDB/MySQL tuning, indexing strategies, slow queries, or multi-connection patterns — even when the user just says 'this query is slow'."
personas:
  - eloquent-tamer
domain: engineering
workspaces:
  - engineering
packs:
  - engineering-base
---

# database


> **Grounded corpus (Tier-1 consultation):** symptom → index/strategy
> decisions come grounded — `./scripts-run
> <skills-root>/corpus-grounding/scripts/ground search --manifest
> <skills-root>/database/data/manifest.json "<symptom>"` returns root
> cause, strategy, good-code sketch, anti-pattern, and the verification
> probe (EXPLAIN expectation). Corpus:
> [`data/query-tuning.csv`](data/query-tuning.csv) (PostgreSQL 16 /
> MySQL 8-derived).

## When to use

Use when designing schemas, optimizing queries, adding indexes, or troubleshooting database performance.

Do NOT use when:
- Writing framework-specific ORM models (use the matching skill — e.g. `eloquent` for Laravel, `symfony-workflow` for Doctrine, framework-native skill for Prisma / TypeORM / SQLAlchemy / GORM / Diesel)
- Creating migrations only — use the framework-specific migration skill (`laravel-migration` for Laravel, framework-native for others)

## Procedure: Optimize a query

### Step 0: Inspect

1. Read project docs in `agents/reference/docs/` for database architecture.
2. Check `config/database.php` for connection definitions.
3. Detect engine: check `.env` driver and `docker-compose.yml`.

### Step 1: Diagnose

Run `EXPLAIN` / `EXPLAIN ANALYZE`:

```sql
EXPLAIN ANALYZE SELECT * FROM projects WHERE customer_id = 42 AND status = 'active';
```

Check for: full table scans (`type=ALL`), missing indexes (`key=NULL`), filesort, temporary tables.

### Step 2: Fix

- Add missing indexes (most selective column first in composites)
- Rewrite anti-patterns (subquery → JOIN, `OFFSET` → cursor, `SELECT *` → specific columns)
- Add eager loading for N+1 queries
- Always paginate list endpoints

### Step 3: Verify

Re-run `EXPLAIN` and confirm improved plan.

## Schema awareness (anti-hallucination)

**Never guess table or column names.** Verify before writing queries/migrations:

1. **Read migrations** — source of truth
2. **Read models** — `$table`, `$connection`, `$fillable`, `$casts`, relationships
3. **Run schema queries** — use the project's REPL or a raw introspection query:
   - Laravel: `php artisan tinker --execute="Schema::getColumnListing('table')"`
   - Symfony / Doctrine: `bin/console doctrine:mapping:info`
   - Rails: `bin/rails runner "p ActiveRecord::Base.connection.columns('table').map(&:name)"`
   - Prisma: `npx prisma db pull --print | grep -A20 "model Table"`
   - Generic SQL: `psql -d mydb -c "\d table"` / `mysql -e "DESCRIBE table"`
4. **Check project docs** — `agents/reference/docs/` for conventions

| Trap | Reality |
|---|---|
| Assuming column exists | Check migration/model first |
| Wrong table prefix | Customer tables may have prefixes |
| Wrong connection | `api_database` vs `customer_database` — verify |
| Inventing pivot tables | Check if they actually exist |

### Dump to the Evidence Report (source-discovery)

When the task touches schema-driven work, this dump **is** the DB surface of the
[`source-discovery`](../source-discovery/SKILL.md) discipline. Record it to the
gitignored session cache with provenance, framework-neutral (MySQL / Postgres /
SQLite; ORM-agnostic):

- Capture **tables, columns, types, primary/foreign/unique keys, indexes,
  relations**, and the derived **filter/sort/group-ability** — each with
  `observed_at` / `source` (`migration:line` or the introspection command).
- **In-codebase = local, read fresh, no card.** A schema defined by repo
  migrations / models / ORM / app code (including schemaless stores the app
  controls — Mongoose / Prisma / Firestore rules) is always resolved locally and
  re-read each task. The **migration is intended truth, the live DB is actual** —
  surface any divergence as a drift signal.
- **Only negative facts graduate to a committed card** (`agents/knowledge/`):
  "searched, column/table does not exist" after an exhausted search. Positive
  structure stays in the session Evidence Report, re-read fresh — never a card.
- A **DB-not-in-codebase** (vendor SaaS / partner / legacy, schema not in the
  repo and not app-controlled) is the only DB that may be card-worthy.

## Conventions

→ See guideline `php/database.md` for indexing, transactions, migrations, multi-connection patterns.

## Output format

1. Migration file or query change with EXPLAIN analysis
2. Index recommendations with rationale

## Gotcha

**MySQL and MariaDB share a query-syntax world. They never share a migration
one.** Treat them as one engine for writing a `SELECT`, and as two engines for
everything that changes a schema or reports on a plan: online-DDL semantics,
lock behavior under `ALTER`, feature availability, and `EXPLAIN` output all
diverge. Read the engine and its version from the project before making any
claim in that second group; where the project does not declare one, say the
engine is unknown rather than assuming.

- Check existing indexes before adding — duplicates waste write performance.
- Consider multi-tenant implications — queries may need customer DB scoping.
- `EXPLAIN` output varies between MariaDB and MySQL.
- Don't use `TEXT` in WHERE without prefix index.

## Do NOT

- Do NOT guess table/column names — verify against migrations or models first.
- Do NOT add indexes without checking existing ones — duplicates waste write performance.
- Do NOT use `float` for money — use `decimal`.

## Auto-trigger keywords

- database
- MariaDB
- MySQL
- migration
- indexing
- query optimization
