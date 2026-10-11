---
name: performance-review
description: Find real performance problems — hot loops, N+1 calls, needless I/O, memory bloat.
trigger: when the user says slow, optimize, performance, or profiling
---
## When to use
The user reports slowness or asks to optimize/profile code.

## How
1. `read_file` the code; find the hot path before judging anything.
2. Look for, in impact order:
   - **N+1 patterns** — a query/API/file call inside a loop that could batch.
   - **Wrong complexity** — nested scans where a set/dict lookup works;
     repeated `list.index`/`in list` on large lists.
   - **Needless I/O** — re-reading files, re-opening connections, no caching
     for repeated pure calls.
   - **Memory** — loading whole files/datasets when streaming works; holding
     references that prevent cleanup.
   - **Sync blocking in async code.**
3. Estimate the win in plain words ("this turns 10k queries into 1").
4. Suggest measuring first when the hot path is unclear: `time.perf_counter`
   around suspects or `python -m cProfile -s cumtime`.

## Avoid
- Micro-optimizations (f-string vs concat) while an N+1 sits in the loop.
- "Rewrite it in X" — fix the algorithm first.
- Claiming speedups you can't justify.

## Done well
The few changes that matter, ranked by expected win, each with location and
a concrete replacement — plus how to verify the improvement.
