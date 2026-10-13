---
name: python-backpressure-flow-control
description: >
  Use this when designing fan-out methods that publish downstream, reviewing
  unbounded list/queue buffers, sizing producer/consumer pipelines for a
  throughput target, or debugging OOM under production load. Covers
  asyncio.BoundedSemaphore inflight caps, bounded asyncio.Queue(maxsize=N) with
  block-vs-drop submit shapes, drop-newest / drop-oldest / block strategy
  selection, worker pools with task_done pairing, BackpressureError surfacing,
  and queue-depth + drop-count OTel signals.
  Triggers: asyncio.Semaphore, asyncio.BoundedSemaphore, asyncio.Queue, maxsize, drop, block, put_nowait, QueueFull, inflight, backpressure.
---

# python-backpressure-flow-control (v1.0.0)

## Rationale

If the SDK admits work faster than the downstream can absorb, three things happen — pick which one is correct for your domain:

1. **Block the producer** until capacity frees up — work is preserved, latency degrades.
2. **Drop the work** with an error — latency stays predictable, work is lost.
3. **Buffer it** — works briefly, then either becomes #1 (blocking on memory) or runs out of memory.

Option 3 (unbounded buffer) is never correct. The pack's choice between #1 and #2 is per-workload. This skill describes the primitives, the decision criteria, and the metric that proves backpressure is happening.

This skill is cited by `code-reviewer-python` (resilience review-criteria), `python-asyncio-patterns` (Rule 6 Semaphore), `python-asyncio-leak-prevention` (bounded queue leak gates), `python-otel-instrumentation` (queue-depth metric), `python-sdk-config-pattern` (Config bounds), and `idempotent-retry-safety` (drop policy).

## Activation signals

- Designing a fan-out method that publishes to a downstream.
- Code review surfaces unbounded `list.append(...)` collecting in-flight work.
- TPRD §3 declares a throughput target the SDK must respect.
- Tests pass at low load but OOM at production volume.
- Reviewing whether dropped work is acceptable for a given workload.

## Core decision — block or drop?

```
Is the work safe to lose? (consumer can detect loss; idempotent retry exists; informational data only)
  └── YES → DROP (raise BackpressureError; caller decides what to do)
  └── NO  → BLOCK (await capacity; producer waits until consumer drains)
```

Either choice is RIGHT for some workloads:
- **DROP** — telemetry / metrics emission, log shipping, gossip protocols. Loss is preferable to latency.
- **BLOCK** — order placements, financial transactions, transaction events. Latency is preferable to loss.

Neither is right for "stream as much as you can buffer" — that's the unbounded-buffer trap.

## Rule 1 — `asyncio.BoundedSemaphore` for inflight cap

The simplest backpressure: cap the NUMBER of in-flight async operations. A producer waits at the semaphore acquisition point if the cap is reached.

```python
import asyncio

class Client:
    def __init__(self, config: Config) -> None:
        self._publish_sem = asyncio.BoundedSemaphore(config.max_concurrent_publishes)

    async def publish(self, topic: str, payload: bytes) -> None:
        async with self._publish_sem:           # blocks if N publishes already inflight
            await self._do_publish(topic, payload)
```

`BoundedSemaphore` (over plain `Semaphore`) catches the bug where you `release()` more than you `acquire()` — it raises `ValueError`. Always pick `BoundedSemaphore` for a fixed cap.

This is the BLOCK choice — the producer waits. The cap is in `Config.max_concurrent_publishes` so the consumer tunes per their throughput tolerance.

## Rule 2 — `asyncio.Queue(maxsize=N)` for buffered fan-out

When the producer should not block (fast path) but the consumer is slower, decouple via a bounded queue:

```python
class StreamPublisher:
    def __init__(self, config: Config, client: Client) -> None:
        self._queue: asyncio.Queue[Message] = asyncio.Queue(maxsize=config.queue_size)
        self._client = client
        self._worker_task: asyncio.Task[None] | None = None

    async def __aenter__(self) -> "StreamPublisher":
        self._worker_task = asyncio.create_task(self._consume(), name="stream.publisher.consumer")
        return self

    async def __aexit__(self, exc_type, exc_val, tb) -> None:
        await self._queue.join()                 # drain pending
        if self._worker_task is not None:
            self._worker_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._worker_task

    # BLOCK variant — producer waits if queue is full
    async def submit(self, msg: Message) -> None:
        await self._queue.put(msg)               # awaits if maxsize reached

    # DROP variant — producer raises if queue is full
    def submit_or_drop(self, msg: Message) -> None:
        try:
            self._queue.put_nowait(msg)
        except asyncio.QueueFull as e:
            raise BackpressureError(
                "queue is full; consumer cannot keep up"
            ) from e

    async def _consume(self) -> None:
        while True:
            msg = await self._queue.get()
            try:
                await self._client.publish(msg.topic, msg.payload)
            finally:
                self._queue.task_done()
```

Two `submit` methods to make the choice explicit at the API surface. The class exposes BOTH or just ONE depending on the use case; document which.

`asyncio.QueueFull` raised by `put_nowait` on overflow. Wrap in the SDK's `BackpressureError`:

```python
class BackpressureError(MotadataError):
    """Buffer is full; the caller should slow down or drop."""
```

## Rule 3 — Never `Queue()` without `maxsize`

```python
# WRONG — unbounded, silent OOM
self._queue = asyncio.Queue()

# RIGHT — bounded
self._queue = asyncio.Queue(maxsize=config.queue_size)
```

`asyncio.Queue()` (no `maxsize`) defaults to UNBOUNDED — the producer never blocks. Memory grows until the process dies. Always set `maxsize`.

A `maxsize` of 0 means unbounded too. Pick a real number based on the worst tolerable memory use:

```python
queue_size: int = 1024              # ~16 MB if each Message averages 16 KB
```

## Rule 4 — Backpressure surfaces as a metric

Operators want to see backpressure HAPPENING. Counter the queue depth and the drop count:

```python
from opentelemetry import metrics

meter = metrics.get_meter(__name__)
queue_depth_gauge = meter.create_observable_gauge(
    name="motadata.publisher.queue_depth",
    callbacks=[lambda options: [metrics.Observation(self._queue.qsize())]],
    description="Pending messages in the publisher queue",
)
queue_dropped = meter.create_counter(
    name="motadata.publisher.dropped",
    description="Messages dropped due to backpressure",
)
```

Increment `queue_dropped` from `submit_or_drop` on every `QueueFull`:

```python
def submit_or_drop(self, msg: Message) -> None:
    try:
        self._queue.put_nowait(msg)
    except asyncio.QueueFull as e:
        queue_dropped.add(1, {"reason": "queue_full"})
        raise BackpressureError(...) from e
```

Operators graph `queue_depth` over time + `queue_dropped` rate. Persistent depth + non-zero drops = the consumer is undersized; either grow the worker pool (Rule 5) or accept higher capacity in `Config`.

## Rule 5 — Worker pool for parallel consumption

When ONE consumer is too slow, spawn N workers behind the queue:

```python
class StreamPublisher:
    async def __aenter__(self) -> "StreamPublisher":
        async with asyncio.TaskGroup() as tg:
            self._workers = [
                tg.create_task(self._consume(), name=f"publisher.worker.{i}")
                for i in range(self._config.publisher_worker_count)
            ]
        return self
```

Wait — `TaskGroup` body waits for all tasks. That's not what we want; the workers run concurrently with the rest of the SDK's lifetime. Instead, store strong references (per `python-asyncio-patterns` Rule 2):

```python
async def __aenter__(self) -> "StreamPublisher":
    self._workers = [
        asyncio.create_task(self._consume(), name=f"publisher.worker.{i}")
        for i in range(self._config.publisher_worker_count)
    ]
    return self

async def __aexit__(self, exc_type, exc_val, tb) -> None:
    await self._queue.join()
    for w in self._workers:
        w.cancel()
    await asyncio.gather(*self._workers, return_exceptions=True)
```

`asyncio.Queue` is safe under multiple consumers (one consumer per `get()`). Each worker pulls from the same queue, processes, calls `task_done()`.

## Rule 6 — `task_done()` pairs with `get()`, ALWAYS

```python
async def _consume(self) -> None:
    while True:
        msg = await self._queue.get()
        try:
            await self._client.publish(msg.topic, msg.payload)
        finally:
            self._queue.task_done()              # always; even on exception
```

`Queue.join()` waits for `task_done()` calls equal to puts. If a worker raises and skips `task_done()`, `join()` hangs forever on shutdown. Always pair `get()` with `task_done()` in a `finally`.

## Rule 7 — Choose: drop-newest, drop-oldest, or block

When `submit_or_drop` would drop, you have options:

| Strategy | Use when |
|----------|----------|
| Drop incoming | Default. Simplest. The caller knows about backpressure. |
| Drop oldest | Stale data is worse than missing data (e.g., metrics). Discard the front of the queue. |
| Block (await put) | Loss is unacceptable; latency degradation is. |

Drop-oldest pattern:

```python
async def submit_drop_oldest(self, msg: Message) -> None:
    if self._queue.full():
        try:
            old = self._queue.get_nowait()
            queue_dropped.add(1, {"reason": "drop_oldest", "topic": old.topic})
            self._queue.task_done()
        except asyncio.QueueEmpty:
            pass
    await self._queue.put(msg)
```

The race between `get_nowait` and `put` is acceptable — under contention the queue may briefly drop one extra; the metric still counts.

## Rule 8 — Document the policy at the public API

```python
async def submit(self, msg: Message) -> None:
    """Submit ``msg`` for publishing.

    Backpressure: if the internal queue is full, this method awaits until
    capacity frees up. Maximum wait is bounded by the consumer's drain rate;
    monitor ``motadata.publisher.queue_depth`` to verify backpressure is healthy.

    Raises:
        ValidationError: If ``msg.topic`` is empty.
    """
```

vs:

```python
def submit_or_drop(self, msg: Message) -> None:
    """Submit ``msg`` for publishing; raise BackpressureError if the queue is full.

    Use this method when the caller can tolerate dropped messages and prefers
    bounded latency over guaranteed delivery.

    Raises:
        ValidationError: If ``msg.topic`` is empty.
        BackpressureError: If the internal queue is full.
    """
```

The docstring's `Raises:` block discriminates the two. A consumer reading the API knows which method matches their tolerance.

## Rule 9 — Test backpressure under load

```python
async def test_drop_when_queue_full(monkeypatch) -> None:
    cfg = Config(..., queue_size=2, publisher_worker_count=0)  # zero workers; no drain
    async with StreamPublisher(cfg, client) as pub:
        pub.submit_or_drop(Message("topic", b"a"))
        pub.submit_or_drop(Message("topic", b"b"))
        with pytest.raises(BackpressureError):
            pub.submit_or_drop(Message("topic", b"c"))


async def test_block_when_queue_full() -> None:
    cfg = Config(..., queue_size=1, publisher_worker_count=1)  # one slow worker
    fake_client = SlowFakeClient(delay=0.5)
    async with StreamPublisher(cfg, fake_client) as pub:
        await pub.submit(Message("topic", b"a"))
        # Second submit blocks until first drains
        start = time.perf_counter()
        await pub.submit(Message("topic", b"b"))
        elapsed = time.perf_counter() - start
        assert 0.4 < elapsed < 0.6
```

The two tests prove the policy; without them, a future refactor can silently flip drop ↔ block.

## GOOD: full publisher class

```python
import asyncio
import contextlib
import logging
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Self

from opentelemetry import metrics

from motadatapysdk.errors import BackpressureError, MotadataError, ValidationError

logger = logging.getLogger(__name__)
meter = metrics.get_meter(__name__)
queue_dropped = meter.create_counter(
    "motadata.publisher.dropped",
    description="Messages dropped due to backpressure",
)


@dataclass(frozen=True, slots=True, kw_only=True)
class Message:
    topic: str
    payload: bytes


class StreamPublisher:
    """Buffered publisher with bounded queue + worker pool.

    Examples:
        >>> async def demo() -> None:
        ...     async with StreamPublisher(Config(...), client) as pub:
        ...         await pub.submit(Message(topic="orders", payload=b"x"))
        >>> asyncio.run(demo())  # doctest: +SKIP
    """

    def __init__(self, config: Config, client: Client) -> None:
        self._config = config
        self._client = client
        self._queue: asyncio.Queue[Message] = asyncio.Queue(
            maxsize=config.publisher_queue_size
        )
        self._workers: list[asyncio.Task[None]] = []
        self._closed = False

        meter.create_observable_gauge(
            "motadata.publisher.queue_depth",
            callbacks=[self._observe_depth],
            description="Pending messages",
        )

    async def __aenter__(self) -> Self:
        self._workers = [
            asyncio.create_task(self._consume(), name=f"publisher.worker.{i}")
            for i in range(self._config.publisher_worker_count)
        ]
        return self

    async def __aexit__(self, exc_type, exc_val, tb) -> None:
        if self._closed:
            return
        self._closed = True
        await self._queue.join()                 # drain pending
        for w in self._workers:
            w.cancel()
        await asyncio.gather(*self._workers, return_exceptions=True)

    async def submit(self, msg: Message) -> None:
        """Submit ``msg``; awaits until the queue has capacity (BLOCK)."""
        if not msg.topic:
            raise ValidationError("topic must not be empty")
        await self._queue.put(msg)

    def submit_or_drop(self, msg: Message) -> None:
        """Submit ``msg``; raise BackpressureError if the queue is full (DROP)."""
        if not msg.topic:
            raise ValidationError("topic must not be empty")
        try:
            self._queue.put_nowait(msg)
        except asyncio.QueueFull as e:
            queue_dropped.add(1, {"reason": "queue_full", "topic": msg.topic})
            raise BackpressureError(
                f"publisher queue is full ({self._config.publisher_queue_size} entries); "
                "increase publisher_queue_size or publisher_worker_count"
            ) from e

    async def _consume(self) -> None:
        while True:
            msg = await self._queue.get()
            try:
                await self._client.publish(msg.topic, msg.payload)
            except Exception as e:
                logger.warning("publish failed for %s: %s", msg.topic, e)
                # decide: re-enqueue (with care: infinite loop risk), drop, or DLQ
            finally:
                self._queue.task_done()

    def _observe_depth(self, options: metrics.CallbackOptions) -> Iterable[metrics.Observation]:
        yield metrics.Observation(self._queue.qsize())
```

Demonstrates: bounded queue (Rule 3), both submit shapes documented (Rule 8), worker pool (Rule 5), task_done in finally (Rule 6), queue-depth observable (Rule 4), graceful drain on close.

## BAD anti-patterns

```python
# 1. Unbounded queue
self._queue = asyncio.Queue()                   # silent OOM

# 2. Hardcoded maxsize
self._queue = asyncio.Queue(maxsize=1024)       # not Config-driven

# 3. No task_done
async def _consume(self):
    while True:
        msg = await self._queue.get()
        await process(msg)                       # no task_done; join() hangs

# 4. Drop without metric
try:
    self._queue.put_nowait(msg)
except asyncio.QueueFull:
    return                                       # silent; operator can't see drops

# 5. plain Semaphore(N) instead of BoundedSemaphore
sem = asyncio.Semaphore(N)                      # release imbalance not detected

# 6. Block AND drop in same method (caller can't tell which)
def submit(self, msg):
    if self._queue.full():
        return
    asyncio.create_task(self._queue.put(msg))   # BOTH dropping AND deferring

# 7. Worker that doesn't propagate exceptions
async def _consume(self):
    try:
        msg = await self._queue.get()
        await process(msg)
    except Exception:
        pass                                     # silent failures; operators blind

# 8. submit_or_drop returns success/failure as bool
def submit_or_drop(self, msg) -> bool:
    try:
        self._queue.put_nowait(msg); return True
    except asyncio.QueueFull:
        return False                             # caller forgets to check; data lost
# Use exceptions; "ignored bool" is a known bug magnet.

# 9. unbounded list as buffer
self._buffer: list[Message] = []
self._buffer.append(msg)                        # unbounded; OOM

# 10. Worker count > queue size
queue_size=4, worker_count=10                   # workers race; no useful concurrency
```

## Choosing `queue_size` and `worker_count`

A starting heuristic:

```
queue_size  = max(throughput_per_second × p99_latency_seconds × 2, 64)
worker_count = ceil(throughput_per_second × p50_latency_seconds)
```

Tune by watching `queue_depth` under realistic load:
- Depth at 0 most of the time → over-provisioned; reduce `worker_count`.
- Depth at `queue_size` most of the time → under-provisioned; raise `worker_count`.
- Depth oscillating from 0 to `queue_size` → bursty load; raise `queue_size`.

Document the heuristic in the Config docstring so consumers understand how to tune.

## Cross-references

- `python-asyncio-patterns` Rule 6 (Semaphore / Lock / Event), Rule 1 (TaskGroup for fan-out).
- `python-asyncio-leak-prevention` (worker tasks must be cancelled in `__aexit__`).
- `python-client-shutdown-lifecycle` (graceful drain pattern).
- `python-otel-instrumentation` (queue-depth observable + drop counter).
- `python-sdk-config-pattern` (queue_size + worker_count as Config fields).
- `python-exception-patterns` (`BackpressureError` extends `MotadataError`).
- `python-circuit-breaker-policy` — pairs with breaker for downstream failures.
- `idempotent-retry-safety` — drop policy presumes some workloads CAN tolerate loss.
