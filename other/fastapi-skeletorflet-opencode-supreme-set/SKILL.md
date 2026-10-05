---
name: fastapi
description: FastAPI Python web framework. Use when building async APIs with FastAPI, Pydantic v2 models, dependency injection, WebSocket endpoints, or OpenAPI auto-documentation.
---

## fastapi

Modern Python web framework built on Starlette and Pydantic for high-performance async APIs.

### Core Concepts
- Async endpoints: define routes with `async def`, FastAPI handles concurrency via asyncio
- Pydantic v2 models: request/response validation with `BaseModel`, automatic JSON Schema generation
- Dependency Injection: `Depends()` resolves reusable components across route handlers
- OpenAPI/Swagger: auto-generated interactive docs at /docs and /redoc from type hints

### Common Patterns
- Background tasks: `BackgroundTasks` for post-response operations like email or logging
- CORS middleware: `CORSMiddleware` with allow_origins for cross-origin browser requests
- WebSocket: `WebSocket` endpoint with `websocket.accept()` for real-time bidirectional communication
- Router modularity: `APIRouter` with prefix and tags to organize endpoints by domain

### Best Practices
- Use Pydantic v2 `model_validator` over v1 custom validators for cleaner validation logic
- Split routes into versioned routers (v1, v2) for backward-compatible API evolution
- Set `response_model` on route decorators to control serialization and docs schema
- Use `httpx.AsyncClient` with `TestClient` for testing async endpoint chains

### Common Code Patterns
- `@app.post("/items")` with `Depends(get_current_user)` for auth-gated endpoints
- `async with db.session()` context manager for transactional database operations
