---
name: python-tdd-patterns
description: >
  Use this for the Python-specific realization of the SKELETON→RED→GREEN→REFACTOR
  TDD cycle — Protocol-based interface skeletons, NotImplementedError stubs,
  pytest fixtures, parametrize tables, AsyncMock for async ports, async test
  shape with `pytest-asyncio`, and `pytest.raises` for error-path verification.
  Pairs with the language-neutral `tdd-patterns` skill (cycle + agent
  coordination); this skill is the Python syntax layer.
  Triggers: pytest, async def test_, @pytest.mark.asyncio, AsyncMock, MagicMock, parametrize, pytest.raises, NotImplementedError, fixture, monkeypatch, Protocol.
version: 1.0.0
last-evolved-in-run: v0.6.0-rc.0-sanitization
status: stable
tags: [python, tdd, testing, pytest]
---

# python-tdd-patterns (v1.0.0)

## Scope

Realizes the cycle defined in shared-core `tdd-patterns` for Python targets. Agent coordination is language-neutral and lives there; everything below is Python syntax.

## SKELETON — Protocol port + stub implementation

```python
# motadatapysdk/ports/repository.py
from typing import Protocol, runtime_checkable, Generic, TypeVar

T = TypeVar("T")

@runtime_checkable
class Repository(Protocol[T]):
    """Persistence operations for an entity."""
    async def create(self, entity: T) -> T: ...
    async def get_by_id(self, entity_id: str) -> T | None: ...
```

```python
# motadatapysdk/application/service.py
from dataclasses import dataclass

@dataclass(frozen=True, slots=True, kw_only=True)
class CreateEntityCommand:
    name: str

class Service:
    def __init__(self, *, repo: Repository[Entity]) -> None:
        self._repo = repo

    async def create_entity(self, cmd: CreateEntityCommand) -> Entity:
        """STUB — raises NotImplementedError until GREEN phase."""
        raise NotImplementedError
```

Skeleton rules:
- All Protocols fully defined (every method signature with types)
- Constructors keyword-only (`*` separator) for clarity
- Method stubs raise `NotImplementedError` (typed checkers like mypy keep flagging missing impl until real code lands)
- `@runtime_checkable` lets tests use `isinstance(impl, Repository)` for sanity

## RED — assertion-first failing tests with AsyncMock

```python
import pytest
from unittest.mock import AsyncMock, create_autospec

@pytest.mark.asyncio
async def test_create_entity_returns_entity_with_id():
    mock_repo = create_autospec(Repository, instance=True)
    captured: list[Entity] = []

    async def fake_create(entity: Entity) -> Entity:
        assert entity.id, "ID should be generated before persistence"
        captured.append(entity)
        return entity

    mock_repo.create.side_effect = fake_create

    svc = Service(repo=mock_repo)
    entity = await svc.create_entity(CreateEntityCommand(name="test"))

    assert entity is not None
    assert entity.id
    mock_repo.create.assert_awaited_once()
```

Conventions:
- `create_autospec(Repository, instance=True)` enforces signature parity — calling with wrong args fails the test, not the production code months later.
- `side_effect = async_callable` lets you assert on the argument shape AND return a constructed entity.
- `assert_awaited_once()` (not `assert_called_once()`) for AsyncMock — the await matters.
- Plain `assert` is sufficient; pytest rewrites it to show useful diffs.

## RED — parametrize table

```python
@pytest.mark.parametrize(
    "cmd, want_exc",
    [
        pytest.param(CreateEntityCommand(name=""),    InvalidNameError, id="empty-name"),
        pytest.param(CreateEntityCommand(name="x"),   None,             id="valid"),
    ],
)
@pytest.mark.asyncio
async def test_create_entity_validation(cmd, want_exc):
    mock_repo = create_autospec(Repository, instance=True)
    if want_exc is None:
        mock_repo.create.return_value = Entity(id="e1", name=cmd.name)

    svc = Service(repo=mock_repo)

    if want_exc is not None:
        with pytest.raises(want_exc):
            await svc.create_entity(cmd)
    else:
        result = await svc.create_entity(cmd)
        assert result.id
```

Conventions:
- `pytest.param(..., id="...")` gives readable test names (`test_create_entity_validation[empty-name]`).
- `pytest.raises(ExceptionClass)` is the canonical error-path assertion. Use `match="regex"` to assert message shape when relevant.

## RED — fixture composition

```python
@pytest.fixture
def mock_repo() -> AsyncMock:
    return create_autospec(Repository, instance=True)

@pytest.fixture
def service(mock_repo: AsyncMock) -> Service:
    return Service(repo=mock_repo)

@pytest.mark.asyncio
async def test_with_fixtures(service: Service, mock_repo: AsyncMock) -> None:
    mock_repo.create.return_value = Entity(id="e1")
    entity = await service.create_entity(CreateEntityCommand(name="x"))
    assert entity.id == "e1"
```

`function`-scoped fixtures (default) recreate per test — clean isolation. Use `module` or `session` scope only when setup is expensive (e.g., spinning up a testcontainer).

## GREEN — implementation rules

After RED, code-generator reads all `tests/` and writes minimum impl:

- Read every `test_*.py` in the package first
- If a test uses `pytest.raises(ErrSomething)`, raise exactly that exception class
- If a test asserts a UUID is non-empty, generate one
- Run `pytest -x --no-header` after each significant change
- Don't add behavior that isn't tested

## Anti-patterns

**1. Bare `Mock()` without `spec=`.** `mock = Mock()`; `mock.create(...)` succeeds even if `create` doesn't exist on the protocol. Always `create_autospec(Protocol, instance=True)` or `Mock(spec=Protocol)`.

**2. `assert_called_once()` on AsyncMock.** Awaitable mocks need `assert_awaited_once()` — the regular call assertion misses await semantics.

**3. Sleeping in tests.** `await asyncio.sleep(0.5)` to "wait for things" is flaky. Use `pytest.approx` for time-sensitive assertions and `freezegun` for time control.

## Cross-references

- shared-core `tdd-patterns` — agent cycle and orchestration
- `python-pytest-patterns` — fixture scope, parametrize, marker registration
- `python-mock-strategy` — Fake-first decision tree, AsyncMock vs MagicMock
- `python-exception-patterns` — exception class hierarchy + `pytest.raises` match patterns
- `python-asyncio-patterns` — async test conventions, TaskGroup, anyio
