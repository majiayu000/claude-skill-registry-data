---
name: setup-rls
description: Configure Row Level Security policies for Supabase tables to control data access. Triggers when user mentions security, permissions, access control, or RLS policies.
allowed-tools: Read, Write, Edit, Grep
---

# RLS Setup Skill

Configure comprehensive Row Level Security policies for Supabase tables.

## Purpose

Implement secure, performant RLS policies that control data access at the database level.

## When to Use

- User needs to secure table data
- Requests permission-based access
- Mentions RLS, security, or access control
- Asks about user data isolation
- Needs role-based access control

## Instructions

1. **Analyze Access Requirements**
   - Who can read data?
   - Who can create/update/delete?
   - Any special permission rules?
   - Multi-tenant considerations?

2. **Enable RLS**
   ```sql
   ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;
   ```

3. **Create Policies**
   - One policy per operation type (SELECT, INSERT, UPDATE, DELETE)
   - Use descriptive policy names
   - Wrap auth functions in SELECT for performance
   - Consider restrictive policies for additional security

4. **Test Policies**
   - Test as different users
   - Verify expected access
   - Check performance impact

## Common Policy Patterns

### User Owns Record
```sql
CREATE POLICY "Users can view own records"
  ON table_name FOR SELECT
  USING ((SELECT auth.uid()) = user_id);
```

### Public Read, Authenticated Write
```sql
CREATE POLICY "Public read access"
  ON table_name FOR SELECT
  USING (true);

CREATE POLICY "Authenticated users can insert"
  ON table_name FOR INSERT
  WITH CHECK (auth.role() = 'authenticated');
```

### Multi-tenant Isolation
```sql
CREATE POLICY "Users see only their tenant data"
  ON table_name FOR ALL
  USING (
    tenant_id = (SELECT auth.jwt()->>'tenant_id')::UUID
  );
```

### Restrictive MFA Policy
```sql
CREATE POLICY "Require MFA for updates"
  ON sensitive_table FOR UPDATE
  AS RESTRICTIVE
  TO authenticated
  USING ((SELECT auth.jwt()->>'aal') = 'aal2');
```

## Output Format

1. Complete RLS policy SQL
2. Explanation of each policy
3. Testing instructions
4. Performance optimization notes
