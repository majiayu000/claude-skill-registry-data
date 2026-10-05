---
name: python-typing-and-async
description: "Type hints are checked by a separate tool (`mypy`, `pyright`), never by CPython"
---

# Python Typing And Async (Verbose)

## Core Patterns

### Type The Boundaries

Type hints are checked by a separate tool (`mypy`, `pyright`), never by CPython
at runtime. Their value is proportional to how much a tool can prove. Annotate
public signatures, return types, and data structures; leave obvious locals bare.

```python
def group_by_role(users: list[User]) -> dict[str, list[User]]:
    out: dict[str, list[User]] = {}      # annotate: the checker can't infer empty
    for u in users:
        out.setdefault(u["role"], []).append(u)
    return out
```

Enable strict mode in CI. Without enforcement, hints drift out of sync with the
code and become misleading comments.

### Protocol vs ABC

Use a `Protocol` for a contract satisfied by shape, and an abstract base class
only when you also want to share implementation or force explicit registration.

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...

def cleanup(res: Closeable) -> None:
    res.close()          # files, sockets, DB connections all satisfy this
```

A `Protocol` needs no cooperation from the classes it matches — third-party
types conform automatically if the methods line up. That is the point.

### TypedDict For Payload Shapes

```python
from typing import TypedDict, NotRequired

class Order(TypedDict):
    id: int
    total: float
    coupon: NotRequired[str]     # key may be absent (3.11+)

def summarize(o: Order) -> str:
    base = f"#{o['id']}: {o['total']}"
    return base + (f" ({o['coupon']})" if "coupon" in o else "")
```

`TypedDict` documents and checks a dict's keys without forcing a class or a
serialization step — ideal for JSON at the edges of a system.

### Literal And Narrowing

```python
from typing import Literal

Mode = Literal["r", "w", "a"]

def opener(mode: Mode) -> None:
    if mode == "r":
        ...              # inside this branch the checker knows mode == "r"
    else:
        reveal_type(mode)   # Literal["w", "a"]
```

Combine `Literal` with narrowing to make illegal states unrepresentable — a
typo like `"read"` fails the check at the call site.

### Generics And Bounds

```python
from typing import TypeVar

Num = TypeVar("Num", bound=float)   # int and float both count

def clamp(x: Num, lo: Num, hi: Num) -> Num:
    return max(lo, min(x, hi))
```

PEP 695 gives lighter syntax on 3.12+:

```python
def first[T](xs: list[T]) -> T | None:
    return xs[0] if xs else None
```

Generics keep the concrete type flowing through the call, so `first([1, 2])` is
`int | None`, not `object`.

### The Event Loop

`asyncio` runs a single-threaded event loop. `await` on an awaitable suspends the
current coroutine and hands control back to the loop, which runs another ready
task. Nothing is preemptive: a coroutine keeps the loop until it awaits.

```python
import asyncio

async def worker(name: str, delay: float) -> str:
    await asyncio.sleep(delay)     # suspension point — loop runs others here
    return f"{name} done"

async def main() -> None:
    async with asyncio.TaskGroup() as tg:
        for i in range(3):
            tg.create_task(worker(f"w{i}", i * 0.1))

asyncio.run(main())
```

### Keeping Blocking Work Off The Loop

A synchronous call has no suspension point, so it blocks the entire loop until it
returns. Offload it:

```python
import hashlib

# CPU-bound or legacy blocking I/O
digest = await asyncio.to_thread(hashlib.sha256, big_bytes)
```

`to_thread` runs the callable in a worker thread and awaits it — the loop stays
responsive. For CPU-bound work, threads still contend on the GIL; use a process
pool instead.

### gather vs TaskGroup

```python
# gather — ordered results, but a raised exception leaves siblings running
a, b = await asyncio.gather(fetch(1), fetch(2))

# TaskGroup — if any task fails, the rest are cancelled and errors surface together
async with asyncio.TaskGroup() as tg:
    t1 = tg.create_task(fetch(1))
    t2 = tg.create_task(fetch(2))
result = t1.result(), t2.result()
```

### The GIL And Choosing A Concurrency Model

The Global Interpreter Lock serializes execution of Python bytecode: one thread
at a time. This shapes the choice of tool:

| Workload | Tool | Why |
|---|---|---|
| Network / disk I/O | `asyncio` | Waiting releases the GIL; thousands of coroutines on one thread |
| Blocking library I/O | threads / `to_thread` | GIL released during the blocking syscall |
| Pure CPU computation | `multiprocessing` | Separate interpreters run truly in parallel |

Reaching for threads to accelerate a number-crunching loop is the classic
mistake — the GIL prevents the parallelism you were hoping for. See the
`python-runtime` skill for GIL internals and memory management.

## Common Anti-Patterns

❌ **`Any` to silence the checker**
```python
def load(path) -> Any:      # everything downstream is now unchecked
    return json.load(open(path))
```
✅ **Type the real shape**
```python
def load(path: str) -> dict[str, object]:
    with open(path) as f:
        return json.load(f)
```

❌ **Blocking calls inside a coroutine**
```python
async def get(url):
    return requests.get(url).json()   # freezes the loop for every caller
```
✅ **Use an async client, or offload**
```python
async def get(url):
    async with httpx.AsyncClient() as c:
        return (await c.get(url)).json()
```

❌ **Fire-and-forget tasks that swallow errors**
```python
asyncio.create_task(sync_to_remote())   # exception vanishes if never awaited
```
✅ **Own the task in a TaskGroup**
```python
async with asyncio.TaskGroup() as tg:
    tg.create_task(sync_to_remote())    # failure propagates
```

❌ **Threads for CPU-bound parallelism**
```python
with ThreadPoolExecutor() as ex:        # GIL serializes the work anyway
    ex.map(crunch, chunks)
```
✅ **Processes for CPU work**
```python
with ProcessPoolExecutor() as ex:
    ex.map(crunch, chunks)
```

## Typing And Async Checklist

- [ ] Public signatures and data shapes annotated; trivial locals left bare
- [ ] `mypy --strict` or `pyright` runs in CI, not just locally
- [ ] `Protocol` used for shape-based contracts instead of forced inheritance
- [ ] `TypedDict` / `Literal` express payload shapes and closed value sets
- [ ] Generics used so element types survive the call
- [ ] No `Any` added purely to mute the checker
- [ ] No blocking I/O, `time.sleep`, or CPU loops inside coroutines
- [ ] `asyncio.to_thread` / process pool for unavoidable blocking work
- [ ] `TaskGroup` preferred over bare `gather` for structured cancellation
- [ ] Concurrency model matches workload: async/threads for I/O, processes for CPU
- [ ] No un-awaited coroutines (watch the `RuntimeWarning`)
