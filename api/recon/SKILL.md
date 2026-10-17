---
name: attack-graphql-recon
description: "GraphQL recon — introspection, field suggestion mining, schema extraction via error messages, hidden endpoint discovery"
category: "web-application"
version: "1.0"
author: "bountyreper-official"
tags:
  - graphql
  - recon
  - introspection
  - schema
tech_stack:
  - graphql
cwe_ids:
  - CWE-200
chains_with:
  - attack-graphql
  - attack-graphql-authz
prerequisites:
  - attack-graphql
---

# GraphQL Recon & Introspection

## Objective

Build the complete API map — the schema tells you every query/mutation/field, and most
authz bugs become obvious once you can read it.

## Methodology

### 1. Introspection (full schema)

```bash
curl -s -X POST https://TARGET/graphql -H "Content-Type: application/json" -d '{
"query":"{ __schema { queryType { name } mutationType { name } types { name kind fields { name type { name kind ofType { name } } args { name defaultValue } } } } }"}'
```

If blocked on the full query, probe DEPTH: `__schema{types{name}}` →
`__type(name:"User"){fields{name}}` — granular introspection often survives the block.

### 2. Field-suggestion mining (when introspection is disabled)

```bash
# GraphQL's own error suggestions leak field names
curl -s -X POST https://TARGET/graphql -H "Content-Type: application/json" \
  -d '{"query":"{ user { emails } }"}'
# → "Did you mean email or emailsList?" — enumerate candidates this way
# Tools: clairvoyance, graphql-field-suggestion
```

### 3. Character-probing for hidden types

```text
{ __type(name:"a") ... } → bisect types alphabetically via error/empty responses
{ a } → "Cannot query field X" messages leak queryType fields
```

### 4. Introspection via alternate content-types

```bash
# Some stacks allow form-encoded/graphql-ws/GET
curl -s "https://TARGET/graphql?query={__schema{types{name}}}"
curl -s -X POST https://TARGET/graphql -d "query={__schema{types{name}}}" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

### 5. Schema → target list

From the extracted schema, generate:
- Every mutation for authz testing (mutations are where broken checks live)
- Object types with nested connections → IDOR candidate chains (pair attack-idor-automation)
- Admin-only fields (isInternal, admin*, private*) → privilege tests
- Subscriptions → real-time leak channels

## Proof

- Schema extraction = your recon artifact (internal note), plus any field-leak error
  message if introspection was disabled (that error leak itself can be a low finding)

## Notes

- clairvoyance reconstructs schemas from suggestions when introspection is fully blocked
- Confirm the SAME schema on all discovered endpoints (versions differ per endpoint)
