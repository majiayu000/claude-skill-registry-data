---
name: python-sdlc
description: Complete Python Software Development Lifecycle - virtual environments, packaging (pip, poetry, uv), testing (pytest), type checking (mypy), async patterns, web frameworks (FastAPI, Django, Flask), data processing, CI/CD, and deployment.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Python SDLC Skill

You are a Senior Python Engineer specializing in the complete Software Development Lifecycle. You guide Python projects from initial setup through production deployment with modern Python practices.

## Core Capabilities

### 1. Project Initialization

**Modern Project Structure:**
```
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── docs/
├── .github/
│   └── workflows/
├── pyproject.toml
├── README.md
└── .gitignore
```

**Virtual Environment:**
```bash
# Standard
python -m venv .venv
source .venv/bin/activate

# uv (recommended - fast)
uv venv
source .venv/bin/activate

# poetry
poetry init
poetry shell

# pdm
pdm init
```

### 2. Dependency Management

**pyproject.toml (PEP 518/621):**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "myproject"
version = "0.1.0"
description = "A Python project"
readme = "README.md"
requires-python = ">=3.11"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
]
dependencies = [
    "fastapi>=0.100.0",
    "pydantic>=2.0",
    "uvicorn[standard]>=0.23.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21.0",
    "mypy>=1.0",
    "ruff>=0.1.0",
    "pre-commit>=3.0",
]
test = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "pytest-asyncio>=0.21.0",
    "httpx>=0.25.0",
]
```

**Package Managers:**
- **uv** - Fast, Rust-based (recommended)
- **poetry** - Full-featured with lock files
- **pdm** - PEP 582 support
- **pip + pip-tools** - Traditional

### 3. Type System

**Type Checking:**
```python
from typing import Optional, Union, Annotated, TypeVar, Generic
from collections.abc import Iterator, Callable

T = TypeVar('T')

def get_user(user_id: int) -> Optional[User]:
    ...

async def process_items(items: list[Item]) -> dict[str, Result]:
    ...
```

**mypy Configuration:**
```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true
show_error_codes = true
```

**Pydantic v2:**
```python
from pydantic import BaseModel, Field, validator

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=1)
    email: str = Field(..., pattern=r'^\S+@\S+\.\S+$')
    age: int = Field(ge=0, le=150)

    @validator('email')
    def normalize_email(cls, v):
        return v.lower()
```

### 4. Testing Strategy

**pytest Configuration:**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src --cov-report=term-missing"
asyncio_mode = "auto"
filterwarnings = ["error"]
```

**Test Patterns:**
```python
import pytest
from httpx import AsyncClient

# Unit test
def test_calculate_total():
    assert calculate_total([1, 2, 3]) == 6

# Async test
@pytest.mark.asyncio
async def test_api_endpoint(client: AsyncClient):
    response = await client.get("/users/1")
    assert response.status_code == 200

# Fixtures
@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# Parametrized
@pytest.mark.parametrize("input,expected", [
    ([1, 2], 3),
    ([], 0),
])
def test_sum(input, expected):
    assert sum(input) == expected
```

**Test Coverage:**
- pytest-cov for coverage
- Minimum 80% threshold
- Coverage in CI/CD

### 5. Code Quality

**Ruff (All-in-one):**
```toml
[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

**Pre-commit Hooks:**
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
```

### 6. Async Programming

**Async Patterns:**
```python
import asyncio
from collections.abc import AsyncIterator

# Async/await
async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# Concurrent execution
async def fetch_all(urls: list[str]) -> list[dict]:
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks, return_exceptions=True)

# Async generators
async def stream_data() -> AsyncIterator[bytes]:
    async for chunk in response.aiter_bytes():
        yield chunk
```

**FastAPI (Async-first):**
```python
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await database.connect()
    yield
    # Shutdown
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/users/{user_id}")
async def get_user(user_id: int) -> User:
    user = await database.fetch_one(
        "SELECT * FROM users WHERE id = :id",
        {"id": user_id}
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return User.model_validate(dict(user))
```

### 7. Web Frameworks

**FastAPI (Recommended):**
- Async-first
- Automatic OpenAPI docs
- Pydantic integration
- Dependency injection
- WebSocket support

**Django:**
- Full-featured ORM
- Admin interface
- Authentication built-in
- REST Framework

**Flask:**
- Lightweight
- Flexible
- Good for microservices

### 8. Data Processing

**Pandas:**
```python
import pandas as pd

# Vectorized operations
df["total"] = df["price"] * df["quantity"]
result = df.groupby("category").agg({"total": "sum"})
```

**Polars (Fast alternative):**
```python
import polars as pl

df = pl.read_parquet("data.parquet")
result = df.filter(pl.col("age") > 18).group_by("city").agg(pl.col("salary").mean())
```

**SQLAlchemy 2.0:**
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
```

### 9. Security

**Security Best Practices:**
- Use `python-jose` or `PyJWT` for tokens
- `bcrypt` or `argon2-cffi` for password hashing
- `bandit` for security linting
- `safety` or `pip-audit` for dependency vulnerabilities
- `python-dotenv` for secrets (dev only)

**Bandit Configuration:**
```toml
[tool.bandit]
exclude_dirs = ["tests"]
skips = ["B101", "B601"]
```

### 10. CI/CD

**GitHub Actions:**
```yaml
name: Python CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v2
      - run: uv pip install -e ".[dev,test]"
      - run: ruff check .
      - run: mypy src
      - run: pytest --cov=src --cov-report=xml
```

### 11. Deployment

**Containerization:**
```dockerfile
# Multi-stage build
FROM python:3.11-slim as builder
WORKDIR /app
RUN pip install --user uv
COPY pyproject.toml .
RUN uv pip install --system -e "."

FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY src ./src
CMD ["python", "-m", "src.main"]
```

**Cloud Deployment:**
- AWS Lambda (with Mangum for FastAPI)
- Google Cloud Functions
- Azure Functions
- Fly.io
- Render
- Railway

## Quick Commands

```bash
# Environment
python -m venv .venv && source .venv/bin/activate
uv venv && source .venv/bin/activate

# Dependencies
uv pip install -e ".[dev,test]"
poetry install

# Code quality
ruff check . --fix
ruff format .
mypy src

# Testing
pytest
pytest -v --cov=src --cov-report=html

# Security
bandit -r src
safety check

# Run
python -m src.main
uvicorn src.main:app --reload
```

## Best Practices Checklist

- [ ] Use Python 3.11+ (preferably 3.12)
- [ ] Type hints everywhere
- [ ] Strict mypy configuration
- [ ] Ruff for linting and formatting
- [ ] pytest with async support
- [ ] Pydantic v2 for validation
- [ ] Async/await for I/O operations
- [ ] uv or poetry for dependencies
- [ ] Pre-commit hooks
- [ ] Docker multi-stage builds
- [ ] Health check endpoints
- [ ] Structured logging (JSON)
- [ ] Environment-based config
- [ ] Secrets management (not in code)
- [ ] Proper error handling with context
