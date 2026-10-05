---
name: api-contract
description: >
  Design a REST API contract for a given resource or feature. Auto-invoke when
  the user says "design the API for", "what endpoints do we need for",
  "define the contract for", or "API spec for X".
allowed-tools: Read, Write, Glob
argument-hint: <resource-or-feature-description>
---
 
# API Contract Skill
 
Design a complete, production-ready REST API contract for: `$ARGUMENTS`
 
## Step 1 — Clarify (if ambiguous)
If the resource or feature description is vague, ask ONE clarifying question before proceeding.
E.g.: "Is this a public API or internal service-to-service? Does it need auth?"
 
## Step 2 — Design the Endpoints
 
For each endpoint, define:
 
```
[METHOD] /api/v1/<resource>
  Auth:        required | public | service-to-service
  Description: <what it does>
  Request:     <body schema or query params>
  Response:    <success schema>
  Errors:      <expected error codes and when they occur>
```
 
### Rules
- Resource names: plural nouns (`/orders`, `/users`, `/payment-methods`)
- HTTP verbs map to intent: GET=query, POST=create, PUT=full replace, PATCH=partial update, DELETE=remove
- Always version the API: `/api/v1/`
- Use **cursor-based pagination** for list endpoints — include `cursor`, `limit`, `hasMore`, `nextCursor`
- Consistent response envelope:
  ```json
  { "data": {}, "meta": {}, "error": null }
  ```
- Error envelope:
  ```json
  { "data": null, "error": { "code": "ORDER_NOT_FOUND", "message": "...", "details": {} } }
  ```
 
## Step 3 — Define Schemas
 
For each request and response body, write a clear schema:
 
```
CreateOrderRequest {
  userId:   string (UUID, required)
  items:    Array<{ productId: string, quantity: number (min: 1) }>
  currency: string (ISO 4217, required)
}
 
OrderResponse {
  id:        string (UUID)
  userId:    string (UUID)
  status:    enum: pending | paid | shipped | cancelled
  items:     Array<OrderItemResponse>
  total:     number (decimal, 2dp)
  currency:  string
  createdAt: ISO 8601 datetime
}
```
 
## Step 4 — Define Error Codes
 
List all domain-specific error codes this resource can produce:
 
| Code | HTTP Status | When |
|---|---|---|
| `ORDER_NOT_FOUND` | 404 | Requested order ID does not exist |
| `ITEM_OUT_OF_STOCK` | 422 | One or more items unavailable |
| `INVALID_CURRENCY` | 400 | Currency code not supported |
 
## Step 5 — Flag Design Concerns
 
Point out any of the following if applicable:
- Endpoints that would create N+1 problems
- Operations that should be async (return 202 Accepted + a job/status endpoint)
- Endpoints that need idempotency keys
- Breaking changes if this is modifying an existing API
 
## Output
- Write the contract to `docs/api/<resource>-contract.md` in the project
- Print a summary of: endpoints count, auth model, pagination strategy, async operations if any
