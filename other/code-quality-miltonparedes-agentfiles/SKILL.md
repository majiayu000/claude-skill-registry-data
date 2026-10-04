---
name: python-code-quality
description: Python code quality standards. Use when working with types, linting, type checking, exceptions, logging, or configuring ruff/ty/pyproject.toml.
---

# Python Code Quality

## Typing Rules

- **Must** annotate all function signatures (parameters and return)
- **Must** type HTTP responses with Pydantic models—never return raw `dict` from API endpoints
- **Must** use generics (`list[str]`, `dict[str, Any]`)—never bare `list`, `dict`, `tuple`
- **Must** use Pydantic models at API boundaries (requests, responses, external data)
- **Should** use `T | None` over `Optional[T]`
- **Should** use keyword-only args (`*`) for functions with 3+ parameters
- **Should** use `TypeAlias` for complex dict types instead of repeating `dict[str, Any]`
- **Avoid** `Any` except at true boundaries; prefer specific types or generics
- **Never** use mutable defaults (`def f(items=[])`); use `None` and initialize inside

## Type Choice Guide

| Need | Use |
|------|-----|
| API request/response | Pydantic `BaseModel` |
| DB + API unified | `SQLModel` |
| Internal data transfer | `dataclass(frozen=True, slots=True)` |
| Dict with known keys | `TypedDict` |
| Primitive wrapper | `NewType` |
| Fixed string values | `Literal` |

- **Should** use `NewType` for domain primitives (`UserId`, `OrderId`) to prevent mixing
- **Avoid** stringly-typed code—prefer enums or `Literal` for fixed values

## Tooling

- **Must** use `ruff` for linting and formatting
- **Must** use `ty` (astral.sh) for type checking
- **Must** run before committing: `ruff format . && ruff check --fix . && ty check .`
- **Must** enable `ANN`, `TCH`, `I`, `E`, `F`, `W` ruff rules
- **Should** use `line-length = 120`

See `../project-setup/references/pyproject.template.toml` for complete configuration.

## Exceptions

- **Must** define a base `ServiceError` with `message`, `code`, `status_code`
- **Must** create specific exceptions inheriting from base (`NotFoundError`, `ConflictError`)
- **Never** swallow exceptions silently—always re-raise or wrap with context
- **Should** use `logger.exception()` to include traceback before re-raising

## Logging

- **Must** use structured logging (`structlog` or `loguru` with JSON sink in production)
- **Must** include `request_id` in all log entries
- **Never** log sensitive data (tokens, passwords, PII)

## Caching

- **Should** use `@lru_cache` for expensive pure functions
- **Must** set `maxsize` based on expected input cardinality
- **Never** cache functions with side effects or mutable state
- **Should** use `async-lru` (`@alru_cache`) for async functions (not bare `@lru_cache`)
