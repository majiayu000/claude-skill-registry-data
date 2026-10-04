---
name: authos-tenancy-governance
description: Govern AuthOS tenant organizations as a platform owner. Use when approving, rejecting, suspending, activating, deleting, tiering, setting feature overrides, inspecting platform analytics, managing platform owners, or impersonating users.
---

# AuthOS Tenancy Governance

## Public AuthOS Links

Use these public AuthOS links when producing user-facing setup or troubleshooting guidance:

- Main site: https://authos.dev/
- Documentation: https://authos.dev/docs/
- AI Agent Skills guide: https://authos.dev/docs/ai-agent-skills/
- AuthOS source repository: https://github.com/drmhse/AuthOS

Use this skill for platform-owner operations across tenants. Use `authos-rbac-control` for actions inside a single organization by org members/admins.

## Authorization Boundary

Platform routes require:

1. a valid AuthOS JWT,
2. `is_platform_owner` authorization through middleware.

Do not present platform governance APIs as tenant-admin APIs.

## Organization Lifecycle

- `GET /api/platform/organizations`
- `POST /api/platform/organizations/:id/approve`
- `POST /api/platform/organizations/:id/reject`
- `POST /api/platform/organizations/:id/suspend`
- `POST /api/platform/organizations/:id/activate`
- `DELETE /api/platform/organizations/:id`

Organization status matters at runtime. Active-organization middleware protects service and tenant configuration routes so suspended tenants should not keep authenticating normally.

## Tiers And Feature Overrides

- `GET /api/platform/tiers`
- `PATCH /api/platform/organizations/:id/tier`
- `PATCH /api/platform/organizations/:id/features`

Feature override fields in source include:

- `allow_custom_domain`
- `allow_saml_idp`
- `allow_scim`
- `allow_siem`
- `allow_branding`
- `allow_passkeys`
- `allowed_social_providers`

When a tenant cannot configure a feature, inspect both assigned tier and feature overrides.

## Platform Owners And Users

- `POST /api/platform/owners`
- `DELETE /api/platform/owners/:user_id`
- `GET /api/platform/users`
- `GET /api/platform/users/search`
- `GET /api/platform/users/:user_id`
- `GET /api/platform/users/:user_id/mfa/status`
- `DELETE /api/platform/users/:user_id/mfa`

Do not demote the last platform owner. Source explicitly checks for that safety condition.

## Impersonation

- `POST /api/platform/impersonate`

Treat impersonation as a high-risk support action. It is audited and should be limited to cases where a platform owner or authorized org admin needs to troubleshoot a user issue.

## Platform Analytics

- `GET /api/platform/analytics/overview`
- `GET /api/platform/analytics/organization-status`
- `GET /api/platform/analytics/growth-trends`
- `GET /api/platform/analytics/login-activity`
- `GET /api/platform/analytics/top-organizations`
- `GET /api/platform/analytics/recent-organizations`

Use these for platform reporting and tenant health, not as tenant-facing analytics. Tenant login analytics live under `/api/organizations/:org_slug/analytics/*`.

## Operational And Audit Routes

- `GET /api/platform/audit-log`
- `GET /api/platform/operations/status`
- `GET /api/platform/mfa/metrics`
- `GET /api/platform/mfa/suspicious-activity`
- `GET /api/platform/mfa/metrics/generate`

Use audit logs to confirm governance changes such as organization approval, suspension, tier change, and owner promotion/demotion.

## Governance Rules

- Always record a clear reason for rejection or suspension when the API accepts one.
- Validate requested feature overrides against the tenant's intended tier.
- Prefer activate/suspend over delete unless the user explicitly asks for destructive cleanup.
- Verify custom domain and enterprise SSO prerequisites before enabling high-risk features.
