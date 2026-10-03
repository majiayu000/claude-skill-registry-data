---
name: supabase-rls-beamix
last_updated: 2026-05-17
description: "Beamix RLS conventions: per-user row-level security, service-role bypass patterns for Inngest jobs, war-room table deny-all policies, and audit_log write permissions. Use when writing or reviewing any Supabase migration or RLS policy in this project."
tags: [database, beamix-specific, security, supabase]
source: beamix-authored 2026-05-16
risk: low
---

# Supabase RLS — Beamix

## Quick reference

> Every table with user data needs RLS ENABLE + at least one policy. `auth.uid()` for user-owned. Service-role bypass = audit_log row.

## When to use

- Writing a new migration that adds a table requiring RLS
- Reviewing whether an existing table has correct policies
- Debugging an "insufficient privilege" error from a product API route
- Writing war-room table policies for agent observability tables

## When NOT to use

- For application-layer auth (that's Supabase Auth + middleware)
- For pgvector RAG query patterns (see `pgvector-rag-beamix`)

## Core RLS conventions

### User-scoped tables (product data)

All product tables with user data use `user_id = auth.uid()` as the baseline policy.

```sql
-- Standard pattern for user-scoped tables
ALTER TABLE businesses ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users_own_businesses"
  ON businesses
  FOR ALL
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());
```

Tables that follow this pattern:
- `businesses`
- `scans`
- `scan_engine_results`
- `agent_jobs`
- `credit_pools`
- `credit_transactions`
- `content_items`
- `recommendations`
- `user_profiles`
- `subscriptions`
- `notification_preferences`

### Read-only public tables

Some tables are readable by any authenticated user but not writable (e.g., reference data):

```sql
CREATE POLICY "authenticated_read_only"
  ON industries
  FOR SELECT
  USING (auth.role() = 'authenticated');
```

### Service-role bypass (for Inngest and background jobs)

Inngest functions, Routines, and the Cloudflare bridge use the Supabase service-role key, which bypasses RLS entirely. This is intentional — background jobs need to write to any user's rows.

```typescript
// In Inngest functions or server-side jobs — use service role
import { createClient } from '@supabase/supabase-js';

const adminClient = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!  // never expose this to the client
);

// This bypasses RLS — use for background job writes only
await adminClient.from('audit_log').insert({ ... });
```

For product API routes (user-facing), use the user's session client instead:

```typescript
// In Next.js API routes — use session (respects RLS)
import { createServerClient } from '@supabase/ssr';

const supabase = createServerClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  { cookies: ... }
);
```

## War-room table policies

War-room tables store agent observability data. They use `RLS deny-all` + service-role bypass only.

```sql
-- audit_log: deny all to authenticated users, service role only
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

-- No policies = deny all by default (RLS enabled, zero policies)
-- Service role bypasses this automatically

-- Adam reads via server-side /war-room route (checks session.user.email = ADAM_EMAIL)
-- This enforcement happens in Next.js middleware, not in RLS
```

War-room tables with deny-all policy:
- `audit_log`
- `audit_log_daily`
- `claude_progress`
- `rag_corpus`
- `mem0_pending_writes` (when implemented)

### /war-room access pattern

```typescript
// apps/web/src/app/war-room/page.tsx (server component)
import { headers } from 'next/headers';
import { createServerClient } from '@supabase/ssr';

export default async function WarRoomPage() {
  const supabase = createServerClient(...);
  const { data: { user } } = await supabase.auth.getUser();

  // Hard gate: only Adam can see this page
  if (user?.email !== process.env.ADAM_EMAIL) {
    redirect('/dashboard');
  }

  // Use admin client to read war-room tables (deny-all RLS)
  const adminClient = createClient(..., process.env.SUPABASE_SERVICE_ROLE_KEY!);
  const { data: auditLog } = await adminClient
    .from('audit_log')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(100);

  return <WarRoomView data={auditLog} />;
}
```

## plpgsql SQL Editor bug (known issue)

When running plpgsql in the Supabase SQL Editor, the editor splits on semicolons inside `$$` blocks, causing `42P01` errors where DECLARE variables are treated as table lookups.

Workaround: always use `LANGUAGE sql` + CTEs instead of plpgsql DECLARE blocks in migrations:

```sql
-- WRONG: plpgsql with DECLARE (SQL Editor breaks this)
DO $$
DECLARE
  v_user_id uuid;
BEGIN
  SELECT id INTO v_user_id FROM auth.users LIMIT 1;
  -- ...
END $$;

-- CORRECT: LANGUAGE sql + CTE
WITH target_user AS (
  SELECT id FROM auth.users LIMIT 1
)
INSERT INTO user_profiles (user_id, created_at)
SELECT id, now() FROM target_user
ON CONFLICT (user_id) DO NOTHING;
```

## Migration naming convention

```
apps/web/supabase/migrations/YYYYMMDDHHMMSS_description.sql
```

Example: `20260516120000_add_audit_log_indexes.sql`

Each migration must be idempotent (safe to re-run). Use `IF NOT EXISTS`, `ON CONFLICT DO NOTHING`, `CREATE INDEX CONCURRENTLY IF NOT EXISTS`.

## See also

- `postgresql` — [[postgresql]]
- `sql-optimization-patterns` — [[sql-optimization-patterns]]
- `gdpr-data-handling` — [[gdpr-data-handling]]
- `database-design` — [[database-design]]

## Anti-patterns

- Using service-role key in client-side code (exposes full DB access)
- Writing product API routes with admin client (bypasses RLS, exposes other users' data)
- Adding an RLS policy without enabling RLS first (`ALTER TABLE ... ENABLE ROW LEVEL SECURITY`)
- plpgsql DECLARE blocks in SQL Editor migrations (use LANGUAGE sql + CTEs)
- Mixing war-room table writes with product API routes (war-room writes = bridge + Inngest only)
- Enabling RLS without any policies (deny-all is intentional for war-room tables, but accidental deny-all on product tables breaks the app)
