---
name: python-testing
description: Python testing patterns. Use when writing tests, setting up pytest, mocking dependencies, or reviewing test code.
---

# Python Testing

## Philosophy

- Tests document expected behavior—prioritize clarity over cleverness
- Test behavior at boundaries, not internal implementation
- **Ask before writing**: "What bug would this test catch?" If no clear answer, skip it

## Rules

- **Must** follow AAA pattern: Arrange, Act, Assert (clearly separated)
- **Should** use `@pytest.mark.parametrize` for testing multiple inputs
- **Should** use markers (`@pytest.mark.slow`, `@pytest.mark.integration`) for categorization

## Tooling

| Need | Use | Avoid |
|------|-----|-------|
| Mocking | `pytest-mock` (`mocker` fixture) | `unittest.mock.patch` directly |
| HTTP mocking | `respx` (for httpx) | Manual response mocks |
| Async testing | `pytest-asyncio` with `asyncio_mode = "auto"` | Manual event loop management |
| DB testing | In-memory SQLite (`aiosqlite`) or testcontainers | Mocking the ORM |

## Fixtures

- **Must** use fixtures for reusable setup—extract if same mock appears in 2+ tests
- **Must** use `httpx.AsyncClient` with `ASGITransport` for FastAPI test client
- **Should** scope fixtures appropriately: `function` default, `module` for expensive setup
- **Avoid** `autouse=True` except for truly universal setup

## Test Organization

```
tests/
├── conftest.py      # Shared fixtures
├── unit/            # Fast, isolated, mock all externals
└── integration/     # Real dependencies, slower
```

## What to Test

- **Do test**: Business logic, edge cases, error paths, API contracts, regressions
- **Avoid testing**: Framework behavior, library internals, trivial getters/setters
- **Never** write tests just to hit coverage numbers
