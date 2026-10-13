---
name: web-http-parameter-pollution
description: >
  Send the same parameter more than once so the WAF/validator and the backend disagree on which
  value wins — bypassing filters, access control, or business logic. Load on "HPP", when a value is
  validated at one layer but used at another, or when a WAF blocks a payload you need to slip past.
  Signals: proxies/gateways in front of the app, duplicated params reflected inconsistently.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
owasp: [A03]
cwe: [CWE-235]
tools: [burp]
schema_version: 1
---

# HTTP parameter pollution

## When it applies
A request passes through more than one component that parses parameters — a WAF/gateway, then the
app; or a frontend that builds a backend request. If they resolve a duplicated parameter
differently, you can show one value to the guard and another to the logic.

## Why it works
There is no single rule for `?x=a&x=b`: PHP/Apache take the **last**, ASP/IIS **concatenates**
(`a,b`), classic JSP takes the **first**, Node/Express makes an **array**. When the validator and
the consumer sit on different stacks, a value that passes validation isn't the value that's used.

## Method
1. **Map the parsing**: send `?p=1&p=2` (and body dups) and observe which value the response reflects
   or acts on — that tells you first/last/concat/array.
2. **Split a blocked payload**: if a WAF blocks `q=<svg onload=..>`, try `q=<svg&q=onload=..>` where
   the backend concatenates — the signature never appears whole to the WAF.
3. **Override server-side params**: append your own copy of a param the app also sets internally
   (e.g. `role`, `amount`, `redirect_uri`) so your last-wins value overrides the trusted one.
4. **Access control / logic**: pollute IDs or flags where the auth check reads one occurrence and the
   data layer reads another.
5. **Client-side HPP**: when a link/form is built from your input, inject `&`-encoded params to add
   fields to the generated request.

## Gotchas
- Behaviour is stack-specific — always confirm the parsing empirically before relying on it.
- Body vs query vs path params may parse differently in the same app; test each channel.
- Concatenation (`a,b`) can corrupt the payload — order the duplicates to land valid syntax.

## Verify success
The duplicated parameter produces a different outcome than the single one — a filter is bypassed, an
internal value overridden, or a logic/authz decision changes — reproducibly.

## References
OWASP Testing Guide (HPP); PortSwigger notes on parameter parsing; framework parameter-precedence tables.
