---
name: refactor-for-optimize
description: Refactor code for performance — algorithmic complexity, data structure selection, unnecessary I/O, hot-path improvement, and memory usage. Use explicitly in the REFACTOR phase of TDD when the developer judges performance improvement is warranted, or when a measurable bottleneck is identified. Does not overlap with refactor-for-clarity (readability) or refactor-for-reuse (DRY/extraction). Trigger on phrases like "this is slow", "optimize the hot path", "O(n²) loop", "N+1 queries", "too much memory", "profile shows this is the bottleneck".
license: MIT
metadata:
  version: "1.0.1"
  created: "2026-06-10"
  category: refactoring
  tags: refactoring, performance, optimization, algorithmic-complexity, python
  risk: safe
---

# Refactor for Optimization

## Overview

Improve the performance profile of working code — without changing what it does. The goal is not fewer lines or cleaner structure — it's measurably faster or lower-memory execution on the paths that matter. Every change must pass: "Is this demonstrably faster or cheaper than before, with all tests still green?"

## When to Use

- In the REFACTOR phase of `test-driven-development`, when the developer identifies a hot path needing improvement
- When profiling reveals a specific function or loop is the bottleneck
- When algorithmic complexity is clearly wrong (O(n²) scan of a list that should be an O(1) set lookup)
- When unnecessary I/O occurs inside a loop (repeated file reads, N+1 database queries, repeated computations)
- When memory pressure is measurable and the cause is identifiable

**When NOT to use:**

- You haven't measured — optimize only where profiling or reasoning confirms the bottleneck
- The code isn't correct yet — correctness first, performance second
- The issue is naming, nesting, or structural complexity — use `refactor-for-clarity` instead
- The issue is duplication or dead code — use `refactor-for-reuse` instead
- You're about to rewrite the module entirely — wait; optimizing throwaway code wastes effort
- The "optimization" trades correctness for speed — never acceptable

## The Four Principles

### 1. Preserve Behavior Exactly

Don't change what the code does — only how fast or efficiently it does it. All inputs, outputs, side effects, error behavior, and edge cases must remain identical.

```
ASK BEFORE EVERY CHANGE:
→ Does this produce the same output for every input?
→ Does this maintain the same error behavior?
→ Does this preserve the same side effects and ordering?
→ Do all existing tests still pass without modification?
```

### 2. Measure Before and After

Guessing where the bottleneck is causes more harm than the original problem. Optimize only where you can demonstrate a measurable cost.

```
BEFORE optimizing:
- Profile to identify the actual hot path (cProfile, py-spy, timeit)
- Name the specific bottleneck — a function, a loop, a query — not "it feels slow"
- Establish a baseline: what does it cost now?

AFTER optimizing:
- Verify the change is faster on realistic data, not synthetic micro-benchmarks
- Confirm the improvement is in the hot path, not in code that's rarely executed
```

If profiling isn't available, state the complexity change explicitly (e.g., "O(n²) → O(n)") and explain why it matters at the expected input scale.

### 3. Algorithmic Over Micro-Optimization

An O(n log n) algorithm beats a hand-tuned O(n²) algorithm at any meaningful scale. Fix the algorithm before tuning constants.

```
PRIORITY ORDER:
1. Algorithmic complexity   (O(n²) → O(n log n) → O(n))
2. Data structure selection (list scan → set/dict lookup)
3. I/O reduction            (N+1 → batch, redundant reads → cache)
4. Memory reduction         (materializing full list → generator)
5. Constant-factor tuning   (only when 1–4 are exhausted)
```

Micro-optimizations (avoiding a function call, caching an attribute lookup, reordering branches) are rarely worth the readability cost unless 1–4 have been exhausted.

### 4. Keep the Code Maintainable

A 10% speedup that makes the code unreadable is usually not worth it. If an optimization makes the code harder to follow, add a short comment explaining why — or choose the cleaner, slightly-slower implementation.

The exception: when the hot path is a genuine bottleneck and the faster version is the idiomatic form (e.g., set membership check vs. list scan), take it — it's both clearer and faster.

## Working with the Other Refactoring Skills

The three refactoring skills run in order: **clarity → reuse → optimize**. Each assumes the previous one's work is correct and load-bearing.

**Treat prior clarity and reuse improvements as non-negotiable by default.** This means:

- Do not inline extracted helpers just because function calls have overhead. In Python, that overhead is negligible — and the profiler will tell you if it isn't.
- Do not rename clear, descriptive variables back to terse forms for "speed."
- Do not break DRY abstractions to repeat logic in multiple hot paths.

**The correct action when the hot path is inside an extracted helper:** optimize the *body* of that helper, not its existence. If `_get_active_rows()` is slow, fix what it does internally — don't dissolve it back into its callers.

**When the trade-off is genuinely unavoidable** — profiling confirms the abstraction itself is the bottleneck — you may inline or restructure, but:

1. The profiler result is the justification, not an opinion.
2. Add a comment explaining why the less-obvious form is necessary: `# Inlined from _get_active_rows — profiler shows call overhead is 40% of hot path at 10k ticks/s`.
3. Flag the change explicitly in the commit message so the next developer understands the trade-off.

**The tie-breaker:** measured performance gain must outweigh the readability cost. A sub-1% gain on a cold path does not justify undoing a good extraction. If you cannot measure the gain, do not make the trade.

## The Refactoring Process

### Step 1: Verify Test Coverage

Before touching anything, confirm the code you're about to optimize is covered by tests. Tests are the only proof that behavior is preserved after optimization.

If coverage is missing: invoke **`test-driven-development`** to write characterization tests first — tests that pin the current behavior before any performance changes begin. Commit them before proceeding.

### Step 2: Understand Before Touching (Chesterton's Fence)

Before changing a data structure or algorithm, understand why the original was chosen.

```
BEFORE OPTIMIZING, ANSWER:
- What is this code's responsibility?
- What calls it? What data does it receive, and how large does that data get?
- Why might it have been written this way? (correctness constraint? platform limit? historical reason?)
- Check git blame: was this a deliberate choice or just the first-pass implementation?
```

If you can't answer these, you're not ready to optimize. Read more context first.

### Step 3: Identify the Hot Path

Scan for these patterns — each is a concrete signal, not a vague smell:

**Algorithmic complexity:**

| Pattern | Signal | Optimization |
|---------|--------|--------------|
| `if x in list` inside a loop | O(n) scan per iteration → O(n²) total | Convert `list` to `set` before the loop |
| Nested loops over the same data | O(n²) for a task doable in O(n) | Sort + single pass, or use a dict/set for lookup |
| Re-sorting a partially-built structure | Wasted work each insert | Use `heapq` or maintain a sorted structure |
| Recursive calls with repeated subproblems | Exponential without memoization | Add `@functools.lru_cache` or convert to iterative with memo dict |
| Building result by repeated concatenation | O(n²) string or list growth | Collect into a list, then `''.join()` or extend at end |

**Data structure selection:**

| Pattern | Signal | Optimization |
|---------|--------|--------------|
| `list` used only for membership checks | O(n) lookup | Replace with `set` |
| `dict` values are lists being appended to | Manual check-and-create per key | Replace with `collections.defaultdict(list)` |
| Sorted list searched linearly | O(n) search | Use `bisect` for O(log n) |
| Counter built manually with `dict.get` | Verbose and slower at scale | Use `collections.Counter` |

**Unnecessary I/O:**

| Pattern | Signal | Optimization |
|---------|--------|--------------|
| File/DB read inside a loop | N+1 reads | Batch read before the loop, access by key inside |
| Same pure computation repeated each call | Redundant work | Cache result (local variable, `lru_cache`, class attribute) |
| Writing to disk inside a hot loop | I/O-bound loop | Buffer writes, flush once at end |
| `re.compile(pattern)` called inside a function | Pattern recompiled every call | Move `re.compile` to module level |

**Memory usage:**

| Pattern | Signal | Optimization |
|---------|--------|--------------|
| Large list fully materialized for single-pass use | Unnecessary peak memory | Replace with generator expression |
| Loading entire file to process line by line | Unnecessary memory | Iterate line by line |
| Large intermediate structures not released | Memory pressure between steps | Delete or narrow scope of intermediate data |

### Step 4: Apply Changes Incrementally

Make one optimization at a time. Run tests after each change.

```
FOR EACH OPTIMIZATION:
1. Make the change
2. Run the test suite
3. If tests pass → verify the performance gain → commit
4. If tests fail → revert immediately — do NOT modify tests to force a pass
```

**The Rule of 500:** If an optimization would touch more than 500 lines, reconsider whether a larger architectural change is needed instead of piecemeal tuning.

### Step 5: Verify the Result

After all changes:

```
COMPARE BEFORE AND AFTER:
- Is the optimized version measurably faster or cheaper on realistic inputs?
- Did you introduce correctness issues at edge cases (empty input, large input, concurrent access)?
- Is the optimized code still understandable, or does it need a comment explaining why?
- Would a teammate recognize this as an improvement, not just a different implementation?
```

If the optimization is not measurably better, or breaks an edge case, revert.

## Language-Specific Guidance

```python
# SET MEMBERSHIP: O(n) per lookup → O(1)
# Before
valid_ids = [1, 2, 3, ...]   # built elsewhere
for item in items:
    if item.id in valid_ids:  # O(n) scan every iteration → O(n²) total
        process(item)
# After
valid_ids = {1, 2, 3, ...}   # set
for item in items:
    if item.id in valid_ids:  # O(1) lookup → O(n) total
        process(item)


# DICT GROUPING: eliminate per-key existence check
# Before
groups = {}
for item in items:
    if item.category not in groups:
        groups[item.category] = []
    groups[item.category].append(item)
# After
from collections import defaultdict
groups = defaultdict(list)
for item in items:
    groups[item.category].append(item)


# STRING BUILDING: O(n²) → O(n)
# Before
result = ""
for line in lines:
    result += line + "\n"   # new string object allocated every iteration
# After
result = "\n".join(lines) + "\n"


# N+1 READ: batch before loop
# Before
for user_id in user_ids:
    user = db.get_user(user_id)   # one query per iteration
    process(user)
# After
users = {u.id: u for u in db.get_users(user_ids)}  # single batch query
for user_id in user_ids:
    process(users[user_id])


# GENERATOR: avoid materializing large intermediate lists
# Before
def get_active_names(users):
    return [u.name for u in users if u.active]   # full list in memory
# After — only when the caller iterates once
def get_active_names(users):
    return (u.name for u in users if u.active)   # generator


# MEMOIZATION: repeated subproblems
# Before
def fib(n):
    if n <= 1: return n
    return fib(n - 1) + fib(n - 2)  # O(2^n)
# After
from functools import lru_cache
@lru_cache(maxsize=None)
def fib(n):
    if n <= 1: return n
    return fib(n - 1) + fib(n - 2)  # O(n)


# MODULE-LEVEL COMPILE: avoid per-call recompile
# Before
def extract_numbers(text):
    return re.findall(r'\d+', text)   # re.compile called implicitly each time
# After
_NUMBER_RE = re.compile(r'\d+')
def extract_numbers(text):
    return _NUMBER_RE.findall(text)
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It's fast enough" | Profile first to confirm. "Fast enough" needs a number, not a feeling. |
| "This optimization is obvious" | Obvious optimizations that break correctness at edge cases happen constantly. Measure and test every change. |
| "I'll optimize the whole thing at once" | One change at a time. If something breaks, you need to know which optimization caused it. |
| "The set/dict version is harder to read" | For membership checks and grouping, idiomatic Python is both clearer and faster — take it. |
| "This only matters at scale" | Correct — state the expected scale explicitly. If input is always ≤100 items, document why the O(n²) form is fine rather than optimizing it. |
| "I'll add a comment explaining the trick" | If the code needs a paragraph to explain, the performance gain may not be worth the maintenance cost. Consider keeping the readable form. |

## Red Flags

- Optimizing before profiling — you're solving the wrong problem
- Optimization that requires modifying tests to pass — you changed behavior
- Making code significantly harder to read for a sub-1% speedup on a cold path
- Adding thread-unsafe mutable shared state to avoid redundant computation — race conditions are not worth the gain
- Inlining complex logic "for speed" without measuring — the readability cost is real; the speed gain may not be
- Batching many optimizations into one large untested commit
- Optimizing code that is not on the hot path

## Verification

**Existing tests are read-only.** If an optimization requires modifying an existing test to pass, stop — you changed behavior, not just performance.

After completing an optimization pass:

- [ ] All existing tests pass without modification
- [ ] Build succeeds with no new warnings
- [ ] Linter/formatter passes (no style regressions)
- [ ] Optimization is in the confirmed hot path (not cold code)
- [ ] Performance gain verified on realistic inputs (not synthetic micro-benchmarks only)
- [ ] Correctness at edge cases verified (empty input, single element, maximum realistic size)
- [ ] The diff is clean — no unrelated changes mixed in
- [ ] Refactored code follows project conventions (checked against AGENTS.md, CLAUDE.md or equivalent)
- [ ] No error handling was removed or weakened
- [ ] If the optimized code is less obvious, a short comment explains *why* the less-readable form is necessary
- [ ] A teammate or review agent would approve the change as a net improvement
