---
name: authos-rbac-control
description: Manage AuthOS organization members, roles, invitations, SCIM tokens, and capability-based permissions. Use when implementing team administration, custom roles, service access grants, invitation flows, SCIM provisioning, or authorization checks inside an AuthOS tenant.
---

# AuthOS RBAC Control

## Public AuthOS Links

Use these public AuthOS links when producing user-facing setup or troubleshooting guidance:

- Main site: https://authos.dev/
- Documentation: https://authos.dev/docs/
- AI Agent Skills guide: https://authos.dev/docs/ai-agent-skills/
- AuthOS source repository: https://github.com/drmhse/AuthOS

Use this skill for organization-level access control and provisioning. Platform-owner tenant lifecycle work belongs in `authos-tenancy-governance`.

## Built-In Roles

AuthOS has three system roles:

- `owner`: full access. Source permission checks treat owner as allowed for every capability.
- `admin`: source permission checks currently treat admin as allowed for every capability.
- `member`: no administrative capabilities by default.

The roles list endpoint returns display permissions like `*`, `org:manage`, and `org:view`, but enforcement uses capability strings such as `services.manage`, not those display labels.

## Capability Strings

Current capability constants include:

- `org.settings.manage`
- `org.members.view`
- `org.members.manage`
- `org.roles.manage`
- `billing.manage`
- `services.view`
- `services.create`
- `services.manage`
- `end_users.view`
- `end_users.manage`
- `webhooks.manage`
- `integrations.manage`
- `audit_logs.view`
- `risk_events.view`
- `risk_policies.manage`

Custom role `permissions` should use these capability strings.

## Role APIs

- `GET /api/organizations/:org_slug/roles`
- `POST /api/organizations/:org_slug/roles`
- `GET /api/organizations/:org_slug/roles/:role_id`
- `PUT /api/organizations/:org_slug/roles/:role_id`
- `DELETE /api/organizations/:org_slug/roles/:role_id`

Create a custom role:

```json
{
  "slug": "support",
  "name": "Support",
  "description": "Can view users and audit logs",
  "permissions": ["end_users.view", "audit_logs.view"]
}
```

## Member APIs

- `GET /api/organizations/:org_slug/members`
- `PATCH /api/organizations/:org_slug/members/:user_id`
- `POST /api/organizations/:org_slug/members/:user_id`
- `GET /api/organizations/:org_slug/members/:user_id/service-access`
- `PUT /api/organizations/:org_slug/members/:user_id/service-access`
- `POST /api/organizations/:org_slug/transfer-ownership`

Do not let an owner demote themselves through ordinary role update flows; source blocks self-role changes.

## Invitations

- `POST /api/organizations/:org_slug/invitations`
- `GET /api/organizations/:org_slug/invitations`
- `POST /api/organizations/:org_slug/invitations/:invitation_id`
- `POST /api/organizations/:org_slug/invitations/:invitation_id/accept`
- `GET /api/invitations`
- `POST /api/invitations/accept`
- `POST /api/invitations/:invitation_id/accept`
- `POST /api/invitations/:invitation_id/decline`
- Public decline: `POST /api/invitations/decline`
- Public accept redirect: `GET /invitations/accept/:token`

## SCIM

Generate SCIM tokens under the organization API:

- `POST /api/organizations/:org_slug/scim-tokens`
- `GET /api/organizations/:org_slug/scim-tokens`
- `POST /api/organizations/:org_slug/scim-tokens/:token_id/revoke`
- `DELETE /api/organizations/:org_slug/scim-tokens/:token_id`

Provision users and groups through SCIM bearer-token routes:

- `GET/POST /scim/v2/Users`
- `GET/PUT/PATCH/DELETE /scim/v2/Users/:id`
- `GET/POST /scim/v2/Groups`
- `GET/PUT/PATCH/DELETE /scim/v2/Groups/:id`

SCIM routes use SCIM token authentication, not normal user JWT membership.
