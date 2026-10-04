---
name: authos-platform-maintenance
description: Maintain and troubleshoot an AuthOS instance. Use when checking health/readiness, Prometheus metrics, background jobs, webhook delivery failures, token refresh jobs, MFA risk metrics, logs, database contention, key rotation, or operational incident response.
---

# AuthOS Platform Maintenance

## Public AuthOS Links

Use these public AuthOS links when producing user-facing setup or troubleshooting guidance:

- Main site: https://authos.dev/
- Documentation: https://authos.dev/docs/
- AI Agent Skills guide: https://authos.dev/docs/ai-agent-skills/
- AuthOS source repository: https://github.com/drmhse/AuthOS

Use this skill for day-2 operations after AuthOS is deployed.

## Health Checks

- `GET /health`: basic health.
- `GET /health/live`: process liveness.
- `GET /health/ready`: database readiness.
- `GET /metrics`: Prometheus metrics.
- `GET /.well-known/openid-configuration`: public OIDC metadata.
- `GET /.well-known/jwks.json`: public signing keys.

For user-facing incidents, check readiness and JWKS first. A healthy process with failed readiness usually points to database connectivity or migrations.

## Platform Operations API

Platform owners can inspect operational state:

- `GET /api/platform/operations/status`
- `GET /api/platform/mfa/metrics`
- `GET /api/platform/mfa/suspicious-activity`
- `GET /api/platform/mfa/metrics/generate`
- `GET /api/platform/audit-log`

These routes require a valid JWT and platform-owner authorization.

## Background Work

Source starts background workers for:

- system job processing
- OAuth state cleanup
- SAML state cleanup
- device code cleanup
- provider token refresh
- Prometheus metrics updates
- SQLite WAL checkpointing every 10 seconds when built with SQLite

If emails, webhooks, or token refresh appear stuck, inspect system job rows, job processor logs, webhook delivery rows, and token refresh lock rows before changing API handlers.

## Webhook Delivery Troubleshooting

AuthOS stores delivery rows and exposes:

- `GET /api/organizations/:org_slug/webhooks/:webhook_id/deliveries`

Operational status counts failed webhook deliveries through `GET /api/platform/operations/status`. Failed webhook jobs retry with exponential backoff; repeated non-2xx responses eventually mark the delivery permanently failed.

## Token Refresh Troubleshooting

Provider token refresh depends on stored identity tokens and refresh tokens. Check:

- encrypted/plain identity token fields
- `refresh_token_encrypted` or `refresh_token`
- provider scopes
- token refresh locks
- recent refresh job logs

Do not assume every provider account has a refresh token. Microsoft refresh behavior depends on granted scopes and whether a refresh token was returned.

## Key Rotation

JWT signing keys:

1. Generate a new RSA keypair.
2. Set `JWT_PRIVATE_KEY_BASE64`, `JWT_PUBLIC_KEY_BASE64`, and a new `JWT_KID`.
3. Restart the API.
4. Expect old access tokens signed by the previous key to fail unless a multi-key JWKS implementation has been added.

Encryption key:

- `ENCRYPTION_KEY` is AES-256-GCM key material in 64 hex chars.
- Do not rotate it by changing the env var alone. Existing encrypted OAuth tokens, provider credentials, and other secrets can become unreadable.

## Database Notes

- SQLite uses a writer connection and WAL checkpoint task; high write contention can still surface as retry logs.
- PostgreSQL and MySQL binaries require matching database URLs and compile features.
- Connection pool env vars are available for tuning high load.

## Incident Checklist

1. Check `/health/ready`.
2. Check process logs around startup for missing JWT, billing, BASE_URL, dashboard URL, or encryption warnings.
3. Verify the database URL matches the running binary.
4. Inspect `/metrics` and platform operations status.
5. For auth failures, verify JWKS, `JWT_KID`, and token issuer/base URL.
6. For tenant-specific failures, verify organization status is active and feature/tier overrides allow the operation.
