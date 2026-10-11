---
name: gotrue
description: GoTrue auth — user management, JWT, refresh tokens, custom claims.
---

# GoTrue

GoTrue is a stateless authentication microservice. It issues JWTs, manages user sessions, and handles OAuth flows. Supabase embeds it as the `auth` service; it can also run standalone.

---

## Detection Signals

Load this skill when any of the following are present:

| Signal | Location |
|---|---|
| `GOTRUE_*` env vars | `.env`, `.env.example`, deploy config |
| `SUPABASE_JWT_SECRET`, `SUPABASE_SERVICE_ROLE_KEY` | `.env`, `.env.example` |
| `@supabase/supabase-js`, `@supabase/auth-js`, `@supabase/ssr` | `package.json` |
| `supabase.auth.*` calls | application source |
| `[auth]` or `[auth.hook.*]` section | `supabase/config.toml` |
| `auth.users` table or `auth` schema | database schema / migrations |
| `supabase/auth` or `gotrue` image | `docker-compose.yml` |

---

## Auth Methods

| Method | API call (supabase-js) |
|---|---|
| Email + password | `supabase.auth.signInWithPassword({ email, password })` |
| Magic link | `supabase.auth.signInWithOtp({ email })` |
| Phone OTP | `supabase.auth.signInWithOtp({ phone })` |
| OAuth (Google, GitHub, etc.) | `supabase.auth.signInWithOAuth({ provider: 'google' })` |
| Anonymous | `supabase.auth.signInAnonymously()` |
| SSO / SAML | `supabase.auth.signInWithSSO({ domain })` |

---

## Core Rules

These decide the shape of the work. Code-level detail lives in the references below.

| Area | Rule |
|---|---|
| Authorization source | Read roles and permissions from `app_metadata` only — it is server-controlled |
| `user_metadata` | User-writable. Never an authorization input, under any circumstance |
| Server-side trust | `getSession()` does not verify — always follow with `getUser()` before trusting an identity on the server |
| Service-role key | Server-side only. Reaching it from client code grants full auth admin access |
| Token lifetime | Access tokens are short-lived (1h default); the client must handle refresh via `onAuthStateChange` |
| Claim changes | Custom claims are frozen into an issued JWT — a role change only applies after a token refresh |
| Environment parity | Confirm email-confirmation and expiry settings match between environments; GoTrue defaults differ |

---

## References

| File | Load when |
|---|---|
| `references/client-and-admin-api.md` | Implementing sign-in, sessions, refresh, the Admin API, or server-side JWT verification |
| `references/claims-and-hooks.md` | Adding custom claims, writing RLS against them, or configuring GoTrue hooks |

---

## Common Pitfalls

- Reading `user_metadata` for authorization — users control it, never trust it for permissions
- Not calling `onAuthStateChange` on the client — sessions expire silently
- Using `getSession()` on the server without re-verification — the session in the cookie may be stale; always call `getUser()` to verify server-side
- Exposing the service-role key in client code — gives full auth admin access
- Not enabling email confirmations in production — GoTrue defaults may differ between environments
- Assuming a revoked role takes effect immediately — the old JWT stays valid until it expires or is refreshed
