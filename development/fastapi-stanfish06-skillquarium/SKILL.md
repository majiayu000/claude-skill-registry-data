---
name: fastapi
description: Building HTTP/JSON APIs in Python with FastAPI — path/query/body params, Pydantic v2 models, async endpoints, dependency injection, the lifespan startup/shutdown pattern, error handling, and testing with TestClient/httpx. Use when creating a REST API or web backend in Python, adding endpoints, wiring request validation, or serving an ML model behind HTTP. Deploy with uvicorn/gunicorn (often via docker).
---

# FastAPI — Python web APIs

## Overview

FastAPI is an async Python web framework with automatic request validation (Pydantic v2)
and OpenAPI/Swagger docs out of the box. Use it for REST/JSON backends and for serving ML
models behind HTTP. Pairs with [[pydeseq2]]-style scientific code or any service layer;
containerize with [[docker]], set up the project with [[modern-python]].

```bash
uv add fastapi "uvicorn[standard]"
uv run uvicorn app:app --reload          # dev server, interactive docs at /docs
```

## Minimal app with validation

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Example API")

class Item(BaseModel):
    name: str
    price: float = Field(gt=0)
    tags: list[str] = []

DB: dict[int, Item] = {}

@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:        # path param, type-coerced + validated
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="not found")
    return DB[item_id]

@app.get("/items")
def list_items(limit: int = Query(10, le=100)) -> list[Item]:   # query param
    return list(DB.values())[:limit]

@app.post("/items/{item_id}", status_code=201)
def create_item(item_id: int, item: Item) -> Item:              # JSON body -> Pydantic
    DB[item_id] = item
    return item
```

Type hints drive everything: path/query params, JSON body parsing, response serialization,
and the OpenAPI schema. Return a Pydantic model or set `response_model=` to control output.

## Async & blocking work

```python
import httpx

@app.get("/proxy")
async def proxy():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.example.com/data")
    return r.json()
```

Use `async def` for I/O-bound endpoints (await async clients). For **blocking** CPU/IO work
(a sync DB driver, a heavy model) use a plain `def` endpoint — FastAPI runs it in a
threadpool so it won't block the event loop. Never call blocking code inside `async def`.

## Dependency injection

```python
from fastapi import Depends, Header

async def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

def require_token(x_token: str = Header()):
    if x_token != "secret":
        raise HTTPException(401, "bad token")

@app.get("/secure")
def secure(db=Depends(get_db), _=Depends(require_token)):
    return {"ok": True}
```

`Depends` resolves and caches per-request, supports `yield` for setup/teardown, and is the
idiomatic way to share DB sessions, auth, and config.

## Lifespan (startup/shutdown)

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model()    # startup: load once
    yield
    app.state.model.close()           # shutdown

app = FastAPI(lifespan=lifespan)
```

Use the `lifespan` context manager (the modern replacement for the deprecated
`@app.on_event("startup")`) to load models/connection pools once at boot.

## Testing

```python
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_create_and_get():
    assert client.post("/items/1", json={"name": "x", "price": 2}).status_code == 201
    r = client.get("/items/1")
    assert r.status_code == 200 and r.json()["name"] == "x"
```

`TestClient` (sync, Starlette) needs no running server. For async tests use
`httpx.ASGITransport` with `httpx.AsyncClient`. See [[pytest]] for fixtures/markers.

## Gotchas

- **Blocking inside `async def`** stalls the whole server — use `def` endpoints for sync work.
- **Pydantic v2:** `model_config`, `model_dump()`, `field_validator` (v1 `Config`/`.dict()`
  are gone). Validation errors auto-return HTTP 422 with field detail.
- **Production server:** `uvicorn` for a single process; behind a process manager use
  `gunicorn -k uvicorn.workers.UvicornWorker -w 4`. Put it behind nginx/a load balancer.
- **CORS:** browsers need `CORSMiddleware` configured explicitly.
- **Big request bodies / file uploads** use `UploadFile` (streamed), not `bytes`.

## Related

Test with [[pytest]]; containerize and serve via [[docker]]; project tooling in
[[modern-python]]; CI in [[github-actions-ci]]; GPU/serverless model serving via [[modal]].
