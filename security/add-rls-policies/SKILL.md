---
name: add-rls-policies
description: Generate Row Level Security policies for a Supabase table following Arch Systems department isolation patterns
disable-model-invocation: true
---

# Add RLS Policies Skill

## Purpose

Generate Row Level Security (RLS) policies for Supabase tables following the Arch Systems department isolation and role-based access patterns.

## Process

### 1. Ask for policy details

- **table** — Table name (e.g. `operational_delays`, `breakdowns`)
- **schema** — Schema (default: `public`)
- **scope** — Access scope:
  - `department` — Users can only see/modify rows in their department (most common)
  - `admin-only` — Only admins can access
  - `owner` — Users can only see/modify their own records (e.g. personal tasks)
  - `public-read` — All authenticated users can read, only department members can write
- **operations** — Which operations to create policies for: SELECT, INSERT, UPDATE, DELETE
- **append-only** — Is this table append-only? (like `daily_logs` — no UPDATE/DELETE needed)
- **soft-delete** — Should DELETE policy check for `deleted_at IS NULL`?

### 2. Generate the SQL

#### Department-scoped policies (most common)

```sql
-- Enable RLS
ALTER TABLE public.<table> ENABLE ROW LEVEL SECURITY;

-- SELECT: department members + admin
CREATE POLICY "<table>_select_department" ON public.<table>
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM employees e
      WHERE e.auth_id = auth.uid()
        AND (
          e.role = 'admin'
          OR e.department_id = <table>.department_id
          OR <table>.department_id = ANY(e.accessible_departments)
        )
    )
  );

-- INSERT: department members + admin
CREATE POLICY "<table>_insert_department" ON public.<table>
  FOR INSERT TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM employees e
      WHERE e.auth_id = auth.uid()
        AND (
          e.role = 'admin'
          OR e.department_id = <table>.department_id
          OR <table>.department_id = ANY(e.accessible_departments)
        )
    )
  );

-- UPDATE: department members + admin (optionally restricted to record creator)
CREATE POLICY "<table>_update_department" ON public.<table>
  FOR UPDATE TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM employees e
      WHERE e.auth_id = auth.uid()
        AND (
          e.role = 'admin'
          OR e.department_id = <table>.department_id
          OR <table>.department_id = ANY(e.accessible_departments)
        )
    )
  );

-- DELETE: admin only (or restrict to supervisors/admins)
CREATE POLICY "<table>_delete_admin" ON public.<table>
  FOR DELETE TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM employees e
      WHERE e.auth_id = auth.uid()
        AND e.role = 'admin'
    )
  );
```

#### Append-only policies (for logs, audit trails)

```sql
-- Same SELECT and INSERT as above
-- NO UPDATE policy — records are immutable
-- NO DELETE policy — records cannot be removed
-- Optionally add a soft-update policy for corrections only:
CREATE POLICY "<table>_update_corrections" ON public.<table>
  FOR UPDATE TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM employees e
      WHERE e.auth_id = auth.uid()
        AND (e.role = 'admin' OR e.role = 'supervisor')
    )
  );
```

#### Admin-only policies

```sql
CREATE POLICY "<table>_select_admin" ON public.<table>
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM employees e
      WHERE e.auth_id = auth.uid()
        AND e.role = 'admin'
    )
  );

-- Similar for INSERT, UPDATE, DELETE with admin-only check
```

#### Public-read, department-write policies

```sql
-- SELECT: all authenticated users
CREATE POLICY "<table>_select_authenticated" ON public.<table>
  FOR SELECT TO authenticated
  USING (true);

-- INSERT/UPDATE: department members only (same as department-scoped WITH CHECK)
```

### 3. Add supporting indexes

Always include these indexes for department-scoped tables:

```sql
CREATE INDEX idx_<table>_department ON public.<table>(department_id);
CREATE INDEX idx_<table>_created_at ON public.<table>(created_at DESC);

-- If table has a status column:
CREATE INDEX idx_<table>_status ON public.<table>(status)
  WHERE deleted_at IS NULL;
```

### 4. Add updated_at trigger (if table has `updated_at` column)

```sql
CREATE TRIGGER update_<table>_updated_at
  BEFORE UPDATE ON public.<table>
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

Note: The `update_updated_at_column()` function should already exist from the initial migration. Only create the trigger.

### 5. Add to existing migration or create new one

- If adding policies to an existing table, create a new migration file
- If creating a new table with policies, include everything in one migration
- Naming: `packages/database/migrations/NNN_<description>.sql`

### 6. Post-creation

1. Push migration: `cd packages/database && pnpm supabase:push`
2. Verify in Supabase Studio that policies appear under Authentication > Policies
3. Test with different roles (admin, supervisor, operator)
4. Commit the migration file

## Policy Naming Convention

- `<table>_<operation>_<scope>` — e.g., `operational_delays_select_department`
- Always include the table name prefix
- Always include the scope suffix (`_department`, `_admin`, `_authenticated`, `_owner`)

## Security Checklist

Before finalizing, verify:

- [ ] RLS is enabled (`ALTER TABLE ... ENABLE ROW LEVEL SECURITY`)
- [ ] Every table has at minimum a SELECT policy
- [ ] INSERT policies include `WITH CHECK` (not just `USING`)
- [ ] DELETE is restricted (admin-only or not present for audit tables)
- [ ] `department_id` column exists on the table for department-scoped policies
- [ ] `employees.accessible_departments` is checked for cross-department access
- [ ] Service role key is NEVER used in client-side code or `NEXT_PUBLIC_*` variables
