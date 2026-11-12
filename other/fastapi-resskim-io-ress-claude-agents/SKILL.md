---
name: fastapi
description: "FastAPI 서버 — Pydantic v2 스키마, lifespan, Depends 의존성 주입, async SQLAlchemy, BackgroundTasks, WebSocket, OAuth2+JWT. Use when FastAPI 로 비동기 API 서버를 구축하거나 인증·DB 연동을 구성할 때."
---

# FastAPI Production Patterns

FastAPI + Pydantic v2 + SQLAlchemy async 기반 고성능 API 서버 구축 가이드.

## Quick Reference

```
엔드포인트 설계?
├── CRUD API ──────────> APIRouter + Depends
├── WebSocket 실시간 ──> WebSocket endpoint
├── 파일 업로드 ───────> UploadFile + BackgroundTasks
├── 인증 필요 ─────────> OAuth2PasswordBearer + JWT
└── 비동기 작업 ───────> BackgroundTasks or Celery

응답 모델 선택?
├── 단일 객체 ─────────> response_model=ItemResponse
├── 목록 + 페이지 ─────> PaginatedResponse[ItemResponse]
├── 에러 ──────────────> HTTPException + detail
└── 스트리밍 ──────────> StreamingResponse
```

---

## Project Structure

```
app/
├── main.py              # Application factory, lifespan
├── config.py            # Settings (pydantic-settings)
├── dependencies.py      # Shared dependencies
├── routers/
│   ├── __init__.py
│   ├── users.py
│   └── orders.py
├── models/
│   ├── __init__.py
│   ├── user.py          # SQLAlchemy models
│   └── order.py
├── schemas/
│   ├── __init__.py
│   ├── user.py          # Pydantic request/response
│   └── order.py
├── services/
│   ├── __init__.py
│   ├── user_service.py  # Business logic
│   └── order_service.py
├── repositories/
│   ├── __init__.py
│   └── user_repo.py     # Data access layer
└── middleware/
    ├── __init__.py
    └── logging.py
```

## Application Lifespan

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup
    await Database.connect(settings.database_url)
    await RedisClient.connect(settings.redis_url)
    yield
    # Shutdown
    await Database.disconnect()
    await RedisClient.close()

app = FastAPI(
    title="My Service",
    version="1.0.0",
    lifespan=lifespan,
)
```

## Dependency Injection

```python
from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncIterator[AsyncSession]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    payload = decode_jwt(token)
    user = await UserRepository(db).find_by_id(payload["sub"])
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Type aliases for common dependencies
DbSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
```

## Pydantic v2 Schemas

```python
from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    name: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("비밀번호에 대문자가 포함되어야 합니다")
        if not any(c.isdigit() for c in v):
            raise ValueError("비밀번호에 숫자가 포함되어야 합니다")
        return v

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str
    created_at: datetime

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int

    @computed_field
    @property
    def has_next(self) -> bool:
        return self.page < self.pages
```

## Async Endpoints

```python
from fastapi import APIRouter, HTTPException, Query, status

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    db: DbSession,
) -> User:
    existing = await UserRepository(db).find_by_email(payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    user = User(**payload.model_dump())
    user.password_hash = hash_password(payload.password)
    db.add(user)
    await db.flush()
    return user

@router.get("/", response_model=PaginatedResponse[UserResponse])
async def list_users(
    db: DbSession,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
) -> dict:
    total = await UserRepository(db).count()
    users = await UserRepository(db).find_all(offset=(page - 1) * size, limit=size)
    return {
        "items": users,
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size,
    }

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: DbSession) -> User:
    user = await UserRepository(db).find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## Background Tasks

```python
from fastapi import BackgroundTasks

@router.post("/users/", status_code=201)
async def create_user(
    payload: UserCreate,
    db: DbSession,
    background_tasks: BackgroundTasks,
) -> UserResponse:
    user = await user_service.create(db, payload)
    background_tasks.add_task(send_welcome_email, user.email, user.name)
    background_tasks.add_task(track_signup_event, user.id)
    return user

async def send_welcome_email(email: str, name: str) -> None:
    async with create_http_client() as client:
        await client.post(
            f"{settings.email_service_url}/send",
            json={"to": email, "template": "welcome", "vars": {"name": name}},
        )
```

## Middleware

```python
import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "method=%s path=%s status=%d duration_ms=%.1f",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        response.headers["X-Process-Time"] = f"{duration_ms:.1f}ms"
        return response

# Rate Limiting with slowapi
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.get("/search")
@limiter.limit("30/minute")
async def search(request: Request, q: str = Query(min_length=1)) -> list[dict]:
    return await search_service.search(q)

# CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Error Handling

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, status_code: int, detail: str, code: str = "ERROR"):
        self.status_code = status_code
        self.detail = detail
        self.code = code

class NotFoundError(AppException):
    def __init__(self, resource: str, id: int | str):
        super().__init__(404, f"{resource} not found: {id}", "NOT_FOUND")

class ConflictError(AppException):
    def __init__(self, detail: str):
        super().__init__(409, detail, "CONFLICT")

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "detail": exc.detail}},
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled error: path=%s error=%s", request.url.path, exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_ERROR", "detail": "Internal server error"}},
    )
```

## WebSocket Support

```python
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self) -> None:
        self.active: dict[str, WebSocket] = {}

    async def connect(self, ws: WebSocket, client_id: str) -> None:
        await ws.accept()
        self.active[client_id] = ws

    def disconnect(self, client_id: str) -> None:
        self.active.pop(client_id, None)

    async def send(self, client_id: str, data: dict) -> None:
        if ws := self.active.get(client_id):
            await ws.send_json(data)

    async def broadcast(self, data: dict) -> None:
        for ws in self.active.values():
            await ws.send_json(data)

manager = ConnectionManager()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(ws: WebSocket, client_id: str):
    await manager.connect(ws, client_id)
    try:
        while True:
            data = await ws.receive_json()
            await manager.broadcast({"from": client_id, **data})
    except WebSocketDisconnect:
        manager.disconnect(client_id)
```

## Database Integration (SQLAlchemy Async)

```python
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(
    settings.database_url,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    echo=settings.debug,
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str]
    password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
```

## Authentication (OAuth2 + JWT)

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)) -> str:
    payload = {**data, "exp": datetime.utcnow() + expires_delta}
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")

def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e

@router.post("/auth/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DbSession,
) -> dict:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
```

## Testing

```python
import pytest
from httpx import AsyncClient, ASGITransport

@pytest.fixture
def app():
    from app.main import create_app
    return create_app()

@pytest_asyncio.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture
async def auth_client(client, test_user):
    token = create_access_token({"sub": str(test_user.id)})
    client.headers["Authorization"] = f"Bearer {token}"
    yield client

async def test_create_user(client: AsyncClient):
    # Given
    payload = {"email": "test@example.com", "name": "Test", "password": "StrongP4ss"}

    # When
    response = await client.post("/users/", json=payload)

    # Then
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"

async def test_create_user_duplicate_email(client: AsyncClient, test_user):
    # Given
    payload = {"email": test_user.email, "name": "Dup", "password": "StrongP4ss"}

    # When
    response = await client.post("/users/", json=payload)

    # Then
    assert response.status_code == 409
```

## Deployment

```python
# uvicorn production config
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# gunicorn with uvicorn workers (recommended for production)
# gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Dockerfile
"""
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
EXPOSE 8000
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
"""
```

## Performance Tips

```python
# 1. Use orjson for faster JSON serialization
from fastapi.responses import ORJSONResponse

app = FastAPI(default_response_class=ORJSONResponse)

# 2. Streaming large responses
from fastapi.responses import StreamingResponse

@router.get("/export")
async def export_data(db: DbSession) -> StreamingResponse:
    async def generate():
        async for chunk in iter_data_chunks(db):
            yield chunk.encode()

    return StreamingResponse(generate(), media_type="text/csv")

# 3. Gzip compression
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```
