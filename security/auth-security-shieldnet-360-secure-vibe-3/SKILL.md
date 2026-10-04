---
id: auth-security
version: "1.1.0"
title: "Authentication & Authorization Security"
description: "Authentication and authorization: JWT, OAuth 2.0 / OIDC, session management, CSRF, password hashing, MFA, and object-level / function-level authorization (BOLA, IDOR) — confirming the caller may access the specific resource they asked for. Use when generating login, signup, or password-reset flows, issuing or verifying JWTs, writing OAuth or OIDC code, wiring session cookies or MFA, or writing any endpoint that reads or writes a resource by id."
category: prevention
severity: critical
applies_to:
  - "when generating login / signup / password-reset flows"
  - "when generating JWT issuance or verification"
  - "when generating OAuth 2.0 / OIDC client or server code"
  - "when wiring session cookies, CSRF tokens, MFA"
  - "when writing an endpoint that reads or writes a resource by id"
  - "when adding a role, permission, or ownership check"
languages: ["*"]
token_budget:
  minimal: 1500
  compact: 1900
  full: 3300
rules_path: "rules/"
related_skills: ["api-security", "crypto-misuse", "error-handling-security", "frontend-security", "secret-detection"]
last_updated: "2026-08-12"
sources:
  - "OWASP Authentication Cheat Sheet"
  - "OWASP Session Management Cheat Sheet"
  - "RFC 6749 — OAuth 2.0"
  - "RFC 7519 — JSON Web Token"
  - "RFC 9700 — OAuth 2.0 Security BCP"
  - "NIST SP 800-63B (Authenticator Assurance)"
---

# Authentication & Authorization Security

## Rules (for AI agents)

### ALWAYS
- Authorize at the **object level** — confirm the authenticated subject actually has
  access to the requested resource ID, not just that they are logged in. Being signed
  in is not permission to read record 4,182 (OWASP API1 — BOLA / IDOR).
- Bind object-level authorization to the **authenticated principal**, never to an
  actor id echoed in the request: checking that a request-supplied
  `senderId`/`ownerId`/`actedBy` is a valid member validates the *claimed* actor, not
  the caller (looks like authorization, isn't).
- On `/{scopeId}/.../{subjectId}` routes, authorize the **relationship** — confirm the
  subject belongs to that scope. A caller-vs-scope check alone does not authorize the
  subject (multi-key BOLA).
- Authorize **each subject on streaming responses** (SSE/chunked/WebSocket): the `200`
  is committed before the handler runs, so an empty/filtered stream — not a `4xx` — is
  the deny signal; an unauthorized subject gets zero events.
- Enforce a **function-level role / privilege check** on any write that publishes into
  a shared or global namespace (a global gallery, shared catalog, public template
  list). Authentication is not authorization (OWASP API5 — Broken Function Level
  Authorization); a low-privilege user posting into a globally-visible store is a
  delivery vector for stored-XSS and malicious-link chains.
- For JWT verification, pin the expected algorithm (`RS256`, `EdDSA`, or `ES256`)
  and verify `iss`, `aud`, `exp`, `nbf`, and `iat`. Reject `alg=none` and any
  unexpected algorithm.
- For OAuth 2.0 public clients (SPA / mobile / CLI), use the **authorization
  code flow with PKCE** (S256). Never the implicit flow. Never the resource
  owner password credentials grant.
- Cookies for sessions: `Secure; HttpOnly; SameSite=Lax` (or `Strict` for
  sensitive flows). Use the `__Host-` prefix when there's no subdomain sharing.
- Rotate the session identifier on login and on privilege change. Bind the
  session to the user agent only as a soft signal — never as the sole check.
- Consult `crypto-misuse` for every cryptographic primitive this flow touches —
  the password KDF and its work factors, the RNG behind session IDs and reset
  tokens, and constant-time comparison. It names the correct call per language,
  which is the half a "do not use X" rule leaves out.
- Make both authentication failure paths cost the same. Do not return early when the
  account does not exist: run an equivalent KDF verification — against a fixed dummy
  hash held for the purpose — before returning the same failure the wrong-password
  path returns. Matching the message alone still discloses which accounts exist,
  because the not-found branch skips the expensive work and answers sooner. Aim for a
  comparable processing path, not a constant wall-clock time, which HTTP cannot
  deliver. `error-handling-security` owns what that response says.
- Consult `frontend-security` for where a token may live in the browser. Its rule
  covers **every** JWT and token, not just long-lived refresh ones — any XSS reads
  `localStorage` — and pairs with the matching `document.cookie` restriction.
- Enforce password length ≥ 12 characters with no composition rules; allow
  Unicode; check candidate passwords against a known-breached list
  (HIBP / pwned-passwords k-anonymity API). The length floor tracks NIST
  SP 800-63B, current as of 2026-06.
- Implement account lockout *or* rate limiting for password attempts. NIST
  SP 800-63B §5.2.2 caps this at 100 failures over 30 days as of the 2026-06
  revision; verify the section still reads that way before citing the number.
- Implement CSRF protection for state-changing requests reachable from a
  browser session: synchronizer token, double-submit cookie, or
  `SameSite=Strict` for high-risk endpoints.
- Require MFA / step-up for administrative operations, password changes,
  MFA-device changes, billing changes.
- For OIDC, validate the `nonce` you sent against the `nonce` in the ID token;
  validate the `at_hash` / `c_hash` when present.

### NEVER
- Accept JWT `alg=none`; or accept HS256 from a client when the issuer signs
  with RS256 (classic algorithm-confusion attack).
- Put access tokens, refresh tokens, or session IDs in URL query strings —
  they leak to logs, Referer headers, and browser history.
- Trust client-supplied roles / claims at the API layer — re-derive the
  authenticated subject and look up server-side authorization on each request.
- Act on a subject/owner id asserted by an upstream **producer** (queue, topic,
  webhook) without authenticating the channel and re-validating the asserted
  subject — a spoofed producer otherwise drives forged cross-tenant effects.
- Issue long-lived (>1 hour) access tokens; rely on refresh tokens with
  rotation.
- Use the implicit flow or the password grant.

### KNOWN FALSE POSITIVES
- A write into the caller's **own** private / tenant-scoped namespace needs only
  authentication plus object-level ownership — function-level role gating applies
  specifically to writes whose result becomes visible beyond the creator.
- Service-to-service tokens with long TTLs are sometimes acceptable when stored
  in a secret manager and bound to a specific workload identity.
- Local-development "magic link" auth without password hashing for ephemeral
  dev users is fine if it's gated behind an env flag and disabled in prod.
- Tokens in URL query are tolerable in *one* place — the OAuth authorization
  code return — because the value is short-lived and one-time-use.

## Context (for humans)

Authentication failures show up consistently in OWASP Top 10 (A07:2021 —
Identification and Authentication Failures). The common modes are: weak
password storage, predictable tokens, missing MFA, JWT misconfiguration, and
session fixation. RFC 9700 (OAuth 2.0 Security BCP) and NIST SP 800-63B are
the authoritative references for the recipe.

AI assistants tend to ship "works in dev" auth: HS256 JWTs with hard-coded
secrets, `bcrypt.hash` with default cost 10, no PKCE, tokens in localStorage.
This skill catches the first two directly and routes the rest to the skill that
owns them — work factors to `crypto-misuse`, browser storage to
`frontend-security`.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `rules/jwt_safe_config.json`
- `rules/oauth_flows.json`
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) — the source of record for work factors; read it, do not recall it.
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html).
- [RFC 9700 — OAuth 2.0 Security BCP](https://datatracker.ietf.org/doc/html/rfc9700).
- [NIST SP 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html).
