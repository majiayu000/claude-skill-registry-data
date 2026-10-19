---
name: api-design-review
description: Use when designing a new REST API, reviewing endpoints, routes, controllers or an OpenAPI/Swagger spec, choosing status codes, pagination, versioning or error formats, or checking an API change for breaking changes.
---

# API Design Review

## Overview

Judge an API from the client's side: predictable names, honest status codes, one error shape, safe retries, and no surprise breaking changes. Every finding points at a concrete route and shows the corrected design.

## Method

1. **Inventory.** List every endpoint as `METHOD /path → status codes → request/response shape`. Read routes, controllers, OpenAPI files and DTOs.
2. **Check each endpoint** against the rules below.
3. **Check the API as a whole:** consistency across endpoints matters more than any single choice.
4. **Changes:** if reviewing a diff, compare old and new contracts and flag anything that breaks existing clients.
5. **Report** using the contract below.

## Rules

| Area | Rule |
|---|---|
| Resources | Plural nouns, no verbs: `POST /orders`, not `/createOrder`. Nest only for true ownership: `/users/{id}/orders`. |
| Methods | GET reads and is safe. POST creates. PUT replaces. PATCH partially updates. DELETE removes. Never change state on GET. |
| Status codes | 200 OK, 201 Created (+ `Location`), 204 No Content, 400 invalid input, 401 not authenticated, 403 not allowed, 404 missing, 409 conflict, 422 validation, 429 rate limited, 5xx only for server faults. Never 200 with `{"error": ...}`. |
| Errors | One shape everywhere, e.g. RFC 9457: `{ "type", "title", "status", "detail", "errors": [{ "field", "message" }] }`. No stack traces or SQL in responses. |
| Naming | One casing for JSON fields (camelCase or snake_case), consistent IDs, ISO 8601 UTC timestamps, money as integer minor units or decimal string plus currency. |
| Collections | Paginate every list (cursor preferred for large or changing data), cap page size, return next cursor or links. Filtering and sorting via query params. |
| Idempotency | Retried POSTs that create payments, orders or emails accept an `Idempotency-Key`. PUT and DELETE are idempotent by design. |
| Versioning | A clear strategy (`/v1` path or header). Breaking changes go to a new version. |
| Breaking changes | Removing or renaming fields, changing types, making optional input required, changing status codes or error shape, tightening validation. |
| Security | Auth on every non-public route, object-level ownership checks, rate limits on auth and expensive routes, no sensitive data in URLs. |
| Performance | No unbounded responses, support `fields` or sparse responses for heavy objects, ETag or Cache-Control for cacheable GETs. |

## Output contract

Start with: `N endpoints reviewed, M findings (X breaking).` Then, highest impact first:

```
### [Breaking | High | Medium | Low] Title
- Endpoint: METHOD /path (file:line)
- Problem: what a client experiences
- Fix: the corrected route, status code or JSON shape
```

Finish with a short **Consistency summary** (casing, error shape, pagination, versioning: consistent or not) and, when designing from scratch, the proposed endpoint table.

## Common mistakes

- Reviewing endpoints one by one and missing that two of them disagree on casing or error shape.
- Recommending a redesign when a backward-compatible addition would do.
- Calling a change safe because the server code still works: check what existing clients send and expect.
- Using 500 for validation errors or 404 for permission failures without deciding deliberately.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
