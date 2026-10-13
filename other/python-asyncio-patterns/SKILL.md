---
name: python-asyncio-patterns
description: >
  Use this when writing async I/O methods, fan-out work, background workers, or
  bridging blocking code into a Python SDK client. Covers asyncio.TaskGroup
  structured concurrency, strong-ref task storage to prevent mid-flight GC,
  gather vs wait selection, asyncio.to_thread / run_in_executor for sync
  bridging, and Task.cancel() semantics.
  Triggers: asyncio, create_task, ensure_future, TaskGroup, gather, wait, run_in_executor, fire-and-forget, async, await.
---

# python-asyncio-patterns (v1.0.0)

## Rationale

Async Python is a sharp tool. The same syntax that gives you `Promise.all`-style fan-out can also leak tasks, swallow cancellations, deadlock on a forgotten `await`, or crash a caller already inside an event loop. The Python pack's SDK code targets `requires-python >= 3.12`, which means **`asyncio.TaskGroup` is the default**. The patterns below describe what to use and what to avoid.

This skill is cited by `code-reviewer-python` (review-criteria §asyncio safety), `refactoring-agent-python` (R-4 time.sleep in async, R-5 discarded create_task), `sdk-asyncio-leak-hunter-python` (L-1 task leakage), `sdk-api-ergonomics-devil-python` (E-3 async-context-manager protocol), and `conventions.yaml` (`async_ownership`, `cancellation_primitive`).

## Activation signals

- Designing or reviewing any `async def` function in SDK code.
- Code review surfaces `asyncio.gather` without explicit reasoning.
- Code review surfaces `asyncio.create_task(coro())` whose return value is discarded.
- Code under review uses `time.sleep` inside `async def`.
- Code under review uses `asyncio.run(...)` inside library code.
- Constructor / factory of an SDK client spawns background tasks (lifetime ownership question).

## Core rules

### Rule 1 — TaskGroup is the default fan-out primitive

Use `asyncio.TaskGroup` (Python 3.11+) for structured concurrency. The first failure cancels siblings; cancellation is propagated cleanly; exceptions surface as `ExceptionGroup` / `BaseExceptionGroup`. The body of the `async with` block does not exit until every spawned task has finished.

```python
import asyncio

async def fan_out_publishes(client, messages: list[Message]) -> None:
    async with asyncio.TaskGroup() as tg:
        for msg in messages:
            tg.create_task(client.publish(msg.topic, msg.payload))
    # Every publish completed (or every-publish-was-cancelled because one failed).
```

`gather` is allowed ONLY when one of its specific behaviors is required:
- `return_exceptions=True` semantics — collect both successes and failures into one list.
- "Return as soon as the first one finishes" via `asyncio.wait(..., return_when=FIRST_COMPLETED)` (and only `wait`, not `gather` — `gather` does not support FIRST_COMPLETED).

If the use case is "run N coroutines concurrently, fail fast on any error" — that is `TaskGroup`, not `gather`.

### Rule 2 — Every Task gets a strong reference

`asyncio.create_task(coro())` whose return value is discarded is a footgun: the Task can be garbage-collected mid-execution because the event loop only weakly references running tasks (this is a documented behavior since Python 3.7, with a known DeprecationWarning in 3.11+ for this exact pattern in some contexts).

```python
# WRONG — task may be GC'd mid-execution
asyncio.create_task(self._background_keepalive())

# RIGHT — instance keeps a strong ref; cancel on shutdown
self._keepalive_task = asyncio.create_task(self._background_keepalive())

# In __aexit__ / close():
self._keepalive_task.cancel()
try:
    await self._keepalive_task
except asyncio.CancelledError:
    pass
```

If the lifetime is scope-local rather than instance-local, prefer `TaskGroup`:

```python
async with asyncio.TaskGroup() as tg:
    keepalive = tg.create_task(self._keepalive())
    # work...
# keepalive completes / is cancelled when the block exits.
```

### Rule 3 — Library code never calls `asyncio.run`

`asyncio.run` creates and tears down a new event loop. If the caller already has a loop running (which is normally the case for any async caller), `asyncio.run` raises `RuntimeError: asyncio.run() cannot be called from a running event loop`. SDK code MUST expose coroutines and let the consumer drive the loop.

```python
# WRONG — library code
def publish(message: bytes) -> None:
    asyncio.run(_async_publish(message))   # crashes any async caller

# RIGHT
async def publish(message: bytes) -> None:
    await _async_publish(message)

# Consumer pattern (consumer's code, not SDK code):
asyncio.run(client.publish(b"hello"))
```

If a synchronous facade is part of the SDK contract (e.g., `motadatapysdk.sync.Client`), it lives in a separate sync module and uses `asyncio.run` at its OWN entry point — but only there, and the async client is the canonical surface.

### Rule 4 — Cancellation safety

Every `await` point in a public async function is a cancellation point. The function MUST be safe to cancel at any of those points: no half-mutated state, no leaked file handles, no half-released locks.

```python
# RISKY — cancellation between session create and lock release leaks state
async def publish(self, msg: bytes) -> None:
    self._lock_held = True
    await self._send(msg)         # <-- cancellation here leaves _lock_held=True
    self._lock_held = False

# RIGHT — `try`/`finally` ensures cleanup runs on cancellation
async def publish(self, msg: bytes) -> None:
    self._lock_held = True
    try:
        await self._send(msg)
    finally:
        self._lock_held = False

# BETTER — use the actual asyncio primitive
async def publish(self, msg: bytes) -> None:
    async with self._lock:
        await self._send(msg)
```

Never catch `asyncio.CancelledError` to suppress it. Re-raise after cleanup (the `finally` block above is the canonical pattern). Catching and not re-raising = suppressing cancellation = the calling `TaskGroup` waits forever.

```python
# WRONG — swallows cancellation
try:
    await self._step()
except asyncio.CancelledError:
    log.warning("cancelled")
    return                  # <-- swallowed; caller's TaskGroup hangs

# RIGHT
try:
    await self._step()
except asyncio.CancelledError:
    log.warning("cancelled")
    raise                   # <-- re-raise after side-effects
```

In Python 3.8+, `asyncio.CancelledError` inherits from `BaseException` (not `Exception`). A bare `except Exception:` does NOT catch it — that is intentional; do not "fix" this with `except BaseException:`.

### Rule 5 — `asyncio.timeout` over `asyncio.wait_for`

For Python 3.11+, prefer the context-manager form:

```python
import asyncio

async def fetch_with_timeout(self, url: str) -> bytes:
    async with asyncio.timeout(5.0):
        return await self._http.get(url)
```

`asyncio.timeout()` is composable (you can stack it inside another `timeout()` for nested deadlines), uses `TimeoutError` (not the older `asyncio.TimeoutError`, which is now an alias), and integrates cleanly with `TaskGroup`. `asyncio.wait_for(coro, timeout)` is still acceptable but is the older API.

### Rule 6 — Synchronization primitives

For mutual exclusion of `await`-able critical sections:

```python
self._lock = asyncio.Lock()                  # one holder at a time
async with self._lock:
    await self._do_critical()
```

For bounded concurrency (rate limiting fan-out):

```python
self._sem = asyncio.Semaphore(max_concurrent=10)
async def _bounded_publish(self, msg: bytes) -> None:
    async with self._sem:
        await self._publish(msg)
```

For waiting on a flag:

```python
self._ready = asyncio.Event()
# Producer: self._ready.set()
# Consumer: await self._ready.wait()
```

NEVER use `threading.Lock` / `threading.Event` / `threading.Semaphore` from async code. They block the event loop. The asyncio counterparts are not interchangeable with the threading ones.

### Rule 7 — Mixing threads and asyncio

When async code MUST call a blocking sync function (legacy library, CPU-bound work, blocking C extension), use `asyncio.to_thread` (3.9+):

```python
# Blocking sync function (e.g., a CPU-bound parser)
def parse_blob_sync(data: bytes) -> Record: ...

# Async wrapper — runs the sync code on the default ThreadPoolExecutor.
async def parse_blob(data: bytes) -> Record:
    return await asyncio.to_thread(parse_blob_sync, data)
```

For tighter control over the executor (custom thread pool with bounded size), use `loop.run_in_executor(executor, fn, *args)`. The default `to_thread` uses a process-wide pool, which is fine for occasional blocking calls but can be saturated by SDK-driven fan-out. Document the choice in the affected client's docstring.

### Rule 8 — Async context manager pattern for clients

Any SDK client that holds resources (connections, pools, background tasks) implements `__aenter__` and `__aexit__`. The canonical usage in Quick start is `async with`:

```python
class Client:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._session: aiohttp.ClientSession | None = None
        self._keepalive_task: asyncio.Task[None] | None = None

    async def __aenter__(self) -> Client:
        self._session = aiohttp.ClientSession(...)
        self._keepalive_task = asyncio.create_task(self._keepalive())
        return self

    async def __aexit__(self, exc_type, exc_val, tb) -> None:
        if self._keepalive_task is not None:
            self._keepalive_task.cancel()
            try:
                await self._keepalive_task
            except asyncio.CancelledError:
                pass
        if self._session is not None:
            await self._session.close()
```

Manual `await client.close()` is acceptable as a fallback API but the documented canonical usage is `async with`.

## GOOD: full client example

```python
import asyncio
import logging

import aiohttp

logger = logging.getLogger(__name__)


class Client:
    """Async client for the motadata events API.

    Examples:
        >>> async with Client(Config(base_url="https://example.com")) as client:
        ...     await client.publish("topic", b"payload")  # doctest: +SKIP
    """

    def __init__(self, config: Config) -> None:
        self._config = config
        self._session: aiohttp.ClientSession | None = None
        self._publish_sem = asyncio.Semaphore(config.max_concurrent_publishes)

    async def __aenter__(self) -> "Client":
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self._config.timeout_s),
        )
        return self

    async def __aexit__(self, exc_type, exc_val, tb) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None

    async def publish(self, topic: str, payload: bytes) -> None:
        if self._session is None:
            raise RuntimeError("Client is not entered; use 'async with Client(...) as client:'")
        async with self._publish_sem, asyncio.timeout(self._config.timeout_s):
            async with self._session.post(self._url(topic), data=payload) as resp:
                resp.raise_for_status()

    async def fan_out_publish(self, items: list[tuple[str, bytes]]) -> None:
        async with asyncio.TaskGroup() as tg:
            for topic, payload in items:
                tg.create_task(self.publish(topic, payload))
```

This example demonstrates: rule 8 (`__aenter__` / `__aexit__`), rule 6 (Semaphore bounded fan-out), rule 5 (`asyncio.timeout`), rule 1 (TaskGroup fan-out), rule 4 (cancellation safety via `async with`).

## BAD anti-patterns

```python
# 1. asyncio.run in library code
def publish(message: bytes) -> None:
    asyncio.run(_async_publish(message))     # CRASHES caller's loop

# 2. Discarded create_task
asyncio.create_task(self._keepalive())        # task may be GC'd

# 3. time.sleep in async
async def slow_op() -> None:
    time.sleep(1)                              # blocks the event loop
                                               # USE: await asyncio.sleep(1)

# 4. Swallowing CancelledError
try:
    await self._step()
except asyncio.CancelledError:
    return                                     # caller hangs

# 5. asyncio.gather + return_exceptions=True for plain fan-out
results = await asyncio.gather(*tasks, return_exceptions=True)
# (use TaskGroup unless you specifically want errors as values)

# 6. Sync threading primitive in async code
lock = threading.Lock()                        # blocks loop on contention

# 7. Synchronous I/O in async function
async def read_config() -> dict:
    return json.load(open("config.json"))      # blocking read inside async

# 8. New event loop in library code
loop = asyncio.new_event_loop()                # interferes with caller's loop
```

## Cancellation contract — when to document `Raises: asyncio.CancelledError`

Every public async function may be cancelled. The docstring's `Raises:` block lists `asyncio.CancelledError` only when the function does something specific on cancellation that the caller should know about (e.g., "cancellation aborts the in-flight HTTP request and rolls back the transaction"). For most SDK methods the implicit "may be cancelled, no rollback needed" is the default and does not need explicit documentation.

## Decision tree — which primitive?

| Need | Primitive |
|------|-----------|
| Run N coroutines concurrently, fail-fast | `asyncio.TaskGroup` |
| Run N coroutines concurrently, collect both successes and errors | `asyncio.gather(..., return_exceptions=True)` |
| Wait for first to complete (race) | `asyncio.wait(..., return_when=FIRST_COMPLETED)` |
| Cap at N parallel | `asyncio.Semaphore(N)` |
| Mutual exclusion | `asyncio.Lock` |
| Producer/consumer signal | `asyncio.Event` |
| Bounded queue | `asyncio.Queue(maxsize=N)` |
| Bounded ordered queue | `asyncio.PriorityQueue` |
| Single-shot deadline | `async with asyncio.timeout(s):` |
| Sleep / pace | `await asyncio.sleep(s)` |
| Run blocking sync in thread | `await asyncio.to_thread(fn, *args)` |

## Cross-references

- `python-pytest-patterns` — `asyncio_mode = "auto"` for pytest-asyncio testing of these patterns.
- `python-client-shutdown-lifecycle` — full `__aenter__` / `__aexit__` lifecycle.
- `python-asyncio-leak-prevention` — testing for task leaks via gc-based scanners.
- `conventions.yaml` `async_ownership` — design-rule equivalent enforced at D3.
- `conventions.yaml` `cancellation_primitive` — the rule above for `asyncio.timeout` over `wait_for`.
