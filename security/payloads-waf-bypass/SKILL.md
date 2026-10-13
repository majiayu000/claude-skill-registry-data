---
name: payloads-waf-bypass
description: >
  Bypass WAFs/filters blocking your payloads. Load when a payload that should work is blocked,
  you see 403/406/429 or "request blocked", Cloudflare/Akamai/Imperva/AWS-WAF/ModSecurity, or a
  filter strips keywords. Signals: works locally but blocked on target, generic block pages.
domain: payloads
type: reference
stability: learning
modes: [pentest, bugbounty]
severity: info
cwe: [CWE-693]
tools: [burp, ffuf]
schema_version: 1
---

# WAF / filter bypass

## When it applies
The vuln is real but a WAF or input filter blocks the exploit payload (sudden 403/406/429, a
block page, or your keyword silently stripped). You need the same payload in a form the filter
doesn't recognize but the backend still executes.

## Why it works
A WAF pattern-matches a normalized view of the request; the backend parses it differently.
Every gap between those two parsers — encoding, case, comments, alternate syntax, request
shape — is a bypass. The goal is a payload the WAF doesn't flag but the app still runs.

## Method (bypass axes — try in this order)
1. **Confirm it's the WAF, not "not vulnerable"**: does a benign version pass and the payload
   get blocked? Fingerprint (`wafw00f`), note which token triggers the block (bisect the payload).
2. **Encoding/representation**: URL/double-URL encode, HTML entities, unicode/overlong,
   mixed case, whitespace/comment insertion (`/**/`, newlines), null bytes.
3. **Alternate syntax**: SQL `UNION`→`un/**/ion`, `OR`→`||`; XSS tag/event variety (`<svg>`,
   `onpointerenter`); command `id`→`i''d`, `$IFS` for spaces.
4. **Request shaping**: change method/content-type (JSON vs form), parameter pollution, chunked
   encoding, oversized body, or move the payload to another parameter/header.
5. **Origin & rate**: find the origin IP behind the CDN (bypasses the WAF entirely); slow down
   or rotate to beat rate-limit-based blocking.
6. **Automate**: `ffuf` a bypass wordlist against the blocked param; `sqlmap --tamper` for SQLi.

See [`reference/waf-bypass-payloads.md`](reference/waf-bypass-payloads.md) for concrete payload
transforms per vuln class.

## Gotchas
- Bisect to find the *exact* blocked token before spraying — otherwise you're guessing blind.
- Origin-IP discovery often beats any payload trickery — check DNS history / SSRF / misconfig.
- Respect RoE: WAF-bypass fuzzing is noisy; throttle on live programs.

## References
OWASP evasion; PortSwigger WAF bypass; `sqlmap` tamper scripts; wafw00f.
