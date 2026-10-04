---
name: okta
description: "Expert agent for Okta identity platform. Provides deep expertise in Universal Directory, Adaptive MFA, Lifecycle Management, Workflows, API Access Management, ThreatInsight, and Identity Governance. WHEN: \"Okta\", \"Universal Directory\", \"OIN\", \"Okta Workflows\", \"Okta MFA\", \"Okta SSO\", \"ThreatInsight\", \"Okta Lifecycle\", \"Okta SCIM\", \"Okta API Access Management\"."
license: MIT
---

# Okta

This skill covers the Okta identity platform. It has deep knowledge of Universal Directory, Adaptive MFA, Lifecycle Management, Workflows, API Access Management, OIN integrations, Identity Governance, and ThreatInsight.

## Identity and Scope

Okta is a cloud-native identity platform that provides:
- Universal Directory for centralized identity management
- SSO via SAML 2.0, OIDC, and WS-Federation to 7,000+ OIN integrations
- Adaptive MFA with risk-based authentication
- Lifecycle Management for automated provisioning (SCIM, HR-driven)
- Workflows for no-code identity automation
- API Access Management (OAuth 2.0 authorization server)
- Identity Governance for access certifications and SOD
- ThreatInsight and Identity Threat Protection for security intelligence

## How to Approach Tasks

When you receive a request:

1. **Classify** the request:
   - **SSO / Integration** -- Application integration via OIN, SAML, OIDC
   - **MFA / Authentication** -- Factor enrollment, Adaptive MFA, authenticator configuration
   - **Provisioning** -- SCIM, Lifecycle Management, HR-driven flows
   - **Automation** -- Workflows, event hooks, inline hooks
   - **API security** -- API Access Management, OAuth 2.0 authorization servers
   - **Governance** -- Access certifications, entitlement management
   - **Security** -- ThreatInsight, Identity Threat Protection, log analysis

2. **Identify Okta SKU** -- Features vary by license:
   - **SSO** -- Basic SSO, MFA, Universal Directory, OIN
   - **Adaptive SSO** -- Risk-based authentication, ThreatInsight
   - **Lifecycle Management** -- SCIM provisioning, HR integrations
   - **Workflows** -- No-code automation
   - **API Access Management** -- Custom OAuth 2.0 authorization servers
   - **Identity Governance** -- Access certifications, entitlement management, SOD
   - **Identity Threat Protection** -- Continuous risk evaluation, CAEP

3. **Analyze** -- Apply Okta-specific reasoning. Consider Universal Directory profile mappings, authentication policies, and Okta Expression Language.

4. **Recommend** -- Provide actionable configuration guidance with Okta admin console paths and API examples.

## Core Expertise

### Universal Directory

Okta's cloud directory that serves as the hub for all identities:

- **Profile master** -- Defines which source controls each attribute (Okta, AD, LDAP, HR system)
- **Custom attributes** -- Extend the Okta user profile with custom properties
- **Profile mappings** -- Map attributes between Okta profile and application profiles
- **Groups** -- Push groups, Okta groups, AD groups, dynamic groups (Okta Expression Language)

**Profile master priority:** When multiple sources provide the same attribute, profile master priority determines which source wins. Example: HR system masters `department`, AD masters `samAccountName`, Okta masters custom attributes.

**Okta Expression Language (OEL):**
```javascript
// Dynamic group rule: all users in Engineering department
user.department == "Engineering"

// Conditional attribute mapping
user.department == "Sales" ? "sales-team" : "general"

// String manipulation
String.substringBefore(user.email, "@")

// Array operations
Arrays.contains(user.groups, "Admin")
```

### Authentication Policies

Okta uses authentication policies (formerly Sign-On Policies) to control how users authenticate:

**Global Session Policy:**
- Controls session behavior (MFA requirements, session lifetime)
- Evaluated first, determines if MFA is required for the session

**Authentication Policies (per-app):**
- Controls access to specific applications
- Can require specific authenticators, device trust, network zones
- Priority-ordered rules evaluated top-to-bottom

**Policy evaluation flow:**
```
User requests access to app
  --> Global Session Policy (session-level MFA, session lifetime)
  --> App-level Authentication Policy (app-specific requirements)
  --> Authenticator enrollment policy (which factors user can use)
  --> Access granted or denied
```

### Adaptive MFA

Okta's risk-based authentication evaluates context to determine authentication requirements:

**Risk signals:**
- Device context (known vs. unknown device, managed vs. unmanaged)
- Network context (known network zone, IP reputation)
- Location context (country, impossible travel)
- Behavior context (login patterns, velocity)
- ThreatInsight signals (IP-based threat intelligence)

**Authenticator types:**

| Authenticator | Type | Phishing Resistant | Notes |
|---|---|---|---|
| Okta Verify (push) | Possession | No (fatigue risk) | Number challenge improves resistance |
| Okta Verify (TOTP) | Possession | No | Standard TOTP |
| Okta FastPass | Possession + Device | Yes (device-bound) | Passwordless, phishing-resistant |
| FIDO2/WebAuthn | Possession + Inherence | Yes | Hardware security keys, platform authenticators |
| Phone (SMS/Voice) | Possession | No | SIM swap vulnerable, last resort |
| Email | Possession | No | Account compromise risk |
| Google Authenticator | Possession | No | Standard TOTP |
| Security Question | Knowledge | No | Weak, being deprecated |

**Recommendation:** Okta FastPass + FIDO2 for phishing-resistant passwordless. Okta Verify with number challenge as fallback.

### Lifecycle Management

Automated user provisioning and deprovisioning:

**Provisioning methods:**
- **SCIM 2.0** -- Standard REST API provisioning to SCIM-enabled applications
- **SAML JIT** -- Just-in-Time provisioning on first SAML login (limited attributes)
- **HR-driven** -- Source identities from Workday, BambooHR, SAP SuccessFactors, etc.
- **Custom** -- API-based provisioning via Workflows or event hooks

**Provisioning features:**
- **Push groups** -- Sync Okta groups to downstream applications
- **Attribute mapping** -- Map Okta user profile attributes to application attributes
- **Provisioning actions:** Create users, update profiles, deactivate users, sync passwords
- **Profile sync** -- Bidirectional sync (Okta to app, app to Okta)

**HR-driven provisioning flow:**
```
HR System (Workday, etc.)
  --> Okta Universal Directory (create/update/deactivate user)
  --> Downstream Apps via SCIM (provision/deprovision)
  --> AD/LDAP via Okta AD Agent (if hybrid)
```

### Workflows

No-code identity automation platform:

**Components:**
- **Flows** -- Sequences of actions triggered by events
- **Connectors** -- Pre-built integrations (Slack, Jira, ServiceNow, O365, custom API)
- **Tables** -- Built-in data storage for workflow state
- **Functions** -- Custom logic (list operations, text manipulation, math, branching)

**Common workflow patterns:**
- **Onboarding automation** -- When user created: assign groups, send welcome email, create Jira ticket, provision Slack
- **Offboarding automation** -- When user deactivated: revoke sessions, remove from groups, transfer file ownership, archive mailbox
- **Access request** -- User requests access via Slack, manager approves, Workflow grants access
- **Scheduled reports** -- Weekly report of users without MFA enrolled, sent to security team
- **Threat response** -- When suspicious activity detected: suspend user, notify SOC, create incident ticket

### API Access Management

Okta as an OAuth 2.0 authorization server for API security:

**Custom authorization servers:**
- Define scopes, claims, and access policies per API
- Issue access tokens (JWT) for API consumers
- Support token introspection and revocation
- Inline hooks for custom claim augmentation

**Token structure:**
```json
{
  "iss": "https://company.okta.com/oauth2/default",
  "sub": "user@example.com",
  "aud": "api://my-api",
  "iat": 1712345678,
  "exp": 1712349278,
  "scp": ["read:data", "write:data"],
  "groups": ["Engineering", "API-Users"],
  "custom_claim": "custom_value"
}
```

**Access policies:** Control which clients can request which scopes:
- Client application whitelist
- Scope restrictions per policy rule
- Token lifetime configuration
- Refresh token behavior

### ThreatInsight

IP-based threat intelligence:
- Evaluates sign-in attempts against Okta's threat intelligence database
- Actions: none, audit (log only), block (deny + log)
- Protects against credential stuffing, brute force, and distributed attacks
- Operates at the org level, before authentication policy evaluation
- Exempt trusted proxy IPs (CDN, WAF) from ThreatInsight evaluation

### Identity Threat Protection with Okta AI

Continuous risk evaluation during active sessions:
- Evaluates risk signals throughout the session (not just at login)
- Integrates with CAEP (Continuous Access Evaluation Protocol)
- Can trigger step-up authentication, session termination, or alerts mid-session
- Integrates with third-party security signals (EDR, SIEM)

### Identity Governance (OIG)

Access certifications and governance:
- **Access certifications** -- Periodic reviews of user access to applications and resources
- **Entitlement management** -- Request, approve, and audit access to resources
- **SOD policies** -- Define and enforce separation of duties rules
- **Governance reports** -- Visibility into who has access to what

## Okta Administration

### System Log

Okta System Log is the primary audit trail:
```
GET /api/v1/logs?filter=eventType eq "user.session.start"&since=2024-01-01T00:00:00Z
```

**Critical events to monitor:**
- `user.session.start` -- User sign-in
- `user.authentication.auth_via_mfa` -- MFA challenge
- `policy.evaluate_sign_on` -- Policy evaluation
- `user.lifecycle.create` -- User creation
- `user.lifecycle.deactivate` -- User deactivation
- `user.account.lock` -- Account lockout
- `system.api_token.create` -- API token created (high alert)
- `application.user_membership.add` -- User assigned to app
- `zone.update` -- Network zone modified

### Rate Limits

Okta enforces rate limits per endpoint:
- `/api/v1/authn` -- 600/minute (authentication)
- `/api/v1/users` -- 600/minute (user CRUD)
- `/api/v1/apps` -- 600/minute (app management)
- `/oauth2/default/v1/token` -- 2400/minute (token issuance)

Monitor `X-Rate-Limit-Remaining` headers. Implement exponential backoff in automations.

## Common Pitfalls

1. **Default authentication policy too permissive** -- The default "catch-all" rule often allows password-only access. Always configure MFA requirements.
2. **Okta Verify without number challenge** -- Simple push notifications are vulnerable to MFA fatigue attacks. Enable number matching.
3. **Over-scoped API tokens** -- Okta API tokens inherit the permissions of the creating admin. Use scoped OAuth 2.0 tokens (service apps) instead.
4. **Profile mapping conflicts** -- When multiple sources map to the same attribute, unexpected values can occur. Clearly define profile mastering.
5. **Not monitoring System Log** -- Okta System Log is the primary security telemetry source. Export to SIEM and alert on critical events.
6. **Deprovisioning gaps** -- Applications not connected to Lifecycle Management require manual deprovisioning. Audit for coverage.

## Reference Files

Load these for deep knowledge:
- `references/architecture.md` -- Okta internals: Universal Directory data model, agent architecture, OIN integration patterns, rate limits, high availability, and Okta Expression Language reference.
