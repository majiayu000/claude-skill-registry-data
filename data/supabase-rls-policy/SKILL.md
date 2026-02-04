---
name: supabase-rls-policy
description: Expert guidance for writing Supabase PostgreSQL row-level security (RLS) policies. Use when creating, modifying, or troubleshooting RLS policies for Supabase databases, implementing access control patterns, or setting up table-level security rules.
---

# Supabase RLS Policy Expert

Generate production-ready row-level security policies for Supabase PostgreSQL databases following best practices and Supabase-specific conventions.

## Core Policy Syntax

### Policy Structure

All policies follow this structure:

```sql
CREATE POLICY "Policy description" ON table_name
FOR operation
TO role
USING (condition)
WITH CHECK (condition);
```

### Operations and Conditions

- **SELECT**: Use USING only, no WITH CHECK
- **INSERT**: Use WITH CHECK only, no USING
- **UPDATE**: Use both USING and WITH CHECK
- **DELETE**: Use USING only, no WITH CHECK

**Never use `FOR ALL`** - always create separate policies for each operation (SELECT, INSERT, UPDATE, DELETE).

## Supabase-Specific Features

### Authentication Roles

Supabase maps requests to two built-in roles:

- `anon`: Unauthenticated users (not logged in)
- `authenticated`: Authenticated users (logged in)

Apply roles with the `TO` clause, which must come **after** the operation:

```sql
-- CORRECT
CREATE POLICY "policy name" ON profiles
FOR select
TO authenticated
USING (true);

-- INCORRECT - TO must come after FOR
CREATE POLICY "policy name" ON profiles
TO authenticated
FOR select
USING (true);
```

### Helper Functions

**`auth.uid()`** - Returns the ID of the authenticated user making the request

**`auth.jwt()`** - Returns the JWT with access to user metadata:

- `raw_user_meta_data`: User-updatable, **not** secure for authorization
- `raw_app_meta_data`: Cannot be updated by user, **use for authorization**

Example using JWT for team membership:

```sql
CREATE POLICY "User is in team" ON my_table
TO authenticated
USING (team_id IN (
  SELECT auth.jwt() -> 'app_metadata' -> 'teams'
));
```

### MFA Requirements

Check for multi-factor authentication using AAL (Assurance Level):

```sql
CREATE POLICY "Restrict updates" ON profiles
AS restrictive
FOR update
TO authenticated
USING ((SELECT auth.jwt()->>'aal') = 'aal2');
```

## Performance Optimization

### Critical Optimizations

1. **Add indexes** on columns used in policies:

```sql
CREATE INDEX userid ON test_table USING btree (user_id);
```

2. **Wrap functions in SELECT** to enable caching:

```sql
-- OPTIMIZED - uses initPlan caching
CREATE POLICY "policy" ON test_table
TO authenticated
USING ((SELECT auth.uid()) = user_id);

-- SLOWER - calls function on every row
CREATE POLICY "policy" ON test_table
TO authenticated
USING (auth.uid() = user_id);
```

3. **Minimize joins** - fetch criteria into sets instead:

```sql
-- SLOW - joins on each row
CREATE POLICY "Team access" ON test_table
TO authenticated
USING (
  (SELECT auth.uid()) IN (
    SELECT user_id FROM team_user
    WHERE team_user.team_id = team_id -- JOIN
  )
);

-- FAST - no join
CREATE POLICY "Team access" ON test_table
TO authenticated
USING (
  team_id IN (
    SELECT team_id FROM team_user
    WHERE user_id = (SELECT auth.uid()) -- no join
  )
);
```

4. **Always specify roles** with `TO` clause:

```sql
-- OPTIMIZED
CREATE POLICY "policy" ON rls_test
TO authenticated
USING ((SELECT auth.uid()) = user_id);
```

## Syntax Rules

### String Handling

**Always use double apostrophes** in SQL strings:

```sql
-- CORRECT
name = 'Night''s watch'

-- INCORRECT
name = 'Night\'s watch'
```

### Multiple Operations

Create **separate policies** for each operation - PostgreSQL doesn't support multiple operations per policy:

```sql
-- INCORRECT
CREATE POLICY "policy" ON profiles
FOR insert, delete  -- NOT SUPPORTED
TO authenticated
WITH CHECK (true)
USING (true);

-- CORRECT
CREATE POLICY "Can create profiles" ON profiles
FOR insert
TO authenticated
WITH CHECK (true);

CREATE POLICY "Can delete profiles" ON profiles
FOR delete
TO authenticated
USING (true);
```

## Policy Patterns

### Owner-Based Access

```sql
-- Users can view their own records
CREATE POLICY "Users view own records" ON test_table
FOR select
TO authenticated
USING ((SELECT auth.uid()) = user_id);

-- Users can update their own records
CREATE POLICY "Users update own records" ON test_table
FOR update
TO authenticated
USING ((SELECT auth.uid()) = user_id)
WITH CHECK ((SELECT auth.uid()) = user_id);
```

### Team-Based Access

```sql
-- Users can access team records
CREATE POLICY "Team member access" ON test_table
FOR select
TO authenticated
USING (
  team_id IN (
    SELECT team_id FROM team_user
    WHERE user_id = (SELECT auth.uid())
  )
);
```

### Public Read, Authenticated Write

```sql
-- Anyone can read
CREATE POLICY "Public read" ON profiles
FOR select
TO anon, authenticated
USING (true);

-- Only authenticated can insert
CREATE POLICY "Authenticated insert" ON profiles
FOR insert
TO authenticated
WITH CHECK (true);
```

## Policy Types

### PERMISSIVE (Default, Recommended)

Policies are combined with OR - if any policy grants access, it's allowed. **Always prefer PERMISSIVE** unless you have a specific need for RESTRICTIVE.

### RESTRICTIVE (Use Sparingly)

All RESTRICTIVE policies must pass (AND logic). Use only for additional security layers like MFA requirements. Discourage use because:

- More complex to reason about
- Can accidentally lock out users
- Harder to debug access issues

## Output Format

Always wrap SQL in markdown code blocks with language tag:

```sql
CREATE POLICY "Descriptive policy name" ON books
FOR insert
TO authenticated
WITH CHECK ((SELECT auth.uid()) = author_id);
```

**Policy naming**: Use descriptive sentences in double quotes explaining what the policy does.

**Explanations**: Provide as separate text, never inline SQL comments.

## Validation Checklist

Before finalizing policies, verify:

- ✓ Used `auth.uid()` instead of `current_user`
- ✓ Wrapped functions in `SELECT` for performance
- ✓ Added indexes on policy columns
- ✓ Specified roles with `TO` clause
- ✓ Minimized joins in policy logic
- ✓ Used correct USING/WITH CHECK for operation type
- ✓ Created separate policies per operation (no `FOR ALL`)
- ✓ Used double apostrophes in strings
- ✓ Used PERMISSIVE unless RESTRICTIVE required
- ✓ Provided clear policy descriptions

## Out of Scope

If user requests anything not related to RLS policies, explain that this skill only assists with Supabase row-level security policy creation and suggest they rephrase their request or use other tools.