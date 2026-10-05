---
name: api-design
description: Design clean, consistent, and well-documented APIs using contract-first principles. Use for REST API design, endpoint naming, request/response modeling, error handling patterns, versioning strategies, OpenAPI specification writing, and API documentation.
---

# API Design

Design APIs that are intuitive, consistent, and maintainable.

## Design-First Workflow

1. **Define the contract** (OpenAPI spec) before writing code
2. **Review with consumers** (even if that's just future-you)
3. **Generate server stubs** from the spec
4. **Implement** against the contract
5. **Validate** responses match the spec

## REST Fundamentals

### Resource Naming
```
# Use nouns, not verbs
GET  /users          ✓
GET  /getUsers       ✗

# Plural for collections
GET  /users          ✓
GET  /user           ✗

# Nested for relationships
GET  /users/123/orders
POST /users/123/orders

# Use kebab-case for multi-word
GET  /user-profiles  ✓
GET  /userProfiles   ✗
```

### HTTP Methods
| Method | Purpose | Idempotent | Request Body |
|--------|---------|------------|--------------|
| GET | Read resource(s) | Yes | No |
| POST | Create resource | No | Yes |
| PUT | Replace resource | Yes | Yes |
| PATCH | Partial update | Yes | Yes |
| DELETE | Remove resource | Yes | No |

### Status Codes
```
2xx Success
  200 OK              - General success
  201 Created         - Resource created (return Location header)
  204 No Content      - Success, no body (DELETE)

4xx Client Error
  400 Bad Request     - Malformed request, validation error
  401 Unauthorized    - No/invalid authentication
  403 Forbidden       - Authenticated but not authorized
  404 Not Found       - Resource doesn't exist
  409 Conflict        - State conflict (duplicate, version mismatch)
  422 Unprocessable   - Valid syntax, invalid semantics

5xx Server Error
  500 Internal Error  - Unexpected server failure
  503 Unavailable     - Temporary overload/maintenance
```

## Request/Response Patterns

### Consistent Response Envelope
```json
// Success
{
  "data": { ... },
  "meta": {
    "page": 1,
    "total": 100
  }
}

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [
      { "field": "email", "issue": "must be valid email" }
    ]
  }
}
```

### Pagination
```
# Offset-based (simple, has issues at scale)
GET /users?page=2&limit=20

# Cursor-based (preferred for large datasets)
GET /users?cursor=abc123&limit=20

Response includes:
{
  "data": [...],
  "meta": {
    "next_cursor": "def456",
    "has_more": true
  }
}
```

### Filtering and Sorting
```
# Filtering
GET /users?status=active&role=admin

# Sorting
GET /users?sort=created_at:desc,name:asc

# Field selection (sparse fieldsets)
GET /users?fields=id,name,email
```

## Error Handling

### Error Response Structure
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User with ID 123 not found",
    "request_id": "req_abc123",
    "documentation_url": "https://api.example.com/docs/errors#RESOURCE_NOT_FOUND"
  }
}
```

### Error Code Standards
Use consistent, machine-readable codes:
```
VALIDATION_ERROR      - Request validation failed
AUTHENTICATION_ERROR  - Auth token missing/invalid
AUTHORIZATION_ERROR   - Insufficient permissions
RESOURCE_NOT_FOUND    - Entity doesn't exist
CONFLICT              - State conflict
RATE_LIMITED          - Too many requests
INTERNAL_ERROR        - Server-side failure
```

### Validation Errors
Return specific field-level details:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      { "field": "email", "code": "INVALID_FORMAT", "message": "Must be valid email" },
      { "field": "age", "code": "OUT_OF_RANGE", "message": "Must be 18 or older" }
    ]
  }
}
```

## Versioning

### Strategies
```
# URL path (most common, explicit)
/v1/users
/v2/users

# Header (cleaner URLs, less discoverable)
Accept: application/vnd.api+json; version=1

# Query param (easy to test, pollutes caching)
/users?version=1
```

### Versioning Policy
- Bump major version only for breaking changes
- Breaking: removing fields, changing types, new required params
- Non-breaking: adding optional fields, new endpoints
- Support N-1 version minimum, deprecate with timeline

## OpenAPI Specification

### Basic Structure
```yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0
  description: API for managing users

servers:
  - url: https://api.example.com/v1

paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'

components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
```

### Documentation Tips
- Write descriptions for every endpoint and parameter
- Include realistic examples in schemas
- Document all possible error responses
- Use `operationId` for code generation

## API Design Checklist

Before finalizing an API:
- [ ] Resources named as nouns, plural
- [ ] Consistent response structure
- [ ] All error cases documented with codes
- [ ] Pagination for list endpoints
- [ ] Idempotency keys for non-idempotent operations
- [ ] Rate limiting headers documented
- [ ] Authentication method specified
- [ ] Versioning strategy defined
- [ ] OpenAPI spec validates
