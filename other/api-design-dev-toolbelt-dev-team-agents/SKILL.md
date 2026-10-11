---
name: api-design
description: REST/GraphQL design — naming, status codes, pagination, idempotency.
---

# API Design

## REST API Principles

### Resource Naming

- Use **nouns**, not verbs: `/users`, `/orders`, not `/getUsers`, `/createOrder`
- Use **plural** for collections: `/products`, `/invoices`
- Use **kebab-case** for multi-word resources: `/fuel-types`, `/gas-stations`
- Nest resources to express ownership (max 2 levels): `/users/{id}/orders`
- Avoid deep nesting — use query parameters instead: `/orders?userId=X`

### HTTP Methods

| Method | Semantics | Idempotent | Safe |
|--------|-----------|-----------|------|
| GET | Read resource(s) | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource entirely | Yes | No |
| PATCH | Partial update | No | No |
| DELETE | Remove resource | Yes | No |

### HTTP Status Codes

| Code | When to use |
|------|-------------|
| 200 OK | Successful GET, PUT, PATCH |
| 201 Created | Successful POST that created a resource |
| 204 No Content | Successful DELETE or action with no response body |
| 400 Bad Request | Invalid input, validation error |
| 401 Unauthorized | Not authenticated |
| 403 Forbidden | Authenticated but not authorized |
| 404 Not Found | Resource does not exist |
| 409 Conflict | State conflict (duplicate, optimistic lock) |
| 422 Unprocessable Entity | Syntactically valid but semantically invalid |
| 429 Too Many Requests | Rate limit exceeded |
| 500 Internal Server Error | Unexpected server failure |

### Response Envelope

All responses use a consistent envelope:

```json
{ "status": "success", "data": { ... } }
```

```json
{
  "status": "error",
  "message": "Human-readable summary",
  "code": "MACHINE_READABLE_CODE",
  "details": [
    { "field": "email", "message": "must be a valid email address" }
  ]
}
```

- `status`: `"success"` or `"error"` — always present
- `data`: payload on success; omitted on error
- `message`: human-readable description of the error
- `code`: machine-readable identifier in SCREAMING_SNAKE_CASE
- `details`: optional array of field-level validation errors

### Pagination

For list endpoints, always paginate:
```json
{
  "status": "success",
  "data": {
    "items": [...],
    "meta": {
      "total": 150,
      "per_page": 20,
      "current_page": 1,
      "last_page": 8
    }
  }
}
```

Use cursor-based pagination for large datasets or real-time feeds.

### Filtering & Sorting

Use query parameters:
```
GET /orders?status=active&sort=created_at&direction=desc
GET /products?category=fuel&min_price=10&max_price=50
```

### Versioning

Use URL prefix versioning — never header-based versioning:
```
/api/v1/users
/api/v2/users
```

- Never remove a field without a major version bump
- Deprecate with `Deprecation` and `Sunset` response headers
- Maintain at least one previous major version during deprecation cycles

### Idempotency

- `GET`, `PUT`, `DELETE` must be idempotent — repeated calls with the same payload produce the same result
- `POST` is not idempotent by default
- For payment processing and other critical operations, support the `Idempotency-Key` request header:
  - Client generates a unique key per operation attempt
  - Server stores the result and returns the same response for duplicate keys
  - Key expiry: 24 hours minimum
- Guard against duplicate `POST` submissions when relevant (e.g., order placement, account creation)

---

## API Security

- **Always use HTTPS** — no exceptions in production
- **Auth**: prefer stateless JWT (Bearer token) or OAuth 2.0; avoid session cookies for APIs
- **Rate limiting**: apply per-user and per-IP; return 429 with `Retry-After` header
- **Input validation**: validate all query params, body fields, and path params server-side
- **Never expose internal IDs** — use UUIDs or opaque external identifiers in public APIs

---

## GraphQL Schema Conventions

> When the project exposes a GraphQL API, load `skills/architecture/graphql/SKILL.md` for the full reference. The rules below are always active.

- **Schema-first**: define `.graphql` schema files before implementing resolvers
- Types use `PascalCase`: `UserProfile`, `OrderItem`
- Fields use `camelCase`: `firstName`, `totalAmount`
- Queries: descriptive names — `userById`, `activeOrders`
- Mutations: verb + noun — `createUser`, `updateOrderStatus`, `deleteProduct`
- **Mutations always return** the affected resource plus any errors — never return `Boolean` alone
- Use `input` types for mutation arguments: `CreateUserInput`, `UpdateProductInput`
- **DataLoader is mandatory** for any resolver that fetches related entities — prevents N+1 queries
- Pagination: use Relay Connection spec (`edges`, `node`, `pageInfo`)
- Errors: expose `errors` alongside `data` in mutation payloads (not via HTTP 4xx):

```graphql
type UpdateUserPayload {
  user: User
  errors: [UserError!]!
}
```

---

## Documentation Standards

Document every endpoint with:
1. **Method + Path**: `POST /api/v1/users`
2. **Description**: what it does, when to use it
3. **Auth required**: yes/no, which role/scope
4. **Request**: headers, body schema with types and required fields
5. **Response**: status codes, response schema with examples
6. **Errors**: possible error codes and their meaning

Generate OpenAPI 3.0 spec for machine-readable documentation.
