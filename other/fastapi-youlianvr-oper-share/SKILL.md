---
name: fastapi
description: >-
  FastAPI and Pydantic conventions for API work: `Annotated` parameters and
  dependencies, return types and response models, router-level parameters, async
  versus sync path operations, JSON Lines / SSE / byte streaming, serving a built
  frontend, and native OpenTelemetry. Use when writing or reviewing a FastAPI app
  in this workspace.
---

# FastAPI

> Part of the `dev` router. The body below is the core; details live in
> `references/` and are read by topic.

## Choosing a reference

| Need | Read |
|---|---|
| Models, validation, no `RootModel`, no `...` | `references/pydantic.md` |
| Response shapes, filtering, `response_model` | `references/responses.md` |
| Routing, prefixes, tags, shared dependencies | `references/path-operations.md` |
| `yield` dependencies, scopes, class dependencies | `references/dependencies.md` |
| JSON Lines, SSE, byte streaming | `references/streaming.md` |
| Frontend serving, OpenTelemetry, uv/Ruff/ty, Asyncer/SQLModel/HTTPX | `references/frontend-and-telemetry.md`, `references/other-tools.md` |

## The `fastapi` CLI

```bash
fastapi dev      # local, reload
fastapi run      # production
```

Prefer the entrypoint in `pyproject.toml`; pass a path only when that is not possible:

```toml
[tool.fastapi]
entrypoint = "my_app.main:app"
```

## `Annotated` for parameters and dependencies

Always prefer `Annotated`; it keeps signatures reusable and typed.

```python
from typing import Annotated
from fastapi import Depends, FastAPI, Path, Query

app = FastAPI()

def get_current_user():
    return {"username": "johndoe"}

CurrentUserDep = Annotated[dict, Depends(get_current_user)]

@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(ge=1, description="The item ID")],
    q: Annotated[str | None, Query(max_length=50)] = None,
    current_user: CurrentUserDep = None,
):
    return {"message": "Hello World"}
```

## No `...` for required fields

Do not use `...` as a default for required parameters or model fields; a missing
default already means required.

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float = Field(gt=0)
```

## Return types and response models

Declare a return type when possible: FastAPI validates, filters, documents and
serializes from it, and Pydantic does the serialization in Rust.

```python
@app.get("/items/me")
async def get_item() -> Item:
    return Item(name="Plumbus", description="All-purpose home device")
```

Use `response_model` only when the public schema differs from what the function
returns. Do not use `ORJSONResponse` / `UJSONResponse` — deprecated; the return
type covers the performance case.

## Routers

Declare prefix, tags and shared dependencies on the `APIRouter`, not in
`include_router()`.

```python
router = APIRouter(prefix="/items", tags=["items"], dependencies=[Depends(get_current_user)])

@router.get("/")
async def list_items():
    return []

app.include_router(router)
```

## Dependencies

Use a dependency when the logic cannot live in Pydantic validation, needs an
external resource, needs cleanup via `yield`, or is shared across endpoints.
Apply shared ones at the router level.

## Async versus sync

`async def` only when every call inside is genuinely awaitable and non-blocking.
When in doubt use `def`: FastAPI runs it in a threadpool, so it does not block the
loop. Blocking calls inside `async` functions work but destroy throughput; for
mixing the two, use Asyncer (`references/other-tools.md`).

## Streaming

```python
from collections.abc import AsyncIterable
from fastapi import FastAPI
from fastapi.sse import EventSourceResponse, ServerSentEvent

app = FastAPI()

@app.get("/events", response_class=EventSourceResponse)
async def stream_events() -> AsyncIterable[ServerSentEvent]:
    yield ServerSentEvent(data={"status": "started"}, event="status", id="1")
```

Plain objects are serialized as SSE `data:` fields; `ServerSentEvent` gives full
control, `raw_data` takes pre-formatted strings. JSON Lines and byte streaming:
`references/streaming.md`.

## No `RootModel`

Use `Annotated` with validation utilities instead of a wrapper model:

```python
@app.post("/items/")
async def create_items(items: Annotated[list[int], Field(min_length=1), Body()]):
    return items
```

## One HTTP operation per function

One function per method keeps concerns separate and the OpenAPI document honest.
Do not branch on the verb inside a single handler.
