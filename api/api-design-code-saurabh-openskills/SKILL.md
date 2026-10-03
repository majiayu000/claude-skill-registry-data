---
name: api-design
description: Design production-grade APIs — REST, GraphQL, gRPC, and WebSocket — with a focus on consistency, versioning, error standards, and developer experience. Use when the user asks to design an API, define endpoints, choose between REST and GraphQL, structure request/response schemas, handle API versioning, design pagination, or produce an OpenAPI/Swagger spec.
---

# API Design

Approach every API as a product. The developer calling your API is your user. An API that is hard to understand, inconsistent, or unpredictable is a broken product — even if it technically works.

Design the API before writing a single line of implementation. An API is a contract. Changing it after clients depend on it is expensive. Getting it right upfront is cheap.

---

## API Design Principles

- **Spec first, implement second.** Write the OpenAPI spec, GraphQL schema, or proto file before any implementation. The spec is the contract. Implementation details are irrelevant to the caller.
- **Consistency is the most important quality.** Every endpoint in an API should behave according to the same rules: same error format, same naming convention, same pagination pattern, same auth mechanism. Inconsistency forces callers to write special-case code for every endpoint.
- **APIs are forever.** Every field you add is a field you must support until you version or sunset the API. Every field you remove is a breaking change. Design with permanence in mind.
- **Design for the caller, not the data model.** Your database schema is an implementation detail. Your API shape should reflect what callers need, not what your ORM produces.
- **Explicit over implicit.** Undefined behaviour in an API becomes the behaviour callers depend on. Make every behaviour explicit: required vs optional fields, error codes, rate limits, pagination behaviour at the end of a list.
- **Developer experience is a first-class requirement.** An API that requires a PhD to understand will not be adopted. Good error messages, consistent naming, and accurate documentation are as important as correct behaviour.

---

## Step 0: Ground the API Design

Before designing any endpoint, answer these questions:

1. **Who is the caller?** Internal service, third-party developer, mobile app, browser, CLI? Each has different needs (auth mechanism, response size, error verbosity).
2. **What resources does the API expose?** List the core domain entities the API manages.
3. **What operations does each resource support?** CRUD is not always the right decomposition — sometimes `cancel`, `approve`, `publish` are better verbs than generic CRUD.
4. **What are the read/write patterns?** High-read, low-write? Real-time? Bulk operations? Streaming? This determines the API style.
5. **What are the latency and payload size constraints?** A mobile API on a 3G connection has different constraints than a backend-to-backend integration.
6. **What versioning strategy is needed from day one?** If this API will have external consumers, versioning must be designed in before the first endpoint ships.

---

## Choosing the Right API Style

| Style | Best for | Avoid when |
|-------|----------|------------|
| **REST** | Resource-oriented APIs, public APIs, broad client compatibility, simple CRUD | Complex queries with many relationships, real-time, or highly variable response shapes |
| **GraphQL** | Flexible queries, multiple clients with different data needs, frontend-driven development, deeply nested data | Simple APIs, teams without GraphQL tooling, when over-fetching is not a real problem |
| **gRPC** | High-performance internal service communication, streaming, strongly-typed contracts, polyglot microservices | Browser clients (requires grpc-web proxy), teams unfamiliar with protobuf |
| **WebSocket** | Real-time bidirectional communication (chat, live dashboards, multiplayer) | Request-response patterns that do not need real-time; adds complexity without benefit |
| **Webhooks** | Asynchronous event notification to external systems | When the caller needs to poll or query state; use REST polling or SSE instead |

---

## REST API Design Standards

### URL Structure
```
# Pattern
/{version}/{resource}/{id}/{sub-resource}

# Examples — good
GET    /v1/users
GET    /v1/users/{userId}
GET    /v1/users/{userId}/orders
POST   /v1/users
PUT    /v1/users/{userId}
PATCH  /v1/users/{userId}
DELETE /v1/users/{userId}

# Actions that don't map to CRUD — use sub-resources
POST   /v1/orders/{orderId}/cancel
POST   /v1/invoices/{invoiceId}/send
POST   /v1/users/{userId}/password-reset
```

**URL rules:**
- Always lowercase, hyphen-separated (`user-profiles`, not `userProfiles` or `user_profiles`)
- Nouns for resources, not verbs (`/users`, not `/getUsers`)
- Plural for collections (`/users`, not `/user`)
- Version in the URL path (`/v1/`) for public APIs — query param or header for internal APIs
- Never expose database IDs directly where possible (use UUIDs or opaque string IDs)

### HTTP Methods — Correct Usage
| Method | Semantics | Idempotent | Safe |
|--------|-----------|------------|------|
| `GET` | Retrieve resource(s) | ✅ | ✅ |
| `POST` | Create a new resource or trigger an action | ❌ | ❌ |
| `PUT` | Replace a resource entirely | ✅ | ❌ |
| `PATCH` | Partially update a resource | ❌ (should be) | ❌ |
| `DELETE` | Remove a resource | ✅ | ❌ |

**Rule:** `GET` requests must never have side effects. Never use `GET` to trigger a state change.

### Request & Response Shape

**Request body — always:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "role": "admin"
}
```

**Single resource response:**
```json
{
  "id": "usr_01HXYZ",
  "name": "Jane Doe",
  "email": "jane@example.com",
  "role": "admin",
  "createdAt": "2026-01-15T10:30:00Z",
  "updatedAt": "2026-01-15T10:30:00Z"
}
```

**Collection response — always wrap in an envelope:**
```json
{
  "data": [
    { "id": "usr_01HXYZ", "name": "Jane Doe" },
    { "id": "usr_02HABC", "name": "John Smith" }
  ],
  "pagination": {
    "cursor": "eyJpZCI6InVzcl8wMkhBQkMifQ==",
    "hasMore": true,
    "total": 247
  }
}
```

**Why an envelope?** Adding metadata (pagination, request ID, warnings) to a bare array response is a breaking change. An envelope allows non-breaking additions forever.

### Naming Conventions
- Field names: `camelCase` for JSON APIs (`firstName`, not `first_name` or `FirstName`)
- Timestamps: ISO 8601 UTC (`"2026-01-15T10:30:00Z"`) — never Unix timestamps in the response body
- Booleans: positive framing (`isActive`, not `isNotActive`; `isEnabled`, not `isDisabled`)
- IDs: string type always, even if internally numeric (prevents JavaScript integer overflow)
- Money: integer cents, never floating-point (`"amount": 1999` means $19.99)
- Enums: SCREAMING_SNAKE_CASE (`"status": "IN_PROGRESS"`)

---

## Error Response Standard

Every API must have one error format used consistently across all endpoints:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Must be a valid email address"
      }
    ],
    "requestId": "req_01HXYZ123",
    "docsUrl": "https://docs.example.com/errors/VALIDATION_ERROR"
  }
}
```

**Rules:**
- `code` is a machine-readable string constant — callers switch on this, not on the HTTP status
- `message` is human-readable — never put a machine-parseable value here
- `details` is an array — multiple validation errors in one response, never force callers to fix one error at a time
- `requestId` on every error response — this is how support traces the request in logs
- `docsUrl` for each error code — link to documentation explaining the error and how to fix it

### HTTP Status Codes — Correct Usage
| Code | When to use |
|------|------------|
| `200 OK` | Successful GET, PATCH, PUT |
| `201 Created` | Successful POST that creates a resource |
| `204 No Content` | Successful DELETE or action with no response body |
| `400 Bad Request` | Validation error, malformed request |
| `401 Unauthorized` | Not authenticated |
| `403 Forbidden` | Authenticated but not authorized for this resource |
| `404 Not Found` | Resource does not exist |
| `409 Conflict` | State conflict (duplicate, version mismatch) |
| `422 Unprocessable Entity` | Semantically invalid request (valid syntax, invalid business logic) |
| `429 Too Many Requests` | Rate limit exceeded |
| `500 Internal Server Error` | Unexpected server error |
| `503 Service Unavailable` | Planned downtime or dependency unavailable |

**Never use `200` with an error body.** `{ "success": false, "error": "..." }` with a 200 status is a broken API.

---

## Pagination Patterns

### Cursor-based Pagination (recommended for most cases)
```
GET /v1/users?cursor=eyJpZCI6InVzcl8wMkhBQkMifQ==&limit=20
```
**When:** Ordered, append-heavy collections (feeds, logs, events). Stable pages even when new items are inserted.

### Offset-based Pagination (simple, but has edge cases)
```
GET /v1/products?page=3&pageSize=20
```
**When:** Admin UIs where users jump to specific pages. Avoid for large or frequently-updated datasets (items shift as pages load).

### Keyset Pagination (for high-performance sorted queries)
```
GET /v1/orders?afterId=ord_01HXYZ&limit=50
```
**When:** Database queries on an indexed column where offset queries become slow.

**Pagination response fields (always include):**
- `cursor` or `nextPage` — how to get the next page
- `hasMore` (boolean) — whether more results exist after this page
- `total` (optional) — total count (expensive on large datasets; omit if not needed)
- `limit` — the limit that was applied (echo it back)

---

## API Versioning Strategy

### URL Path Versioning (recommended for public APIs)
```
/v1/users
/v2/users
```
**Pros:** Explicit, easy to route in proxies/gateways, cacheable.
**Use for:** External/public APIs, mobile app APIs (clients pin to a version).

### Header Versioning (recommended for internal APIs)
```
API-Version: 2026-01-15
```
**Pros:** Keeps URLs clean; date-based versions are self-documenting.
**Use for:** Internal services, APIs with sophisticated clients.

### Breaking vs Non-Breaking Changes
**Non-breaking (safe to add without versioning):**
- Adding new optional fields to responses
- Adding new optional request parameters
- Adding new endpoints
- Loosening validation on existing fields

**Breaking (requires version bump):**
- Removing or renaming fields
- Changing field types
- Changing HTTP status codes
- Tightening validation
- Changing authentication requirements
- Removing endpoints

**Deprecation policy:** Mark deprecated fields with a `X-Deprecated-Fields` response header and a `deprecated` note in the OpenAPI spec. Give callers a minimum of 6 months notice before removal.

---

## OpenAPI Spec Standards

Every REST API ships with an OpenAPI 3.x spec. No exceptions.

```yaml
openapi: 3.1.0
info:
  title: User Management API
  version: 1.0.0
  description: Manages user accounts and profiles

paths:
  /v1/users/{userId}:
    get:
      summary: Get a user by ID
      operationId: getUserById
      tags: [Users]
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'
        '401':
          $ref: '#/components/responses/Unauthorized'

components:
  schemas:
    User:
      type: object
      required: [id, name, email, createdAt]
      properties:
        id:
          type: string
          example: usr_01HXYZ
        name:
          type: string
          example: Jane Doe
        email:
          type: string
          format: email
        createdAt:
          type: string
          format: date-time
```

**OpenAPI rules:**
- `operationId` on every endpoint — used for SDK generation
- `tags` on every endpoint — groups endpoints in documentation
- Every response code documented — not just 200
- `$ref` for shared schemas — no duplication
- Realistic `example` values — not `string`, `foo`, or `123`
- Security schemes defined and applied to every protected endpoint

---

## Rate Limiting

Every public API must implement rate limiting. Communicate it clearly:

**Response headers (always include on rate-limited APIs):**
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 842
X-RateLimit-Reset: 1737892800
Retry-After: 60        (only on 429 responses)
```

**Rate limit strategy:**
- Per API key / per user: prevents one caller from starving others
- Per endpoint: expensive endpoints get tighter limits than cheap ones
- Sliding window preferred over fixed window (avoids burst at window boundary)
- Return `429` with `Retry-After` header — never silently drop requests

---

## Authentication Standards

| Mechanism | Use case |
|-----------|----------|
| **Bearer JWT** | User-facing APIs, mobile/web clients |
| **API Key** (`Authorization: Bearer sk_...`) | Server-to-server, third-party integrations |
| **OAuth 2.0 + PKCE** | Third-party access on behalf of a user |
| **mTLS** | High-security internal service communication |

**Rules:**
- Always use `Authorization: Bearer <token>` header — never query parameters for auth tokens
- API keys in query parameters appear in server logs. Never.
- Short-lived access tokens (15 min – 1 hour) with refresh token rotation
- Scopes on API keys — a key should only have access to what it needs

---

## Bundled Reference

Read [openapi-review.md](./references/openapi-review.md) when reviewing or writing an OpenAPI contract. It supplements, but does not replace, the API-specific requirements in this skill.

## API Design Review Checklist

Before finalising any API design:

**Resource & URL Design**
- [ ] URLs are nouns, lowercase, hyphenated
- [ ] HTTP methods used correctly (no state-changing GETs)
- [ ] Version included in URL or header strategy defined
- [ ] IDs are string type (not integer)
- [ ] Actions not mappable to CRUD use sub-resource + POST

**Request & Response**
- [ ] Collections wrapped in an envelope object
- [ ] Consistent field naming (camelCase)
- [ ] Timestamps in ISO 8601 UTC format
- [ ] Money in integer cents, not floats
- [ ] All required fields documented

**Errors**
- [ ] Single error format used across all endpoints
- [ ] Machine-readable error codes defined
- [ ] Field-level validation errors returned in one response (not one at a time)
- [ ] Correct HTTP status codes used
- [ ] RequestId on every error response

**Pagination**
- [ ] All collection endpoints paginated (never return unbounded lists)
- [ ] Pagination strategy documented
- [ ] `hasMore` and cursor/nextPage in every paginated response

**Versioning & Breaking Changes**
- [ ] Versioning strategy defined before first endpoint ships
- [ ] Deprecation policy defined
- [ ] No breaking changes to existing endpoints without a version bump

**Security**
- [ ] Auth mechanism defined for all endpoints
- [ ] Rate limiting applied and communicated via headers
- [ ] No secrets in URLs or query parameters
- [ ] HTTPS only — no HTTP fallback

**Documentation**
- [ ] OpenAPI 3.x spec complete with all endpoints, schemas, and error responses
- [ ] Realistic examples on all request/response fields
- [ ] Authentication documented with example token format
- [ ] Rate limits documented
