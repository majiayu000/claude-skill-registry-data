---
name: web-xss
description: >
  Find and prove Cross-Site Scripting (reflected, stored, DOM). Load when input is echoed
  into HTML/JS/attributes, a search/comment/profile field renders your text, a URL param
  appears in the response, or a sink like innerHTML/document.write is in client JS. Signals:
  "search=", reflected values, error pages echoing input, Angular/React dangerouslySetInnerHTML.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A03:2021-Injection]
cwe: [CWE-79]
tools: [burp, caido, curl]
schema_version: 1
---

# Cross-Site Scripting (XSS)

## When it applies
Any place your input reaches the response or the DOM without correct context-aware output
encoding: reflected (in the immediate response), stored (saved then rendered to others),
or DOM-based (client-side JS writes attacker data into a sink).

## Why it works
The browser can't tell your data from the page's own markup/script. If input lands in an
HTML context and the app doesn't encode `< > " ' &` *for that exact context*, your bytes
become new elements, attributes, or script. Filters usually fail because they encode for
the wrong context (HTML-encode but you're in a JS string, or in an attribute, or in a URL).

## Method
1. **Find reflections.** Inject a unique canary `rn0x931` in every param/header and grep the
   response for it. `ffuf`/Burp Intruder to spray params; note *where* it lands (tag body,
   attribute, JS string, comment).
2. **Break the context** with the minimum needed for that spot:
   - HTML body: `<svg onload=alert(document.domain)>`
   - Attribute value: `" autofocus onfocus=alert(document.domain) x="` (close the attr first).
   - JS string: `';alert(document.domain);//`  (close the string/statement).
   - `href`/URL: `javascript:alert(document.domain)`.
3. **DOM XSS:** trace `location.hash`/`search`/`name` → `innerHTML`/`document.write`/`eval`/
   jQuery `$()`. Use browser DevTools + `DOMInvader` (Burp) to auto-find source→sink flows.
4. **Prove impact** for a report: `document.domain` in the alert, or exfil a cookie/CSRF token
   to your collaborator — not `alert(1)` on a sandboxed origin.

## Gotchas
- `alert()` fires but it's a different origin / sandbox → not impactful; check the origin.
- CSP can neuter inline script — look for `unsafe-inline`, a JSONP endpoint, or an allowed CDN you can abuse.
- Reflected-but-encoded (`&lt;`) means right context, wrong break — try attribute/JS breakouts, not more tags.
- Stored XSS may render in an admin panel you can't see; report the stored sink + a plausible viewer.

## Verify success
Script executes in the target's origin (alert shows the real `document.domain`), or your
collaborator receives the exfil'd token. Screenshot the popup with the URL bar visible.

## References
PortSwigger Web Security Academy (XSS); OWASP XSS Prevention Cheat Sheet.
