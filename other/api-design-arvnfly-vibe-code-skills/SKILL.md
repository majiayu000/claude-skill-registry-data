---
name: api-design
description: "Universal standards for RESTful API architecture, RFC 7807 error envelopes, cursor-based pagination, idempotency keys, and schema contracts (Zod, Pydantic, OpenAPI)."
---

# API Design Standards & Contract Protocol

When designing, implementing, or reviewing APIs (REST, RPC, or GraphQL), adhere strictly to these architectural standards.

---

## 1. Resource Naming & URI Conventions

1. **Plural Nouns for Collections**:
   - `GET /v1/users` (list users)
   - `POST /v1/users` (create user)
   - `GET /v1/users/{id}` (fetch user)
   - `PATCH /v1/users/{id}` (partial update user)
   - `DELETE /v1/users/{id}` (remove user)
2. **Sub-resources for Relationships**:
   - `GET /v1/organizations/{orgId}/members`
   - `POST /v1/organizations/{orgId}/invitations`
3. **No Verbs in URIs**:
   - Bad: `POST /v1/users/create` or `POST /v1/users/deleteUser`
   - Good: `POST /v1/users` or `DELETE /v1/users/{id}`
   - Action exception: When modeling an operation that does not map to CRUD, use explicit sub-actions:
     `POST /v1/deployments/{id}/rollback`

---

## 2. Standardized Response Formats

### Success Payloads
Always wrap top-level items or return consistent object envelopes:

```json
{
  "data": {
    "id": "usr_99824",
    "email": "user@example.com",
    "role": "admin",
    "createdAt": "2026-10-19T09:00:00Z"
  }
}
```

### RFC 7807 Standard Error Envelope
All 4xx and 5xx responses MUST use RFC 7807 Problem Details structure:

```json
{
  "error": {
    "type": "https://api.example.com/errors/validation-failed",
    "title": "Validation Failed",
    "status": 422,
    "detail": "The payload contains invalid fields.",
    "instance": "/v1/users",
    "invalidParams": [
      {
        "name": "email",
        "reason": "Must be a valid email address format"
      }
    ]
  }
}
```

---

## 3. Idempotency Keys on Mutations

For non-idempotent operations (`POST`), require or support the `Idempotency-Key` header:
1. Client transmits unique UUID v4 in `Idempotency-Key: 7b841a54-7f12-4d2a-89aa-0a0d4c9e88b2`.
2. Server verifies cache/store for previous execution with the identical key:
   - In-progress: Return `HTTP 409 Conflict` with `concurrent_mutation`.
   - Completed: Return identical cached HTTP status and body payload.
   - New key: Execute mutation and record result with TTL (typically 24 hours).

---

## 4. Pagination Protocols

### Cursor-Based Pagination (Default for high-velocity datasets)
```
GET /v1/transactions?limit=25&after=cursor_tx_78829
```

Response payload:
```json
{
  "data": [...],
  "pagination": {
    "hasMore": true,
    "nextCursor": "cursor_tx_78854",
    "limit": 25
  }
}
```

### Offset Pagination (Restricted to low-volume administrative tables)
```
GET /v1/audit-logs?page=2&pageSize=50
```

---

## 5. Schema Validation at Trust Boundaries

1. Every inbound payload must validate against a strict schema (e.g. Zod, Pydantic, Joi) before hitting controllers or handlers.
2. Strip unrecognised properties (`stripUnknown: true` or `extra: 'forbid'`) to prevent prototype pollution and parameter injection.
3. Validate parameter types, string lengths, regex patterns, and numeric ranges.
