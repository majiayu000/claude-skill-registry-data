---
name: create-migration
description: Scaffold a new SQL migration for Arch-Mk2's Supabase database. Use when the user says "create a migration", "add a migration", "new table for X", or asks to add a column/RLS policy/function. Encodes the project's NNN_description.sql naming, RLS-required-by-default rule, and the packages/database/migrations/ ↔ packages/supabase/supabase/migrations/ deploy-copy split.
disable-model-invocation: true
---

# Create Migration

User-only side-effect skill. Walks the contributor through authoring a new SQL migration that conforms to Arch-Mk2's database conventions.

## When to use

- User says "create a migration", "add a new table for X", "add a column to Y"
- User is doing schema work in `packages/database/migrations/`
- User wants to add an RLS policy, index, function, or trigger

## When NOT to use

- User is editing `packages/supabase/supabase/migrations/` — **block and explain**: that's a deploy-time copy, the source of truth is `packages/database/migrations/`. The PreToolUse hook in `.claude/settings.json` already enforces this; if the user explicitly overrides, do not edit but flag.
- The work is documentation, type generation, or app code — not SQL.

## Workflow

1. **Find the next NNN.** Run `ls packages/database/migrations/ | sort | tail -5` to get the highest current number, then add 1 (zero-padded to 3 digits). For multi-file migrations in one batch, increment from there.
2. **Choose the file path.** Always `packages/database/migrations/NNN_description.sql` where description is snake_case. Never `packages/supabase/supabase/migrations/`.
3. **Pick a template.** Three templates cover ~95% of cases:
   - **New table** → `templates/migration.sql` (CREATE TABLE + ALTER TABLE ENABLE RLS + comment header)
   - **Column / index on existing table** → start from a stripped-down version of `templates/migration.sql` (no RLS block, just the ALTER)
   - **Function / trigger / policy** → start from `templates/migration.sql`, replace the body
4. **Fill in the body.** Every `CREATE TABLE` must be paired with `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` unless an inline comment explains why not (the `rls-prompt` PreToolUse hook will soft-warn otherwise).
5. **Validate locally** by running `bash .claude/plugins/arch-mk2-dev/skills/create-migration/scripts/validate.sh packages/database/migrations/NNN_description.sql`. It checks:
   - Filename pattern `NNN_description.sql`
   - Path is `packages/database/migrations/` (not the deploy copy)
   - Presence of a header comment with date
   - For CREATE TABLE: presence of ENABLE ROW LEVEL SECURITY
6. **Sync to the deploy copy.** The repo deploys from `packages/supabase/supabase/migrations/`. After validation, copy with `cp packages/database/migrations/NNN_description.sql packages/supabase/supabase/migrations/`. A pre-commit hook does this automatically when the file is staged; verify with `git status` after `git add`.
7. **Regenerate types** with `pnpm --filter @repo/database supabase:gen` (the user must run this; it touches `packages/types/src/database.types.ts`).
8. **Tell the user** what was created and what to do next (sync, typegen, run migration locally via Supabase CLI).

## Agents to consider

| Agent                   | When                                                            |
| ----------------------- | --------------------------------------------------------------- |
| `database-developer`    | Schema, RLS, indexes, query perf                                |
| `migration-coordinator` | Multi-file migration batch, typegen, app code updates           |
| `auth-flow-reviewer`    | Anything touching the `employees` table, role, or department_id |

## Templates

### templates/migration.sql

```sql
-- NNN_description.sql
-- Created: YYYY-MM-DD
-- Purpose: <one-line summary of the change>

-- ============================================================================
-- Up Migration
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.<table_name> (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  -- columns here
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

-- RLS: required for new tables per .claude/rules/auth.md
ALTER TABLE public.<table_name> ENABLE ROW LEVEL SECURITY;

-- Default-deny policy: explicit grants to authenticated role
CREATE POLICY "<table_name>_select_authenticated"
  ON public.<table_name>
  FOR SELECT
  TO authenticated
  USING (true);

-- Indexes for common query patterns (add as needed)
-- CREATE INDEX <table_name>_created_at_idx ON public.<table_name> (created_at DESC);

-- ============================================================================
-- Down Migration (manual; Supabase does not auto-rollback)
-- ============================================================================
-- DROP POLICY IF EXISTS "<table_name>_select_authenticated" ON public.<table_name>;
-- DROP TABLE IF EXISTS public.<table_name>;
```

## Anti-patterns

- **Editing the deploy copy directly** — there is a PreToolUse hook to block this; the source of truth is `packages/database/migrations/`.
- **Skipping RLS** — every new table gets it. If intentional (e.g. a seed/ref table), add `-- INTENTIONAL: <reason>` above the CREATE TABLE.
- **Using `ALTER TABLE ADD COLUMN` without a default** — Postgres rewrites the entire table. Always provide a default for non-null columns on large tables.
- **Putting the date in the filename** — `NNN_description.sql` only. Date goes in the file header.
- **Forgetting to regenerate types** — `packages/types/src/database.types.ts` is auto-generated; the new column/table won't be visible to TypeScript until you run `pnpm --filter @repo/database supabase:gen`.
