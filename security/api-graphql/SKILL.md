---
name: api-graphql
description: >
  Attack GraphQL APIs. Load on /graphql, /graphiql, /v1/graphql, a POST with {"query":"..."},
  Apollo/Hasura/graphene stacks, or "query/mutation" language. Signals: introspection enabled,
  batched queries, deeply nested fields, __schema, aliases.
domain: api
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp_api: [API1:2023-BOLA, API5:2023-BFLA]
cwe: [CWE-639, CWE-284]
tools: [graphw00f, clairvoyance, burp, inql]
schema_version: 1
---

# GraphQL abuse

## When it applies
The target exposes a GraphQL endpoint. GraphQL collapses many objects behind one URL, so
authorization gaps and info leaks are common and easy to miss with URL-based testing.

## Why it works
One endpoint, a self-describing schema, and per-field resolvers mean access control must be
enforced at every field/resolver — it frequently isn't. Introspection hands you the entire
attack surface; batching/aliases turn one request into thousands.

## Method
1. **Fingerprint & map**: `graphw00f` for the engine; if introspection is on, dump the schema
   (`{__schema{types{name fields{name}}}}`) with `inql`/`clairvoyance`. If off, brute field
   names with `clairvoyance` (error messages leak valid fields).
2. **AuthZ testing (BOLA/BFLA)**: call queries/mutations for objects and admin operations you
   shouldn't reach; swap ids in arguments (same as IDOR) — resolvers often skip owner checks.
3. **Info disclosure**: reach sensitive fields/types (users, tokens, internal flags) via
   nested relations even when the "front door" query hides them.
4. **DoS / cost**: deeply nested recursive queries and aliased batching (`a:login b:login ...`)
   to bypass rate limits or brute-force — respect program rules on this.
5. **Injection**: arguments feed backends — test SQLi/NoSQLi in GraphQL variable values.

## Gotchas
- Introspection off ≠ safe — field brute-forcing and suggestion errors still map the schema.
- Rate-limit bypass via batching/aliases is a real, reportable finding on many programs.
- Mutations are where impact lives; don't stop at read queries.

## Verify success
Retrieve/modify data through a query or mutation your role shouldn't allow, or dump a schema
that reveals hidden admin operations.

## References
PortSwigger GraphQL labs; OWASP API Security Top 10 (2023); graphw00f/inql docs.
