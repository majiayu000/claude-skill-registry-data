---
name: python-testing
description: >
  Apply backend pytest conventions: expects assertions, async fixtures, autospecced
  repository ports, test paths and layer-specific examples. Use when writing or
  refining a Python test under backend/tests. Choosing checks, diagnosing failures
  or assessing coverage belongs to verify-change; TypeScript tests use their own guidance.
---

# Python Testing — SaaS Bootstrap Backend

Use this reference for test syntax, fixtures and placement after the behavior to
verify is identified. [verify-change](../verify-change/SKILL.md) owns test selection,
diagnosis, coverage scope and evidence; [TDD](../tdd/SKILL.md) describes the incremental
red/green method. Consulting these conventions does not start another workflow.

## Applying the conventions

1. Read the source file to test
2. Determine the **architectural layer** (domain, application, infrastructure, presentation)
3. Read existing fixtures in `tests/conftest.py` and relevant module `conftest.py` files
4. Read the **layer-specific patterns** from [references/patterns.md](references/patterns.md)
5. Write the test at the matching path for the selected behavior. Follow the
   project's verification guide for commands, markers and services; API tests
   require the API selector. Tests are not selected by source layer alone.

## Path Convention

Source: `backend/src/<module>/<layer>/<feature>/<file>.py`
Test: `backend/tests/<module>/<layer>/<feature>/test_<file>.py`

Ensure `__init__.py` exists in every directory of the test path.

## Core Rules

- **Value assertions** use `expects` (`expect(x).to(equal(y))`), never bare `assert`.
  Known debt: some installed tests still use bare `assert`
  (`tests/tenants/presentation/test_tenant_user_endpoint.py`,
  `tests/common/test_settings.py`); do not copy it.
- **Exceptions**: `with pytest.raises(SomeDomainError): await use_case.execute()`.
  It awaits the coroutine inside the block, so it works for async code. Do not
  write try/except capture blocks, and do not use the `raise_error` matcher on an
  async method (it never runs the coroutine body).
- **Calls on mocks**: autospecced async methods are `AsyncMock`s; assert with
  `assert_awaited_once_with(...)`, `assert_not_awaited()` or read `await_args`.
- **Standalone functions** — never classes with `@staticmethod`
- **AAA pattern** — blank line before Assert block
- **async by default** — `async def test_...` for async code. `asyncio_mode = "auto"`
  is configured in `backend/pyproject.toml`; no `@pytest.mark.asyncio` needed.
- Cover the error path, and for tenant-scoped behavior both the allowed and a
  wrong tenant scope.
- Test naming: `test_<action>__<scenario>` (double underscore separates action from scenario)

## Available Fixtures

The conftest files and the `[tool.pytest.ini_options]` markers in
`backend/pyproject.toml` are the source of truth. This summary helps you find
them; read the fixture before relying on its shape, and trust the code if they
disagree.

### Global (`tests/conftest.py`)
- `tenant_id`: random UUID
- `tenant`: `Tenant` domain model (ACTIVE status, fixed slug `test-company`)
- `setup_database` (session-scoped, requested by DB fixtures): creates an exclusive
  test database and all tables, drops it on teardown
- `database_config` (session-scoped): the shared engine, disposed at the end
- `session_maker`: its `async_sessionmaker`, to read back through a new session
- `async_session`: function-scoped `AsyncSession` for DB operations

### E2E API (`tests/api/conftest.py`)
- `BASE_URL` (from `E2E_BASE_URL`) and `LoginTestContext`: import them, never hard-code the URL
- `api_key_header`: admin API key header dict
- `new_registered_user`: registers test user via HTTP
- `new_registered_tenant`: registers test tenant via HTTP
- `login_user`: `LoginTestContext` with `access_token`, `refresh_token`, `tenant_slug`, `tenant_id`

### Module-level (in `tests/<module>/<layer>/conftest.py`)
Place autospecced ports and buses here with
`create_autospec(spec=Port, spec_set=True, instance=True)`; e.g.
`tests/users/application/conftest.py` provides `query_bus` and `command_bus`.

### Inline (in test file)
Use for fixtures specific to that test file only (e.g., `use_case`, `orm_instance`).

## Test Markers

```python
@pytest.mark.single       # Run with pytest -m single — for debugging one test
@pytest.mark.api          # API/E2E test (module-level `pytestmark`)
@pytest.mark.skip(reason="...")
```

`db` is added automatically by `pytest_collection_modifyitems` in
`tests/conftest.py` to every test that requests `setup_database` or
`async_session`; do not add it by hand. Add it manually only for a DB test that
uses neither fixture (`tests/common/database/test_migrations.py`).

## Database isolation gotchas

- `async_session` does not wrap the test in a rolled-back transaction, and
  repository writes commit through `atomic_transaction`. Rows persist in the test
  database for the rest of the pytest session.
- Therefore generate unique slugs/emails per test (`f"t-{uuid4().hex[:8]}"`); the
  `tenant` fixture's fixed slug collides if two tests persist it.
- Do not use the `get_scoped_session` factories in `src/common/database/factories/`
  from tests; they open their own engine outside `async_session`.
- pytest-asyncio loop scope: `backend/pyproject.toml` sets both
  `asyncio_default_fixture_loop_scope` and `asyncio_default_test_loop_scope` to
  `session`, so the session-scoped `database_config` engine (disposed at the end)
  is shared safely; `async_session` opens a session from its `session_maker`.
- Repository adapters have integration tests against PostgreSQL
  (`tests/users/infrastructure/repositories/`); check durability by reading back
  through a new session, since a flush-only write looks correct inside the same
  one.
- Warnings are not ignored globally: fix a new `DeprecationWarning` or add a
  targeted filter with the reason.

## Quick Reference by Layer

| Layer                  | DB?  | Async? | Mocks?        | Exemplar / fixture source |
|------------------------|------|--------|---------------|---------------------------|
| Domain                 | No   | No     | No            | `tests/common/domain/models/tenants/test_tenant_user.py` |
| Application            | No   | Yes    | Yes (ports, buses) | `tests/users/application/use_cases/tenant_user/test_remover.py` |
| Infrastructure         | Yes  | Yes    | No            | `async_session` |
| Presentation (unit)    | No   | Yes    | Fakes via `monkeypatch` | `tests/tenants/presentation/test_tenant_user_endpoint.py` |
| Presentation (API/E2E) | Stack| No*    | No            | `tests/api/test_users.py`, `login_user` |

*API tests use `requests` (sync HTTP client) against a running stack.

For detailed patterns and examples per layer, see [references/patterns.md](references/patterns.md).
