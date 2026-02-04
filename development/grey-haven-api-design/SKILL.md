---
name: grey-haven-api-design
description: "Design RESTful APIs following Grey Haven standards - FastAPI routes, Pydantic schemas, HTTP status codes, pagination, filtering, error responses, OpenAPI docs, and multi-tenant patterns. Use when creating API endpoints, designing REST resources, implementing server functions, configuring FastAPI, writing Pydantic schemas, setting up error handling, implementing pagination, or when user mentions 'API', 'endpoint', 'REST', 'FastAPI', 'Pydantic', 'server function', 'OpenAPI', 'pagination', 'validation', 'error handling', 'rate limiting', 'CORS', or 'authentication'."
# v2.0.43: Skills to auto-load for API design
skills:
  - grey-haven-code-style
  - grey-haven-data-validation
  - grey-haven-security-practices
# v2.0.74: Tools for API implementation
allowed-tools:
  - Read
  - Write
  - MultiEdit
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# Grey Haven API Design Standards

**RESTful API design for FastAPI backends and TanStack Start server functions.**

Follow these standards when creating API endpoints, defining schemas, and handling errors in Grey Haven projects.

## Supporting Documentation

- **[examples/](examples/)** - Complete endpoint examples (all files <500 lines)
  - [fastapi-crud.md](examples/fastapi-crud.md) - CRUD endpoints with repository pattern
  - [pydantic-schemas.md](examples/pydantic-schemas.md) - Request/response schemas
  - [tanstack-start.md](examples/tanstack-start.md) - Server functions
  - [pagination.md](examples/pagination.md) - Pagination patterns
  - [testing.md](examples/testing.md) - API testing
- **[reference/](reference/)** - Configuration references (all files <500 lines)
  - [fastapi-setup.md](reference/fastapi-setup.md) - Main app configuration
  - [openapi.md](reference/openapi.md) - OpenAPI customization
  - [error-handlers.md](reference/error-handlers.md) - Exception handlers
  - [authentication.md](reference/authentication.md) - JWT configuration
  - [cors-rate-limiting.md](reference/cors-rate-limiting.md) - CORS and rate limiting
- **[templates/](templates/)** - Copy-paste ready endpoint templates
- **[checklists/](checklists/)** - API design and security checklists

## Quick Reference

### RESTful Resource Design

**URL Patterns:**
- ✅ `/api/v1/users` (plural nouns, lowercase with hyphens)
- ✅ `/api/v1/organizations/{org_id}/teams` (hierarchical)
- ❌ `/api/v1/getUsers` (no verbs in URLs)
- ❌ `/api/v1/user_profiles` (no underscores)

**HTTP Verbs:**
- `GET` - Retrieve resources
- `POST` - Create new resources
- `PUT` - Update entire resource
- `PATCH` - Update partial resource
- `DELETE` - Remove resource

### HTTP Status Codes

**Success:**
- `200 OK` - GET, PUT, PATCH requests
- `201 Created` - POST request (resource created)
- `204 No Content` - DELETE request

**Client Errors:**
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing/invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource doesn't exist
- `409 Conflict` - Duplicate resource, concurrent update
- `422 Unprocessable Entity` - Validation errors

**Server Errors:**
- `500 Internal Server Error` - Unhandled exception
- `503 Service Unavailable` - Database/service down

### Multi-Tenant Isolation

**Always enforce tenant isolation:**
```python
# Extract tenant_id from JWT
repository = UserRepository(db, tenant_id=current_user.tenant_id)

# All queries automatically filtered by tenant_id
users = await repository.list()  # Only returns users in this tenant
```

### FastAPI Route Pattern

```python
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """Create a new user in the current tenant."""
    repository = UserRepository(db, tenant_id=current_user.tenant_id)
    user = await repository.create(user_data)
    return user
```

**See [examples/fastapi-crud.md](examples/fastapi-crud.md) for complete CRUD endpoints.**

### Pydantic Schema Pattern

```python
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=8)

class UserRead(BaseModel):
    """Schema for reading user data (public fields only)."""
    id: str
    tenant_id: str
    email: EmailStr
    full_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

**See [examples/pydantic-schemas.md](examples/pydantic-schemas.md) for validation patterns.**

### TanStack Start Server Functions

```typescript
// app/routes/api/users.ts
import { createServerFn } from "@tanstack/start";
import { z } from "zod";

const createUserSchema = z.object({
  email: z.string().email(),
  fullName: z.string().min(1).max(255),
});

export const createUser = createServerFn({ method: "POST" })
  .validator(createUserSchema)
  .handler(async ({ data, context }) => {
    const authUser = await getAuthUser(context);
    // Create user with tenant isolation
  });
```

**See [examples/tanstack-start.md](examples/tanstack-start.md) for complete examples.**

### Error Response Format

```json
{
  "error": "User with ID abc123 not found",
  "status_code": 404
}
```

**Validation errors:**
```json
{
  "error": "Validation error",
  "detail": [
    {
      "field": "email",
      "message": "value is not a valid email address",
      "code": "value_error.email"
    }
  ],
  "status_code": 422
}
```

**See [reference/error-handlers.md](reference/error-handlers.md) for exception handlers.**

### Pagination

**Offset-based (simple):**
```python
@router.get("", response_model=PaginatedResponse[UserRead])
async def list_users(skip: int = 0, limit: int = 100):
    users = await repository.list(skip=skip, limit=limit)
    total = await repository.count()
    return PaginatedResponse(items=users, total=total, skip=skip, limit=limit)
```

**Cursor-based (recommended for large datasets):**
```python
@router.get("")
async def list_users(cursor: Optional[str] = None, limit: int = 100):
    users = await repository.list_cursor(cursor=cursor, limit=limit)
    next_cursor = users[-1].id if len(users) == limit else None
    return {"items": users, "next_cursor": next_cursor}
```

**See [examples/pagination.md](examples/pagination.md) for complete implementations.**

## Core Principles

### 1. Repository Pattern

**Always use tenant-aware repositories:**
- Extract `tenant_id` from JWT claims
- Pass to repository constructor
- All queries automatically filtered
- Prevents cross-tenant data leaks

### 2. Pydantic Validation

**Define schemas for all requests/responses:**
- `{Model}Create` - Fields for creation
- `{Model}Read` - Public fields for responses
- `{Model}Update` - Optional fields for updates
- Never return password hashes or sensitive data

### 3. OpenAPI Documentation

**FastAPI auto-generates docs:**
- Add docstrings to all endpoints
- Use `summary`, `description`, `response_description`
- Document all parameters and responses
- Available at `/docs` (Swagger UI) and `/redoc` (ReDoc)

**See [reference/openapi.md](reference/openapi.md) for customization.**

### 4. Rate Limiting

**Protect public endpoints:**
```python
from app.core.rate_limit import rate_limit

@router.get("", dependencies=[Depends(rate_limit)])
async def list_users():
    """List users (rate limited to 100 req/min)."""
    pass
```

**See [templates/rate-limiter.py](templates/rate-limiter.py) for Upstash Redis implementation.**

### 5. CORS Configuration

**Use Doppler for allowed origins:**
```python
# NEVER hardcode origins in production!
allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
)
```

**See [reference/cors-rate-limiting.md](reference/cors-rate-limiting.md) for complete setup.**

## When to Apply This Skill

Use this skill when:
- ✅ Creating new FastAPI endpoints or TanStack Start server functions
- ✅ Designing RESTful resource hierarchies
- ✅ Writing Pydantic schemas for validation
- ✅ Implementing pagination, filtering, or sorting
- ✅ Configuring error response formats
- ✅ Setting up OpenAPI documentation
- ✅ Implementing rate limiting or CORS
- ✅ Designing multi-tenant API isolation
- ✅ Testing API endpoints with pytest
- ✅ Reviewing API design in pull requests
- ✅ User mentions: "API", "endpoint", "REST", "FastAPI", "Pydantic", "server function", "OpenAPI", "pagination", "validation"

## Template References

These API design patterns come from Grey Haven's actual templates:
- **Backend**: `cvi-backend-template` (FastAPI + SQLModel + Repository Pattern)
- **Frontend**: `cvi-template` (TanStack Start server functions)

## Critical Reminders

1. **Repository pattern** - Always use tenant-aware repositories for multi-tenant isolation
2. **Pydantic schemas** - Never return password hashes or sensitive fields in responses
3. **HTTP status codes** - 201 for create, 204 for delete, 404 for not found, 422 for validation errors
4. **Pagination** - Use cursor-based for large datasets (better performance than offset)
5. **Error format** - Consistent error structure with `error`, `detail`, and `status_code` fields
6. **OpenAPI docs** - Document all parameters, responses, and errors with docstrings
7. **Rate limiting** - Protect public endpoints with Upstash Redis (100 req/min default)
8. **CORS** - Use Doppler for allowed origins, never hardcode in production
9. **JWT authentication** - Extract `tenant_id` from JWT claims for multi-tenant isolation
10. **Testing** - Use FastAPI TestClient with `doppler run --config test -- pytest`

## Next Steps

- **Need endpoint examples?** See [examples/](examples/) for FastAPI CRUD and TanStack Start
- **Need configurations?** See [reference/](reference/) for OpenAPI, CORS, error handlers
- **Need templates?** See [templates/](templates/) for copy-paste ready endpoint code
- **Need checklists?** Use [checklists/](checklists/) for systematic API design reviews
