---
name: web-idor
description: >
  Insecure Direct Object Reference / broken access control on web objects. Load when a
  request references an object by id you can change: /account/1234, ?invoice=987, UUIDs in
  URLs/bodies, "download", "view", "edit" endpoints, numeric or guessable identifiers, or
  multi-tenant apps. Signals: sequential IDs, object refs in JSON, role/owner not re-checked.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A01:2021-Broken-Access-Control]
owasp_api: [API1:2023-BOLA]
cwe: [CWE-639, CWE-284]
tools: [burp, autorize, caido]
schema_version: 1
---

# Insecure Direct Object Reference (IDOR)

## When it applies
The app trusts a client-supplied identifier to decide which object to return or mutate, and
authorization is checked at the *route* ("is logged in?") but not at the *object* ("does THIS
user own THIS object?").

## Why it works
Access control is missing at the data layer. The server maps id → row and returns it without
asking whether the current session is allowed that row. Sequential/predictable ids make
enumeration trivial; even UUIDs leak (in listings, referrers, other endpoints).

## Method
1. **Get two accounts** (A = attacker, B = victim). Do an action as B, capture the request,
   note the object id.
2. **Replay as A**: swap in B's id (or A's session + B's id). Returned/changed = IDOR.
3. **Cover all verbs & spots**: id in path, query, body, JSON, cookie, and `X-*` headers;
   test GET/POST/PUT/DELETE — read-only checks often miss write IDOR.
4. **Automate the two-session diff** with Burp **Autorize**/**AutoRepeater**: it re-sends every
   request with A's cookies and flags responses that shouldn't succeed.
5. **Enumerate** where ids are sequential to size impact (count of exposed records), without
   hoarding real PII.

## Gotchas
- "UUID so it's safe" is false — UUIDs appear in other responses, emails, and referers.
- Sometimes the id is hashed/encoded (base64, `md5(id)`) — decode, tamper, re-encode.
- Mass-assignment overlaps: changing an `owner_id`/`user_id` in the body can grant access.
- Blind write-IDOR: no response body, but the victim object changed — verify from B's view.

## Verify success
You read or modify an object belonging to another tenant/user using your own session.
Screenshot both: your session token + the victim's data/changed state.

## References
PortSwigger access-control labs; OWASP API Security Top 10 (BOLA).
