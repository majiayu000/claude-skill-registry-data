---
name: api-design-rest
description: When creating or extending an HTTP API for client consumption.
version: 2.0.0
category: backend
tags: [backend, api, rest, http]
skill_type: architecture
author: skiLLM
license: MIT
compatible_agents: [claude-code, cursor, copilot, codex]
estimated_context_tokens: 1600
dangerous: false
requires_review: false
security_level: safe
dependencies: [error-handling-architecture]
triggers: [api, endpoint, rest, http, resource]
permissions:
  filesystem: { read: true, write: true }
  network: { outbound: false }
  shell: { execute: false }
input_requirements: [existing API codebase or new service structure]
output_contract: [lowercase URLs, status codes used semantically, RFC 7807 errors, versioned endpoints]
failure_conditions: [using verbs in URLs, HTTP 200 for failures, nesting deeper than 2 levels]
last_updated: 2026-05-15
---

# RESTful API Design

## Purpose
REST APIs MUST be intuitive, predictable, and semantically correct. This skill ensures APIs use HTTP methods correctly, communicate errors clearly via standard formats, and maintain consistency across resources so clients can interact with them reliably without surprise behavior.

## When to use
- Building a new backend service exposing resources
- Adding a new domain entity to an existing API
- Creating integration endpoints for third-party partners
- Designing webhooks or callback mechanisms
- Standardizing an inconsistent API across a microservices architecture

## When NOT to use
- Error handling specifics (use Error Handling Architecture skill)
- API authentication/authorization (separate concern)
- Rate limiting or throttling strategies (separate concern)
- GraphQL design (different paradigm)

## Inputs required
- Existing API codebase or documented business entities
- HTTP framework (Express, Django, FastAPI, etc.)
- OpenAPI/Swagger familiarity preferred

## Workflow
1. **Identify Resources**: Map business entities to Plural Nouns (users, orders, invoices, not getUsers)
2. **Assign Verbs**: Map CRUD operations to HTTP methods: GET (read), POST (create), PUT (replace), PATCH (update), DELETE (remove)
3. **Design URL Hierarchy**: Nest resources logically but NO DEEPER than 2 levels (e.g., `/users/{id}/orders` ONLY)
4. **Standardize Responses**: All success payloads wrapped consistently; all errors use RFC 7807 format
5. **Add Pagination**: For collection endpoints, REQUIRE `limit` and `offset` (or cursor-based pagination)
6. **Version the API**: Use `/v1/` prefix or header-based versioning from day one
7. **Document with OpenAPI**: Generate OpenAPI schema automatically or maintain it in sync

## Rules
- MUST use HTTP status codes semantically (see failure conditions below)
- MUST NOT use verbs in URLs (no `GET /getUsers`)
- MUST NOT nest resources beyond 2 levels deep
- MUST use lowercase URLs with hyphens for multi-word resource names
- MUST require API versioning
- MUST return RFC 7807 problem details for ALL errors
- MUST paginate collection responses

## Anti-patterns
- **Verbs in URLs**: `GET /getUsers`, `POST /createOrder` (use nouns + HTTP methods)
- **HTTP 200 for Errors**: Returning 200 with `{ status: 'error' }` payload (use 4xx/5xx status codes)
- **Deep Nesting**: `/companies/{id}/departments/{id}/employees/{id}/tasks` (use max 2 levels)
- **Mixed Status Codes**: Endpoint returns 200 for success, 200 for validation errors (inconsistent)
- **Unversioned APIs**: Adding `/api/users` without versioning path for future breaking changes

## Failure conditions
- URLs contain action verbs
- HTTP 200 returned for failed requests
- Resource nesting exceeds 2 levels
- Collection endpoint has no pagination
- Errors not in RFC 7807 format
- API has no versioning strategy

## Validation checklist
- [ ] All resource URLs are plural nouns (users, orders, not getUsers)
- [ ] HTTP methods used semantically (GET=read, POST=create, PATCH=partial, DELETE=remove)
- [ ] No verbs in URL paths
- [ ] Status codes are correct (201 for create, 204 for delete, 400 for validation, 500 for server errors)
- [ ] All error responses use RFC 7807 format with `type`, `title`, `detail`, `status`
- [ ] Collection endpoints support `limit` and `offset` parameters
- [ ] URLs include version (e.g., `/v1/users` or header-based)
- [ ] URLs use lowercase with hyphens (e.g., `/user-profiles` not `/userProfiles`)
- [ ] Resource nesting does not exceed 2 levels
- [ ] OpenAPI schema is generated or synchronized

## Output format
- **Response structure**: JSON with consistent key naming (snake_case or camelCase, not mixed)
- **Error format**: RFC 7807 Problem Details (`type`, `title`, `detail`, `status`, `instance`)
- **Pagination**: Include `limit`, `offset`, `total` in collection response envelope
- **Versioning**: `/v1/` URL prefix or `API-Version: 1.0` header
- **Documentation**: OpenAPI 3.0+ schema

## Security considerations
- Pagination defaults MUST have max limits (prevent DOS via `limit=999999999`)
- Error messages MUST NOT leak internal implementation details
- Resource IDs should not expose sequential patterns (use UUIDs, not auto-increment)
- API MUST enforce authentication/authorization (separate skill)
- Rate limiting MUST be enforced (separate skill)

## Agent execution notes
- Agent MAY: Create new endpoints, design resource hierarchies, add pagination, generate OpenAPI schema
- Agent MUST NEVER: Use verbs in URLs, return 200 for errors, nest beyond 2 levels, mix status code semantics
- Agent MUST ASK: Before changing versioning strategy, before modifying existing endpoint contracts
- Agent MUST VALIDATE: All status codes correct, no URL verbs, pagination present, RFC 7807 errors

## Example

**❌ Anti-pattern (Verbs in URL, wrong status codes, deep nesting, no pagination):**
```http
GET /api/getUsers HTTP/1.1

HTTP/1.1 200 OK
{
  "status": "error",
  "message": "User not found"
}

GET /api/companies/123/departments/456/employees/789/tasks/assignToUser HTTP/1.1
```

**✅ Correct pattern (Nouns, semantic status, proper nesting, paginated):**
```http
GET /v1/users?limit=20&offset=0 HTTP/1.1

HTTP/1.1 200 OK
{
  "data": [...],
  "pagination": {
    "limit": 20,
    "offset": 0,
    "total": 150
  }
}

GET /v1/users/123 HTTP/1.1

HTTP/1.1 404 Not Found
{
  "type": "https://api.example.com/errors/resource-not-found",
  "title": "Resource Not Found",
  "detail": "The requested user does not exist",
  "status": 404,
  "instance": "/v1/users/123"
}

GET /v1/users/123/orders?limit=10&offset=0 HTTP/1.1
```
