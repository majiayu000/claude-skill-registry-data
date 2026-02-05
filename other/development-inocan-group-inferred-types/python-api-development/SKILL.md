---
name: python-api-development
description: Implement REST APIs with FastAPI including endpoints, Pydantic models, validation, dependency injection, and error handling. Use when building API endpoints, request validation, or authentication.
---

# Python API Development Specialist

Specialized in building REST APIs with FastAPI, Pydantic models, and dependency injection.

## When to Use This Skill

- Implementing REST API endpoints
- Creating Pydantic models for request/response validation
- Setting up dependency injection
- Implementing authentication and authorization
- Handling API errors with structured responses
- Creating middleware

## Core Principles

- **Schema-First Design**: Define Pydantic models before implementation
- **Dependency Injection**: Use FastAPI's DI for testability
- **Structured Error Responses**: Consistent error format
- **Request/Response Validation**: Automatic validation with Pydantic
- **Type Safety**: Full type hints for editor support
- **Clear HTTP Status Codes**: Use appropriate status codes

## Implementation Guidelines

### Basic FastAPI Endpoint

```python
# app/main.py
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI(title="User API", version="1.0.0")

class UserCreate(BaseModel):
    """Request model for user creation."""

    email: EmailStr
    name: str
    age: Optional[int] = None

class UserResponse(BaseModel):
    """Response model for user data."""

    id: int
    email: str
    name: str
    age: Optional[int] = None

    class Config:
        from_attributes = True  # Enable ORM mode

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> UserResponse:
    """Create new user.

    Args:
        user: User data from request body

    Returns:
        Created user data

    Raises:
        HTTPException: If user already exists
    """
    # Check if user exists
    existing_user = await user_repository.get_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Create user
    created_user = await user_repository.create(user)
    return UserResponse.from_orm(created_user)

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int) -> UserResponse:
    """Get user by ID."""
    user = await user_repository.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    return UserResponse.from_orm(user)
```

### Pydantic Models with Validation

```python
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user model with shared fields."""

    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)

class UserCreate(UserBase):
    """Model for user creation request."""

    password: str = Field(..., min_length=8)

    @validator('password')
    def password_strength(cls, v):
        """Validate password strength.

        WHY: Enforce security requirements at API boundary.
        """
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

class UserUpdate(BaseModel):
    """Model for user update request."""

    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)

class UserResponse(UserBase):
    """Model for user response."""

    id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    """Model for paginated user list."""

    users: list[UserResponse]
    total: int
    page: int
    page_size: int
```

### Dependency Injection

```python
from fastapi import Depends, HTTPException, status
from typing import Annotated
from app.database import Database
from app.repositories.user_repository import UserRepository

# Database dependency
async def get_database() -> Database:
    """Provide database connection.

    WHY: Use dependency injection for testability and connection pooling.
    """
    db = Database()
    try:
        yield db
    finally:
        await db.close()

# Repository dependency
async def get_user_repository(
    db: Annotated[Database, Depends(get_database)]
) -> UserRepository:
    """Provide user repository."""
    return UserRepository(db)

# Use in endpoint
@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserResponse:
    """Get user with injected repository."""
    user = await repo.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse.from_orm(user)
```

### Authentication

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
import jwt

security = HTTPBearer()

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> User:
    """Get current authenticated user from JWT token.

    Args:
        credentials: Bearer token from request header
        repo: User repository

    Returns:
        Authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=["HS256"]
        )
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = await repo.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user

# Protected endpoint
@app.get("/users/me")
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_user)]
) -> UserResponse:
    """Get current user information (protected endpoint)."""
    return UserResponse.from_orm(current_user)
```

### Error Handling

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

class ErrorResponse(BaseModel):
    """Structured error response model."""

    error: str
    detail: str
    status_code: int

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors.

    WHY: Provide consistent error format for validation failures.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": str(exc),
            "status_code": 422
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
) -> JSONResponse:
    """Handle HTTP exceptions with structured response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Handle unexpected errors.

    WHY: Log and return safe error message to client.
    """
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "status_code": 500
        }
    )
```

### Query Parameters and Pagination

```python
from fastapi import Query
from typing import Annotated

@app.get("/users", response_model=UserListResponse)
async def list_users(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    search: Annotated[Optional[str], Query(max_length=100)] = None,
    repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserListResponse:
    """List users with pagination and search.

    Args:
        page: Page number (1-indexed)
        page_size: Number of items per page (max 100)
        search: Optional search query
        repo: User repository

    Returns:
        Paginated user list
    """
    offset = (page - 1) * page_size
    users = await repo.list(
        offset=offset,
        limit=page_size,
        search=search
    )
    total = await repo.count(search=search)

    return UserListResponse(
        users=[UserResponse.from_orm(u) for u in users],
        total=total,
        page=page,
        page_size=page_size
    )
```

### Middleware

```python
from fastapi import Request
from time import time
import logging

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests with timing.

    WHY: Monitor API performance and track request patterns.
    """
    start_time = time()

    # Process request
    response = await call_next(request)

    # Log request details
    duration = time() - start_time
    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} duration={duration:.3f}s"
    )

    return response
```

## Tools to Use

- `Read`: Read existing API code
- `Write`: Create new API endpoints
- `Edit`: Modify existing endpoints
- `Bash`: Run FastAPI server and tests

### Bash Commands

```bash
# Run development server
uvicorn app.main:app --reload

# Run with specific host and port
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Test API endpoints
curl http://localhost:8000/users
httpie http://localhost:8000/users

# Run tests
pytest tests/test_api.py
```

## Workflow

1. **Understand Requirements**: Clarify API requirements
2. **Write Tests First**: Use `pytest-api-testing` skill
3. **Verify Tests Fail**: Confirm tests fail (Red)
4. **Define Pydantic Models**: Create request/response schemas
5. **Implement Endpoint**: Write endpoint logic
6. **Run Tests**: Verify tests pass (Green)
7. **Test Manually**: Use curl/httpie for manual testing
8. **Run Linter**: Check code quality
9. **Commit**: Create atomic commit

## Related Skills

- `pytest-api-testing`: For testing API endpoints
- `python-core-development`: For implementing business logic
- `pytest-testing`: For unit tests

## Coding Standards

See [Python Coding Standards](../_shared/python-coding-standards.md)

## TDD Workflow

Follow [Python TDD Workflow](../_shared/python-tdd-workflow.md)

## Key Reminders

- Define Pydantic models for all request/response data
- Use dependency injection for repositories and services
- Return appropriate HTTP status codes
- Use structured error responses consistently
- Implement authentication with FastAPI dependencies
- Use type hints for all parameters
- Validate input with Pydantic validators
- Write tests before implementation (TDD)
- Use query parameters for filtering and pagination
- Log requests and errors for monitoring
