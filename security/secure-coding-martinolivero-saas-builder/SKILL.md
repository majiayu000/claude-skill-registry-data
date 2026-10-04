---
name: secure-coding
description: This skill should be used while WRITING any backend, API, auth, or data-handling code for a web app or SaaS — to prevent vulnerabilities before they ship, not to audit them after. Trigger phrases include "add an endpoint", "handle user input", "store user data", "is this secure", "build the API", "save to the database", "handle the form", "user uploads", "process payment", "handle secrets", "set up CORS", "rate limit". It applies OWASP Top 10 prevention, input validation, secrets hygiene, and GDPR basics as you build.
---

# Secure Coding

This skill keeps you from introducing vulnerabilities while you build. It is **prevention, not audit** — it runs at the moment you write an endpoint, a form handler, or a database write, and bakes in the safe default before the bug exists.

Analogy: it is the seatbelt you put on before driving, not the crash investigator who shows up afterward. Audit tools (Trail of Bits, Semgrep, CodeQL) inspect the wreck. This skill stops the crash.

## Scope

This skill is for the solo dev or small team who has **no security tooling installed** and just wants to ship without leaving holes. If a dedicated audit plugin is present, this skill still runs first — preventing a vuln is always cheaper than finding it later.

## Trigger

Activate whenever code touches: a request handler/endpoint, user input, a database write, authentication, file uploads, secrets/env vars, CORS, or any third-party webhook. Default-deny mindset: code with no explicit security decision is the bug.

## Discovery (max 3 questions, only if unknown)

1. Is this endpoint/data public, authenticated, or admin-only?
2. Does it touch personal data (email, name, payment, location, anything identifying a person)?
3. What is the backend — serverless functions (Vercel), a Node server, or a BaaS (Supabase/InsForge)?

## The OWASP Top 10, as prevention rules

Apply the matching rule the instant you write the code. Each maps an OWASP 2021 category to a concrete default.

| Risk | Prevent it by |
| --- | --- |
| **A01 Broken Access Control** | Check authorization on the **server, on every endpoint**. Verify the resource belongs to `req.user` (stop IDOR). Default-deny: no explicit check = bug. Never trust client-sent role/price/owner fields. |
| **A02 Cryptographic Failures** | HTTPS everywhere (free on Vercel). Hash passwords with **bcrypt or argon2**, never plaintext/reversible. Encrypt PII at rest. Never roll your own crypto. |
| **A03 Injection** | **Never string-concat SQL.** Parameterized queries / ORM only (pg params, Drizzle, Prisma, Kysely). Validate every input at the boundary with **zod** before it reaches logic or the DB. |
| **A04 Insecure Design** | Threat-model the feature first: who can call this, what is the worst input. Enforce limits by design — quotas, server-side amount/price checks. |
| **A05 Security Misconfiguration** | Add **Helmet** for secure headers. CORS = explicit origin allowlist (never `*` with `credentials: true`). Disable verbose error stacks in prod. |
| **A06 Vulnerable Components** | Pin deps, run `npm audit` + Dependabot, remove unused packages, update before shipping. |
| **A07 Auth Failures** | Use a vetted auth provider (see the `auth` skill). Rate-limit login routes harder. httpOnly + Secure + SameSite cookies for sessions. MFA where possible. |
| **A08 Data Integrity** | Verify webhook signatures (e.g. Stripe signing secret). Don't deserialize untrusted data. Commit the lockfile. |
| **A09 Logging Failures** | Log auth + authz denials — but **never log PII, tokens, passwords, or full request bodies**. Redact first. |
| **A10 SSRF** | Don't fetch user-supplied URLs server-side without an allowlist; block internal/metadata IP ranges. |

## API security defaults

- **Validate at the boundary with `zod`**, and use `.strict()` schemas that whitelist exactly the allowed fields. This kills **mass assignment** — never spread `req.body` into a DB write; explicitly drop `role`, `isAdmin`, `id`, `ownerId`.
- **Rate-limit** every public and auth endpoint (`express-rate-limit`, or the platform's edge limiter). Auth routes get a stricter limit.
- **CORS**: allowlist origins explicitly. With credentials, `*` is forbidden by spec and a real hole.
- Return correct status codes — `401` vs `403`, `422` on validation, `429 + Retry-After` on limit.

## User data & GDPR basics (for developers)

- **Collect the minimum PII.** Drop optional fields. Less data = less liability (GDPR Art. 5 minimization).
- **Encrypt in transit (TLS) and at rest.** GDPR Art. 32 cites encryption as the recommended safeguard.
- **Set retention + deletion.** Provide a way to delete a user's data on request.
- **Never log PII.** Redact emails, tokens, bodies before they hit logs or Sentry.

## Secrets hygiene

- `.gitignore` `.env`, `.env*.local`, `*.pem`, `*.key`. Commit a `.env.example` with names only.
- Secrets live in the platform's encrypted store (Vercel env vars marked **Sensitive**), never in the repo.
- On Vite, only `VITE_`-prefixed vars reach the browser — a secret behind that prefix is a public leak.
- Rotate by **add-new → redeploy → revoke-old**. Optionally run **gitleaks** as a pre-commit net.

## Output

For each piece of code, deliver: the secure implementation, a one-line note on which risk it defends against, and any validation schema (`zod`) inline. When you spot a violation in existing code the user shows you, flag it with the fix — but the job is to write it safe the first time.

## Reference

OWASP Cheat Sheet Series (~29k⭐), OWASP Top 10:2021, GDPR.eu / gdpr-info Art. 32. Tools: `zod`, `helmet`, `express-rate-limit`, `bcrypt`/`argon2`, `gitleaks`.
