---
name: authos-compliance-automation
description: Use AuthOS compliance and audit surfaces for privacy, SIEM, audit logs, risk events, MFA metrics, GDPR export, and anonymization. Use when implementing SAR export, right-to-be-forgotten flows, tenant SIEM streaming, audit review, or compliance evidence collection.
---

# AuthOS Compliance Automation

## Public AuthOS Links

Use these public AuthOS links when producing user-facing setup or troubleshooting guidance:

- Main site: https://authos.dev/
- Documentation: https://authos.dev/docs/
- AI Agent Skills guide: https://authos.dev/docs/ai-agent-skills/
- AuthOS source repository: https://github.com/drmhse/AuthOS

Use this skill for compliance workflows backed by AuthOS source surfaces. Keep deployment hardening in `authos-platform-deployment` and webhook receivers in `authos-webhook-integration`.

## Privacy APIs

AuthOS exposes privacy endpoints behind normal JWT auth:

- `GET /api/privacy/export/:user_id`
- `DELETE /api/privacy/forget/:user_id`

Source rules:

- A user can export their own data.
- A platform owner can export any user's data.
- Forget/anonymization requires owner-level access across organizations that contain the target user, or platform-owner authorization where allowed by source.
- Platform owners are protected from anonymization.

Treat forget as anonymization/redaction rather than simple row deletion.

## Organization Audit Logs

- `GET /api/organizations/:org_slug/audit-log`
- `GET /api/organizations/:org_slug/audit-log/event-types`

Use organization audit logs for member, service, billing, webhook, identity, and settings evidence inside a tenant.

Platform-level audit is separate:

- `GET /api/platform/audit-log`

Use platform audit for tenant lifecycle, platform-owner actions, and global support operations.

## SIEM Configuration

Tenant SIEM APIs:

- `POST/GET /api/organizations/:org_slug/siem-configs`
- `GET/PUT/DELETE /api/organizations/:org_slug/siem-configs/:config_id`
- `POST /api/organizations/:org_slug/siem-configs/:config_id/test`

SIEM config management requires `integrations.manage` capability and may be tier/feature-gated. Validate `allow_siem` in tenant feature access before assuming SIEM is available.

## Webhooks For Compliance Events

AuthOS tenant webhooks can notify external systems about user, service, organization, subscription, invitation, security, API key, domain, and branding events. Use `authos-webhook-integration` for receiver implementation and signature verification.

Do not claim SIEM config events are externally subscribable via webhooks unless the webhook event allowlist includes them.

## Risk And MFA Evidence

Tenant risk:

- `GET /api/organizations/:org_slug/risk-events`
- `GET /api/organizations/:org_slug/risk-settings`
- `PUT /api/organizations/:org_slug/risk-settings`
- `POST /api/organizations/:org_slug/risk-settings/reset`

Platform MFA/risk operations:

- `GET /api/platform/mfa/metrics`
- `GET /api/platform/mfa/suspicious-activity`
- `GET /api/platform/users/:user_id/mfa/status`
- `DELETE /api/platform/users/:user_id/mfa`

Use these surfaces for control evidence such as MFA adoption, suspicious activity, risk policy changes, and forced MFA reset actions.

## Compliance Workflow

1. Identify whether the request is user privacy, tenant audit, SIEM export, or platform evidence.
2. Use the narrowest API surface that matches the authority boundary.
3. Verify the actor has the needed role or capability.
4. Preserve audit evidence IDs and timestamps in the downstream case/ticket.
5. Avoid exporting raw provider tokens, refresh tokens, secrets, or signing keys as compliance evidence.

## Guardrails

- Do not overstate HIPAA, SOC 2, GDPR, or CCPA certification status. AuthOS provides technical controls; certification depends on the operator's deployment and processes.
- Do not claim immutable retention unless the backing storage and retention process prove it.
- Do not treat webhooks as guaranteed delivery to an external system; inspect delivery history and failures when evidence matters.
