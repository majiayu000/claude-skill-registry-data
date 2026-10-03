---
name: api-design-standards
description: >
  Use when designing, implementing, or reviewing APIs to ensure consistent, reliable,
  and developer-friendly interfaces. This skill provides standardized API design principles
  and patterns across all companies and services.
---

# API Design Standards

## Overview
This skill defines API design standards for consistent, reliable, and developer-friendly APIs. Good API design reduces integration friction, prevents bugs, and makes cross-company collaboration smooth.

## When to Use
- When designing any new API endpoint or service interface
- When modifying existing APIs
- When reviewing API specifications or documentation
- When integrating between companies or external services
- **Don't use when:** Building internal-only functions with no network exposure

## Core Procedures

### Step 1: Design Principles
Apply these principles to all API design:
- **RESTful:** Use standard HTTP methods (GET, POST, PUT, PATCH, DELETE) appropriately
- **Resource-Based:** URLs represent resources, actions are HTTP methods
- **Consistent Naming:** Use lowercase-with-dashes for paths, plural nouns for collections
- **Versioned:** Include version in URL or header from day one
- **Documented:** Every endpoint, parameter, and response documented

### Step 2: Endpoint Design
```
GET /api/v1/{resource}         # List resources (paginated)
GET /api/v1/{resource}/{id}    # Get specific resource
POST /api/v1/{resource}        # Create new resource
PUT /api/v1/{resource}/{id}    # Replace resource
PATCH /api/v1/{resource}/{id}  # Partial update
DELETE /api/v1/{resource}/{id} # Delete resource
```

### Step 3: Request Standards
- **Query Parameters:** Filtering (?status=active), sorting (?sort=created_at:desc), pagination (?page=1&limit=20)
- **Request Body:** JSON content type, validated against schema, clear error messages
- **Headers:** Content-Type, Accept, Authorization with Bearer token
- **Idempotency:** POST not guaranteed idempotent, PUT/PATCH/DELETE are

### Step 4: Response Standards
All responses include:
- Appropriate HTTP status code (200, 201, 400, 401, 403, 404, 409, 422, 429, 500)
- JSON response body for successful responses
- Consistent error format:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [{"field": "name", "issue": "Required field"}]
  }
}
```
- Pagination metadata for collection responses

### Step 5: Security Standards
- Authentication required for all non-public endpoints
- Authorization checked for every resource access
- Rate limiting applied to prevent abuse
- Input validation and sanitization on all parameters
- HTTPS required, never transmit over HTTP
- No secrets in URLs, query parameters, or error messages

## Quality Checklist
- [ ] RESTful principles applied to all endpoints
- [ ] Consistent naming conventions followed
- [ ] API versioned from day one
- [ ] All endpoints documented with request/response examples
- [ ] Error responses follow standard format
- [ ] Authentication and authorization in place
- [ ] Rate limiting configured
- [ ] Input validation on all parameters

## Error Handling
- **Error:** API design doesn't fit RESTful pattern
  **Response:** Document why non-RESTful approach is needed, get architecture review
- **Error:** Breaking change needed to existing API
  **Response:** Create new version, deprecate old version with sunset header, provide migration guide
- **Error:** Response times exceed SLA
  **Response:** Implement pagination, add caching, optimize queries

## Cross-Team Integration
**Related Skills:** testing-strategy, secrets-handling, documentation-quality-check, data-modeling-standards
**Used By:** Backend engineers, API developers, Integrators, any agent creating interfaces used by others