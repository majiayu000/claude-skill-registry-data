---
name: python-client-shutdown-lifecycle
description: >
  Use this when designing a new Python SDK client class, reviewing a __del__
  method or non-idempotent close(), seeing aclose() that lacks a drain timeout,
  or auditing whether the test suite ever exercises the close path. Covers the
  async with canonical surface with aclose() fallback, the _closed flag plus
  optional asyncio.Lock for idempotency, ordered teardown (tasks → drain →
  sessions → executors), aclose vs close naming, bounded drain with force-cancel,
  asyncio.shield for cancellation safety, post-close InvalidStateError raising,
  __aexit__ delegation, and AsyncExitStack composition.
  Triggers: aclose, close, __aenter__, __aexit__, async with, shutdown, cleanup, idempotent, _closed.
---

# python-client-shutdown-lifecycle (v1.0.0)

## Rationale

Every Python SDK client that holds resources must shut down cleanly. "Cleanly" means: idempotent (safe to call twice), bounded (the user can wait at most `timeout_s`), ordered (sub-resources released in the reverse order they were acquired), and leak-free (no asyncio task / aiohttp session / file descriptor outlives the close call). Get this wrong and the SDK ships an asyncio-shaped foot-gun.

This skill prescribes the canonical Python pack lifecycle: `async with` as the primary surface, `aclose()` as the fallback, the `_closed` flag for idempotency, ordered teardown sub-routines, and a cancellation-safe drain primitive.

This skill is cited by `code-reviewer-python` (review-criteria), `sdk-api-ergonomics-devil-python` (E-3 async-context-manager protocol), `sdk-asyncio-leak-hunter-python` (leak gates rely on this contract), `sdk-convention-devil-python` (C-5), `python-asyncio-patterns` (Rule 8), `python-asyncio-leak-prevention`, and `python-sdk-config-pattern`.

## Activation signals

- Designing or reviewing a new SDK client class.
- Code review surfaces a `__del__` method (red flag — see Rule 1).
- Code review surfaces `close()` without idempotency guard.
- The Quick start uses `client.close()` as the default rather than `async with`.
- Test suite tests the happy path but never the close path.

## Core rules

### Rule 1 — `async with` is the canonical surface; `aclose()` is the fallback

```python
class Client:
    """Async client for the motadata API.

    Examples:
        Canonical usage::

            >>> async with Client(Config(...)) as client:
            ...     await client.publish("topic", b"x")  # doctest: +SKIP

        Manual lifecycle (fallback)::

            >>> client = Client(Config(...))
            >>> try:
            ...     await client.publish("topic", b"x")  # doctest: +SKIP
            ... finally:
            ...     await client.aclose()                # doctest: +SKIP
    """
```

`async with` wins because:
- Cleanup runs even on exception inside the body.
- Cleanup runs on cancellation.
- The lifecycle scope is visible to the reader.

`aclose()` (NOT `close()` for async; see Rule 4) is for cases where the lifetime can't be a single block — long-lived clients owned by a framework, dependency-injected clients managed by the framework's own lifecycle.

NEVER rely on `__del__` for cleanup. `__del__` runs whenever the GC decides — possibly never, possibly after the event loop is closed (raising "Event loop is closed" exceptions during shutdown). The class invariant is: "if `aclose()` was not called, the client is leaked." Document this.

### Rule 2 — `_closed` flag for idempotency

```python
class Client:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._closed = False
        self._session: aiohttp.ClientSession | None = None

    async def aclose(self) -> None:
        if self._closed:
            return
        self._closed = True               # set BEFORE awaiting cleanup
        # ... cleanup ...

    async def __aexit__(self, exc_type, exc_val, tb) -> None:
        await self.aclose()
```

Setting `_closed = True` BEFORE the first `await` is critical. Without it, two concurrent `aclose()` calls both reach the cleanup path. With it, the second call returns immediately at the `if self._closed: return` check.

For pure-thread-safety on top of asyncio safety, use `asyncio.Lock`:

```python
class Client:
    def __init__(self, config: Config) -> None:
        ...
        self._closed = False
        self._close_lock = asyncio.Lock()

    async def aclose(self) -> None:
        async with self._close_lock:
            if self._closed:
                return
            self._closed = True
            # ... cleanup ...
```

The lock makes `aclose()` safe under concurrent invocation. Most clients don't need it (callers shouldn't be racing close), but for SDKs used in framework code where two cleanup paths might fire simultaneously, the lock is cheap insurance.

### Rule 3 — Ordered teardown — reverse acquisition order

Acquire: tasks → executors → sessions → connections.
Release: connections → sessions → executors → tasks (reverse).

This sequencing matters because sessions hold connections (close session before connection); executors run tasks (cancel tasks before shutting executor); tasks hold sessions (cancel tasks before closing sessions to avoid in-flight requests on a closed session).

Concrete ordering for a typical SDK client:

```python
async def aclose(self) -> None:
    if self._closed:
        return
    self._closed = True

    # 1. Cancel background tasks first — they may be holding resources we're about to close
    if self._keepalive_task is not None:
        self._keepalive_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._keepalive_task
        self._keepalive_task = None

    # 2. Drain in-flight requests (with timeout)
    await self._drain_inflight(timeout_s=self._config.shutdown_drain_s)

    # 3. Close sessions (closes connections too)
    if self._session is not None:
        await self._session.close()
        self._session = None

    # 4. Shut down custom executor (last — anything still running gets cancelled)
    if self._executor is not None:
        self._executor.shutdown(wait=False, cancel_futures=True)
        self._executor = None
```

### Rule 4 — `aclose()` (async) vs `close()` (sync)

Naming:
- Sync resource (e.g., a sync wrapper around a sync client): `close()`.
- Async resource: `aclose()`.

The `aclose` convention comes from the stdlib (`asyncio.StreamWriter.aclose`, `asyncio.AbstractEventLoop.shutdown_asyncgens` patterns) and PEP 525 (async generators). Call it `aclose` so callers know they need to `await`.

Never define BOTH `close()` AND `aclose()` on an async client unless the sync `close()` is genuinely a separate operation (e.g., a sync facade wrapping the async client, where `Client.close()` is "kill the underlying connection synchronously without draining"). Two close methods invite the bug where consumers call the wrong one.

### Rule 5 — Drain with bounded timeout

```python
async def _drain_inflight(self, *, timeout_s: float) -> None:
    """Wait for in-flight requests to finish; force-cancel after timeout_s."""
    if not self._inflight:
        return
    try:
        async with asyncio.timeout(timeout_s):
            await asyncio.gather(*self._inflight, return_exceptions=True)
    except builtins.TimeoutError:
        # Drain timed out; force-cancel remaining
        for task in self._inflight:
            if not task.done():
                task.cancel()
        # Wait briefly for cancellations to settle
        await asyncio.gather(*self._inflight, return_exceptions=True)
        logger.warning(
            "shutdown drain timed out after %.1fs; cancelled %d in-flight",
            timeout_s, sum(1 for t in self._inflight if not t.done()),
        )
```

Drain semantics:
- WAIT for in-flight to complete naturally (up to `timeout_s`).
- After timeout, CANCEL remaining and wait briefly for cancellation to settle.
- LOG the cancellation count — operators want to know shutdown was forced.

`return_exceptions=True` on the gather is important — without it, the first exception would short-circuit and leave the others still running (leak).

`shutdown_drain_s` is a Config field with a sensible default (typically 5–10 seconds). Document that callers can set it to `0` for "drain best-effort, return immediately."

### Rule 6 — Cancellation safety

`__aexit__` and `aclose()` MUST be cancellation-safe. If the consumer's `async with` body is cancelled, the cleanup still runs (Python guarantees this for `__aexit__`). If the cleanup ITSELF is cancelled mid-flight, the client may leak — defend against it:

```python
async def aclose(self) -> None:
    if self._closed:
        return
    self._closed = True
    # Shield critical cleanup from outer cancellation:
    try:
        await asyncio.shield(self._do_cleanup())
    except asyncio.CancelledError:
        # If we WERE cancelled, _do_cleanup may have completed inside shield;
        # still re-raise so the calling context sees cancellation
        raise
```

`asyncio.shield` makes the inner task uncancellable from outside (the inner task continues running even if the outer awaiter is cancelled). The outer awaiter still raises `CancelledError`, but cleanup completes.

Use shield SPARINGLY — overuse defeats cancellation. The right rule: shield only the SHORT, idempotent, leak-preventing operations (closing a session, releasing a fd). Don't shield drain (it should respect cancellation; a cancelled close means "force shutdown immediately").

### Rule 7 — Operations after close raise

```python
async def publish(self, topic: str, payload: bytes) -> None:
    if self._closed:
        raise RuntimeError("client is closed")    # or InvalidStateError if defined
    if self._session is None:
        raise RuntimeError("client is not entered; use 'async with Client(...) as c:'")
    # ... do the publish
```

The check is at the START of every public method. Don't wait for a downstream NPE on `self._session.post(...)` — fail fast with a clear message.

For SDKs that define typed errors (per `python-exception-patterns`):

```python
class InvalidStateError(MotadataError, RuntimeError):
    """Operation invoked on a closed or unentered client."""
```

### Rule 8 — `__aexit__` delegates to `aclose()`

```python
async def __aexit__(
    self,
    exc_type: type[BaseException] | None,
    exc_val: BaseException | None,
    tb: TracebackType | None,
) -> None:
    await self.aclose()
```

The signature has annotations (mypy `--strict`). The return type is `None` (NEVER `bool` unless you specifically want to suppress exceptions, which an SDK client almost never does).

`__aexit__` returning `None` means: pass any exception in the body up to the caller. Returning `True` would SWALLOW exceptions — a footgun.

### Rule 9 — Consumer pattern with `AsyncExitStack` for multiple clients

```python
import contextlib

async def main() -> None:
    async with contextlib.AsyncExitStack() as stack:
        client = await stack.enter_async_context(Client(client_cfg))
        cache = await stack.enter_async_context(Cache(cache_cfg))
        storage = await stack.enter_async_context(Storage(storage_cfg))
        # ... use them
    # All three exit in REVERSE order, even on exception.
```

`AsyncExitStack` is the right primitive when a consumer needs to compose multiple async-context-manager clients. Document it in the SDK README's "Multi-client" section if the use case is common.

## GOOD: full lifecycle pattern

```python
from __future__ import annotations

import asyncio
import contextlib
import logging
from types import TracebackType
from typing import Self

import aiohttp

from motadatapysdk.errors import InvalidStateError, MotadataError

logger = logging.getLogger(__name__)


class Client:
    """Async client for the motadata API.

    Examples:
        >>> async def main() -> None:
        ...     async with Client(Config(base_url="...", api_key="...")) as client:
        ...         await client.publish("topic", b"x")
        >>> asyncio.run(main())  # doctest: +SKIP
    """

    def __init__(self, config: Config) -> None:
        self._config = config
        self._closed = False
        self._close_lock = asyncio.Lock()
        self._session: aiohttp.ClientSession | None = None
        self._keepalive_task: asyncio.Task[None] | None = None
        self._inflight: set[asyncio.Task[None]] = set()

    async def __aenter__(self) -> Self:
        timeout = aiohttp.ClientTimeout(total=self._config.timeout_s)
        self._session = aiohttp.ClientSession(timeout=timeout)
        self._keepalive_task = asyncio.create_task(
            self._keepalive(),
            name="motadata.client.keepalive",
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """Close the client, releasing all resources. Idempotent."""
        async with self._close_lock:
            if self._closed:
                return
            self._closed = True

        # 1. Cancel background task
        if self._keepalive_task is not None:
            self._keepalive_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._keepalive_task
            self._keepalive_task = None

        # 2. Drain in-flight (bounded)
        await self._drain_inflight(timeout_s=self._config.shutdown_drain_s)

        # 3. Close session
        if self._session is not None:
            await self._session.close()
            self._session = None

    async def publish(self, topic: str, payload: bytes) -> None:
        """Publish ``payload`` to ``topic``."""
        if self._closed:
            raise InvalidStateError("client is closed")
        if self._session is None:
            raise InvalidStateError(
                "client is not entered; use 'async with Client(...) as c:'"
            )

        task = asyncio.create_task(
            self._do_publish(topic, payload),
            name=f"motadata.client.publish.{topic}",
        )
        self._inflight.add(task)
        task.add_done_callback(self._inflight.discard)
        try:
            await task
        finally:
            self._inflight.discard(task)

    async def _do_publish(self, topic: str, payload: bytes) -> None:
        assert self._session is not None
        async with self._session.post(self._url(topic), data=payload) as resp:
            resp.raise_for_status()

    async def _keepalive(self) -> None:
        try:
            while not self._closed:
                await asyncio.sleep(self._config.keepalive_interval_s)
                # ... send ping ...
        except asyncio.CancelledError:
            raise

    async def _drain_inflight(self, *, timeout_s: float) -> None:
        if not self._inflight:
            return
        try:
            async with asyncio.timeout(timeout_s):
                await asyncio.gather(*self._inflight, return_exceptions=True)
        except TimeoutError:
            cancelled = 0
            for task in self._inflight:
                if not task.done():
                    task.cancel()
                    cancelled += 1
            await asyncio.gather(*self._inflight, return_exceptions=True)
            logger.warning(
                "shutdown drain timed out after %.1fs; force-cancelled %d task(s)",
                timeout_s, cancelled,
            )

    def _url(self, topic: str) -> str:
        return f"{self._config.base_url.rstrip('/')}/topics/{topic}"
```

Demonstrates: Rule 1 (async with primary), Rule 2 (`_closed` + lock), Rule 3 (ordered teardown), Rule 4 (`aclose` not `close`), Rule 5 (drain with timeout), Rule 7 (operations-after-close raise), Rule 8 (`__aexit__` delegates), set-based inflight tracking.

## BAD anti-patterns

```python
# 1. close() not idempotent
async def close(self):
    await self._session.close()         # second call → AttributeError

# 2. __del__ for cleanup
def __del__(self):                       # runs when GC decides; may be never
    asyncio.run(self.aclose())          # may RuntimeError if loop is gone

# 3. Wrong close order (session before tasks)
async def aclose(self):
    await self._session.close()         # in-flight publish on closed session
    self._task.cancel()

# 4. No timeout on drain
async def aclose(self):
    await asyncio.gather(*self._inflight)  # could hang forever

# 5. close() name on async client
async def close(self) -> None:           # callers may forget to await

# 6. __aexit__ returns True (swallows exceptions)
async def __aexit__(self, ...) -> bool:
    await self.aclose()
    return True                          # body's exception is swallowed

# 7. Operations don't check _closed
async def publish(self, ...):
    await self._session.post(...)        # AttributeError when session is None

# 8. _closed flag set AFTER await
async def aclose(self):
    await self._session.close()
    self._closed = True                  # race: concurrent aclose double-closes

# 9. Manual lifecycle in Quick start example
"""Quick start:
    client = Client(...)
    await client.publish(...)
    await client.aclose()                # error path leaks
"""
# Use `async with` in the example.

# 10. CancelledError swallowed in cleanup
try:
    await self._keepalive_task
except asyncio.CancelledError:
    return                               # caller's outer cancellation hangs
```

## Test gates

The leak fixtures from `python-asyncio-leak-prevention` (asyncio_task_tracker, unclosed_session_tracker, fd_tracker) automatically verify the close path. Add explicit tests:

```python
async def test_aclose_idempotent() -> None:
    client = Client(Config(...))
    async with client:
        ...
    await client.aclose()                # second close is a no-op
    await client.aclose()                # third close is a no-op

async def test_publish_after_close_raises() -> None:
    client = Client(Config(...))
    async with client:
        ...
    with pytest.raises(InvalidStateError, match="client is closed"):
        await client.publish("topic", b"x")

async def test_drain_timeout_forces_cancel(monkeypatch) -> None:
    # Construct a publisher whose underlying call hangs
    cfg = Config(..., shutdown_drain_s=0.05)
    async with Client(cfg) as client:
        task = asyncio.create_task(client.publish("topic", b"x"))
        # ... arrange the publish to hang ...
    # Outer __aexit__ should complete within drain_s + ~0.5s slop
```

## Cross-references

- `python-asyncio-patterns` Rule 4 (cancellation safety) + Rule 8 (`__aenter__`/`__aexit__`).
- `python-asyncio-leak-prevention` — leak fixtures verify this contract.
- `python-exception-patterns` — `InvalidStateError` for operations after close.
- `python-sdk-config-pattern` — `shutdown_drain_s` and `keepalive_interval_s` are Config fields.
- `python-doctest-patterns` — Quick start examples use `async with` form.
- `sdk-convention-devil-python` C-5 — design-rule enforcement at D3.
