---
name: consistency
description: Audits codebase for consistency after building features or pulling from reference repos. Claude MUST run this automatically after /verify passes. Do not wait for user to ask.
allowed-tools: Read Grep Glob Bash(poetry run pytest *)
argument-hint: "[optional: specific directory or feature to check, e.g. 'services/' or 'F4']"
---

You are a code consistency auditor for ConvoPilot. The codebase pulls patterns from 4 different reference repos, so things can drift. Your job is to find and flag inconsistencies.

**Scope:** $ARGUMENTS (if empty, audit the entire backend at service-one/src/api/)

---

## 1. File & Directory Structure

Check that every service follows the same layout:
```
services/<feature>/
  __init__.py
  service.py
```

Flag: missing __init__.py, files named differently (e.g. `handler.py` instead of `service.py`), nested directories that break the pattern.

Reference pattern: `services/ingestion/service.py`

---

## 2. Import Style

All files must use the same import ordering:
```python
# stdlib
# third-party
# local (api.*)
```

Flag: mixed ordering, relative imports (use `from api.x import y` not `from .x import y`), direct SDK imports (`import anthropic`, `import openai`, `import google.generativeai`) in service code.

Reference: `services/ingestion/service.py`, `services/interpretation/service.py`

---

## 3. Class & Function Naming

- Services: `<Name>Service` (e.g. `IngestionService`, `SpecBuilderService`)
- One class per service file
- Constructor: `def __init__(self, db: AsyncSession)` or `def __init__(self, llm: LLMInterface, db: AsyncSession)`
- All I/O methods: `async def`

Flag: classes not ending in `Service`, sync methods doing I/O, constructors with different parameter patterns.

---

## 4. Database Patterns

- Use `self._db` (underscore prefix for private)
- Use `flush()` never `commit()`
- Use `select()` from sqlalchemy, not raw SQL
- Use `scalar_one_or_none()` for single results
- Use `scalars().all()` for lists
- Always return ORM model instances, not dicts

Flag: `commit()` calls, raw SQL strings, returning dicts instead of models, inconsistent private attribute naming.

Reference: `services/ingestion/service.py`

---

## 5. Error Handling

- Services raise `ValueError` for invalid input
- Routes catch exceptions and return LLD Section 3.4 format:
  ```json
  {"error": {"code": "...", "message": "...", "request_id": "..."}}
  ```
- Use the `_error_response()` helper in routes
- LLM failures: log warning, don't crash — graceful degradation

Flag: bare `except:`, inconsistent error shapes, missing request_id, services returning HTTP responses directly.

Reference: `routes/test_cases.py`

---

## 6. Pydantic Schemas

- All in `schemas/<feature>.py`
- Response models use `model_config = ConfigDict(from_attributes=True)`
- Request models use `@model_validator` for input validation
- Field types: `str | None = None` (not `Optional[str]`)

Flag: raw dicts in responses, missing `from_attributes`, `Optional[]` instead of `| None`, schemas defined inside route files.

---

## 7. Route Patterns

- Router: `APIRouter(prefix="/<resource>", tags=["<resource>"])`
- Dependencies: `db: AsyncSession = Depends(get_db_session)`
- Request ID: `request_id = getattr(request.state, "request_id", "")`
- POST returns 201, GET returns 200, not found returns 404
- response_model on every route

Flag: missing response_model, wrong status codes, missing request_id in errors, services instantiated at module level instead of per-request.

Reference: `routes/test_cases.py`

---

## 8. LLM Usage

- All calls through `LLMInterface` from `api/llm/interfaces.py`
- Provider via `get_llm_provider()` from `api/llm/factory.py`
- temperature=0 on all evaluation/judge calls
- System prompt as `LLMMessage(role="system", content=...)`
- Parse responses handling both raw JSON and markdown code blocks

Flag: direct SDK imports, temperature != 0 on eval calls, no JSON parse fallback.

Reference: `services/interpretation/service.py`

---

## 9. Logging

- `import logging` + `logger = logging.getLogger(__name__)`
- Use `logger.info()`, `logger.warning()`, `logger.error()`
- Never log secrets, auth_headers, or API keys
- Include context: `logger.warning("Spec builder failed for test_case %s: %s", tc_id, e)`

Flag: `print()` statements, logging secrets, no logger defined, inconsistent logger names.

---

## 10. Code from Reference Repos

When code is adapted from external reference repos:
- Rename classes/functions to match ConvoPilot conventions (above)
- Replace any direct SDK imports with our LLM interface
- Replace sync code with async
- Replace their DB patterns with our SQLAlchemy async patterns
- Remove any framework-specific dependencies (test mocks, rollbar, etc.)

Flag: foreign class names still present, unused third-party SDK imports in service code, sync HTTP calls, references to external gateways.

---

## Output Format

```
## Consistency Audit Report

### Passes
- [list what's consistent]

### Issues Found
1. **[Category]** — `file:line` — description — how to fix
2. ...

### Summary
X issues found across Y files. Priority fixes: [list top 3]
```

Run this audit, then report findings. Do NOT auto-fix — just report. The user decides what to fix.
