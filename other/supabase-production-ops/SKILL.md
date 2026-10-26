---
name: supabase-production-ops
description: Safe Supabase production operations, migration deployments, database connection pooling, RLS auditing, and backup verification for LKDV.
---

# Supabase Production Operations & Auditing

This skill governs all production database operations on Supabase for Le Kit du Voyageur (LKDV), targeting project `icxyvwzfjbflcbqukpfz`.

## 1. Safety Rules & Production Migrations

- **Zero Data Loss Principle**:
  - Never run `DROP TABLE` or destructive `ALTER TABLE ... DROP COLUMN` directly in production.
  - Follow the two-phase migration pattern: Expand (add column/function) -> Backfill & Deploy code -> Contract (cleanup deprecated schema).
- **Migration Deployment**:
  - All migrations are tracked in `supabase/migrations/` with UTC timestamps.
  - Test migrations locally with `npx supabase db reset` or test harness before proposing execution in production.
  - Tony applies migrations to production via the Supabase Dashboard SQL Editor or via the Supabase CLI (`npx supabase db push`) when authorized.

## 2. Row Level Security (RLS) & PostGIS Indexing

- **RLS Mandatory on 100% of Public Tables**:
  - Every table created must immediately have:
    ```sql
    ALTER TABLE public.<table_name> ENABLE ROW LEVEL SECURITY;
    ```
  - Standard policy template:
    ```sql
    CREATE POLICY "Users can only view their own items"
      ON public.<table_name> FOR SELECT
      USING (auth.uid() = user_id);
    ```
- **PostGIS Performance**:
  - All spatial query columns (`geog` or `geom` with SRID 4326) MUST have a GiST or SP-GiST index:
    ```sql
    CREATE INDEX IF NOT EXISTS idx_<table_name>_geom ON public.<table_name> USING GIST (geom);
    ```
  - Use `ST_DWithin` with geography or spatial indexes instead of computing Cartesian distance on huge tables.

## 3. Connection Pooling & Resource Health

- **Supavisor / Transaction Pooling**:
  - Always connect serverless Next.js functions via the transaction pooler port (6543) with `pgbouncer=true` query parameter for high concurrency.
  - Reserve direct session connections (port 5432) strictly for long-running administrative migrations.
- **Monitoring & Alerts**:
  - Monitor database CPU, connection count, and disk IOPS in the Supabase Dashboard.
  - Verify that `SECURITY DEFINER` functions have explicit `search_path = public, pg_temp;`.

## 4. Supabase MCP & CLI Tools

- **Supabase MCP Server**:
  - Query project metadata, schema introspection, table structures, and run verified diagnostic queries.
- **Supabase CLI**:
  - `supabase migration list`
  - `supabase gen types typescript --project-id icxyvwzfjbflcbqukpfz > src/lib/supabase/types.ts`
  - `supabase db lint`
