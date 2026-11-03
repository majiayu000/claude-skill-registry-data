---
name: api-design
description: Design the HTTP contract of an ASP.NET Core API before implementing it - resource naming, methods and status codes, pagination, filtering, ProblemDetails errors, versioning, rate limiting, and idempotency. Use when adding or changing endpoints, reviewing an API's shape, or deciding conventions for a new API. For implementing endpoints, OpenAPI metadata, and .http files, use the dotnet-webapi skill.
---

# API Design (ASP.NET Core)

Decide the contract first, write it down in the plan or PR, then implement it with the `dotnet-webapi` skill. Follow the conventions already in the codebase when they exist; use these defaults when they don't.

## Resources and URLs

- Plural nouns for collections, ids for items: `/orders`, `/orders/{id}`.
- Nest only for true ownership, at most one level: `/orders/{id}/items`.
- Lowercase, kebab-case path segments; camelCase JSON properties (the System.Text.Json web default).
- Actions that don't map to CRUD become sub-resources with POST: `POST /orders/{id}/cancel`.
- Route constraints on ids: `/orders/{id:guid}` or `{id:int}`.

## Methods and status codes

| Operation | Method | Success | Common failures |
|---|---|---|---|
| List | GET | 200 | 400 invalid query |
| Get one | GET | 200 | 404 |
| Create | POST | 201 + `Location` header + body | 400, 409 conflict, 422 business rule |
| Replace | PUT | 200 with body, or 204 | 400, 404, 409 |
| Partial update | PATCH | 200 with body | 400, 404, 409 |
| Delete | DELETE | 204 | 404 (or 204 if already gone, pick one and be consistent) |

- 401 when unauthenticated, 403 when authenticated but not allowed. Return 404 instead of 403 when revealing that the resource exists is itself a leak.
- Use typed results (`TypedResults.Ok`, `TypedResults.Created`, `TypedResults.NotFound`) so status codes appear in OpenAPI.

## Request and response models

- Separate request and response DTOs from EF entities; never bind or return entities directly.
- Requests contain only client-settable fields: no ids, timestamps, or computed values.
- Use `DateTimeOffset` in UTC with ISO 8601 for timestamps; decimals for money, never `double`.
- Enums as strings (`JsonStringEnumConverter`) so adding values doesn't break clients reading numbers.

## Errors

- Use `ProblemDetails` (RFC 9457) for every error: `builder.Services.AddProblemDetails()`, `TypedResults.Problem(...)`, and `TypedResults.ValidationProblem(errors)` for 400s with field errors.
- Keep `title` stable per error type; put specifics in `detail`. Add machine-readable codes as an extension (`"code": "order.cart_empty"`).
- Never return exception messages or stack traces outside Development.

## Pagination, filtering, sorting

- Every list endpoint is paginated with a maximum page size; never return an unbounded collection.
- Offset paging (`?page=2&pageSize=20`) for small, stable admin lists. Cursor paging (`?cursor=...&limit=20`) for large or frequently changing data and infinite scroll.
- Response envelope for lists: `{ "items": [...], "nextCursor": "..." }` or `{ "items": [...], "page": 2, "pageSize": 20, "totalCount": 135 }`. Only compute `totalCount` when the UI needs it; it costs a second query.
- Filters as query parameters named after response fields (`?status=paid&customerId=...`); sorting as `?sort=createdAt` / `?sort=-createdAt`, with an allowlist of sortable fields.

## Versioning

- Don't version until there is a breaking change you can't avoid. Additive changes (new optional fields, new endpoints) are not breaking.
- When needed, use `Asp.Versioning.Http` (minimal APIs) or `Asp.Versioning.Mvc` (controllers) with URL segment versioning (`/v1/orders`), and keep the previous version until clients have moved.
- Breaking: removing or renaming fields, changing types or meaning, new required request fields, changing status codes clients depend on.

## Rate limiting

- Use the built-in middleware: `builder.Services.AddRateLimiter(...)`, `app.UseRateLimiter()`, and `.RequireRateLimiting("policy")` per endpoint group.
- Set `RejectionStatusCode = StatusCodes.Status429TooManyRequests`; the default is 503.
- Partition by user id when authenticated, by client IP otherwise. Stricter policies on auth and expensive endpoints.

## Idempotency and concurrency

- GET, PUT, and DELETE must be idempotent. For POSTs that create money-moving or otherwise non-repeatable effects, accept an `Idempotency-Key` header and return the stored result on retries.
- Prevent lost updates with optimistic concurrency: an EF Core concurrency token surfaced as an `ETag`, checked via `If-Match`, returning 412 on mismatch (or 409 if not using ETags).

## Checklist before implementing

- [ ] URLs, methods, and status codes for every endpoint
- [ ] Request/response DTOs, with validation rules
- [ ] Error cases and their ProblemDetails shape
- [ ] Pagination and filters for every list
- [ ] Auth requirement per endpoint
- [ ] Breaking-change check against existing clients
