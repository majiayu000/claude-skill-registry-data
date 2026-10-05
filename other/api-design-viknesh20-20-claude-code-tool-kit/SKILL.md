---
name: api-design
description: "Designs REST or GraphQL APIs with endpoint definitions, request/response schemas, error codes, authentication requirements, and OpenAPI spec generation. Use when building new APIs or extending existing ones."
argument-hint: "[resource name or feature description]"
allowed-tools: Read, Grep, Glob, Bash, Write
---

# API Design

## Existing API Patterns
!`find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.java" -o -name "*.rb" -o -name "*.cs" \) -path "*/route*" -o -path "*/controller*" -o -path "*/handler*" -o -path "*/endpoint*" -o -path "*/api*" 2>/dev/null | grep -v node_modules | grep -v vendor | grep -v .git | head -20`

!`find . -name "openapi*" -o -name "swagger*" -o -name "*.graphql" -o -name "*.gql" -o -name "schema.*" 2>/dev/null | grep -v node_modules | head -10`

---

## Design Process

### Step 1: Understand the Domain
1. Identify the resource(s) being modeled
2. Define the data model with all fields and types
3. Map relationships between resources
4. Identify the consumers (frontend, mobile, third-party)

### Step 2: Design Endpoints (REST)

For each resource, define:

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | /api/v1/{resources} | List all (paginated) | Required |
| GET | /api/v1/{resources}/:id | Get single by ID | Required |
| POST | /api/v1/{resources} | Create new | Required |
| PUT | /api/v1/{resources}/:id | Full update | Required |
| PATCH | /api/v1/{resources}/:id | Partial update | Required |
| DELETE | /api/v1/{resources}/:id | Delete | Required |

### Step 3: Define Schemas

For each endpoint, define:
- **Request body** (JSON schema with types, required fields, validation rules)
- **Response body** (JSON schema with all fields)
- **URL parameters** (path params, query params for filtering/sorting/pagination)
- **Headers** (Content-Type, Authorization, custom headers)

### Step 4: Error Handling

Standard error response format:
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Human-readable description",
    "details": []
  }
}
```

Standard HTTP status codes:
- `200` OK — successful GET/PUT/PATCH
- `201` Created — successful POST
- `204` No Content — successful DELETE
- `400` Bad Request — validation errors
- `401` Unauthorized — missing/invalid auth
- `403` Forbidden — insufficient permissions
- `404` Not Found — resource doesn't exist
- `409` Conflict — duplicate or state conflict
- `422` Unprocessable Entity — valid JSON but semantic errors
- `429` Too Many Requests — rate limited
- `500` Internal Server Error — unexpected failure

### Step 5: Pagination, Filtering, Sorting

**Pagination** (cursor or offset):
```
GET /api/v1/users?page=2&per_page=20
GET /api/v1/users?cursor=abc123&limit=20
```

**Filtering**:
```
GET /api/v1/users?status=active&role=admin
```

**Sorting**:
```
GET /api/v1/users?sort=created_at&order=desc
```

### Step 6: Generate Specification
Output an OpenAPI 3.0 spec (YAML) or GraphQL schema as appropriate for the project.

---

## Design Principles
- Use plural nouns for resource names (`/users` not `/user`)
- Use kebab-case for multi-word endpoints (`/user-profiles`)
- Version the API (`/api/v1/`)
- Be consistent with existing patterns in the project
- Follow REST constraints: stateless, cacheable, uniform interface
- Design for the consumer, not the database schema
