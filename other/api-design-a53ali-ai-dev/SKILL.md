---
name: api-design
description: Design REST or GraphQL APIs with strong contracts, versioning, and error handling
triggers: [api design, rest api, graphql, endpoint, design contract, api contract, versioning]
audience: engineer
---

# API Design

## Context
A well-designed API is a stable contract between producers and consumers. Poor API design creates coupling, breaks clients unexpectedly, and generates support burden. This skill guides the design of RESTful and GraphQL APIs that are intuitive, evolvable, and resilient.

Use this skill when:
- Designing a new endpoint or resource
- Reviewing an API for correctness
- Planning API versioning or evolution
- Designing internal service APIs in a distributed system

## Instructions

### REST API Design

#### Resource Naming
- Use nouns for resource names, not verbs: `/orders` not `/getOrders`
- Use plural for collections: `/users`, `/products`
- Nest resources only when the relationship is truly hierarchical: `/users/{id}/orders`
- Keep paths shallow (max 3 levels). Deep nesting is a design smell.

#### HTTP Methods
| Action | Method | Idempotent |
|--------|--------|------------|
| Read collection | GET /resources | Yes |
| Read item | GET /resources/{id} | Yes |
| Create | POST /resources | No |
| Full replace | PUT /resources/{id} | Yes |
| Partial update | PATCH /resources/{id} | No |
| Delete | DELETE /resources/{id} | Yes |

#### Status Codes
- `200 OK` — successful GET, PATCH, PUT
- `201 Created` — successful POST that creates a resource (include `Location` header)
- `204 No Content` — successful DELETE or action with no response body
- `400 Bad Request` — client validation error (include error details in body)
- `401 Unauthorized` — not authenticated
- `403 Forbidden` — authenticated but not authorized
- `404 Not Found` — resource does not exist
- `409 Conflict` — state conflict (e.g., duplicate creation, stale update)
- `422 Unprocessable Entity` — validation passed but semantic error
- `429 Too Many Requests` — rate limited (include `Retry-After` header)
- `500 Internal Server Error` — unexpected server error (never expose stack traces)

#### Error Response Format (consistent across all endpoints)
```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Human-readable description",
    "details": [{ "field": "email", "issue": "must be a valid email address" }]
  }
}
```

#### Versioning
- Prefer URI versioning for external APIs: `/v1/users`
- Use `Accept` header versioning for internal or evolving APIs
- Never break an existing version — deprecate and provide a migration path with a sunset date
- Document breaking vs. non-breaking changes explicitly

### GraphQL API Design
- Design schema around domain types, not database tables
- Use nullable fields conservatively — only where truly optional
- Implement cursor-based pagination for all list fields: `{ edges { node cursor } pageInfo }`
- Never expose internal IDs directly — use opaque global IDs
- Use mutations for all state changes; queries must be side-effect-free
- Rate limit by query complexity, not just request count

### Idempotency
- All GET, PUT, DELETE operations must be idempotent by design
- For POST operations where idempotency matters (e.g., payment), support an `Idempotency-Key` header
- Document which operations are idempotent in the API contract

## Principles
- Source: [Richardson Maturity Model — Martin Fowler](https://martinfowler.com/articles/richardsonMaturityModel.html)
- Source: [Tolerant Reader — Martin Fowler](https://martinfowler.com/bliki/TolerantReader.html)
- Key idea: *"A good API is one that makes the simple things simple and the complex things possible, without exposing the complexity of its implementation."*

## Output Format
When applying this skill, the agent should:
- Produce the resource model and endpoint list for new API designs
- Flag any violations of the above principles in existing APIs
- Show the error response schema
- Call out any breaking change risks and suggest a migration path
