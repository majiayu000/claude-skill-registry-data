---
name: api-design-patterns
description: REST API design patterns including versioning strategies (URL, header, content negotiation), pagination (offset, cursor, keyset), filtering and sorting, error response formats (RFC 7807), authentication (JWT, OAuth 2.0, API keys), rate limiting, and OpenAPI specification. Use when designing APIs, documenting endpoints, implementing authentication, standardizing error responses, or reviewing API implementations.
allowed-tools:
  - Read
  - Write
  - Grep
---

# API Design Patterns

**Purpose:** Comprehensive REST API design patterns for building consistent, scalable, and maintainable APIs.

**When to use:** Designing new APIs, documenting endpoints, implementing authentication/authorization, standardizing error responses, reviewing API implementations, or troubleshooting API issues.

**For detailed examples, OpenAPI specs, and implementation guides:** See reference.md

---

## Core Principles

1. **Resources over actions** - Use nouns not verbs in URLs
2. **Standard HTTP methods** - GET/POST/PUT/PATCH/DELETE with correct semantics
3. **Predictable structure** - Consistent patterns across all endpoints
4. **Client-friendly errors** - Clear, actionable error messages
5. **Versioning from day one** - APIs evolve, plan for it
6. **Security by default** - Authentication and authorization required

---

## REST Fundamentals

### Resource Design

**Resources are nouns, not verbs:**

| Pattern | Example | Status |
|---------|---------|--------|
| ✅ Good | `GET /users`, `POST /orders` | Use nouns |
| ❌ Bad | `GET /getUsers`, `POST /createOrder` | Avoid verbs |

**Hierarchy reflects relationships:**
```
/users                          # Collection
/users/{id}                     # Single resource
/users/{id}/orders              # Nested collection
/users/{id}/orders/{orderId}    # Nested resource
```

**Naming conventions:**
- Plural nouns: `/users`, `/orders`, `/products`
- Lowercase with hyphens: `/user-profiles` not `/userProfiles`
- Keep shallow (max 3 levels)

---

## HTTP Methods & Status Codes

### Method Semantics

| Method | Purpose | Idempotent | Safe | Example |
|--------|---------|------------|------|---------|
| **GET** | Retrieve resource(s) | Yes | Yes | `GET /users/123` |
| **POST** | Create resource | No | No | `POST /users` |
| **PUT** | Replace resource | Yes | No | `PUT /users/123` |
| **PATCH** | Update resource | No | No | `PATCH /users/123` |
| **DELETE** | Delete resource | Yes | No | `DELETE /users/123` |

**Idempotent:** Multiple identical requests have same effect
**Safe:** No side effects, read-only

### Status Codes Reference

| Code | Meaning | Use When |
|------|---------|----------|
| **2xx Success** | | |
| 200 OK | Success (with body) | GET, PUT, PATCH success |
| 201 Created | Resource created | POST success, return Location header |
| 204 No Content | Success (no body) | DELETE success |
| **4xx Client Errors** | | |
| 400 Bad Request | Invalid syntax/data | Validation errors, malformed JSON |
| 401 Unauthorized | Missing/invalid auth | No token, expired token |
| 403 Forbidden | Insufficient permissions | Valid auth but not authorized |
| 404 Not Found | Resource doesn't exist | Invalid ID, deleted resource |
| 409 Conflict | Resource state conflict | Duplicate email, version mismatch |
| 422 Unprocessable Entity | Semantic errors | Valid JSON but business rule violation |
| 429 Too Many Requests | Rate limit exceeded | Client exceeded rate limit |
| **5xx Server Errors** | | |
| 500 Internal Server Error | Unexpected error | Uncaught exceptions |
| 503 Service Unavailable | Temporarily down | Maintenance, overloaded |

**For complete status code reference:** See reference.md

---

## API Versioning

### Versioning Strategies Comparison

| Strategy | Example | Pros | Cons | Use When |
|----------|---------|------|------|----------|
| **URL Path** | `/v1/users` | Simple, visible, cacheable | URL changes | Public APIs |
| **Header** | `Accept: vnd.api.v1+json` | Clean URLs | Hidden complexity | Enterprise APIs |
| **Query Param** | `/users?version=1` | Optional versioning | Less discoverable | Internal APIs |

### URL Versioning (Recommended)

```
GET /v1/users
GET /v2/users
```

**Rules:**
- Major version only (v1, v2, v3)
- Breaking changes require new version
- Support N-1 versions (current + previous)

**Breaking changes:**
- Removing endpoints or fields
- Changing field types or validation
- Changing authentication requirements

**Non-breaking changes (same version):**
- Adding endpoints or optional fields
- Adding response fields
- Relaxing validation

**For version deprecation headers and examples:** See reference.md

---

## Pagination

### Pagination Strategies Comparison

| Strategy | Best For | Pros | Cons |
|----------|----------|------|------|
| **Offset** | Small datasets (<10K), user-facing pages | Simple, page numbers | Slow for large offsets, duplicates if data changes |
| **Cursor** | Large datasets, feeds/timelines | Fast, consistent | Opaque tokens, can't jump to page |
| **Keyset** | Large datasets, stable ordering | Fast, consistent, transparent | Requires indexed field, complex queries |

### Offset Pagination

```http
GET /users?limit=20&offset=40

Response:
{
  "data": [...],
  "pagination": {
    "limit": 20,
    "offset": 40,
    "total": 1000
  }
}
```

### Cursor Pagination (Recommended)

```http
GET /users?limit=20&cursor=eyJpZCI6MTIzfQ==

Response:
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTQzfQ==",
    "has_more": true
  }
}
```

**Benefits:** Fast, consistent results, works with real-time data

**For cursor encoding and keyset pagination:** See reference.md

---

## Filtering & Sorting

```http
# Simple filtering
GET /users?status=active&role=admin

# Multiple values (OR)
GET /users?status=active,pending

# Range filtering
GET /orders?min_amount=100&max_amount=500

# Sorting
GET /users?sort=created_at              # Ascending
GET /users?sort=-created_at             # Descending (- prefix)
GET /users?sort=last_name,first_name    # Multiple fields

# Combined
GET /users?status=active&sort=-created_at&limit=20
```

### Advanced Filtering (LHS Brackets)

```http
GET /products?price[gte]=100&price[lte]=500
GET /users?tags[in]=admin,moderator
GET /articles?title[contains]=design
```

**Operators:** `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `in`, `nin`, `contains`, `startsWith`

---

## Error Response Format

### RFC 7807 Problem Details (Recommended)

```json
{
  "type": "https://api.example.com/errors/validation-failed",
  "title": "Validation Failed",
  "status": 400,
  "detail": "One or more fields failed validation",
  "instance": "/users",
  "errors": [
    {
      "field": "email",
      "message": "Email address is already in use",
      "code": "EMAIL_DUPLICATE"
    }
  ],
  "trace_id": "abc123-def456-ghi789"
}
```

### Error Response Fields

| Field | Required | Description |
|-------|----------|-------------|
| `type` | Yes | URI identifying error type (documentation link) |
| `title` | Yes | Human-readable summary |
| `status` | Yes | HTTP status code |
| `detail` | No | Specific explanation |
| `instance` | No | Request path or trace ID |
| `errors` | No | Field-specific errors |
| `trace_id` | No | Internal trace ID |

**Response headers:**
```http
HTTP/1.1 400 Bad Request
Content-Type: application/problem+json
```

**For error examples by status code:** See reference.md

---

## Authentication & Authorization

### Authentication Patterns Comparison

| Pattern | Use Case | Stateless | Pros | Cons |
|---------|----------|-----------|------|------|
| **JWT** | Microservices, SPAs | Yes | Scalable, no DB lookup | Can't revoke before expiry |
| **OAuth 2.0** | Third-party access | No | Industry standard, granular scopes | Complex setup |
| **API Keys** | Server-to-server | Yes | Simple | Less secure, no user context |

### JWT Authentication (Recommended)

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Token endpoint:**
```http
POST /auth/token
{
  "username": "user@example.com",
  "password": "secret"
}

Response:
{
  "access_token": "eyJhbGc...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "def50200..."
}
```

**Best practices:**
- Short-lived access tokens (15-60 min)
- Long-lived refresh tokens (7-30 days)
- Minimal claims (sub, role, exp, iat)
- Strong algorithm (RS256 or HS256)

### OAuth 2.0 Flow

```
1. Client → Auth server: authorization request
2. User grants permission
3. Auth server → Client: authorization code
4. Client → Auth server: exchange code for token
5. Auth server → Client: access token + refresh token
```

**Scopes:**
```
read:users       # Read user data
write:users      # Create/update users
admin:*          # Full admin access
```

### API Keys (Server-to-Server)

```http
X-API-Key: sk_live_51H2xPqF3...
```

**Best practices:**
- Prefix by environment: `sk_test_`, `sk_live_`
- Hash in database
- Support key rotation
- Scope to specific permissions

**For detailed OAuth flow, key management, and authorization patterns:** See reference.md

---

## Rate Limiting

### Rate Limit Headers

```http
# Standard headers (RateLimit Policy Draft)
HTTP/1.1 200 OK
RateLimit-Limit: 100
RateLimit-Remaining: 75
RateLimit-Reset: 1640000000

# After limit hit
HTTP/1.1 429 Too Many Requests
RateLimit-Remaining: 0
Retry-After: 60
```

### Rate Limiting Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| **Fixed Window** | Count per fixed time window | Simple, allows 2x burst at edge |
| **Sliding Window** | Rolling time window | Smooth rate limiting |
| **Token Bucket** | Tokens refill, burst allowed | Variable load |
| **Leaky Bucket** | Constant rate, excess rejected | Strict rate limiting |

**Rate limit tiers:**
```
Free:        100 requests/hour
Basic:       1,000 requests/hour
Premium:     10,000 requests/hour
Enterprise:  Custom limits
```

---

## OpenAPI Specification

**Use for:** API documentation, client generation, validation

**Basic structure:**
```yaml
openapi: 3.0.3
info:
  title: User API
  version: 1.0.0

paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
          format: email

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - BearerAuth: []
```

**Tools:**
- Swagger UI: Interactive docs
- Redoc: Clean, responsive docs
- OpenAPI Generator: Generate clients/servers

**For complete OpenAPI examples:** See reference.md

---

## Quick Reference Checklist

**Designing new API:**
- [ ] Version from day one (URL path recommended)
- [ ] Use nouns for resources, plural names
- [ ] Standard HTTP methods (GET/POST/PUT/PATCH/DELETE)
- [ ] Pagination for collections (cursor recommended)
- [ ] Filtering and sorting via query params
- [ ] RFC 7807 error responses
- [ ] Authentication (JWT recommended)
- [ ] Rate limiting with standard headers
- [ ] OpenAPI specification

**Endpoint design:**
- [ ] Resource naming follows conventions
- [ ] Correct HTTP method and status codes
- [ ] Request validation with clear errors
- [ ] Consistent response structure
- [ ] Security headers (CORS, CSP)
- [ ] ETag/Last-Modified for caching

**Documentation:**
- [ ] OpenAPI spec complete
- [ ] Authentication flow documented
- [ ] Rate limits documented
- [ ] Error responses documented
- [ ] Example requests/responses

---

## Common Patterns Summary

```http
# List with pagination
GET /v1/users?limit=20&cursor=abc123

# Filter and sort
GET /v1/products?category=electronics&status=active&sort=-price

# Create
POST /v1/users
Authorization: Bearer <token>

# Update (partial)
PATCH /v1/users/123
Authorization: Bearer <token>

# Delete
DELETE /v1/users/123
Authorization: Bearer <token>

# Nested resources
GET /v1/users/123/orders

# Search
GET /v1/users?q=john&fields=name,email

# Batch operations
POST /v1/users/batch
{
  "operations": [
    {"op": "create", "data": {...}},
    {"op": "update", "id": 123, "data": {...}}
  ]
}
```

---

**For detailed examples, complete OpenAPI specs, implementation guides, and language-specific patterns:** See reference.md
