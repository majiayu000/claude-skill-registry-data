---
name: generate-speakmanai-code-python
description: Internal LANG_CONFIG reference for Python/FastAPI projects, read automatically by the generate-speakmanai-code router (Step 1c). Not a standalone workflow — do not trigger this on its own; use generate-speakmanai-code instead.
---

# generate-speakmanai-code-python — Python / FastAPI Variant

This file is read by the `generate-speakmanai-code` router (Step 1c) to extract LANG_CONFIG
for Python / FastAPI projects. It is not invoked directly.

Architecture: FastAPI monolith serving REST API, MCP SSE, and Admin UI (Jinja2 + HTMX)
from a single process. No BFF. No separate frontend service. Cloud Run Jobs share the same
`src/` codebase via a separate entrypoint. Node.js exists only as a co-bundled subprocess
for PDF rendering, invoked via `asyncio.create_subprocess_exec`.

---

## LANG_CONFIG

### CODING_STANDARDS

- **Style**: PEP 8; enforced via `ruff check` + `ruff format` (configured in `pyproject.toml`)
- **Indent**: 4 spaces
- **Type hints**: required on all function signatures and class attributes — no bare `Any`
- **Async**: FastAPI routes, application use cases, and infrastructure methods are all `async def`
- **Domain layer**: synchronous only — no `async`, no `await`, no I/O imports anywhere in `src/domain/`
- **Domain objects**: `@dataclass(frozen=True)` for entities and value objects — immutable by construction
- **API schemas**: Pydantic `BaseModel` for request/response shapes only — never in domain or application layers
- **Errors**: `raise DomainError(code='VALIDATION_ERROR', message='...')` — never `HTTPException` from domain or application layers
- **Naming**:
  - Python identifiers and JSON fields: `snake_case` (per NAMING_DICT `canonical_name` / `json_field`)
  - DB columns: `snake_case` (per NAMING_DICT `sql_column`)
  - All canonical names in NAMING_DICT take precedence over any inferred name
- **Imports**: absolute from `src/` root (e.g. `from domain.todo.entity import TodoItem`)
- **Secrets**: read from `os.environ` at call time inside functions — never cached at module level
- **Boolean fields**: validate with `isinstance(value, bool)` — never `bool(value)` which coerces strings

---

### DIR_SKELETON_LAYOUT

```
{REPO_PATH}/
  src/
    domain/
      shared/
        errors.py           ← DomainError class (single shared definition)
      {aggregate}/          ← one directory per aggregate root in DOMAIN_MODEL
        entity.py           ← @dataclass(frozen=True) aggregate and child entities
        value_objects.py    ← @dataclass(frozen=True) value objects
        repository.py       ← Protocol interface for this aggregate's repository
    application/
      use_cases/
        {uc_name}.py        ← one file per UC-XX
    infrastructure/
      database/
        connection.py       ← async DB connection + lifespan helper
        migrations.py       ← idempotent DDL runner
        {aggregate}_repository.py  ← one per aggregate root
      {external_service}/   ← one directory per external service in API_SCHEMA tags
    api/
      routers/
        {aggregate}.py      ← FastAPI APIRouter per aggregate
      schemas/
        {aggregate}.py      ← Pydantic request/response models per aggregate
      dependencies.py       ← FastAPI Depends() factories (get_db, get_repo, require_auth)
      middleware.py         ← security headers, CORS
      app.py                ← create_app() factory function
    mcp/
      server.py             ← FastMCP instance and mount point
      tools.py              ← @mcp.tool() definitions
    admin/
      routes.py             ← Jinja2 + HTMX admin APIRouter
      templates/            ← Jinja2 .html template files
        base.html
        {section}/
    jobs/
      {job_name}.py         ← Cloud Run Job entrypoints (same src/, different __main__)
    migration/
      migrate.py            ← data migration script (run once; source → target schema)
  tests/
    conftest.py             ← shared fixtures: db, client, test token factory
    domain/                 ← pure unit tests; synchronous; no pytest-asyncio needed
    application/            ← async unit tests; AsyncMock repositories
    infrastructure/         ← async integration tests; real :memory: DB
    api/                    ← async integration tests; httpx.AsyncClient + ASGITransport
    e2e/                    ← async journey tests; full stack, no seeding at seams
  pdf_renderer/             ← co-bundled Node.js PDF binary (NOT a web service)
    package.json            ← {"type":"module","dependencies":{...}}
    index.js                ← reads JSON from stdin, writes PDF bytes to stdout
  main.py                   ← uvicorn entry point: `uvicorn src.api.app:app`
  pyproject.toml            ← ruff config, pytest config, package metadata
  requirements.txt          ← production dependencies
  requirements-dev.txt      ← dev/test dependencies
  .env.example
  Dockerfile
```

`src/mcp/` and `src/admin/` are always present — omit only if the workflow has no MCP tools
or no admin interface. `pdf_renderer/` is present whenever PDF export is in scope.

---

### DEPENDENCIES_DERIVATION

Derive packages from the contracts:

**`requirements.txt` (production)**

| Source | Package |
|---|---|
| Always | `fastapi[standard]` (includes uvicorn, python-multipart) |
| Always | `python-dotenv` |
| Always | `aiosqlite` (default dev DB; swap driver for production) |
| API_SCHEMA BearerAuth security scheme | `PyJWT` |
| DOMAIN_MODEL or FIELD_DEFS: password hashing | `bcrypt` |
| Admin UI in scope | `jinja2` (included in `fastapi[standard]`) |
| MCP tools in scope | `fastmcp` |
| External service in API_SCHEMA tags | service-specific SDK (e.g. `google-cloud-storage`, `stripe`, `motor` for MongoDB) |
| Embeddings in scope | `google-cloud-aiplatform` or `openai` |
| TECH_STACK specifies MongoDB | `motor` (async MongoDB driver) |
| TECH_STACK specifies PostgreSQL | `asyncpg` + `sqlalchemy[asyncio]` |

**`requirements-dev.txt` (dev + test)**

| Source | Package |
|---|---|
| Always | `pytest` |
| Always | `pytest-asyncio` |
| Always | `httpx` (async test client via ASGITransport) |
| Always | `ruff` |
| TEST_STRATEGY tooling column | any additional listed tools |

**`pdf_renderer/package.json`** (only if PDF rendering is in scope):

```json
{
  "type": "module",
  "dependencies": {
    "@react-pdf/renderer": "^3.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  }
}
```

---

### SCAFFOLD_CONFIG

**`pyproject.toml`:**
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
pythonpath = ["src"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]
ignore = ["E501"]
```

**`requirements.txt`** (generated from DEPENDENCIES_DERIVATION — one package per line, no version pins at scaffold time; pin after first successful run):
```
fastapi[standard]
python-dotenv
aiosqlite
PyJWT
bcrypt
fastmcp
```

**`requirements-dev.txt`:**
```
pytest
pytest-asyncio
httpx
ruff
```

---

### SCAFFOLD_FILES

**`src/domain/shared/errors.py`** — create at scaffold time; used everywhere:
```python
class DomainError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)
```

**`src/api/app.py`** — app factory; required before any routes can be written:
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from domain.shared.errors import DomainError

def create_app(db=None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if db is None:
            from infrastructure.database.connection import connect_db, close_db
            app.state.db = await connect_db()
            yield
            await close_db(app.state.db)
        else:
            app.state.db = db
            yield

    app = FastAPI(lifespan=lifespan)

    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
        STATUS_MAP = {
            'NOT_FOUND': 404, 'UNAUTHORIZED': 401,
            'CONFLICT': 409, 'VALIDATION_ERROR': 422,
        }
        status = STATUS_MAP.get(exc.code, 500)
        return JSONResponse(
            status_code=status,
            content={'error': exc.code, 'message': exc.message if status != 500 else 'Internal server error'},
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        import logging
        logging.getLogger(__name__).error('Unhandled error', exc_info=exc)
        return JSONResponse(status_code=500, content={'error': 'INTERNAL_ERROR', 'message': 'Internal server error'})

    @app.get('/health', include_in_schema=False)
    async def health() -> dict:
        return {'status': 'ok'}

    return app
```

**`main.py`** — uvicorn entry point:
```python
import uvicorn
from src.api.app import create_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
```

**`tests/conftest.py`** — shared test fixtures:
```python
import pytest
import aiosqlite
import httpx
import jwt
import os
from infrastructure.database.migrations import run_migrations
from api.app import create_app

@pytest.fixture
async def db():
    async with aiosqlite.connect(':memory:') as conn:
        conn.row_factory = aiosqlite.Row
        await run_migrations(conn)
        yield conn

@pytest.fixture
async def client(db):
    app = create_app(db)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as c:
        yield c

def make_test_token(user_id: str = 'test-user', role: str = 'user') -> str:
    return jwt.encode({'sub': user_id, 'role': role}, os.environ.get('JWT_SECRET', 'test-secret'), algorithm='HS256')
```

---

### GITIGNORE_ENTRIES

```
__pycache__/
*.pyc
*.pyo
.venv/
venv/
.env
*.db
*.sqlite
dist/
.ruff_cache/
.pytest_cache/
.coverage
htmlcov/
pdf_renderer/node_modules/
```

---

### SECRET_GENERATION_CMD

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Use this to generate `JWT_SECRET` and `DB_ENCRYPTION_KEY` in the dev `.env` file.

---

### VALIDATION_GATE

```bash
pytest
```

Run from repo root. `pythonpath = ["src"]` in `pyproject.toml` ensures imports resolve
without a package install step.

---

### MILESTONE_GATES

```
install:        pip install -r requirements.txt -r requirements-dev.txt
domain:         pytest tests/domain/ -v
application:    pytest tests/application/ -v
infrastructure: pytest tests/infrastructure/ -v
interface:      pytest tests/api/ -v
e2e:            pytest tests/e2e/ -v
ui_build:       N/A — FastAPI serves Jinja2 templates directly; no build step
```

`uv` users: replace `pip install` with `uv pip install`.

---

### LOCAL_DB_TEST

SQLite in-memory: pass `':memory:'` to `aiosqlite.connect()`.

```python
async with aiosqlite.connect(':memory:') as conn:
    conn.row_factory = aiosqlite.Row
    await run_migrations(conn)
    # conn is a real database — no mocks
```

The `db` fixture in `tests/conftest.py` wraps this pattern — use it in all infrastructure
and API tests.

---

### DOMAIN_IMPLEMENTATION_GUIDE

Implement each aggregate root, child entity, and value object as a `@dataclass(frozen=True)`.
Validation runs in `__post_init__`. No async, no I/O, no imports from outside `src/domain/`.

**Value Object pattern** (`src/domain/{aggregate}/value_objects.py`):
```python
from dataclasses import dataclass
from domain.shared.errors import DomainError

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if not self.value or '@' not in self.value:
            raise DomainError(code='VALIDATION_ERROR', message='Email must be a valid email address')
        object.__setattr__(self, 'value', self.value.lower())
```

**Aggregate Root pattern** (`src/domain/{aggregate}/entity.py`):
```python
from dataclasses import dataclass, field
from domain.shared.errors import DomainError

@dataclass(frozen=True)
class TodoItem:
    id: str
    title: str
    is_completed: bool = False

    def __post_init__(self) -> None:
        if not self.id:
            raise DomainError(code='VALIDATION_ERROR', message='id is required')
        if not self.title or not self.title.strip():
            raise DomainError(code='VALIDATION_ERROR', message='title is required')
        if len(self.title) > 500:
            raise DomainError(code='VALIDATION_ERROR', message='title must be 500 characters or fewer')
```

**Rules:**
- All invariant violations raise `DomainError` — never `ValueError`, `AssertionError`, or `HTTPException`
- `object.__setattr__` is the only way to mutate a frozen dataclass field (use for normalisation in `__post_init__` only)
- No `async` methods. No imports from `application/`, `infrastructure/`, or `api/`

---

### REPO_INTERFACE_PATTERN

Define repository interfaces as `Protocol` in `src/domain/{aggregate}/repository.py`.

```python
from typing import Protocol
from domain.todo.entity import TodoItem

class TodoRepository(Protocol):
    async def save(self, item: TodoItem) -> None: ...
    async def find_by_id(self, id: str) -> TodoItem | None: ...
    async def find_all(self) -> list[TodoItem]: ...
    async def delete(self, id: str) -> None: ...
```

`Protocol` provides structural subtyping — the infrastructure implementation does not need
to inherit from it, only satisfy the method signatures. Application use cases receive the
`Protocol` type in their signature; infrastructure passes the concrete class.

---

### DOMAIN_TEST_GUIDE

Use `pytest`. Domain tests are synchronous — no `pytest-asyncio` needed for this layer.
One test file per aggregate / value object in `tests/domain/`.

```python
import pytest
from domain.todo.entity import TodoItem
from domain.shared.errors import DomainError

def test_raises_validation_error_when_title_is_empty():
    with pytest.raises(DomainError) as exc_info:
        TodoItem(id='1', title='')
    assert exc_info.value.code == 'VALIDATION_ERROR'

def test_raises_validation_error_when_id_is_missing():
    with pytest.raises(DomainError) as exc_info:
        TodoItem(id='', title='Buy milk')
    assert exc_info.value.code == 'VALIDATION_ERROR'

def test_creates_with_default_is_completed_false():
    item = TodoItem(id='1', title='Buy milk')
    assert item.is_completed is False

def test_creates_valid_item():
    item = TodoItem(id='1', title='Buy milk')
    assert item.id == '1'
    assert item.title == 'Buy milk'
```

Cover every invariant: one test that violates it, one that satisfies it.

---

### APPLICATION_IMPLEMENTATION_GUIDE

One file per UC-XX in `src/application/use_cases/`. Each use case is an `async def` function
that receives repository instances as its first arguments (dependency injection by position).

```python
# src/application/use_cases/create_todo_item.py
import uuid
from domain.todo.entity import TodoItem
from domain.todo.repository import TodoRepository
from domain.audit.repository import AuditRepository
from domain.shared.errors import DomainError

async def create_todo_item(
    todo_repo: TodoRepository,
    audit_repo: AuditRepository,
    *,
    title: str,
    user_id: str,
) -> TodoItem:
    item = TodoItem(id=str(uuid.uuid4()), title=title)
    await todo_repo.save(item)
    await audit_repo.save(action='TODO_CREATED', entity_id=item.id, user_id=user_id)
    return item
```

```python
# src/application/use_cases/get_todo_item.py
async def get_todo_item(
    todo_repo: TodoRepository,
    *,
    id: str,
    user_id: str,
) -> TodoItem:
    item = await todo_repo.find_by_id(id)
    if item is None:
        raise DomainError(code='NOT_FOUND', message=f'Todo item {id} not found')
    return item
```

**Rules:**
- Repositories are always injected — never imported from `infrastructure/`
- Write an audit log entry on every mutation use case
- Raise domain error codes only (`NOT_FOUND`, `UNAUTHORIZED`, `CONFLICT`, `VALIDATION_ERROR`)
- Never import from `api/`, `admin/`, or `mcp/`

---

### APPLICATION_TEST_GUIDE

Use `pytest-asyncio` with `AsyncMock` from `unittest.mock`.

```python
import pytest
from unittest.mock import AsyncMock
from application.use_cases.create_todo_item import create_todo_item
from domain.shared.errors import DomainError

@pytest.fixture
def todo_repo():
    repo = AsyncMock()
    repo.save = AsyncMock(return_value=None)
    repo.find_by_id = AsyncMock(return_value=None)
    return repo

@pytest.fixture
def audit_repo():
    repo = AsyncMock()
    repo.save = AsyncMock(return_value=None)
    return repo

async def test_creates_item_and_writes_audit(todo_repo, audit_repo):
    result = await create_todo_item(todo_repo, audit_repo, title='Buy milk', user_id='u1')
    assert result.title == 'Buy milk'
    todo_repo.save.assert_called_once()
    audit_repo.save.assert_called_once()

async def test_raises_not_found_when_item_missing(todo_repo, audit_repo):
    todo_repo.find_by_id = AsyncMock(return_value=None)
    with pytest.raises(DomainError) as exc_info:
        await get_todo_item(todo_repo, id='missing', user_id='u1')
    assert exc_info.value.code == 'NOT_FOUND'
```

`asyncio_mode = "auto"` in `pyproject.toml` means no `@pytest.mark.asyncio` decorator
is needed — all `async def test_*` functions run automatically.

---

### INFRASTRUCTURE_IMPLEMENTATION_GUIDE

**Connection module** (`src/infrastructure/database/connection.py`):
```python
import os
import aiosqlite

async def connect_db(path: str | None = None) -> aiosqlite.Connection:
    db_path = path or os.environ.get('DB_PATH', './data/dev.db')
    conn = await aiosqlite.connect(db_path)
    conn.row_factory = aiosqlite.Row
    return conn

async def close_db(conn: aiosqlite.Connection) -> None:
    await conn.close()
```

**Migration runner** (`src/infrastructure/database/migrations.py`):
```python
import aiosqlite

async def run_migrations(db: aiosqlite.Connection) -> None:
    await db.execute("""
        CREATE TABLE IF NOT EXISTS todo_items (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            is_completed INTEGER NOT NULL DEFAULT 0,
            user_id TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    await db.execute("CREATE INDEX IF NOT EXISTS idx_todo_items_created_at ON todo_items(created_at)")
    await db.commit()
```

**Repository implementation** (`src/infrastructure/database/todo_repository.py`):
```python
import aiosqlite
from domain.todo.entity import TodoItem
from domain.shared.errors import DomainError

class SqliteTodoRepository:
    def __init__(self, db: aiosqlite.Connection) -> None:
        self._db = db

    def _row_to_entity(self, row: aiosqlite.Row) -> TodoItem:
        return TodoItem(
            id=row['id'],
            title=row['title'],
            is_completed=bool(row['is_completed']),
        )

    async def save(self, item: TodoItem) -> None:
        try:
            await self._db.execute(
                'INSERT OR REPLACE INTO todo_items (id, title, is_completed, user_id, created_at) VALUES (?, ?, ?, ?, datetime("now"))',
                (item.id, item.title, 1 if item.is_completed else 0, item.user_id),
            )
            await self._db.commit()
        except aiosqlite.IntegrityError as e:
            raise DomainError(code='CONFLICT', message=str(e)) from e

    async def find_by_id(self, id: str) -> TodoItem | None:
        async with self._db.execute('SELECT * FROM todo_items WHERE id = ?', (id,)) as cursor:
            row = await cursor.fetchone()
        return self._row_to_entity(row) if row else None

    async def find_all(self) -> list[TodoItem]:
        async with self._db.execute('SELECT * FROM todo_items ORDER BY created_at DESC') as cursor:
            rows = await cursor.fetchall()
        return [self._row_to_entity(r) for r in rows]

    async def delete(self, id: str) -> None:
        await self._db.execute('DELETE FROM todo_items WHERE id = ?', (id,))
        await self._db.commit()
```

**Error mapping rules:**
- `aiosqlite.IntegrityError` (UNIQUE constraint) → `DomainError(code='CONFLICT')`
- Row not found → return `None` from `find_by_id`; the application use case raises `NOT_FOUND`

---

### INFRASTRUCTURE_TEST_GUIDE

Use the shared `db` fixture from `tests/conftest.py` — real in-memory SQLite, no mocks.

```python
import pytest
from domain.todo.entity import TodoItem
from domain.shared.errors import DomainError
from infrastructure.database.todo_repository import SqliteTodoRepository

async def test_save_and_find_by_id(db):
    repo = SqliteTodoRepository(db)
    item = TodoItem(id='1', title='Buy milk', user_id='u1')
    await repo.save(item)
    found = await repo.find_by_id('1')
    assert found is not None
    assert found.title == 'Buy milk'

async def test_find_by_id_returns_none_for_unknown(db):
    repo = SqliteTodoRepository(db)
    result = await repo.find_by_id('nonexistent')
    assert result is None

async def test_boolean_round_trips_correctly(db):
    repo = SqliteTodoRepository(db)
    item = TodoItem(id='1', title='Done', is_completed=True, user_id='u1')
    await repo.save(item)
    found = await repo.find_by_id('1')
    assert found.is_completed is True

async def test_raises_conflict_on_duplicate_id(db):
    repo = SqliteTodoRepository(db)
    item = TodoItem(id='1', title='First', user_id='u1')
    await repo.save(item)
    duplicate = TodoItem(id='1', title='Second', user_id='u1')
    with pytest.raises(DomainError) as exc_info:
        await repo.save(duplicate)
    assert exc_info.value.code == 'CONFLICT'
```

---

### INTERFACE_IMPLEMENTATION_GUIDE

**FastAPI router** (`src/api/routers/{aggregate}.py`):
```python
from fastapi import APIRouter, Depends
from api.schemas.todo import CreateTodoRequest, TodoResponse
from api.dependencies import get_todo_repo, get_audit_repo, require_auth
from application.use_cases.create_todo_item import create_todo_item

router = APIRouter(prefix='/api/todos', tags=['todos'])

@router.post('/', response_model=TodoResponse, status_code=201)
async def create_todo(
    body: CreateTodoRequest,
    auth: dict = Depends(require_auth),
    todo_repo=Depends(get_todo_repo),
    audit_repo=Depends(get_audit_repo),
):
    item = await create_todo_item(todo_repo, audit_repo, title=body.title, user_id=auth['sub'])
    return TodoResponse.model_validate(item.__dict__)
```

**Pydantic schemas** (`src/api/schemas/{aggregate}.py`):
```python
from pydantic import BaseModel, Field

class CreateTodoRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)

class TodoResponse(BaseModel):
    model_config = {'from_attributes': True}
    id: str
    title: str
    is_completed: bool
```

**Dependencies** (`src/api/dependencies.py`):
```python
import os
import jwt
from fastapi import Depends, HTTPException, Request, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from infrastructure.database.todo_repository import SqliteTodoRepository

security = HTTPBearer()

async def get_db(request: Request):
    return request.app.state.db

async def get_todo_repo(db=Depends(get_db)) -> SqliteTodoRepository:
    return SqliteTodoRepository(db)

async def require_auth(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> dict:
    try:
        return jwt.decode(
            credentials.credentials,
            os.environ['JWT_SECRET'],
            algorithms=['HS256'],
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail={'error': 'UNAUTHORIZED', 'message': 'Invalid or missing token'},
        )
```

**Security headers middleware** (`src/api/middleware.py`):
```python
from fastapi import Request
from fastapi.responses import Response

async def add_security_headers(request: Request, call_next) -> Response:
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
    return response
```

Register in `create_app()`:
```python
from fastapi.middleware.cors import CORSMiddleware
app.middleware('http')(add_security_headers)
app.add_middleware(CORSMiddleware, allow_origins=[os.environ['CORS_ORIGIN']], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
```

**Admin UI routes** (`src/admin/routes.py`):
```python
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix='/admin')
templates = Jinja2Templates(directory='src/admin/templates')

@router.get('/')
async def admin_home(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})
```

**MCP server** (`src/mcp/server.py`):
```python
from fastmcp import FastMCP

mcp = FastMCP(name='{REPO_NAME}')
```

Mount in `create_app()`:
```python
from mcp.server import mcp
app.mount('/mcp', mcp.get_asgi_app())
```

**PDF subprocess** (invoke from any use case or route that needs PDF output):
```python
import asyncio, json

async def render_pdf(data: dict) -> bytes:
    proc = await asyncio.create_subprocess_exec(
        'node', 'pdf_renderer/index.js',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate(json.dumps(data).encode())
    if proc.returncode != 0:
        raise RuntimeError(f'PDF renderer failed: {stderr.decode()}')
    return stdout
```

**Non-negotiable interface rules:**
- `GET /health` always returns `200 {"status": "ok"}` with no auth requirement — wired in `create_app()`
- Global `Exception` handler returns `{"error": "INTERNAL_ERROR", "message": "Internal server error"}` — never forward `str(exc)` to the client
- Boolean request fields validated with `isinstance(value, bool)` — Pydantic enforces this automatically when the field type is `bool` (strict mode not required for primitive booleans in Pydantic v2)
- `CORS_ORIGIN` is always read from `os.environ` — never hardcoded

---

### BFF_PRESENT

`false` — FastAPI serves the REST API, MCP SSE, and Admin UI directly. There is no separate
BFF proxy service. The Jinja2 + HTMX admin templates make direct calls to the FastAPI
`/api/` routes via HTMX attributes.

---

### BFF_IMPLEMENTATION

Not applicable — BFF_PRESENT is false.

---

### INTERFACE_TEST_GUIDE

Use `httpx.AsyncClient` with `ASGITransport` against the real FastAPI app backed by
the in-memory `db` fixture from `tests/conftest.py`.

```python
async def test_create_todo_returns_201(client):
    token = make_test_token()
    response = await client.post(
        '/api/todos',
        json={'title': 'Buy milk'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 201
    body = response.json()
    assert body['title'] == 'Buy milk'
    assert body['is_completed'] is False
    assert 'id' in body

async def test_create_todo_returns_422_when_title_missing(client):
    token = make_test_token()
    response = await client.post(
        '/api/todos',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 422

async def test_create_todo_returns_401_without_token(client):
    response = await client.post('/api/todos', json={'title': 'Buy milk'})
    assert response.status_code == 401

async def test_health_requires_no_auth(client):
    response = await client.get('/health')
    assert response.status_code == 200
```

---

### E2E_IMPLEMENTATION_GUIDE

One test file per UC-XX named `test_UC{XX}_{name}.py` in `tests/e2e/`. Use the shared
`client` fixture from `tests/conftest.py`. Full app stack, no DB seeding at seams — all
values obtained from prior API responses.

```python
async def test_UC01_create_and_retrieve_todo(client):
    # Step 1: register a user — obtain token from the API response, not from a DB insert
    register_res = await client.post(
        '/api/auth/register',
        json={'username': 'alice', 'password': 'Password123!'},
    )
    assert register_res.status_code == 201
    token = register_res.json()['token']

    # Step 2: create a todo
    create_res = await client.post(
        '/api/todos',
        json={'title': 'Buy milk'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert create_res.status_code == 201
    todo_id = create_res.json()['id']

    # Step 3: retrieve — ID obtained from step 2, not seeded
    get_res = await client.get(
        f'/api/todos/{todo_id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert get_res.status_code == 200
    assert get_res.json()['title'] == 'Buy milk'
```

**No DB seeding at seams**: if a use case produces a value (ID, token, slug) that a later
use case consumes, extract it from the API response — never insert it directly into the
database between steps.

---

### RUN_LOCALLY_INSTRUCTIONS

```
# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt
# (or: uv pip install -r requirements.txt -r requirements-dev.txt)

# Copy env file and fill in values
cp .env.example .env

# Install PDF renderer (only if pdf_renderer/ is present)
cd pdf_renderer && npm install && cd ..

# Start the server
python main.py
# → FastAPI on http://localhost:8000
# → REST API at /api/
# → MCP SSE at /mcp
# → Admin UI at /admin/

# Run tests
pytest                         # full suite
pytest tests/domain/           # domain only
pytest tests/application/      # application only
pytest tests/infrastructure/   # infrastructure only
pytest tests/api/              # interface only
pytest tests/e2e/              # e2e only

# Lint
ruff check src/ tests/
ruff format src/ tests/
```
