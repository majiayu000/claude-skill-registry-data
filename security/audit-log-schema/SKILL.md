---
name: audit-log-schema
description: Use this skill whenever writing code that creates, queries, or exports audit log entries — including privileged actions, policy changes, data exports, role assignments, result issuance, security events, and compliance reporting. This defines the immutable audit entry schema, the complete trigger list, the query API, and the export contract for regulators and admins. Load this skill before writing any audit logging code.
---

This skill defines the audit logging system for the Myelin platform. Audit logs are immutable, tenant-scoped, and retention-class A (10-year minimum). Every privileged action on the platform must produce an audit entry. No exceptions based on convenience or performance.

---

## Core Principle: Immutable and Complete

Audit logs are never updated or deleted during their retention period. Every write is an insert. The audit log is the ground truth for compliance reporting, security investigations, and data subject rights responses.

---

## AuditLog Entry Schema

```json
{
  "logId":          "uuid v4 — unique per entry",
  "tenantId":       "uuid | null — null only for Super Admin platform-level actions",
  "actorId":        "uuid — the user who performed the action",
  "actorRole":      "string — role at time of action (STUDENT | LECTURER | ADMIN | etc.)",
  "actorIp":        "string — IP address of the request",
  "actorUserAgent": "string — User-Agent header",
  "sessionId":      "uuid | null — session at time of action if applicable",

  "action":         "string — action code from the trigger list below",
  "actionCategory": "string — AUTH | DATA | POLICY | ASSESSMENT | SECURITY | COMPLIANCE | AI",

  "resourceType":   "string — entity type acted upon e.g. User, ResultStatement, FeatureFlag",
  "resourceId":     "uuid | null — PK of the affected record",
  "resourceTenantId": "uuid | null — tenant that owns the resource (may differ from actorId tenant for Super Admin actions)",

  "before":         "JSONB | null — state before change; null for create actions",
  "after":          "JSONB | null — state after change; null for delete/read actions",

  "outcome":        "SUCCESS | FAILURE | BLOCKED",
  "failureReason":  "string | null — if outcome is FAILURE or BLOCKED",

  "timestamp":      "ISO 8601 UTC — server time, not client time",

  "metadata":       "JSONB | null — action-specific supplementary fields"
}
```

### Field rules

- `actorId` must always be set — anonymous actions are prohibited on all protected routes
- `before` and `after` must use snapshot values at the moment of the action — not references to live records that could change
- Sensitive values in `before`/`after` snapshots must be redacted: password hashes → `[REDACTED]`, JWT tokens → `[REDACTED]`
- `metadata` is used for action-specific data that does not fit the standard fields (e.g. file name on upload, export scope on data export)

---

## Audit Write Function

```javascript
async function writeAuditEntry(action, context, options = {}) {
  const { tenantId, actorId, actorRole, req, resourceType, resourceId,
          before, after, outcome = 'SUCCESS', failureReason, metadata } = options;

  await db.query(`
    INSERT INTO audit_logs (
      log_id, tenant_id, actor_id, actor_role, actor_ip, actor_user_agent,
      session_id, action, action_category, resource_type, resource_id,
      resource_tenant_id, before, after, outcome, failure_reason,
      timestamp, metadata
    ) VALUES (
      $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,NOW(),$17
    )
  `, [
    generateUUID(),
    tenantId || null,
    actorId,
    actorRole,
    req?.ip || 'system',
    req?.headers?.['user-agent'] || 'system',
    context?.sessionId || null,
    action,
    resolveCategory(action),
    resourceType || null,
    resourceId || null,
    options.resourceTenantId || tenantId || null,
    before ? JSON.stringify(redactSensitiveFields(before)) : null,
    after  ? JSON.stringify(redactSensitiveFields(after))  : null,
    outcome,
    failureReason || null,
    metadata ? JSON.stringify(metadata) : null
  ]);
}

function redactSensitiveFields(obj) {
  const redacted = { ...obj };
  const sensitiveKeys = ['passwordHash', 'password_hash', 'token', 'accessToken',
                         'refreshToken', 'jwtSigningKey', 'apiKey'];
  sensitiveKeys.forEach(k => { if (k in redacted) redacted[k] = '[REDACTED]'; });
  return redacted;
}
```

`writeAuditEntry` must be called within the same transaction as the action being audited where possible. If the action is asynchronous (background job, async workflow), the audit entry must be written before the action is considered complete.

---

## Complete Action Trigger List

### AUTH category

| Action code | Trigger |
|-------------|---------|
| `AUTH_LOGIN_SUCCESS` | Successful email/password login |
| `AUTH_LOGIN_FAILURE` | Failed login attempt |
| `AUTH_LOGOUT` | Explicit logout |
| `AUTH_SSO_PROCESSED` | SSO assertion received and validated |
| `AUTH_SSO_FAILURE` | SSO assertion rejected |
| `AUTH_TOKEN_REFRESHED` | Access token refreshed via refresh token |
| `AUTH_SESSION_REVOKED` | Session explicitly revoked by user or admin |
| `AUTH_ALL_SESSIONS_REVOKED` | All sessions revoked for a user |
| `AUTH_PASSWORD_CHANGED` | Password successfully changed |
| `AUTH_PASSWORD_RESET_INITIATED` | Password reset flow triggered |
| `AUTH_PASSWORD_RESET_COMPLETED` | Password reset completed |
| `AUTH_MFA_ENABLED` | MFA enabled for account (v2) |
| `AUTH_MFA_DISABLED` | MFA disabled for account (v2) |
| `CONSENT_CAPTURED` | Learner consent recorded |
| `CONSENT_REVOKED` | Learner consent revoked |

### DATA category

| Action code | Trigger |
|-------------|---------|
| `DATA_EXPORT_REQUESTED` | Any report or data export initiated |
| `DATA_EXPORT_COMPLETED` | Export file generated and delivered |
| `DATA_SUBJECT_ACCESS_EXPORT` | POPIA data subject access request fulfilled |
| `DATA_SUBJECT_ANONYMISED` | Learner record anonymised after retention period |
| `DATA_SUBJECT_CORRECTION` | Personal information corrected on request |
| `CROSS_BORDER_EXPORT` | Data exported to a non-SA jurisdiction |

### POLICY category

| Action code | Trigger |
|-------------|---------|
| `ROLE_ASSIGNMENT_CREATED` | New role assignment created |
| `ROLE_ASSIGNMENT_REVOKED` | Role assignment revoked |
| `FEATURE_FLAG_ENABLED` | Feature flag enabled for a tenant |
| `FEATURE_FLAG_DISABLED` | Feature flag disabled for a tenant |
| `POLICY_CONFIG_CHANGED` | Institution policy configuration changed |
| `SSO_CONFIG_CHANGED` | SSO configuration added or modified |
| `SCENARIO_ACTIVATED` | Simulation scenario activated for a tenant |
| `NOTIFICATION_TEMPLATE_CHANGED` | Notification template modified |
| `PROGRAMME_PUBLISHED` | Programme published or version incremented |
| `MODULE_PUBLISHED` | Module published or version incremented |

### ASSESSMENT category

| Action code | Trigger |
|-------------|---------|
| `SUBMISSION_REVIEWED` | Lecturer grades or returns a submission |
| `SUBMISSION_OUTCOME_CHANGED` | Assessment outcome changed post-review |
| `PEER_REVIEW_MODERATED` | Peer review moderated by lecturer |
| `MENTOR_SIGNOFF_RECORDED` | Mentor approves or rejects logbook entry |
| `RESULT_STATEMENT_ISSUED` | Statement of results generated and issued |
| `RESULT_STATEMENT_AMENDED` | Result statement amended post-issuance |
| `RESULT_STATEMENT_REVOKED` | Result statement revoked |
| `SIMULATION_ATTEMPT_ACCESSED` | Lecturer or admin accesses a simulation attempt record |

### SECURITY category

| Action code | Trigger |
|-------------|---------|
| `SECURITY_MALWARE_DETECTED` | Malware scan flagged an uploaded file |
| `SECURITY_RATE_LIMIT_EXCEEDED` | Rate limit triggered for a user or IP |
| `SECURITY_TENANT_SCOPE_VIOLATION` | Attempt to access cross-tenant data |
| `SECURITY_INVALID_TOKEN` | Invalid or expired token presented |
| `SECURITY_SUSPICIOUS_PATTERN` | Automated pattern detection flag |
| `TENANT_OFFBOARDED` | Tenant status set to OFFBOARDED |
| `TENANT_SUSPENDED` | Tenant status set to SUSPENDED |

### COMPLIANCE category

| Action code | Trigger |
|-------------|---------|
| `RETENTION_JOB_COMPLETE` | Nightly retention automation job completed |
| `EVIDENCE_EXPORT_GENERATED` | Simulation evidence export pack generated |
| `CURRICULUM_OUTCOME_MAP_CREATED` | Scenario-to-curriculum mapping created for tenant |
| `COMPLIANCE_POLICY_PACK_CHANGED` | Tenant compliance policy pack updated |

### AI category

| Action code | Trigger |
|-------------|---------|
| `AI_ESCALATION_CREATED` | Distress or policy escalation queue entry created |
| `AI_ESCALATION_RESOLVED` | Escalation marked resolved by admin |
| `AI_ESCALATION_DISMISSED` | Escalation dismissed by admin |
| `AI_POLICY_VIOLATION_FLAGGED` | Agent response flagged for policy review |
| `AI_RESPONSE_HELD` | Agent response held pending moderation |

---

## Query API

### Admin — query audit log for their tenant

```javascript
async function queryAuditLog(adminSession, filters = {}) {
  requireRole(adminSession, ['ADMIN', 'SUPER_ADMIN']);
  const tenantId = adminSession.role === 'SUPER_ADMIN'
    ? (filters.tenantId || null)   // Super Admin may query any tenant
    : adminSession.tenantId;       // Admin scoped to their own tenant

  await db.query(`SET LOCAL app.current_tenant_id = '${adminSession.tenantId}'`);

  return db.query(`
    SELECT log_id, actor_id, actor_role, action, action_category,
           resource_type, resource_id, outcome, timestamp, metadata
    FROM audit_logs
    WHERE ($1::uuid IS NULL OR tenant_id = $1)
      AND ($2::text IS NULL OR action_category = $2)
      AND ($3::uuid IS NULL OR actor_id = $3)
      AND ($4::timestamptz IS NULL OR timestamp >= $4)
      AND ($5::timestamptz IS NULL OR timestamp <= $5)
    ORDER BY timestamp DESC
    LIMIT 500
  `, [
    tenantId,
    filters.category   || null,
    filters.actorId    || null,
    filters.dateFrom   || null,
    filters.dateTo     || null
  ]);
}
```

`before` and `after` snapshots are excluded from the default query response — they are returned only in explicit detail requests to avoid over-exposing state history in list views.

### Regulator audit export

```javascript
async function generateRegulatorAuditExport(adminSession, scope) {
  requireRole(adminSession, ['ADMIN', 'SUPER_ADMIN']);

  const entries = await db.query(`
    SELECT *
    FROM audit_logs
    WHERE tenant_id = $1
      AND action_category IN ('ASSESSMENT', 'COMPLIANCE', 'POLICY')
      AND timestamp BETWEEN $2 AND $3
    ORDER BY timestamp ASC
  `, [adminSession.tenantId, scope.dateFrom, scope.dateTo]);

  const exportPack = {
    exportId:        generateUUID(),
    exportTimestamp: new Date().toISOString(),
    tenantId:        adminSession.tenantId,
    generatedBy:     adminSession.actorId,
    scope,
    entries:         entries.rows,
    checksum:        sha256(JSON.stringify(entries.rows))
  };

  await writeAuditEntry('DATA_EXPORT_COMPLETED', {
    tenantId:     adminSession.tenantId,
    actorId:      adminSession.userId,
    actorRole:    adminSession.role,
    resourceType: 'AuditLog',
    metadata:     { exportId: exportPack.exportId, entryCount: entries.rows.length }
  });

  return exportPack;
}
```

The `checksum` (SHA-256 of serialised entries) enables the regulator to verify the export has not been tampered with after generation.

---

## Super Admin Visibility

Super Admin actions are logged with `tenantId: null` when acting at the platform level. They are visible to Super Admin in a cross-tenant audit view. They are never visible in tenant-scoped Admin audit log views.

```javascript
function isSuperAdminAction(action) {
  return [
    'TENANT_OFFBOARDED', 'TENANT_SUSPENDED', 'FEATURE_FLAG_ENABLED',
    'FEATURE_FLAG_DISABLED', 'ROLE_ASSIGNMENT_CREATED', 'SCENARIO_ACTIVATED'
  ].includes(action) && actorRole === 'SUPER_ADMIN';
}
```

---

## Performance

The audit log table will be high-volume. Index strategy:

```sql
CREATE INDEX idx_audit_tenant_timestamp ON audit_logs (tenant_id, timestamp DESC);
CREATE INDEX idx_audit_actor            ON audit_logs (actor_id, timestamp DESC);
CREATE INDEX idx_audit_resource         ON audit_logs (resource_type, resource_id);
CREATE INDEX idx_audit_action_category  ON audit_logs (action_category, tenant_id, timestamp DESC);
```

Do not add full-text indexes on `before`, `after`, or `metadata` — these are large JSONB columns and full-text indexing will dominate storage. Query them with `->` and `->>` operators only.

For high-traffic audit writes, use a write buffer: batch audit entries into a queue and flush to the database every 500ms or 100 entries, whichever comes first. Security and compliance category entries bypass the buffer and write synchronously.

---

## What Not To Do

- Do not update or delete any audit log entry
- Do not store password hashes or tokens in `before`/`after` snapshots — redact them
- Do not allow Admin to query audit logs for a different tenant
- Do not omit `actorId` from any audit entry — even system jobs must use a named service account
- Do not use client-supplied timestamps for `timestamp` — always use server time
- Do not add full-text indexes on JSONB audit fields
- Do not bypass the buffer for non-security writes only — security and compliance writes are always synchronous
