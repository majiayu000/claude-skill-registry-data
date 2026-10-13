---
name: python-circuit-breaker-policy
description: >
  Use this when wrapping a Python SDK client around an external dependency that
  can go down, adding a backstop to a retry loop, designing fail-fast behavior
  for sustained downstream outage, or reviewing whether breaker scope and
  thresholds are right. Covers purgatory (default) / aiocircuitbreaker library
  choice, closed/open/half-open transitions, per-endpoint factory-cached
  breakers, ValidationError exclusion, CircuitOpenError wrap of OpenedState,
  retry pairing that doesn't retry an open circuit, OTel state-transition hooks,
  and Config-driven thresholds.
  Triggers: circuit, breaker, purgatory, aiocircuitbreaker, pybreaker, open state, half-open, failure_threshold, recovery_timeout, OpenedState, CircuitOpenError.
---

# python-circuit-breaker-policy (v1.0.0)

## Rationale

Retries amplify downstream pain. When the dependency is genuinely down, retrying makes things worse. A circuit breaker fails fast: after N consecutive failures, the breaker OPENS and rejects calls immediately for a cooldown window. After cooldown, ONE probe call decides whether to close (resume traffic) or stay open. The SDK gives consumers the breaker as a wrapper around the client method; the consumer chooses the thresholds.

This skill is cited by `code-reviewer-python` (resilience review-criteria), `python-asyncio-patterns` (cancellation safety), `idempotent-retry-safety` (retry pairs with breaker), `python-otel-instrumentation` (state-transition spans), and `sdk-api-ergonomics-devil-python` (E-4 exception design).

## Activation signals

- SDK client wraps an external dependency that may go down.
- Production incident: client retried itself into amplification under outage.
- TPRD §3 declares a downstream availability concern.
- Reviewing retry logic — does it have a backstop?

## Library choice

Three viable Python libraries (in preference order):

| Library | License | Async | Maintenance | Recommendation |
|---------|---------|-------|-------------|----------------|
| `purgatory` | MIT | Yes (3.10+) | Active | DEFAULT for new code |
| `aiocircuitbreaker` | Apache-2.0 | Yes | Active | Acceptable if `purgatory` rejected |
| `pybreaker` | BSD-3 | Sync only (3.x) | Active | Fall back ONLY for sync code |

`purgatory` is the Python pack default: typed, async-native, simple decorator + context-manager API, tiny dependency footprint. Always vet before adoption per `python-dependency-vetting`.

## Core states

```
CLOSED   →  every call passes through; failures counted
   ↓ (failure_threshold reached)
OPEN     →  every call REJECTED with OpenError; no downstream load
   ↓ (recovery_timeout elapsed)
HALF-OPEN →  ONE probe call allowed; result decides next state
   ↓ probe success           ↓ probe failure
CLOSED                        OPEN (reset cooldown)
```

The breaker is a state machine attached to a SCOPE (typically an endpoint or service). One breaker per scope — global breakers hide which dependency is failing.

## Configuration policy

```python
from purgatory import AsyncCircuitBreakerFactory
from purgatory.domain.model import CircuitBreaker

breaker_factory = AsyncCircuitBreakerFactory()

# Per-endpoint breaker
publish_breaker = await breaker_factory.get_breaker(
    name="motadata.publish",
    threshold=5,                  # failures before opening
    ttl=30.0,                     # seconds in OPEN before half-open probe
)
```

Defaults (Python pack convention):
- `threshold=5` — open after 5 consecutive failures.
- `ttl=30s` — recovery window. Tune per endpoint: 30s for fast services, 5–10 minutes for slow / batch.
- ONE breaker per logical endpoint (`publish`, `fetch`, `delete`). Don't pool across endpoints — different failure modes deserve different breakers.

## Rule 1 — Decorator vs context manager

Decorator form (preferred for whole-method protection):

```python
import logging
from purgatory import AsyncCircuitBreakerFactory

logger = logging.getLogger(__name__)
breaker_factory = AsyncCircuitBreakerFactory()


class Client:
    async def publish(self, topic: str, payload: bytes) -> None:
        async with await breaker_factory.get_breaker(
            "motadata.publish", threshold=5, ttl=30.0
        ):
            await self._http.post(self._url(topic), data=payload)
```

Context-manager form is the canonical pattern for `purgatory` — it scopes the protection to ONE await block. The breaker increments a failure count if the block raises; resets if it returns cleanly.

## Rule 2 — Failure types — only network errors count

Not every exception is a circuit-breaker signal. A `ValidationError` is the caller's fault, not the downstream's. A breaker that opens on validation errors silently blocks legitimate traffic.

```python
from motadatapysdk.errors import NetworkError, ServerError, TimeoutError as SDKTimeoutError

async def publish(self, topic: str, payload: bytes) -> None:
    try:
        async with await breaker_factory.get_breaker(...):
            await self._http.post(...)
    except (NetworkError, ServerError, SDKTimeoutError):
        # These count as breaker failures
        raise
    except ValidationError:
        # Caller error — NOT a breaker signal; re-raise without breaker reset
        raise
```

Most circuit-breaker libraries (purgatory included) accept an `excluded_exceptions=` parameter to whitelist non-failure types:

```python
breaker = await breaker_factory.get_breaker(
    "motadata.publish",
    threshold=5,
    ttl=30.0,
    excluded_exceptions=(ValidationError,),     # don't count these as failures
)
```

## Rule 3 — OpenError surfaces clearly

When the breaker is open, calls raise `purgatory.OpenedState`:

```python
from purgatory.domain.model import OpenedState
from motadatapysdk.errors import CircuitOpenError

async def publish(self, topic: str, payload: bytes) -> None:
    try:
        async with await breaker_factory.get_breaker(...):
            await self._http.post(...)
    except OpenedState as e:
        raise CircuitOpenError(
            f"motadata.publish circuit is open; downstream is unavailable",
        ) from e
```

Wrap the library exception in the SDK's typed exception (`CircuitOpenError`) so consumers catch it via the `MotadataError` base. The library exception is an implementation detail.

`CircuitOpenError` is a subclass of `MotadataError` — define it in `<pkg>/errors.py`:

```python
class CircuitOpenError(MotadataError):
    """The circuit breaker for an endpoint is open; downstream is unavailable."""
```

## Rule 4 — Pair with retry — but bounded

```python
import asyncio
import random


async def publish_with_retry(
    self, topic: str, payload: bytes, *, max_retries: int = 3
) -> None:
    last_exc: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            async with await breaker_factory.get_breaker(
                "motadata.publish", threshold=5, ttl=30.0
            ):
                await self._http.post(self._url(topic), data=payload)
            return
        except CircuitOpenError:
            # Breaker is open — STOP RETRYING. Bubble up so the consumer knows.
            raise
        except (NetworkError, SDKTimeoutError) as e:
            last_exc = e
            if attempt < max_retries:
                delay = (2 ** attempt) * 0.1 + random.uniform(0, 0.05)
                await asyncio.sleep(delay)
                continue
            raise
    raise last_exc                              # mypy
```

Note the `except CircuitOpenError: raise` — when the circuit is open, retrying inside the same function is the failure mode the breaker is designed to prevent. Bubble up immediately.

For full retry policy (jitter, idempotency safety, retry-after), see `idempotent-retry-safety` (shared skill).

## Rule 5 — Observe state transitions

Every breaker state change is operationally interesting. Hook them to OTel (per `python-otel-instrumentation`):

```python
from opentelemetry import metrics, trace

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

breaker_state_changes = meter.create_counter(
    "motadata.circuit_breaker.state_change",
    description="Breaker state transitions",
)


# purgatory exposes a Hook protocol
class OTelHook:
    async def on_state_change(self, breaker_name: str, old_state: str, new_state: str) -> None:
        breaker_state_changes.add(
            1, {"breaker": breaker_name, "from": old_state, "to": new_state},
        )
        with tracer.start_as_current_span("motadata.breaker.state_change") as span:
            span.set_attribute("circuit_breaker.name", breaker_name)
            span.set_attribute("circuit_breaker.from", old_state)
            span.set_attribute("circuit_breaker.to", new_state)
```

Wire the hook into the factory:

```python
breaker_factory = AsyncCircuitBreakerFactory(hooks=[OTelHook()])
```

Operators see the state transitions in their OTel backend; sustained OPEN states surface as alerts.

## Rule 6 — Per-endpoint, NOT per-method-call

```python
# WRONG — new breaker per call; state never accumulates
async def publish(self, topic: str, payload: bytes) -> None:
    breaker = AsyncCircuitBreakerFactory().get_breaker(...)   # leaks state
    async with await breaker:
        ...

# RIGHT — breaker is instance-level (or factory-level)
class Client:
    def __init__(self, config: Config) -> None:
        self._breaker_factory = AsyncCircuitBreakerFactory()

    async def publish(self, topic: str, payload: bytes) -> None:
        async with await self._breaker_factory.get_breaker(
            "motadata.publish", threshold=5, ttl=30.0
        ):
            ...
```

Factories are shared across calls. The factory caches breakers by name — repeated `get_breaker("motadata.publish", ...)` returns the SAME breaker. State accumulates.

## Rule 7 — One breaker per logical endpoint

```python
# WRONG — coarse-grained
breaker = factory.get_breaker("motadata", threshold=5, ttl=30.0)
# publish failures + fetch failures + delete failures → all reset the same counter

# RIGHT — per-method
publish_breaker = factory.get_breaker("motadata.publish", threshold=5, ttl=30.0)
fetch_breaker = factory.get_breaker("motadata.fetch", threshold=5, ttl=10.0)
```

Per-method breakers let one endpoint fail without blocking others. Different endpoints deserve different `ttl` (fetch is fast; recovery is fast — 10s; publish is slow — 30s).

## Rule 8 — When NOT to use a circuit breaker

- **Cache lookups** — failure is cheap (cache miss); retry is cheap (re-fetch). Not worth the breaker overhead.
- **One-shot operations** in CLI tools — there's no sustained load to amplify.
- **Idempotent-but-rare operations** like a config refresh that runs once an hour — a breaker adds machinery for a single call.
- **Non-network code** — a CPU-bound hot path doesn't have a "downstream" to circuit.

The breaker pays off when the SDK is in a tight loop calling a remote endpoint. Most SDK clients fit; some don't.

## Rule 9 — Configuration policy in Config

Expose the breaker thresholds as Config fields so consumers tune them:

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    base_url: str
    api_key: str
    breaker_failure_threshold: int = 5
    breaker_recovery_seconds: float = 30.0
    breaker_excluded_exceptions: tuple[type[Exception], ...] = (ValidationError,)
```

The Client uses these values at breaker construction:

```python
async def publish(self, topic: str, payload: bytes) -> None:
    breaker = await self._breaker_factory.get_breaker(
        "motadata.publish",
        threshold=self._config.breaker_failure_threshold,
        ttl=self._config.breaker_recovery_seconds,
    )
    async with breaker:
        ...
```

Breaker `breaker_failure_threshold = 0` should DISABLE the breaker (some consumers want it off for testing). Implement as:

```python
if self._config.breaker_failure_threshold == 0:
    await self._http.post(...)
else:
    async with breaker:
        await self._http.post(...)
```

## GOOD: full client method with breaker + retry + OTel

```python
import asyncio
import random
import logging

from opentelemetry import metrics, trace
from purgatory import AsyncCircuitBreakerFactory
from purgatory.domain.model import OpenedState

from motadatapysdk.errors import (
    CircuitOpenError, MotadataError, NetworkError, ServerError, TimeoutError as SDKTimeoutError,
    ValidationError,
)

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)
publish_attempts = meter.create_counter(
    "motadata.publish.attempts",
    description="Publish attempt count by outcome",
)


class Client:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._breaker_factory = AsyncCircuitBreakerFactory()

    async def publish(self, topic: str, payload: bytes) -> None:
        """Publish ``payload`` to ``topic``.

        Raises:
            ValidationError: If ``topic`` is empty.
            CircuitOpenError: If the publish endpoint's circuit is open.
            NetworkError: On wire failure after exhausting retries.
        """
        if not topic:
            raise ValidationError("topic must not be empty")

        breaker = await self._breaker_factory.get_breaker(
            "motadata.publish",
            threshold=self._config.breaker_failure_threshold,
            ttl=self._config.breaker_recovery_seconds,
            excluded_exceptions=(ValidationError,),
        )

        max_retries = self._config.max_retries
        for attempt in range(max_retries + 1):
            try:
                async with breaker, tracer.start_as_current_span("motadata.client.publish") as span:
                    span.set_attribute("messaging.destination.name", topic)
                    span.set_attribute("attempt", attempt)
                    await self._do_publish(topic, payload)
                publish_attempts.add(1, {"outcome": "success"})
                return
            except OpenedState as e:
                publish_attempts.add(1, {"outcome": "circuit_open"})
                raise CircuitOpenError(
                    "motadata.publish circuit is open; downstream is unavailable"
                ) from e
            except (NetworkError, ServerError, SDKTimeoutError):
                publish_attempts.add(1, {"outcome": "retry"})
                if attempt >= max_retries:
                    raise
                delay = min(2 ** attempt, 30) * 0.1 + random.uniform(0, 0.05)
                logger.info("publish retry %d after %.2fs", attempt + 1, delay)
                await asyncio.sleep(delay)
```

Demonstrated: per-endpoint breaker (Rule 7), excluded ValidationError (Rule 2), CircuitOpenError wrap (Rule 3), retry pairs with breaker (Rule 4), OTel observation (Rule 5), Config-driven thresholds (Rule 9), bounded retries.

## BAD anti-patterns

```python
# 1. New breaker per call
async def publish(self, topic):
    factory = AsyncCircuitBreakerFactory()
    breaker = await factory.get_breaker("...")    # state never accumulates

# 2. Coarse breaker scope
factory.get_breaker("everything", ...)            # one failing endpoint blocks all

# 3. Counting validation errors as breaker failures
async with breaker:
    if not topic:
        raise ValidationError("...")              # opens breaker for caller's bug

# 4. Retry loop that ignores OpenedState
for _ in range(retries):
    try:
        async with breaker: ...
    except Exception:                              # OpenedState retried = amplification
        await asyncio.sleep(1)
        continue

# 5. Library exception leaks past public API
async def publish(self, topic, payload):
    async with breaker: ...                       # OpenedState bubbles to caller
                                                  # caller now depends on purgatory's exception type

# 6. No OTel signal on state transition
# Operator can't see WHY traffic dropped to zero

# 7. Hardcoded thresholds
breaker = factory.get_breaker("...", threshold=5, ttl=30)   # not Config-driven; consumer can't tune

# 8. Breaker on cache lookup
async def cache_get(key):
    async with breaker: return self._cache[key]   # cache miss is cheap; breaker overhead is wasted

# 9. Sync breaker (pybreaker) in async code
sync_breaker = pybreaker.CircuitBreaker(...)
async def f():
    with sync_breaker: await something()           # blocks event loop

# 10. excluded_exceptions=(Exception,)
# defeats the breaker entirely; everything is "excluded"
```

## Cross-references

- `python-asyncio-patterns` Rule 4 (cancellation safety) — `async with breaker` survives cancellation.
- `python-exception-patterns` — `CircuitOpenError` extends `MotadataError`.
- `idempotent-retry-safety` — retry pairs with breaker; only retry idempotent operations.
- `python-otel-instrumentation` — state-transition observation.
- `python-sdk-config-pattern` — breaker thresholds are Config fields.
- `python-dependency-vetting` — vet `purgatory` (or alternative) before adoption.
- `network-error-classification` — which exceptions count as breaker failures.
