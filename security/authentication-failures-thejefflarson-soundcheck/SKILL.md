---
name: authentication-failures
description: Detects weak password storage, flawed JWT validation, sessions surviving
  logout, and missing MFA in authentication code. Use when writing login
  flows, session management, password storage, JWT handling, MFA
  implementation, credential validation, or any code that authenticates users.
  Also invoke when implementing "remember me" functionality or API key
  management.
---

# Authentication Failures Security Check (A07:2025)

## What this checks

Protects identity and session integrity. Weak password storage, flawed JWT handling,
and sessions that survive logout let attackers impersonate users, escalate privileges,
and persist after credential rotation.

## Vulnerable patterns

- JWT verification call with a weak, short, or hardcoded signing secret
- JWT decode that disables signature verification or accepts the `none` algorithm
- Logout handler that does not invalidate the session or token server-side
- Login flow with no rate limiting or account lockout, allowing credential stuffing
- Password or API-key comparison using a non-constant-time equality operator

For password hashing issues (MD5/SHA), see `cryptographic-failures`.
For hardcoded API keys/passwords in source, see `hardcoded-secrets`.

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties:

1. **Signing keys come from outside the source tree** — environment variable, secret
   manager, or KMS. Enforce a minimum length or entropy check at load time so a
   misconfigured deploy fails loudly rather than silently using a tiny secret.
2. **JWT verification pins the accepted algorithm(s) to an explicit allowlist**
   that rejects `none` and rejects algorithm switching between symmetric and
   asymmetric families (the classic HS256-vs-RS256 public-key-as-HMAC attack).
   The check must be algorithm-specific, however the library expresses it.
3. **Logout invalidates credentials server-side.** Either delete a server session
   record, add the token to a revocation list, or rotate a per-user signing key.
   Short token expiry alone does not satisfy this — a stolen token works until
   it expires. The code must demonstrate an active revocation mechanism.
4. **Password and API-key comparisons are constant-time** — use the language's
   documented constant-time comparison primitive, never a plain equality operator.
5. **Login has a rate limit or lockout.** Credential stuffing is cheap; unbounded
   guess rates make every leaked password list a working brute-force dictionary.

Translate these principles to the audited file's language and framework. Use the
documented authentication and crypto APIs for that stack; do not roll your own.

## Verification

Confirm these properties hold (language-agnostic):

- [ ] JWT signing/verification keys are sourced from outside the source tree (environment variable, secret manager, KMS) AND the code enforces a minimum length/entropy check at load time — a comment asserting "must be ≥32 bytes" without a runtime check does not satisfy this
- [ ] JWT verification pins the accepted algorithm(s) to an explicit allowlist that rejects `none` and rejects algorithm switching between symmetric and asymmetric families — whether expressed as a `algorithms=[...]` parameter, a `.withAlgorithm(...)` builder call, a `Validation::new(Algorithm::HS256)` constructor, or equivalent
- [ ] A logout / session termination path exists that invalidates credentials server-side — either by deleting a server session record, adding the token to a revocation list (DB, Redis, in-memory set), or rotating a per-user signing key. Short token expiry alone does not satisfy this; the code must demonstrate an active revocation mechanism

## References

- CWE-287 ([Improper Authentication](https://cwe.mitre.org/data/definitions/287.html))
- CWE-307 ([Improper Restriction of Excessive Authentication Attempts](https://cwe.mitre.org/data/definitions/307.html))
- [OWASP A07:2025 – Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
