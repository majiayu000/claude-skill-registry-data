---
name: performance-profiling
description: Profile and optimize Python/Node.js — cProfile, py-spy, clinic.js, memory profiling, async bottlenecks, DB query analysis
triggers:
  - performance profiling
  - profile python
  - profile nodejs
  - cprofile
  - py-spy
  - memory leak python
  - memory profiling
  - slow query analysis
  - performance bottleneck
  - async performance
  - optimize python
do_not_use_for:
  - frontend performance — use web-performance skill
  - load testing — use k6/locust
  - error debugging — use error-handling-patterns
see_also:
  - ai-code-maintainability
  - logging-observability
  - web-performance
---

# Performance Profiling

## Python: cProfile (CPU)

```bash
# Profile entire script
python -m cProfile -s cumulative -o profile.prof my_script.py

# Visualize with snakeviz
pip install snakeviz
snakeviz profile.prof
```

```python
import cProfile
import pstats
from pstats import SortKey

# Profile a specific function
profiler = cProfile.Profile()
profiler.enable()
result = slow_function(data)
profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats(SortKey.CUMULATIVE)
stats.print_stats(20)   # top 20 functions by cumulative time
```

## Python: py-spy (Production-safe sampling)

```bash
# Install
pip install py-spy

# Profile running process without restarting
py-spy top --pid 12345              # live top-style view
py-spy record -o profile.svg --pid 12345  # flame graph
py-spy dump --pid 12345             # one-time stack dump

# Profile from start
py-spy record -o profile.svg -- python my_script.py
```

## Python: Memory Profiling

```python
# tracemalloc — built-in, no overhead when not active
import tracemalloc

tracemalloc.start()
# ... run code ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics("lineno")
for stat in top_stats[:10]:
    print(stat)

# memory-profiler — line-by-line
pip install memory-profiler
from memory_profiler import profile

@profile
def process_large_file(path: str) -> None:
    with open(path) as f:
        data = f.read()      # see how much memory this line uses
    process(data)
```

## Python: Async Bottlenecks

```python
import asyncio
import time

# Find which coroutine is slow
async def timed(coro, label: str):
    start = time.perf_counter()
    result = await coro
    elapsed = time.perf_counter() - start
    if elapsed > 0.1:   # log slow coroutines
        print(f"SLOW [{label}]: {elapsed:.3f}s")
    return result

# Profile concurrent tasks
async def main():
    tasks = [
        timed(fetch_user(uid), f"fetch_user({uid})")
        for uid in user_ids
    ]
    results = await asyncio.gather(*tasks)

# Detect event loop blocking
import asyncio

async def detect_blocking(threshold: float = 0.05):
    """Alert if anything blocks the event loop > 50ms."""
    while True:
        t0 = time.perf_counter()
        await asyncio.sleep(0)   # yield to event loop
        elapsed = time.perf_counter() - t0
        if elapsed > threshold:
            print(f"Event loop blocked for {elapsed:.3f}s!")
```

## DB Query Analysis

```python
# SQLAlchemy: log all queries with timing
import logging
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Or use sqlalchemy-utils query profiler
from sqlalchemy_utils import QueryChain

with QueryChain() as qc:
    users = session.execute(select(User)).scalars().all()

print(f"Queries: {qc.count}, Total: {qc.total_time:.3f}s")
for q in qc.queries:
    print(f"  {q.duration:.3f}s — {q.statement[:80]}")

# EXPLAIN ANALYZE for slow queries (PostgreSQL)
from sqlalchemy import text

result = session.execute(text(
    "EXPLAIN ANALYZE SELECT * FROM users WHERE email = :email"
), {"email": "test@example.com"})
for row in result:
    print(row[0])
```

## Node.js: clinic.js

```bash
# Install
npm install -g clinic

# Doctor — quick diagnosis
clinic doctor -- node server.js

# Flame graph — CPU profiling
clinic flame -- node server.js

# Bubble — event loop delays
clinic bubbleprof -- node server.js
```

## Quick Win Checklist

```python
# 1. Avoid repeated attribute lookups in tight loops
# ❌ Slow
for item in items:
    result = self.config.timeout * self.config.multiplier   # 2 lookups per iter

# ✅ Cache outside loop
timeout = self.config.timeout
multiplier = self.config.multiplier
for item in items:
    result = timeout * multiplier

# 2. Use generators for large sequences
# ❌ Creates entire list in memory
data = [transform(x) for x in large_file]

# ✅ Stream processing
data = (transform(x) for x in large_file)

# 3. String concatenation in loops
# ❌ O(n²) — creates new string each iteration
result = ""
for chunk in chunks:
    result += chunk

# ✅ O(n) — join at end
result = "".join(chunks)

# 4. Set/dict lookups vs list membership
# ❌ O(n) per check
allowed = ["admin", "editor", "viewer"]
if role in allowed:

# ✅ O(1) per check
ALLOWED_ROLES = frozenset({"admin", "editor", "viewer"})
if role in ALLOWED_ROLES:
```

## Anti-Fake-Pass Checks

- cProfile adds overhead — don't profile micro-benchmarks with it, use `timeit` instead
- py-spy requires `--sudo` for other user processes on Linux
- Memory profiler `@profile` decorator slows code significantly — remove in prod
- `asyncio.gather()` parallelizes I/O, not CPU — use `ProcessPoolExecutor` for CPU-bound
- "EXPLAIN ANALYZE" actually runs the query — don't use on destructive queries
- Flame graphs show wall clock time — CPU flame graphs only show CPU time, not I/O waits
