---
name: fastapi-api-patterns
description: REST API design and implementation patterns for FastAPI endpoints including CRUD operations, pagination, filtering, error handling, and request/response models. Use when building FastAPI endpoints, creating REST APIs, implementing CRUD operations, adding pagination, designing API routes, handling API errors, or when user mentions FastAPI patterns, REST API design, endpoint structure, API best practices, or HTTP endpoints.
allowed-tools: Bash, Read, Write, Edit, WebFetch
---

# fastapi-api-patterns

## Instructions

This skill provides comprehensive REST API design patterns and implementation templates for FastAPI applications. It covers CRUD operations, pagination, filtering, request/response models, error handling, and API organization following modern best practices.

### 1. CRUD Endpoint Patterns

Create, Read, Update, Delete endpoints using FastAPI routers:

```bash
# Use CRUD template to generate complete endpoint set
cp ./skills/fastapi-api-patterns/templates/crud_endpoint.py app/routers/items.py

# Customize for your model
# - Replace Item model with your Pydantic model
# - Update database operations
# - Add authentication dependencies
```

**What This Provides:**
- `POST /items/` - Create new item
- `GET /items/{item_id}` - Read single item by ID
- `GET /items/` - Read multiple items with pagination
- `PUT /items/{item_id}` - Update entire item
- `PATCH /items/{item_id}` - Partial update
- `DELETE /items/{item_id}` - Delete item

**Router Structure:**
```python
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)
```

### 2. Pagination and Filtering

Implement pagination with query parameters:

```bash
# Use pagination template
cp ./skills/fastapi-api-patterns/templates/pagination.py app/utils/pagination.py
```

**Pagination Strategies:**

**1. Offset-Based Pagination (Simple):**
```python
@router.get("/items/")
async def list_items(skip: int = 0, limit: int = 10):
    return items[skip : skip + limit]
```

**2. Cursor-Based Pagination (Performance):**
```python
@router.get("/items/")
async def list_items(cursor: str | None = None, limit: int = 10):
    # Use last item ID as cursor for next page
    # Better for large datasets
```

**3. Page-Based Pagination (User-Friendly):**
```python
@router.get("/items/")
async def list_items(page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size
    return items[skip : skip + page_size]
```

**Filtering Patterns:**
```python
@router.get("/items/")
async def list_items(
    skip: int = 0,
    limit: int = 10,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
):
    # Apply filters before pagination
    filtered_items = apply_filters(items, category, min_price, max_price, search)
    return filtered_items[skip : skip + limit]
```

**Sorting:**
```python
from enum import Enum

class SortBy(str, Enum):
    name = "name"
    price = "price"
    created_at = "created_at"

@router.get("/items/")
async def list_items(
    sort_by: SortBy = SortBy.created_at,
    order: Literal["asc", "desc"] = "desc",
):
    # Sort before returning
```

### 3. Request and Response Models

Define clear Pydantic models for type safety and validation:

**Base Models:**
```python
from pydantic import BaseModel, Field, validator
from datetime import datetime

class ItemBase(BaseModel):
    """Shared properties"""
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    category: str

class ItemCreate(ItemBase):
    """Properties required for creation"""
    pass

class ItemUpdate(BaseModel):
    """Properties that can be updated"""
    name: str | None = None
    description: str | None = None
    price: float | None = Field(None, gt=0)
    category: str | None = None

class ItemInDB(ItemBase):
    """Properties stored in database"""
    id: int
    created_at: datetime
    updated_at: datetime

class Item(ItemInDB):
    """Properties returned to client"""
    class Config:
        from_attributes = True
```

**Response Models with Metadata:**
```python
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int

@router.get("/items/", response_model=PaginatedResponse[Item])
async def list_items(page: int = 1, page_size: int = 10):
    total = len(items)
    pages = (total + page_size - 1) // page_size
    skip = (page - 1) * page_size

    return PaginatedResponse(
        items=items[skip : skip + page_size],
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )
```

### 4. Error Handling Strategies

Implement consistent error handling:

```bash
# Use error handling template
cp ./skills/fastapi-api-patterns/templates/error_handling.py app/utils/errors.py
```

**HTTP Exception Patterns:**
```python
from fastapi import HTTPException, status

# 404 Not Found
if item is None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {item_id} not found"
    )

# 400 Bad Request
if price < 0:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Price must be positive"
    )

# 409 Conflict
if item_exists:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Item with this name already exists"
    )

# 403 Forbidden
if not is_owner:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to modify this item"
    )
```

**Custom Exception Handlers:**
```python
from fastapi import Request
from fastapi.responses import JSONResponse

class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "not_found",
            "message": f"Item {exc.item_id} not found",
            "item_id": exc.item_id
        }
    )
```

**Validation Error Customization:**
```python
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "Invalid request data",
            "details": exc.errors()
        }
    )
```

### 5. Dependency Injection for Common Logic

Use dependencies for authentication, database sessions, and validation:

```python
from fastapi import Depends, Header, HTTPException

# Authentication dependency
async def verify_token(x_token: str = Header(...)):
    if x_token != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return x_token

# Database session dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pagination dependency
async def pagination_params(
    skip: int = 0,
    limit: int = 10,
    max_limit: int = 100
):
    if limit > max_limit:
        limit = max_limit
    return {"skip": skip, "limit": limit}

# Use in endpoints
@router.get("/items/")
async def list_items(
    token: str = Depends(verify_token),
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
):
    return db.query(Item).offset(pagination["skip"]).limit(pagination["limit"]).all()
```

### 6. API Router Organization

Structure APIs with APIRouter for modularity:

```python
# app/routers/items.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}},
)

# app/main.py
from fastapi import FastAPI
from app.routers import items, users

app = FastAPI()

app.include_router(items.router)
app.include_router(users.router, prefix="/api/v1")
```

### 7. OpenAPI Documentation Enhancement

Generate better API documentation:

```bash
# Generate enhanced OpenAPI docs
bash ./skills/fastapi-api-patterns/scripts/generate-openapi-docs.sh
```

**Endpoint Documentation:**
```python
@router.post(
    "/items/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
    description="Create a new item with the provided data",
    response_description="The created item",
    responses={
        201: {"description": "Item created successfully"},
        400: {"description": "Invalid input data"},
        409: {"description": "Item already exists"},
    }
)
async def create_item(item: ItemCreate):
    """
    Create a new item with all the information:

    - **name**: Item name (required, 1-100 characters)
    - **description**: Item description (optional, max 500 characters)
    - **price**: Item price (required, must be positive)
    - **category**: Item category (required)
    """
    pass
```

## Examples

### Example 1: Complete CRUD API for Chat Messages

```bash
# Copy chat API example
cp ./skills/fastapi-api-patterns/examples/chat_api.py app/routers/chat.py
```

**Features:**
- Create chat messages
- List messages with pagination and filtering
- Get single message by ID
- Update message content
- Delete messages
- Search messages by content
- Filter by user, channel, date range

**Result:** Production-ready chat message API with full CRUD operations

### Example 2: User Management API

```bash
# Copy user management example
cp ./skills/fastapi-api-patterns/examples/user_management.py app/routers/users.py
```

**Features:**
- User registration with validation
- User authentication (simulated)
- Profile retrieval and updates
- Password change endpoint
- List users with role filtering
- User deactivation (soft delete)

**Result:** Complete user management system with security best practices

### Example 3: Memory/Context Endpoints for AI Applications

```bash
# Copy memory endpoints example
cp ./skills/fastapi-api-patterns/examples/memory_endpoints.py app/routers/memory.py
```

**Features:**
- Store conversation context
- Retrieve context by session ID
- Update context with new messages
- Clear old contexts
- Search contexts by keywords
- Pagination for large context histories

**Result:** API for managing AI conversation memory and context

## Requirements

**Dependencies:**
- FastAPI 0.100+
- Pydantic 2.0+
- Python 3.10+

**Optional Dependencies:**
- SQLAlchemy (for database operations)
- python-jose (for JWT authentication)
- passlib (for password hashing)
- python-multipart (for file uploads)

**Project Structure:**
```
app/
├── main.py
├── routers/
│   ├── __init__.py
│   ├── items.py
│   ├── users.py
│   └── chat.py
├── models/
│   ├── __init__.py
│   └── schemas.py
├── utils/
│   ├── pagination.py
│   └── errors.py
└── dependencies.py
```

## Best Practices

**1. Use Response Models:**
- Always specify `response_model` to control what's returned
- Use separate models for create, update, and read operations
- Never expose sensitive data (passwords, tokens)

**2. Consistent Error Responses:**
- Use standard HTTP status codes
- Return structured error objects with `error`, `message`, and `details`
- Include request ID for debugging

**3. Pagination Everywhere:**
- Never return unbounded lists
- Default to reasonable page sizes (10-50 items)
- Include total count and page metadata

**4. Validation and Documentation:**
- Use Pydantic Field validators for complex validation
- Document all endpoints with descriptions and examples
- Use response examples in OpenAPI schema

**5. Dependencies for Reusability:**
- Extract common logic into dependencies
- Use dependency injection for auth, DB, pagination
- Keep endpoints thin, move logic to services

**6. Versioning:**
- Use prefix-based versioning (`/api/v1/items`)
- Keep old versions running during migration
- Document breaking changes clearly

## Validation Script

Validate endpoint structure and best practices:

```bash
# Validate all endpoints in a router file
bash ./skills/fastapi-api-patterns/scripts/validate-endpoints.sh app/routers/items.py

# What it checks:
# - Response models defined
# - Status codes specified
# - Error handling present
# - Documentation strings
# - Proper HTTP methods
# - Path parameter validation
```

## Performance Considerations

**Database Queries:**
- Use pagination to limit query size
- Add indexes on frequently filtered fields
- Use database-level filtering, not Python filtering
- Implement query result caching for expensive operations

**Response Size:**
- Exclude unnecessary fields from responses
- Support field selection via query params
- Compress responses with gzip middleware
- Use streaming for large responses

**Request Validation:**
- Set reasonable limits on request sizes
- Validate early and fail fast
- Use background tasks for heavy processing
- Implement rate limiting on expensive endpoints

---

**Plugin:** fastapi-backend
**Version:** 1.0.0
**Category:** API Development
**Skill Type:** REST API Patterns
