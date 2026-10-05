---
name: secure-auth
description: Implement authentication securely — authentication vs authorization, password hashing (argon2id/bcrypt), sessions vs JWT (storage, expiry, refresh, revocation), MFA, OAuth2/OIDC flows, and defenses against credential stuffing, session fixation, and CSRF. Worked examples + a runnable password-policy check.
type: skill
version: 2.0.0
updated: 2026-06-29
---
# Secure Authentication

Authentication is the front door to your system, and it is the single control attackers probe hardest.
The goal of this skill is **not** to teach you to invent a clever scheme — it is to help you assemble
well-understood primitives correctly, because almost every real-world breach in this area comes from a
broken assembly of good parts, not from cracked cryptography. Heavy detail lives in `references/`;
copy-paste material in `examples/`; a runnable policy check in `scripts/`.

## Mental model

Three distinct questions get muddled constantly. Keep them separate:

| Question | Concern | Wrong answer looks like |
|---|---|---|
| Who are you? | **Authentication** (login, password, MFA) | trusting a client-supplied `user_id` |
| What may you do? | **Authorization** (roles, ownership, scopes) | checking auth but not ownership (IDOR) |
| How do we remember you? | **Session management** (cookies/tokens) | long-lived tokens you can't revoke |

A request can be perfectly *authenticated* and still be an attack if you skip *authorization*. The most
common API vulnerability — Broken Object Level Authorization — is exactly this: a logged-in user reads
`/accounts/124` when they only own `124`'s neighbor. Always check ownership server-side, never trust an
identifier the client could change.

## 1. Password storage: slow hash, never plaintext

The non-negotiable rule: **never store a recoverable password.** Store a one-way hash produced by a
*deliberately slow* algorithm so that a stolen database is expensive to crack offline.

```ts
import argon2 from 'argon2';

// Registration / password change — argon2id is the current default recommendation.
const hash = await argon2.hash(password, { type: argon2.argon2id });
// Store `hash` (it embeds the salt + cost params). NEVER store `password`.

// Login — constant-time verify; argon2 reads cost params from the stored hash.
const ok = await argon2.verify(hash, attempt);
```

Use **argon2id** (preferred) or **bcrypt** (battle-tested, fine if argon2 isn't available). Never use
fast general-purpose hashes (`MD5`, `SHA-256`) — a GPU computes billions of those per second, so a leak
becomes a mass account takeover within hours. Always salt (argon2/bcrypt do this for you), and validate
the password against a policy and a breached-password list *before* hashing — run
`scripts/check-password-policy.mjs --selftest` to see the kind of check that belongs at this boundary.
The full parameter-tuning guidance is in [references/password-hashing.md](references/password-hashing.md).

## 2. Sessions vs JWT: how you remember a logged-in user

Two dominant models, with a real trade-off around **revocation**:

- **Server-side sessions** — a random opaque session ID in an `HttpOnly; Secure; SameSite` cookie; state
  lives server-side (DB/Redis). Revocation is trivial: delete the row. This is the safe default for
  classic web apps.
- **Stateless JWTs** — a signed token the client carries. Scales without shared session storage, but you
  **cannot un-issue a signed token** before it expires. Mitigate with short-lived access tokens
  (5–15 min) plus a revocable, rotating refresh token kept server-side.

```http
Set-Cookie: session=9f2c...; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=3600
```

Storage matters enormously: a token in `localStorage` is readable by any XSS payload, so prefer
`HttpOnly` cookies (which JavaScript cannot read) over web storage for anything that authenticates a
request. The complete comparison — expiry, refresh rotation, reuse detection, and revocation strategies —
is in [references/sessions-vs-jwt.md](references/sessions-vs-jwt.md).

## 3. MFA and step-up

A password alone is a single point of failure against phishing and credential stuffing. Offer a second
factor and require it for sensitive actions (password change, payouts):

- **TOTP** (authenticator app) — good baseline, phishable but cheap.
- **WebAuthn / passkeys** — phishing-resistant, hardware-backed; prefer where you can.
- **SMS** — weakest (SIM-swap), use only as a fallback.

Treat MFA as *step-up*: don't force it on every request, escalate it when risk rises.

## 4. OAuth2 / OIDC: delegated auth done right

When you offload login to a provider (Google, an identity platform), use **OAuth2 Authorization Code
flow with PKCE** for web and mobile/SPA clients. Do not use the implicit flow (deprecated) and never the
resource-owner password flow for third-party login. OIDC layers an identity `id_token` on top of OAuth2's
access token. Validate the `id_token` signature, `iss`, `aud`, and `exp`, and use the `state` parameter to
defend against CSRF on the callback. See [references/oauth2-oidc.md](references/oauth2-oidc.md) for the
full flow diagrams and validation checklist, and `examples/auth-flow.md` for an annotated walk-through.

## 5. Account recovery

Recovery flows are a favorite bypass — they are authentication's back door. Make reset tokens
**single-use, time-limited (e.g. 15–30 min), and high-entropy**, store only their hash, and invalidate
all active sessions on a successful reset. Critically, return the **same response** whether or not the
email exists, and keep timing uniform, so the endpoint can't be used to enumerate accounts.

## Common pitfalls (failure modes)

- **Fast/unsalted hashes** (`SHA-256`, `MD5`) — instantly crackable at scale after a DB leak.
- **JWT you can't revoke** — a long-lived access token stays valid after logout/compromise; keep them short.
- **Tokens in `localStorage`** — any XSS exfiltrates them; use `HttpOnly` cookies.
- **Session fixation** — not rotating the session ID on login lets an attacker pre-seed a known ID; always
  regenerate the session identifier at the moment privilege changes.
- **Missing CSRF protection** on cookie-authenticated state-changing requests — use `SameSite` cookies
  plus anti-CSRF tokens. See [references/auth-attacks.md](references/auth-attacks.md).
- **Account enumeration** — different responses/timing for "wrong password" vs "no such user."
- **No rate limiting / lockout** — credential stuffing walks straight in; throttle and add MFA.
- **Authn without authz** — checking *who* but not *whether they own this object* (IDOR/BOLA).

## When NOT to roll your own / trade-offs

Prefer a vetted identity provider or library over hand-built auth whenever you can. Building it yourself
means owning password reset, MFA enrollment, session revocation, breach monitoring, and audit trails
*forever*. Reach for a managed IdP (OIDC provider, an auth platform) when you want SSO, social login, or
compliance offload; the cost is vendor lock-in and per-MAU pricing. Build in-house only when you have
hard data-residency constraints or genuinely unusual requirements — and even then, wrap proven libraries
(argon2, a maintained OAuth2 client) rather than primitives. Stateless JWT trades easy revocation for
horizontal scale; if you rarely need to scale auth across regions, server-side sessions are simpler and
safer.

## Files in this package

- `references/password-hashing.md` — argon2id vs bcrypt, cost tuning, pepper, rehash-on-login
- `references/sessions-vs-jwt.md` — cookies vs tokens, expiry, refresh rotation, revocation
- `references/oauth2-oidc.md` — Authorization Code + PKCE, token validation, OIDC claims
- `references/auth-attacks.md` — credential stuffing, session fixation, CSRF, enumeration + defenses
- `examples/jwt-verify.ts` — dependency-light JWT verification with the right checks
- `examples/auth-flow.md` — annotated login + refresh + OAuth2 callback walk-through
- `scripts/check-password-policy.mjs` — runnable policy check (length, classes, breached list); `--selftest`

Pairs with `owasp-top10`, `secrets-management`, `rest-api-design`, `audit-logging`, and `gdpr-compliance`.
