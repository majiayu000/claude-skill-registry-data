---
name: api-design
description: REST and GraphQL API design patterns, best practices, and conventions. Use when designing APIs, discussing HTTP methods, status codes, versioning, or API documentation. Triggers on mentions of REST, API, GraphQL, endpoint, HTTP methods, OpenAPI, swagger, API versioning.
---

# API Design Best Practices

## REST Fundamentals

### Resource Naming
```
# Good - nouns, plural, lowercase
GET    /users
GET    /users/{id}
POST   /users
PUT    /users/{id}
DELETE /users/{id}

# Nested resources
GET    /users/{id}/orders
POST   /users/{id}/orders

# Bad
GET    /getUsers
POST   /createUser
GET    /user_list
```

### HTTP Methods
| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Retrieve resource | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Partial update | No | No |
| DELETE | Remove resource | Yes | No |

### Status Codes
```
# Success
200 OK              - Successful GET, PUT, PATCH
201 Created         - Successful POST
204 No Content      - Successful DELETE

# Client Errors
400 Bad Request     - Invalid input
401 Unauthorized    - Authentication required
403 Forbidden       - Authenticated but not allowed
404 Not Found       - Resource doesn't exist
409 Conflict        - Resource state conflict
422 Unprocessable   - Validation failed

# Server Errors
500 Internal Error  - Unexpected server error
502 Bad Gateway     - Upstream service error
503 Unavailable     - Service temporarily unavailable
```

## Request/Response Design

### Request Format
```json
POST /users
Content-Type: application/json

{
  "name": "Alice",
  "email": "alice@example.com",
  "role": "admin"
}
```

### Response Format
```json
{
  "data": {
    "id": "user_123",
    "name": "Alice",
    "email": "alice@example.com",
    "role": "admin",
    "createdAt": "2024-01-15T10:30:00Z"
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
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

## Pagination

### Offset-based
```
GET /users?offset=20&limit=10

{
  "data": [...],
  "pagination": {
    "total": 100,
    "offset": 20,
    "limit": 10
  }
}
```

### Cursor-based (Preferred)
```
GET /users?cursor=abc123&limit=10

{
  "data": [...],
  "pagination": {
    "nextCursor": "xyz789",
    "hasMore": true
  }
}
```

## Filtering and Sorting

### Query Parameters
```
# Filtering
GET /users?status=active&role=admin

# Sorting
GET /users?sort=createdAt:desc

# Multiple sorts
GET /users?sort=role:asc,name:asc

# Field selection
GET /users?fields=id,name,email
```

### Search
```
GET /users?q=alice
GET /products?search=laptop&category=electronics
```

## Versioning

### URL Path (Recommended)
```
/v1/users
/v2/users
```

### Header
```
GET /users
Accept: application/vnd.api+json; version=1
```

### Query Parameter
```
GET /users?version=1
```

## Authentication

### Bearer Token
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### API Key
```
X-API-Key: your-api-key
# Or in query (less secure)
?api_key=your-api-key
```

## Rate Limiting

### Response Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

### 429 Response
```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests",
    "retryAfter": 60
  }
}
```

## GraphQL Patterns

### Schema Design
```graphql
type User {
  id: ID!
  name: String!
  email: String!
  orders(first: Int, after: String): OrderConnection!
}

type Order {
  id: ID!
  total: Float!
  status: OrderStatus!
  user: User!
}

enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
}
```

### Queries
```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    orders(first: 10) {
      edges {
        node {
          id
          total
        }
      }
    }
  }
}
```

### Mutations
```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    user {
      id
      name
    }
    errors {
      field
      message
    }
  }
}
```

## Documentation

### OpenAPI/Swagger
```yaml
openapi: 3.0.0
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
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
```

## HATEOAS

### Links in Response
```json
{
  "data": {
    "id": "user_123",
    "name": "Alice"
  },
  "links": {
    "self": "/users/user_123",
    "orders": "/users/user_123/orders",
    "profile": "/users/user_123/profile"
  }
}
```

## Best Practices

### Consistency
- Use consistent naming (camelCase or snake_case)
- Consistent error format across all endpoints
- Consistent pagination format

### Security
- Always use HTTPS
- Validate all input
- Don't expose internal IDs
- Rate limit all endpoints
- Use appropriate authentication

### Performance
- Support compression (gzip)
- Cache with ETags
- Allow field selection
- Implement pagination

## Anti-Patterns to Avoid

- Verbs in URLs (`/getUser`)
- Returning 200 for errors
- Inconsistent response formats
- Missing pagination
- Exposing database IDs
- No versioning strategy
- Missing rate limiting
- Chatty APIs (many small calls)
