---
name: authentication-flow
description: Implement, review, and improve authentication flows securely and consistently. Use when Codex needs to work on login, registration, logout, password handling, password reset, email or OTP verification, sessions, JWTs, refresh tokens, OAuth/social login, auth state, protected frontend routes, backend auth middleware, token storage, failed login handling, account status, or user identity responses for web, mobile, admin, staff, customer, SaaS, ecommerce, booking, delivery, or multi-role business apps.
---

# Authentication Flow

Use this skill when work touches how users prove identity, stay logged in, recover access, or reach protected areas.

## Core Rule

Treat authentication as security-sensitive work. Inspect the existing identity, credential, token/session, frontend state, backend guard, logout, and role/ownership patterns before editing.

## Workflow

1. Understand the authentication requirement:
   - actor, platform, credential type, identity record, protected areas, success behavior, and failure behavior
2. Inspect existing authentication patterns:
   - auth routes, user/account models, password utilities, token/session helpers, middleware/guards, frontend auth store/context, protected routes, mobile secure storage, env config, tests, and docs
3. Identify the current auth method:
   - email/password, username/password, phone/OTP, magic link, JWT, refresh token, cookie session, OAuth/social login, API key, or SSO
4. Extend the existing auth method unless there is a clear reason to change it.
5. Review credential handling:
   - password hashing, password validation, reset tokens, verification codes, generic errors, and absence of credential logging
6. Review registration and login behavior:
   - required fields, uniqueness checks, account status, verification status, role assignment, token/session creation, safe response shape, and frontend state update
7. Review token or session behavior:
   - payload, expiration, signing secret usage, refresh rotation, revocation, storage location, expired-session handling, and logout invalidation
8. Review frontend auth behavior:
   - storage, route guards, loading state, unauthenticated redirects, role-specific navigation, logout cleanup, and private data cache clearing
9. Review backend protection:
   - every protected endpoint must validate auth server-side and apply authorization or ownership checks where roles, tenants, shops, customers, or staff scopes matter
10. Review reset, verification, failed login, and account recovery flows when they are involved.
11. Add or update tests where practical.
12. Summarize the implemented or reviewed flow, files changed, checks run, risks, and follow-up recommendations.

Read `references/authentication-checklist.md` for field-level checks, sensitive-data rules, test ideas, and the final report format.

## Non-Negotiable Rules

- Do not store passwords in plain text.
- Do not return password hashes, reset tokens, refresh tokens, or internal security flags in API responses.
- Do not log passwords, tokens, OTP codes, reset links, secrets, or private credentials.
- Do not place sensitive private data inside JWT payloads.
- Do not let public registration assign privileged roles unless explicitly protected.
- Do not rely only on frontend route guards to protect data.
- Do not skip backend auth checks for protected endpoints.
- Do not skip authorization or ownership checks when roles or tenant scope matter.
- Do not expose whether an account exists through overly specific login, reset, or verification errors.
- Do not leave refresh tokens or server sessions active after logout when revocation is expected.
- Do not store mobile tokens in plain insecure storage when secure storage exists.
- Do not introduce a new authentication method without a clear project reason.

## Output Contract

When using this skill, provide:

1. Authentication feature reviewed or implemented.
2. Auth method and token/session strategy.
3. Registration, login, logout, refresh, reset, or verification behavior involved.
4. Protected frontend routes and backend endpoints.
5. Sensitive data protections.
6. Validation and error handling rules.
7. Files changed.
8. Tests/checks or manual verification.
9. Risks, gaps, and recommended follow-up.
