---
name: api-contract-design
description: Contract-first API development — error semantics, status codes, request/response design, OpenAPI/Swagger standards. Prevents inconsistent APIs and breaking changes without migration paths.
---

# API Contract Design

## Problem it solves

APIs built without contracts develop inconsistencies and breaking changes:
- Inconsistent error formats (sometimes string, sometimes object, sometimes nothing)
- Missing status codes (everything returns 200 with errors in the body)
- Breaking changes without version bumps or migration paths
- Undocumented endpoints that only the author understands
- Inconsistent naming (sometimes camelCase, sometimes snake_case)
- No request validation — bad input causes 500s instead of 400s

## Protocol

### 1. Contract-first design

Before writing any API implementation, define the contract:
- Operations: what endpoints exist and what do they do
- Requests: what input does each endpoint accept (path params, query params, body)
- Responses: what does each endpoint return (success and error shapes)
- Status codes: what HTTP status codes are used for each outcome
- Error format: a consistent error structure across all endpoints

### 2. HTTP status code conventions

| Code | When to use |
|------|-------------|
| 200 OK | Successful GET, PUT, PATCH |
| 201 Created | Successful POST (resource created) |
| 204 No Content | Successful DELETE |
| 400 Bad Request | Invalid input, missing required fields, validation failure |
| 401 Unauthorized | Missing or invalid authentication |
| 403 Forbidden | Authenticated but not authorized |
| 404 Not Found | Resource does not exist |
| 409 Conflict | Resource state conflict (duplicate, stale version) |
| 422 Unprocessable | Semantic validation failure (business rule violation) |
| 429 Too Many Requests | Rate limit exceeded |
| 500 Internal Server | Unexpected server error (do not expose details) |

### 3. Error response format

Every error response should follow a consistent structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "A human-readable description",
    "details": [
      { "field": "email", "reason": "must be a valid email address" }
    ]
  }
}
```

### 4. API versioning

- Use URL-based versioning (`/v1/`, `/v2/`) or header-based (Accept header)
- Never remove or modify existing fields in a version
- Adding a field is safe (consumers ignore unknown fields)
- Changing a field or removing one requires a new version
- Deprecate before removing: add `Deprecation` header, keep old version for N months

### 5. Request/Response design rules

- **Use standard HTTP methods**: GET (read), POST (create), PUT (replace), PATCH (partial update), DELETE (remove)
- **Use standard content types**: `application/json` for REST APIs
- **Pagination**: Always paginate list endpoints. Return `{ data: [...], next: "url" }` or `{ data: [...], total, page, size }`
- **Filtering/Sorting**: Use query parameters (`?status=active&sort=name:asc`)
- **Idempotency**: PUT and DELETE should be idempotent. POST should return 201 with Location header
- **Naming**: Use plural nouns for resources (`/users`, not `/user`). Use kebab-case for paths (`/user-profiles`)

### 6. OpenAPI/Swagger

- Document every endpoint with OpenAPI 3.x
- Include request/response schemas, examples, and error responses
- Keep the spec in version control alongside the code
- Generate client libraries and server stubs from the spec when possible

## Detection triggers

Activate when:
- Designing or implementing an API endpoint
- Modifying an existing API contract
- Adding request/response handling
- User says "design API", "create endpoint", "build REST API"
- Reviewing API changes in a PR

## When NOT to use

- Internal function/method signatures (use spec-driven-development)
- GraphQL APIs (schema-first with different conventions)
- RPC or event-driven architectures
- User explicitly says "no contract needed"

## Cross-references

- **spec-driven-development** — Write the API contract as part of the spec before implementation.

- **test-driven-development** — Test the API contract (request/response shapes, status codes, error formats) before implementation.

- **code-review** — The architecture axis should verify API contracts follow these conventions.

- **adr-and-documentation** — API contract changes should be documented in ADRs. OpenAPI specs are living documentation.

- **security-best-practices** — API security (auth, rate limiting, input validation) should be designed into the contract, not added later.

- **follow-existing-patterns** — API contracts must match the project's existing API conventions (naming, versioning, error format).

- **git-workflow-conventional-commits** — Breaking API changes should be clearly marked with BREAKING CHANGE footer.
