---
name: supabase-rls
description: Supabase Row-Level Security for multi-tenancy. Use when implementing database security, tenant isolation, or access control. Triggers on mentions of RLS, row-level security, multi-tenant, tenant isolation, or database policies.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Supabase Row-Level Security (RLS)

## Why RLS?

RLS ensures data isolation between tenants (organizations) at the database level. Even if application code has bugs, users can never access other organizations' data.

## Multi-Tenant Architecture

```
Organization (tenant boundary)
└── Users (belong to org)
└── Venues (belong to org)
    └── Zones (belong to venue)
        └── Schedules, etc.
```

## Enable RLS

```sql
-- Always enable RLS on tenant tables
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE venues ENABLE ROW LEVEL SECURITY;
ALTER TABLE zones ENABLE ROW LEVEL SECURITY;
ALTER TABLE schedules ENABLE ROW LEVEL SECURITY;
ALTER TABLE playlists ENABLE ROW LEVEL SECURITY;
ALTER TABLE tracks ENABLE ROW LEVEL SECURITY;
```

## Policy Patterns

### Direct Organization Reference

For tables with `organization_id`:

```sql
-- Users can only see their organization
CREATE POLICY org_isolation ON venues
  FOR ALL
  USING (organization_id = (
    SELECT organization_id FROM users
    WHERE id = auth.uid()
  ));
```

### Indirect Reference (Through Parent)

For tables related through hierarchy:

```sql
-- Zones: check via venue → organization
CREATE POLICY zone_org_policy ON zones
  FOR ALL
  USING (venue_id IN (
    SELECT id FROM venues
    WHERE organization_id = (
      SELECT organization_id FROM users
      WHERE id = auth.uid()
    )
  ));

-- Schedules: check via zone → venue → organization
CREATE POLICY schedule_org_policy ON schedules
  FOR ALL
  USING (zone_id IN (
    SELECT z.id FROM zones z
    JOIN venues v ON z.venue_id = v.id
    WHERE v.organization_id = (
      SELECT organization_id FROM users
      WHERE id = auth.uid()
    )
  ));
```

### Separate Policies per Operation

```sql
-- SELECT: all org members can view
CREATE POLICY venues_select ON venues
  FOR SELECT
  USING (organization_id = get_user_org_id());

-- INSERT: only admins can create
CREATE POLICY venues_insert ON venues
  FOR INSERT
  WITH CHECK (
    organization_id = get_user_org_id()
    AND is_org_admin()
  );

-- UPDATE: only admins can modify
CREATE POLICY venues_update ON venues
  FOR UPDATE
  USING (organization_id = get_user_org_id())
  WITH CHECK (is_org_admin());

-- DELETE: only admins can delete
CREATE POLICY venues_delete ON venues
  FOR DELETE
  USING (organization_id = get_user_org_id() AND is_org_admin());
```

## Helper Functions

Create reusable functions for cleaner policies:

```sql
-- Get current user's organization ID
CREATE OR REPLACE FUNCTION get_user_org_id()
RETURNS UUID AS $$
  SELECT organization_id FROM users WHERE id = auth.uid()
$$ LANGUAGE SQL SECURITY DEFINER STABLE;

-- Check if current user is an admin
CREATE OR REPLACE FUNCTION is_org_admin()
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1 FROM users
    WHERE id = auth.uid() AND role = 'admin'
  )
$$ LANGUAGE SQL SECURITY DEFINER STABLE;

-- Check if user has access to venue
CREATE OR REPLACE FUNCTION can_access_venue(venue_id UUID)
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1 FROM venues
    WHERE id = venue_id
    AND organization_id = get_user_org_id()
  )
$$ LANGUAGE SQL SECURITY DEFINER STABLE;
```

## Simplified Policies with Functions

```sql
CREATE POLICY venues_policy ON venues
  FOR ALL
  USING (organization_id = get_user_org_id());

CREATE POLICY zones_policy ON zones
  FOR ALL
  USING (can_access_venue(venue_id));
```

## Shared Content (System Library)

For content shared across organizations:

```sql
-- Tracks: org-specific OR system library (org_id IS NULL)
CREATE POLICY tracks_policy ON tracks
  FOR SELECT
  USING (
    organization_id IS NULL  -- System library
    OR organization_id = get_user_org_id()  -- Org's own tracks
  );

-- Only org admins can modify their org's tracks
CREATE POLICY tracks_modify ON tracks
  FOR INSERT UPDATE DELETE
  USING (
    organization_id = get_user_org_id()
    AND is_org_admin()
  );
```

## Service Role Bypass

The Supabase service role key bypasses RLS. Use for:
- Cron jobs
- Admin operations
- Cross-org analytics

```typescript
import { createClient } from '@supabase/supabase-js';

// This client bypasses RLS
const supabaseAdmin = createClient(
  SUPABASE_URL,
  SUPABASE_SERVICE_ROLE_KEY
);

// This client respects RLS
const supabase = createClient(
  SUPABASE_URL,
  SUPABASE_ANON_KEY
);
```

## Testing RLS

```sql
-- Test as a specific user
SET request.jwt.claim.sub = 'user-uuid-here';

-- Now queries will use RLS
SELECT * FROM venues; -- Should only show user's org venues

-- Reset
RESET request.jwt.claim.sub;
```

## Common Mistakes

1. **Forgetting to enable RLS** - Table is open to all
2. **Using auth.uid() in SECURITY INVOKER functions** - Use SECURITY DEFINER
3. **Complex subqueries** - Create helper functions instead
4. **No policy = no access** - RLS blocks all access by default when enabled
5. **Service role in frontend** - Never expose service role key

## Performance Tips

1. **Index foreign keys** used in policies
2. **Use SECURITY DEFINER functions** to cache user info
3. **Avoid deep joins** in policies - use materialized helper tables if needed
4. **Test query plans** with EXPLAIN ANALYZE
