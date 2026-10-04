---
name: api-review
description: Review an authorized API surface for access control, mass assignment, schema validation, rate limiting, SSRF, error leakage, webhook verification, and unsafe defaults. Use for REST, GraphQL, RPC, and webhook handlers.
---

# API Review

## Focus

- route, resolver, and webhook authorization
- object scoping and tenant filters
- request validation and mass assignment
- response leakage and error behavior
- rate limiting and abuse resistance
- server-side fetch and callback verification

## Output rule

Prioritize externally reachable issues and admin-facing paths first.
