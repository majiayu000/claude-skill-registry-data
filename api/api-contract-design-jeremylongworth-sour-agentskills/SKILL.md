---
name: api-contract-design
description: Design API contracts for backend services, SDKs, and integrations. Use when Codex is asked to define endpoints, request/response shapes, resource models, status codes, idempotency, versioning, pagination, filtering, or OpenAPI-style API contracts.
license: MIT
---

# API Contract Design

## Core Workflow

1. Identify API consumers, use cases, resource model, auth context, and
   compatibility constraints.
2. Define endpoints or methods with request fields, response fields, status
   codes, errors, pagination, filtering, sorting, and idempotency.
3. Specify validation rules, defaults, field ownership, and backward-compatible
   evolution rules.
4. Separate public contract from implementation detail.
5. Include examples and edge cases that clients can test against.
6. Flag open decisions and review needs before implementation.

## Safety Rules

- Do not invent production behavior, security guarantees, rate limits, or auth
  scopes not present in source material.
- Do not expose internal-only fields, private identifiers, secrets, or customer
  data in examples.
- Require review for contracts affecting billing, auth, customer data, public
  APIs, or backward compatibility.

## Deliverable Shape

For API contracts, provide:

- Consumer and use case
- Resource model
- Endpoint or method table
- Request and response schemas
- Error and status-code contract
- Idempotency, pagination, filtering, and versioning notes
- Examples and edge cases
- Open decisions and review gates

## References

- Read `references/api-contract-design-checklist.md` when designing or
  reviewing an API contract.
