---
name: web-account-takeover
description: >
  Systematic account-takeover hunting — password reset, email change, session, and linking flaws
  that seize another user's account. Load on "ATO", password-reset/forgot flows, email-change,
  OTP/2FA, "login as", session handling. Signals: reset tokens, email-change without re-auth,
  OTP, magic links.
domain: web
type: technique
stability: learning
modes: [bugbounty]
severity: critical
owasp: [A07:2021-Auth-Failures]
cwe: [CWE-640, CWE-287]
tools: [burp]
schema_version: 1
---

# Account takeover (ATO)

## When it applies
Any flow that can grant control of another user's account: password reset, email change, session
issuance, social/SSO linking, OTP/2FA. ATO is the highest-value web finding — hunt it deliberately.

## Why it works
Auth flows have many moving parts (tokens, emails, sessions, second factors); a single weak link
— a predictable reset token, a host-header-controlled reset link, an email change without
re-auth, an OTP with no rate limit — hands over the account.

## Method
1. **Password reset**: token predictability/entropy, token not invalidated after use/expiry,
   `Host`/`X-Forwarded-Host` poisoning the reset link (→ leak token to your domain), reset for
   another user by changing the `email`/`id` param, response leaking the token.
2. **Email change**: change to attacker email without password re-auth or without confirming the
   old address → then reset.
3. **OTP/2FA**: no rate limit (brute — see `web-race-conditions`), OTP reuse, response leaks the
   code, 2FA skippable by hitting the post-2FA endpoint directly, backup-code weaknesses.
4. **Session**: fixation, tokens not rotated on login/priv-change, JWT flaws (→ `web-auth-jwt`),
   long-lived "remember me" tokens.
5. **SSO/linking**: pre-account-takeover and `redirect_uri` theft (→ `web-oauth`).

## Gotchas
- Use two accounts you own; prove takeover end-to-end (log in as the "victim" account you control).
- Host-header reset-poisoning needs the app to build the link from the header — test it explicitly.
- Chain small pieces (info leak → reset param) rather than expecting one silver bullet.

## Verify success
You authenticate as another account without its legitimate credentials, demonstrated across two
accounts you own.

## References
PortSwigger auth labs; "Account takeover methodology" write-ups; OWASP WSTG (authentication).
