---
name: web-dom-clobbering
description: >
  Overwrite a page's JavaScript variables using only injected HTML — no script needed. Load when a
  sanitizer allows tags/attributes but strips script, and the app reads config/state from the DOM or
  globals. Signals: HTML injection behind DOMPurify/an allowlist, client code using `window.X`,
  `document.getElementById(...)`, or `config.*` that could come from named elements.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
owasp: [A03]
cwe: [CWE-79]
tools: [burp]
schema_version: 1
---

# DOM clobbering

## When it applies
You can inject HTML but not script (a sanitizer blocks JS), and the application's own JavaScript
reads values from named DOM elements or global properties. Clobbering turns pure markup into
control over those values — often the missing link to XSS or a logic bypass.

## Why it works
The browser auto-creates properties from element `id`/`name`: `<a id=x>` makes `window.x` (and
`document.x`) reference that element. Legacy code that does `var cfg = window.config || {}` or
`document.getElementById('token')` can be *clobbered* — you supply the element, so you control what
that "variable" resolves to.

## Method
1. **Find the sink**: JS that reads a global or a named element and uses it in a dangerous way —
   `element.src`, `location`, `innerHTML`, a URL it fetches, or a feature flag.
2. **Clobber a single value**: `<a id=config href="//attacker">` so `config` resolves to an element
   whose `href`/`toString()` you control.
3. **Clobber nested props**: two elements with the same `name` form an `HTMLCollection`, so
   `<a id=config name=url>` + `<a id=config>` lets you shape `config.url`. Forms clobber too:
   `<form id=x><input name=y>` gives `x.y`.
4. **Reach a script gadget**: point a clobbered `src`/URL at attacker JS, or flip a security flag the
   code trusts (e.g. `if(config.debug)`), to escalate to XSS or an open redirect.
5. **Confirm** the app's own code now reads your value.

## Gotchas
- Needs code that *reads* the DOM/global — no sink, no bug. Read the JS first.
- Sanitizer config matters: `id`/`name` must survive (DOMPurify allows them by default unless
  `SANITIZE_NAMED_PROPS` is set).
- Clobbering gives a value/element, not code execution by itself — you still need a sink to weaponise.

## Verify success
The application's JavaScript observably uses your clobbered value (e.g. loads your script, redirects,
or changes a security decision) with no script tag involved.

## References
PortSwigger DOM clobbering; DOMPurify docs (named-property sanitisation); HTMLCollection/named-access spec.
