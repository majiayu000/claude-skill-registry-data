---
name: "postgres-supabase-expert"
description: "Advanced guide for PostgreSQL and Supabase. Covers schema design, RLS, query optimization, migrations, Edge Functions, and database security."
---

# Postgres & Supabase Expert Guide

This skill provides comprehensive rules for designing, optimizing, and securing databases on PostgreSQL and the Supabase platform.

## 🏗 Schema Design
- **Normalization**: Follow 3NF unless denormalization is required for performance.
- **Data Types**: Use appropriate types (e.g., `UUID` for IDs, `TIMESTAMPTZ` for dates, `JSONB` for flexible data).
- **Constraints**: Use `NOT NULL`, `UNIQUE`, and `CHECK` constraints to ensure data integrity at the database level.
- **Indexes**: Use `B-tree` for equality and range queries, `GIN` for JSONB/Arrays, and `BRIN` for large sequential datasets.

## 🛡 Security & Privacy

### R-01 RLS DEFAULT & POLICY ENFORCEMENT (Moved from engineering-contracts former §17 — Canonical Authority for Postgres/Supabase)

> **SCOPE:** Applies ONLY to PostgreSQL and Supabase. Do NOT use RLS syntax on MySQL, SQLite, MongoDB, Cassandra, or non-Postgres databases — for those see engineering-contracts §17 pointer.

Enforcement Rule (HARD — every new table):
1. **For EVERY new table:** immediately add `ALTER TABLE <schema>.<table> ENABLE ROW LEVEL SECURITY;` in the migration.
2. **Define explicit read/write policies per role** (e.g. `organizer_select_policy`, `admin_all_policy`). A table with RLS enabled but ZERO policies = no rows can be read/written (default deny) — good.
3. **Add an Acceptance Criteria in the SPEC (if using che-spec standalone or /che-act SM §0.5 SPEC gate) specifically for RLS:** e.g. `- [MUST] AC-RLS GIVEN Organizer A authenticated WHEN querying tickets/events owned by Organizer B THEN HTTP 403 or 404 returned | TEST=qa_integration` literal format in §4. This is validated during QA.
4. **ONLY exception (allowed logged + user approved DOUBLE CONFIRMATION):**
   - Pure lookup tables (enum reference tables, immutable public seed data for everyone) → RLS not needed, BUT:
     - Explicitly mark in Non-Goals / Data Model notes of the SPEC.
     - Log exception + user approval in `decisions.log.jsonl`
     - Table name + reason documented in migration notes.

### Additional Security & Privacy (R-02 …)
- **RLS per-table minimum 1 policy of each kind** where applicable: SELECT/INSERT/UPDATE/DELETE — don't leave a write-path open if only SELECT was thought through.
- **Encryption**: Use `pg_sodium` for sensitive data encryption at-rest where PII cannot be hashed.
- **Schemas**: Isolate data using different Postgres schemas (e.g. `public`, `private`, `auth`) + grant usage per role.
- **PII**: Avoid storing raw PII where possible. Use hashing (with NOTIFICATION_PII_HASH_SECRET-style secret) for correlation IDs, or pg_crypto/pg_sodium encryption if storage is unavoidable.
- **`auth.uid()` default-deny pattern**: In Supabase, start every policy with `auth.uid() = <owner_column>` — then add admin/org overrides on top. Never write a policy that is `true` for `anon` role unless it is genuinely a public-visible lookup table (and §R-01 exception 4 was filed).

## 🚀 Performance & Optimization
- **EXPLAIN ANALYZE**: Always use to identify slow queries and sequential scans.
- **Vacuum & Analyze**: Monitor bloat and keep statistics up to date.
- **Connection Pooling**: Use `Supavisor` or `PgBouncer` for high-concurrency applications.
- **Pagination**: Prefer keyset pagination (cursor-based) over `OFFSET` for large datasets.

## ⚡ Supabase Features
- **Edge Functions**: Use for logic that requires external API calls or heavy processing. Use Deno/TypeScript.
- **Realtime**: Use sparingly for live updates. Filter channels to reduce overhead.
- **Storage**: Use for large assets. Enforce RLS on buckets and folders.
- **Migrations**: Use the Supabase CLI for declarative migrations. Never make manual changes in production.

## 🔗 References
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Supabase Documentation](https://supabase.com/docs)
- [Supabase RLS Guide](https://supabase.com/docs/guides/auth/row-level-security)
