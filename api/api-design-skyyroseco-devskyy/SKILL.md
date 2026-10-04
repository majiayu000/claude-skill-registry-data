---
name: api-design
description: REST API design patterns including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting for production APIs. Use when designing or reviewing HTTP API endpoints, contracts, pagination, error formats, versioning, or rate limits. Do NOT use for GraphQL schema design (api/graphql/), MCP tool schemas (devskyy_mcp.py), or internal function signatures — this covers the HTTP/REST surface only.
origin: ECC
---

# API Design Patterns

Conventions and best practices for designing consistent, developer-friendly REST APIs.

## When to use

- Designing new API endpoints
- Reviewing existing API contracts
- Adding pagination, filtering, or sorting
- Implementing error handling for APIs
- Planning API versioning strategy
- Building public or partner-facing APIs

**When NOT to use:**

- GraphQL schema/resolver design (`api/graphql/`) — type and resolver rules differ from REST resource rules
- MCP tool definitions (`devskyy_mcp.py`) — tool schemas, not HTTP resources
- WordPress REST conventions on skyyrose.co — that surface follows WordPress core patterns, owned by the `wp-rest-api` skill

## Inputs

Required before starting. **Absent input = stop** — never proceed by inventing a convention.

- **The existing API surface being extended.** In this repo: FastAPI routers under `api/v1/` and `api/v2/`, mounted by `main_enterprise.py`. Read the sibling router closest to the new resource first.
- **The conventions already in force** — envelope shape, naming case, auth dependency, error format — taken from that sibling router, not from this document's defaults. A second convention that is internally consistent is still a defect.
- **The boundary-validation library**: Pydantic for the Python backend, Zod for Next.js routes (`frontend/`).
- **The consumer contract**, when one exists (OpenAPI spec, frontend caller, partner doc). If the consumer's field names cannot be located, stop and ask — do not guess them.

## Procedure

1. Read the nearest existing router (`api/v1/<domain>.py`) and record its envelope, naming case, auth dependency, and error shape.
2. Design the URL per **Resource Design** below — plural noun, kebab-case; verbs only for non-CRUD actions.
3. Pick method and status codes from the tables below: 201 + `Location` for creates, 204 for deletes, 4xx for client errors — never 200-for-everything.
4. Define request/response schemas with validation at the boundary (Pydantic/Zod), field-level details per the **Error Response** format.
5. For list endpoints, choose pagination from the cursor-vs-offset table; add filtering/sorting only where a consumer needs it.
6. Wire authentication and a rate-limit tier from the tables below; an intentionally public endpoint says so explicitly.
7. Walk the **API Design Checklist**; every unchecked box is either fixed or named as a known gap in the deliverable.
8. Run every command in **Verification** and report the observed output with evidence-scope tags.

## Resource Design

### URL Structure

```
# Resources are nouns, plural, lowercase, kebab-case
GET    /api/v1/users
GET    /api/v1/users/:id
POST   /api/v1/users
PUT    /api/v1/users/:id
PATCH  /api/v1/users/:id
DELETE /api/v1/users/:id

# Sub-resources for relationships
GET    /api/v1/users/:id/orders
POST   /api/v1/users/:id/orders

# Actions that don't map to CRUD (use verbs sparingly)
POST   /api/v1/orders/:id/cancel
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
```

### Naming Rules

```
# GOOD
/api/v1/team-members          # kebab-case for multi-word resources
/api/v1/orders?status=active  # query params for filtering
/api/v1/users/123/orders      # nested resources for ownership

# BAD
/api/v1/getUsers              # verb in URL
/api/v1/user                  # singular (use plural)
/api/v1/team_members          # snake_case in URLs
/api/v1/users/123/getOrders   # verb in nested resource
```

## HTTP Methods and Status Codes

### Method Semantics

| Method | Idempotent | Safe | Use For |
|--------|-----------|------|---------|
| GET | Yes | Yes | Retrieve resources |
| POST | No | No | Create resources, trigger actions |
| PUT | Yes | No | Full replacement of a resource |
| PATCH | No* | No | Partial update of a resource |
| DELETE | Yes | No | Remove a resource |

*PATCH can be made idempotent with proper implementation

### Status Code Reference

```
# Success
200 OK                    — GET, PUT, PATCH (with response body)
201 Created               — POST (include Location header)
204 No Content            — DELETE, PUT (no response body)

# Client Errors
400 Bad Request           — Validation failure, malformed JSON
401 Unauthorized          — Missing or invalid authentication
403 Forbidden             — Authenticated but not authorized
404 Not Found             — Resource doesn't exist
409 Conflict              — Duplicate entry, state conflict
422 Unprocessable Entity  — Semantically invalid (valid JSON, bad data)
429 Too Many Requests     — Rate limit exceeded

# Server Errors
500 Internal Server Error — Unexpected failure (never expose details)
502 Bad Gateway           — Upstream service failed
503 Service Unavailable   — Temporary overload, include Retry-After
```

### Common Mistakes

```
# BAD: 200 for everything
{ "status": 200, "success": false, "error": "Not found" }

# GOOD: Use HTTP status codes semantically
HTTP/1.1 404 Not Found
{ "error": { "code": "not_found", "message": "User not found" } }

# BAD: 500 for validation errors
# GOOD: 400 or 422 with field-level details

# BAD: 200 for created resources
# GOOD: 201 with Location header
HTTP/1.1 201 Created
Location: /api/v1/users/abc-123
```

## Response Format

### Success Response

```json
{
  "data": {
    "id": "abc-123",
    "email": "alice@example.com",
    "name": "Alice",
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

### Collection Response (with Pagination)

```json
{
  "data": [
    { "id": "abc-123", "name": "Alice" },
    { "id": "def-456", "name": "Bob" }
  ],
  "meta": {
    "total": 142,
    "page": 1,
    "per_page": 20,
    "total_pages": 8
  },
  "links": {
    "self": "/api/v1/users?page=1&per_page=20",
    "next": "/api/v1/users?page=2&per_page=20",
    "last": "/api/v1/users?page=8&per_page=20"
  }
}
```

### Error Response

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address",
        "code": "invalid_format"
      },
      {
        "field": "age",
        "message": "Must be between 0 and 150",
        "code": "out_of_range"
      }
    ]
  }
}
```

### Response Envelope Variants

```typescript
// Option A: Envelope with data wrapper (recommended for public APIs)
interface ApiResponse<T> {
  data: T;
  meta?: PaginationMeta;
  links?: PaginationLinks;
}

interface ApiError {
  error: {
    code: string;
    message: string;
    details?: FieldError[];
  };
}

// Option B: Flat response (simpler, common for internal APIs)
// Success: just return the resource directly
// Error: return error object
// Distinguish by HTTP status code
```

## Pagination

### Offset-Based (Simple)

```
GET /api/v1/users?page=2&per_page=20

# Implementation
SELECT * FROM users
ORDER BY created_at DESC
LIMIT 20 OFFSET 20;
```

**Pros:** Easy to implement, supports "jump to page N"
**Cons:** Slow on large offsets (OFFSET 100000), inconsistent with concurrent inserts

### Cursor-Based (Scalable)

```
GET /api/v1/users?cursor=eyJpZCI6MTIzfQ&limit=20

# Implementation
SELECT * FROM users
WHERE id > :cursor_id
ORDER BY id ASC
LIMIT 21;  -- fetch one extra to determine has_next
```

```json
{
  "data": [...],
  "meta": {
    "has_next": true,
    "next_cursor": "eyJpZCI6MTQzfQ"
  }
}
```

**Pros:** Consistent performance regardless of position, stable with concurrent inserts
**Cons:** Cannot jump to arbitrary page, cursor is opaque

### When to Use Which

| Use Case | Pagination Type |
|----------|----------------|
| Admin dashboards, small datasets (<10K) | Offset |
| Infinite scroll, feeds, large datasets | Cursor |
| Public APIs | Cursor (default) with offset (optional) |
| Search results | Offset (users expect page numbers) |

## Filtering, Sorting, and Search

### Filtering

```
# Simple equality
GET /api/v1/orders?status=active&customer_id=abc-123

# Comparison operators (use bracket notation)
GET /api/v1/products?price[gte]=10&price[lte]=100
GET /api/v1/orders?created_at[after]=2025-01-01

# Multiple values (comma-separated)
GET /api/v1/products?category=electronics,clothing

# Nested fields (dot notation)
GET /api/v1/orders?customer.country=US
```

### Sorting

```
# Single field (prefix - for descending)
GET /api/v1/products?sort=-created_at

# Multiple fields (comma-separated)
GET /api/v1/products?sort=-featured,price,-created_at
```

### Full-Text Search

```
# Search query parameter
GET /api/v1/products?q=wireless+headphones

# Field-specific search
GET /api/v1/users?email=alice
```

### Sparse Fieldsets

```
# Return only specified fields (reduces payload)
GET /api/v1/users?fields=id,name,email
GET /api/v1/orders?fields=id,total,status&include=customer.name
```

## Authentication and Authorization

### Token-Based Auth

```
# Bearer token in Authorization header
GET /api/v1/users
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

# API key (for server-to-server)
GET /api/v1/data
X-API-Key: sk_live_abc123
```

### Authorization Patterns

```typescript
// Resource-level: check ownership
app.get("/api/v1/orders/:id", async (req, res) => {
  const order = await Order.findById(req.params.id);
  if (!order) return res.status(404).json({ error: { code: "not_found" } });
  if (order.userId !== req.user.id) return res.status(403).json({ error: { code: "forbidden" } });
  return res.json({ data: order });
});

// Role-based: check permissions
app.delete("/api/v1/users/:id", requireRole("admin"), async (req, res) => {
  await User.delete(req.params.id);
  return res.status(204).send();
});
```

## Rate Limiting

### Headers

```
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000

# When exceeded
HTTP/1.1 429 Too Many Requests
Retry-After: 60
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Rate limit exceeded. Try again in 60 seconds."
  }
}
```

### Rate Limit Tiers

| Tier | Limit | Window | Use Case |
|------|-------|--------|----------|
| Anonymous | 30/min | Per IP | Public endpoints |
| Authenticated | 100/min | Per user | Standard API access |
| Premium | 1000/min | Per API key | Paid API plans |
| Internal | 10000/min | Per service | Service-to-service |

## Versioning

### URL Path Versioning (Recommended)

```
/api/v1/users
/api/v2/users
```

**Pros:** Explicit, easy to route, cacheable
**Cons:** URL changes between versions

### Header Versioning

```
GET /api/users
Accept: application/vnd.myapp.v2+json
```

**Pros:** Clean URLs
**Cons:** Harder to test, easy to forget

### Versioning Strategy

```
1. Start with /api/v1/ — don't version until you need to
2. Maintain at most 2 active versions (current + previous)
3. Deprecation timeline:
   - Announce deprecation (6 months notice for public APIs)
   - Add Sunset header: Sunset: Sat, 01 Jan 2026 00:00:00 GMT
   - Return 410 Gone after sunset date
4. Non-breaking changes don't need a new version:
   - Adding new fields to responses
   - Adding new optional query parameters
   - Adding new endpoints
5. Breaking changes require a new version:
   - Removing or renaming fields
   - Changing field types
   - Changing URL structure
   - Changing authentication method
```

## Implementation Patterns

### TypeScript (Next.js API Route)

```typescript
import { z } from "zod";
import { NextRequest, NextResponse } from "next/server";

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

export async function POST(req: NextRequest) {
  const body = await req.json();
  const parsed = createUserSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json({
      error: {
        code: "validation_error",
        message: "Request validation failed",
        details: parsed.error.issues.map(i => ({
          field: i.path.join("."),
          message: i.message,
          code: i.code,
        })),
      },
    }, { status: 422 });
  }

  const user = await createUser(parsed.data);

  return NextResponse.json(
    { data: user },
    {
      status: 201,
      headers: { Location: `/api/v1/users/${user.id}` },
    },
  );
}
```

### Python (Django REST Framework)

```python
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response

class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=100)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "created_at"]

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUserSerializer
        return UserSerializer

    def create(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserService.create(**serializer.validated_data)
        return Response(
            {"data": UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
            headers={"Location": f"/api/v1/users/{user.id}"},
        )
```

### Go (net/http)

```go
func (h *UserHandler) CreateUser(w http.ResponseWriter, r *http.Request) {
    var req CreateUserRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        writeError(w, http.StatusBadRequest, "invalid_json", "Invalid request body")
        return
    }

    if err := req.Validate(); err != nil {
        writeError(w, http.StatusUnprocessableEntity, "validation_error", err.Error())
        return
    }

    user, err := h.service.Create(r.Context(), req)
    if err != nil {
        switch {
        case errors.Is(err, domain.ErrEmailTaken):
            writeError(w, http.StatusConflict, "email_taken", "Email already registered")
        default:
            writeError(w, http.StatusInternalServerError, "internal_error", "Internal error")
        }
        return
    }

    w.Header().Set("Location", fmt.Sprintf("/api/v1/users/%s", user.ID))
    writeJSON(w, http.StatusCreated, map[string]any{"data": user})
}
```

## API Design Checklist

Before shipping a new endpoint:

- [ ] Resource URL follows naming conventions (plural, kebab-case, no verbs)
- [ ] Correct HTTP method used (GET for reads, POST for creates, etc.)
- [ ] Appropriate status codes returned (not 200 for everything)
- [ ] Input validated with schema (Zod, Pydantic, Bean Validation)
- [ ] Error responses follow standard format with codes and messages
- [ ] Pagination implemented for list endpoints (cursor or offset)
- [ ] Authentication required (or explicitly marked as public)
- [ ] Authorization checked (user can only access their own resources)
- [ ] Rate limiting configured
- [ ] Response does not leak internal details (stack traces, SQL errors)
- [ ] Consistent naming with existing endpoints (camelCase vs snake_case)
- [ ] Documented (OpenAPI/Swagger spec updated)

## Verification

Run from the repo root. All three commands confirmed runnable in this repo on 2026-07-29.

1. The OpenAPI schema still builds with the change mounted:

```bash
python3 -c "from main_enterprise import app; spec = app.openapi(); print('openapi', spec['openapi'], '| paths:', len(spec['paths']))"
```

**PASS:** exits 0 and prints spec version + path count (baseline 2026-07-29: `openapi 3.1.0 | paths: 288`). A traceback is a FAIL. `[repro]`

2. No duplicate operation IDs — duplicates silently corrupt OpenAPI-driven client generators:

```bash
python3 -W error::UserWarning -c "from main_enterprise import app; app.openapi(); print('operation ids unique')"
```

**PASS:** prints `operation ids unique` and exits 0. Baseline is currently RED (observed 2026-07-29, exit 1): 3 pre-existing duplicates — `list_tools` and `test_tool` in `api/tools.py`, `list_agents` in `api/v1/monitoring.py`. Per rule 4 of `docs/skill-authoring-standard.md`, diff the warning *list*, not the exit code: the change passes when it adds zero NEW duplicates. `[repro]`

3. API contract tests stay green:

```bash
rtk proxy pytest tests/api -q
```

**PASS:** exits 0, all collected tests pass. Use `rtk proxy`, never bare pytest — bare `python3 -m pytest tests/api -q --co` falsely reported "No tests collected" in this session while `rtk proxy` collected 37 tests across 4 files. `[test]`

## Worked example

Invoked 2026-07-29 in this worktree, auditing the mounted surface before endpoint work. Real commands, real observed output:

```text
$ python3 -c "from main_enterprise import app; spec = app.openapi(); print('openapi', spec['openapi'], '| paths:', len(spec['paths']))"
openapi 3.1.0 | paths: 288

$ python3 -W error::UserWarning -c "from main_enterprise import app; app.openapi(); print('operation ids unique')"
UserWarning: Duplicate Operation ID list_tools_api_v1_tools_get for function list_tools at .../api/tools.py
(exit 1)

$ rtk proxy pytest tests/api/test_ml_predict.py -q
.....                                                                    [100%]
```

Finding from check 2: the generated spec contains colliding `operationId`s for `list_tools`/`test_tool` (`api/tools.py`) and `list_agents` (`api/v1/monitoring.py`), so a generated client would overwrite one method with the other. Scope: `[repro]` — schema-build observation only; live behavior of api.devskyy.app was not probed this session.

## Failure modes

- **200-for-everything** — error state hidden in the body; monitors and clients cannot distinguish outcomes. See *Common Mistakes* above.
- **Duplicate operation IDs** from copy-pasted handlers or double-mounted routers. Symptom: `UserWarning` at schema build (real instance observed 2026-07-29, Verification check 2). Consequence: OpenAPI client generators key on `operationId` and drop one of the two operations.
- **Second-convention drift** — a new endpoint that invents its own envelope/naming instead of matching its sibling router. Passes its own tests, fails integration review.
- **Breaking change shipped as an addition** — field rename or type change without a version bump. The *Versioning Strategy* section defines what counts as breaking.
- No `bug-NNN` id is cited above; when one of these bites in production, log it to `.wolf/buglog.json` and reference the id here.
