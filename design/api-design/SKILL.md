---
name: api-design
description: RESTful API design principles, patterns, and best practices. Use when building backend APIs. (project)
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# API Design Principles

## REST Conventions

### HTTP Methods
| Method | Purpose | Idempotent |
|--------|---------|------------|
| GET | Retrieve resource(s) | Yes |
| POST | Create new resource | No |
| PUT | Replace entire resource | Yes |
| PATCH | Partial update | Yes |
| DELETE | Remove resource | Yes |

### URL Structure
```
GET    /api/v1/users           # List all users
GET    /api/v1/users/:id       # Get single user
POST   /api/v1/users           # Create user
PUT    /api/v1/users/:id       # Replace user
PATCH  /api/v1/users/:id       # Update user
DELETE /api/v1/users/:id       # Delete user

# Nested resources
GET    /api/v1/users/:id/posts # User's posts
```

## Response Format

### Success Response
```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

### Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  }
}
```

## HTTP Status Codes

### Success (2xx)
- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE

### Client Errors (4xx)
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource doesn't exist
- `409 Conflict` - Resource conflict
- `422 Unprocessable Entity` - Validation failed

### Server Errors (5xx)
- `500 Internal Server Error` - Unexpected error
- `503 Service Unavailable` - Temporary unavailable

## Pagination

### Offset-based
```
GET /api/v1/users?page=2&limit=20
```

### Cursor-based
```
GET /api/v1/users?cursor=abc123&limit=20
```

## Filtering & Sorting

```
GET /api/v1/users?status=active&role=admin
GET /api/v1/users?sort=-created_at,name
GET /api/v1/users?fields=id,name,email
```

## Authentication

### JWT Token
```
Authorization: Bearer <token>
```

### API Key
```
X-API-Key: <api-key>
```

## Versioning

### URL Path (Recommended)
```
/api/v1/users
/api/v2/users
```

### Header
```
Accept: application/vnd.api+json; version=1
```

## Rate Limiting Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```
