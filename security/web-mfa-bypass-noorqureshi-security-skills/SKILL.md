---
name: web-mfa-bypass
description: >
  Defeat a second authentication factor — OTP/TOTP, SMS, push, or backup codes. Load when login has
  a 2FA/MFA step and you want to reach the account without the factor, on "2FA bypass", "OTP brute",
  "MFA", or during account-takeover work. Signals: an OTP/verification screen after password, a
  "verify your device" step, `/verify`, `/2fa`, `otp`/`code` parameters.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A07]
cwe: [CWE-287]
tools: [burp, turbo-intruder]
schema_version: 1
---

# 2FA / MFA bypass

## When it applies
Authentication has a second step after the password. MFA is only as strong as its enforcement — the
common flaws are in the *flow*, not the crypto, and each is worth a quick check before assuming the
factor is solid.

## Why it works
The second factor is usually bolted onto a stateful flow, and the server often trusts the client to
follow it. Skip the step, replay a state, or brute a short code with no rate limit, and the factor
never actually gates access.

## Method — work the checklist
1. **Missing server-side enforcement**: complete step 1, then request a post-auth endpoint directly
   (forced browsing) or reuse the step-1 session — if it works, 2FA is cosmetic.
2. **No rate limit on the code**: brute the 6-digit OTP (Turbo Intruder); watch for missing lockout,
   or a lockout you can reset by re-triggering send. Also test code **reuse** and **non-expiry**.
3. **Response/flag manipulation**: flip `"mfa_required":true`→`false`, `verified:false`→`true`, or a
   200/302 the client trusts to advance.
4. **Flow/logic**: change the account/email between step 1 and 2 (bind your factor to their session),
   downgrade to a factor you control, or use password-reset to skip MFA entirely.
5. **Backup/remember**: weak/guessable backup codes, a "remember this device" cookie that's static
   or forgeable, or OAuth/SSO paths that skip MFA.

## Gotchas
- Account lockout can burn the test account — throttle and use your own accounts.
- Distinguish "reached the OTP screen" from "reached the account" — only the latter is the bypass.
- Some apps enforce MFA at sensitive actions, not login — test the step-up too.

## Verify success
You reach the authenticated account (or perform the MFA-gated action) without presenting a valid
second factor, reproducibly from a clean session with test accounts.

## References
PortSwigger 2FA bypass labs; OWASP Authentication Testing (OTP/MFA); OWASP ASVS auth requirements.
