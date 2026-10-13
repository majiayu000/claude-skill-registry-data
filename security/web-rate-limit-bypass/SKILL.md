---
name: web-rate-limit-bypass
description: >
  Bypass rate limits and anti-automation to enable brute force, OTP guessing, coupon abuse, and
  enumeration. Load when an endpoint is throttled (429/"too many attempts"), on login/OTP/reset,
  or "rate limit". Signals: 429 responses, lockout messages, per-account throttling, OTP/2FA.
domain: web
type: technique
stability: learning
modes: [bugbounty]
severity: medium
owasp_api: [API4:2023-Unrestricted-Resource-Consumption]
cwe: [CWE-307, CWE-799]
tools: [burp, ffuf]
schema_version: 1
---

# Rate-limit bypass

## When it applies
An endpoint limits attempts (login, OTP/2FA, password reset, coupon, search) and you need more
attempts than allowed — to brute force, guess a code, or enumerate. The limit is the only control
standing between you and the bug.

## Why it works
Rate limits are enforced on a key the attacker can often change or spoof: an IP header, a session,
an account id, or a per-endpoint counter. If the key is attacker-controlled or the limit is
inconsistent across paths/casing, you reset or dodge the counter.

## Method
1. **Find the key**: is the limit per-IP, per-account, per-session, or global? Change it:
   - **IP spoof headers**: `X-Forwarded-For`, `X-Real-IP`, `X-Client-IP`, `X-Originating-IP` —
     rotate values per request; many WAFs/apps trust these.
   - **Session/token**: rotate cookies/CSRF tokens; unauthenticated vs authenticated paths.
2. **Path/param tricks**: case (`/Login`), trailing `/`, added query params, HTTP/2 multiplexing,
   or a different endpoint that hits the same backend without the limit.
3. **Race the window**: fire a burst in parallel before the counter updates (→ `web-race-conditions`),
   e.g. many OTP guesses at once.
4. **Automate** with Burp Intruder / `ffuf`, injecting a rotating `X-Forwarded-For` per request.

## Gotchas
- Confirm attempts actually go through (watch for silent drops that return 200 but don't count).
- OTP brute needs the code space small enough (4–6 digits) and no per-account lockout — check both.
- Respect program RoE — brute force is noisy; throttle and stop once the bypass is proven.

## Verify success
Attempts continue past the documented limit (no 429), demonstrated by a successful brute/OTP guess
or sustained enumeration that the limit should have blocked.

## References
OWASP API Security (API4); PortSwigger auth/OTP labs; OWASP WSTG anti-automation.
