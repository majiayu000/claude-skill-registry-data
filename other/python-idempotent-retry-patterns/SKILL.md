---
name: python-idempotent-retry-patterns
description: >
  Use this for the Python-specific realization of idempotent-retry-safety —
  exception-class predicate using `isinstance` / `__cause__` chains,
  asyncio-friendly backoff with cancellation propagation, `tenacity` decorator
  patterns, `Idempotency-Key` headers on httpx requests, and dedup-key handling
  on aiokafka producers. Pairs with shared-core `idempotent-retry-safety`
  (taxonomy + decision criteria).
  Triggers: tenacity, retry, asyncio.TimeoutError, asyncio.CancelledError, raise from, idempotency-key, httpx, aiokafka, AIMD, Retry-After, RateLimitError.
version: 1.0.0
last-evolved-in-run: v0.6.0-rc.0-sanitization
status: stable
tags: [python, retry, resilience, asyncio, sdk]
---

# python-idempotent-retry-patterns (v1.0.0)

## Scope

Python realization of the rules in shared-core `idempotent-retry-safety`. The shared skill defines the taxonomy (retriable vs fatal vs auth), idempotency-envelope requirement, and jittered backoff mandate. This skill is the Python code that realizes them.

## Retry predicate — exception-class based

```python
from typing import Type
import asyncio
import httpx

# Fatal exceptions — never retry. Mirror shared taxonomy.
FATAL_EXCEPTIONS: tuple[Type[BaseException], ...] = (
    ValidationError,
    AuthError,
    ClientError,            # 4xx — caller's bug
    asyncio.CancelledError, # caller asked to stop
)

# Retriable exceptions — safe to retry given idempotency.
RETRIABLE_EXCEPTIONS: tuple[Type[BaseException], ...] = (
    TimeoutError,
    asyncio.TimeoutError,
    NetworkError,
    httpx.NetworkError,
    httpx.PoolTimeout,
    ServerError,            # 5xx with idempotent op
)

def is_retryable(exc: BaseException) -> bool:
    """Classify an exception. Cancellation is never retriable."""
    if isinstance(exc, FATAL_EXCEPTIONS):
        return False
    if isinstance(exc, RETRIABLE_EXCEPTIONS):
        return True
    # Walk __cause__ chain for wrapped exceptions
    cause = exc.__cause__
    while cause is not None:
        if isinstance(cause, FATAL_EXCEPTIONS):
            return False
        if isinstance(cause, RETRIABLE_EXCEPTIONS):
            return True
        cause = cause.__cause__
    return False  # Conservative default: unknown = don't retry
```

Key points:
- `isinstance` against the class hierarchy; never `str(exc)` matching.
- Walk `__cause__` chain for wrapped exceptions (Python's typed-error chain mechanism, analogous to typed-cause traversal in other languages).
- `asyncio.CancelledError` is **never** retriable — it propagates from cooperative cancellation; retrying would defeat the cancel.
- Conservative default `False` — Python encourages explicit allowlists for retry.

## Context-aware backoff with `tenacity`

```python
from tenacity import (
    retry, retry_if_exception, stop_after_attempt, wait_exponential_jitter
)

@retry(
    retry=retry_if_exception(is_retryable),
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=0.1, max=5.0, jitter=0.1),
    reraise=True,
)
async def publish(client: httpx.AsyncClient, payload: bytes, *, idempotency_key: str) -> None:
    response = await client.post(
        "/events",
        content=payload,
        headers={"Idempotency-Key": idempotency_key},
    )
    response.raise_for_status()
```

`tenacity`'s `wait_exponential_jitter` produces `min(max, initial * 2**n + uniform(0, jitter))` per attempt — same shape as Go SDK's `RetryMiddleware`. Use `reraise=True` so the original exception (not `RetryError`) surfaces to the caller.

## Manual loop when `tenacity` is overkill

```python
async def execute_with_retry(
    op: Callable[[], Awaitable[T]],
    *,
    max_attempts: int = 3,
    initial: float = 0.1,
    max_wait: float = 5.0,
) -> T:
    last_exc: BaseException | None = None
    for attempt in range(max_attempts):
        try:
            return await op()
        except asyncio.CancelledError:
            raise  # never swallow cancellation
        except BaseException as exc:
            last_exc = exc
            if not is_retryable(exc) or attempt >= max_attempts - 1:
                raise
        # Jittered exponential backoff; asyncio.sleep is cancellable.
        backoff = min(max_wait, initial * (2 ** attempt))
        backoff += random.uniform(0, backoff * 0.1)  # ±10% jitter
        await asyncio.sleep(backoff)
    raise last_exc  # type: ignore[misc]
```

Critical: `await asyncio.sleep(d)` is cancellable. Unlike Python's `time.sleep`, it propagates `CancelledError` from the surrounding task. Never use `time.sleep` inside an async retry loop — it blocks the event loop AND ignores cancellation.

## Idempotency envelope

**HTTP POST/PATCH** — caller-supplied `Idempotency-Key` header (UUID v4 per logical request):

```python
async def publish_event(client: httpx.AsyncClient, event: Event) -> None:
    key = event.idempotency_key or str(uuid.uuid4())
    await client.post(
        "/events",
        json=event.model_dump(),
        headers={"Idempotency-Key": key},
    )
```

**aiokafka producer** — message `key` parameter is the dedup field; brokers configured with `max.in.flight.requests.per.connection=1` + `enable.idempotence=true`:

```python
producer = AIOKafkaProducer(
    bootstrap_servers="localhost:9092",
    enable_idempotence=True,
    acks="all",
)
await producer.send_and_wait(
    topic="events",
    key=event.id.encode(),  # dedup key
    value=msgpack.packb(event.model_dump()),
)
```

**HTTP GET/PUT/DELETE** — idempotent by RFC 9110 contract. Retry freely on transport errors; no header needed.

## Anti-patterns

**1. `except BaseException: pass` in retry loop.** Swallows `KeyboardInterrupt`, `SystemExit`, `CancelledError`. Fix: catch `Exception`, AND re-raise `CancelledError` explicitly.

**2. `time.sleep(d)` instead of `await asyncio.sleep(d)`.** Blocks event loop; ignores cancellation. Always `await asyncio.sleep`.

**3. Bare `tenacity.retry()` with no retry predicate.** Retries on every exception including programmer errors (`AttributeError`, `KeyError`). Always pass `retry=retry_if_exception(predicate)`.

**4. Catching `asyncio.TimeoutError` and not re-raising on cancellation.** A cancelled task that catches its own `TimeoutError` may not propagate. Use `asyncio.timeout()` context manager (Python 3.11+) which re-raises cleanly.

**5. POST without idempotency key + retry on 5xx.** Same anti-pattern as Go: caller can't tell whether server committed. Fix: add `Idempotency-Key` OR don't retry POST on 5xx.

## Cross-references

- shared-core `idempotent-retry-safety` — taxonomy, decision criteria, HTTP semantics
- `network-error-classification` — exception taxonomy that the predicate reads
- `python-circuit-breaker-policy` — breaker + retry are dual; same exception classes feed both
- `python-asyncio-patterns` — TaskGroup, structured concurrency around the retry loop
- `python-asyncio-cancellation` — when CancelledError surfaces and how to honor it
- `python-exception-patterns` — exception class hierarchy + `raise from` chaining

## Guardrail hooks

- python-leak-prevention (G63-py) — catches `time.sleep` in async paths
- python-bench regression — retry fast-path MUST not regress
- python-asyncio-leak-prevention — retry loops that swallow CancelledError leak tasks
