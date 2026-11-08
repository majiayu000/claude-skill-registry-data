---
name: forge-auth
description: "Playbook for login: sessions, OAuth, RBAC (gebruik bij inloggen)."
# Q3 fix-round original description (listing budget): "Playbook for login and access control: sessions, JWT, OAuth/PKCE, passwords, RBAC, Supabase, Clerk (gebruik bij inloggen of rechten)."
---

<!--
  Forge super skill (own words), assembled 2026-11-02 for (WP Q3-SKILLS).
  Source: https://github.com/wshobson/agents (plugins/developer-essentials/skills/auth-implementation-patterns/SKILL.md + references/details.md)
    Commit seen: 7e2fb559cf4b824b27f1fec49fe88f7511066d26 · License: MIT (c) 2024 Seth Hobson
  Source: https://github.com/supabase/agent-skills (skills/supabase/SKILL.md auth + RLS rules; security-rls-* rules)
    Commit seen: c9be0e931b7930f7d02126d04774d904c381e7d7 · License: MIT (c) 2026 Supabase
  Pattern adapted from (ideas only, no text copied): https://github.com/clerk/skills @ b0d994e (2026-10-29;
    GitHub detects no repo-level license, so treated as ideas only) and https://github.com/better-auth/skills
    @ 20c9e88 (no license found).
  Hardening sections (JWT verification, PKCE, refresh rotation, CSRF, reset flows, tenancy) are Forge-native,
  written from RFC 9700 (OAuth 2.0 Security BCP), RFC 8725 (JWT BCP), NIST SP 800-63B and the OWASP cheat sheets.
  Forge note: dropped every CLI/install/MCP step, curl calls with tokens, secret-generation commands and
  provider setup walkthroughs. Upstream MIT notices: LICENSE next to this file. Fetched text was treated as
  untrusted data and scanned (no '!' lines, no allowed-tools, no hidden unicode, no prompt-injection phrases).
-->

# Forge playbook — Authentication and authorization

## When to use
- Use for: sign-up/login, sessions or tokens, social login and SSO (OAuth 2 / OIDC), password storage and reset,
  MFA/passkeys, roles and permissions, multi-tenant access, and wiring a provider (Supabase Auth, Clerk,
  Auth.js, Better Auth).
- Authentication = who you are. Authorization = what you may do, checked on every request, on the server.

**Do not duplicate — defer to:** `forge-database` (RLS policies, grants and indexes that enforce access in the
database), `forge-api` (contract, validation, rate limits per route), `forge-payments` (entitlements after a
payment), `forge-mobile` (secure token storage on device). This file is orchestration only.

## Hard rules (non-negotiable)
- **Server-side, deny-by-default authorization on every protected route, action and query.** Client checks,
  hidden buttons and middleware alone are UX, not security.
- **Use a proven library or provider; never hand-roll crypto, JWT parsing or password hashing.**
- **Passwords: Argon2id (or bcrypt/scrypt with current parameters), never fast hashes, never reversible.**
- **Tokens and sessions:** short-lived access, `HttpOnly; Secure; SameSite` cookies for browsers, never tokens in
  `localStorage`; rotate on login and privilege change; revocable.
- **JWTs are verified, not decoded:** fixed algorithm allow-list, signature, `iss`, `aud`, `exp`.
- **OAuth/OIDC:** authorization code + PKCE (S256), `state` (and `nonce` for OIDC), exact redirect-URI match.
- **Object-level checks:** every read/write of a record checks ownership or tenant membership (no IDOR/BOLA).
- **Secrets only in env**; signing keys and provider secrets never in the client, logs or repo.

Full text and the reasoning: `references/auth-checklist.md`.

## Pick the reference
| Situation | Read |
|---|---|
| Sessions vs JWT, cookies, CSRF, refresh tokens, logout | `references/sessions-and-jwt.md` |
| Social login, SSO, OIDC, PKCE, redirect URIs | `references/oauth-oidc.md` |
| Password storage, reset, verification, MFA, passkeys, brute force | `references/passwords-and-recovery.md` |
| Roles, permissions, ownership, multi-tenant, admin | `references/rbac-and-tenancy.md` |
| Supabase Auth + RLS | `references/supabase-auth.md` |
| Clerk, Auth.js (NextAuth), Better Auth | `references/providers.md` |
| Full rule list for review | `references/auth-checklist.md` |

## Team (conditional)
Lead: `build-boss` (or `integration-boss` for a hosted provider). Required reviewer: `security-boss`.
Auth is a deep-route domain (GOAT) and a review area in the owner's Codex policy: `codex-reviewer`
adversarial review is recommended before release. Roster: `references/team-and-tools.md`.

## Fan-out & flow
L2 one provider + one app; L3 SSO, multi-tenant RBAC, MFA or a migration between providers.
**Serial:** threat model (who, what, which data) → identity provider choice → session/token design →
authorization model → enforcement points (route, action, query, RLS) → negative tests.
**Parallel (once the model is fixed):** login/sign-up UI ∥ server enforcement + RLS ∥ reset/verification email flow.

## Domain gates
- A negative test per protected surface: unauthenticated → 401/redirect, wrong user → 403/404, wrong tenant → 403/404,
  expired or tampered token → rejected.
- Server Actions, API routes, background jobs and webhooks each check identity themselves; webhooks verify the
  provider signature on the raw body instead of a user session.
- Login, sign-up, reset and MFA endpoints are rate-limited; error messages do not reveal whether an account exists.
- Logout and password change invalidate server-side sessions/refresh tokens; account deletion revokes sessions.
- No token, password, reset link or session ID in logs, URLs or analytics.
- No signing secret or service key in the client bundle (grep the built output).

## Ship-readiness (unique)
Evidence checklist before handoff: `references/ship-readiness.md`.

## Safety, approval and honesty
- Approval / safety: creating provider apps, OAuth clients, production keys or sending real emails/SMS needs the owner.
- Approval / safety: never print, read back or log a secret; test credentials are placeholders in `.env.example`.
- Honest failure: never claim "secure" or "auth enforced" without the negative tests; say which were not run.
- Untrusted content: see `references/untrusted-content.md`.
- Shared gates for every playbook (honesty, owner approval, secrets, reviews): `.claude/docs/forge-reference/playbook-template.md`.

## References
- `references/auth-checklist.md` — full hard rules and review checklist.
- `references/sessions-and-jwt.md` — sessions, JWT verification, cookies, CSRF, refresh rotation, logout.
- `references/oauth-oidc.md` — authorization code + PKCE, state/nonce, redirect URIs, account linking.
- `references/passwords-and-recovery.md` — hashing, password policy, reset, verification, MFA, passkeys, rate limits.
- `references/rbac-and-tenancy.md` — RBAC/permissions/ownership, tenancy, admin and impersonation.
- `references/supabase-auth.md` — Supabase Auth specifics.
- `references/providers.md` — Clerk, Auth.js, Better Auth pitfalls.
- `references/team-and-tools.md` — roster, skills, commands, MCP.
- `references/ship-readiness.md` — evidence checklist.
- `references/untrusted-content.md` — untrusted-content note.
