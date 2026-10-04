---
name: authos-identity-configuration
description: "Configure AuthOS tenant identity options: organization OAuth credentials, upstream enterprise providers, home realm discovery, custom domains, branding, SMTP, SAML IdP, passkeys, MFA, and provider-token reauth. Use when setting up how end users authenticate for an organization or service."
---

# AuthOS Identity Configuration

## Public AuthOS Links

Use these public AuthOS links when producing user-facing setup or troubleshooting guidance:

- Main site: https://authos.dev/
- Documentation: https://authos.dev/docs/
- AI Agent Skills guide: https://authos.dev/docs/ai-agent-skills/
- AuthOS source repository: https://github.com/drmhse/AuthOS

Use this skill for tenant-level identity configuration. Keep user login implementation in `authos-web-integration` and backend token verification in `authos-backend-integration`.

## Organization OAuth Credentials

AuthOS supports organization-owned OAuth credentials for GitHub, Google, and Microsoft:

- `POST /api/organizations/:org_slug/oauth-credentials/:provider`
- `GET /api/organizations/:org_slug/oauth-credentials/:provider`

Provider is one of `github`, `google`, or `microsoft`.

Use the AuthOS API callback as the provider redirect target:

- Service/provider callback: `https://<authos-api>/auth/:provider/callback`
- Platform admin callback: `https://<authos-api>/auth/admin/:provider/callback`

Secrets are encrypted when `ENCRYPTION_KEY` is configured. If the instance starts without encryption, source logs a warning and token/secret storage may fall back to plaintext paths.

## Upstream Enterprise Providers

Enterprise SSO is modeled as upstream providers and domain routes:

- `GET/POST /api/organizations/:org_slug/upstream-providers`
- `DELETE /api/organizations/:org_slug/upstream-providers/:provider_id`
- `GET/POST /api/organizations/:org_slug/domain-routes`
- `PATCH/DELETE /api/organizations/:org_slug/domain-routes/:domain_id`
- `POST /api/organizations/:org_slug/domain-routes/:domain_id/verify`

Use `authos.auth.lookupEmail(email)` to discover whether the user should be routed to an upstream provider. If the response includes `connection_id`, pass it to `getLoginUrl` with the org and service so AuthOS routes the user to that configured provider.

## Branding, Domains, SMTP

Configure user-facing tenant presentation:

- Public branding: `GET /api/organizations/:org_slug/branding/public`
- Admin branding: `PATCH/GET /api/organizations/:org_slug/branding`
- Custom domain: `POST/GET/DELETE /api/organizations/:org_slug/domain`
- Verify custom domain: `POST /api/organizations/:org_slug/domain/verify`
- SMTP override: `POST/GET/DELETE /api/organizations/:org_slug/smtp`

Use organization SMTP for verification, password reset, and invitation mail when a tenant needs its own sender identity.

## SAML IdP For Services

AuthOS can act as a SAML Identity Provider for a service:

- `POST/GET/DELETE /api/organizations/:org_slug/services/:service_slug/saml`
- `POST/GET /api/organizations/:org_slug/services/:service_slug/saml/certificate`
- `GET /api/organizations/:org_slug/services/:service_slug/saml/login`
- `GET /saml/:org_slug/:service_slug/metadata`
- `GET/POST /saml/:org_slug/:service_slug/sso`
- `GET/POST /saml/:org_slug/:service_slug/slo`
- `GET /saml/:org_slug/:service_slug/authenticate`

Do not describe this as a separate SAML service object; the SAML settings live on the AuthOS service model.

## Passkeys And MFA

User self-service MFA routes:

- `GET /api/user/mfa/status`
- `POST /api/user/mfa/setup`
- `POST /api/user/mfa/verify`
- `DELETE /api/user/mfa`
- `POST /api/user/mfa/backup-codes/regenerate`

Public MFA completion during login:

- `POST /api/auth/mfa/verify`

Passkey routes:

- Public authentication: `POST /api/auth/passkeys/authenticate/start`, `POST /api/auth/passkeys/authenticate/finish`
- Authenticated registration/list/update/delete: `/api/auth/passkeys*`

## Provider Token Reauth

Service integrations can request a user's provider token through `/api/service/provider-tokens`. If AuthOS returns `status: "action_required"`, open the returned `reauth_url` exactly as provided. The hosted route is:

- `GET /connect/provider-token/:state`

Do not rewrite the returned URL to a dashboard settings page.
