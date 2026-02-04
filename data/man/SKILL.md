---
name: python-performance
description: Use when Python code runs slowly, needs profiling, requires async/await patterns, or needs concurrent execution - covers profiling tools, optimization patterns, and asyncio; measure before optimizing (plugin:python@dot-claude)
allowed-tools: Bash(python:*), Read, Write, Edit
---

# Python Performance & Concurrency

Profiling, optimization, and async patterns for Python.

## Before Writing Code

1. Read `references/pythonic-style.md` for style conventions
2. Check Python version: 3.13+ enables free-threaded concurrency options
3. **Profile before optimizing** - never guess at bottlenecks

## Reference Files

| Topic | When to Load | File |
|-------|--------------|------|
| Pythonic style | Before generating code | `../references/pythonic-style.md` |
| Semaphores, locks, producers/consumers | Advanced async | `references/async-advanced.md` |
| Database, memory, NumPy optimization | Deep optimization | `references/optimization-advanced.md` |

## Profiling First

### cProfile (CPU)

```bash
python -m cProfile -o output.prof script.py
python -m pstats output.prof  # Interactive analysis
```

```python
import cProfile
import pstats

with cProfile.Profile() as pr:
    main()

stats = pstats.Stats(pr)
stats.sort_stats("cumulative").print_stats(10)
```

### line_profiler (Line-by-Line)

```bash
uv add line-profiler
kernprof -l -v script.py  # Requires @profile decorator
```

### py-spy (Production)

```bash
py-spy record -o profile.svg -- python script.py
py-spy top --pid 12345  # Live profiling
```

### memory_profiler

```bash
uv add memory-profiler
python -m memory_profiler script.py  # Requires @profile decorator
```

## Concurrency Pattern Selection

| Workload | Solution |
|----------|----------|
| I/O-bound (network, disk) | `async`/`await` |
| CPU-bound (GIL Python) | `multiprocessing` |
| CPU-bound (nogil 3.13+) | `threading` |
| Mixed | async + ProcessPoolExecutor |

## Async/Await Patterns

### Basic Async

```python
import asyncio

async def fetch_data(url: str) -> dict:
    await asyncio.sleep(1)  # Simulates I/O
    return {"url": url, "data": "result"}

async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

asyncio.run(main())
```

### Concurrent Execution

```python
async def fetch_all(urls: list[str]) -> list[dict]:
    # Concurrent I/O eliminates sequential waiting: 10 URLs at 100ms each
    # complete in ~100ms total, not 1000ms. Critical for API aggregation.
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)
```

### Error Handling

```python
async def safe_fetch(url: str) -> dict | None:
    try:
        return await fetch_data(url)
    except Exception as e:
        print(f"Error: {e}")
        return None

async def fetch_with_errors(urls: list[str]):
    results = await asyncio.gather(
        *[safe_fetch(url) for url in urls],
        return_exceptions=True  # Don't fail on first error
    )
    return [r for r in results if r and not isinstance(r, Exception)]
```

### Timeouts

```python
try:
    result = await asyncio.wait_for(slow_operation(), timeout=5.0)
except asyncio.TimeoutError:
    print("Operation timed out")
```

## Async Pitfalls

```python
# WRONG: Forgetting await
result = async_function()  # Returns coroutine, doesn't execute!

# WRONG: Blocking the event loop
import time
async def bad():
    time.sleep(1)  # Blocks everything!

# CORRECT
async def good():
    await asyncio.sleep(1)  # Non-blocking

# WRONG: Calling async from sync
def sync_func():
    result = await async_func()  # SyntaxError!

# CORRECT
def sync_func():
    result = asyncio.run(async_func())
```

## Optimization Patterns

### Data Structures

```python
# Sets use hash tables for O(1) membership testing. For collections
# checked repeatedly or exceeding ~10 items, the overhead of hashing
# pays off vs linear scanning.
if item in items_list:  # O(n) - scans every element
if item in items_set:   # O(1) - hash lookup

# String immutability in Python forces reallocation on every +=.
# For N concatenations, this creates O(n²) total copying.
# join() pre-calculates final size and allocates once.
result = ""
for s in strings:
    result += s  # Creates N intermediate string objects

result = "".join(strings)  # Single allocation, O(n) total
```

### List Comprehensions

```python
# List comprehensions bypass method dispatch overhead (no .append lookup)
# and CPython pre-sizes the result list. For simple transforms, prefer
# comprehensions unless loop body requires complex logic or side effects.
result = []
for i in range(n):
    result.append(i**2)  # Method lookup + call per iteration

result = [i**2 for i in range(n)]  # Optimized bytecode path
```

### Generators for Memory

```python
import sys

list_data = [i for i in range(1_000_000)]  # ~8MB in memory
gen_data = (i for i in range(1_000_000))   # ~100 bytes (lazy evaluation)

# Generators yield values on-demand, preventing memory exhaustion when
# processing data larger than available RAM. Essential for log parsing,
# ETL pipelines, or any single-pass data processing.
def process_large_file(path):
    with open(path) as f:
        for line in f:  # File iterator is itself a generator
            yield process(line)
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    # Cached: subsequent calls with same n return instantly
    return sum(i**2 for i in range(n))

# Clear cache if needed
expensive_computation.cache_clear()
```

### Local Variables

```python
# Python's LEGB resolution requires dictionary lookups for global/nonlocal
# variables, but uses direct array indexing for locals. In tight loops with
# 10k+ iterations, this overhead compounds significantly.
GLOBAL = 100
def slow():
    for i in range(10000):
        x = GLOBAL * i  # Dict lookup each iteration

def fast():
    local = 100  # Captured once at function entry
    for i in range(10000):
        x = local * i  # Direct array index
```

## Multiprocessing (CPU-Bound)

```python
import multiprocessing as mp

def cpu_task(n: int) -> int:
    return sum(i**2 for i in range(n))

if __name__ == "__main__":
    with mp.Pool(4) as pool:
        results = pool.map(cpu_task, [1_000_000] * 4)
```

## Async + Sync Integration

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

def cpu_bound(n: int) -> int:
    return sum(i**2 for i in range(n))

async def main():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_bound, 1_000_000)
    print(result)

asyncio.run(main())
```

## Testing Async Code

```python
import pytest

@pytest.mark.asyncio
async def test_fetch():
    result = await fetch_data("https://api.example.com")
    assert result is not None

@pytest.mark.asyncio
async def test_timeout():
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_operation(), timeout=0.1)
```

## Benchmarking

```python
import timeit

# Quick benchmark
time = timeit.timeit(lambda: my_function(), number=1000)
print(f"{time:.4f}s for 1000 runs")

# pytest-benchmark (uv add --dev pytest-benchmark)
def test_performance(benchmark):
    result = benchmark(my_function)
    assert result is not None
```

## Workflow Integration

| Task | Skill |
|------|-------|
| Writing async tests | `python:python-testing` |
| Root cause analysis | `debug:systematic` |
| Before claiming done | `core:verification` |

## Best Practices

1. **Profile before optimizing** - find real bottlenecks
2. **Use async for I/O** - network, disk, databases
3. **Use multiprocessing for CPU** - heavy computation
4. **Consider nogil (3.13+)** - threading for CPU-bound
5. **Use appropriate data structures** - set/dict for lookups
6. **Cache expensive operations** - lru_cache
7. **Use generators** - for large data iteration
8. **Avoid blocking in async** - no time.sleep()
9. **Handle cancellation** - catch CancelledError
10. **Benchmark changes** - prove improvement
