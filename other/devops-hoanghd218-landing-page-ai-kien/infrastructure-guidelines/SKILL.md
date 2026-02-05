---
name: infrastructure-guidelines
description: Infrastructure guidelines for A4C-AppSuite. Covers idempotent Supabase SQL migrations with RLS policies, Kubernetes deployments for Temporal workers, CQRS projections with PostgreSQL triggers, and AsyncAPI contract-first event design. Emphasizes safety, idempotency, and SQL-first development.
version: 1.0.0
tags: [infrastructure, supabase, kubernetes, postgresql, rls, cqrs, events, asyncapi, sql, migrations]
---

# Infrastructure Guidelines

Infrastructure patterns for the A4C-AppSuite monorepo. This skill covers:

- **Supabase SQL**: Idempotent migrations, RLS policies with JWT claims, event triggers
- **Kubernetes**: Temporal worker deployments, namespace organization, resource management
- **CQRS**: Projection tables, event-driven triggers, read model optimization
- **AsyncAPI**: Contract-first event schema design, schema registry, event versioning

## Quick Start

### Creating a New Database Migration

> **CRITICAL: Always use `supabase migration new` - NEVER manually create migration files**
>
> The Supabase CLI automatically generates the correct UTC timestamp. Manually creating
> files with hand-typed timestamps causes migration ordering errors that break CI/CD.
>
> ```bash
> # ✅ CORRECT: CLI generates timestamp (e.g., 20251223193037_feature_name.sql)
> supabase migration new feature_name
>
> # ❌ WRONG: Manual file creation with invented timestamp
> touch supabase/migrations/20251223120000_feature_name.sql
> # This WILL break if timestamp is earlier than already-deployed migrations
> ```

```bash
# Create a new migration file via Supabase CLI
cd infrastructure/supabase
supabase migration new add_my_table

# Edit the generated file: supabase/migrations/YYYYMMDDHHMMSS_add_my_table.sql
# Write idempotent SQL:

-- Create table with idempotent pattern
CREATE TABLE IF NOT EXISTS my_table (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID NOT NULL REFERENCES organizations(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Create RLS policy using JWT claims (drop first for idempotency)
DROP POLICY IF EXISTS my_table_tenant_isolation ON my_table;
CREATE POLICY my_table_tenant_isolation
  ON my_table
  FOR ALL
  USING (org_id = (current_setting('request.jwt.claims', true)::json->>'org_id')::uuid);

-- Enable RLS
ALTER TABLE my_table ENABLE ROW LEVEL SECURITY;

# Test and deploy
export SUPABASE_ACCESS_TOKEN="your-token"
supabase link --project-ref "your-project-ref"
supabase db push --linked --dry-run  # Preview
supabase db push --linked            # Apply
```

### Creating an Event Contract

```bash
# Define AsyncAPI contract first
cd infrastructure/supabase/contracts
cat > organization-events.yaml <<'EOF'
asyncapi: '2.6.0'
info:
  title: Organization Domain Events
  version: 1.0.0

channels:
  organization.created:
    publish:
      message:
        $ref: '#/components/messages/OrganizationCreated'

components:
  messages:
    OrganizationCreated:
      payload:
        type: object
        required: [aggregate_id, organization_name, created_at]
        properties:
          aggregate_id:
            type: string
            format: uuid
          organization_name:
            type: string
          created_at:
            type: string
            format: date-time
EOF

# Register contract - see resources/asyncapi-contracts.md
```

### Deploying Temporal Workers

```bash
# Update worker deployment
cd infrastructure/k8s/temporal
kubectl apply -f worker-deployment.yaml

# Verify deployment
kubectl rollout status deployment/temporal-worker -n temporal
kubectl get pods -n temporal -l app=workflow-worker
```

## Common Imports and Patterns

```sql
-- Idempotent SQL patterns
CREATE TABLE IF NOT EXISTS ...;
CREATE INDEX IF NOT EXISTS ...;
DROP POLICY IF EXISTS ...; CREATE POLICY ...;
ALTER TABLE ... ENABLE ROW LEVEL SECURITY;

-- RLS with JWT claims
(current_setting('request.jwt.claims', true)::json->>'org_id')::uuid
(current_setting('request.jwt.claims', true)::json->>'user_role')::text

-- CQRS projection triggers
CREATE OR REPLACE FUNCTION update_projection_on_event()
RETURNS TRIGGER AS $$
BEGIN
  -- Update projection based on event
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER organization_projection_trigger
  AFTER INSERT ON domain_events
  FOR EACH ROW
  WHEN (NEW.event_type = 'OrganizationCreated')
  EXECUTE FUNCTION update_projection_on_event();
```

```yaml
# Kubernetes deployment pattern
apiVersion: apps/v1
kind: Deployment
metadata:
  name: temporal-worker
  namespace: temporal
spec:
  replicas: 2
  selector:
    matchLabels:
      app: workflow-worker
  template:
    spec:
      containers:
      - name: worker
        image: ghcr.io/analytics4change/a4c-workflows:latest
        env:
        - name: TEMPORAL_ADDRESS
          value: "temporal-frontend.temporal.svc.cluster.local:7233"
```

## Topics

### 1. Supabase Migrations ([resources/supabase-migrations.md](resources/supabase-migrations.md))
Idempotent SQL patterns using IF NOT EXISTS/IF EXISTS, RLS policy implementation with JWT custom claims, foreign key relationships, event trigger setup, migration file naming, and local testing workflows.

### 2. Kubernetes Deployments ([resources/k8s-deployments.md](resources/k8s-deployments.md))
Temporal worker deployment patterns, namespace organization, ConfigMap and Secret management, resource limits and requests, service discovery, and health checks.

### 3. CQRS Projections ([resources/cqrs-projections.md](resources/cqrs-projections.md))
Projection table design patterns, PostgreSQL trigger implementation for event processing, handling event ordering and idempotency, projection rebuilding strategies, and query optimization.

### 4. AsyncAPI Contracts ([resources/asyncapi-contracts.md](resources/asyncapi-contracts.md))
Contract-first event schema design, event naming conventions, schema versioning strategies, contract registration workflow, and integration with Temporal activities.

## Navigation

| Resource | Topics Covered | Lines |
|----------|---------------|-------|
| [supabase-migrations.md](resources/supabase-migrations.md) | Idempotency, RLS, triggers, testing | ~490 |
| [k8s-deployments.md](resources/k8s-deployments.md) | Workers, namespaces, configs, resources | ~470 |
| [cqrs-projections.md](resources/cqrs-projections.md) | Projections, triggers, ordering, rebuilding | ~485 |
| [asyncapi-contracts.md](resources/asyncapi-contracts.md) | Contract-first, schemas, versioning | ~475 |

## Core Principles

### 1. Safety First: Idempotency Everywhere

All infrastructure changes must be idempotent and reversible.

```sql
-- ✅ GOOD: Idempotent patterns
CREATE TABLE IF NOT EXISTS users (...);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
DROP POLICY IF EXISTS users_rls ON users;
CREATE POLICY users_rls ON users USING (...);

-- ❌ BAD: Non-idempotent (fails on second run)
CREATE TABLE users (...);
CREATE INDEX idx_users_email ON users(email);
```

**Why**: Migrations run multiple times during testing, rollbacks, and production deployments. Non-idempotent migrations break the deployment pipeline.

### 2. Contract-First Development

Define event contracts before implementing producers or consumers.

```yaml
# ✅ GOOD: Contract defined first
# 1. Create AsyncAPI schema in infrastructure/supabase/contracts/
# 2. Review schema with team
# 3. Register contract (see asyncapi-contracts.md)
# 4. Implement activity to emit event
# 5. Implement projection trigger to consume event
```

**Why**: Contracts establish the interface between services. Defining them first prevents breaking changes and ensures all parties agree on event structure.

### 3. Multi-Tenant Isolation via RLS

Every table with organization data must have RLS policies using JWT claims.

```sql
-- ✅ GOOD: RLS policy using JWT claim
CREATE POLICY tenant_isolation ON medications
  FOR ALL
  USING (org_id = (current_setting('request.jwt.claims', true)::json->>'org_id')::uuid);

ALTER TABLE medications ENABLE ROW LEVEL SECURITY;
```

**Why**: RLS enforces data isolation at the database layer, preventing cross-tenant data leaks even if application logic has bugs.

### 4. Event-Driven CQRS Architecture

Write models (domain_events) are separate from read models (projections).

```
Write: Temporal Activity → domain_events table (append-only)
Read:  PostgreSQL Trigger → projection tables (derived state)
```

**Why**: Separating writes from reads allows independent scaling, provides event audit trail, and enables time-travel debugging.

### 5. Event Metadata as Audit Trail

The `domain_events` table is the SOLE audit trail - there is no separate audit table.

All events MUST include audit context in metadata:

| Field | When Required | Description |
|-------|---------------|-------------|
| `user_id` | Always | UUID of user who initiated the action |
| `reason` | When meaningful | Human-readable justification |
| `ip_address` | Edge Functions | Client IP from request headers |
| `user_agent` | Edge Functions | Client info from request headers |
| `request_id` | When available | Correlation with API logs |

```sql
-- ✅ GOOD: Query audit trail directly from domain_events
SELECT event_type, event_metadata->>'user_id' as actor,
       event_metadata->>'reason' as reason, created_at
FROM domain_events WHERE stream_id = '<resource_id>'
ORDER BY created_at DESC;

-- ❌ BAD: Creating a separate audit table
-- Duplicates data, requires synchronization, adds complexity
```

**Why**: The event store already captures every state change with full context. A separate audit table is redundant and creates maintenance burden.

### 6. Supabase CLI Migrations

All infrastructure changes go through Supabase CLI migrations. **ALWAYS use the CLI to create migration files.**

```bash
# ✅ GOOD: Use CLI to create migration (generates correct timestamp)
cd infrastructure/supabase
supabase migration new add_medications_table
# Creates: supabase/migrations/YYYYMMDDHHMMSS_add_medications_table.sql
# Edit the generated file with idempotent SQL
# Commit to git, deploy via CI/CD (supabase db push)

# ❌ BAD: Manually create migration file with hand-typed timestamp
touch supabase/migrations/20251223120000_feature.sql
# Timestamp may be out-of-order with already-deployed migrations!
# CI/CD will FAIL with: "Found local migration files to be inserted before the last migration"

# ❌ BAD: Manual changes in Supabase dashboard
# Creates drift between code and reality
```

**Why**:
1. CLI generates correct UTC timestamp based on current time
2. Migrations must be in chronological order - manual timestamps easily break this
3. Version control and code review require file-based migrations

### 7. Dry-Run Before Deployment

Preview all migrations before applying to production.

```bash
# ✅ GOOD: Supabase CLI dry-run workflow
cd infrastructure/supabase
supabase link --project-ref "your-project-ref"
supabase db push --linked --dry-run   # Preview changes
supabase db push --linked             # Apply if preview looks correct
```

**Why**: Catch migration errors early, validate changes, and ensure migrations are correct before affecting shared environments.

### 8. Projection Triggers Are Idempotent

CQRS projection triggers must handle duplicate events gracefully.

```sql
-- ✅ GOOD: Upsert pattern for idempotency
INSERT INTO organization_projection (org_id, name, ...)
VALUES (new_org_id, new_name, ...)
ON CONFLICT (org_id)
DO UPDATE SET
  name = EXCLUDED.name,
  updated_at = now();
```

**Why**: Events may be replayed or delivered multiple times. Idempotent triggers prevent data corruption.

### 9. Kubernetes Declarative Configuration

All K8s resources defined as YAML, managed via git and kubectl apply.

```bash
# ✅ GOOD: Declarative YAML files
kubectl apply -f infrastructure/k8s/temporal/worker-deployment.yaml

# ❌ BAD: Imperative commands
kubectl run temporal-worker --image=...
# No version control, hard to reproduce
```

**Why**: YAML files in git provide version control, code review, and reproducible deployments.

## Complete Migration Template

```sql
-- File: infrastructure/supabase/sql/02-tables/medications/table.sql
CREATE TABLE IF NOT EXISTS medications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID NOT NULL REFERENCES organizations(id),
  rxcui VARCHAR(20) NOT NULL,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(org_id, rxcui)
);

-- Indexes (idempotent)
CREATE INDEX IF NOT EXISTS idx_medications_org_id ON medications(org_id);

-- RLS policy (requires drop first for idempotency)
DROP POLICY IF EXISTS medications_tenant_isolation ON medications;
CREATE POLICY medications_tenant_isolation ON medications
  FOR ALL USING (org_id = (current_setting('request.jwt.claims', true)::json->>'org_id')::uuid);

ALTER TABLE medications ENABLE ROW LEVEL SECURITY;

-- See resources/supabase-migrations.md for complete patterns
```

## Complete CQRS Projection Template

```sql
-- File: infrastructure/supabase/sql/04-projections/organization_projection.sql
CREATE TABLE IF NOT EXISTS organization_projection (
  org_id UUID PRIMARY KEY,
  organization_name VARCHAR(255) NOT NULL,
  status VARCHAR(50) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  last_event_id UUID
);

CREATE OR REPLACE FUNCTION update_organization_projection()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.event_type = 'OrganizationCreated' THEN
    INSERT INTO organization_projection (org_id, organization_name, status, created_at, last_event_id)
    VALUES (NEW.aggregate_id, NEW.event_data->>'organization_name', 'provisioning', NEW.created_at, NEW.id)
    ON CONFLICT (org_id) DO NOTHING; -- Idempotent
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS organization_projection_trigger ON domain_events;
CREATE TRIGGER organization_projection_trigger
  AFTER INSERT ON domain_events FOR EACH ROW
  WHEN (NEW.aggregate_type = 'organization')
  EXECUTE FUNCTION update_organization_projection();

-- See resources/cqrs-projections.md for complete patterns
```

## Anti-Pattern: Manual Console Changes

**❌ PROBLEM**: Making changes directly in Supabase dashboard or kubectl without version control

```bash
# ❌ BAD: Manual changes
# Developer opens Supabase dashboard
# Creates table manually via SQL editor
# No code review, no version control, no teammate awareness
```

**✅ SOLUTION**: Always use Supabase CLI migrations

```bash
# ✅ GOOD: Supabase CLI migration workflow
# 1. Create migration: supabase migration new feature_name
# 2. Write idempotent SQL in the generated file
# 3. Preview: supabase db push --linked --dry-run
# 4. Commit to git
# 5. Code review
# 6. Deploy via CI/CD (GitHub Actions runs supabase db push)
```

## Quick Reference

### File Organization

```
infrastructure/
├── supabase/
│   ├── supabase/               # Supabase CLI project directory
│   │   ├── migrations/         # SQL migrations (Supabase CLI managed)
│   │   │   └── 20240101000000_baseline.sql  # Day 0 baseline
│   │   ├── functions/          # Edge Functions (Deno)
│   │   └── config.toml         # Supabase CLI configuration
│   ├── sql.archived/           # Archived granular SQL files (reference only)
│   ├── contracts/              # AsyncAPI event schemas
│   └── scripts/                # OAuth setup, verification scripts
└── k8s/
    └── temporal/               # Temporal worker deployments
        ├── worker-deployment.yaml
        ├── configmap-dev.yaml
        └── secrets.yaml
```

### Testing Commands

```bash
# Supabase CLI migration workflow
cd infrastructure/supabase
export SUPABASE_ACCESS_TOKEN="your-token"
supabase link --project-ref "your-project-ref"
supabase migration list --linked      # Check migration status
supabase db push --linked --dry-run   # Preview pending migrations
supabase db push --linked             # Apply migrations

# Kubernetes validation
kubectl config use-context k3s-a4c
kubectl get pods -n temporal
kubectl logs -n temporal deployment/temporal-worker
```

### Common Migration Patterns

```sql
-- Idempotent table creation
CREATE TABLE IF NOT EXISTS table_name (...);

-- Idempotent index creation
CREATE INDEX IF NOT EXISTS idx_name ON table_name(column);

-- Idempotent policy creation (requires drop first)
DROP POLICY IF EXISTS policy_name ON table_name;
CREATE POLICY policy_name ON table_name USING (...);

-- Safe column addition
ALTER TABLE table_name ADD COLUMN IF NOT EXISTS column_name TYPE;

-- Safe column removal (be careful!)
ALTER TABLE table_name DROP COLUMN IF EXISTS column_name;

-- Idempotent trigger creation
CREATE OR REPLACE FUNCTION function_name() RETURNS TRIGGER AS $$ ... $$;
DROP TRIGGER IF EXISTS trigger_name ON table_name;
CREATE TRIGGER trigger_name ... EXECUTE FUNCTION function_name();
```

## Related Documentation

- [infrastructure/CLAUDE.md](../../infrastructure/CLAUDE.md) - Component-specific infrastructure guidance
- [infrastructure/supabase/contracts/README.md](../../infrastructure/supabase/contracts/README.md) - AsyncAPI contract registration
- [temporal-workflow-guidelines](../temporal-workflow-guidelines/SKILL.md) - Event emission from activities
- Root [CLAUDE.md](../../../CLAUDE.md) - Monorepo overview

## When to Use This Skill

This skill auto-activates when:
- Working with files in `infrastructure/supabase/` or `infrastructure/k8s/`
- User prompt contains keywords: supabase, migration, sql, kubernetes, rls, cqrs, projection, asyncapi
- Creating or modifying: database migrations, RLS policies, K8s manifests, event contracts
- Implementing event-driven projections or triggers

Load relevant resource files as needed:
- Creating migrations → [supabase-migrations.md](resources/supabase-migrations.md)
- Updating projections → [cqrs-projections.md](resources/cqrs-projections.md)
- Defining events → [asyncapi-contracts.md](resources/asyncapi-contracts.md)
- Deploying workers → [k8s-deployments.md](resources/k8s-deployments.md)
