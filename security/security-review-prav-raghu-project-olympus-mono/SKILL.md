---
description: Security audit for backend services and API endpoints — authentication gaps, injection risks, hardcoded secrets, and permission bypass vectors.
disable-model-invocation: true
argument-hint: <branch, path, or service name, e.g. "apps/backend/admin-api/src/modules">
---

# Security Review

Audit the changes or files at: $ARGUMENTS

Run this diff first if reviewing a branch:

!`git diff origin/main..HEAD -- $ARGUMENTS 2>/dev/null || find $ARGUMENTS -name "*.ts" | head -20`

## Audit checklist

### Authentication & Authorization

- [ ] MSAL Bearer token validation happens via `AzureAuthGuard`, consistently — never a locally-signed/custom JWT in production code
- [ ] No route skips auth via query param, header trick, or env flag
- [ ] Genuinely public/unauthenticated endpoints are the exception, not the default
- [ ] `PermissionsGuard` (`@RequirePermissions`) fires on every write/destructive endpoint
- [ ] `req.user` is never taken from the request body or query string — only from the validated MSAL token

### Input Validation

- [ ] Every request body goes through `class-validator` decorators + the global `ValidationPipe({ whitelist: true, transform: true })`
- [ ] `forbidNonWhitelisted: true` (or equivalent) so unexpected fields are rejected, not silently dropped
- [ ] No raw/unparameterized SQL (Prisma raw queries, if any, are parameterized)
- [ ] File uploads validate MIME type and size before processing

### Secrets & Credentials

- [ ] No hardcoded secrets, Azure client secrets, API keys, tokens, or connection strings anywhere
- [ ] No sensitive values in log output (check `AzureMonitorLogger`'s redact list is complete)
- [ ] `.env` is gitignored; only `.env.example` with placeholders is committed
- [ ] No custom password hashing/storage anywhere — auth is delegated entirely to Azure MSAL

### Output & Data Exposure

- [ ] Prisma queries use `select` to exclude sensitive fields from responses
- [ ] Audit log `redact()` covers password, token, secret, hash, `twoFactorSecret`
- [ ] Webhook payloads contain no PII, passwords, or internal system IDs
- [ ] No stack traces or internal error messages in production API responses

### Infrastructure

- [ ] No wildcard `*` in CORS `origin` config in production
- [ ] Helmet is registered in every service's `main.ts`
- [ ] `@nestjs/throttler` rate limiting applied per tier (global/auth/sensitive/admin)
- [ ] SSRF prevention in place on any service making outbound HTTP calls (webhook delivery, `external-apis`)
- [ ] MySQL and Redis are never exposed on a public network/subnet

## Report format

Group findings as:

**Blockers** (must fix before merge) → **Warnings** (should fix) → **Suggestions** (nice to have)

Each finding: location, issue, concrete fix.
