---
name: api-design
description: API design principles for REST, GraphQL, and gRPC including versioning, pagination, error handling, and documentation. Use when designing new APIs.
---

# API Design

Comprehensive guidance for designing, documenting, and evolving APIs across REST, GraphQL, and gRPC paradigms, covering resource modeling, versioning strategies, error handling standards, pagination, rate limiting, and contract-first development.

## When to Use This Skill

Use this skill for:

- Designing a new REST, GraphQL, or gRPC API from scratch
- Reviewing an existing API contract for consistency and best practices
- Choosing between REST, GraphQL, and gRPC for a given use case
- Implementing pagination, filtering, and sorting patterns
- Designing error response formats (RFC 7807 Problem Details)
- Planning API versioning and evolution strategies
- Setting up rate limiting and authentication headers
- Writing OpenAPI, GraphQL schema, or protobuf definitions
- Migrating between API styles (REST to GraphQL, REST to gRPC)

**Trigger phrases**: "API design", "REST API", "GraphQL schema", "gRPC proto", "API versioning", "pagination", "error handling", "OpenAPI", "API contract", "rate limiting", "HATEOAS"

## What This Skill Does

Provides API design patterns including:

- **REST Design**: Resource naming, HTTP methods, status codes, HATEOAS links
- **GraphQL Design**: Schema definition, query/mutation patterns, N+1 prevention
- **gRPC Design**: Service definitions, protobuf best practices, streaming patterns
- **Versioning**: URL path, header, content negotiation strategies with trade-offs
- **Pagination**: Cursor-based, offset-based, keyset patterns with examples
- **Error Handling**: RFC 7807 Problem Details, GraphQL error extensions, gRPC status codes
- **Rate Limiting**: Token bucket, sliding window, response headers
- **Authentication**: API key, OAuth 2.0, JWT bearer token header conventions
- **Documentation**: OpenAPI 3.1, GraphQL introspection, gRPC reflection

## Instructions

### Step 1: Choose the Right API Style

**Decision Matrix**:

| Factor | REST | GraphQL | gRPC |
|--------|------|---------|------|
| Client diversity | Many unknown clients | Multiple frontends (web, mobile) | Internal service-to-service |
| Data shape | Fixed, resource-oriented | Flexible, client-driven | Fixed, contract-driven |
| Performance | Good (HTTP caching) | Variable (no HTTP caching) | Excellent (binary, HTTP/2) |
| Real-time | Webhooks, SSE | Subscriptions | Bidirectional streaming |
| Discoverability | OpenAPI, HATEOAS | Introspection | Reflection, proto files |
| Learning curve | Low | Medium | Medium-High |
| Browser support | Native | Native (via HTTP) | Requires grpc-web proxy |
| File uploads | Native multipart | Awkward (base64 or multipart) | Streaming chunks |

**When to Choose Each**:

```
REST:    Public APIs, third-party integrations, CRUD-heavy services,
         when HTTP caching matters, when you need broad tooling support.

GraphQL: Multiple client types with different data needs (mobile wants
         less data than web), rapid frontend iteration, aggregating
         data from multiple backend services into a single query.

gRPC:    Internal microservice communication, low-latency requirements,
         polyglot environments (code generation from proto files),
         bidirectional streaming (chat, live data feeds).
```

### Step 2: Design REST APIs

**Resource Naming Conventions**:

```
# Use nouns (not verbs) for resources
GET    /users                  # List users
POST   /users                  # Create user
GET    /users/{id}             # Get single user
PUT    /users/{id}             # Replace user
PATCH  /users/{id}             # Partial update
DELETE /users/{id}             # Delete user

# Use plural nouns
GET    /orders                 # Not /order
GET    /order-items            # Hyphenated, not camelCase or snake_case

# Nest for clear ownership (max 2 levels deep)
GET    /users/{id}/orders      # Orders belonging to user
POST   /users/{id}/orders      # Create order for user

# Use query parameters for filtering, sorting, searching
GET    /orders?status=pending&sort=-created_at&limit=20
GET    /products?category=electronics&min_price=100&q=laptop
```

**HTTP Methods and Status Codes**:

```
Method    Idempotent  Safe   Common Status Codes
------    ----------  ----   --------------------
GET       Yes         Yes    200 OK, 304 Not Modified
POST      No          No     201 Created, 202 Accepted, 400 Bad Request
PUT       Yes         No     200 OK, 204 No Content, 409 Conflict
PATCH     No          No     200 OK, 422 Unprocessable Entity
DELETE    Yes         No     204 No Content, 404 Not Found

Status Code Ranges:
  2xx  Success (200 OK, 201 Created, 202 Accepted, 204 No Content)
  3xx  Redirection (301 Moved, 304 Not Modified)
  4xx  Client error (400 Bad Request, 401 Unauthorized, 403 Forbidden,
       404 Not Found, 409 Conflict, 422 Unprocessable Entity, 429 Too Many)
  5xx  Server error (500 Internal, 502 Bad Gateway, 503 Unavailable)
```

**OpenAPI 3.1 Example**:

```yaml
openapi: 3.1.0
info:
  title: Order Management API
  version: 1.2.0
  description: API for managing customer orders
  contact:
    name: Platform Team
    email: platform@example.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api.staging.example.com/v1
    description: Staging

paths:
  /orders:
    get:
      operationId: listOrders
      summary: List orders with filtering and pagination
      tags: [Orders]
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [draft, placed, confirmed, shipped, delivered, cancelled]
        - name: cursor
          in: query
          description: Pagination cursor from previous response
          schema:
            type: string
        - name: limit
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
      responses:
        "200":
          description: Paginated list of orders
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: "#/components/schemas/Order"
                  pagination:
                    $ref: "#/components/schemas/CursorPagination"
          headers:
            X-RateLimit-Remaining:
              schema:
                type: integer

    post:
      operationId: createOrder
      summary: Create a new order
      tags: [Orders]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateOrderRequest"
      responses:
        "201":
          description: Order created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Order"
          headers:
            Location:
              schema:
                type: string
                format: uri
        "422":
          description: Validation error
          content:
            application/problem+json:
              schema:
                $ref: "#/components/schemas/ProblemDetail"

components:
  schemas:
    Order:
      type: object
      required: [id, customerId, status, lines, total, createdAt]
      properties:
        id:
          type: string
          format: uuid
        customerId:
          type: string
          format: uuid
        status:
          type: string
          enum: [draft, placed, confirmed, shipped, delivered, cancelled]
        lines:
          type: array
          items:
            $ref: "#/components/schemas/OrderLine"
        total:
          $ref: "#/components/schemas/Money"
        createdAt:
          type: string
          format: date-time
        _links:
          type: object
          properties:
            self:
              type: object
              properties:
                href:
                  type: string
                  format: uri

    OrderLine:
      type: object
      properties:
        productId:
          type: string
          format: uuid
        productName:
          type: string
        unitPrice:
          $ref: "#/components/schemas/Money"
        quantity:
          type: integer
          minimum: 1

    Money:
      type: object
      properties:
        amount:
          type: integer
          description: Amount in smallest currency unit (cents)
        currency:
          type: string
          pattern: "^[A-Z]{3}$"

    CreateOrderRequest:
      type: object
      required: [customerId, lines]
      properties:
        customerId:
          type: string
          format: uuid
        lines:
          type: array
          minItems: 1
          items:
            type: object
            required: [productId, quantity]
            properties:
              productId:
                type: string
                format: uuid
              quantity:
                type: integer
                minimum: 1

    CursorPagination:
      type: object
      properties:
        nextCursor:
          type: string
          nullable: true
        hasMore:
          type: boolean

    ProblemDetail:
      type: object
      properties:
        type:
          type: string
          format: uri
        title:
          type: string
        status:
          type: integer
        detail:
          type: string
        instance:
          type: string
          format: uri
        errors:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              message:
                type: string

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

### Step 3: Design GraphQL APIs

**Schema Design Example**:

```graphql
# schema.graphql

type Query {
  """Fetch a single order by ID."""
  order(id: ID!): Order

  """List orders with filtering and pagination."""
  orders(
    filter: OrderFilter
    first: Int = 20
    after: String
  ): OrderConnection!

  """Search products by text query."""
  searchProducts(query: String!, first: Int = 10): ProductConnection!
}

type Mutation {
  """Create a new order from cart items."""
  createOrder(input: CreateOrderInput!): CreateOrderPayload!

  """Cancel an existing order with a reason."""
  cancelOrder(input: CancelOrderInput!): CancelOrderPayload!

  """Add a line item to a draft order."""
  addOrderLine(input: AddOrderLineInput!): AddOrderLinePayload!
}

type Subscription {
  """Stream order status updates in real time."""
  orderStatusChanged(orderId: ID!): OrderStatusEvent!
}

# --- Types ---

type Order implements Node {
  id: ID!
  customer: Customer!
  status: OrderStatus!
  lines: [OrderLine!]!
  total: Money!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type OrderLine {
  product: Product!
  unitPrice: Money!
  quantity: Int!
  lineTotal: Money!
}

type Money {
  amount: Int!
  currency: Currency!
  formatted: String!
}

enum OrderStatus {
  DRAFT
  PLACED
  CONFIRMED
  SHIPPED
  DELIVERED
  CANCELLED
}

enum Currency {
  USD
  EUR
  GBP
}

# --- Connections (Relay-style pagination) ---

type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type OrderEdge {
  node: Order!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# --- Inputs ---

input CreateOrderInput {
  customerId: ID!
  lines: [OrderLineInput!]!
}

input OrderLineInput {
  productId: ID!
  quantity: Int!
}

input CancelOrderInput {
  orderId: ID!
  reason: String!
}

input AddOrderLineInput {
  orderId: ID!
  productId: ID!
  quantity: Int!
}

input OrderFilter {
  status: OrderStatus
  customerId: ID
  createdAfter: DateTime
  createdBefore: DateTime
}

# --- Payloads (union for errors) ---

type CreateOrderPayload {
  order: Order
  errors: [UserError!]!
}

type CancelOrderPayload {
  order: Order
  errors: [UserError!]!
}

type AddOrderLinePayload {
  order: Order
  errors: [UserError!]!
}

type UserError {
  field: String
  message: String!
  code: ErrorCode!
}

enum ErrorCode {
  VALIDATION_ERROR
  NOT_FOUND
  CONFLICT
  UNAUTHORIZED
}

# --- Events ---

type OrderStatusEvent {
  orderId: ID!
  previousStatus: OrderStatus!
  newStatus: OrderStatus!
  occurredAt: DateTime!
}

interface Node {
  id: ID!
}

scalar DateTime
```

**Preventing N+1 Queries with DataLoader**:

```python
# graphql/dataloaders.py
from aiodataloader import DataLoader

class ProductLoader(DataLoader):
    """Batches individual product lookups into a single query."""

    def __init__(self, product_repo):
        super().__init__()
        self._repo = product_repo

    async def batch_load_fn(self, product_ids: list[str]):
        products = await self._repo.find_by_ids(product_ids)
        product_map = {p.id: p for p in products}
        return [product_map.get(pid) for pid in product_ids]

# graphql/resolvers.py
async def resolve_order_line_product(line, info):
    return await info.context["product_loader"].load(line.product_id)
```

### Step 4: Design gRPC APIs

**Protobuf Service Definition**:

```protobuf
// order_service.proto
syntax = "proto3";

package commerce.orders.v1;

option go_package = "github.com/example/commerce/orders/v1;ordersv1";
option java_package = "com.example.commerce.orders.v1";

import "google/protobuf/timestamp.proto";
import "google/protobuf/field_mask.proto";

// OrderService manages the order lifecycle.
service OrderService {
  // CreateOrder creates a new order from the provided line items.
  rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse);

  // GetOrder retrieves a single order by ID.
  rpc GetOrder(GetOrderRequest) returns (Order);

  // ListOrders returns a paginated list of orders.
  rpc ListOrders(ListOrdersRequest) returns (ListOrdersResponse);

  // CancelOrder cancels an existing order.
  rpc CancelOrder(CancelOrderRequest) returns (Order);

  // WatchOrderStatus streams order status changes in real time.
  rpc WatchOrderStatus(WatchOrderStatusRequest)
      returns (stream OrderStatusEvent);
}

message Order {
  string id = 1;
  string customer_id = 2;
  OrderStatus status = 3;
  repeated OrderLine lines = 4;
  Money total = 5;
  google.protobuf.Timestamp created_at = 6;
  google.protobuf.Timestamp updated_at = 7;
}

message OrderLine {
  string product_id = 1;
  string product_name = 2;
  Money unit_price = 3;
  int32 quantity = 4;
}

message Money {
  int64 amount = 1;          // Smallest currency unit (cents)
  string currency_code = 2;  // ISO 4217 (e.g., "USD")
}

enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_DRAFT = 1;
  ORDER_STATUS_PLACED = 2;
  ORDER_STATUS_CONFIRMED = 3;
  ORDER_STATUS_SHIPPED = 4;
  ORDER_STATUS_DELIVERED = 5;
  ORDER_STATUS_CANCELLED = 6;
}

message CreateOrderRequest {
  string customer_id = 1;
  repeated CreateOrderLineItem lines = 2;
}

message CreateOrderLineItem {
  string product_id = 1;
  int32 quantity = 2;
}

message CreateOrderResponse {
  Order order = 1;
}

message GetOrderRequest {
  string id = 1;
}

message ListOrdersRequest {
  int32 page_size = 1;      // Max 100
  string page_token = 2;     // Opaque cursor
  OrderStatus status_filter = 3;
  string customer_id_filter = 4;
}

message ListOrdersResponse {
  repeated Order orders = 1;
  string next_page_token = 2;
  int32 total_count = 3;
}

message CancelOrderRequest {
  string order_id = 1;
  string reason = 2;
}

message WatchOrderStatusRequest {
  string order_id = 1;
}

message OrderStatusEvent {
  string order_id = 1;
  OrderStatus previous_status = 2;
  OrderStatus new_status = 3;
  google.protobuf.Timestamp occurred_at = 4;
}
```

### Step 5: Implement Error Handling

**RFC 7807 Problem Details (REST)**:

```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "The request body contains invalid fields.",
  "instance": "/orders/abc-123",
  "errors": [
    {
      "field": "lines[0].quantity",
      "message": "Quantity must be a positive integer.",
      "code": "INVALID_VALUE"
    },
    {
      "field": "customerId",
      "message": "Customer not found.",
      "code": "RESOURCE_NOT_FOUND"
    }
  ]
}
```

**Standard Error Types**:

```
Type URI                                    Status  When to Use
-----------------------------------         ------  -----------
/errors/validation-error                    422     Invalid request body fields
/errors/resource-not-found                  404     Entity does not exist
/errors/conflict                            409     Optimistic lock failure, duplicate
/errors/unauthorized                        401     Missing or invalid credentials
/errors/forbidden                           403     Valid credentials, insufficient permissions
/errors/rate-limited                        429     Too many requests
/errors/internal-error                      500     Unexpected server failure
/errors/service-unavailable                 503     Dependency down, circuit open
```

**Error Handling Implementation (Node.js/Express)**:

```typescript
// middleware/error-handler.ts
import { Request, Response, NextFunction } from "express";

interface ProblemDetail {
  type: string;
  title: string;
  status: number;
  detail: string;
  instance?: string;
  errors?: Array<{ field: string; message: string; code: string }>;
}

export class AppError extends Error {
  constructor(
    public status: number,
    public type: string,
    public title: string,
    public detail: string,
    public fieldErrors?: Array<{ field: string; message: string; code: string }>
  ) {
    super(detail);
  }
}

export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  _next: NextFunction
): void {
  if (err instanceof AppError) {
    const problem: ProblemDetail = {
      type: `https://api.example.com/errors/${err.type}`,
      title: err.title,
      status: err.status,
      detail: err.detail,
      instance: req.originalUrl,
    };
    if (err.fieldErrors) {
      problem.errors = err.fieldErrors;
    }
    res.status(err.status)
      .contentType("application/problem+json")
      .json(problem);
    return;
  }

  // Unexpected errors: log full details, return minimal info
  console.error("Unhandled error:", err);
  res.status(500)
    .contentType("application/problem+json")
    .json({
      type: "https://api.example.com/errors/internal-error",
      title: "Internal Server Error",
      status: 500,
      detail: "An unexpected error occurred. Please try again later.",
      instance: req.originalUrl,
    });
}
```

### Step 6: Implement Pagination

**Cursor-Based Pagination (recommended for most cases)**:

```python
# Encoding/decoding cursors
import base64, json

def encode_cursor(data: dict) -> str:
    return base64.urlsafe_b64encode(
        json.dumps(data).encode()
    ).decode()

def decode_cursor(cursor: str) -> dict:
    return json.loads(
        base64.urlsafe_b64decode(cursor.encode())
    )

# Query implementation
async def list_orders(
    status: str | None = None,
    cursor: str | None = None,
    limit: int = 20,
) -> dict:
    query = "SELECT * FROM orders"
    params = []
    conditions = []

    if status:
        conditions.append("status = %s")
        params.append(status)

    if cursor:
        decoded = decode_cursor(cursor)
        conditions.append("(created_at, id) < (%s, %s)")
        params.extend([decoded["created_at"], decoded["id"]])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY created_at DESC, id DESC LIMIT %s"
    params.append(limit + 1)  # Fetch one extra to detect hasMore

    rows = await db.fetch(query, params)
    has_more = len(rows) > limit
    items = rows[:limit]

    next_cursor = None
    if has_more and items:
        last = items[-1]
        next_cursor = encode_cursor({
            "created_at": last["created_at"].isoformat(),
            "id": str(last["id"]),
        })

    return {
        "data": items,
        "pagination": {
            "nextCursor": next_cursor,
            "hasMore": has_more,
        },
    }
```

### Step 7: API Versioning Strategy

**Comparison of Versioning Approaches**:

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| URL path | `/v1/orders` | Simple, explicit, cacheable | Breaks client URLs on version bump |
| Custom header | `X-API-Version: 2` | URLs stay stable | Easy to forget, not cacheable by URL |
| Content negotiation | `Accept: application/vnd.example.v2+json` | Semantically correct | Complex, poor tooling support |
| Query parameter | `/orders?version=2` | Simple to test | Pollutes query string, caching issues |

**Recommended: URL Path Versioning with Sunset Headers**:

```
# Current version
GET /v2/orders HTTP/1.1

# Response for deprecated version
HTTP/1.1 200 OK
Sunset: Sat, 01 Jun 2026 00:00:00 GMT
Deprecation: true
Link: <https://api.example.com/v2/orders>; rel="successor-version"
```

**Rate Limiting Headers**:

```
HTTP/1.1 200 OK
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 742
X-RateLimit-Reset: 1709510400

# When rate limited:
HTTP/1.1 429 Too Many Requests
Retry-After: 30
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1709510400
```

## Best Practices

- **Design the API before writing code** - Contract-first development prevents drift
- **Use consistent naming** - Pick camelCase or snake_case and stick with it project-wide
- **Return appropriate status codes** - 201 for creation, 204 for deletion, 422 for validation
- **Always paginate list endpoints** - Even if you think the list will be small
- **Version from day one** - Adding versioning later is painful
- **Use RFC 7807 for errors** - Structured errors are machine-parseable and debuggable
- **Include rate limit headers** - Clients need to know their quota without guessing
- **Make APIs idempotent** - Use idempotency keys for POST operations
- **Document every endpoint** - Undocumented APIs are unusable APIs
- **Validate inputs strictly, accept outputs liberally** - Postel's law applies to APIs

## Common Patterns

### Pattern 1: Idempotency Key for POST

Prevent duplicate resource creation due to retries:

```
POST /v1/orders HTTP/1.1
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
Content-Type: application/json

{"customerId": "abc", "lines": [...]}
```

```python
# Server-side idempotency check
async def create_order(request):
    key = request.headers.get("Idempotency-Key")
    if key:
        cached = await redis.get(f"idempotency:{key}")
        if cached:
            return json.loads(cached)  # Return same response

    order = await order_service.create(request.json)
    response = serialize(order)

    if key:
        await redis.set(f"idempotency:{key}", json.dumps(response),
                        ex=86400)  # 24-hour TTL
    return response, 201
```

### Pattern 2: HATEOAS Links for Discoverability

```json
{
  "id": "order-123",
  "status": "placed",
  "total": {"amount": 4999, "currency": "USD"},
  "_links": {
    "self": {"href": "/v1/orders/order-123"},
    "cancel": {"href": "/v1/orders/order-123/cancel", "method": "POST"},
    "customer": {"href": "/v1/customers/cust-456"},
    "lines": {"href": "/v1/orders/order-123/lines"}
  }
}
```

### Pattern 3: Bulk Operations

```
POST /v1/orders/bulk HTTP/1.1
Content-Type: application/json

{
  "operations": [
    {"method": "POST", "body": {"customerId": "a", "lines": [...]}},
    {"method": "POST", "body": {"customerId": "b", "lines": [...]}}
  ]
}

HTTP/1.1 207 Multi-Status
{
  "results": [
    {"status": 201, "body": {"id": "order-1", ...}},
    {"status": 422, "body": {"type": "/errors/validation-error", ...}}
  ]
}
```

## Quality Checklist

- [ ] All resources use plural nouns (not verbs) in URL paths
- [ ] HTTP methods used correctly (GET is safe, PUT is idempotent)
- [ ] Status codes are specific and correct (not 200 for everything)
- [ ] Error responses follow RFC 7807 Problem Details format
- [ ] All list endpoints are paginated (cursor-based preferred)
- [ ] API is versioned from the initial release
- [ ] Rate limit headers included in every response
- [ ] Authentication scheme documented (Bearer token, API key)
- [ ] OpenAPI/GraphQL schema/proto files are the source of truth
- [ ] Breaking changes go through a deprecation cycle with Sunset headers
- [ ] Idempotency keys supported for state-changing POST operations
- [ ] Request/response examples provided for every endpoint

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "We'll version the API when we need to break it" | Adding versioning to an unversioned API requires coordinating all consumers simultaneously; the Stripe API has never forced a breaking change on consumers precisely because versioning was built in from day one. |
| "Error codes don't matter, clients just check HTTP status" | Undifferentiated 400 responses with no error code force clients to parse free-text error messages to distinguish "invalid email format" from "email already exists", creating brittle integrations that break when wording changes. |
| "Cursor-based pagination is too complex; offset is fine" | Offset pagination silently skips or duplicates records when items are inserted or deleted between pages; this causes data loss in exports and duplicate processing in event consumers at any non-trivial insert rate. |
| "The OpenAPI spec is documentation, not the source of truth" | When code and spec diverge, the spec becomes actively harmful — clients build to the spec and encounter runtime errors; contract-first development enforces equivalence at every build. |
| "We'll add rate limiting after launch if it becomes a problem" | Unrated endpoints have been used in credential-stuffing attacks that generated millions of login attempts within minutes of launch; retroactively adding rate limiting to a live API requires coordinating with all existing integrations. |
| "GraphQL means we don't need to worry about over-fetching" | GraphQL eliminates over-fetching at the field level but introduces N+1 query problems at the resolver level; without DataLoader or query depth limits, a single client request can trigger thousands of database queries. |

## Verification

- [ ] API versioning strategy is implemented (URL path, header, or content-type negotiation) and documented
- [ ] All error responses conform to RFC 7807 Problem Details with a machine-readable `type` and `code` field
- [ ] Pagination is implemented with cursor-based or keyset approach for all list endpoints (no raw offset on mutable collections)
- [ ] OpenAPI, GraphQL SDL, or proto file is checked into source control and matches the deployed API behavior
- [ ] Rate limiting headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`) are returned on throttled responses
- [ ] All state-changing POST endpoints that may be retried support idempotency keys

## Related Skills

- `architecture-design` - System-level architecture that APIs expose
- `ddd-strategic-design` - Published language and open host service patterns
- `api-documentation` - Generating and maintaining API reference docs
- `security-review` - Authentication, authorization, and API security audit
- `performance-review` - API latency optimization and caching strategies

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
