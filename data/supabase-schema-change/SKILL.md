---
name: supabase-schema-change
description: Complete workflow for Supabase schema changes. This skill should be used when modifying database schema including tables, columns, functions, views, triggers, indexes, or RLS policies. Automatically triggers when user mentions 'add column', 'drop column', 'add field', 'remove field', 'schema change', 'alter table', 'create function', 'create view', 'create trigger', 'add index', 'RLS policy', or 'database migration'. Enforces a comprehensive workflow to ensure complete migration with type safety across any Supabase + Next.js project.
---

# Supabase Schema Change Workflow

## Overview

This skill provides a complete, enforced workflow for making Supabase schema changes in any Next.js + Supabase project. It ensures all changes are properly migrated, typed, and propagated through the entire codebase.

## Supported Schema Changes

| Category | Operations |
|----------|------------|
| **Tables** | CREATE, ALTER, DROP, RENAME |
| **Columns** | ADD, DROP, ALTER, RENAME |
| **Functions** | CREATE, REPLACE, DROP |
| **Views** | CREATE, REPLACE, DROP |
| **Triggers** | CREATE, DROP, ENABLE, DISABLE |
| **Indexes** | CREATE, DROP |
| **RLS Policies** | CREATE, ALTER, DROP |
| **Constraints** | ADD, DROP (FK, UNIQUE, CHECK) |

## Critical Rules

1. **ALWAYS use Supabase MCP first** - Query real-time database state before any changes
2. **NEVER skip steps** - Each step depends on the previous one
3. **⚠️ MANDATORY: Ask for confirmation** - Present a detailed Migration Plan and wait for explicit user approval before applying ANY changes
4. **UPDATE all layers** - Types, API routes, services, and UI components
5. **DOCUMENT everything** - Migration files should be self-explanatory

## Mandatory Confirmation Step

**Before applying ANY schema change, you MUST:**

1. Present a formatted **Migration Plan** showing:
   - Table/Object being modified
   - Action (ADD/DROP/ALTER/CREATE/etc.)
   - Changes table with columns, types, and actions
   - SQL to execute
   - Files that need updating
   - Impact assessment (breaking changes, rollback SQL)

2. Ask explicitly: **"Proceed with migration? (yes/no)"**

3. **Only proceed if user confirms "Yes"**

Example Migration Plan format:
```
## Migration Plan

**Table:** `public.table_name`
**Action:** DROP column

### Changes:
| Column | Type | Action |
|--------|------|--------|
| column_name | UUID | DROP |

### SQL to Execute:
ALTER TABLE public.table_name DROP COLUMN IF EXISTS column_name;

### Files to Update:
- supabase/migrations/YYYYMMDD_*.sql - Delete or update
- types/entity.ts - Remove from interfaces
- app/api/module/route.ts - Remove from GET, POST, PUT
- app/api/module/[id]/route.ts - Remove from GET

**Proceed with migration? (yes/no)**
```

## Schema Change Decision Tree

```
What are you changing?
├── Column (ADD/DROP/ALTER)
│   └── Follow: Column Change Workflow
├── Function (CREATE/REPLACE/DROP)
│   └── Follow: Function Change Workflow
├── View (CREATE/REPLACE/DROP)
│   └── Follow: View Change Workflow
├── Trigger (CREATE/DROP)
│   └── Follow: Trigger Change Workflow
├── Index (CREATE/DROP)
│   └── Follow: Index Change Workflow
├── RLS Policy (CREATE/ALTER/DROP)
│   └── Follow: RLS Policy Workflow
└── Table (CREATE/DROP/RENAME)
    └── Follow: Table Change Workflow
```

---

## Column Change Workflow (10 Steps)

### Step 1: Query Current Schema

```sql
-- Check current table structure using MCP
mcp__supabase__execute_sql
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'your_table'
ORDER BY ordinal_position;

-- For ADD: Check if column already exists
mcp__supabase__execute_sql
SELECT column_name FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'your_table'
  AND column_name = 'new_column';

-- For DROP: Check dependencies
mcp__supabase__execute_sql
SELECT
  tc.constraint_name,
  tc.constraint_type,
  kcu.column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
  ON tc.constraint_name = kcu.constraint_name
WHERE tc.table_name = 'your_table'
  AND kcu.column_name = 'column_to_drop';
```

### Step 2: Validate Changes

**For ADD column:**
- [ ] Column doesn't already exist
- [ ] Data type is appropriate
- [ ] Nullable vs NOT NULL decision made
- [ ] Default value specified if needed
- [ ] Naming follows snake_case convention

**For DROP column:**
- [ ] Column exists
- [ ] No foreign key dependencies
- [ ] No index dependencies
- [ ] No view dependencies
- [ ] No function dependencies

**For ALTER column:**
- [ ] Current data is compatible with new type
- [ ] NOT NULL constraint can be satisfied

### Step 3: Create Migration Query

```sql
-- ADD column
ALTER TABLE public.table_name
ADD COLUMN IF NOT EXISTS column_name DATA_TYPE DEFAULT default_value;

-- DROP column
ALTER TABLE public.table_name
DROP COLUMN IF EXISTS column_name;

-- ALTER column type
ALTER TABLE public.table_name
ALTER COLUMN column_name TYPE NEW_TYPE USING column_name::NEW_TYPE;

-- ALTER column nullable
ALTER TABLE public.table_name
ALTER COLUMN column_name SET NOT NULL;
-- or
ALTER TABLE public.table_name
ALTER COLUMN column_name DROP NOT NULL;

-- RENAME column
ALTER TABLE public.table_name
RENAME COLUMN old_name TO new_name;
```

### Step 4: Ask for Confirmation (MANDATORY)

**⚠️ CRITICAL: NEVER skip this step. ALWAYS present the migration plan and wait for user approval.**

Present a formatted migration plan and use `AskUserQuestion` tool to get explicit confirmation:

---

#### Migration Plan Template

```markdown
## Migration Plan

**Table:** `public.table_name`
**Action:** [ADD/DROP/ALTER/RENAME] column

### Changes:
| Column | Type | Nullable | Default | Action |
|--------|------|----------|---------|--------|
| column_name | DATA_TYPE | YES/NO | value | ADD/DROP/ALTER |

### SQL to Execute:
```sql
ALTER TABLE public.table_name
[ADD COLUMN IF NOT EXISTS / DROP COLUMN IF EXISTS / ALTER COLUMN] column_name ...;
```

### Files to Update:
| File | Change Required |
|------|-----------------|
| `supabase/migrations/YYYYMMDD_*.sql` | Create/Update/Delete migration |
| `types/[entity].ts` | Add/Remove field from interface(s) |
| `app/api/[module]/route.ts` | Update SELECT, INSERT, UPDATE queries |
| `app/api/[module]/[id]/route.ts` | Update SELECT query |
| `services/[module]/*` | Check for field references |
| `app/[route]/[module]/page.tsx` | Check UI references |

### Impact Assessment:
- **Breaking Changes:** [Yes/No - describe if yes]
- **Data Migration Required:** [Yes/No - describe if yes]
- **Rollback SQL:** `[rollback statement]`

---

**Proceed with migration? (yes/no)**
```

---

#### Confirmation Request

After presenting the plan, use `AskUserQuestion` tool:

```typescript
AskUserQuestion({
  questions: [{
    question: "Proceed with the schema migration as described above?",
    header: "Confirm",
    options: [
      { label: "Yes, proceed", description: "Apply the migration and update all files" },
      { label: "No, cancel", description: "Cancel the migration - no changes will be made" }
    ],
    multiSelect: false
  }]
})
```

**Only proceed to Step 5 if user confirms "Yes".**

### Step 5: Apply Migration

```
mcp__supabase__apply_migration
Name: [action]_[column]_[direction]_[table] (e.g., add_verified_at_to_users)
Query: [SQL statement]
```

Verify:
```sql
mcp__supabase__execute_sql
SELECT column_name, data_type FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'your_table';
```

### Step 6: Update Migration File

**Location:** `supabase/migrations/YYYYMMDD_description.sql`

```sql
-- Migration: [Description]
-- Date: YYYY-MM-DD
-- Type: Column [ADD/DROP/ALTER]
-- Status: APPLIED via Supabase MCP

[SQL statement]

-- Rollback (if applicable):
-- [Rollback SQL]
```

### Step 7: Update TypeScript Types

```typescript
// types/[entity].ts

export interface Entity {
  // For ADD: add the field
  new_field?: string

  // For DROP: remove the field
  // deleted_field was here
}
```

### Step 8: Update API Routes

**For ADD:** Add to SELECT, INSERT, UPDATE queries
**For DROP:** Remove from all queries

### Step 9: Update Service Files

Check if services have custom transformations that reference the column.

### Step 10: Check UI Components

**For ADD:** Add to forms/tables if needed
**For DROP:** Remove from all UI references

---

## Function Change Workflow

### Step 1: Query Existing Function

```sql
mcp__supabase__execute_sql
SELECT
  routine_name,
  routine_type,
  data_type as return_type,
  routine_definition
FROM information_schema.routines
WHERE routine_schema = 'public'
  AND routine_name = 'function_name';

-- Check function dependencies
mcp__supabase__execute_sql
SELECT
  p.proname as function_name,
  pg_get_functiondef(p.oid) as definition
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE n.nspname = 'public'
  AND p.proname = 'function_name';
```

### Step 2: Create/Replace Function

```sql
-- CREATE or REPLACE function
CREATE OR REPLACE FUNCTION public.function_name(
  p_param1 TYPE,
  p_param2 TYPE DEFAULT default_value
)
RETURNS return_type
LANGUAGE plpgsql
SECURITY INVOKER  -- or DEFINER if needed
SET search_path = ''
AS $$
DECLARE
  v_result return_type;
BEGIN
  -- Function logic using fully qualified names
  SELECT column_name
  INTO v_result
  FROM public.table_name
  WHERE condition = p_param1;

  RETURN v_result;
EXCEPTION
  WHEN OTHERS THEN
    RAISE EXCEPTION 'Error in function_name: %', SQLERRM;
END;
$$;

-- Grant permissions
GRANT EXECUTE ON FUNCTION public.function_name TO authenticated;
GRANT EXECUTE ON FUNCTION public.function_name TO anon;

-- Add comment
COMMENT ON FUNCTION public.function_name IS 'Description of what this function does';
```

### Step 3: Drop Function (if needed)

```sql
-- Check if function exists first
mcp__supabase__execute_sql
SELECT proname FROM pg_proc
WHERE proname = 'function_name';

-- Drop with signature
DROP FUNCTION IF EXISTS public.function_name(TYPE, TYPE);
```

### Step 3: Ask for Confirmation (MANDATORY)

**⚠️ CRITICAL: NEVER skip this step.**

Present the function change plan:

```markdown
## Migration Plan

**Schema Object:** `public.function_name`
**Type:** Function
**Action:** [CREATE/REPLACE/DROP]

### Function Signature:
| Parameter | Type | Default |
|-----------|------|---------|
| p_param1 | TYPE | - |
| p_param2 | TYPE | default_value |

**Returns:** return_type

### SQL to Execute:
```sql
[Function SQL statement]
```

### Files to Update:
| File | Change Required |
|------|-----------------|
| `supabase/migrations/YYYYMMDD_*.sql` | Document function |
| `supabase/setup/02_functions.sql` | Add/Update function definition |
| Application files calling this function | Update calls if signature changed |

### Dependencies to Check:
- [ ] RLS policies using this function
- [ ] Triggers using this function
- [ ] Views using this function
- [ ] Application code calling this function

---

**Proceed with function change? (yes/no)**
```

### Step 4: Update References

- Check RLS policies using the function
- Check triggers using the function
- Check views using the function
- Check application code calling the function

---

## View Change Workflow

### Step 1: Query Existing View

```sql
mcp__supabase__execute_sql
SELECT
  table_name as view_name,
  view_definition
FROM information_schema.views
WHERE table_schema = 'public'
  AND table_name = 'view_name';

-- Check view dependencies
mcp__supabase__execute_sql
SELECT
  dependent_ns.nspname as dependent_schema,
  dependent_view.relname as dependent_view
FROM pg_depend
JOIN pg_rewrite ON pg_depend.objid = pg_rewrite.oid
JOIN pg_class as dependent_view ON pg_rewrite.ev_class = dependent_view.oid
JOIN pg_namespace dependent_ns ON dependent_view.relnamespace = dependent_ns.oid
WHERE pg_depend.refobjid = 'public.view_name'::regclass;
```

### Step 2: Create/Replace View

```sql
-- CREATE or REPLACE view
CREATE OR REPLACE VIEW public.view_name AS
SELECT
  t1.id,
  t1.name,
  t2.related_field
FROM public.table1 t1
LEFT JOIN public.table2 t2 ON t1.id = t2.table1_id
WHERE t1.is_active = true;

-- Add comment
COMMENT ON VIEW public.view_name IS 'Description of view purpose';

-- Grant access (views inherit table permissions, but can be restricted)
GRANT SELECT ON public.view_name TO authenticated;
```

### Step 3: Ask for Confirmation (MANDATORY)

**⚠️ CRITICAL: NEVER skip this step.**

Present the view change plan:

```markdown
## Migration Plan

**Schema Object:** `public.view_name`
**Type:** View [Standard/Materialized]
**Action:** [CREATE/REPLACE/DROP]

### View Definition:
```sql
SELECT columns FROM tables WHERE conditions...
```

### SQL to Execute:
```sql
[View SQL statement]
```

### Files to Update:
| File | Change Required |
|------|-----------------|
| `supabase/migrations/YYYYMMDD_*.sql` | Document view |
| `supabase/setup/05_views.sql` | Add/Update view definition |
| `types/[entity].ts` | Add TypeScript type for view (if needed) |
| API routes querying this view | Update if columns changed |

### Dependencies:
- **Tables used:** [list of tables]
- **Dependent views:** [list if any]

---

**Proceed with view change? (yes/no)**
```

### Step 4: Materialized Views (if needed)

```sql
-- Create materialized view
CREATE MATERIALIZED VIEW public.mv_name AS
SELECT ...
WITH DATA;

-- Create index on materialized view
CREATE UNIQUE INDEX idx_mv_name_id ON public.mv_name(id);

-- Refresh materialized view
REFRESH MATERIALIZED VIEW CONCURRENTLY public.mv_name;
```

---

## Trigger Change Workflow

### Step 1: Query Existing Triggers

```sql
mcp__supabase__execute_sql
SELECT
  trigger_name,
  event_manipulation,
  event_object_table,
  action_timing,
  action_statement
FROM information_schema.triggers
WHERE trigger_schema = 'public'
  AND event_object_table = 'table_name';
```

### Step 2: Create Trigger Function

```sql
-- Create trigger function first
CREATE OR REPLACE FUNCTION public.trigger_function_name()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = ''
AS $$
BEGIN
  -- For INSERT/UPDATE triggers
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;

  -- For DELETE triggers
  -- RETURN OLD;
END;
$$;
```

### Step 3: Create Trigger

```sql
-- Create trigger
CREATE TRIGGER trg_table_action
  BEFORE INSERT OR UPDATE ON public.table_name
  FOR EACH ROW
  EXECUTE FUNCTION public.trigger_function_name();

-- Common trigger patterns:
-- updated_at auto-update
CREATE TRIGGER trg_table_updated_at
  BEFORE UPDATE ON public.table_name
  FOR EACH ROW
  EXECUTE FUNCTION public.update_updated_at();

-- Audit logging
CREATE TRIGGER trg_table_audit
  AFTER INSERT OR UPDATE OR DELETE ON public.table_name
  FOR EACH ROW
  EXECUTE FUNCTION public.audit_log();
```

### Step 4: Ask for Confirmation (MANDATORY)

**⚠️ CRITICAL: NEVER skip this step.**

Present the trigger change plan:

```markdown
## Migration Plan

**Schema Object:** `trg_table_action`
**Type:** Trigger
**Action:** [CREATE/DROP/ENABLE/DISABLE]

### Trigger Details:
| Property | Value |
|----------|-------|
| Table | `public.table_name` |
| Timing | BEFORE/AFTER |
| Events | INSERT/UPDATE/DELETE |
| For Each | ROW/STATEMENT |
| Function | `public.trigger_function_name()` |

### SQL to Execute:
```sql
[Trigger SQL statement]
```

### Files to Update:
| File | Change Required |
|------|-----------------|
| `supabase/migrations/YYYYMMDD_*.sql` | Document trigger |
| `supabase/setup/04_triggers.sql` | Add/Update trigger definition |
| `supabase/setup/02_functions.sql` | Add trigger function (if new) |

---

**Proceed with trigger change? (yes/no)**
```

### Step 5: Drop Trigger (if needed)

```sql
DROP TRIGGER IF EXISTS trg_name ON public.table_name;
DROP FUNCTION IF EXISTS public.trigger_function_name();
```

---

## Index Change Workflow

### Step 1: Query Existing Indexes

```sql
mcp__supabase__execute_sql
SELECT
  indexname,
  indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'table_name';

-- Check index usage
mcp__supabase__execute_sql
SELECT
  schemaname,
  relname,
  indexrelname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
  AND relname = 'table_name';
```

### Step 2: Create Index

```sql
-- Standard B-tree index
CREATE INDEX IF NOT EXISTS idx_table_column
ON public.table_name(column_name);

-- Unique index
CREATE UNIQUE INDEX IF NOT EXISTS idx_table_column_unique
ON public.table_name(column_name);

-- Composite index
CREATE INDEX IF NOT EXISTS idx_table_col1_col2
ON public.table_name(column1, column2);

-- Partial index
CREATE INDEX IF NOT EXISTS idx_table_active
ON public.table_name(column_name)
WHERE is_active = true;

-- GIN index for JSONB
CREATE INDEX IF NOT EXISTS idx_table_jsonb
ON public.table_name USING GIN (jsonb_column);

-- GiST index for full-text search
CREATE INDEX IF NOT EXISTS idx_table_search
ON public.table_name USING GIN (to_tsvector('english', text_column));
```

### Step 3: Ask for Confirmation (MANDATORY)

**⚠️ CRITICAL: NEVER skip this step.**

Present the index change plan:

```markdown
## Migration Plan

**Schema Object:** `idx_table_column`
**Type:** Index
**Action:** [CREATE/DROP]

### Index Details:
| Property | Value |
|----------|-------|
| Table | `public.table_name` |
| Columns | `column1, column2` |
| Type | B-tree/GIN/GiST/HASH |
| Unique | Yes/No |
| Partial | `WHERE condition` (if applicable) |

### SQL to Execute:
```sql
[Index SQL statement]
```

### Performance Impact:
- **Write Performance:** [Slight overhead on INSERT/UPDATE/DELETE]
- **Read Performance:** [Improved for queries on indexed columns]
- **Storage:** [Additional disk space required]

### Files to Update:
| File | Change Required |
|------|-----------------|
| `supabase/migrations/YYYYMMDD_*.sql` | Document index |

---

**Proceed with index change? (yes/no)**
```

### Step 4: Drop Index (if needed)

```sql
DROP INDEX IF EXISTS public.idx_name;
```

---

## RLS Policy Workflow

### Step 1: Query Existing Policies

```sql
mcp__supabase__execute_sql
SELECT
  policyname,
  permissive,
  roles,
  cmd,
  qual as using_expression,
  with_check as with_check_expression
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename = 'table_name';

-- Check if RLS is enabled
mcp__supabase__execute_sql
SELECT
  tablename,
  rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename = 'table_name';
```

### Step 2: Enable RLS

```sql
-- Enable RLS on table
ALTER TABLE public.table_name ENABLE ROW LEVEL SECURITY;

-- Force RLS for table owner too
ALTER TABLE public.table_name FORCE ROW LEVEL SECURITY;
```

### Step 3: Create Policies

```sql
-- SELECT policy (USING only)
CREATE POLICY "Users can view own records"
ON public.table_name
FOR SELECT
TO authenticated
USING ((SELECT auth.uid()) = user_id);

-- INSERT policy (WITH CHECK only)
CREATE POLICY "Users can insert own records"
ON public.table_name
FOR INSERT
TO authenticated
WITH CHECK ((SELECT auth.uid()) = user_id);

-- UPDATE policy (both USING and WITH CHECK)
CREATE POLICY "Users can update own records"
ON public.table_name
FOR UPDATE
TO authenticated
USING ((SELECT auth.uid()) = user_id)
WITH CHECK ((SELECT auth.uid()) = user_id);

-- DELETE policy (USING only)
CREATE POLICY "Users can delete own records"
ON public.table_name
FOR DELETE
TO authenticated
USING ((SELECT auth.uid()) = user_id);
```

### Step 4: Ask for Confirmation (MANDATORY)

**⚠️ CRITICAL: NEVER skip this step.**

Present the RLS policy change plan:

```markdown
## Migration Plan

**Schema Object:** RLS Policies for `public.table_name`
**Type:** Row Level Security
**Action:** [CREATE/ALTER/DROP/ENABLE]

### Policy Summary:
| Policy Name | Command | Roles | Action |
|-------------|---------|-------|--------|
| "Users can view own records" | SELECT | authenticated | CREATE |
| "Users can insert own records" | INSERT | authenticated | CREATE |
| "Users can update own records" | UPDATE | authenticated | CREATE |
| "Users can delete own records" | DELETE | authenticated | CREATE |

### SQL to Execute:
```sql
[RLS Policy SQL statements]
```

### Required Indexes:
| Index | Columns | Purpose |
|-------|---------|---------|
| `idx_table_user_id` | `user_id` | Policy performance |

### Security Considerations:
- **USING clause:** [Expression for SELECT/UPDATE/DELETE]
- **WITH CHECK clause:** [Expression for INSERT/UPDATE]
- **Permissive/Restrictive:** [Type]

### Files to Update:
| File | Change Required |
|------|-----------------|
| `supabase/migrations/YYYYMMDD_*.sql` | Document policies |
| `supabase/setup/03_policies.sql` | Add/Update policy definitions |

---

**Proceed with RLS policy change? (yes/no)**
```

### Step 5: Create Required Indexes

```sql
-- ALWAYS create indexes on columns used in policies
CREATE INDEX IF NOT EXISTS idx_table_user_id
ON public.table_name(user_id);
```

---

## Common Patterns

### Standard Column Types

| Purpose | PostgreSQL Type | TypeScript Type | Default |
|---------|-----------------|-----------------|---------|
| Primary key | `UUID` | `string` | `gen_random_uuid()` |
| Foreign key | `UUID REFERENCES table(id)` | `string` | none |
| Boolean flag | `BOOLEAN` | `boolean` | `false` |
| Short text | `VARCHAR(n)` | `string` | `''` or `null` |
| Long text | `TEXT` | `string` | `''` or `null` |
| Timestamp | `TIMESTAMPTZ` | `string` | `now()` or `null` |
| Integer | `INTEGER` | `number` | `0` or `null` |
| Decimal | `NUMERIC(p,s)` | `number` | `0` or `null` |
| JSON | `JSONB` | `Record<string, any>` | `'{}'::jsonb` |
| Array | `TYPE[]` | `TYPE[]` | `'{}'` |
| Enum | `custom_enum` | `string` (union) | first value |

### File Location Patterns

| Layer | Location Pattern |
|-------|------------------|
| Types | `types/[entity].ts` |
| API Routes | `app/api/[module]/route.ts` |
| API Single | `app/api/[module]/[id]/route.ts` |
| Services | `services/[module]/[entity]-service.ts` or `lib/services/[module]/` |
| Hooks | `hooks/[module]/use-[entity].ts` |
| Pages | `app/[route-group]/[module]/page.tsx` |
| Migrations | `supabase/migrations/YYYYMMDD_*.sql` |
| Functions | `supabase/setup/02_functions.sql` |
| Views | `supabase/setup/05_views.sql` |
| Policies | `supabase/setup/03_policies.sql` |
| Triggers | `supabase/setup/04_triggers.sql` |

---

## Completion Checklist

### For Column Changes
- [ ] Current schema queried via MCP
- [ ] Changes validated (existence, dependencies)
- [ ] Migration query created
- [ ] User confirmation received
- [ ] Migration applied and verified
- [ ] Migration file documented
- [ ] TypeScript types updated
- [ ] API routes updated
- [ ] Service files checked
- [ ] UI components checked

### For Function/View/Trigger Changes
- [ ] Existing object queried via MCP
- [ ] Dependencies checked
- [ ] Object created/modified
- [ ] Permissions granted
- [ ] Callers/references updated
- [ ] Migration file documented

### For RLS Policy Changes
- [ ] Existing policies queried
- [ ] RLS enabled on table
- [ ] Policies created (SELECT, INSERT, UPDATE, DELETE separately)
- [ ] Required indexes created
- [ ] Policies tested with different roles

---

## Integration with TodoWrite

```typescript
// Column change todo list
[
  { content: "Query current schema via MCP", status: "pending", activeForm: "Querying schema" },
  { content: "Validate changes", status: "pending", activeForm: "Validating changes" },
  { content: "Create migration query", status: "pending", activeForm: "Creating query" },
  { content: "Get user confirmation", status: "pending", activeForm: "Getting confirmation" },
  { content: "Apply migration via MCP", status: "pending", activeForm: "Applying migration" },
  { content: "Update migration file", status: "pending", activeForm: "Updating migration file" },
  { content: "Update TypeScript types", status: "pending", activeForm: "Updating types" },
  { content: "Update API routes", status: "pending", activeForm: "Updating API routes" },
  { content: "Update service files", status: "pending", activeForm: "Updating services" },
  { content: "Check UI components", status: "pending", activeForm: "Checking UI" }
]

// Function/View change todo list
[
  { content: "Query existing object via MCP", status: "pending", activeForm: "Querying object" },
  { content: "Check dependencies", status: "pending", activeForm: "Checking dependencies" },
  { content: "Create/modify object", status: "pending", activeForm: "Creating object" },
  { content: "Grant permissions", status: "pending", activeForm: "Granting permissions" },
  { content: "Update callers/references", status: "pending", activeForm: "Updating references" },
  { content: "Document in migration file", status: "pending", activeForm: "Documenting" }
]
```

---

## MCP Commands Quick Reference

```
# List all tables
mcp__supabase__list_tables

# Execute SQL query
mcp__supabase__execute_sql
Query: [SQL]

# Apply migration
mcp__supabase__apply_migration
Name: [migration_name]
Query: [SQL]

# List migrations
mcp__supabase__list_migrations

# Get logs
mcp__supabase__get_logs
Service: postgres

# Generate TypeScript types
mcp__supabase__generate_typescript_types
```

---

**Skill Version:** 2.1.0
**Updated:** 2025-12-30
**Compatibility:** Any Next.js + Supabase project

### Changelog
- **v2.1.0** - Added mandatory confirmation step with detailed Migration Plan templates for all schema change types (Column, Function, View, Trigger, Index, RLS Policy)
- **v2.0.0** - Extended to support functions, views, triggers, indexes, RLS policies; made project-agnostic
- **v1.0.0** - Initial column-focused workflow for JKKN COE project
