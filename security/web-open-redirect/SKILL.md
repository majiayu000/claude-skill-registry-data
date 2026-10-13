---
name: web-open-redirect
description: >
  Open redirect — abuse a redirect param to send users to attacker sites, and chain it (OAuth
  token theft, SSRF filter bypass, phishing). Load on params like redirect=, next=, url=,
  return=, callback=, dest=, or a 30x Location built from input. Signals: `?returnUrl=`, login
  redirects, OAuth `redirect_uri`.
domain: web
type: technique
stability: learning
modes: [bugbounty]
severity: low
owasp: [A01:2021-Broken-Access-Control]
cwe: [CWE-601]
tools: [burp]
schema_version: 1
---

# Open redirect

## When it applies
The app redirects to a location derived from user input without validating it stays on-site.
Low severity alone — but a powerful chain link.

## Why it works
The redirect target is attacker-controlled and trusted. On its own it's phishing; chained, it
turns other flows malicious (OAuth codes/tokens sent to your host, SSRF allowlist bypass via a
redirect to an internal URL).

## Method
1. **Find the param** (`redirect/next/url/return/dest/callback`) and set it to an external URL;
   follow the response — a 30x `Location: https://evil.com` (or JS/meta redirect) confirms.
2. **Bypass naive validation**: `//evil.com`, `https:evil.com`, `https://target.com@evil.com`,
   `https://target.com.evil.com`, `/\evil.com`, whitelisted-prefix tricks, double-encoding, CRLF.
3. **Chain for impact**:
   - **OAuth**: if it's the `redirect_uri`/return in an auth flow → steal the code/token (→ `web-oauth`, ATO).
   - **SSRF allowlist**: allowed host that open-redirects to an internal target bypasses the filter.
   - **XSS**: `javascript:` scheme in the redirect where the sink allows it.

## Gotchas
- Standalone open redirect is often low/informational — lead with the chain (OAuth/SSRF) for real severity.
- Test both server 30x and client-side (JS `location`, meta refresh) redirects.
- Path-relative allowlists frequently miss `//` and `\` — try them.

## Verify success
The app redirects the user to an attacker-controlled origin, or (chained) a token/code is
delivered to your host / an SSRF filter is bypassed.

## References
PortSwigger OAuth+redirect labs; OWASP Unvalidated Redirects Cheat Sheet.
