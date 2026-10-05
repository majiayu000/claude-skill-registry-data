---
name: attack-signup
description: "Signup functionality flaws — duplicate accounts, email verification bypass, and weak validation"
category: "identity-management"
version: "1.0"
author: "bountyreper-official"
tags:
  - signup
  - authentication
  - idor
tech_stack:
  - web
cwe_ids:
  - CWE-287
  - CWE-640
chains_with:
  - wstg-idnt-02
  - attack-account-takeover
prerequisites: []
---

# Signup Functionality Hunting

## Objective

Find flaws in registration that lead to account takeover, enumeration, or privilege escalation.

> **Attribution:** Methodology from [KathanP19/HowToHunt — Sign_Up_Functionality](https://github.com/KathanP19/HowToHunt/tree/master/Sign_Up_Functionality). Licensed GPL-3.0.

## Testing Methodology

```bash
# Duplicate account
curl -X POST https://target.com/register -d "email=victim@target.com&password=pass123"
curl -X POST https://target.com/register -d "email=victim@target.com&password=pass456" # 200 = duplicate allowed

# Email verification bypass
# Register, intercept verification request, change email param
POST /verify?email=attacker@evil.com&code=1234
# Change to victim@target.com with same code

# Weak validation
curl -X POST https://target.com/register -d "email=test@test&password=1" # short/invalid accepted?

# Check for auto-login after signup without verification
```

## References

- [HowToHunt — Signup](https://github.com/KathanP19/HowToHunt/tree/master/Sign_Up_Functionality)
