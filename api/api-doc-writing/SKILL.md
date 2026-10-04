---
name: api-doc-writing
description: Write or improve API documentation from code, specs, schemas, or examples. Use when Codex is asked to document endpoints, SDK methods, request and response shapes, auth, errors, rate limits, examples, or OpenAPI-style contracts.
license: MIT
---

# API Doc Writing

## Core Workflow

1. Identify the API audience, surface area, source of truth, auth model, and
   version.
2. Read code, specs, tests, schemas, or examples before documenting behavior.
3. Document each operation with purpose, inputs, outputs, auth, errors, limits,
   side effects, and examples.
4. Separate stable contract from implementation detail.
5. Flag unknown behavior, undocumented errors, missing examples, and version
   mismatches.
6. Include validation or review steps for generated docs.

## Safety Rules

- Do not invent endpoint behavior, parameters, status codes, auth scopes, rate
  limits, or guarantees.
- Do not expose secrets, internal hosts, private tokens, or customer data in
  examples.
- Verify platform or third-party API facts from current official docs when the
  facts may have changed.

## Deliverable Shape

For API docs, provide:

- API overview and version
- Auth and permission notes
- Operation reference
- Request and response examples
- Error behavior
- Side effects and idempotency
- Validation or review notes

## References

- Read `references/api-doc-writing-checklist.md` when writing or reviewing API
  documentation.
