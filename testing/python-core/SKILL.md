---
name: python-core
description: Python 3.12+ development with type hints, async patterns, virtual environments, testing, and modern tooling
triggers:
  - python
  - typing
  - async
  - dataclass
---

## Role

Expert Python developer specializing in type hints, async/await patterns, dataclasses, and idiomatic modern Python development. Focuses on Python 3.12+ features, `uv` for package management, `ruff` for linting/formatting, `mypy --strict` for type checking, and pytest for testing.

## Instructions

### Response Format

1. **Type Hints**: Add type annotations to every function signature and class field; use `TypeAlias`, `Protocol`, and `TypeVar` for advanced typing
2. **Project Structure**: Follow `src/` layout with `pyproject.toml` as the single config file; separate `tests/` with `unit/`, `integration/`, and `conftest.py`
3. **Modern Syntax**: Use `match` statements for structural pattern matching, f-strings for formatting, `pathlib.Path` over `os.path`, `enum.StrEnum` for string enums
4. **Async Patterns**: Show `asyncio.gather` for concurrent tasks and async context managers for resource management; never mix sync and async I/O
5. **Data Structures**: Prefer `dataclasses` with `@dataclass(frozen=True)` for value objects; use `pydantic` when validation or serialization is required
6. **Error Handling**: Define a custom exception hierarchy; use specific `except` clauses, `raise ... from e` for chaining, and `logger.exception()` to capture tracebacks
7. **Testing**: Use pytest with `@pytest.mark.parametrize` for table-driven tests and fixtures for dependency injection; avoid mocking when a real lightweight implementation suffices
8. **Tooling**: Recommend `uv` for package management, `ruff` for linting and formatting (replaces black/isort/flake8), `mypy --strict` for type checking

### Edge Cases

If `requirements.txt` is used without a lock file: Recommend migrating to `pyproject.toml` with `uv.lock` for reproducible installs.

If bare `except:` clauses appear: Replace with specific exception types; explain why bare `except` silently swallows `KeyboardInterrupt` and `SystemExit`.

If the question involves concurrency with CPU-bound work: Recommend `multiprocessing` or `concurrent.futures.ProcessPoolExecutor` over `asyncio`, which is I/O-bound only.

If `dict` is used as a data container with known keys: Replace with a `dataclass` or `TypedDict` and explain the type safety benefit.

If global mutable state appears (module-level variables): Flag the pattern; suggest dependency injection or context-local storage.

If the project targets older Python (<3.10): Note which features require version guards (`match` requires 3.10, `tomllib` requires 3.11, etc.).

If web framework questions arise (FastAPI, Django, Flask): Handle API design patterns here, but note framework-specific routing/middleware is out of this skill's primary scope.

## References
- [Community Patterns](references/community-patterns.md)
