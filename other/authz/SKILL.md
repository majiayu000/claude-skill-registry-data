---
name: attack-graphql-authz
description: "GraphQL authorization bypass — field-level authz, IDOR via nesting, mutations without ownership checks, mass assignment, info disclosure via errors"
category: "web-application"
version: "1.0"
author: "bountyreper-official"
tags:
  - graphql
  - authz
  - idor
  - mass-assignment
tech_stack:
  - graphql
cwe_ids:
  - CWE-284
  - CWE-639
chains_with:
  - attack-graphql
  - attack-idor-automation
prerequisites:
  - attack-graphql
---

# GraphQL Authorization Testing

## Objective

GraphQL's nested object model breaks naive authz: checks on the ROOT query don't
cascade into nested fields. Test every field path, not just the entrypoint.

## Methodology

### 1. Field-level authz (the classic GraphQL authz bug)

```text
{ user(id:"<victim-id>") { id email } }              ← allowed for you?
{ user(id:"<victim-id>") { paymentMethods { last4 } } }  ← NESTED field, often unchecked
{ user(id:"<victim-id>") { sessions { ip token } } }     ← admin-ish fields
```

Own your ID everywhere it appears as a nested path — the root check passes, nested
fields bypass. Test one query per sensitive field with a victim ID.

### 2. IDOR via object nesting / aliases

```text
query { me { ... } } + aliased second fetch:
{ a: user(id:1){email} b: user(id:2){email} }   ← batched in ONE request
```

- Batch aliases let you test MANY victim IDs per request (pair with attack-idor-automation)
- Connections (`orders(first:100)`) often skip ownership checks on edges

### 3. Mutation authz (highest yield)

For EVERY mutation in the schema:
- Call with another user's object ID → ownership check missing?
- Call as the LOWEST-privilege role (signup-only account) against admin mutations
- Mass assignment: extra args the schema doesn't declare (role, status, verified)
  → some resolvers spread args server-side — try `role:"admin"` in variables

### 4. Error-message disclosure

```text
{ user(id:"<admin-id>") { email } }
→ "Not authorized for field paymentMethods of User:<id>" — the ERROR leaks which
fields EXIST and which checks fire (recon for stage 1 above)
```

### 5. Direct object access via fragments

```text
fragment A on InternalType { secretFlag }   ← if fragment spread on an unrelated
{ user { ...A } }                            type is allowed, type-level checks are absent
```

## Proof requirements

- TWO accounts minimum (different roles if possible)
- The EXACT query pair (allowed vs bypassed) side by side
- Data values REDACTED when PII — show field names + structure, not content
- One bug per field-path: "user.paymentMethods.billingAddress leaks cross-account" is
  the report, not "GraphQL authz broken"

## Notes

- Authz layers (hasura rules, postgraphile) return EMPTY data instead of errors —
  compare against YOUR OWN query's output shape, empty-vs-data is the signal
