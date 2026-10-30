---
name: insecure-design
description: Detects missing security controls — rate limits, MFA, re-auth — that should
  have been designed in from the start. Use when designing authentication
  flows, implementing rate limiting, building business logic for financial or
  access-sensitive operations, or writing code that enforces security
  requirements at the application layer.
---

# Insecure Design Security Check (A06:2025)

## What this checks

Catches security controls that were never designed in. Missing rate limiting,
skippable workflow steps, and unenforced re-authentication enable account takeover,
fraud, and privilege escalation.

## Vulnerable patterns

- Credential-accepting endpoint (login, password reset, MFA verify) with no rate limit or lockout
- Multi-step workflow that advances based on a client-supplied step name or boolean rather than server-side state
- Authentication failure response that distinguishes "user not found" from "wrong password" via message text, status code, or timing
- Sensitive state change (email change, fund transfer, account deletion) protected only by session existence — no re-auth or step-up challenge
- Security-relevant decision (lockout status, role, authorization level) read from a request parameter, cookie, or header the client can freely modify

## Fix immediately

Flag the vulnerable code and explain the risk. Translate the principles below to the
audited file's language, web framework, and rate-limiter or session library — use that
stack's documented middleware rather than rolling your own.

For each finding, establish these properties:

1. **Every credential-accepting endpoint has a rate limit or lockout keyed on a
   caller-controlled identifier** (IP, username, email, or account id). Apply to
   *every* such endpoint — login, password reset, MFA verify, token exchange,
   re-auth — not just login. Unlimited retries are never acceptable.
2. **Authentication failure responses do not distinguish "user not found" from
   "wrong password"** — same message, same status code, same timing. Always
   compute the password hash even when the user is missing (compare against a
   dummy hash to equalize latency); short-circuit branches leak account existence.
3. **Sensitive state changes (password change, email change, fund transfer, account
   deletion, permission grant) require a check stronger than "session exists"** —
   re-prompt for the current password, verify a step-up token, or require MFA.
4. **Multi-step workflows read the current step from server-side state** —
   session, database, or a signed token — never from a client-supplied parameter.
   The server owns the progression.
5. **No security-relevant decision (lockout status, step progression,
   authorization level) is read from request parameters, cookies, or headers that
   the client can freely modify.**

## Verification

Confirm these properties hold for every endpoint present (language-agnostic;
criteria apply only to patterns actually present):

- [ ] Every credential-accepting endpoint present (login, password reset, MFA verify, token exchange) is gated by at least one rate-limiting or lockout mechanism keyed on a caller-controlled identifier (IP, username, email, or account id) — unlimited retries are not permitted
- [ ] Authentication failure responses do not distinguish "user not found" from "wrong password" via message text, status code, or response timing
- [ ] Any sensitive state-change operation present in the code (password change, email change, fund transfer, account deletion, permission grant) performs an authorization check stronger than "session exists" — e.g., re-prompts for the current password, verifies a step-up token, or requires an MFA challenge
- [ ] Multi-step workflows present in the code determine the current step from server-side state (session, database, signed token), not from a client-supplied step name, token, or boolean
- [ ] No security-relevant decision (lockout status, step progression, authorization level) is read from request parameters, cookies, or headers that the client can freely modify

## References

- CWE-657 ([Violation of Secure Design Principles](https://cwe.mitre.org/data/definitions/657.html))
- CWE-840 ([Business Logic Errors](https://cwe.mitre.org/data/definitions/840.html))
- [OWASP A06:2025 – Insecure Design](https://owasp.org/Top10/A06_2021-Insecure_Design/)
