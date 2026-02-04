---
name: python-fastapi-ai
description: Python FastAPI patterns, Alembic migrations, Pydantic v2, and AI Engineering (raw patterns, LangChain, Google ADK). This skill should be used when working with Python APIs, database migrations, or AI/LLM applications.
---

## Helper Scripts

- `scripts/linter-formatter.sh` - Formats Python code with ruff, always execute with --help flag first

## AI Engineering Reference

For detailed AI Engineering patterns (RAG, tool calling, LangChain, Google ADK), refer to `references/ai-engineering.md`

# FastAPI Development Patterns

## Project Structure

### Module-Functionality Structure (Recommended for larger apps)

```
app/
├── core/
│   ├── config.py      # Settings with pydantic-settings
│   ├── security.py    # Auth utilities
│   └── deps.py        # Shared dependencies
├── models/            # SQLAlchemy models
├── schemas/           # Pydantic schemas
├── api/
│   ├── v1/
│   │   ├── endpoints/
│   │   └── router.py
│   └── deps.py
├── services/          # Business logic
├── repositories/      # Data access layer
└── main.py
```

## Async Best Practices

### Route Definition

- Use `async def` for I/O-bound operations (DB, HTTP calls)
- Use `def` for CPU-bound operations (FastAPI runs in threadpool)
- Never mix blocking calls in async routes

```python
@router.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await user_service.get_by_id(db, user_id)

@router.post("/process")
def process_cpu_intensive(data: ProcessRequest):
    return heavy_computation(data)
```

### Route Path Conventions (Trailing Slashes)

**Be consistent** - FastAPI returns 307 redirects when trailing slash doesn't match.

**Recommended: NO trailing slashes** (simpler, matches REST conventions)

```python
router = APIRouter(prefix="/users", tags=["users"])

# Root collection routes - NO trailing slash
@router.post("")  # POST /users
@router.get("")   # GET /users

# Resource routes - NO trailing slash
@router.get("/{user_id}")           # GET /users/{id}
@router.patch("/{user_id}")         # PATCH /users/{id}
@router.delete("/{user_id}")        # DELETE /users/{id}

# Nested routes - NO trailing slash
@router.get("/{user_id}/posts")     # GET /users/{id}/posts
@router.post("/{user_id}/posts")    # POST /users/{id}/posts
```

**Alternative: WITH trailing slashes** (if you prefer)

```python
@router.post("/")  # POST /users/
@router.get("/")   # GET /users/
```

**NEVER mix** - pick one style and use it everywhere.

### Async Patterns

```python
async def fetch_multiple():
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        return await asyncio.gather(*tasks)

async with asyncio.TaskGroup() as tg:
    task1 = tg.create_task(fetch_data())
    task2 = tg.create_task(process_data())
```

## Dependencies

### Reusable Dependencies

```python
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    return await auth_service.validate_token(db, token)

CurrentUser = Annotated[User, Depends(get_current_user)]

@router.get("/me")
async def read_current_user(user: CurrentUser):
    return user
```

### Dependency for Validation

```python
async def valid_post_id(post_id: UUID, db: AsyncSession = Depends(get_db)) -> Post:
    post = await post_repo.get(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

ValidPost = Annotated[Post, Depends(valid_post_id)]
```

## Service Layer Pattern

- Keep controllers thin (max 10 lines)
- Place business logic in Service classes
- **NEVER name methods `list`** in classes with SQLAlchemy models - shadows Python's builtin `list` type, breaking type hints like `list[Model]` later in the class. Use `list_all`, `find_all`, or `get_all` instead.

```python
class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: UserCreate) -> User:
        ...

    # WRONG: shadows builtin, breaks `list[User]` type hint below
    async def list(self, page: int = 1) -> tuple[list[User], int]:
        ...

    # CORRECT: use list_all instead
    async def list_all(self, page: int = 1, limit: int = 20) -> tuple[list[User], int]:
        stmt = select(User).offset((page - 1) * limit).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all()), total
```

# Pydantic v2 Best Practices

## Schema Design

```python
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Annotated

class UserBase(BaseModel):
    email: EmailStr
    name: Annotated[str, Field(min_length=1, max_length=100)]

class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=8)]

class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
```

## Validators

```python
from pydantic import field_validator, model_validator

class OrderCreate(BaseModel):
    items: list[OrderItem]
    discount_code: str | None = None

    @field_validator("items")
    @classmethod
    def validate_items_not_empty(cls, v):
        if not v:
            raise ValueError("Order must have at least one item")
        return v

    @model_validator(mode="after")
    def validate_total(self):
        if self.total < 0:
            raise ValueError("Total cannot be negative")
        return self
```

## Strict Types

```python
from pydantic import BaseModel, StrictInt, StrictStr

class StrictConfig(BaseModel):
    count: StrictInt
    name: StrictStr
```

# Alembic Migrations

## Setup & Configuration

```python
# alembic/env.py
from app.core.config import settings
from app.models import Base

config.set_main_option("sqlalchemy.url", settings.database_url)
target_metadata = Base.metadata
```

## Naming Conventions

- `create_users_table` - new tables
- `add_status_to_orders_table` - adding columns
- `drop_legacy_column_from_users` - removals

## Migration Best Practices

### Always Include Downgrade

```python
def upgrade():
    op.add_column("users", sa.Column("status", sa.String(50)))

def downgrade():
    op.drop_column("users", "status")
```

### Safe Non-Nullable Column Addition

```python
def upgrade():
    op.add_column("users", sa.Column("role", sa.String(50), nullable=True))
    op.execute("UPDATE users SET role = 'user' WHERE role IS NULL")
    op.alter_column("users", "role", nullable=False)
```

### Handle Renames Manually (Alembic sees DROP + ADD)

```python
def upgrade():
    op.alter_column("users", "old_name", new_column_name="new_name")
```

### Data Migrations with Inline Tables

```python
def upgrade():
    users = sa.table("users", sa.column("id"), sa.column("status"))
    op.execute(users.update().where(users.c.status == "old").values(status="new"))
```

## Workflow

```bash
alembic revision --autogenerate -m "add_status_to_orders"
alembic check
alembic upgrade head
alembic downgrade -1
```
