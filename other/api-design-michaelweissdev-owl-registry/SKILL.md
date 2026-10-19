---
name: api-design
description: >
  Architect intuitive, consistent, and backward-compatible RESTful and library APIs.
  Use when defining HTTP REST endpoints, standardizing JSON payloads and status codes,
  designing clean function signatures, enforcing semantic versioning on APIs,
  or writing OpenAPI / Swagger specifications.
compatibility: >
  Agent Skills-compatible coding agents designing or reviewing public library
  interfaces or REST HTTP services.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "api-design, rest, openapi, endpoints, backward-compatibility, json"
  topics: "software-development, architecture"
---

# API Design and Contract Standards

An Application Programming Interface (API) is a formal contract between service providers and consumers. Exceptional API design prioritizes consistency, predictability, backward compatibility, and developer ergonomics across both programming language libraries and HTTP REST services.

## Core Rules

1. **Be consistent in naming and casing**: In REST APIs, use plural nouns for resources (`/users`, `/orders`) and consistent JSON casing (`camelCase` or `snake_case` across all endpoints).
2. **Never break backward compatibility without versioning**: Adding optional response fields or optional query parameters is compatible; removing fields or changing data types requires a new API version (e.g. `/v2/`).
3. **Use standard HTTP methods according to RFC 9110**:
   - `GET`: Safe, idempotent retrieval. Never modifies server state.
   - `POST`: Non-idempotent creation or command execution.
   - `PUT`: Idempotent full replacement of a resource.
   - `PATCH`: Idempotent partial update of a resource.
   - `DELETE`: Idempotent deletion of a resource.
4. **Use standard HTTP status codes**: Return `200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `422 Unprocessable Entity`, `500 Internal Error`.
5. **Always provide pagination on list endpoints**: Unbounded list queries (`SELECT * FROM users`) degrade performance and cause server memory exhaustion.

---

## 1. RESTful URL Hierarchy and Resource Modeling

```http
# Collections & Items
GET    /api/v1/organizations               # List organizations (paginated)
POST   /api/v1/organizations               # Create new organization
GET    /api/v1/organizations/{org_id}      # Get single organization
PATCH  /api/v1/organizations/{org_id}      # Update organization fields
DELETE /api/v1/organizations/{org_id}      # Remove organization

# Nested Sub-Resources (Parent-Child)
GET    /api/v1/organizations/{org_id}/members    # List members within organization
POST   /api/v1/organizations/{org_id}/members    # Add member to organization

# Actions / Commands (when not modeling pure CRUD)
POST   /api/v1/invoices/{inv_id}/cancel          # State transition action
```

---

## 2. Standardized JSON Response Formats

### Successful Response Envelope
```json
{
  "data": {
    "id": "usr_9a8b7c6d",
    "email": "developer@example.com",
    "status": "ACTIVE",
    "createdAt": "2026-10-15T10:00:00Z"
  }
}
```

### Paginated Collection Response (Cursor Pagination)
```json
{
  "data": [
    { "id": "ord_001", "totalCents": 4500 },
    { "id": "ord_002", "totalCents": 1200 }
  ],
  "pagination": {
    "limit": 20,
    "hasMore": true,
    "nextCursor": "ord_002"
  }
}
```

### Standard Error Envelope (RFC 7807 Problem Details)
```json
{
  "type": "https://api.example.com/errors/validation-failed",
  "title": "Validation Failed",
  "status": 422,
  "detail": "The provided payload failed schema validation.",
  "instance": "/api/v1/users",
  "invalidParams": [
    {
      "name": "email",
      "reason": "Must be a valid email address format"
    }
  ]
}
```

---

## 3. Library API Design: Function & Method Signatures

In programming language APIs (Python, TypeScript, Go):
- **Avoid boolean flags in function calls**: `createUser("Alice", true, false, true)` is unreadable. Use keyword arguments, options objects, or enums:
  ```python
  # Unclear:
  search("python", True, False)

  # Clear:
  search("python", case_sensitive=True, include_archived=False)
  ```
- **Return sensible objects, not primitive tuples**: Return dataclasses or typed dictionaries with named fields.

---

## 4. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| `GET /deleteUser?id=5` | Modifies state via GET; triggers destructive actions on web crawler pre-fetches | Use `DELETE /api/v1/users/5` |
| Returning `200 OK` with `{"error": "Failed"}` | Confuses client libraries, monitoring, and HTTP caches | Use appropriate 4xx/5xx HTTP status codes |
| Unbounded collections (`GET /transactions`) | Server crash on memory exhaustion when data grows | Require pagination (`limit=50&cursor=...`) |
| Inconsistent pluralization (`/user` vs `/orders`) | Confusing developer experience | Always use plural nouns for collections |
| Leaking internal database IDs without obfuscation | Predictable enumeration attacks | Use UUIDv7 or prefixed IDs (`usr_...`, `inv_...`) |

---

## 5. Verification Checklist

- [ ] HTTP verbs align with standard REST semantics (GET is safe/idempotent).
- [ ] Error responses follow RFC 7807 format with correct HTTP status codes.
- [ ] All list endpoints enforce pagination limits.
- [ ] No breaking changes in minor/patch API revisions.
- [ ] OpenAPI (OAS 3.1) documentation matches real endpoint schemas.
