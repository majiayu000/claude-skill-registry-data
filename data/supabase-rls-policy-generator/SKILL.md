---
name: supabase-rls-policy-generator
description: This skill should be used when the user requests to generate, create, or add Row-Level Security (RLS) policies for Supabase databases in multi-tenant or role-based applications. It generates comprehensive RLS policies using auth.uid(), auth.jwt() claims, and role-based access patterns. Trigger terms include RLS, row level security, supabase security, generate policies, auth policies, multi-tenant security, role-based access, database security policies, supabase permissions, tenant isolation.
---

# Supabase RLS Policy Generator

To generate comprehensive Row-Level Security policies for Supabase databases, follow these steps systematically.

## Step 1: Analyze Current Schema

Before generating policies:
1. Ask user for the database schema file path or table names
2. Read the schema to understand table structures, foreign keys, and relationships
3. Identify tables that need RLS protection
4. Determine the security model: multi-tenant, role-based, or hybrid

## Step 2: Identify Security Requirements

Determine access patterns by asking:
- Is this a multi-tenant application? (tenant_id isolation)
- What roles exist in the system? (admin, user, viewer, etc.)
- Are there public vs private resources?
- Do users need to share resources across accounts?
- Are there hierarchical permissions? (organization > team > user)

Consult `references/rls-patterns.md` for common security patterns.

## Step 3: Generate RLS Policies

For each table requiring protection, generate policies following this structure:

### Enable RLS
```sql
ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;
```

### Policy Types to Generate

**SELECT Policies** - Control read access:
- User can view their own records
- User can view records in their tenant
- Role-based viewing (admins see all)
- Public records accessible to all authenticated users

**INSERT Policies** - Control creation:
- User can create records with their own user_id
- User can create records in their tenant
- Role-based creation restrictions

**UPDATE Policies** - Control modifications:
- User can update their own records
- Admins can update all records
- Tenant-scoped updates

**DELETE Policies** - Control deletion:
- User can delete their own records
- Admin-only deletion
- Tenant-scoped deletion

### Policy Templates

Use templates from `assets/policy-templates.sql`:

**Basic User Ownership**:
```sql
CREATE POLICY "Users can view own records"
  ON table_name FOR SELECT
  USING (auth.uid() = user_id);
```

**Multi-Tenant Isolation**:
```sql
CREATE POLICY "Tenant isolation"
  ON table_name FOR ALL
  USING (
    tenant_id IN (
      SELECT tenant_id FROM user_tenants
      WHERE user_id = auth.uid()
    )
  );
```

**Role-Based Access**:
```sql
CREATE POLICY "Admins have full access"
  ON table_name FOR ALL
  USING (
    auth.jwt() ->> 'role' = 'admin'
  );
```

**JWT Claims**:
```sql
CREATE POLICY "Organization access"
  ON table_name FOR SELECT
  USING (
    organization_id = (auth.jwt() -> 'app_metadata' ->> 'organization_id')::uuid
  );
```

## Step 4: Generate Helper Functions

Create PostgreSQL functions to support complex policies:

```sql
-- Function to check user role
CREATE OR REPLACE FUNCTION auth.user_has_role(required_role TEXT)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN (auth.jwt() ->> 'role') = required_role;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to check tenant membership
CREATE OR REPLACE FUNCTION auth.user_in_tenant(target_tenant_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM user_tenants
    WHERE user_id = auth.uid()
    AND tenant_id = target_tenant_id
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## Step 5: Generate Testing Queries

Create test queries to verify policies work correctly:

```sql
-- Test as authenticated user
SET request.jwt.claim.sub = 'user-uuid';
SELECT * FROM table_name; -- Should see only accessible records

-- Test as admin
SET request.jwt.claim.role = 'admin';
SELECT * FROM table_name; -- Should see all records

-- Test as different tenant
SET request.jwt.claim.sub = 'other-user-uuid';
SELECT * FROM table_name; -- Should see different tenant's records
```

## Step 6: Create Migration File

Generate a migration file with proper structure:

```sql
-- Migration: Add RLS policies
-- Created: [timestamp]

-- Enable RLS on tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE items ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if any
DROP POLICY IF EXISTS "policy_name" ON table_name;

-- Create new policies
[Generated policies here]

-- Create helper functions
[Generated functions here]

-- Grant necessary permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON table_name TO authenticated;
GRANT SELECT ON table_name TO anon; -- If public read needed
```

## Step 7: Document Generated Policies

Create documentation explaining:
- What each policy does
- Which users/roles have what access
- Any special cases or exceptions
- How to test the policies
- Common troubleshooting tips

Use template from `assets/policy-documentation-template.md`.

## Implementation Guidelines

### Security Best Practices
- Always enable RLS on tables with user data
- Use auth.uid() for user-owned records
- Use JWT claims for role-based access
- Prefer SECURITY DEFINER functions for complex logic
- Test policies with different user roles
- Use USING clause for read access, WITH CHECK for write validation

### Performance Considerations
- Add indexes on columns used in policies (user_id, tenant_id, role)
- Keep policy logic simple for better performance
- Use helper functions for reusable complex logic
- Avoid subqueries in policies when possible

### Common Patterns

Consult `references/rls-patterns.md` for detailed examples of:
- Multi-tenant isolation
- Role-based access control (RBAC)
- Attribute-based access control (ABAC)
- Hierarchical permissions
- Public/private resource splitting
- Shared resource access

## Output Format

Generate files in the following structure:
```
migrations/
  [timestamp]_add_rls_policies.sql
docs/
  rls-policies.md (documentation)
tests/
  rls_tests.sql (test queries)
```

## Verification Checklist

Before completing:
- [ ] RLS enabled on all sensitive tables
- [ ] Policies cover all operations (SELECT, INSERT, UPDATE, DELETE)
- [ ] Policies tested with different user roles
- [ ] Indexes added for policy columns
- [ ] Helper functions created for complex logic
- [ ] Documentation generated
- [ ] Test queries provided
- [ ] No policies accidentally grant excessive access

## Consulting References

Throughout generation:
- Consult `references/rls-patterns.md` for security patterns
- Consult `references/supabase-auth.md` for auth.uid() and JWT structure
- Use templates from `assets/policy-templates.sql`

## Completion

When finished:
1. Display the generated migration file
2. Summarize the policies created
3. Provide testing instructions
4. Offer to generate additional policies or modify existing ones
