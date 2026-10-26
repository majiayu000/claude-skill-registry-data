---
name: nextjs-security
description: Use when writing or reviewing any Next.js server code — Route Handlers, Server Actions, middleware, auth, cookies, env vars, headers. Enforces the project's Next.js security checklist.
---

# Next.js Security

## Auth & sessions

- Store session tokens in `httpOnly` + `Secure` + `SameSite=Lax` cookies, set via
  `cookies()` from `next/headers`. Never store session tokens in `localStorage`.
- Session timeout ≤ 24h; rotate the session token on any privilege change (login,
  role change, password reset).

## Authorization

- Re-verify auth **inside every** Route Handler / Server Action, not just in
  middleware. Return `401` when there is no session, `403` on a role mismatch.
- Middleware is edge routing, **not** a security boundary. Protect admin/privileged
  routes both in middleware *and* in the handler itself.

## CVE-2025-29927 (middleware bypass)

- Patch floor: Next.js **≥ 15.2.3**. The vulnerability lets an attacker set the
  `x-middleware-subrequest` header to skip middleware entirely.
- This repo currently pins `^15.1.0` — **below the floor**. Flag this whenever
  touching `next.config.ts`, `middleware.ts`, or the `next` dependency, and treat
  bumping to ≥ 15.2.3 as a blocking security task, not a nice-to-have.

## Input validation

- Validate all `formData` / request bodies server-side with Zod `.safeParse` (or
  equivalent) before acting on them. Client-side validation is UX only — never
  trust it as the security control.

## Headers in `next.config.ts`

Set security headers centrally:

- **CSP:** `default-src 'self'`, with a scoped `script-src` / `connect-src`
  (avoid `unsafe-inline`/`unsafe-eval` where possible) and `frame-ancestors 'none'`.
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy` — deny camera/microphone/geolocation unless explicitly needed.
- `Strict-Transport-Security` (HSTS) in production.

## Other hard rules

- Never put secrets in `NEXT_PUBLIC_*` env vars — anything with that prefix ships
  to the browser bundle. Keep `.env*` files out of version control.
- Rate-limit login, OTP, and password-reset endpoints.
- Sanitize or avoid `dangerouslySetInnerHTML`; if unavoidable, sanitize with
  `isomorphic-dompurify`.
- Validate any post-login `returnTo`/redirect URL is a relative, same-origin path
  — never redirect to an unvalidated absolute URL (open-redirect risk).
- Run `pnpm audit` periodically and address high/critical findings.

---
Source: authgear.com/post/nextjs-security-best-practices
