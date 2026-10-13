---
name: python-hexagonal-architecture
description: >
  Use this when laying out a Python SDK with non-trivial domain logic, when
  multiple adapter implementations (HTTP + gRPC, prod + in-memory) are
  anticipated, when domain tests are slow because they boot real adapters, or
  when reviewing whether a future backend swap is feasible. Covers the
  src/<pkg>/{domain,ports,adapters,application}/ layout with a client.py
  composition root, the inner-only-imports dependency rule, pure
  frozen-dataclass domain entities + pure-function policies, Protocol (with
  optional @runtime_checkable) over ABC for ports, constructor-injected
  adapters that wrap external libraries, per-layer test strategy (unit / use
  case with fakes / integration), __all__ hygiene, import-linter layered
  contracts, and when a thin single-file SDK is the right call instead.
  Triggers: hexagonal, ports, adapters, domain, application, Protocol, dependency injection, ports and adapters, clean architecture.
---

# python-hexagonal-architecture (v1.0.0)

## Rationale

Hexagonal architecture (Cockburn 2005, also "ports and adapters") draws three concentric layers: a pure DOMAIN inside, a thin APPLICATION layer that orchestrates use cases, and ADAPTERS at the edge that translate between the application's PORTS (interfaces) and the outside world (HTTP, database, message queue, filesystem). The Python pack uses this layout for SDKs that have non-trivial domain logic — anything beyond a thin pass-through to a remote service.

The payoffs:
- Domain code is pure (no I/O, no `async`); tests run fast and cover the actual logic.
- Adapters are swappable (HTTP today, gRPC tomorrow) without touching domain or application.
- Ports are Python `Protocol`s, structurally typed, fakeable for tests.
- mypy `--strict` enforces the layering at type-check time.

This skill is cited by `python-mock-strategy` (Protocol = port = test seam), `python-mypy-strict-typing` (Protocol over ABC), `python-sdk-config-pattern` (Config wires the adapters), `python-asyncio-patterns` (async lives at adapter edge), `code-reviewer-python` (architecture review-criteria), `sdk-design-devil` (design quality).

## When to use it

Hexagonal pays off when:
- The SDK has DOMAIN logic — validation, retry decisions, state machines, business rules.
- Multiple adapter implementations exist — sync + async, HTTP + gRPC, prod + in-memory test.
- The team will swap dependencies over time.

It does NOT pay off when:
- The SDK is a thin client (auth header + serialize + HTTP POST). One module is enough.
- The team is small and the SDK is single-purpose. Don't pre-plan abstraction.

If unsure: skip hexagonal at v0.1.0; refactor toward it at v0.3.0+ when the layers naturally emerge.

## Activation signals

- TPRD §3 declares non-trivial domain logic (validation, scheduling, retry semantics).
- Two adapter implementations are anticipated (e.g., HTTP and gRPC for the same service).
- Domain tests are slow because they boot real adapters.
- Code review surfaces I/O calls scattered across what should be pure logic.
- Reviewing whether a future "swap the backend" change is feasible.

## Layout

```
src/motadatapysdk/
├── __init__.py                 # public API re-exports (User-facing)
├── py.typed
│
├── domain/                     # PURE — no I/O, no async, no third-party deps
│   ├── __init__.py
│   ├── models.py               # frozen @dataclass entities + value objects
│   ├── events.py               # domain events
│   └── policies.py             # pure functions: retry decisions, validation
│
├── ports/                      # CONTRACTS — Protocol classes
│   ├── __init__.py
│   ├── repository.py           # Repository protocol (storage backend)
│   ├── publisher.py            # Publisher protocol (message bus)
│   └── credentials.py          # CredentialProvider protocol
│
├── application/                # USE CASES — orchestrates domain + ports
│   ├── __init__.py
│   ├── publish_use_case.py     # PublishUseCase: validates, calls port
│   └── fetch_use_case.py
│
├── adapters/                   # EDGES — concrete implementations of ports
│   ├── __init__.py
│   ├── http/
│   │   ├── __init__.py
│   │   ├── publisher.py        # HttpPublisher implements Publisher protocol
│   │   └── repository.py
│   ├── grpc/                   # alternative adapter (if needed)
│   │   └── publisher.py
│   ├── memory/                 # in-memory adapter for tests + unit demos
│   │   ├── publisher.py
│   │   └── repository.py
│   └── env_credentials.py      # CredentialProvider impl
│
├── client.py                   # COMPOSITION ROOT — wires everything per Config
└── errors.py                   # exception hierarchy (depended on by everything)
```

The dependency rule is: outer layers depend on inner; inner never depends on outer.

```
client.py (composition) → application/ → ports/ ← domain/
                          adapters/    ↗ (implements)
```

`domain/` imports nothing from `application/`, `ports/`, `adapters/`, or `client.py`. `ports/` imports from `domain/` only. `application/` imports from `domain/` and `ports/` but NEVER from `adapters/`. `adapters/` imports from `domain/` (for entity types) and `ports/` (the Protocol they implement) but NEVER from `application/`.

## Rule 1 — Domain is pure

```python
# src/motadatapysdk/domain/models.py
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class Topic:
    """A validated topic identifier."""
    namespace: str
    name: str

    def __post_init__(self) -> None:
        if not self.namespace or not self.name:
            raise ValueError("namespace and name must both be non-empty")
        if "." in self.namespace or "." in self.name:
            raise ValueError("namespace and name must not contain '.'")

    @property
    def qualified(self) -> str:
        return f"{self.namespace}.{self.name}"

    @classmethod
    def parse(cls, raw: str) -> "Topic":
        ns, _, name = raw.partition(".")
        return cls(namespace=ns, name=name)


@dataclass(frozen=True, slots=True, kw_only=True)
class Message:
    topic: Topic
    payload: bytes
```

```python
# src/motadatapysdk/domain/policies.py
from .models import Message


def is_retriable_failure(error_code: int) -> bool:
    """Pure decision: should this server response code be retried?"""
    return error_code in (429, 500, 502, 503, 504)


def estimate_backoff_seconds(*, attempt: int, base: float = 0.1) -> float:
    """Pure: exponential backoff with cap at 30 seconds."""
    return min(30.0, base * (2 ** attempt))
```

These modules import nothing async, nothing I/O, nothing third-party. They run at thousands of tests per second.

## Rule 2 — Ports are Protocols

```python
# src/motadatapysdk/ports/publisher.py
from typing import Protocol

from motadatapysdk.domain.models import Message


class Publisher(Protocol):
    """The seam the application calls; adapters implement.

    Implementations must accept a domain Message and return None on success
    or raise a domain exception on failure.
    """

    async def publish(self, message: Message) -> None: ...
```

Protocol — not ABC. Structural typing means an adapter doesn't import the Protocol; it just has the right method shape. Tests can fake without inheritance:

```python
# Test fake — implements Publisher structurally; no inheritance
class InMemoryPublisher:
    def __init__(self) -> None:
        self.published: list[Message] = []

    async def publish(self, message: Message) -> None:
        self.published.append(message)
```

mypy `--strict` accepts `InMemoryPublisher` as `Publisher` because the method shapes match.

For ports the SDK consumer might subclass (rare; usually they fake), mark `@runtime_checkable`:

```python
@runtime_checkable
class Publisher(Protocol):
    async def publish(self, message: Message) -> None: ...
```

`runtime_checkable` enables `isinstance(x, Publisher)` — useful for SDK code that wants to verify a passed-in adapter satisfies the contract at construction.

## Rule 3 — Application layer is async, but minimal

```python
# src/motadatapysdk/application/publish_use_case.py
from __future__ import annotations

import logging

from motadatapysdk.domain.models import Message, Topic
from motadatapysdk.domain.policies import estimate_backoff_seconds, is_retriable_failure
from motadatapysdk.errors import NetworkError, ValidationError
from motadatapysdk.ports.publisher import Publisher

logger = logging.getLogger(__name__)


class PublishUseCase:
    """Orchestrates: parse → validate → call port → handle retriable errors.

    Constructor takes a Publisher (port). The application code does NOT
    know whether the Publisher is HTTP, gRPC, or in-memory.
    """

    def __init__(self, publisher: Publisher, *, max_retries: int = 3) -> None:
        self._publisher = publisher
        self._max_retries = max_retries

    async def execute(self, *, raw_topic: str, payload: bytes) -> None:
        try:
            topic = Topic.parse(raw_topic)            # domain validation
        except ValueError as e:
            raise ValidationError(str(e)) from e

        message = Message(topic=topic, payload=payload)
        for attempt in range(self._max_retries + 1):
            try:
                await self._publisher.publish(message)
                return
            except NetworkError as e:
                if attempt >= self._max_retries:
                    raise
                logger.info("publish retry %d", attempt + 1, exc_info=e)
                await asyncio.sleep(estimate_backoff_seconds(attempt=attempt))
```

The use case is async (it awaits the port). It does NOT import aiohttp / asyncpg / redis / OTel. Those live in adapters.

## Rule 4 — Adapters wrap external libraries

```python
# src/motadatapysdk/adapters/http/publisher.py
from __future__ import annotations

import httpx

from motadatapysdk.domain.models import Message
from motadatapysdk.errors import NetworkError, ServerError


class HttpPublisher:
    """HTTP adapter implementing the Publisher port via httpx.

    The adapter knows about HTTP status codes, headers, retries from the
    transport layer; it does NOT know about domain validation or use-case
    orchestration.
    """

    def __init__(self, http: httpx.AsyncClient, *, base_url: str) -> None:
        self._http = http
        self._base_url = base_url.rstrip("/")

    async def publish(self, message: Message) -> None:
        url = f"{self._base_url}/topics/{message.topic.qualified}"
        try:
            response = await self._http.post(url, content=message.payload)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if 500 <= e.response.status_code < 600:
                raise ServerError(
                    f"server error {e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e
            raise
        except httpx.HTTPError as e:
            raise NetworkError(f"HTTP error: {e}") from e
```

The adapter is the ONLY place that imports `httpx`. If a future version swaps to `aiohttp` or `grpcio`, only this file changes.

## Rule 5 — Composition root wires everything

```python
# src/motadatapysdk/client.py
from __future__ import annotations

from typing import Self

import httpx

from motadatapysdk.adapters.http.publisher import HttpPublisher
from motadatapysdk.application.publish_use_case import PublishUseCase
from motadatapysdk.config import Config


class Client:
    """Top-level SDK client.

    Constructs adapters from Config, wires them into use cases, exposes
    the user-facing API.

    Examples:
        >>> async def demo() -> None:
        ...     async with Client(Config(base_url="https://x", api_key="k")) as client:
        ...         await client.publish("orders.created", b"x")
        >>> asyncio.run(demo())  # doctest: +SKIP
    """

    def __init__(self, config: Config) -> None:
        self._config = config
        self._http: httpx.AsyncClient | None = None
        self._publish_use_case: PublishUseCase | None = None

    async def __aenter__(self) -> Self:
        self._http = httpx.AsyncClient(
            base_url=self._config.base_url,
            timeout=self._config.timeout_s,
        )
        publisher = HttpPublisher(self._http, base_url=self._config.base_url)
        self._publish_use_case = PublishUseCase(
            publisher, max_retries=self._config.max_retries,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, tb) -> None:
        if self._http is not None:
            await self._http.aclose()
            self._http = None

    async def publish(self, topic: str, payload: bytes) -> None:
        """Publish ``payload`` to ``topic``.

        Args:
            topic: Topic in ``namespace.name`` form.
            payload: Bytes to publish.

        Raises:
            ValidationError: If the topic is malformed.
            NetworkError: On wire failure.
        """
        if self._publish_use_case is None:
            raise RuntimeError("client not entered")
        await self._publish_use_case.execute(raw_topic=topic, payload=payload)
```

The Client is the ONE place that knows the full wiring. Switching adapters means changing the Client; the use case and domain are untouched.

## Rule 6 — Test each layer independently

```python
# tests/unit/test_domain_topic.py
import pytest
from motadatapysdk.domain.models import Topic


@pytest.mark.parametrize("ns,name", [("ord", ""), ("", "x"), ("a.b", "x"), ("a", "b.c")])
def test_topic_invalid(ns, name) -> None:
    with pytest.raises(ValueError):
        Topic(namespace=ns, name=name)


def test_topic_qualified() -> None:
    assert Topic(namespace="orders", name="created").qualified == "orders.created"
```

Domain tests run in microseconds — no I/O, no async, no fixtures.

```python
# tests/unit/test_publish_use_case.py
import pytest
from motadatapysdk.application.publish_use_case import PublishUseCase
from motadatapysdk.errors import NetworkError, ValidationError
from tests.fakes import InMemoryPublisher


async def test_publish_invalid_topic_raises() -> None:
    fake = InMemoryPublisher()
    use_case = PublishUseCase(fake)
    with pytest.raises(ValidationError):
        await use_case.execute(raw_topic="no-dot", payload=b"x")
    assert fake.published == []                      # never reached the port


async def test_publish_retries_on_network_error() -> None:
    fake = FlakyPublisher(fail_first_n=2)
    use_case = PublishUseCase(fake, max_retries=3)
    await use_case.execute(raw_topic="orders.created", payload=b"x")
    assert fake.publish_calls == 3                   # retried twice, succeeded on 3rd
```

Use case tests use FakePublisher (an in-memory Publisher) — no httpx, no testcontainers, no Docker.

```python
# tests/integration/test_http_publisher.py
import httpx
import pytest
from motadatapysdk.adapters.http.publisher import HttpPublisher
from motadatapysdk.domain.models import Message, Topic

pytestmark = pytest.mark.integration


async def test_http_publisher_sends_payload(http_test_server) -> None:
    async with httpx.AsyncClient(base_url=http_test_server.url) as http:
        publisher = HttpPublisher(http, base_url=http_test_server.url)
        await publisher.publish(Message(
            topic=Topic(namespace="orders", name="created"),
            payload=b"x",
        ))
    assert http_test_server.received == [(b"/topics/orders.created", b"x")]
```

Adapter tests run against real HTTP (testcontainer or local mock server). Slowest layer; smallest surface.

## Rule 7 — `__init__.py` re-exports the user surface

```python
# src/motadatapysdk/__init__.py
"""Public API for the motadata SDK."""
from motadatapysdk.client import Client
from motadatapysdk.config import Config
from motadatapysdk.errors import (
    AuthError,
    MotadataError,
    NetworkError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from motadatapysdk.domain.models import Message, Topic

__all__ = [
    "Client",
    "Config",
    "Message",
    "Topic",
    "MotadataError",
    "AuthError",
    "NetworkError",
    "RateLimitError",
    "ServerError",
    "ValidationError",
]
```

`ports/`, `application/`, `adapters/` are NOT re-exported — they're internal architecture, not part of the public API. Consumers see only what they need to use the SDK.

`__all__` is mandatory (per `python-mypy-strict-typing` Rule 7). External tooling (sphinx, IDE autocomplete, `from motadatapysdk import *`) honors it.

## Rule 8 — Guard the layering with mypy / linting

`pyproject.toml`:

```toml
[tool.mypy]
strict = true

# Domain must not import from application / adapters / client
[[tool.mypy.overrides]]
module = "motadatapysdk.domain.*"
disallow_any_explicit = true

# import-linter for layered enforcement (advisory)
[tool.importlinter]
root_packages = ["motadatapysdk"]

[[tool.importlinter.contracts]]
name = "Hexagonal layering"
type = "layers"
layers = [
    "motadatapysdk.client",
    "motadatapysdk.application",
    "motadatapysdk.ports",
    "motadatapysdk.adapters",
    "motadatapysdk.domain",
]
```

`import-linter` (third-party) catches cross-layer imports as part of CI. Cheap insurance against drift.

## Rule 9 — When to skip hexagonal — thin SDK is fine

A thin client SDK like:

```python
# motadatapysdk/__init__.py — single-file SDK
class Client:
    async def publish(self, topic: str, payload: bytes) -> None:
        async with httpx.AsyncClient(timeout=self._timeout) as http:
            await http.post(f"{self._base_url}/topics/{topic}", content=payload)
```

…is fine. Don't impose three layers on 30 lines of code. Hexagonal earns its keep when the SDK has 500+ lines of domain logic and/or anticipated adapter swaps.

The decision: when the file count for the single-module SDK approaches double digits OR when a second adapter is on the roadmap, refactor toward hexagonal. Until then, ship simple.

## GOOD: minimal complete hexagonal SDK

```
src/motadatapysdk/
├── __init__.py
├── client.py
├── config.py
├── errors.py
├── domain/
│   ├── __init__.py
│   └── models.py           # Topic, Message
├── ports/
│   ├── __init__.py
│   └── publisher.py        # Publisher Protocol
├── application/
│   ├── __init__.py
│   └── publish_use_case.py
└── adapters/
    ├── __init__.py
    └── http/
        ├── __init__.py
        └── publisher.py     # HttpPublisher
```

10 files. Layered. mypy --strict clean. Tests:

```
tests/
├── unit/
│   ├── test_domain_topic.py        # 5 ms total
│   └── test_publish_use_case.py    # 50 ms total (uses FakePublisher)
└── integration/
    └── test_http_publisher.py       # 2 s total (real HTTP server)
```

## BAD anti-patterns

```python
# 1. Domain imports adapter
# domain/policies.py
import httpx                                    # domain is no longer pure

# 2. Application imports adapter
# application/publish_use_case.py
from motadatapysdk.adapters.http.publisher import HttpPublisher
# now use case can't be tested without httpx

# 3. Adapter imports use case
# adapters/http/publisher.py
from motadatapysdk.application.publish_use_case import PublishUseCase
# circular dependency; layer violation

# 4. Pure domain function with side effects
# domain/policies.py
def estimate_backoff_seconds(...):
    logger.info("computing backoff")           # side effect; not pure

# 5. ABC port instead of Protocol
class Publisher(ABC):
    @abstractmethod
    async def publish(self, message): ...      # forces inheritance; less testable

# 6. Adapter knows about Config
class HttpPublisher:
    def __init__(self, config: Config) -> None:   # adapter shouldn't know whole Config
        ...                                        # pass narrow params instead

# 7. No __all__ in top-level __init__
# users see ports, adapters, application — internals leak

# 8. application/ depends on a concrete adapter type
async def publish(self, msg, *, publisher: HttpPublisher) -> None:
    ...                                          # use case is now bound to HTTP

# 9. Domain entity is mutable
@dataclass
class Message:
    topic: str
    payload: bytes              # not frozen — mutation breaks invariants

# 10. Composition logic scattered across modules
# Each module instantiates its own httpx.AsyncClient
# instead of one place wiring everything
```

## Cross-references

- `python-mock-strategy` Rule 1 — Protocol port = test seam.
- `python-mypy-strict-typing` Rules 5 (Protocol over ABC) + 7 (__all__).
- `python-sdk-config-pattern` — Config consumed at composition root.
- `python-pytest-patterns` — unit tests at domain + use-case layers; integration at adapter layer.
- `python-asyncio-patterns` — async lives at adapter edge.
- `python-exception-patterns` — domain raises typed errors that adapters wrap further.
- `python-client-shutdown-lifecycle` — Client (composition root) owns all close paths.
- `spec-driven-development` (shared) — story-to-symbol mapping aligns with use cases.
