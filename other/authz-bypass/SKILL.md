---
name: authz-bypass
description: >
  Test horizontal and vertical authorization bypass via session ID swapping between accounts,
  IDOR through parameter manipulation (invoice=, user=, menuitem=, EventID=), and special header
  injection (X-Original-URL, X-Rewrite-URL, X-Forwarded-For, X-Remote-IP, X-Client-IP with
  127.0.0.1/localhost/RFC1918 values). Tools: Burp Suite with Autorize/AuthMatrix extensions,
  OWASP ZAP Access Control Testing add-on.
license: MIT
compatibility: Designed for Claude Code. Requires Burp Suite with Autorize or AuthMatrix extension.
metadata:
  category: web
  version: "0.1"
  source: https://owasp.org/www-project-web-security-testing-guide/stable/
  source_types: framework
  wstg: WSTG-ATHZ-02, WSTG-ATHZ-04
---

# Authorization Bypass and IDOR

## What Is Broken and Why

Access control failures occur when applications enforce authorization only at the UI layer, rely
on obscurity of object identifiers, or fail to validate that the requesting session owns the
referenced resource. Horizontal bypass allows users to access peer accounts' data by swapping
identifiers. Vertical bypass allows low-privileged users to invoke admin-only operations by
replaying high-privilege request structures with a low-privilege session. IDOR (Insecure Direct
Object Reference) exposes any predictable or discoverable resource identifier as a direct handle
to unauthorized data. Special request headers (`X-Original-URL`, `X-Rewrite-URL`) can override
routing in some reverse proxy configurations, bypassing ACL rules applied at the path level.

## Key Signals

- Numeric or sequential IDs in URLs or parameters: `invoice=12345`, `user=100`, `EventID=1000001`
- Different accounts created at similar times with adjacent IDs
- Responses containing another user's PII, financial data, or account settings when ID swapped
- Admin-only actions (delete, promote, deactivate) accessible via session swap
- `X-Original-URL` or `X-Rewrite-URL` headers triggering 404 vs 403 — confirms header processing
- `X-Forwarded-For: 127.0.0.1` bypassing IP-based access restrictions to admin panels
- GUIDs or opaque tokens that, when substituted, return another user's object
- `menuitem=` or `accessPage=` parameters accepting values outside a user's visible menu set
- Password change endpoint accepting `user=` parameter without session-ownership validation

## Methodology

1. **Map object references**: During application use, record every parameter that references a
   resource (document ID, user ID, order number, file name, menu item).
2. **Create test accounts**: Register at least two accounts at different privilege levels; note
   all object IDs each account owns.
3. **Horizontal bypass**: With Account B's session, request objects owned by Account A by
   substituting Account A's IDs.
4. **Vertical bypass**: With low-privilege session, replay admin-only requests (delete, role
   change, config update) captured from an admin session.
5. **IDOR enumeration**: Increment/decrement integer IDs; test adjacent values; attempt GUID
   prediction if UUIDs appear time-seeded.
6. **Header injection test**: Send `X-Original-URL: /admin` and `X-Rewrite-URL: /admin` on a
   request to `/`; 404 response (vs 403 on direct access) confirms header support.
7. **IP spoofing header test**: Send `X-Forwarded-For: 127.0.0.1` on requests to IP-restricted
   admin endpoints; observe access control difference.
8. **POST-to-GET conversion**: Test if server accepts session ID or IDOR parameter via GET when
   originally designed for POST.

## Payloads & Tools

```bash
# Horizontal IDOR — access another user's invoice
curl -s "https://TARGET/invoice?id=12345" \
  -H "Cookie: SessionID=ATTACKER_SESSION"
# Enumerate adjacent IDs
for id in $(seq 12340 12350); do
  echo -n "ID $id: "
  curl -s -o /dev/null -w "%{http_code}" \
    "https://TARGET/invoice?id=$id" \
    -H "Cookie: SessionID=ATTACKER_SESSION"
  echo
done

# Vertical bypass — low-priv session attempting admin delete
curl -X POST "https://TARGET/account/deleteEvent" \
  -H "Cookie: SessionID=CUSTOMER_USER_SESSION" \
  -d "EventID=1000002"

# X-Original-URL header test (confirms if reverse proxy processes it)
curl -s -o /dev/null -w "%{http_code}" \
  "https://TARGET/" \
  -H "X-Original-URL: /admin/users"

curl -s -o /dev/null -w "%{http_code}" \
  "https://TARGET/" \
  -H "X-Rewrite-URL: /admin/config"

# X-Original-URL bypass attempt to restricted path
curl -s "https://TARGET/" \
  -H "X-Original-URL: /admin/dashboard" \
  -H "Cookie: SessionID=LOW_PRIV_SESSION"

# IP spoofing via forwarding headers to bypass IP-based admin restriction
for header in "X-Forwarded-For" "X-Forward-For" "X-Remote-IP" "X-Originating-IP" \
              "X-Remote-Addr" "X-Client-IP"; do
  echo -n "$header: "
  curl -s -o /dev/null -w "%{http_code}" \
    "https://TARGET/admin/" \
    -H "$header: 127.0.0.1"
  echo
done

# IDOR on direct password change
curl -X POST "https://TARGET/changepassword" \
  -H "Cookie: SessionID=ATTACKER_SESSION" \
  -d "user=VICTIM_USERNAME&newPassword=hacked123"

# IDOR on file resource
curl "https://TARGET/showImage?img=img00001" \
  -H "Cookie: SessionID=ATTACKER_SESSION"
# Try adjacent:
curl "https://TARGET/showImage?img=img00002" \
  -H "Cookie: SessionID=ATTACKER_SESSION"

# Burp Autorize — install extension, browse as low-priv user; it auto-replays
# all requests with low-priv session to detect access control failures
```

## Bypass Techniques

- **Encoded IDs**: Base64 or hex-encoded object IDs that decode to integers are still enumerable.
- **GUIDs**: UUIDv1 contains a timestamp; reconstruct approximate range and brute-force.
- **Indirect reference swap**: If application uses indirect maps (1→real_id), find the mapping
  endpoint and enumerate it separately.
- **Method switching**: Try GET instead of POST, or PUT/PATCH instead of POST for restricted
  operations.
- **Content-Type switch**: Change `application/json` to `application/x-www-form-urlencoded`;
  some authorization middleware only inspects one.
- **Case and encoding variation**: `/Admin/` vs `/admin/`; URL encoding of path segments to
  evade path-based ACL matching.
- **Parameter pollution**: `user=ADMIN_ID&user=ATTACKER_ID` — some frameworks take first, some
  take last; test both.

## Exploitation Scenarios

**Scenario 1 — Horizontal IDOR: Access Another User's Account Settings**
Setup: Account settings URL is `https://TARGET/viewSettings?username=example_user`.
Trigger: Attacker changes `username=example_user` to `username=victim_user` with own session.
Impact: Attacker reads victim's personal data, email, phone number, saved payment info.

**Scenario 2 — Vertical Bypass via Session Swap on Admin Endpoint**
Setup: Admin delete endpoint `POST /account/deleteEvent` captured; attacker has customer session.
Trigger: Replay identical POST with `SessionID=CUSTOMER_USER_SESSION` and a valid `EventID`.
Impact: Customer can delete any event, causing data loss or service disruption.

**Scenario 3 — X-Original-URL Header Bypass on Reverse Proxy**
Setup: Nginx proxy denies requests to `/admin` at the proxy layer; backend trusts `X-Original-URL`.
Trigger: Send `GET / HTTP/1.1` with `X-Original-URL: /admin/users`; proxy allows `GET /`,
backend routes to `/admin/users`.
Impact: Full admin interface access without triggering proxy-level access controls.

## False Positives

- A 200 response to a swapped ID that returns no sensitive data (empty object, generic message)
  is not an exploitable IDOR.
- `X-Original-URL: /nonexistent` returning 404 (not 403) confirms header support but only becomes
  exploitable if the backend also trusts it for access control decisions.
- IP header bypass only matters if the application actually restricts access by IP; confirm by
  testing without the header first.

## Fix Patterns

- Enforce authorization checks server-side on every request; derive the subject from the server
  session, never from user-supplied parameters.
- Use unpredictable object identifiers (cryptographically random UUIDs) to raise the bar for
  enumeration, but do not rely on obscurity alone.
- Validate that the object referenced by the supplied ID belongs to the requesting user's session.
- Disable or strip `X-Original-URL`, `X-Rewrite-URL`, and spoofable IP headers at the reverse
  proxy before they reach the application.
- Implement role-based access control (RBAC) enforced server-side; verify privilege on every
  state-changing operation.
- Use Burp Autorize or OWASP ZAP's Access Control Testing add-on in CI/CD to catch regressions.

## Related Skills

[[bola-idor]] is the most concentrated form of authz bypass — where the authorization failure lives at the object level rather than the route level. [[path-traversal]] applies the same logic to the filesystem: escaping the intended directory is an authz bypass on file resources. When an endpoint accepts a numeric ID parameter, the full enumeration methodology lives in [[bola-idor]]. GraphQL APIs with object-level authz failures are covered in [[graphql-idor-via-introspection-leak]].
