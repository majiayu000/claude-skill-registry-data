---
name: auth-hardening
description: Apply modern authentication standards instead of historical mistakes. Covers NIST 800-63B-aligned passphrase policy (no rotation theatre), MFA enforcement and factor tiering, session versus JWT tradeoffs, OAuth scope minimization, and account lockout that does not enable enumeration. Invoke when building auth from scratch, planning MFA rollout, or handling a credential-stuffing wave.
---

# Auth Hardening

Authentication is where almost every public-facing app eventually gets attacked. The good news: a small set of patterns covers most of the threat surface, and the worst practices (password rotation every 90 days, "security questions") are actively harmful.

This skill is opinionated. The opinions track NIST SP 800-63B, OWASP ASVS, and industry consensus circa 2026.

## When to invoke

- Building auth from scratch
- Reviewing an existing auth system before scaling user count
- Handling a credential-stuffing wave or a brute-force surge
- Planning MFA rollout for staff or customers
- After a password-reset abuse incident or account-takeover report
- Migrating from sessions to JWT (or back)

## Password policy — what to require, what to drop

**Require**:

- **Minimum length 12 characters**, no maximum below 64. Length beats complexity.
- **Allow all printable characters and spaces** — including emoji and unicode. Reject only NULL bytes.
- **Check against breached-password lists** at signup and reset. Use Have I Been Pwned's k-anonymity range API (only first 5 chars of hash leave your server).

**Drop**:

- **No mandatory rotation.** NIST 800-63B explicitly removed periodic rotation in 2017 because it produces predictable patterns (`Password1!` → `Password2!`).
- **No composition rules** ("must contain a symbol"). They reduce entropy by making patterns predictable.
- **No security questions.** Mother's maiden name is on LinkedIn. Pet's name is on Instagram.
- **No password hints stored anywhere users have ever seen them.**

Rotation IS appropriate after: known compromise of the credential, MFA enrollment lapse, or staff offboarding.

## Password storage

- **Argon2id** is the recommended default (memory-hard, side-channel resistant). Tune memory ≥ 64 MB, parallelism 1, iterations to hit ~250–500ms per hash on your hardware.
- **bcrypt** still acceptable (cost ≥ 12) — most languages have mature libraries.
- **scrypt** acceptable but less ergonomic than Argon2.
- **Never roll your own.** Even SHA-256 + salt is wrong here — too fast, GPU-friendly.

```ts
// Node example with argon2 package
import argon2 from 'argon2';

const hash = await argon2.hash(password, {
  type: argon2.argon2id,
  memoryCost: 65536,    // 64 MB
  timeCost: 3,
  parallelism: 1,
});

const ok = await argon2.verify(hash, candidate);
```

Re-hash on login when parameters change (you'll bump cost as hardware improves). Take the hit during the user's session, not in a batch job.

## MFA — when to require, what to accept

**Tier by risk**:

- **Admin / staff** — required, hardware key (WebAuthn) or TOTP only. SMS not acceptable for staff.
- **Customers managing money / sensitive data** — strongly recommended, optionally required. WebAuthn / TOTP. SMS as fallback only.
- **General customers** — optional but well-promoted. Any second factor better than none.

**Recommended factors, in order**:

1. **WebAuthn / passkeys** — phishing-resistant, no shared secret. The right default in 2026.
2. **TOTP via authenticator app** — well-supported, no carrier dependency.
3. **Recovery codes** — single-use, generated at MFA enrollment, must be stored by the user. Avoid recovery via "email a code" alone (that just makes email the actual factor).
4. **SMS / voice** — last resort, susceptible to SIM swap. Note in your threat model.

**Implementation gotchas**:

- Allow multiple second factors per user (so losing one device doesn't lock them out)
- "Trusted device" cookies should expire (30 days max), be revocable from the user's settings, and require re-MFA on sensitive actions
- Never accept the same TOTP code twice in its 30-second window (mark-as-used in cache)

## Session cookies vs JWT

Most apps should use **server-side sessions with HTTP-only cookies**, not JWT.

| | Server sessions (cookie) | JWT (Authorization header) |
|---|---|---|
| Revocation | Trivial — delete the session row | Hard — JWT is self-contained, requires denylist or short TTL + refresh dance |
| Storage | Small cookie + DB / Redis lookup | All claims travel in the token, can bloat to KB |
| Cross-domain | Same-origin or strict CORS | Easier across services / mobile apps |
| Theft impact | Cookie + same domain only (with `SameSite`) | Token usable from anywhere until expiry |

For web apps with a single backend, sessions win. For multi-service / mobile API backends, JWT can pay off if you accept the operational complexity.

**If you use JWT**:

- Sign with **EdDSA / Ed25519** or **RS256**. Avoid HS256 unless you have one signer and one verifier and they can share a secret safely.
- Set short access-token TTL (15 min), longer refresh-token TTL (days/weeks), refresh tokens are opaque random and stored server-side so you can revoke them.
- Validate `iss`, `aud`, `exp`, `nbf` strictly on every request.
- Never let the `alg` header decide. Pin the expected algorithm in your verifier — the `alg: none` family of attacks lives here.

**Cookie attributes (whether sessions or refresh tokens)**:

```
Set-Cookie: sid=...; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=...
```

`SameSite=Strict` is more secure but breaks "login then click email link". `Lax` is the right default. `None` only with explicit need + `Secure`.

## OAuth scope minimization

When integrating "Sign in with Google / GitHub":

- **Request only the scopes you need.** "Sign in" needs email/profile. Asking for `repo` or `gmail.send` for a sign-in flow is a red flag (and users notice).
- **Validate `state` and `nonce`** on every callback. CSRF is real here.
- **Validate the ID token signature** — never just trust the email field. Use the provider's JWKS and the same JWT discipline above.
- **Verify `email_verified: true`** for any flow that auto-links to existing accounts by email.
- **Bind the OAuth identity to your user record** by stable provider-issued `sub` (not email — emails change).

## Account lockout vs enumeration

The naive lockout (`5 failures → lock account 30 min`) creates two problems:

1. **Username enumeration**: attacker probes 100 usernames, sees which ones get locked → those exist.
2. **Self-DoS**: attacker locks your real users' accounts at will.

Modern pattern:

- **Per-IP rate limit** on login (e.g. 10/min). Stops dumb brute-force without locking targeted users.
- **Per-account exponential backoff on bad password** — pauses adding 1s, 2s, 4s, 8s. Cap at 60s. Survives the wave without locking accounts.
- **Generic error message**: "incorrect email or password". Never "no user with that email."
- **CAPTCHA challenge after N failures per IP**, not a lock.
- **Notify the user by email after K failed attempts** ("someone tried to log in") — gives users a chance to respond.
- **Hard lock + manual review** only for clearly automated abuse (e.g. 1000 attempts/hr from one IP).

## Password reset — the highest-leverage takeover vector

Most account takeovers happen through a buggy reset flow, not a password crack.

Patterns:

- **Reset link is single-use, expires in 15–60 min**, invalidated on use OR password change OR another reset issued
- **Token is high-entropy (≥128 bits)**, server-generated, stored hashed in DB (so a DB read doesn't enable resets)
- **Reset email goes only to the email on file** — never accept a new email in the reset request
- **After successful reset, invalidate all existing sessions** for that user
- **Generic response on reset request**: "if an account with that email exists, we sent a reset link". Do not confirm existence.
- **Rate-limit reset requests** per email + per IP (caps spam + enumeration via timing)
- **MFA does not bypass on reset.** If the user has MFA enrolled, the reset flow requires MFA too (or a separate recovery code), otherwise reset becomes the MFA bypass.

## Email change flow — also a takeover vector

Less obvious than password reset, but equally important:

- **Verify both addresses** — old and new. Confirmation link to the new address activates it; notification to the old address with a "this wasn't me, revert" link.
- **48-hour grace period** during which the old email can revert the change. Stops attackers who get a session cookie, change the email, then change the password.
- **Require current password** (and MFA if enrolled) to initiate the change.

## Breached credential detection

Have I Been Pwned's [Pwned Passwords API](https://haveibeenpwned.com/Passwords) lets you check candidate passwords without sending them anywhere. K-anonymity range model: hash the password, send the first 5 chars of the SHA-1 hex, receive back ~500 hashes with that prefix, check locally if your full hash matches.

Use it at:

- **Signup** — reject the worst breached passwords
- **Password change** — same
- **Periodic scan of stored hashes** is not possible (they're hashed with a strong scheme — you cannot reverse), so this is a flow-time check

## Audit log

Authentication events deserve their own log stream. Capture, at minimum:

- successful logins (user, timestamp, IP, user-agent, factor used)
- failed logins (same, plus reason: bad password / locked / MFA failed)
- password changes, MFA changes, email changes, OAuth links/unlinks
- session creations, explicit logouts, session revocations

Retention 12 months is a reasonable default. Surface these in a user-facing "recent activity" view — users catch their own compromises faster than you will.

## Quick checklist

For an auth system going to production:

- [ ] Minimum 12-char passwords, no max <64, all characters allowed
- [ ] Breached-password check at signup and change
- [ ] Argon2id (or bcrypt cost ≥12) for storage
- [ ] MFA available; required for admin/staff
- [ ] WebAuthn supported, not just TOTP
- [ ] Recovery codes generated, displayed once
- [ ] HttpOnly + Secure + SameSite cookies
- [ ] Generic error messages, no enumeration
- [ ] Per-IP rate limit + per-account exponential backoff (no naive lockout)
- [ ] Password reset: single-use, short TTL, hashed in DB, invalidates sessions on success
- [ ] Email change: verify both ends, grace period, current-password required
- [ ] Audit log of auth events, user-visible "recent activity"
- [ ] OAuth: minimum scopes, strict state/nonce, ID token verified, `email_verified` checked
- [ ] No security questions, no rotation cadence, no password hints

## What this skill will not do

- Recommend SMS as a primary factor for any staff account
- Endorse "must change password every 90 days" policies
- Help build authentication for systems you do not own
