---
name: api-design
description: Design clean REST/JSON APIs — resources, status codes, errors, versioning, pagination.
trigger: when the user designs or reviews an HTTP API, endpoints, or request/response shapes
---
## When to use
The user is designing endpoints or asks for a review of an API surface.

## How
1. Resources are plural nouns (`/users/{id}/orders`); verbs live in the HTTP
   method, not the path. Actions that fit no resource → `POST /…/actions`.
2. Status codes that mean what they say: 200/201/204 success; 400 malformed,
   401 unauthenticated, 403 forbidden, 404 missing, 409 conflict,
   422 validation; 5xx only for server faults.
3. One error envelope everywhere:
   `{"error": {"code": "machine_readable", "message": "human readable", "details": [...]}}`.
4. Pagination on every list endpoint from day one (cursor preferred:
   `?cursor=…&limit=…` → `{"items": [...], "next_cursor": …}`).
5. Version in the path (`/v1/`) — and don't break v1 once published.
6. Request/response field naming consistent (pick snake_case or camelCase,
   never both). Timestamps ISO-8601 UTC.
7. Idempotency: PUT/DELETE naturally; POST that charges/creates externally →
   accept an `Idempotency-Key` header.

## Avoid
- 200 with `{"success": false}` — that's a 4xx/5xx.
- Unbounded list responses.
- Leaking internals (DB ids/stack traces) in error messages.

## Done well
A consumer can predict every endpoint's shape from one example; errors are
actionable; nothing breaks when you add fields later.
