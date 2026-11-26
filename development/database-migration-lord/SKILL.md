---
name: database-migration-lord
description: Lord skill for safe database migrations — Laravel migrations, schema design, zero-downtime deploys, MySQL/PostgreSQL/MariaDB compatibility.
triggers:
  - database migration lord
  - database migration
  - laravel migration
  - schema migration
  - zero downtime migration
  - migration safety
  - schema design
  - ترحيل قاعدة البيانات
  - هجرة database
personas:
  - DEV
  - DB
  - SRE
tech_stack:
  - laravel-13
  - mysql-9-7
  - postgresql-19
  - php-8-5
lord: true

---

# Database Migration Lord

[OBJ] Safe database migrations for Laravel 13 — schema design, zero-downtime deploys, MySQL/PostgreSQL/MariaDB compatibility, and migration safety checks.

[RULES]
1. [CMD] Query Context7 for Laravel database docs. Use `/laravel/framework` library ID with migration-specific questions.
2. [REQ] Zero-Downtime Migrations: NEVER run `DROP COLUMN` directly in production. Use 3-phase deploy: (1) add new column nullable, (2) deploy code that writes to both, (3) backfill + drop old column in next deploy.
3. [REQ] Index Creation: `CREATE INDEX CONCURRENTLY` on PostgreSQL (no table lock). On MySQL, use `ALGORITHM=INPLACE` where possible. NEVER create indexes on large tables during peak hours without concurrent option.
4. [REQ] Foreign Keys: Always add foreign key constraints. Name them explicitly (`fk_table_column_foreign`). Use `ON DELETE CASCADE` or `SET NULL` intentionally — NEVER default RESTRICT without documentation.
5. [REQ] Reversible Migrations: Every `up()` must have a `down()`. Test `down()` in staging. NEVER write irreversible migrations (data destructive) without explicit user approval.
6. [REQ] Schema Design: Normalize to 3NF minimum. Denormalize only with measured proof of N+1 or hot-path need. Index foreign keys + frequently queried columns. Use `uuidv7()` for time-ordered UUIDs on PG.
7. [REQ] Vector Columns: Use `AsVector` cast (Laravel 13.31+). Migration: `$table->vector('embedding', dimensions: 1536)` on PG with pgvector. On MariaDB: native `VECTOR` type. NEVER on plain MySQL (no vector support).
8. [REQ] Multi-DB Compatibility: Test migrations on both MySQL and PostgreSQL. Use `Schema::hasColumn()` for conditional logic. Avoid DB-specific raw SQL in migrations — use schema builder. If raw SQL needed, branch on `DB::getDriverName()`.
9. [REQ] Data Backfill: Backfill in batches (`chunk(500)`). NEVER `Model::all()` in migrations. Use raw SQL `UPDATE ... WHERE id BETWEEN ? AND ?` for large tables. Set `timeout` for long backfills.
10. [REQ] Migration Order: `php artisan migrate:status` before deploy. NEVER run migrations out of order. Use `--pretend` to preview SQL. Use `--force` only in CI/CD.
11. [REQ] Rollback Plan: Every deploy must have a documented rollback. `php artisan migrate:rollback --step=1` for last batch. Test rollback in staging. NEVER deploy without rollback plan for schema changes.
12. [REQ] Connection Pooling: `pgbouncer` (transaction mode) for PG. `mysqlnd` persistent connections for MySQL. NEVER exceed `max_connections` — calculate pool size as `workers * connections_per_worker`.

[WORKFLOWS]
1. Add Column (Zero-Downtime): Create migration `add_status_to_users` → `$table->string('status')->nullable()` → deploy → update code to write `status` → create backfill migration `UPDATE users SET status='active' WHERE status IS NULL` → create migration `set_status_not_null` → deploy.
2. Rename Column (Safe): Add new column → dual-write in code → backfill new from old → switch reads to new → drop old column. NEVER `renameColumn()` directly in production (breaks running code).
3. Large Table Index: Create migration with `CREATE INDEX CONCURRENTLY` (PG) → deploy during low traffic → monitor `pg_stat_progress_create_index` → verify with `EXPLAIN`.
4. Vector Search Migration: `CREATE EXTENSION vector` → `$table->vector('embedding', dimensions: 1536)` → add HNSW index → add `AsVector` cast to model → deploy → test `whereVectorSimilarTo()`.
