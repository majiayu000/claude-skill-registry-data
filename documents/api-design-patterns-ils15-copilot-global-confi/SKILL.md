---
name: api-design-patterns
description: Design RESTful APIs with proper HTTP methods, status codes, pagination, filtering, error responses, and OpenAPI documentation. Follows FastAPI best practices with Pydantic validation.
---

# API Design Patterns Skill

## When to Use

Use this skill when:
- Designing new API endpoints
- Reviewing API consistency
- Implementing pagination and filtering
- Creating error response formats
- Writing OpenAPI documentation
- Validating HTTP status codes
- Building request/response schemas

## RESTful Design Principles

### 1. HTTP Methods

```
GET    /users          - List users
GET    /users/{id}     - Get single user
POST   /users          - Create user
PUT    /users/{id}     - Full update
PATCH  /users/{id}     - Partial update
DELETE /users/{id}     - Delete user
```

### 2. Status Codes

```
2xx Success:
- 200 OK              - Successful GET, PUT, PATCH
- 201 Created         - Successful POST
- 204 No Content      - Successful DELETE

4xx Client Errors:
- 400 Bad Request     - Invalid input
- 401 Unauthorized    - Not authenticated
- 403 Forbidden       - Not authorized
- 404 Not Found       - Resource not found
- 409 Conflict        - Duplicate resource
- 422 Unprocessable   - Validation error

5xx Server Errors:
- 500 Internal Error  - Unexpected error
- 503 Service Unavail - Maintenance
```

### 3. Pagination Pattern

```python
from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    
    class Config:
        from_attributes = True

# Endpoint
@router.get("/users", response_model=PaginatedResponse[UserResponse])
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    total = await user_service.count()
    items = await user_service.get_page(page, size)
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )
```

### 4. Filtering Pattern

```python
from typing import Optional
from fastapi import Query

@router.get("/products")
async def list_products(
    # Search
    q: Optional[str] = Query(None, min_length=2, max_length=100),
    
    # Filters
    category: Optional[str] = None,
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    in_stock: Optional[bool] = None,
    
    # Sorting
    sort_by: str = Query("created_at", regex="^(name|price|created_at)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    
    # Pagination
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    return await product_service.search(
        q=q, category=category, 
        min_price=min_price, max_price=max_price,
        in_stock=in_stock,
        sort_by=sort_by, order=order,
        page=page, size=size
    )
```

### 5. Error Response Format

```python
from pydantic import BaseModel
from typing import Optional, List

class ErrorDetail(BaseModel):
    loc: List[str]
    msg: str
    type: str

class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[List[ErrorDetail]] = None
    request_id: Optional[str] = None

# Usage
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            message=str(exc.detail),
            request_id=request.state.request_id
        ).model_dump()
    )
```

### 6. Request/Response Schemas

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# Create (input)
class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8)

# Update (partial)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=2, max_length=100)

# Response (output)
class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# List response
class UserListResponse(BaseModel):
    id: int
    name: str  # Minimal fields for list
```

### 7. OpenAPI Documentation

```python
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
    summary="Create a new user",
    description="Register a new user account with email and password.",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Invalid input data"},
        409: {"description": "Email already exists"},
    },
    tags=["users"],
)
async def create_user(user: UserCreate):
    """
    Create a new user with the following information:
    
    - **email**: valid email address (unique)
    - **name**: user display name (2-100 chars)
    - **password**: secure password (min 8 chars)
    """
    return await user_service.create(user)
```

## Output Format

```markdown
## API Design Review

### Endpoints Analyzed
- GET /users - ✅ Correct
- POST /users - ⚠️ Missing 409 response
- DELETE /users/{id} - ❌ Returns 200 (should be 204)

### Issues Found
1. [Endpoint] - [Issue] - [Fix]

### Recommendations
1. Add pagination to list endpoints
2. Standardize error response format
3. Add request_id to all responses
```

## Example Usage

```
@backend Design CRUD endpoints for products resource
@backend Review API consistency across all endpoints
@backend Add pagination to the orders list endpoint
@backend Create error response schema for the API
```
