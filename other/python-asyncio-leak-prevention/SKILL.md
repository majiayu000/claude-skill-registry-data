---
name: python-asyncio-leak-prevention
description: >
  Use this when adding a Python SDK client class that holds long-lived async
  resources, reviewing code that discards an asyncio.create_task return value,
  designing pytest gates for shutdown, or chasing a ResourceWarning about an
  unclosed session/socket. Covers the leak categories L-A through L-E (tasks,
  aiohttp/asyncpg/aiokafka sessions, file/socket handles, custom executors,
  subprocess pipes), autouse asyncio_task_tracker + unclosed_session_tracker
  fixtures, fd_tracker via psutil, pytest-repeat --count=5 amplification,
  tracemalloc snapshot diffs, and threading.enumerate gates.
  Triggers: leak, asyncio, create_task, ClientSession, Connection, Pool, Producer, tracemalloc, gc, open file, file descriptor, asyncio_task_tracker, unclosed_session_tracker.
---

# python-asyncio-leak-prevention (v1.1.0)

## Rationale

An async Python SDK client has a wide leak surface: an `asyncio.Task` outlives the component that started it; an `aiohttp.ClientSession` keeps a connector pool with open sockets until garbage collection (which may be never under load); an `asyncpg.Connection` holds a server-side process; an unclosed `socket.socket` or `open()` file leaks a file descriptor. Each leak class has a different test gate. The pair `asyncio_task_tracker` + `unclosed_session_tracker` (custom pytest fixtures defined below) fail any test where either count grew across the test boundary.

Most leaks ship because the test suite never exercises shutdown. The discipline below makes shutdown a first-class test target.

This skill is cited by `sdk-asyncio-leak-hunter-python` (M7 + T6 audit catalog L-1 through L-9), `code-reviewer-python` (asyncio safety review-criteria), `refactoring-agent-python` (R-5 discarded create_task), `python-asyncio-patterns` (Rule 2 strong references), `python-client-shutdown-lifecycle` (close contract).

## Activation signals

- Adding a client class that holds long-lived resources.
- Code review surfaces `asyncio.create_task` whose return value is discarded.
- Code review surfaces `aiohttp.ClientSession()` or `asyncpg.create_pool()` without `__aexit__` cleanup.
- Test suite has no shutdown-leak gate.
- `sdk-asyncio-leak-hunter-python` emits a finding.
- A pytest run reports `ResourceWarning: unclosed <socket.socket ...>`.

## Leak categories

### L-A. Asyncio task leaks

A `Task` is leaked when it's still running (or pending) after the SDK component that started it has been closed. Common sources:

1. `asyncio.create_task(coro())` — return value discarded; task can be GC'd mid-execution OR run forever depending on the body.
2. Background keepalive / heartbeat task spawned in `__aenter__` but not cancelled in `__aexit__`.
3. Fan-out task spawned outside a `TaskGroup` whose lifetime exceeds the parent context.
4. `asyncio.ensure_future(...)` whose return value is dropped.

**Fix pattern**:

```python
class Client:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._keepalive_task: asyncio.Task[None] | None = None

    async def __aenter__(self) -> Client:
        self._keepalive_task = asyncio.create_task(
            self._keepalive(),
            name="motadata.client.keepalive",   # name for pytest tracker
        )
        return self

    async def __aexit__(self, exc_type, exc_val, tb) -> None:
        if self._keepalive_task is not None:
            self._keepalive_task.cancel()
            try:
                await self._keepalive_task
            except asyncio.CancelledError:
                pass
            self._keepalive_task = None
```

`name=` is critical — the pytest task tracker uses the name to ATTRIBUTE leaks ("the leaked task is `motadata.client.keepalive`"). Unnamed tasks are reported as `Task-12` and the fix becomes a hunt.

### L-B. Unclosed `aiohttp.ClientSession` / similar

aiohttp emits `ResourceWarning: Unclosed client session` on garbage collection. The session keeps a connector pool with open sockets until GC sweeps it — which may be never under heavy load.

**Fix pattern**:

```python
class Client:
    async def __aenter__(self) -> Client:
        timeout = aiohttp.ClientTimeout(total=self._config.timeout_s)
        self._session = aiohttp.ClientSession(timeout=timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, tb) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None
```

aiohttp + asyncpg + aiokafka + motor all have analogous `close()` / `terminate()` requirements. Document each in your component's docstring.

### L-C. Unclosed file handles / sockets

```python
# WRONG — file leaks if read raises
f = open("config.json", "rb")
data = f.read()
f.close()

# RIGHT — context manager
with open("config.json", "rb") as f:
    data = f.read()

# RIGHT (async) — aiofiles
async with aiofiles.open("config.json", "rb") as f:
    data = await f.read()
```

**Sockets**:

```python
# WRONG
s = socket.socket(...)
s.connect(...)
s.send(b"...")
s.close()                      # leaks if send raises

# RIGHT — context manager (3.x supports it)
with socket.socket(...) as s:
    s.connect(...)
    s.send(b"...")
```

For long-lived sockets owned by an async client, the close lives in `__aexit__`.

### L-D. Threads spawned via `loop.run_in_executor`

A custom executor must be shut down at client close:

```python
class Client:
    def __init__(self, config: Config) -> None:
        self._executor: concurrent.futures.ThreadPoolExecutor | None = None

    async def __aenter__(self) -> Client:
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self._config.executor_workers,
            thread_name_prefix="motadata-blocking",
        )
        return self

    async def __aexit__(self, exc_type, exc_val, tb) -> None:
        if self._executor is not None:
            self._executor.shutdown(wait=True, cancel_futures=True)
            self._executor = None
```

`asyncio.to_thread(...)` uses the default loop executor — that's a process-wide pool managed by the loop and shut down with it. Custom executors are the SDK's responsibility.

### L-E. Subprocess handles

`asyncio.create_subprocess_exec` returns a Process whose `transport` and pipes must be closed:

```python
async def _run(self, *args: str) -> bytes:
    proc = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, _stderr = await proc.communicate()
    finally:
        if proc.returncode is None:
            proc.kill()
            await proc.wait()
    return stdout
```

`communicate()` reads pipes to EOF, which closes them. If you `read()` partial output and skip `communicate()`, the pipes leak.

## Test gates

### Gate 1 — `asyncio_task_tracker` fixture (autouse — NON-NEGOTIABLE)

Drop-in conftest fixture that fails any test where the running-task count grew. **The `autouse=True` decoration is non-negotiable.** A non-autouse leak fixture is a no-op for every test that does not name it explicitly; the leak guarantee is forfeited the moment a single test forgets to list it. The whole point of leak-tracking is that it runs even on tests the author did not write *for* leak coverage.

Authored once at `tests/conftest.py`:

```python
# tests/conftest.py
import asyncio
import pytest

@pytest.fixture(autouse=True)                        # MUST be autouse=True
async def asyncio_task_tracker(request) -> AsyncIterator[None]:
    """Fail the test if it leaks any asyncio task.

    A leak is defined as: a Task that was not present at test start and
    is still running (not Done()) at test end.
    """
    if request.node.get_closest_marker("no_task_tracker"):
        # Explicit opt-out for tests that legitimately leave tasks running.
        yield
        return
    before = {t for t in asyncio.all_tasks() if not t.done()}
    yield
    # Give the loop one tick to drain pending cancellations the test fired.
    await asyncio.sleep(0)
    after = {t for t in asyncio.all_tasks() if not t.done()}
    leaked = after - before
    if leaked:
        names = sorted(t.get_name() for t in leaked)
        pytest.fail(f"asyncio task leak: {len(leaked)} task(s): {names}", pytrace=False)
```

Plumb the opt-out marker so `pytest --strict-markers` recognizes it:

```toml
# pyproject.toml
[tool.pytest.ini_options]
markers = [
    "no_task_tracker: opt out of asyncio_task_tracker autouse leak gate (rare)",
]
```

#### BAD — non-autouse fixture (a no-op for every test that does not name it)

```python
# tests/conftest.py — DO NOT DO THIS
import asyncio
import pytest

@pytest.fixture                                       # MISSING autouse=True
async def asyncio_task_tracker() -> AsyncIterator[None]:
    before = {t for t in asyncio.all_tasks() if not t.done()}
    yield
    await asyncio.sleep(0)
    after = {t for t in asyncio.all_tasks() if not t.done()}
    leaked = after - before
    if leaked:
        pytest.fail(f"asyncio task leak: {sorted(t.get_name() for t in leaked)}")
```

```python
# tests/test_publish.py — silently runs WITHOUT the leak gate
async def test_publish_happy_path():
    async with Client(cfg) as c:
        await c.publish("topic", b"x")
    # If publish() spawned a discarded background task, the leak is invisible:
    # this test never named asyncio_task_tracker as a fixture parameter.
```

Defect SKD-001 in run `sdk-resourcepool-py-pilot-v1` shipped exactly this pattern — `tests/conftest.py:26` defined `asyncio_task_tracker` without `autouse=True`. 59/62 tests in the suite ran completely unguarded against the leak class this skill exists to prevent. The fixture body was identical to the GOOD form below; the missing `autouse=True` decoration was the only delta, and it nullified the entire gate.

#### GOOD — autouse=True with opt-out marker plumbing

```python
# tests/conftest.py
import asyncio
import pytest

@pytest.fixture(autouse=True)                        # required
async def asyncio_task_tracker(request) -> AsyncIterator[None]:
    if request.node.get_closest_marker("no_task_tracker"):
        yield
        return
    before = {t for t in asyncio.all_tasks() if not t.done()}
    yield
    await asyncio.sleep(0)
    after = {t for t in asyncio.all_tasks() if not t.done()}
    leaked = after - before
    if leaked:
        names = sorted(t.get_name() for t in leaked)
        pytest.fail(f"asyncio task leak: {len(leaked)} task(s): {names}", pytrace=False)
```

```python
# tests/test_publish.py — automatically guarded
async def test_publish_happy_path():
    async with Client(cfg) as c:
        await c.publish("topic", b"x")
    # asyncio_task_tracker runs regardless of whether the test mentions it.

# tests/test_long_running.py — explicit, marker-gated opt-out
@pytest.mark.no_task_tracker
async def test_long_running_observer_thread():
    # Legitimately starts a task that outlives the test (rare; document why).
    asyncio.create_task(observer_loop(), name="observer")
```

The opt-out is intentionally verbose — the marker name + docstring forces the author to acknowledge they are forfeiting the leak gate for that one test. **A non-autouse leak fixture is a no-op for every test that does not name it; the leak guarantee is forfeited.**

### Gate 2 — `unclosed_session_tracker` fixture

Catches the `ResourceWarning: Unclosed client session` class of leak. aiohttp / asyncpg / aiokafka all emit `ResourceWarning` on `__del__` when not closed; we promote that warning to a test failure:

```python
import warnings
import pytest

@pytest.fixture(autouse=True)
def unclosed_session_tracker(recwarn: pytest.WarningsRecorder) -> Iterator[None]:
    """Fail the test if any ResourceWarning fires."""
    with warnings.catch_warnings():
        warnings.simplefilter("error", category=ResourceWarning)
        yield
```

`warnings.simplefilter("error", ...)` upgrades the warning to an exception. The first leaked session terminates the test with a stack trace pointing at the leak site.

### Gate 3 — gc + open_fds scan

For tests of full client lifecycle, count open file descriptors before and after:

```python
import os
import gc
import psutil

@pytest.fixture
def fd_tracker() -> Iterator[None]:
    proc = psutil.Process()
    gc.collect()
    fds_before = proc.num_fds() if hasattr(proc, "num_fds") else len(proc.open_files())
    yield
    gc.collect()
    fds_after = proc.num_fds() if hasattr(proc, "num_fds") else len(proc.open_files())
    if fds_after > fds_before:
        pytest.fail(f"file descriptor leak: {fds_before} → {fds_after}", pytrace=False)
```

Run on Linux (`num_fds`); on macOS use `psutil.Process().open_files()`. Skip on Windows where `num_fds` is unavailable.

### Gate 4 — pytest-repeat --count=5

Some leaks fire on iteration 7 of 10, not iteration 1. Run leak-targeted tests with `pytest-repeat`:

```bash
pytest tests/leak/ --count=5 -p no:randomly
```

The `-p no:randomly` keeps the same execution order so failures are reproducible.

`sdk-asyncio-leak-hunter-python` runs this in its T6 wave (count=5) and a more aggressive variant for severity isolation (count=10).

### Gate 5 — Tracemalloc snapshot diff

For memory leaks (objects not released after close), snapshot before/after a full lifecycle:

```python
import tracemalloc

async def test_client_lifecycle_no_growth() -> None:
    tracemalloc.start(25)              # 25-frame stack depth
    snap_before = tracemalloc.take_snapshot()

    # Exercise full lifecycle 100x
    for _ in range(100):
        async with Client(Config(...)) as c:
            await c.publish("topic", b"x")

    gc.collect()
    snap_after = tracemalloc.take_snapshot()
    stats = snap_after.compare_to(snap_before, "lineno")

    growth = sum(stat.size_diff for stat in stats if stat.size_diff > 0)
    assert growth < 1024 * 1024, f"memory growth {growth} bytes after 100 lifecycles"
    tracemalloc.stop()
```

The threshold (1 MiB above) is a heuristic; calibrate per client. Real leaks compound across iterations, so 100 iterations amplify a 1 KB/iter leak into a visible 100 KB delta.

## Class catalog (mirrors `sdk-asyncio-leak-hunter-python` audit catalog L-1 through L-9)

| Code | Pattern | Test gate |
|------|---------|-----------|
| L-1 | Discarded `create_task` return | task_tracker |
| L-2 | Background task without `__aexit__` cancel | task_tracker |
| L-3 | Unclosed `aiohttp.ClientSession` | session_tracker |
| L-4 | Unclosed `asyncpg.Connection` / `Pool` | session_tracker |
| L-5 | Unclosed `aiokafka.AIOKafkaProducer` | session_tracker |
| L-6 | Unclosed file via `open()` (no `with`) | fd_tracker |
| L-7 | Unclosed socket via `socket.socket()` (no `with`) | fd_tracker |
| L-8 | Custom ThreadPoolExecutor not shut down | thread_tracker (via `threading.enumerate()`) |
| L-9 | Subprocess pipes left open after partial read | fd_tracker |

## GOOD: full leak-clean lifecycle test

```python
# tests/leak/test_client_shutdown.py
import asyncio
import pytest
from motadatapysdk import Client, Config

pytestmark = pytest.mark.leak_hunt

async def test_client_shutdown_no_task_leak(asyncio_task_tracker, unclosed_session_tracker, fd_tracker):
    """Full client lifecycle leaves no leaked task/session/fd."""
    cfg = Config(base_url="http://localhost:65535", api_key="x", timeout_s=0.1)

    async with Client(cfg) as client:
        # The body may fail (port not listening) — that's fine; we test cleanup.
        with contextlib.suppress(Exception):
            await client.publish("topic", b"x")

    # Implicit asserts via autouse fixtures
```

The combination — task_tracker + session_tracker + fd_tracker + suppress — exercises shutdown over the EXCEPTION path. Most leaks ship because the test only exercises the happy path.

## Threading enumeration

For SDK code that spawns threads:

```python
import threading

@pytest.fixture(autouse=True)
def thread_tracker() -> Iterator[None]:
    before = {t.name for t in threading.enumerate() if t.is_alive()}
    yield
    after = {t.name for t in threading.enumerate() if t.is_alive()}
    leaked = after - before
    # Filter out daemon threads from the test runner itself
    leaked = {n for n in leaked if not n.startswith(("MainThread", "asyncio_"))}
    if leaked:
        pytest.fail(f"thread leak: {sorted(leaked)}")
```

Custom thread names via `threading.Thread(name="motadata-...")` make the failure attributable. ThreadPoolExecutor's `thread_name_prefix=` (see L-D) covers executor-spawned threads.

## BAD anti-patterns

```python
# 1. Discarded create_task
asyncio.create_task(self._heartbeat())          # L-1

# 2. Session without context
self._session = aiohttp.ClientSession()         # forgot __aexit__ close

# 3. Manual close on success only
self._session = aiohttp.ClientSession()
try:
    await self._do_thing()
    await self._session.close()                  # exception path leaks
except Exception:
    raise                                        # session never closed

# 4. Forgot to wait on cancelled task
self._task.cancel()                              # not awaited; warning suppressed
                                                 # next gc may emit "Task was destroyed but it is pending"

# 5. open() without with
config = json.load(open("config.json"))         # leaks fd

# 6. Custom executor without shutdown
self._exec = ThreadPoolExecutor(max_workers=4)  # never .shutdown(); leaks workers

# 7. Subprocess without communicate / kill
proc = await asyncio.create_subprocess_exec(...)
data = await proc.stdout.read(100)              # partial; pipes leak

# 8. test missing leak fixtures
async def test_publish():
    async with Client(...) as c:
        await c.publish("t", b"x")              # no autouse fixtures = leak invisible
```

## Cross-references

- `python-asyncio-patterns` Rule 2 — strong-ref to Tasks; Rule 4 — cancellation safety.
- `python-client-shutdown-lifecycle` — full close() contract; idempotency; ordered teardown.
- `python-pytest-patterns` Rule 4 — fixture `yield` for cleanup.
- `sdk-asyncio-leak-hunter-python` — M7 + T6 wave that runs the gates.
- `sdk-soak-runner-python` — long-running drift detection for slow leaks.
