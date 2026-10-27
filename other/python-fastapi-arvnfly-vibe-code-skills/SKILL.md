---
name: python-fastapi
description: "FastAPI async web services, Pydantic v2 validation, dependency injection, and background tasks."
---

# FastAPI & Async Python Protocol

Build lightning-fast, typed Python REST APIs.

---

## 1. Async Endpoints & Concurrency

1. Define I/O-bound endpoints with `async def` and `await` async DB queries.
2. Use standard `def` for CPU-bound routes so FastAPI executes them in an internal thread pool without blocking event loops.

---

## 2. Pydantic v2 Models

- Use `field_validator` and `model_validator` for strict schema enforcement.
- Set `model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)`.
