---
name: rest
description: REST API design principles and best practices
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: api-design
---
## What I do
- Design RESTful APIs
- Use proper HTTP methods
- Implement proper status codes
- Handle pagination and filtering
- Version APIs
- Secure endpoints

## When to use me
When building or consuming REST APIs.

## HTTP Methods
```
GET    /users        - List users
GET    /users/:id    - Get user
POST   /users        - Create user
PUT    /users/:id    - Update user (full)
PATCH  /users/:id    - Partial update
DELETE /users/:id    - Delete user
```

## Status Codes
```
200 OK
201 Created
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
500 Internal Server Error
```

## Response Format
```json
{
  "data": { "id": 1, "name": "John" },
  "meta": { "total": 100, "page": 1 },
  "links": { "self": "/users/1" }
}
```
