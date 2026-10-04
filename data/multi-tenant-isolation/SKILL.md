---
name: multi-tenant-isolation
description: Use this skill whenever writing database queries, API handlers, analytics pipelines, export functions, background jobs, or any data access code in the Myelin platform. This defines the row-level isolation contract, cross-tenant prohibition rules, feature-flag gating model, and the package entitlement tiers. A tenantId filter is not optional — it is structurally required on every query. Load this skill before writing any data access or API code.
---

This skill is the single source of truth for multi-tenancy in the Myelin platform. Every query, every API call, every analytics aggregation, and every background job must operate within tenant scope. A missing tenant filter is a data leak — not a performance optimisation.

---

## Core Isolation Principle

Every business record in the platform belongs to exactly one tenant. No code path may return data from more than one tenant in a single response unless the caller holds a Ministry Viewer, Regulator Auditor, or Super Admin role AND the query is explicitly constructed as a cross-tenant aggregation.

Cross-tenant aggregations must:
- Use only tenant-scoped aggregates (counts, rates, medians) — never raw records
- Never expose individual learner identifiers across tenant boundaries
- Be explicitly labelled in code with a comment: `// CROSS_TENANT_AGGREGATE — requires elevated role`

Any other cross-tenant data access is a critical security violation.

---

## Database Layer — Row-Level Security

Tenant isolation is enforced at the database layer using Row-Level Security (RLS). Application-level filtering is a secondary defence, not the primary one.

RLS policy pattern (PostgreSQL):

```sql
-- Enable RLS on every business entity table
ALTER TABLE sim_step_events ENABLE ROW LEVEL SECURITY;

-- Policy: users may only read rows matching their tenant
CREATE POLICY tenant_isolation ON sim_step_events
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
```

The application must set `app.current_tenant_id` from the authenticated session on every database connection before executing any query. Never rely on application-level WHERE clauses alone.

RLS must be enabled and tested on every table in this list:
- `tenants`, `users`, `role_assignments`
- `programmes`, `modules`, `learning_items`, `enrollments`
- `simulation_attempts`, `sim_step_events`
- `submissions`, `rubrics`, `peer_reviews`
- `placements`, `logbook_entries`, `mentor_signoffs`
- `result_statements`
- `notifications`
- `audit_logs`
- `consent_records`
- `agent_transcripts`, `escalation_queue`

The `demo_events` table uses a separate RLS policy that permits only demo-namespace reads and never joins with live tables.

---

## Application Layer — Tenant Context Propagation

Every API handler must extract `tenantId` from the authenticated session token and propagate it to all downstream service and database calls. It must never accept `tenantId` from the request body or query parameters.

```javascript
function getTenantContext(session) {
  if (!session || !session.tenantId) {
    throw new AuthError('NO_TENANT_CONTEXT');
  }
  return session.tenantId;
}

async function getSimStepEvents(session, scenarioId) {
  const tenantId = getTenantContext(session);
  // Set RLS context
  await db.query(`SET LOCAL app.current_tenant_id = '${tenantId}'`);
  // Query — RLS enforces isolation, but always include the filter explicitly too
  return db.query(
    `SELECT * FROM sim_step_events WHERE tenant_id = $1 AND scenario_id = $2`,
    [tenantId, scenarioId]
  );
}
```

Always include the explicit `tenant_id` WHERE clause in addition to RLS. RLS is the enforcement layer; the explicit filter is the intent declaration.

---

## Tenant Record Schema

```json
{
  "tenantId": "uuid — primary identifier",
  "tenantName": "string — institution display name",
  "tenantSlug": "string — URL-safe identifier for routing",
  "packageTier": "PILOT | OPERATIONAL | NATIONAL_PROGRAM",
  "featureFlags": {
    "scenarioLOTO": true,
    "scenarioPV": false,
    "scenarioMobileRepair": false,
    "scenarioPCBRework": false,
    "aiAgentTextMode": true,
    "aiAgentGuidedMedia": false,
    "aiAgentLiveConversational": false,
    "handTrackingMode": false,
    "crossInstitutionDashboard": false
  },
  "compliancePolicyPack": "string — e.g. ZA_POPIA_v1",
  "compliancePolicyVersion": "string — semver",
  "dataResidencyRegion": "string — e.g. af-south-1",
  "ssoConfig": {
    "method": "NONE | OIDC | SAML",
    "issuer": "string | null",
    "clientId": "string | null"
  },
  "retentionPolicyYears": 10,
  "status": "ACTIVE | SUSPENDED | OFFBOARDED",
  "createdAt": "ISO 8601",
  "updatedAt": "ISO 8601"
}
```

---

## Feature Flag Gating Model

Feature flags are stored on the tenant record and are authoritative. Client-side feature detection must always be validated against the server-side tenant config.

### Package entitlement map

| Feature | Pilot | Operational | National Program |
|---------|-------|-------------|-----------------|
| Core curriculum baseline units | Always on | Always on | Always on |
| LOTO simulation | Always on | Always on | Always on |
| AI agent — text mode | Always on | Always on | Always on |
| AI agent — guided media | Configurable | On | On |
| AI agent — live conversational | Off | Configurable | Configurable |
| Solar PV scenario | Feature-flagged | Feature-flagged | Feature-flagged |
| Mobile Repair scenario | Feature-flagged | Feature-flagged | Feature-flagged |
| PCB Rework scenario | Feature-flagged | Feature-flagged | Feature-flagged |
| Multi-site admin controls | Off | On | On |
| Cross-institution dashboard | Off | Off | On |
| Regulator evidence packs | Off | Off | On |
| Hand tracking mode | Off | Configurable | Configurable |

"Feature-flagged" means the feature is available for the tier but must be explicitly enabled by Super Admin with acceptance criteria documented. It is not on by default.

### Feature gate implementation pattern

```javascript
function requireFeature(tenant, featureKey) {
  if (!tenant.featureFlags[featureKey]) {
    throw new FeatureGateError(`FEATURE_NOT_ENABLED: ${featureKey}`);
  }
  return true;
}
```

Call `requireFeature` before entering any feature-flagged code path. The check must happen server-side — never rely on the client to hide gated UI without a server-side gate on the API.

### Scenario activation prerequisite

No scenario may be activated for a tenant unless:
1. The scenario's feature flag is explicitly set to `true` in the tenant record
2. A `SCENARIO_OUTCOME_MAP` record exists linking the scenario version and scoring rules version to at least one of the tenant's approved curriculum outcome IDs
3. The activation has been logged as a Super Admin audit event

If any condition fails, the scenario endpoint must return a `403 FEATURE_NOT_ENABLED` error.

---

## Cross-Tenant Roles — Data Access Rules

### Ministry / Department Viewer

```javascript
async function getMinistryDashboard(session) {
  requireRole(session, ['MINISTRY_VIEWER', 'SUPER_ADMIN']);
  const scopedTenantIds = getMinistryScope(session); // explicit list from role assignment
  // CROSS_TENANT_AGGREGATE — requires elevated role
  return db.query(`
    SELECT
      tenant_id,
      COUNT(*) AS total_learners,
      AVG(completion_rate) AS avg_completion
    FROM cohort_summaries
    WHERE tenant_id = ANY($1)
    GROUP BY tenant_id
  `, [scopedTenantIds]);
}
```

Raw learner records must never appear in cross-tenant queries. Aggregates only.

### Super Admin

Super Admin queries may access any tenant but must always include explicit tenant scoping in the query intent. Super Admin access is not a reason to remove tenant filters — it is a reason to allow dynamic tenant filter values.

---

## Background Jobs and Async Workers

Every background job that processes tenant data must carry the `tenantId` in the job payload and set the RLS context at job start. A job that processes data without setting the tenant context is a critical defect.

```javascript
async function processSimTelemetryJob(job) {
  const { tenantId, sessionId, events } = job.data;
  if (!tenantId) throw new Error('JOB_MISSING_TENANT_CONTEXT');
  await db.query(`SET LOCAL app.current_tenant_id = '${tenantId}'`);
  // proceed with job
}
```

Job queues must not allow a job from one tenant to read or write records belonging to another tenant. Job isolation is enforced by the same RLS mechanism as synchronous queries.

---

## Demo Namespace Isolation

The `demo` tenant is a reserved tenant identifier. It is never a real institution and never receives live learner data.

- Demo events are written to `demo_events` (separate table from `sim_step_events`)
- Demo transcripts are written to `demo_agent_transcripts` (separate from `agent_transcripts`)
- The `demo` tenantId must never appear in any query against live business tables
- Any attempt to join `demo_events` with live tables is a critical defect

See `demo-mode-isolation` skill for the full demo data contract.

---

## Tenant Offboarding

When a tenant's status is set to `OFFBOARDED`:
- All active sessions for that tenant must be invalidated within 15 minutes
- Feature flags must be set to all-false
- Data must be retained for the configured retention period before any deletion
- Deletion, when it occurs, must be logged as a Super Admin audit event with a deletion manifest

Data is never hard-deleted outside of a formal offboarding process.

---

## Automated Isolation Test Requirements

The following isolation scenarios must have automated test coverage before any production release:

1. A Student in Tenant A cannot access any record belonging to Tenant B
2. A Lecturer in Tenant A cannot access cohort or learner data from Tenant B
3. A Ministry Viewer query returns only aggregated data for their scoped tenant set and never raw learner records
4. A demo-mode event never appears in a live tenant query result
5. A feature-flagged scenario returns `403` for a tenant where the flag is false
6. A background job without `tenantId` in its payload throws an error before touching any data

---

## What Not To Do

- Do not accept `tenantId` from a request body or URL parameter — always derive it from the authenticated session
- Do not write a query without an explicit `tenant_id` filter even when RLS is active
- Do not allow a background job to run without setting the RLS tenant context
- Do not enable a scenario for a tenant without a logged Super Admin audit event
- Do not expose raw learner records in any cross-tenant view
- Do not allow the `demo` tenantId to appear in any live business table query
- Do not skip RLS for performance reasons — use query optimisation instead
