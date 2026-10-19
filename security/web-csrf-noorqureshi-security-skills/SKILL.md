---
name: web-csrf
description: >
  Cross-Site Request Forgery — force a victim's browser to perform state-changing actions. Load
  on state-changing requests (POST/PUT/DELETE) that rely only on cookies, missing/weak CSRF
  tokens, `SameSite=None`, or forms/JSON without anti-CSRF. Signals: cookie-only auth, no token,
  token not validated.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
owasp: [A01:2021-Broken-Access-Control]
cwe: [CWE-352]
tools: [burp]
schema_version: 1
---

# Cross-Site Request Forgery (CSRF)

## When it applies
A state-changing action authenticated purely by an ambiently-sent credential (cookie) with no
unpredictable token the attacker's site can't know/replay.

## Why it works
Browsers attach cookies to cross-site requests automatically. If the server accepts the action
on cookie alone, an attacker page can submit it on the victim's behalf. Anti-CSRF tokens /
`SameSite` cookies break this by requiring something cross-site JS can't supply.

## Method
1. **Find a candidate**: a sensitive action (change email/password, transfer, role) that changes state.
2. **Check the defenses**: is there a CSRF token? Is it *validated* (remove it / reuse another
   user's / swap value)? Is the cookie `SameSite=Lax/Strict`? Is it a simple request (no preflight)?
3. **Build the PoC**: auto-submitting HTML form (or `fetch` for simple requests) that fires the
   action; host it and load it as the victim.
4. **Bypass weak tokens**: token not tied to session, predictable, accepted when blank, only
   checked if present, or leaked via GET/referer.
5. **JSON endpoints**: try `Content-Type: text/plain`/form-encoding to avoid preflight; if the
   API accepts it, CSRF applies.

## Gotchas
- `SameSite=Lax` (now default in Chrome) blocks most cross-site POST CSRF — look for `None`, GET-based actions, or method override.
- Token present ≠ safe — always test that it's actually validated and bound to the session.
- Login CSRF and CSRF chained with self-XSS are often the real impact.

## Verify success
Loading your PoC while authenticated as the victim performs the action (email changed, etc.)
with no interaction beyond visiting the page.

## References
PortSwigger CSRF labs; OWASP CSRF Prevention Cheat Sheet.
