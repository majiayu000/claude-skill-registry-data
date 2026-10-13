---
name: web-prototype-pollution
description: >
  JavaScript prototype pollution (client & server) → XSS, auth bypass, RCE via gadgets. Load on
  Node.js/JS apps that merge user objects: query/JSON parsing, `Object.assign`/deep-merge,
  lodash/jQuery.extend, config merges. Signals: __proto__, constructor.prototype in params,
  Node backend, client-side sinks.
domain: web
type: technique
stability: learning
modes: [bugbounty, pentest]
severity: high
owasp: [A08:2021-Software-and-Data-Integrity-Failures]
cwe: [CWE-1321]
tools: [burp, ppmap]
schema_version: 1
---

# Prototype pollution

## When it applies
A JS app merges attacker-controlled keys into an object without blocking `__proto__` /
`constructor` / `prototype`. Client-side or Node server-side. Impact needs a "gadget" — code
that later reads a polluted property.

## Why it works
In JS, every object shares `Object.prototype`. Writing `__proto__.x` via a vulnerable merge sets
`x` on *every* object. A later read of `obj.x` (that the dev assumed was undefined) now returns
your value — turning a config default, an HTML attribute, or a command option to your advantage.

## Method
1. **Find the sink**: params/JSON merged via deep-merge/`Object.assign`/lodash `merge`/`set`,
   `$.extend(true,...)`, query parsers. Test `?__proto__[test]=x` or `{"__proto__":{"test":"x"}}`.
2. **Confirm pollution**: check `Object.prototype.test` in console (client) or a reflected default (server).
3. **Chain to a gadget**:
   - **Client**: pollute a property a library reads to inject HTML/script → DOM XSS (e.g. sanitizer options, template defaults).
   - **Server (Node)**: pollute options later used by `child_process` (`shell`, `NODE_OPTIONS`,
     `argv0`), template engines, or `ejs`/`lodash.template` → RCE; or flip an `isAdmin`/auth default → authz bypass.
4. **Automate discovery** with `ppmap`/DOM Invader prototype-pollution mode.

## Gotchas
- Pollution with no reachable gadget is low-impact — find the read to prove real effect.
- `Object.freeze(Object.prototype)` / `Object.create(null)` / Map usage kills it.
- Server-side needs the polluted key to survive to a dangerous consumer — trace it.

## Verify success
A polluted prototype property produces concrete impact — XSS firing, an auth default flipped, or
command execution via a known gadget.

## References
PortSwigger prototype-pollution labs; "Server-side prototype pollution" (PortSwigger); HackTricks.
