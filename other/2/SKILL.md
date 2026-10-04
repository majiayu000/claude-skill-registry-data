---
name: auth-and-rbac
description: Use this skill whenever writing any authentication flow, session management, role check, permission gate, SSO integration, invite workflow, or access control logic in the Myelin platform. This is the authoritative role map, permission boundary, and identity contract. Do not invent role names, permission levels, or access rules. Load this skill before writing any auth, identity, or role-gated code.
---

This skill defines the complete identity and access control contract for the Myelin platform. Every session, every role check, every permission gate, and every SSO integration must conform to these definitions. Do not approximate or invent role behaviour — this file is the source of truth.

---

## Authentication Methods

### Email and password (all tenants, required)

- Passwords must be hashed with a strong adaptive algorithm (bcrypt, scrypt, or Argon2id). Do not use SHA or MD5.
- Enforce minimum password complexity at the API layer, not only in the UI.
- Login returns a short-lived access token and a long-lived refresh token.
- Access token TTL: 15 minutes. Refresh token TTL: 7 days (rolling).
- Refresh tokens are stored server-side and are revocable per session and per user.

### SSO — OIDC and SAML 2.0 (per institution)

- SSO is configured per tenant by Super Admin. It is not a global toggle.
- OIDC: use authorization code flow with PKCE. Do not use implicit flow.
- SAML 2.0: validate assertion signature, audience restriction, and NotOnOrAfter condition on every assertion.
- On first SSO login, create a platform user record linked to the tenant and SSO subject identifier.
- SSO users follow the same RBAC rules as email/password users — SSO does not grant elevated permissions.
- If an institution disables SSO, existing SSO-linked accounts must fall back to email/password reset flow.

### Session management

- Sessions are tenant-scoped. A user with access to multiple tenants holds a separate session per tenant.
- All active sessions are enumerable by the user in Profile > Security.
- Admins may revoke any session for users within their tenant.
- Super Admin may revoke any session across all tenants.
- Session invalidation takes effect within one access token TTL (15 minutes maximum).

---

## Role Definitions

Eight platform roles. Do not add roles without updating this skill. Do not merge roles to simplify code.

### Student (Learner)

Scope: single tenant, own records only.

Permitted:
- View and progress through their enrolled pathway and modules
- Enter and interact with the simulator
- View their own simulation attempt history and step traces
- Submit evidence to their e-Portfolio
- Complete assigned peer reviews
- Create and manage their own workplace logbook entries
- Request mentor sign-off on their logbook entries
- View their own statement of results
- Interact with the AI learning coach within their active session
- Manage their own profile and preferences

Prohibited:
- View any other learner's records, submissions, or attempts
- Access lecturer, admin, or any elevated role views
- Modify assessment outcomes or scoring rules

### Lecturer

Scope: single tenant, cohorts assigned to them.

Permitted:
- View progress and simulation attempt history for learners in their assigned cohorts
- Review, score, and comment on e-Portfolio submissions
- Assign and moderate peer reviews
- Trigger remediation activities and notifications for their cohort
- Configure assessment windows for their assigned modules (within admin-defined policy)
- View intervention markers and cohort risk indicators
- Use AI Instructor Copilot (draft suggestions, feedback drafts — assistive only)

Prohibited:
- Modify learner identity records
- Manage institution-level policy or feature flags
- Access learners outside their assigned cohorts
- Finalize any AI-drafted recommendation without explicit confirmation

### Admin (Institutional Operations)

Scope: single tenant, all records within that tenant.

Permitted:
- Manage users, cohorts, programmes, and role assignments within their tenant
- Configure institution policy options (funding warning/block, progression rules, notification templates)
- Access audit logs and policy change history for their tenant
- Access institution-level reporting and export
- Configure SSO settings for their tenant
- Enable or disable feature-flagged scenarios within their permitted entitlement tier
- Manage mentor invite and onboarding

Prohibited:
- Access any other tenant's data
- Modify platform-level configuration or cross-tenant settings
- Override Super Admin–controlled entitlement caps

### Employer Mentor

Scope: single tenant, assigned learner placements only.

Permitted:
- View logbook entries for learners assigned to their placement
- Approve, reject, or comment on logbook entries with timestamped sign-off
- View learner placement record

Prohibited:
- Access module content, simulation attempts, e-Portfolio submissions, or peer review records
- View any learner not assigned to their placement
- Self-register — accounts are invite-only, institution-linked

### Ministry / Department Viewer

Scope: cross-institution, read-only, aggregated data only.

Permitted:
- View aggregated completion, competency, and intervention dashboards across their scoped institutions
- Export aggregated KPI reports

Prohibited:
- Access individual learner records
- View institution-identifiable simulation attempt data
- Modify any platform data
- Access non-aggregated analytics

Default: read-only. Elevated access requires explicit override approved and logged by Super Admin.

### Procurement / Commercial Reviewer

Scope: single or scoped institution set, read-only.

Permitted:
- View approved pilot scope and KPI scorecard outcomes
- View commercial package options and pilot-to-annual conversion report

Prohibited:
- Access learner records or cohort details
- View operational dashboards or admin configuration

Default: read-only. No write access under any circumstance.

### Regulator / Quality Assurance Auditor

Scope: scoped institution set, read-only.

Permitted:
- Access audit-ready evidence exports
- Access standards-alignment reports and curriculum outcome mapping coverage
- View signed result provenance reports

Prohibited:
- Access non-anonymized individual learner records unless explicitly approved and logged
- Modify any platform data

Default: read-only. Any elevated access requires Super Admin approval and audit entry.

### Super Admin (Platform Owner — Sethu and authorized operators)

Scope: all tenants, all data.

Permitted:
- All Admin permissions across all tenants
- Tenant creation, configuration, and deactivation
- Global feature flag management and entitlement cap configuration
- Platform release controls and migration tooling
- Cross-tenant incident investigation and session revocation
- Compliance policy enforcement and audit access

Note: Super Admin actions must always create audit log entries. There is no unlogged Super Admin action.

---

## Role Assignment Rules

- A user may hold one role per tenant. Multi-role is not supported in v1.
- Role assignments are made by Admin (within their tenant) or Super Admin (any tenant).
- Employer Mentor accounts are invite-only: Admin issues an invite link tied to a specific tenant and placement. Open self-signup is prohibited.
- Ministry, Procurement, and Regulator roles are assigned by Super Admin only.
- Role changes take effect at next session start (or immediately if session is explicitly refreshed).

---

## Permission Gate Implementation Pattern

Every API endpoint and every UI view that is role-gated must implement the gate as a server-side check. Client-side role checks are for UX only — they are not a security boundary.

```javascript
function requireRole(session, allowedRoles) {
  if (!session || !session.userId || !session.tenantId) {
    throw new AuthError('NO_SESSION');
  }
  if (!allowedRoles.includes(session.role)) {
    throw new AuthError('INSUFFICIENT_ROLE');
  }
  return true;
}
```

Tenant scope must be enforced separately from role:

```javascript
function requireTenantScope(session, resourceTenantId) {
  if (session.role === 'SUPER_ADMIN') return true;
  if (session.tenantId !== resourceTenantId) {
    throw new AuthError('TENANT_SCOPE_VIOLATION');
  }
  return true;
}
```

Always call both checks. A user with the correct role in the wrong tenant must be denied.

---

## POPIA Consent Gate

Before any learner training interaction begins, consent must be captured and confirmed:

```javascript
function requireConsent(session) {
  if (!session.consentRecordId || !session.consentCapturedAt) {
    throw new ConsentError('CONSENT_REQUIRED');
  }
  return true;
}
```

Consent is captured once per learner per tenant enrollment. It is stored as an immutable `ConsentRecord` entity. If a learner revokes consent, their active session must be terminated and their account locked pending data handling resolution.

---

## Audit Trigger List

Every one of these events must produce an immutable audit log entry (see `audit-log-schema` skill for entry shape):

- Login success and failure
- SSO assertion processed
- Session created, refreshed, or revoked
- Role assignment created or changed
- Password changed or reset
- Admin policy configuration changed
- Feature flag enabled or disabled
- Data export requested or completed
- Result statement issued or amended
- Simulation attempt record accessed by Lecturer or Admin
- Super Admin action of any kind

---

## What Not To Do

- Do not invent new role names — use only the eight defined roles
- Do not implement role checks only on the client side
- Do not allow open mentor self-signup
- Do not grant SSO users elevated permissions beyond their assigned role
- Do not allow a role change to take effect in the current session without explicit session refresh
- Do not allow tenant scope and role checks to be called separately — always call both
- Do not omit an audit log entry for any event in the trigger list above
