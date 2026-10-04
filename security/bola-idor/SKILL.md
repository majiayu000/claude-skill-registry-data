---
name: bola-idor
description: >
  Use when hunting Broken Object Level Authorization (BOLA) or Insecure Direct Object
  Reference (IDOR) vulnerabilities in APIs or web applications. Trigger on: "BOLA",
  "IDOR", "broken object level", "access other users", "object reference", numeric or
  UUID IDs in URLs or request bodies, user-scoped resources, horizontal privilege
  escalation, "change the ID in the request", second-order IDOR, blind IDOR,
  indirect reference, encoded ID, deprecated API version, JSON globbing.
license: MIT
compatibility: Designed for Claude Code. Burp Suite (Autorize extension) or curl recommended.
metadata:
  category: authorization
  version: "0.2"
  source: https://owasp.org/www-project-web-security-testing-guide/stable/
  source_types: framework
  wstg: WSTG-ATHZ-04
---

# Broken Object Level Authorization (BOLA / IDOR)

## What Is Broken and Why

The server accepts a resource identifier from the client and fetches the object without
verifying the requesting user owns or has access to it. Authorization is enforced at the
route level ("is this user logged in?") but not at the object level ("does this user own
object 1042?"). An attacker substitutes their identifier for a victim's to read, modify,
or delete resources they should never access. BOLA is consistently the #1 OWASP API Security
risk because it is trivial to test and almost always yields high-severity findings.

## Key Signals

- Numeric or sequential IDs in URL path: `/api/orders/1042`, `/users/7/profile`
- UUIDs or hashes in query params or body referencing another user's object
- Parameters named `user_id`, `account_id`, `owner_id`, `ref`, `target_id`, `invoice`
- Write operations (PUT/PATCH/DELETE) accepting an object ID
- Export/download/share endpoints with a resource ID parameter
- Keywords `me` or `current` used as ID aliases — swappable for integer IDs
- Older API versions still accessible: `/v1/`, `/v2/`, `/legacy/`
- UUIDs discoverable via public profiles, share links, password reset flows, Wayback Machine

## Methodology

1. Map all object identifiers across the entire app — URLs, query params, request body, cookies, headers.
2. Create two accounts with distinctive names (e.g. `attacker_a`, `victim_b`). Use separate browsers to keep sessions fully isolated. Fully populate the victim account with varied resources and document all encountered IDs. Capture all requests with the victim session.
3. Replay each request using the attacker token with the victim's object IDs.
4. Compare responses — same data returned = BOLA confirmed.
5. Test unauthenticated: remove `Authorization` header entirely.
6. Test write operations (PUT/PATCH/DELETE) — impact is higher than reads.
7. Test indirect references: export endpoints, share links, scheduled jobs, email triggers.
8. Test less-visible features: auto-save, draft, notification, audit log, attachment endpoints.
9. Try older API versions (`/v1/`, `/beta/`) which often lack access control patches.
10. For second-order IDOR: store a payload referencing victim's ID, trigger async processing, observe outcome.

## Payloads & Tools

```bash
# ffuf: fuzz numeric IDs around your own
ffuf -w <(seq 1000 2000) -u https://TARGET/api/users/FUZZ \
  -H "Authorization: Bearer YOUR_TOKEN" -mc 200 -fs 0

# curl: direct ID swap
curl -s https://TARGET/api/orders/VICTIM_ID \
  -H "Authorization: Bearer YOUR_TOKEN"

# Append .json to bypass access control
curl https://TARGET/api/receipts/VICTIM_ID.json \
  -H "Authorization: Bearer YOUR_TOKEN"

# Try deprecated API version
curl https://TARGET/v1/users/VICTIM_ID \
  -H "Authorization: Bearer YOUR_TOKEN"
```

```
# Burp Intruder: fuzz ±1000 around your own ID
GET /api/orders/§1042§ HTTP/1.1
Authorization: Bearer YOUR_TOKEN

# JSON globbing in request body
{"user_id": [YOUR_ID, VICTIM_ID]}
{"user_id": "*"}
{"user_id": true}
{"user_id": 0}
{"user_id": -1}
{"user_id": 1235.0}
```

**Burp extension: Autorize** — automatically replaces session token with low-priv token on every request, flags unexpected 200s and response diffs.

## Bypass Techniques

- **JSON globbing**: replace ID with `[id1, id2]`, `*`, `true`, `0`, `-1`, `1234.0` — parsers may match all
- **HTTP verb swap**: GET blocked → try POST, PUT, DELETE, PATCH on same path
- **Parameter pollution**: `?user_id=YOURS&user_id=VICTIM` — server may process last or first
- **Encoded references**: base64/hex decode the ID, increment, re-encode — app trusts encoding as security
- **Alternate field names**: `owner_id`, `account_id`, `ref`, `target`, `resource_id`, `parent_id`
- **Path traversal**: `/api/users/YOURS/../VICTIM`
- **Static keyword swap**: replace `me` or `current` with a numeric ID
- **Content-type switch**: JSON endpoint may behave differently with `application/x-www-form-urlencoded`
- **Second-order**: store a reference to victim's ID in a field, trigger async job that processes it without re-checking auth
- **Append extension**: `/resource/VICTIM_ID.json`, `.xml`, `.csv` may skip access control middleware

## Exploitation Scenarios

**Scenario 1 — Account takeover via email change**
Setup: `PUT /api/users/{id}` accepts `email` as an editable field, no ownership check.
Trigger: Attacker replaces their own `id` with victim's `id` in the request body.
Impact: Victim's email changed to attacker's address → password reset → full account takeover.

**Scenario 2 — Mass PII leak via sequential ID**
Setup: `/api/orders/{id}` returns full order: name, address, card last4, phone.
Trigger: Attacker iterates integer IDs from 1 to N with their own session token.
Impact: Thousands of customers' PII and payment metadata exfiltrated via scripted enumeration.

**Scenario 3 — Second-order IDOR via scheduled export**
Setup: App lets users schedule data exports; export job runs async and emails result.
Trigger: Attacker sets `export_for_user_id=VICTIM_ID` in the schedule request.
Impact: Victim's full data export emailed to attacker — no access control on the async job.

## False Positives

- API returns 200 but with empty or redacted data — access control is working, just silent
- Public resources (product listings, public profiles) — no authorization expected by design
- Response identical regardless of ID — server reads from session context, ID param is ignored
- `me` and `current` aliases that correctly resolve to the authenticated user only

## Fix Patterns

```sql
-- Correct: ownership enforced at query level
SELECT * FROM orders WHERE id = ? AND user_id = current_user_id()
```

```python
# Wrong: fetch then check (inefficient + race-prone)
order = db.find(id)
if order.user_id != current_user:
    raise Forbidden()

# Correct: indirect reference map (never expose raw DB IDs)
user_resource_map = {session_token: [allowed_id_1, allowed_id_2]}
if requested_id not in user_resource_map[session_token]:
    raise Forbidden()
```

- Use indirect reference maps: expose opaque tokens that map server-side to real IDs
- Centralize authorization in middleware — one place, not scattered per-route
- Apply access control consistently across ALL HTTP methods and API versions
- Disable or equally secure deprecated API versions

## Related Skills

[[authz-bypass]] covers the broader authorization failure class — BOLA is its most common manifestation. When the application uses GraphQL, [[graphql-idor-via-introspection-leak]] shows how to enumerate the schema to find every object type accepting an ID argument. [[path-traversal]] is an IDOR on the filesystem: the same "reference to a resource without ownership check" pattern applied to file paths. IDOR findings frequently reveal [[business-logic-flaws]] — such as skipping payment by referencing another order's paid state.
