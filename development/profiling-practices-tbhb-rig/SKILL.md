---
name: profiling-practices
description: Performance profiling best practices using py-spy and other Python profiling tools. Activated when profiling code, analyzing bottlenecks, or optimizing performance.
---

# Profiling practices

## Purpose

Guide for performance profiling using py-spy, cProfile, and other Python profiling tools. Covers CPU profiling, memory profiling, and flame graph analysis.

## When to use

This skill activates when:

- Identifying performance bottlenecks
- Profiling CPU usage
- Analyzing memory consumption
- Creating flame graphs
- Optimizing hot paths

## Core principles

### Profile before optimizing

- NEVER guess where bottlenecks are
- Always measure before and after changes
- Focus optimization on actual hot paths

### Use the right tool

- py-spy for sampling-based profiling
- cProfile for deterministic profiling
- tracemalloc for memory profiling

## CPU profiling with py-spy

### Record profile to file

```bash
# Create flame graph SVG
uv run py-spy record -o profile.svg -- python script.py

# Create speedscope JSON
uv run py-spy record -o profile.json --format speedscope -- python script.py
```

### Live process profiling

```bash
# Top-like view
uv run py-spy top -- python script.py

# Attach to running process
uv run py-spy top --pid 12345
```

### Record options

```bash
# Increase sampling rate
uv run py-spy record --rate 250 -o profile.svg -- python script.py

# Include native frames
uv run py-spy record --native -o profile.svg -- python script.py

# Subprocesses too
uv run py-spy record --subprocesses -o profile.svg -- python script.py
```

## CPU profiling with cProfile

### Basic profiling

```bash
# Run with profiler
uv run python -m cProfile -o profile.prof script.py

# Sort by cumulative time
uv run python -m cProfile -s cumulative script.py
```

### Analyze results

```python
import pstats

# Load and analyze
p = pstats.Stats('profile.prof')
p.sort_stats('cumulative')
p.print_stats(20)  # Top 20 functions

# Filter by function name
p.print_stats('process')
```

### Profile specific code

```python
import cProfile
import pstats

def profile_function(func):
    """Decorator to profile a function."""
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)

        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)

        return result
    return wrapper
```

## Memory profiling

### With tracemalloc

```python
import tracemalloc

# Start tracing
tracemalloc.start()

# Run code to profile
result = process_large_data()

# Get snapshot
snapshot = tracemalloc.take_snapshot()

# Print top memory consumers
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

### Comparing snapshots

```python
import tracemalloc

tracemalloc.start()

# First snapshot
process_step1()
snapshot1 = tracemalloc.take_snapshot()

# Second snapshot
process_step2()
snapshot2 = tracemalloc.take_snapshot()

# Compare
top_stats = snapshot2.compare_to(snapshot1, 'lineno')
for stat in top_stats[:10]:
    print(stat)
```

## Flame graph analysis

### Reading flame graphs

- **Width**: Time spent in function (wider = more time)
- **Height**: Call stack depth (taller = deeper calls)
- **Colors**: Usually arbitrary, can indicate different categories

### What to look for

1. **Wide bars at top**: Direct time consumers
2. **Wide bars lower**: Functions called frequently
3. **Many thin bars**: Possibly inefficient iteration
4. **Deep stacks**: Potential for stack optimization

## Optimization workflow

1. **Establish baseline**: Profile current state
2. **Identify hot path**: Find actual bottleneck
3. **Hypothesize**: Theory for improvement
4. **Implement**: Make targeted change
5. **Verify**: Profile again to confirm improvement
6. **Repeat**: If needed, go back to step 2

## Common optimizations

### Algorithm improvements

```python
# O(n^2) - linear search in loop
for item in items:
    if item in other_items:  # O(n) lookup each time
        ...

# O(n) - use set for O(1) lookup
other_set = set(other_items)
for item in items:
    if item in other_set:  # O(1) lookup
        ...
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(key: str) -> Result:
    """Cache expensive results."""
    return compute(key)
```

### Generator expressions

```python
# Memory-heavy: creates full list
data = [transform(x) for x in large_input]
result = sum(data)

# Memory-efficient: processes one at a time
data = (transform(x) for x in large_input)
result = sum(data)
```

## Checklist

- [ ] Baseline profile established
- [ ] Hot paths identified with data
- [ ] Changes targeted at actual bottlenecks
- [ ] Improvements verified with profiling
- [ ] No functionality broken

---

**Additional resources:**

- [py-spy documentation](https://github.com/benfred/py-spy)
- [cProfile documentation](https://docs.python.org/3/library/profile.html)
- [tracemalloc documentation](https://docs.python.org/3/library/tracemalloc.html)
