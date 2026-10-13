---
name: administering-supabase
version: "1.0.1"
description: >
  Manages Supabase database operations for FlashFusion's production stack —
  schema design, Row Level Security policies, migrations, Edge Functions, and
  debugging. Active project: flashnframe-app (etctmappdhpjuwptdbeb). Activates
  when the user mentions: Supabase, RLS, row level security, migration, schema,
  database, table, Edge Function, auth, policies, Postgres, supabase query,
  database admin, add a column, create a table, why is my query blocked, or
  any task involving the Supabase project or database structure.
---

# Supabase Database Admin

Covers the operations that come up on every build: schema changes, RLS policies,
migrations, and debugging access errors.

Active project: `flashnframe-app` (ID: `etctmappdhpjuwptdbeb`)
Deleted project `oorstbwcydxwiojrsoim` — do not use.

---

## Evals

**Should trigger:**
1. "Add a table to Supabase for storing FlashFusion client records"
2. "My query is returning empty results — RLS might be blocking it"
3. "Write a migration to add a status column to the jobs table"

**Should NOT trigger:**
1. "Help me design the architecture for a new app" — use enabling-ai-solutions
2. "Write a React component that fetches from Supabase" — frontend skill

---

## Decision Tree

```
What's the task?
  ├─ Create or modify a table → Section 2: Schema Design
  ├─ Write or debug an RLS policy → Section 3: Row Level Security
  ├─ Add a column or make a schema change safely → Section 4: Migrations
  ├─ Write or deploy an Edge Function → Section 5: Edge Functions
  └─ Query returning unexpected results → Section 6: Debugging
```

RLS patterns in `references/rls-patterns.md`.

---

## Section 1: Project Setup Reminder

Before any admin work, confirm you're working on the correct project.

```sql
-- Verify in Supabase dashboard or via MCP:
-- Project: flashnframe-app
-- ID: etctmappdhpjuwptdbeb
-- Region: check in dashboard
```

The deleted project (`oorstbwcydxwiojrsoim`) should not appear in any
active connection. If it does, that connection needs to be rotated.

---

## Section 2: Schema Design

### Table naming conventions
- Snake case: `client_records`, `job_queue`, `agent_runs`
- Plural table names
- Junction tables: `{table_a}_{table_b}` alphabetical order
- Avoid reserved words: `user`, `order`, `group`, `schema`

### Standard columns every table should have

```sql
id          uuid          DEFAULT gen_random_uuid() PRIMARY KEY,
created_at  timestamptz   DEFAULT now() NOT NULL,
updated_at  timestamptz   DEFAULT now() NOT NULL
```

Add a trigger for `updated_at` auto-update:

```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON your_table_name
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### Auth user linkage

When a table should be owned by a user:

```sql
user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL
```

Always reference `auth.users`, not a custom users table.
`ON DELETE CASCADE` removes the row when the user is deleted.

---

## Section 3: Row Level Security

**The most common source of bugs in every Supabase project.**

### The two steps that must both happen

```sql
-- Step 1: Enable RLS on the table (required before any policy works)
ALTER TABLE your_table ENABLE ROW LEVEL SECURITY;

-- Step 2: Create at least one policy (without a policy, ALL access is blocked)
```

Skipping either step causes silent failure. A table with RLS enabled and
no policies returns zero rows for every query — no error, just empty results.

### Common policy patterns

Full patterns and explanations in `references/rls-patterns.md`.

**Quick reference:**

```sql
-- Public read (anonymous + authenticated)
CREATE POLICY "public_read" ON your_table
  FOR SELECT USING (true);

-- Authenticated users only
CREATE POLICY "auth_only" ON your_table
  FOR ALL USING (auth.role() = 'authenticated');

-- Owner only (user owns the row)
CREATE POLICY "owner_only" ON your_table
  FOR ALL USING (auth.uid() = user_id);

-- Service role bypass: use service_role key in server-side code —
-- it bypasses RLS entirely. Never expose the service_role key client-side.
```

### Performance requirement

Index every column used in a RLS policy on tables over ~10,000 rows.
Without this, every row requires a sequential scan — a table scan per query.

```sql
CREATE INDEX idx_your_table_user_id ON your_table(user_id);
```

---

## Section 4: Migrations

Use Supabase migration files. Never modify schema directly in production
without a migration file — you lose the change history and reproducibility.

### Migration workflow

```bash
# Create a new migration
supabase migration new add_status_to_jobs

# Edit the generated file in supabase/migrations/
# Run locally first
supabase db reset

# Push to remote
supabase db push
```

### Safe column addition pattern

Adding a column to an existing table with data:

```sql
-- Step 1: Add as nullable (no constraint — safe for existing rows)
ALTER TABLE jobs ADD COLUMN status text;

-- Step 2: Backfill existing rows
UPDATE jobs SET status = 'pending' WHERE status IS NULL;

-- Step 3: Add NOT NULL constraint (only after backfill is complete)
ALTER TABLE jobs ALTER COLUMN status SET NOT NULL;
ALTER TABLE jobs ALTER COLUMN status SET DEFAULT 'pending';
```

**Never** add a NOT NULL column without a default in a single operation
on a table with existing rows. It will fail.

### Destructive change checklist

Before dropping a column or table:
- [ ] Confirm no application code references this column/table
- [ ] Create a backup or snapshot first
- [ ] Drop in a separate migration from the replacement
- [ ] Verify in staging before production

---

## Section 5: Edge Functions

Edge Functions are TypeScript functions that run server-side, useful for:
- Webhook handlers
- Background jobs triggered by database events
- API endpoints that need service_role access (bypass RLS safely)

```bash
# Create a new function
supabase functions new function-name

# Serve locally for testing
supabase functions serve

# Deploy
supabase functions deploy function-name
```

**Environment variables:** never hardcode secrets in Edge Functions.
Use `Deno.env.get('SECRET_NAME')` and store in Supabase secrets:
`supabase secrets set SECRET_NAME=value`

---

## Section 6: Debugging

### Empty results (likely RLS)

```sql
-- Check if RLS is enabled
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public';

-- Check existing policies
SELECT * FROM pg_policies WHERE tablename = 'your_table';

-- Test as authenticated user (in SQL editor, set the role)
SET LOCAL role = authenticated;
SET LOCAL request.jwt.claims = '{"sub": "user-uuid-here"}';
SELECT * FROM your_table;
```

### Permission denied errors

- `permission denied for table` → RLS policy denying access, or table not
  granted to the role
- `new row violates row-level security policy` → INSERT policy is blocking
- Returning empty instead of error → SELECT policy is blocking silently

### auth.uid() returning NULL

This happens in server-side code using the anon key. Switch to:
- Passing the user's JWT from the client for user-context queries
- Using the service_role key for admin operations (bypasses auth.uid())

---

## Self-Verification

Before any schema change in production:
- [ ] Migration file created (not a manual dashboard change)
- [ ] RLS enabled AND at least one policy defined for every new table
- [ ] Indexes added for any column used in RLS policies
- [ ] Column additions follow the nullable → backfill → NOT NULL pattern
- [ ] Tested locally or in staging before pushing to production

---

## CLAIMS
- A table with RLS enabled but no policies returns zero rows silently —
  no error, just empty results; this is the most common Supabase debug scenario
- Indexing RLS policy columns is mandatory on tables over 10K rows;
  unindexed RLS policies cause full table scans on every authenticated query

## COUNTEREXAMPLE
- The service_role key bypasses RLS entirely — it's the correct choice
  for admin scripts and Edge Functions that need elevated access, but
  exposing it client-side is a critical security vulnerability

## CONTRADICTIONS
- "Never modify schema directly in production" conflicts with urgent
  hotfixes; if a production issue requires an immediate column addition,
  add it manually then retroactively create the migration file — document
  the manual change in the migration comment
