---
name: python-mock-strategy
description: >
  Use this when designing tests for a class with external dependencies, deciding
  whether to fake or mock a collaborator, reviewing a test that uses bare Mock()
  without spec=, replacing monkeypatch hacks with a Protocol-typed seam, or
  picking a test-double for HTTP / time / random / filesystem. Covers the
  Fake-first decision tree, Protocol-based dependency-injection seams,
  unittest.mock.AsyncMock(spec=...) and create_autospec for call-pattern
  assertions, respx and aioresponses for HTTP, freezegun for time, seeded
  random.Random and uuid patching, tmp_path vs pyfakefs, the pytest-mock mocker
  fixture, and patch-where-used import-path rules.
  Triggers: Mock, MagicMock, AsyncMock, spec=, patch, fake, Protocol, respx, freezegun, monkeypatch.setattr, create_autospec, pytest-mock.
---

# python-mock-strategy (v1.1.0)

## Rationale

A test that mocks too much asserts implementation, not behavior. A test that mocks too little turns into an integration test (slow, flaky). The Python pack's middle ground: design the SDK so each external dependency goes through a Protocol-typed seam; the test injects an in-memory Fake at that seam; only assert what the consumer would observe. Reach for `unittest.mock.AsyncMock(spec=...)` only when you specifically need call-pattern assertions (was-it-called, was-it-called-with) that a behavioral fake can't make.

This skill is cited by `code-reviewer-python` (test-quality review-criteria), `python-pytest-patterns` (Rule 14 narrow fakes), `python-asyncio-patterns` (AsyncMock for async dependencies), `python-mypy-strict-typing` (Protocol over ABC for fakeable seams), and `sdk-convention-devil-python` (C-14 testing convention).

## Activation signals

- Designing or reviewing tests for any class with external dependencies.
- Test code uses `Mock()` without `spec=`.
- Test patches a function inside the SDK rather than injecting at the boundary.
- Test asserts call-arg patterns when it could assert observable behavior.
- HTTP / DB / time / random / filesystem appears in code under test.
- Test is slow because every test spins up a real container.

## Core decision tree — Fake or Mock?

```
Does the test care about the SHAPE of internal calls (count, ordering, arguments)?
  └── YES → Mock with spec=Class
  └── NO  → Did the dependency have observable behavior the consumer relies on?
            └── YES → in-memory Fake (Protocol-typed)
            └── NO  → call it directly (it has no behavior worth doubling)
```

Fake is the default. Mock is the exception.

### Why Fake first

A Fake is a small purpose-built class implementing the SAME Protocol as the production dependency. It has BEHAVIOR — when you `put` then `get`, you get back what you put. It can be inspected (`fake.published`, `fake.calls`) for assertions. Compared to Mock:
- A Mock returns whatever `return_value=` says, regardless of internal state. A Fake's return derives from its state.
- A Mock's call assertions (`mock.publish.assert_called_once_with(...)`) couple the test to method ORDER. A Fake's state assertions test the OUTCOME the consumer observes.
- A Mock with `side_effect=Iterator` is a brittle script. A Fake handles re-entry naturally.

## Rule 1 — Design for the seam (Protocol)

```python
# motadatapysdk/storage.py
from typing import Protocol

class Backend(Protocol):
    """The seam through which Storage talks to its byte store.

    Implementations: HTTPBackend (production), FileBackend, FakeBackend (tests).
    """
    async def put(self, key: str, value: bytes) -> None: ...
    async def get(self, key: str) -> bytes | None: ...


class Storage:
    def __init__(self, config: Config, *, backend: Backend | None = None) -> None:
        self._backend = backend or HTTPBackend(config.base_url)
```

The `backend=` keyword-only parameter is how tests inject a Fake. In production it's left to default. This is dependency injection without a DI framework — just a constructor parameter.

Without the seam, tests resort to `monkeypatch.setattr` on the SDK's internals. That couples tests to internal symbol paths and breaks every refactor. The seam is the test-friendliness contract.

## Rule 2 — Write the Fake

```python
# tests/fakes.py
class FakeBackend:
    """In-memory Backend for tests.

    Tracks every put/get for assertion. Returns what was put; KeyError if absent.

    Examples:
        >>> fake = FakeBackend()
        >>> import asyncio
        >>> asyncio.run(fake.put("k", b"v"))
        >>> asyncio.run(fake.get("k"))
        b'v'
    """

    def __init__(self) -> None:
        self._store: dict[str, bytes] = {}
        self.put_calls: list[tuple[str, bytes]] = []
        self.get_calls: list[str] = []

    async def put(self, key: str, value: bytes) -> None:
        self.put_calls.append((key, value))
        self._store[key] = value

    async def get(self, key: str) -> bytes | None:
        self.get_calls.append(key)
        return self._store.get(key)

    # Test-only helpers
    @property
    def items(self) -> dict[str, bytes]:
        return dict(self._store)
```

The Fake declares two test-helper attributes (`put_calls`, `get_calls`) that the test asserts against. They are NOT part of the Backend Protocol — they're the Fake's introspection surface.

`mypy --strict` accepts FakeBackend as a Backend because the Protocol is structurally typed. No `class FakeBackend(Backend):` needed (and shouldn't — Protocols are duck-typed).

```python
# tests/test_storage.py
async def test_storage_put_and_get() -> None:
    fake = FakeBackend()
    storage = Storage(Config(base_url="<unused>"), backend=fake)

    await storage.put("user:1", b"alice")
    result = await storage.get("user:1")

    assert result == b"alice"
    assert fake.items == {"user:1": b"alice"}
```

The test asserts OUTCOME (`result == b"alice"`) and STATE (`fake.items`), not call patterns. If the Storage implementation refactors from `backend.put(key, value)` to `backend.put(value=value, key=key)`, the test still passes. That's the point.

## Rule 3 — When you do reach for Mock, use `spec=`

```python
from unittest.mock import AsyncMock

async def test_publish_calls_backend_with_topic() -> None:
    backend = AsyncMock(spec=Backend)
    storage = Storage(Config(base_url="<unused>"), backend=backend)

    await storage.put("topic", b"x")

    backend.put.assert_awaited_once_with("topic", b"x")
```

`spec=Backend` means:
- Calling a method NOT on Backend raises `AttributeError`. Without `spec=`, `backend.flarbnitz()` would silently return a Mock — typos go undetected.
- Auto-generated methods inherit the signature. `backend.put("topic")` (missing positional) raises `TypeError`. Without `spec=`, the Mock accepts anything.
- mypy accepts `AsyncMock(spec=Backend)` as a `Backend` — type-checker friendly.

`AsyncMock` (3.8+) is the async-aware variant. For sync dependencies, use `MagicMock` (or `Mock`).

`assert_awaited_once_with(...)` (NOT `assert_called_once_with`) — the awaitable variant verifies the method was both CALLED and AWAITED.

For complex specs, `create_autospec(Backend, instance=True)` builds a mock from the live spec and respects nested attributes:

```python
from unittest.mock import create_autospec

backend = create_autospec(Backend, instance=True)
backend.get.return_value = b"value"            # but only for set methods
```

Use `create_autospec` when the Protocol has nested objects; use `AsyncMock(spec=...)` for flat Protocols.

## Rule 4 — HTTP: respx (preferred) or aioresponses

For HTTP-bound code that uses httpx, use `respx`:

```python
import respx
import httpx

@respx.mock
async def test_publish_calls_remote() -> None:
    route = respx.post("https://api.example.com/topics/orders").mock(
        return_value=httpx.Response(204)
    )

    async with Client(Config(base_url="https://api.example.com", api_key="k")) as c:
        await c.publish("orders", b"payload")

    assert route.called
    assert route.call_count == 1
    assert route.calls.last.request.content == b"payload"
```

For aiohttp, use `aioresponses`:

```python
from aioresponses import aioresponses

async def test_publish_aiohttp() -> None:
    with aioresponses() as m:
        m.post("https://api.example.com/topics/orders", status=204)
        async with Client(Config(...)) as c:
            await c.publish("orders", b"x")
```

Both libraries patch the HTTP transport — the Client's actual network code runs (timeouts, retries, header construction), but the wire is mocked. This is the right grain: it tests the SDK's HTTP behavior without booting a real server.

DON'T `monkeypatch.setattr(httpx.AsyncClient, "post", ...)` directly — fragile, breaks on internal refactors of the SDK or httpx.

## Rule 5 — Time: freezegun

```python
from freezegun import freeze_time

@freeze_time("2026-01-01 12:00:00")
async def test_token_expires_after_3600s() -> None:
    cfg = Config(...)
    async with Client(cfg) as c:
        token = await c.fetch_token()        # creation_time = 2026-01-01 12:00:00
        # ... advance time ...
```

For dynamic time advance:

```python
with freeze_time("2026-01-01") as frozen:
    token = await client.fetch_token()
    frozen.tick(delta=timedelta(hours=2))
    assert client.token_is_expired(token)
```

Avoid `monkeypatch.setattr(time, "time", lambda: ...)` — only patches one module's import, misses imports in other modules.

For asyncio's clock specifically (`asyncio.get_event_loop().time()`), freezegun is NOT enough — pytest-asyncio's event loop has its own clock. Use:

```python
async def test_with_async_time(monkeypatch) -> None:
    monkeypatch.setattr(asyncio, "sleep", AsyncMock())
    # Or use anyio.fail_after for deadline-driven tests
```

## Rule 6 — Random / UUID

```python
import uuid

async def test_session_id_format(monkeypatch) -> None:
    fake_uuid = uuid.UUID("12345678-1234-5678-1234-567812345678")
    monkeypatch.setattr(uuid, "uuid4", lambda: fake_uuid)

    sid = make_session_id()
    assert sid == "session-12345678-1234-5678-1234-567812345678"
```

Or for `random.random()`-driven jitter, seed at the `random.Random` instance level:

```python
class Retry:
    def __init__(self, *, rng: random.Random | None = None) -> None:
        self._rng = rng or random.Random()

    def jitter(self) -> float:
        return self._rng.uniform(0, 0.1)
```

Tests inject `Retry(rng=random.Random(seed=42))` for deterministic jitter.

## Rule 7 — Filesystem: pyfakefs OR tmp_path

For tests that read/write files, `tmp_path` (pytest built-in) is usually sufficient:

```python
async def test_loads_config(tmp_path: Path) -> None:
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text('{"base_url": "https://x"}')
    cfg = Config.from_file(cfg_path)
    assert cfg.base_url == "https://x"
```

For tests that test the `open()` call patterns (rare — usually a smell), `pyfakefs` simulates a full in-memory filesystem:

```python
def test_with_fakefs(fs):                    # fs fixture from pyfakefs
    fs.create_file("/etc/motadata/config.json", contents='{"x": 1}')
    cfg = Config.from_default_paths()
    assert cfg.x == 1
```

`pyfakefs` is heavyweight; use `tmp_path` first.

## Rule 8 — `pytest-mock` for `mocker` fixture

```python
async def test_with_mocker(mocker) -> None:
    mock_backend = mocker.AsyncMock(spec=Backend)
    storage = Storage(Config(...), backend=mock_backend)
    # mocker fixture auto-undoes patches at test end
```

`mocker` (from `pytest-mock`) is the pytest-friendly wrapper around `unittest.mock`. It auto-undoes patches at test end (so `monkeypatch.setattr` is rarely needed). Same APIs (`mocker.patch`, `mocker.AsyncMock`, `mocker.create_autospec`).

## Rule 9 — Don't mock the public API

Mocking the SDK's OWN public class means the test is testing the test, not the code:

```python
# WRONG — mocks the very class under test
mocker.patch("motadatapysdk.client.Client", AsyncMock())

# RIGHT — uses the real Client; mocks the seam (Backend) it depends on
async with Client(Config(...), backend=fake_backend) as c:
    await c.publish("topic", b"x")
```

The SDK's public surface IS the contract; patching it bypasses the contract. Mock the COLLABORATORS the public class depends on, not the class itself.

## Rule 10 — `unittest.mock.patch` with import paths — patch where USED

```python
# motadatapysdk/client.py
from time import time
def fetch():
    timestamp = time()                 # imports time INTO this module
    ...

# WRONG patch path
mocker.patch("time.time", lambda: 123)             # doesn't patch the imported reference

# RIGHT patch path
mocker.patch("motadatapysdk.client.time", lambda: 123)
```

Patches replace the symbol at the IMPORT path, not the source. If `client.py` did `from time import time`, the symbol now lives at `motadatapysdk.client.time` — patch THAT path.

This is the most common Mock confusion. Prefer the seam pattern (Rule 1) so you never need import-path patching.

## Rule 11.5 — Strict-signature mocking when wrapping a real library API (added v1.1.0)

**Added in v1.1.0** in response to the `motadata-nats-v1` run's B-series root cause: FakeNats / FakeJs / FakeKVStore / FakeObjectStore substrates accepted `**kwargs` to remain forward-compatible with future nats-py releases. The `**kwargs` pattern silently swallowed the kwarg-shape drift between `nats-py 2.7` (TPRD-cited floor) and `nats-py 2.14` (env-installed actual). Unit tests passing `replicas=N` on a FakeJs StreamConfig PASSed; the same call against real nats-py 2.14 FAILed at integration-test time (T2).

The lesson: when your Fake wraps a class from a real external library and unit tests are intended to also catch kwarg-name typos / kwarg-rename drift, **bind the Fake's accepted signature to the real class's signature via `inspect.signature`**, not via permissive `**kwargs`.

```python
# BAD — overly permissive; hides kwarg-rename drift
class FakeJsStreamConfig:
    def __init__(self, *, name, subjects, **kwargs):  # ← swallows everything
        self.name = name
        self.subjects = subjects
        for k, v in kwargs.items():
            setattr(self, k, v)
```

```python
# GOOD — bind to the real class's signature; fail fast on kwarg drift
import inspect
from nats.js.api import StreamConfig as _RealStreamConfig

_REAL_STREAM_SIG = inspect.signature(_RealStreamConfig)

class FakeJsStreamConfig:
    """In-memory analogue of nats.js.api.StreamConfig.

    Accepts ONLY the kwargs the real class accepts AT THE CURRENT INSTALLED
    nats-py minor. Calling with a kwarg the real class would reject (typo,
    rename, removed) raises TypeError at test time — same failure mode as
    integration tests would, just without spinning up testcontainers.
    """

    def __init__(self, **kwargs: object) -> None:
        bound = _REAL_STREAM_SIG.bind(**kwargs)  # raises TypeError on unknown kwarg
        bound.apply_defaults()
        for k, v in bound.arguments.items():
            setattr(self, k, v)
```

The `inspect.signature(real_class).bind(**caller_kwargs)` call introspects the real class's `__init__` and raises `TypeError` if the caller passes a kwarg the real class doesn't accept. The Fake's behavior remains in-memory (no I/O), but its kwarg-acceptance surface is now coupled to the real library's kwarg-acceptance surface at the installed version. A `pip install -U <lib>` in CI that introduces a kwarg rename will instantly fail unit tests at the affected mock site, the same way integration tests would fail — just without the 10-second testcontainers spin-up cost.

**Caveats**:

- Cost: `inspect.signature` is reflection-heavy if called per test; cache the `Signature` object at module level (`_REAL_STREAM_SIG = inspect.signature(...)`).
- Forward-compat: this BINDS to the installed minor. A test that has to assert behavior under a kwarg the SDK uses but the real lib doesn't expose yet (a TPRD invariant) needs a different strategy — usually a per-version conditional `inspect.signature(real_class).parameters` check + `pytest.skip` on incompatible installs.
- Interaction with `python-dependency-vetting` v1.1.0: dep-vet skill's V-12 check catches kwarg-rename at design time (H6) before the SDK code is ever generated. This Rule 11.5 is the SECOND line of defense — catches at unit test time if dep-vet was bypassed or if the dep was upgraded between dep-vet and the test run.

**When NOT to use strict-signature mocking**:

- The Fake is asserting behavior the real library doesn't even attempt (a TPRD-invariant policy layer like tenant-prefix scoping).
- The Fake is for a Protocol-typed seam where there's no real library class to bind against.
- Unit-test budget is dominated by reflection cost (rarely the case; strongly prefer correctness).

## Rule 11 — Async fixtures that return AsyncMock

```python
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
async def mock_backend() -> AsyncMock:
    backend = AsyncMock(spec=Backend)
    backend.get.return_value = b"default-value"
    return backend


async def test_storage_uses_backend(mock_backend) -> None:
    storage = Storage(Config(...), backend=mock_backend)
    result = await storage.get("k")
    assert result == b"default-value"
```

The fixture is async-friendly because pytest-asyncio's `asyncio_mode = "auto"` (per `python-pytest-patterns` Rule 6). `AsyncMock` is constructed synchronously and used in async tests.

## GOOD: full test file

```python
# tests/test_storage.py
"""Tests for motadatapysdk.storage.Storage."""
import pytest
import respx
import httpx
from motadatapysdk.storage import Storage
from motadatapysdk import Config
from tests.fakes import FakeBackend


# --- Behavior tests via Fake (preferred) ---

async def test_put_then_get_roundtrip() -> None:
    fake = FakeBackend()
    storage = Storage(Config(base_url="<unused>", api_key="k"), backend=fake)

    await storage.put("user:1", b"alice")
    result = await storage.get("user:1")

    assert result == b"alice"
    assert fake.items == {"user:1": b"alice"}


async def test_get_missing_returns_none() -> None:
    fake = FakeBackend()
    storage = Storage(Config(base_url="<unused>", api_key="k"), backend=fake)

    result = await storage.get("missing")

    assert result is None


# --- Call-pattern test via AsyncMock(spec=) (when needed) ---

async def test_put_calls_backend_put_exactly_once(mocker) -> None:
    backend = mocker.AsyncMock(spec=Backend)
    storage = Storage(Config(base_url="<unused>", api_key="k"), backend=backend)

    await storage.put("k", b"v")

    backend.put.assert_awaited_once_with("k", b"v")
    backend.get.assert_not_called()


# --- HTTP test via respx (when testing the production HTTP path) ---

@respx.mock
async def test_http_backend_puts_to_correct_url() -> None:
    route = respx.put("https://api.example.com/keys/k").mock(
        return_value=httpx.Response(204)
    )
    async with Storage(Config(base_url="https://api.example.com", api_key="k")) as storage:
        await storage.put("k", b"v")

    assert route.called
    assert route.calls.last.request.content == b"v"
    assert route.calls.last.request.headers["authorization"] == "Bearer k"
```

The file demonstrates: behavior-first via Fake (preferred), call-pattern via Mock (when needed), HTTP-path via respx (production behavior with mocked wire). Three different grains for three different test goals.

## BAD anti-patterns

```python
# 1. Bare Mock without spec
mock = Mock()                               # accepts any attribute, any call
mock.flarbnitz_with_no_typo_check()         # passes; bug undetected

# 2. Mocking the class under test
mocker.patch("motadatapysdk.client.Client", AsyncMock())
async with Client(Config(...)) as c:        # never actually runs Client code

# 3. monkeypatch internal helper
monkeypatch.setattr("motadatapysdk.client._build_request", AsyncMock())
# Brittle to refactor; couples to internal symbol path

# 4. Asserting on call ORDER for a behavior test
mock.put.assert_called_once_with("k", b"v")
mock.get.assert_called_once_with("k")
mock.put.assert_called_once_with(...)        # Order assertions break on legit refactor

# 5. side_effect = list of values
mock.get.side_effect = [b"a", b"b", b"c"]    # IndexError on 4th call

# 6. Patching at the wrong import path
mocker.patch("time.time", ...)               # didn't actually patch where used

# 7. AsyncMock without spec on async dep
backend = AsyncMock()                         # silently accepts any method
backend.put_typoed("k", b"v")                # bug invisible

# 8. Real HTTP in unit test
async with httpx.AsyncClient() as c:
    await c.get("https://api.example.com/...")  # actual network; flaky

# 9. Mock in fixture, return Mock in production seam
@pytest.fixture
def backend(): return Mock()                  # Production code expects a Backend; Mock isn't typed

# 10. assert_called_with on async method
backend.put.assert_called_with("k", b"v")    # for AsyncMock, use assert_awaited_with
```

## When NOT to mock at all

- **Pure functions** — call them directly with inputs. `parse_topic("a.b") == ("a", "b")` doesn't need any mock.
- **Stdlib types** (dict, list, dataclass) — don't mock; use real instances.
- **The class under test** — use real Client + mocked dependencies.
- **Reading test fixtures from disk** — `tmp_path` is fine; pyfakefs is overkill.

## Tooling configuration

Add dev dependencies:

```toml
[project.optional-dependencies]
test = [
    "pytest >= 8.0",
    "pytest-asyncio >= 0.23",
    "pytest-mock >= 3.12",
    "respx >= 0.21",                 # if using httpx
    "aioresponses >= 0.7",           # if using aiohttp
    "freezegun >= 1.4",              # if testing time
    "pyfakefs >= 5.3",               # if testing filesystem heavily
]
```

`pytest-mock` is the only one that's nearly universal; the others are situational. Don't pull all of them by default — `sdk-dep-vet-devil-python` will scrutinize each.

## Cross-references

- `python-pytest-patterns` Rule 14 — fakes vs mocks decision; Rule 11 — indirect fixture parametrization.
- `python-mypy-strict-typing` Rule 5 — Protocol over ABC for fakeable seams.
- `python-asyncio-patterns` — `AsyncMock` for async deps.
- `python-sdk-config-pattern` — Config injection through constructor.
- `python-client-shutdown-lifecycle` — fakes implement `__aenter__`/`__aexit__` if used as async context managers.
- `sdk-convention-devil-python` C-14 — design-rule enforcement at D3.
