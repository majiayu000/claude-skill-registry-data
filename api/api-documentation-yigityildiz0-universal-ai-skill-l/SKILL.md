---
name: api-documentation
description: Create OpenAPI/Swagger specifications, API reference documentation, endpoint descriptions, and usage examples. Use when documenting REST APIs, GraphQL.
---

# API Documentation

Create complete, accurate API documentation that enables developers to quickly understand and successfully integrate with your API.

## When to Use This Skill

Use this skill when you need to:

- Document REST API endpoints
- Create OpenAPI/Swagger specifications
- Write API reference documentation
- Document GraphQL schemas
- Add request/response examples
- Document authentication flows

**Trigger phrases**: "API documentation", "OpenAPI spec", "Swagger", "endpoint documentation", "API reference", "REST docs"

## What This Skill Does

### Documentation Components

1. **OpenAPI Specification** - Machine-readable API definition
2. **Endpoint Reference** - Complete endpoint documentation
3. **Authentication Guide** - Auth flows and examples
4. **Error Reference** - Error codes and handling
5. **Code Examples** - Working examples in multiple languages
6. **Rate Limiting** - Usage limits and best practices

## Instructions

### OpenAPI 3.0 Specification

```yaml
openapi: 3.0.3
info:
  title: User Management API
  description: |
    API for managing users, authentication, and profiles.

    ## Authentication
    All endpoints require Bearer token authentication.
    Obtain tokens via `/auth/login`.

    ## Rate Limiting
    - Standard: 100 requests/minute
    - Authenticated: 1000 requests/minute
  version: 1.0.0
  contact:
    name: API Support
    email: api-support@example.com
    url: https://example.com/support
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging
  - url: http://localhost:8000/v1
    description: Development

tags:
  - name: Authentication
    description: User authentication and token management
  - name: Users
    description: User CRUD operations
  - name: Profiles
    description: User profile management

paths:
  /auth/login:
    post:
      tags:
        - Authentication
      summary: Authenticate user
      description: |
        Authenticate with email and password to receive access token.
        Tokens expire after 24 hours.
      operationId: login
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginRequest'
            example:
              email: user@example.com
              password: securePassword123
      responses:
        '200':
          description: Authentication successful
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthResponse'
              example:
                token: eyJhbGciOiJIUzI1NiIs...
                expires_at: "2025-01-16T10:30:00Z"
                user:
                  id: "550e8400-e29b-41d4-a716-446655440000"
                  email: user@example.com
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '429':
          $ref: '#/components/responses/RateLimitError'

  /users:
    get:
      tags:
        - Users
      summary: List users
      description: Retrieve paginated list of users
      operationId: listUsers
      security:
        - bearerAuth: []
      parameters:
        - name: page
          in: query
          description: Page number (1-indexed)
          schema:
            type: integer
            default: 1
            minimum: 1
        - name: limit
          in: query
          description: Items per page
          schema:
            type: integer
            default: 20
            minimum: 1
            maximum: 100
        - name: sort
          in: query
          description: Sort field
          schema:
            type: string
            enum: [created_at, email, name]
            default: created_at
        - name: order
          in: query
          description: Sort order
          schema:
            type: string
            enum: [asc, desc]
            default: desc
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
        '401':
          $ref: '#/components/responses/UnauthorizedError'

    post:
      tags:
        - Users
      summary: Create user
      description: Create a new user account
      operationId: createUser
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/ValidationError'
        '409':
          description: Email already exists
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /users/{userId}:
    get:
      tags:
        - Users
      summary: Get user by ID
      operationId: getUser
      security:
        - bearerAuth: []
      parameters:
        - name: userId
          in: path
          required: true
          description: User UUID
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: User details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFoundError'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token obtained from /auth/login

  schemas:
    LoginRequest:
      type: object
      required:
        - email
        - password
      properties:
        email:
          type: string
          format: email
          description: User email address
        password:
          type: string
          format: password
          minLength: 8
          description: User password

    AuthResponse:
      type: object
      properties:
        token:
          type: string
          description: JWT access token
        expires_at:
          type: string
          format: date-time
          description: Token expiration timestamp
        user:
          $ref: '#/components/schemas/User'

    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
          description: Unique user identifier
        email:
          type: string
          format: email
        name:
          type: string
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    CreateUserRequest:
      type: object
      required:
        - email
        - password
        - name
      properties:
        email:
          type: string
          format: email
        password:
          type: string
          format: password
          minLength: 8
        name:
          type: string
          minLength: 1
          maxLength: 100

    Error:
      type: object
      properties:
        code:
          type: string
          description: Error code
        message:
          type: string
          description: Human-readable message
        details:
          type: object
          description: Additional error details

  responses:
    UnauthorizedError:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: UNAUTHORIZED
            message: Authentication required

    NotFoundError:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    ValidationError:
      description: Validation failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    RateLimitError:
      description: Rate limit exceeded
      headers:
        X-RateLimit-Limit:
          schema:
            type: integer
          description: Request limit per minute
        X-RateLimit-Remaining:
          schema:
            type: integer
          description: Remaining requests
        X-RateLimit-Reset:
          schema:
            type: integer
          description: Unix timestamp when limit resets
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

### API Reference Documentation

```markdown
# API Reference

## Authentication

### Login

Authenticate with email and password to obtain an access token.

**Endpoint:** `POST /auth/login`

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | User email address |
| password | string | Yes | User password (min 8 chars) |

**Response:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_at": "2025-01-16T10:30:00Z",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Example:**

```bash
curl -X POST https://api.example.com/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securePassword123"}'
```

**Errors:**

| Code | Status | Description |
|------|--------|-------------|
| INVALID_CREDENTIALS | 401 | Email or password incorrect |
| ACCOUNT_LOCKED | 403 | Too many failed attempts |
| RATE_LIMITED | 429 | Too many requests |

---

## Users

### List Users

Retrieve a paginated list of users.

**Endpoint:** `GET /users`

**Authentication:** Required (Bearer token)

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number |
| limit | integer | 20 | Items per page (max 100) |
| sort | string | created_at | Sort field |
| order | string | desc | Sort order (asc/desc) |

**Response:**

```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "name": "John Doe",
      "created_at": "2025-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

**Example:**

```bash
curl https://api.example.com/v1/users?page=1&limit=10 \
  -H "Authorization: Bearer YOUR_TOKEN"
```
```

### Code Examples Template

```markdown
# Code Examples

## Python

```python
import requests

BASE_URL = "https://api.example.com/v1"

# Authenticate
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "user@example.com",
    "password": "securePassword123"
})
token = response.json()["token"]

# Create headers
headers = {"Authorization": f"Bearer {token}"}

# Get users
users = requests.get(f"{BASE_URL}/users", headers=headers)
print(users.json())

# Create user
new_user = requests.post(f"{BASE_URL}/users", headers=headers, json={
    "email": "newuser@example.com",
    "password": "newPassword123",
    "name": "New User"
})
print(new_user.json())
```

## JavaScript (Node.js)

```javascript
const axios = require('axios');

const BASE_URL = 'https://api.example.com/v1';

async function main() {
  // Authenticate
  const auth = await axios.post(`${BASE_URL}/auth/login`, {
    email: 'user@example.com',
    password: 'securePassword123'
  });
  const token = auth.data.token;

  // Configure client
  const client = axios.create({
    baseURL: BASE_URL,
    headers: { Authorization: `Bearer ${token}` }
  });

  // Get users
  const users = await client.get('/users');
  console.log(users.data);

  // Create user
  const newUser = await client.post('/users', {
    email: 'newuser@example.com',
    password: 'newPassword123',
    name: 'New User'
  });
  console.log(newUser.data);
}

main();
```

## cURL

```bash
# Authenticate
TOKEN=$(curl -s -X POST https://api.example.com/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securePassword123"}' \
  | jq -r '.token')

# Get users
curl https://api.example.com/v1/users \
  -H "Authorization: Bearer $TOKEN"

# Create user
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "new@example.com", "password": "pass123", "name": "New"}'
```
```

### Error Reference Template

```markdown
# Error Reference

## Error Response Format

All errors follow this structure:

```json
{
  "code": "ERROR_CODE",
  "message": "Human-readable description",
  "details": {
    "field": "Additional context"
  }
}
```

## Error Codes

### Authentication Errors (4xx)

| Code | HTTP Status | Description | Resolution |
|------|-------------|-------------|------------|
| `UNAUTHORIZED` | 401 | Missing or invalid token | Include valid Bearer token |
| `INVALID_CREDENTIALS` | 401 | Wrong email/password | Check credentials |
| `TOKEN_EXPIRED` | 401 | Token has expired | Re-authenticate |
| `FORBIDDEN` | 403 | Insufficient permissions | Check user role |
| `ACCOUNT_LOCKED` | 403 | Too many failed attempts | Wait or contact support |

### Validation Errors (400)

| Code | HTTP Status | Description | Resolution |
|------|-------------|-------------|------------|
| `VALIDATION_ERROR` | 400 | Request validation failed | Check `details` field |
| `INVALID_EMAIL` | 400 | Email format invalid | Use valid email |
| `WEAK_PASSWORD` | 400 | Password too weak | Use 8+ chars with complexity |

### Resource Errors (4xx)

| Code | HTTP Status | Description | Resolution |
|------|-------------|-------------|------------|
| `NOT_FOUND` | 404 | Resource doesn't exist | Check ID |
| `CONFLICT` | 409 | Resource already exists | Use different identifier |

### Rate Limiting (429)

| Code | HTTP Status | Description | Resolution |
|------|-------------|-------------|------------|
| `RATE_LIMITED` | 429 | Too many requests | Wait and retry with backoff |

**Rate Limit Headers:**
- `X-RateLimit-Limit`: Max requests per window
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Unix timestamp of reset

### Server Errors (5xx)

| Code | HTTP Status | Description | Resolution |
|------|-------------|-------------|------------|
| `INTERNAL_ERROR` | 500 | Server error | Retry later, contact support |
| `SERVICE_UNAVAILABLE` | 503 | Maintenance | Retry later |
```

## Tools

- **Swagger UI**: Interactive documentation
- **Redoc**: Beautiful API docs
- **Stoplight**: API design platform
- **Postman**: API testing and docs
- **OpenAPI Generator**: Client generation

## Quality Checklist

- [ ] All endpoints documented
- [ ] Request/response schemas complete
- [ ] Authentication documented
- [ ] Error codes comprehensive
- [ ] Examples work correctly
- [ ] Rate limits documented
- [ ] Versioning explained
- [ ] OpenAPI spec valid
- [ ] SDK examples provided
- [ ] Changelog maintained

## Related Skills

- `docstrings` - Code documentation
- `technical-documentation` - Architecture docs
- `user-documentation` - User guides

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates documentation_generation/api_docs/


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
