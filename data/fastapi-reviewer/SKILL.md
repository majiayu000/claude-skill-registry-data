---
name: fastapi-reviewer
description: |
  WHEN: FastAPI project review, Pydantic models, async endpoints, dependency injection
  WHAT: Pydantic validation + Dependency injection + Async patterns + OpenAPI docs + Security
  WHEN NOT: Django → django-reviewer, Flask → flask-reviewer, General Python → python-reviewer
---

# FastAPI Reviewer Skill

## Purpose
Reviews FastAPI projects for API design, Pydantic usage, async patterns, and security.

## When to Use
- FastAPI project code review
- Pydantic model review
- API endpoint design review
- Async/await pattern check
- Dependency injection review

## Project Detection
- `fastapi` in requirements.txt/pyproject.toml
- `from fastapi import` imports
- `main.py` with FastAPI() app
- `routers/` directory structure

## Workflow

### Step 1: Analyze Project
```
**FastAPI**: 0.100+
**Pydantic**: v2
**Database**: SQLAlchemy/Tortoise/Prisma
**Auth**: OAuth2/JWT
**Docs**: OpenAPI auto-generated
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full FastAPI review (recommended)
- Pydantic models and validation
- Dependency injection patterns
- Async/await usage
- Security and authentication
multiSelect: true
```

## Detection Rules

### Pydantic Models
| Check | Recommendation | Severity |
|-------|----------------|----------|
| dict instead of model | Use Pydantic BaseModel | MEDIUM |
| Missing Field validation | Add Field constraints | MEDIUM |
| No Config class | Add model_config | LOW |
| Mutable default in Field | Use default_factory | HIGH |

```python
# BAD: Plain dict response
@app.get("/user")
async def get_user() -> dict:
    return {"name": "John", "age": 30}

# GOOD: Pydantic model
class UserResponse(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)

    model_config = ConfigDict(from_attributes=True)

@app.get("/user")
async def get_user() -> UserResponse:
    return UserResponse(name="John", age=30)

# BAD: Mutable default
class Config(BaseModel):
    items: list[str] = []  # Shared across instances!

# GOOD: default_factory
class Config(BaseModel):
    items: list[str] = Field(default_factory=list)
```

### Dependency Injection
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Repeated code in endpoints | Extract to Depends() | MEDIUM |
| Global state access | Use dependency injection | HIGH |
| No cleanup in deps | Use yield for cleanup | MEDIUM |
| Hardcoded dependencies | Use Depends for testability | MEDIUM |

```python
# BAD: Repeated DB session code
@app.get("/users")
async def get_users():
    db = SessionLocal()
    try:
        return db.query(User).all()
    finally:
        db.close()

# GOOD: Dependency injection
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()
```

### Async Patterns
| Check | Recommendation | Severity |
|-------|----------------|----------|
| sync def for I/O | Use async def | HIGH |
| Blocking call in async | Use run_in_executor | CRITICAL |
| No async DB driver | Use asyncpg/aiosqlite | HIGH |
| sync file I/O | Use aiofiles | MEDIUM |

```python
# BAD: Blocking call in async
@app.get("/data")
async def get_data():
    response = requests.get(url)  # Blocks event loop!
    return response.json()

# GOOD: Async HTTP client
@app.get("/data")
async def get_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# BAD: Sync file read
@app.get("/file")
async def read_file():
    with open("data.txt") as f:
        return f.read()

# GOOD: Async file read
@app.get("/file")
async def read_file():
    async with aiofiles.open("data.txt") as f:
        return await f.read()
```

### API Design
| Check | Recommendation | Severity |
|-------|----------------|----------|
| No response_model | Add response_model param | MEDIUM |
| Missing status codes | Add responses param | LOW |
| No tags | Add tags for grouping | LOW |
| Inconsistent naming | Use RESTful conventions | MEDIUM |

```python
# BAD: Minimal endpoint
@app.post("/user")
async def create(data: dict):
    return {"id": 1}

# GOOD: Full specification
@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": ErrorResponse, "description": "User exists"},
    },
    tags=["users"],
    summary="Create a new user",
)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Create a new user with the provided details."""
    return await user_service.create(db, user)
```

### Security
| Check | Recommendation | Severity |
|-------|----------------|----------|
| No auth on endpoints | Add Depends(get_current_user) | CRITICAL |
| Secrets in code | Use environment variables | CRITICAL |
| No rate limiting | Add slowapi/fastapi-limiter | HIGH |
| Missing CORS config | Configure CORSMiddleware | HIGH |

```python
# Security setup
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    user = await verify_token(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

# Protected endpoint
@app.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return user
```

## Response Template
```
## FastAPI Code Review Results

**Project**: [name]
**FastAPI**: 0.109 | **Pydantic**: v2 | **DB**: SQLAlchemy async

### Pydantic Models
| Status | File | Issue |
|--------|------|-------|
| HIGH | schemas.py:15 | Mutable default in Field |

### Dependency Injection
| Status | File | Issue |
|--------|------|-------|
| MEDIUM | routers/users.py | Repeated DB session code |

### Async Patterns
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | services/external.py:34 | Blocking requests.get() call |

### Security
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | main.py | No CORS configuration |

### Recommended Actions
1. [ ] Replace blocking HTTP calls with httpx async
2. [ ] Add CORS middleware configuration
3. [ ] Extract repeated code to dependencies
4. [ ] Add response_model to all endpoints
```

## Best Practices
1. **Pydantic v2**: Use model_config, Field validators
2. **Async Everything**: DB, HTTP, file I/O
3. **Dependencies**: Extract common logic
4. **Security**: OAuth2, CORS, rate limiting
5. **Documentation**: OpenAPI auto-docs with examples

## Integration
- `python-reviewer`: General Python patterns
- `security-scanner`: API security audit
- `api-documenter`: OpenAPI enhancement
