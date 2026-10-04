---
license: Apache-2.0
name: supabase-admin
description: Supabase administration, RLS policies, migrations, and schema design. Use for database architecture, Row Level Security, performance tuning, auth integration. Activate on "Supabase", "RLS", "migration", "policy", "schema", "auth.uid()". NOT for Supabase Auth UI configuration (use dashboard), edge functions (use cloudflare-worker-dev), or general SQL without Supabase context.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - mcp__supabase__*
category: DevOps & Infrastructure
tags:
  - supabase
  - rls
  - database
  - postgres
  - migration
  - schema
  - security
---

# Supabase Administration Expert

Master Supabase schema design, Row Level Security policies, migrations, and performance optimization for production applications.

## Decision Points

### 1. RLS Pattern Selection
```
Check data sensitivity & access patterns:
├── Public content (blogs, docs)
│   └── Use: Public read + owner write policies
├── User-owned data (profiles, settings)
│   └── Use: Owner-only access (auth.uid() = user_id)
├── Multi-tenant (org data)
│   ├── Small orgs (<1000 users): RLS with org_id filter
│   └── Large orgs (>1000 users): Schema per tenant
└── Admin content (system config)
    └── Use: Role-based policies with profiles.role check
```

### 2. Delete Strategy Decision Tree
```
Evaluate data retention needs:
├── Needs audit trail or recovery?
│   ├── High compliance: Soft delete (deleted_at timestamp)
│   └── Medium compliance: Soft delete + cascade trigger
├── Performance critical with large volume?
│   ├── Yes: Hard delete with CASCADE
│   └── No: Soft delete acceptable
└── Referenced by other tables?
    ├── Critical refs: Use ON DELETE RESTRICT
    └── Clean cascade: Use ON DELETE CASCADE
```

### 3. Migration Risk Assessment
```
Check change impact:
├── Schema changes
│   ├── Adding nullable column: Low risk, deploy anytime
│   ├── Adding NOT NULL: Medium risk, needs backfill
│   └── Dropping column: High risk, needs staged deployment
├── RLS policy changes
│   ├── Relaxing permissions: Low risk
│   └── Restricting access: High risk, test with real data
└── Index changes
    ├── Creating index: Use CONCURRENTLY flag
    └── Dropping index: Check query performance impact first
```

## Failure Modes

### Schema Bloat Anti-Pattern
**Symptoms:** Tables with 20+ columns, nullable columns everywhere, poor query performance
**Detection:** `SELECT count(*) FROM information_schema.columns WHERE table_name = 'bloated_table'` returns >15
**Fix:** Normalize into related tables, use JSONB for flexible attributes, add NOT NULL constraints with defaults

### RLS Performance Killer
**Symptoms:** Queries taking >1000ms, high CPU on simple selects, missing auth.uid() in WHERE clauses
**Detection:** `EXPLAIN ANALYZE` shows sequential scans on user_id columns without indexes
**Fix:** Add `CREATE INDEX idx_table_user_id ON table(user_id)` for every RLS-filtered column

### Migration Lock Hell
**Symptoms:** Deployment timeouts, blocked writes during migration, "relation does not exist" errors
**Detection:** Migration contains `ALTER TABLE ADD COLUMN x NOT NULL` without DEFAULT
**Fix:** Split into: 1) Add nullable column with default, 2) Backfill data, 3) Add NOT NULL constraint

### JWT Parsing Overload
**Symptoms:** RLS policies calling auth.uid() for every row, poor performance on large tables
**Detection:** Policy has `auth.uid() = user_id` in USING clause without subquery
**Fix:** Rewrite as `user_id = (SELECT auth.uid())` to parse JWT once per query

### Cascade Confusion
**Symptoms:** Data disappearing unexpectedly, orphaned records, referential integrity errors
**Detection:** Foreign keys without explicit ON DELETE behavior, surprise empty result sets
**Fix:** Explicitly set ON DELETE CASCADE/RESTRICT/SET NULL based on business logic

## Worked Examples

### Multi-Tenant RLS with Performance Optimization

**Scenario:** SaaS app where users belong to organizations, need org-isolated data

**Step 1: Schema Design Decision**
```sql
-- Decision: Use org_id column vs separate schemas
-- Trade-off: RLS filtering vs complete isolation
-- Choice: RLS (easier ops, shared resources)

CREATE TABLE posts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id uuid NOT NULL REFERENCES organizations(id),
  user_id uuid NOT NULL REFERENCES auth.users(id),
  content text NOT NULL,
  created_at timestamptz DEFAULT now()
);
```

**Step 2: Index Strategy (Critical for Performance)**
```sql
-- Compound index: org_id first (highest selectivity for RLS)
CREATE INDEX idx_posts_org_user ON posts(org_id, user_id);
-- Single index for user lookups
CREATE INDEX idx_posts_user ON posts(user_id);
```

**Step 3: RLS Policy with Org Context**
```sql
-- Get user's org_id from profiles table
CREATE POLICY "Org members only" ON posts
  FOR ALL USING (
    org_id = (
      SELECT profiles.org_id 
      FROM profiles 
      WHERE profiles.id = auth.uid()
    )
  );
```

**Step 4: Performance Validation**
```sql
-- Test query performance
EXPLAIN ANALYZE 
SELECT * FROM posts 
WHERE org_id = 'test-org-id' 
LIMIT 10;
-- Should show Index Scan, not Seq Scan
-- Should be <100ms for tables with <1M rows
```

**Expert Insight:** Novices miss the compound index ordering. They create `(user_id, org_id)` which forces RLS to scan all user posts then filter by org. Experts put org_id first since RLS filters by org membership.

## Quality Gates

RLS audit checklist - all must pass before production:

- [ ] All user tables have `ALTER TABLE x ENABLE ROW LEVEL SECURITY`
- [ ] Every auth.uid() reference has corresponding index on user_id column  
- [ ] RLS policies tested with `SET ROLE anon` and real user JWTs
- [ ] `EXPLAIN ANALYZE` shows Index Scan (not Seq Scan) for auth queries
- [ ] Policy queries execute in <100ms with production data volume
- [ ] Migration tested on copy of production data (not empty dev DB)
- [ ] No `ALTER TABLE ADD COLUMN x NOT NULL` without DEFAULT in single transaction
- [ ] Foreign key constraints have explicit ON DELETE behavior (not default)
- [ ] Full-text search uses GIN indexes, not LIKE queries
- [ ] Auth triggers handle edge cases (profile creation failures, duplicate emails)

## NOT-FOR Boundaries

**Do NOT use this skill for:**

- **Supabase Auth UI styling/configuration** → Use Supabase dashboard documentation
- **Edge Functions development** → Use `cloudflare-worker-dev` skill instead  
- **Client-side Supabase SDK** → Use official Supabase JavaScript docs
- **General PostgreSQL optimization** → Use `postgresql-dba` skill for non-Supabase context
- **Real-time subscriptions setup** → Use Supabase Realtime documentation
- **Storage bucket policies** → Use Supabase Storage documentation

**When to delegate:**
- Complex analytical queries → `postgresql-dba` skill
- Frontend integration → Framework-specific skills
- DevOps deployment → `docker-deployment` or `kubernetes-ops` skills