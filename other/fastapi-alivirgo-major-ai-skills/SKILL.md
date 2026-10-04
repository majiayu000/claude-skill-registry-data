---
name: fastapi
description: "Build and test FastAPI services with Pydantic models, dependency injection, async routes, OpenAPI, and authentication hooks."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["fastapi", "python", "pydantic", "openapi", "api", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# FastAPI Python APIs AI Skill Guide

## Overview & Engine Architecture

FastAPI builds HTTP APIs with type hints and Pydantic validation, generating OpenAPI automatically. Routes can be sync or async; dependencies inject auth, DB sessions, and settings. Agents keep CPU-bound or blocking ORM calls from stalling the event loop, validate every input model, and document response models explicitly.

```
uvicorn / gunicorn workers
        |
     FastAPI app
   +----+----+----+
   | routers       |
   | Depends()     |
   | Pydantic I/O  |
   | OpenAPI /docs |
   +---------------+
```

## When to use this skill

- Creating versioned REST/JSON APIs in Python
- Adding auth dependencies and consistent error handlers
- Generating clients from `/openapi.json`
- Writing API tests with `TestClient` or httpx ASGI transport

## Operational directives

1. Define request and response models; avoid raw `dict` returns in public APIs.
2. Use `APIRouter` per domain (`/users`, `/billing`).
3. Put shared settings in a cached `Settings` dependency (pydantic-settings).
4. Prefer async DB drivers for async routes; otherwise run sync work in a threadpool consciously.
5. Never commit secrets; load from environment.

## App sketch

```python
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Inventory API", version="1.2.0")

class ItemIn(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    qty: int = Field(ge=0)

class ItemOut(ItemIn):
    id: int

def get_current_user(auth: str | None = None) -> str:
    if not auth:
        raise HTTPException(status_code=401, detail="unauthorized")
    return "user"

@app.post("/items", response_model=ItemOut)
def create_item(body: ItemIn, user: str = Depends(get_current_user)) -> ItemOut:
    return ItemOut(id=1, **body.model_dump())
```

## Commands

```bash
uvicorn app.main:app --reload --port 8000
# OpenAPI UI: http://127.0.0.1:8000/docs
pytest -q
```

## Testing sketch

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_item_unauthorized():
    r = client.post("/items", json={"sku": "A", "qty": 1})
    assert r.status_code == 401
```

## Best practices

- Centralize exception handlers for domain errors.
- Use status codes correctly (`201` create, `204` delete, `409` conflict).
- Version APIs (`/v1`) when external clients exist.
- Emit structured logs with request IDs.

## Limitations

- BackgroundTasks are not a full job queue; use Celery/RQ/Arq for heavy work.
- WebSockets and GraphQL need additional libraries and patterns.
- Migration tooling (Alembic) is separate from FastAPI itself.

## Related skills

- `@postgresql` - database design behind the API
- `@python-packaging` - project layout, pytest, ruff
- `@docker` - containerizing uvicorn workers
