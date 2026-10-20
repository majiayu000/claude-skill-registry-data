---
name: "api-design"
description: 'Design robust REST APIs with proper versioning, pagination, error handling, rate limiting, and documentation. Use when creating new API endpoints, designing resource naming conventions, implementing pagination or filtering, adding rate limiting, or documenting APIs with OpenAPI/Swagger.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
---

# API Design

> **Purpose**: Design robust, maintainable, and user-friendly REST APIs. 
> **Focus**: Resource naming, HTTP methods, status codes, versioning, documentation. 
> **Note**: Language-agnostic patterns applicable to any tech stack.

---

## When to Use This Skill

- Designing new REST API endpoints
- Implementing pagination, filtering, or sorting
- Adding rate limiting or CORS configuration
- Documenting APIs with OpenAPI/Swagger
- Designing webhook notification systems

## Prerequisites

- HTTP protocol fundamentals
- JSON data format understanding

## Decision Tree

```
Designing an API endpoint?
+- What operation?
| +- Read data -> GET (idempotent, cacheable)
| +- Create resource -> POST (returns 201 + Location header)
| +- Full update -> PUT (idempotent, replaces entire resource)
| +- Partial update -> PATCH (only changed fields)
| - Remove -> DELETE (idempotent, returns 204)
+- Returns collection?
| - Add pagination (cursor or offset) + filtering + sorting
+- Versioning needed?
| +- URL path versioning -> /api/v1/resources (recommended)
| - Header versioning -> Accept: application/vnd.api.v1+json
+- Error handling?
| - RFC 7807 Problem Details with proper HTTP status codes
- Security?
 +- Public? -> Rate limiting + API key
 - Private? -> OAuth2/JWT + scopes
```

## RESTful Conventions

### Resource Naming

```
[PASS] Good:
GET /api/v1/users # List users
POST /api/v1/users # Create user
GET /api/v1/users/{id} # Get specific user
PUT /api/v1/users/{id} # Update user (full)
PATCH /api/v1/users/{id} # Update user (partial)
DELETE /api/v1/users/{id} # Delete user

GET /api/v1/users/{id}/orders # Get user's orders (nested)
POST /api/v1/users/{id}/orders # Create order for user

[FAIL] Bad:
GET /api/v1/get_users
POST /api/v1/create_user
GET /api/v1/user_detail?id=123
POST /api/v1/users/delete/{id} # Use DELETE method instead
```

### Resource Naming Rules

- Use nouns, not verbs (users, not getUsers)
- Use plural form (users, not user)
- Use kebab-case for multi-word resources (order-items)
- Keep URLs lowercase
- Use nesting for relationships (users/{id}/orders)
- Limit nesting to 2 levels maximum

---

## HTTP Methods

### Standard Methods

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| **GET** | Retrieve resource(s) | Yes | Yes |
| **POST** | Create new resource | No | No |
| **PUT** | Replace entire resource | Yes | No |
| **PATCH** | Partial update | No | No |
| **DELETE** | Remove resource | Yes | No |
| **HEAD** | Get metadata only | Yes | Yes |
| **OPTIONS** | Get allowed methods | Yes | Yes |

**Idempotent**: Multiple identical requests have same effect as single request 
**Safe**: Read-only, doesn't modify server state

### Method Usage Examples

```
# GET - Retrieve
GET /api/v1/users/123
Response: 200 OK
{
 "id": 123,
 "email": "user@example.com",
 "name": "John Doe"
}

# POST - Create
POST /api/v1/users
Body: {"email": "new@example.com", "name": "New User"}
Response: 201 Created
Location: /api/v1/users/124

# PUT - Full replacement
PUT /api/v1/users/123
Body: {"email": "updated@example.com", "name": "Updated Name"}
Response: 200 OK

# PATCH - Partial update
PATCH /api/v1/users/123
Body: {"name": "New Name"} # Only updates name
Response: 200 OK

# DELETE - Remove
DELETE /api/v1/users/123
Response: 204 No Content
```

---

## HTTP Status Codes

### Success Codes (2xx)

```
200 OK # Successful GET, PUT, PATCH
201 Created # Successful POST (resource created)
202 Accepted # Request accepted, processing async
204 No Content # Successful DELETE (no response body)
```

### Client Error Codes (4xx)

```
400 Bad Request # Invalid request syntax, validation error
401 Unauthorized # Authentication required or failed
403 Forbidden # Authenticated but insufficient permissions
404 Not Found # Resource doesn't exist
405 Method Not Allowed # HTTP method not supported
409 Conflict # Resource conflict (e.g., duplicate email)
422 Unprocessable # Validation error (semantic issue)
429 Too Many Requests # Rate limit exceeded
```

### Server Error Codes (5xx)

```
500 Internal Server Error # Unhandled server error
502 Bad Gateway # Invalid response from upstream server
503 Service Unavailable # Server temporarily unavailable
504 Gateway Timeout # Upstream server timeout
```

---

## API Best Practices

### Security

- [PASS] Use HTTPS everywhere
- [PASS] Implement authentication
- [PASS] Validate all inputs
- [PASS] Rate limit requests
- [PASS] Use API keys for server-to-server
- [PASS] Implement CORS properly
- [PASS] Log security events

### Performance

- [PASS] Implement caching (ETags, Cache-Control)
- [PASS] Use compression (gzip, brotli)
- [PASS] Paginate large collections
- [PASS] Support field filtering
- [PASS] Use CDN for static content
- [PASS] Monitor API performance

### Developer Experience

- [PASS] Provide clear error messages
- [PASS] Use consistent naming
- [PASS] Version your API
- [PASS] Maintain comprehensive docs
- [PASS] Provide SDK/client libraries
- [PASS] Include examples
- [PASS] Offer sandbox environment

---

## Common API Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| **Overfetching** | Returning too much data | Support field selection |
| **Underfetching** | Requiring multiple requests | Support eager loading |
| **No versioning** | Breaking changes affect clients | Version from day one |
| **Inconsistent naming** | Hard to use | Follow naming conventions |
| **No pagination** | Performance issues | Always paginate collections |
| **Poor error messages** | Hard to debug | Return detailed errors |
| **No rate limiting** | API abuse | Implement rate limits |

---

## Resources

**API Standards:**
- [REST API Design Rulebook](https://www.oreilly.com/library/view/rest-api-design/9781449317904/)
- [JSON:API Specification](https://jsonapi.org)
- [Google API Design Guide](https://cloud.google.com/apis/design)
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)

**Tools:**
- **Documentation**: Swagger/OpenAPI, Postman, Insomnia
- **Testing**: Postman, REST Client, curl
- **Mocking**: Prism, MockServer, WireMock

---

**See Also**: [Skills.md](../../../../Skills.md) - [AGENTS.md](../../../../AGENTS.md)

**Last Updated**: January 27, 2026

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| [`scaffold-openapi.py`](scripts/scaffold-openapi.py) | Generate OpenAPI 3.1 spec from endpoint definitions | `python scripts/scaffold-openapi.py --name "My API" --endpoints "GET /users, POST /users"` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CORS errors in browser | Configure Access-Control-Allow-Origin header with specific origins, not wildcards |
| Pagination inconsistency | Use cursor-based pagination for mutable datasets, offset for static |
| Rate limit bypass attempts | Implement per-user rate limiting with token bucket algorithm |

## References

- [Api Response Patterns](references/api-response-patterns.md)
- [Api Security Patterns](references/api-security-patterns.md)
- [Api Docs Webhooks](references/api-docs-webhooks.md)