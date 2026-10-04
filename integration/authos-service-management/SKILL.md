---
name: authos-service-management
description: Manage AuthOS tenant services, OAuth client credentials, redirect URIs, device activation URIs, plans, API keys, SAML settings, and checkout. Use when creating or configuring applications inside an AuthOS organization.
---

# AuthOS Service Management

## Public AuthOS Links

Use these public AuthOS links when producing user-facing setup or troubleshooting guidance:

- Main site: https://authos.dev/
- Documentation: https://authos.dev/docs/
- AI Agent Skills guide: https://authos.dev/docs/ai-agent-skills/
- AuthOS source repository: https://github.com/drmhse/AuthOS

Use this skill when configuring applications inside an AuthOS organization. Use `authos-service-api-integration` when consuming service API routes with an API key.

## Service Model

An AuthOS service represents an application owned by an organization. Source fields include:

- `slug`, `name`, `service_type`
- `client_id`
- hashed `client_secret`
- provider scopes for GitHub, Google, and Microsoft
- `redirect_uris`
- `device_activation_uri`
- SAML IdP fields such as entity ID, ACS URL, SLO URL, NameID format, attribute mapping, and signing flags

Core API service types used in the codebase include `web`, `api`, `mobile`, and `desktop`. Treat `mobile` and `desktop` as public clients that require PKCE in OAuth callback paths.

The standalone lite Platform Setup workspace currently presents simpler application labels: `web`, `native`, `spa`, and `machine`. Use those labels only when editing the managed standalone config through the lite setup flow; for direct organization service API calls, use the core API service type values unless the source has changed.

## Service APIs

- `GET/POST /api/organizations/:org_slug/services`
- `GET/PATCH/DELETE /api/organizations/:org_slug/services/:service_slug`
- `POST /api/organizations/:org_slug/services/:service_slug/secret/rotate`

Create a service:

```json
{
  "slug": "web-app",
  "name": "Web App",
  "service_type": "web",
  "redirect_uris": ["https://app.example.com/callback"],
  "github_scopes": ["user:email"],
  "google_scopes": ["openid", "email", "profile"],
  "microsoft_scopes": ["offline_access", "User.Read"]
}
```

The secret is hashed server-side. Persist the returned secret immediately; retrieve flows should not expect to read it back later. Use the rotate endpoint when it is lost or compromised.

## Plans

- `GET/POST /api/organizations/:org_slug/services/:service_slug/plans`
- `PATCH/DELETE /api/organizations/:org_slug/services/:service_slug/plans/:plan_id`

Plans belong to services and are used by subscription and checkout flows. Do not delete a plan that still has active subscriptions.

## Service API Keys

- `GET/POST /api/organizations/:org_slug/services/:service_slug/api-keys`
- `GET/DELETE /api/organizations/:org_slug/services/:service_slug/api-keys/:api_key_id`

API keys authenticate service-to-service calls using `X-Api-Key`. Never place these keys in browser, mobile, or desktop client code.

## SAML Configuration

- `POST/GET/DELETE /api/organizations/:org_slug/services/:service_slug/saml`
- `POST/GET /api/organizations/:org_slug/services/:service_slug/saml/certificate`
- `GET /api/organizations/:org_slug/services/:service_slug/saml/login`

Public SAML runtime routes:

- `GET /saml/:org_slug/:service_slug/metadata`
- `GET/POST /saml/:org_slug/:service_slug/sso`
- `GET/POST /saml/:org_slug/:service_slug/slo`
- `GET /saml/:org_slug/:service_slug/authenticate`

## Checkout

Create a checkout session for a service:

- `POST /api/organizations/:org_slug/services/:service_slug/checkout`

AuthOS also has organization-level billing routes and provider-specific webhook receivers. Keep billing provider configuration in deployment or tenancy skills, not inside frontend integration.

## Configuration Rules

- Always register exact `redirect_uris`; AuthOS validates service callbacks against them.
- Configure `device_activation_uri` before offering device flow for a service.
- Use provider scopes on the service to define what end-user OAuth should request.
- For public clients, include PKCE support in the integration plan.
