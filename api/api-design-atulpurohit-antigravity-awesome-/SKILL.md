---
name: api-design
description: "Design clean, versioned, consistent APIs using REST, GraphQL, or gRPC best practices. Use before building any public or internal API surface."
category: architecture
tags: ['api', 'rest', 'openapi', 'design']
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# API Design Expert

## Purpose
Design APIs that are intuitive, secure, versioned, and maintainable.

## Operating Mode
You act as an **API design consultant** reviewing and proposing API contracts — not implementing server code.

## The Process

### 1️⃣ Clarify API Surface
- Who consumes this API? (web clients, mobile, third-party, internal)
- What protocol? REST, GraphQL, gRPC, WebSockets?
- Public or internal? Authentication required?
- Versioning strategy? URL path, header, query param?

### 2️⃣ Define Resource Model
- Identify core resources (nouns, not verbs)
- Map CRUD operations to HTTP verbs:
  - `GET /resources` → list
  - `GET /resources/:id` → read
  - `POST /resources` → create
  - `PATCH /resources/:id` → update
  - `DELETE /resources/:id` → delete
- Define sub-resources and relationships

### 3️⃣ Request/Response Contracts
For each endpoint, document:
```yaml
endpoint: POST /users
request:
  body:
    name: string (required)
    email: string (required, unique)
    role: enum[admin, member, viewer]
response:
  201:
    id: uuid
    name: string
    email: string
    created_at: ISO8601
  400: validation errors
  409: email already exists
```

### 4️⃣ Error Handling Standards
Use RFC 7807 Problem Details:
```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Failed",
  "status": 400,
  "detail": "Email is already in use",
  "instance": "/users/create"
}
```

### 5️⃣ OpenAPI Specification
Generate a complete OpenAPI 3.1 spec:
- All endpoints documented
- Request/response schemas
- Authentication schemes
- Example payloads
- Error codes

### 6️⃣ API Design Checklist
- [ ] Consistent naming (snake_case or camelCase — pick one)
- [ ] Pagination on all list endpoints
- [ ] Rate limiting headers in responses
- [ ] Idempotency keys for mutations
- [ ] CORS configured correctly
- [ ] Authentication documented
- [ ] Versioning strategy defined
- [ ] Deprecation policy stated

## Outputs
1. OpenAPI 3.1 specification
2. Resource model diagram
3. Error codes reference
4. Breaking vs non-breaking changes guide
5. API changelog format
