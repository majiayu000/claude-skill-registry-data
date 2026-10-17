---
name: aiwf-fastapi-coding
description: Use for FastAPI routes, Pydantic models, OpenAPI contracts, async boundaries, auth/CORS, and API validation.
---

# AIWF FastAPI Coding

## Core Rule

Treat FastAPI work as a typed API contract. Inspect FastAPI, Starlette, Pydantic, Uvicorn, dependency injection, and deployment settings before changing routes or models. Keep API behavior verifiable through OpenAPI, tests, and endpoint smokes.

## Workflow

1. Inspect `pyproject.toml`, requirements, app entrypoints, routers, dependency providers, settings, middleware, tests, and deployment commands.
2. Confirm Pydantic major version and FastAPI version before editing validators, model config, response models, or serialization behavior.
3. Preserve request/response contracts unless the task explicitly changes them. Update tests and OpenAPI-facing docs when contracts move.
4. Keep async routes non-blocking. Move blocking CPU, file, model, or network work into the project's existing worker/thread/process pattern.
5. Validate with the repo's API tests and a health or contract smoke.

## FastAPI Guardrails

- Use typed request bodies, path/query parameters, dependencies, and response models. Avoid loose `dict` contracts unless the API is intentionally schema-less.
- Treat Pydantic v1 examples as legacy and version-bound. Current FastAPI releases require Pydantic v2; inspect pinned versions before migrating old validators or models.
- Keep auth, CORS, CSRF, session, cookie, and token behavior explicit. Add `aiwf-security-guardrails` when those surfaces are touched.
- Prefer lifespan handlers for new startup/shutdown work and preserve the app's existing lifecycle pattern. Do not mix lifespan and event handlers or duplicate global initialization paths.
- Keep exception handlers and status codes consistent with existing API behavior.
- For streaming, WebSockets, SSE, upload, and background tasks, validate cancellation and resource cleanup.
- Avoid silently changing generated OpenAPI names that clients may depend on.

## Validation Defaults

Prefer existing commands. Useful fallbacks:

```powershell
python -m compileall <package-or-file>
python -m pytest
python -m uvicorn <module>:<app> --host 127.0.0.1 --port <port>
```

When starting a server, keep it local unless Shawn asks otherwise. For contract checks, use `TestClient`, `httpx`, or the repo's smoke client.

## Primary Source Anchors

- FastAPI documentation: https://fastapi.tiangolo.com/
- FastAPI tutorial and user guide: https://fastapi.tiangolo.com/tutorial/
- FastAPI release notes: https://fastapi.tiangolo.com/release-notes/

FastAPI and Pydantic behavior changes by version. Verify the installed versions before making version-specific edits.
