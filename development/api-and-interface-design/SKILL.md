---
name: api-and-interface-design
description: >
  Design and implement clean, consistent, well-documented APIs and
  interfaces. Use when building REST APIs, GraphQL schemas, library
  interfaces, or internal module boundaries.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
  - shell.exec
triggers:
  - context: "designing an API"
  - context: "building REST endpoints"
  - context: "defining interfaces or contracts"
  - command: "/build"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
dependencies:
  - test-driven-development@^1.0.0
  - security-and-hardening@^1.0.0
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
  gemini:
    enforcement_style: "structured-checklist"
  gpt:
    enforcement_style: "directive-imperative"
author: codehands-core
signed: true
tier: 2
---

## Overview

APIs are contracts. Once published, they're promises to consumers. This skill covers designing APIs that are consistent, predictable, and evolvable — whether REST endpoints, GraphQL schemas, or internal module interfaces.

## When to Use

- When building REST API endpoints
- When designing GraphQL schemas
- When defining library public interfaces
- When establishing internal module boundaries
- NOT for private implementation details

## Process

### 1. Resource-First Design (REST)

Design around resources (nouns), not actions (verbs):

```
GOOD: GET /users/123       → Fetch user
      POST /users          → Create user
      PATCH /users/123     → Update user
      DELETE /users/123    → Delete user

BAD:  POST /getUser        → Verb in URL
      POST /createUser     → Action-based
```

### 2. Consistent Response Format

```json
{
  "data": { ... },
  "meta": { "page": 1, "total": 42, "limit": 10 },
  "errors": [{ "code": "VALIDATION_ERROR", "field": "email", "message": "Invalid email" }]
}
```

- Always wrap in `data` key (consistent parsing)
- Pagination metadata in `meta`
- Errors as array with code, field, and human-readable message

### 3. HTTP Status Codes

| Code | When |
|---|---|
| 200 | Success (GET, PATCH) |
| 201 | Created (POST) |
| 204 | No Content (DELETE) |
| 400 | Bad Request (validation errors) |
| 401 | Unauthorized (not authenticated) |
| 403 | Forbidden (authenticated but not authorized) |
| 404 | Not Found |
| 409 | Conflict (duplicate resource) |
| 422 | Unprocessable Entity (semantic validation) |
| 429 | Too Many Requests (rate limited) |
| 500 | Internal Server Error (unexpected) |

### 4. Versioning

- URL versioning: `/api/v1/users` (simplest, most explicit)
- Header versioning: `Accept: application/vnd.api+json;version=1` (more flexible)
- Pick one strategy and use it consistently

### 5. Error Handling

Errors must be:
- **Machine-readable** — Error code for programmatic handling
- **Human-readable** — Message for debugging
- **Specific** — Which field failed, why

### 6. Rate Limiting & Pagination

- Rate limit ALL endpoints (especially auth)
- Return rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`
- Paginate ALL list endpoints (no unbounded queries)
- Cursor-based pagination for large datasets

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "We won't need versioning" | You will. The cost of adding versioning later is breaking all existing consumers. Add it now. |
| "Error codes are overkill" | Without codes, clients parse error messages as strings — fragile. Codes are the contract. |
| "We don't need pagination for small datasets" | Datasets grow. Add pagination from day one. It's trivial and prevents future catastrophe. |

## Red Flags

- Verbs in URL paths (`/createUser`)
- Inconsistent response format across endpoints
- 200 status code for errors
- No pagination on list endpoints
- No rate limiting on auth endpoints

## Verification

- [ ] Resource-based URL design (nouns, not verbs)
- [ ] Consistent response format across all endpoints
- [ ] Correct HTTP status codes for all responses
- [ ] Pagination on all list endpoints
- [ ] Rate limiting on sensitive endpoints
- [ ] API versioning strategy implemented
- [ ] Error responses include code, field, and message

## See Also

- `codehands:security-and-hardening` — API security (auth, rate limiting, CORS)
- `codehands:test-driven-development` — API contract tests
- `codehands:documentation-and-adrs` — API documentation (OpenAPI/Swagger)
