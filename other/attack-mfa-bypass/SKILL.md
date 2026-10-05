---
name: attack-mfa-bypass
description: "MFA bypass — response manipulation, OTP reuse, and 2FA flow skipping for authentication bypass"
category: "authentication"
version: "1.0"
author: "bountyreper-official"
tags:
  - mfa
  - 2fa
  - otp
  - bypass
tech_stack:
  - web
cwe_ids:
  - CWE-287
  - CWE-308
chains_with:
  - wstg-athn-11
  - attack-oauth
prerequisites: []
---

# MFA Bypass

## Objective

Bypass multi-factor authentication via response manipulation, direct endpoint access, and OTP flaws.

> **Attribution:** Methodology from [KathanP19/HowToHunt — MFA_Bypasses, Authentication_Bypass](https://github.com/KathanP19/HowToHunt/tree/master/MFA_Bypasses). Licensed GPL-3.0.

## Testing Methodology

### Response Manipulation

```http
POST /verify-otp HTTP/1.1
{"code":"0000"}
# Response: {"success":false}
# Change to {"success":true} and forward — if client trusts, bypass
```

### Direct Access to Post-MFA Endpoint

```bash
# Skip MFA by directly hitting authenticated endpoint
curl -H "Cookie: session=pre-mfa-token" https://target.com/dashboard
# If 200 without MFA, bypass
```

### OTP Reuse and Brute Force

```bash
# Reuse same OTP twice
# No rate limit brute force (see attack-password-reset OTP section)
# OTP for one user works for another (not bound)
```

### Backup Code Abuse

- Test if backup codes not invalidated after use
- Test if backup code generation is predictable

## References

- [HowToHunt — MFA Bypasses](https://github.com/KathanP19/HowToHunt/tree/master/MFA_Bypasses)
