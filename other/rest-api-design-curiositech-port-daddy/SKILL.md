---
license: Apache-2.0
name: rest-api-design
description: Design REST API endpoints with Zod validation and OpenAPI documentation. Use when creating new API routes, validating request/response schemas, or updating API documentation. Activates for endpoint design, schema validation, error handling, and API docs.
allowed-tools: Read,Write,Edit,Bash(npm:*,npx:*)
category: Backend & Infrastructure
tags:
  - rest
  - api-design
  - http
  - endpoints
  - best-practices
---

# REST API Design

Design REST API endpoints that follow HTTP semantics and handle edge cases gracefully.

## Decision Points

### HTTP Method Selection

```
Does the request read data without side effects?
├─ YES → GET
│  └─ Never mutate state. Cache-safe.
└─ NO → Does it create a new resource?
   ├─ YES → Server assigns ID?
   │  ├─ YES → POST to collection (/orders)
   │  └─ NO → PUT to specific path (/orders/123)
   └─ NO → Does it replace entire resource?
      ├─ YES → PUT to item (/orders/123)
      │  └─ Send full representation
      └─ NO → Does it update specific fields?
         ├─ YES → PATCH to item (/orders/123)
         │  └─ Send only changed fields
         └─ NO → DELETE the resource
            └─ Must be idempotent
```

### Status Code Selection

```
Operation succeeded?
├─ YES → Returning data?
│  ├─ YES → 200 OK
│  ├─ Created resource? → 201 Created + Location header
│  ├─ Async processing? → 202 Accepted + status URL
│  └─ No content? → 204 No Content
└─ NO → Client error or server error?
   ├─ CLIENT → Malformed request?
   │  ├─ Bad JSON/headers → 400 Bad Request
   │  ├─ Valid syntax, bad data → 422 Unprocessable Entity
   │  ├─ No auth → 401 Unauthorized
   │  ├─ Insufficient permissions → 403 Forbidden
   │  ├─ Resource missing → 404 Not Found
   │  ├─ Conflict/duplicate → 409 Conflict
   │  └─ Rate limited → 429 Too Many Requests
   └─ SERVER → Code threw?
      ├─ YES → 500 Internal Server Error
      ├─ Dependency down? → 502 Bad Gateway
      └─ Overloaded? → 503 Service Unavailable
```

### Pagination Strategy

```
Data volume?
├─ < 100 items → No pagination needed
├─ 100-10k items → Offset-based
│  └─ ?page=1&limit=20
└─ > 10k or real-time → Cursor-based
   └─ ?cursor=abc&limit=50
```

### Resource Nesting

```
Resource relationship?
├─ Independent resource → Top-level (/orders)
├─ Owned by parent → One level nesting (/users/123/orders)
└─ Deeper hierarchy needed?
   └─ STOP → Flatten with query params
      └─ /comments?postId=123 not /posts/123/comments
```

## Failure Modes

### 1. **Verbs-in-URLs Syndrome**
- **Symptoms**: `/getUsers`, `/createOrder`, `/deleteItem/5`
- **Detection**: URL path contains action words (get, create, delete, update)
- **Fix**: HTTP method IS the verb. Use nouns: `GET /users`, `POST /orders`, `DELETE /items/5`

### 2. **Deep Nesting Hell**
- **Symptoms**: `/users/1/posts/2/comments/3/likes/4`
- **Detection**: More than 2 path segments with IDs
- **Fix**: Flatten to `/likes?commentId=3`. If resource has global ID, make it top-level

### 3. **Status Code Soup**
- **Symptoms**: `{"error": "Not found"}` with HTTP 200, or `{"success": false}` with 200
- **Detection**: Error responses use 200 status with error in body
- **Fix**: HTTP status code IS the outcome signal. Use 404, 422, 409, etc.

### 4. **Pagination Inconsistency**
- **Symptoms**: `/users?page=1` but `/posts?offset=0&count=20`
- **Detection**: Different pagination params across endpoints
- **Fix**: Standardize on ONE pattern. Document in API guidelines. Apply everywhere

### 5. **POST Double-Submit Vulnerability** 
- **Symptoms**: User clicks twice, gets duplicate orders. Network retry creates duplicates
- **Detection**: POST endpoints have no idempotency protection
- **Fix**: Accept `Idempotency-Key` header. Cache response by `(userId, key)` for 24h

### 6. **Schema Over-Nesting**
- **Symptoms**: `{"data": {"result": {"items": [{"item": {"value": 123}}]}}}`
- **Detection**: More than 2 levels of nesting in response objects
- **Fix**: Flatten structure. Use consistent envelope: `{"data": [...], "meta": {}}`

### 7. **Missing Error Details**
- **Symptoms**: `{"error": "Validation failed"}` with no field-level info
- **Detection**: 422 responses lack specific field errors
- **Fix**: Include `details` array with `path` and `message` for each validation failure

### 8. **Unbounded Responses**
- **Symptoms**: `GET /users` returns all 50,000 users in one response
- **Detection**: Collection endpoints with no pagination or limits
- **Fix**: Default pagination (limit=20). Max limit (100). Never return unbounded arrays

## Worked Examples

### Scenario: E-commerce Order Management API

**Requirements**: Create orders, list user orders, update shipping address, cancel orders.

**Step 1: Method Selection**
- List orders: Reading data → `GET /orders`
- Create order: Creating resource → `POST /orders` 
- Update address: Partial update → `PATCH /orders/{id}`
- Cancel order: Action → Model as resource → `POST /orders/{id}/cancellation`

**Step 2: Handle Edge Cases**

```typescript
// POST /orders - Creation
{
  "items": [{"productId": "prod_1", "quantity": 2}],
  "shippingAddress": {...},
  "idempotencyKey": "uuid-12345"  // Prevent double-submit
}

// Success: 201 Created + Location header
{
  "id": "ord_123",
  "status": "pending",
  "total": 59.98,
  "createdAt": "2024-01-15T10:30:00Z"
}

// Duplicate: 409 Conflict (idempotency key reused within 24h)
{
  "error": "Order already exists with this idempotency key",
  "code": "DUPLICATE_ORDER",
  "existingOrderId": "ord_123"
}

// Invalid data: 422 Unprocessable Entity
{
  "error": "Validation failed",
  "code": "VALIDATION_ERROR", 
  "details": [
    {"path": "items[0].quantity", "message": "Must be positive integer"},
    {"path": "shippingAddress.zipCode", "message": "Invalid format"}
  ]
}
```

**Step 3: Pagination & Filtering**

```typescript
// GET /orders?status=pending&page=2&limit=10&sort=createdAt:desc
{
  "data": [
    {"id": "ord_124", "status": "pending", "total": 29.99, ...},
    {"id": "ord_123", "status": "pending", "total": 59.98, ...}
  ],
  "pagination": {
    "page": 2,
    "limit": 10, 
    "total": 156,
    "totalPages": 16
  },
  "filters": {
    "status": "pending",
    "sort": "createdAt:desc"
  }
}
```

**Step 4: State Transitions**

```typescript
// PATCH /orders/ord_123 - Update shipping
{"shippingAddress": {"street": "123 New St"}}

// Success if order is pending: 200 OK
{"id": "ord_123", "status": "pending", "shippingAddress": {...}}

// Error if already shipped: 409 Conflict  
{
  "error": "Cannot modify shipped order",
  "code": "ORDER_ALREADY_SHIPPED",
  "currentStatus": "shipped"
}

// POST /orders/ord_123/cancellation - Cancel order
{"reason": "Changed mind"}

// Success: 201 Created
{
  "id": "canc_456", 
  "orderId": "ord_123",
  "reason": "Changed mind",
  "refundAmount": 59.98,
  "createdAt": "2024-01-15T11:00:00Z"
}
```

**What novice misses**: Uses `DELETE /orders/123` for cancellation (loses cancel reason/refund data). Returns 200 for all errors. No idempotency protection.

**What expert catches**: Models cancellation as resource creation. Uses proper status codes. Protects against double-submit. Validates state transitions.

## Quality Gates

- [ ] Every endpoint uses nouns in paths (no verbs like `/getUsers`)
- [ ] Consistent HTTP method usage (GET=read, POST=create, PATCH=partial update)  
- [ ] All mutation endpoints return proper status codes (201/204/409/422, never 200 for errors)
- [ ] Collection endpoints have pagination with consistent params across API
- [ ] Error responses include `error`, `code`, and `details` fields in standard envelope
- [ ] POST endpoints that create resources accept `Idempotency-Key` header
- [ ] Resource nesting limited to 2 levels maximum (/users/123/orders, not deeper)
- [ ] All endpoints documented with request/response examples including error cases
- [ ] Rate limiting strategy defined (requests per minute by endpoint type)
- [ ] Authentication requirements specified per endpoint (public/authenticated/admin)

## NOT-FOR Boundaries

**Don't use REST API design for**:
- GraphQL APIs → Use `graphql-schema-design` skill
- WebSocket/SSE real-time APIs → Use `realtime-api-design` skill  
- Platform-specific APIs (Vercel Edge, Cloudflare Workers) → Use platform-specific skills
- Internal RPC between microservices → Use `grpc-design` or message queues
- File upload/download APIs → Use `file-api-design` skill for multipart handling

**Delegate to other skills**:
- Database schema design → Use `database-design` skill
- Authentication implementation → Use `auth-implementation` skill
- OpenAPI documentation → Use `openapi-documentation` skill
- Performance optimization → Use `api-performance` skill