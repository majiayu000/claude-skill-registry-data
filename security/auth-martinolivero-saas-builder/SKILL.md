---
name: auth
description: This skill should be used when adding authentication or authorization to an app or SaaS — login, signup, sessions, tokens, roles, permissions, multi-tenant access, SSO, or social login. Trigger phrases include "add login", "add auth", "sign in with Google", "protect this route", "user roles", "admin permissions", "JWT or sessions", "which auth provider", "RBAC", "multi-tenant access", "who can see what", "magic link", "SSO". It picks the right provider and pattern instead of rolling auth from scratch.
---

# Auth

This skill makes the two decisions every SaaS gets wrong: **which auth provider** and **how to model permissions**. It picks a vetted provider over hand-rolled auth, and a permission model that fits the product.

Analogy: auth is the lock and the guest list for your building. You don't forge your own lock (you'd leave it pickable) — you buy a good one and decide who gets which key.

## The one rule

**Don't roll your own auth.** Password hashing, session rotation, OAuth flows, and reset tokens are where subtle, catastrophic bugs live. Use a provider or a battle-tested library. (Pairs with the `secure-coding` skill, which covers the OWASP auth-failure defenses.)

## Discovery (max 3 questions, only if unknown)

1. Is this B2C (individual users) or B2B (organizations/teams with members)?
2. Do you need enterprise SSO (SAML/OIDC) for buyers — now or soon?
3. What's the stack/backend — Supabase, plain Vercel + Postgres, or full-stack TypeScript?

## Step 1 — Pick the provider (decision tree)

| Situation | Use | Why |
| --- | --- | --- |
| Building **with an agent** / on **InsForge** | **InsForge Auth** | Agentic-native — the agent wires auth + RLS through its own skills/MCP; every query scopes to the user in SQL. |
| Already on **Supabase** | **Supabase Auth** | Free, RLS-native — every query scopes to the user in SQL. Most-proven ecosystem. |
| Want the best React DX / drop-in components, not tied to a backend | **Clerk** | Best components, orgs/teams built in. ~$0.02/MAU after a free tier. |
| Full-stack TypeScript, want self-hosted control | **Better Auth** (~28k⭐) | TS-native, framework-agnostic, orgs/RBAC/passkeys/SSO. |
| **Enterprise SSO** is a buyer requirement | **Auth0 / WorkOS** | SAML/OIDC, directory sync, the enterprise checkboxes. |

Default for a fresh React + Vite + Postgres SaaS with no SSO need: **InsForge Auth** if you're building agent-first, **Supabase Auth** if on Supabase, or **Clerk** otherwise. All three scope to the user via RLS — match the auth host to the DB host from the `data-modeling` skill.

## Step 2 — Sessions vs JWT

- **Classic web app → server-side sessions** in an **httpOnly, Secure, SameSite** cookie. Easy revocation, no token-in-JS exposure.
- **Stateless API / mobile / microservices → short-lived JWT access token + refresh token.**
- **Never store JWTs in `localStorage`** (XSS-readable). Cookie or in-memory only.
- Keep authorization out of the JWT body beyond coarse role hints — baked-in roles go stale until expiry and can't be revoked. Check permissions server-side per request.

## Step 3 — Model authorization (RBAC by default)

- **Default to RBAC**: a small set of roles — `owner / admin / member / viewer`. Covers most SaaS.
- **Add ABAC/policy rules** only when access depends on attributes: resource owner, department, plan tier, time. Example: "edit invoice only if `role=manager` AND same `department`."
- **Centralize the check** in one middleware/guard or policy layer. Never scatter `if (role === 'admin')` across handlers — that's how a forgotten check becomes a breach.

## Step 4 — Multi-tenant scoping (B2B)

- Scope **every** authz check by `tenant_id` / `org_id`. A valid user of org A must never read org B.
- Let Postgres **Row-Level Security be the backstop** (see the `data-modeling` skill) so even a missed app-layer check can't leak across tenants.
- Use OAuth/OIDC via the provider for social + SSO logins — never handle raw third-party password flows yourself.

## Delegation & fallback

- **Provider available** → wire it (InsForge/Supabase/Clerk/Better Auth) and configure roles/orgs through it. On InsForge, its `insforge` and `insforge-integrations` skills wire auth — including external providers (Clerk/Auth0/WorkOS) into JWT-based RLS — so the agent sets it up end to end.
- **No provider chosen / offline** → fall back to a well-known library (Better Auth or Lucia), httpOnly cookie sessions, bcrypt/argon2 password hashing, and the RBAC pattern above. Never block on a missing provider.

## Output

Deliver: the provider recommendation with a one-line reason, the session/token decision, a concrete role model for this product, the protected-route guard wired in, and the multi-tenant scoping rule if B2B.

## Reference

InsForge Auth (~5k⭐, agentic-native), Better Auth (~28k⭐), Auth.js/next-auth (~28k⭐), Clerk, Supabase Auth (part of supabase ~104k⭐).
