---
name: create-migration
description: Create Supabase migration with RLS validation and best practices
disable-model-invocation: true
---

# Create Migration Skill

## Purpose

Create Supabase migrations with proper RLS policies, following Arch Systems security patterns.

## Process

1. **Ask for migration details:**

   - Table name (or existing table to modify)
   - Columns and types
   - Who should have access (which departments/roles)
   - Should it be append-only (like daily_logs)?

2. **Generate migration file:**

   - Create in `packages/database/migrations/`
   - Naming: `YYYYMMDDHHMMSS_<description>.sql`
   - Include: table creation, RLS enable, policies, indexes

3. **RLS Policy Checklist:**

   - [ ] `ENABLE ROW LEVEL SECURITY`
   - [ ] SELECT policy for authorized users
   - [ ] INSERT policy (with department check if needed)
   - [ ] UPDATE policy (restrict to appropriate users)
   - [ ] DELETE policy (often none for audit tables)
   - [ ] Use `auth.user_department_id()` for department isolation
   - [ ] Use `auth.is_admin()` for admin-only access

4. **TypeScript types:**
   - Run `pnpm --filter @repo/supabase gen-types` to regenerate types after migration changes
   - If the script does not exist, note that types need regeneration

## Template

```sql
-- Create table
CREATE TABLE IF NOT EXISTS schema.table_name (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  -- add columns here
  department_id UUID REFERENCES departments(id) DEFAULT auth.user_department_id()
);

-- Enable RLS
ALTER TABLE schema.table_name ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY select_authorized ON schema.table_name
  FOR SELECT USING (
    auth.is_admin() OR
    auth.has_department_access(department_id)
  );

CREATE POLICY insert_authorized ON schema.table_name
  FOR INSERT WITH CHECK (
    auth.is_admin() OR
    auth.has_department_access(department_id)
  );

-- Indexes
CREATE INDEX idx_table_name_department ON schema.table_name(department_id);
CREATE INDEX idx_table_name_created_at ON schema.table_name(created_at DESC);
```

## After Creation

1. Push to local Supabase: `pnpm --filter @repo/database supabase:push`
2. Test in Supabase Studio
3. Commit migration file
