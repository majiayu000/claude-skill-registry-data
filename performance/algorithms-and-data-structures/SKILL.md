---
name: algorithms-and-data-structures
version: 1.0.0
author: Param
description: Enforces complexity analysis, correct data structure selection, vectorization, and algorithm implementation discipline at principal-engineer level.
applies-to: .py, .ipynb, data processing scripts, ML feature pipelines, algorithm implementations, performance-critical code
---

## Intent

This skill ensures that every algorithm implemented or reviewed in this session is correct before it is optimized, documented with its complexity profile before it is used, and implemented with the most appropriate data structure the problem calls for. It prevents the two most common algorithmic failures in production ML and data engineering code: hidden O(n²) operations disguised as "simple Python loops," and the repeated reimplementation of what the standard library already provides correctly and efficiently. Every data structure choice must be the right tool for the job — not the first one that came to mind.

See also: [`python-excellence/SKILL.md`](../python-excellence/SKILL.md) for code style rules that apply to all algorithm implementations.

---

## 1. Implementation Philosophy

**Before implementing any algorithm, write a mandatory comment block:**

```python
# Algorithm: Merge Intervals
# Time Complexity:  O(n log n) average/worst — dominated by sort
# Space Complexity: O(n) — output array; O(log n) sort stack
# Use-case: Consolidating overlapping time windows in event streams.
# Not suitable for: streaming input (requires full collection first).
# Standard library alternative: None available for this specific operation.
```

**Always prefer standard library implementations** unless there is a documented, benchmarked reason not to:
- Sorting → `list.sort()` / `sorted()` (Timsort, O(n log n), battle-tested)
- Priority queues → `heapq`
- Ordered counting → `collections.Counter`
- Double-ended queues → `collections.deque`
- Sliding windows / combinations → `itertools`
- Bisection → `bisect`

If a custom implementation is chosen over a standard library equivalent, justify it with a comment and a benchmark result.

**Never optimize before correctness is proven.** Implementation order is mandatory:
1. Write the naive, readable version
2. Write tests that verify correctness on edge cases
3. Profile to find the actual bottleneck
4. Optimize the bottleneck with a comment citing the profiler output
5. Verify tests still pass

```python
# WRONG — premature optimization, unverified
def find_duplicates_fast(nums: list[int]) -> list[int]:
    seen = set()
    return [x for x in nums if x in seen or seen.add(x)]  # clever but unreadable

# CORRECT — correct first, then optimized if needed
def find_duplicates(nums: list[int]) -> list[int]:
    """Return elements that appear more than once.

    Time: O(n), Space: O(n)
    """
    counts = Counter(nums)
    return [x for x, count in counts.items() if count > 1]
```

---

## 2. Complexity Awareness Rules

**Any nested loop over the same data structure must have a justifying comment for the O(n²) or worse complexity:**

```python
# O(n²) JUSTIFIED: n is bounded at ≤ 1000 (one workday of 5-minute intervals).
# Quadratic is acceptable here; profiling confirmed < 2ms for max n.
for i in range(len(intervals)):
    for j in range(i + 1, len(intervals)):
        if overlaps(intervals[i], intervals[j]):
            ...
```

If the quadratic behavior cannot be justified, it must be replaced with a better approach. Common substitutions:
- Nested membership check → Set lookup: `O(n²)` → `O(n)`
- Nested sort-and-compare → Sort once, then linear scan: `O(n²)` → `O(n log n)`
- Repeated `min()`/`max()` in a loop → Heap: `O(n²)` → `O(n log n)`

**Any recursive function must document three things in its docstring:**
1. Base case(s): what terminates the recursion?
2. Recursive case: how does the problem reduce toward the base case?
3. Maximum recursion depth: what is the worst-case stack depth, and is it within Python's limit?

```python
def tree_depth(node: TreeNode | None) -> int:
    """Compute the maximum depth of a binary tree.

    Base case: None node has depth 0.
    Recursive case: depth = 1 + max(depth(left), depth(right)).
    Max recursion depth: O(h) where h is tree height. For balanced trees,
    h = O(log n). For degenerate (linked-list-like) trees, h = O(n).
    Warning: Python default recursion limit is 1000. For n > 500 degenerate
    input, use the iterative BFS version instead.
    """
    if node is None:
        return 0
    return 1 + max(tree_depth(node.left), tree_depth(node.right))
```

**Prefer iterative over recursive for production code** unless the recursive version is significantly more readable (e.g., tree traversal where the recursive form matches the mental model exactly). Always note when a recursive version has been left in place for readability over iterative safety.

---

## 3. Sorting and Searching

**Never implement bubble sort, insertion sort, or selection sort for production data.** These are O(n²) and are never the right choice when `sorted()` or `list.sort()` exists. If used for educational or demonstration purposes, add:

```python
# EDUCATIONAL ONLY: O(n²) bubble sort — never use on production data.
# Here to demonstrate the algorithm; use sorted() for any real workload.
```

**Always use the `key=` parameter for custom sort keys.** Never use comparison functions (`cmp`-style).

```python
# WRONG
events.sort(key=lambda e: (e.date, -e.priority))  # Fine, but document the sort key

# RIGHT — named key function for readability and reuse
def event_sort_key(event: Event) -> tuple[date, int]:
    # Sort by date ascending, then by priority descending (negate for reverse)
    return (event.date, -event.priority)

events.sort(key=event_sort_key)
```

**Binary search: always assert or document that the array is sorted before applying.**

```python
import bisect

def find_insertion_point(sorted_values: list[float], target: float) -> int:
    """Find the leftmost index where target can be inserted to maintain sort order.

    Precondition: sorted_values must be sorted in ascending order.
    Time: O(log n), Space: O(1).
    """
    assert sorted_values == sorted(sorted_values), "Input must be sorted"  # dev only
    return bisect.bisect_left(sorted_values, target)
```

---

## 4. Graph Algorithms

**Always document the graph properties before implementing any graph algorithm:**

```python
# Graph properties:
#   Directed: Yes (edges represent causal dependencies)
#   Weighted: Yes (edge weight = estimated processing time in seconds)
#   Cyclic: No (this is a DAG — cycles would indicate circular dependencies)
#   Connected: Not guaranteed — handle disconnected components explicitly
```

**BFS vs DFS choice must always be commented with justification:**
- BFS: shortest path in unweighted graphs, level-order traversal, finding nearest neighbors
- DFS: connectivity testing, topological sort, cycle detection, backtracking problems

```python
# Using BFS: need shortest path (minimum hops) in unweighted dependency graph.
# DFS would find A path but not guarantee the shortest.
def shortest_dependency_path(graph: dict[str, list[str]], start: str, end: str) -> list[str]:
    ...
```

**Always handle disconnected graphs.** Never assume full connectivity without a documented assertion.

```python
def find_all_components(graph: dict[str, list[str]]) -> list[set[str]]:
    """Find all connected components using DFS.

    Handles disconnected graphs: iterates over all nodes as potential
    starting points, visiting each unvisited node exactly once.
    Time: O(V + E), Space: O(V).
    """
    visited: set[str] = set()
    components: list[set[str]] = []

    for node in graph:
        if node not in visited:
            component: set[str] = set()
            _dfs(graph, node, visited, component)
            components.append(component)

    return components
```

---

## 5. Dynamic Programming

**Always show the recurrence relation in a comment before implementing the DP.**

```python
def longest_common_subsequence(s1: str, s2: str) -> int:
    """Compute the length of the longest common subsequence.

    Recurrence:
        dp[i][j] = dp[i-1][j-1] + 1           if s1[i-1] == s2[j-1]
        dp[i][j] = max(dp[i-1][j], dp[i][j-1]) otherwise
    Base case: dp[0][j] = dp[i][0] = 0 (empty string has LCS 0)
    Memoization key: (i, j) — index pair into s1 and s2
    Time: O(m*n), Space: O(m*n) — can be reduced to O(min(m,n)) with rolling array

    Example:
        >>> longest_common_subsequence("ABCBDAB", "BDCABA")
        4  # "BCBA" or "BDAB"
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]
```

**Document the memoization key explicitly** in every top-down DP implementation.

**Include a worked example in the docstring** for any non-trivial DP problem. The example must show the problem input, the expected output, and ideally a brief explanation of how the recurrence produces the answer.

---

## 6. Data Structure Selection Rules

**Every non-trivial data structure choice must be justified in a comment. Default choices require no comment; non-default choices require explicit reasoning.**

| Need | Use | Never Use | Why |
|------|-----|-----------|-----|
| Ordered sequence with fast appends | `list` | — | Default choice |
| Append/pop from both ends | `collections.deque` | `list` | `list.pop(0)` is O(n); deque is O(1) |
| Key-value lookup | `dict` | `list` of tuples | `x in list` is O(n); dict lookup is O(1) |
| Membership testing | `set` | `list` | `x in list` is O(n); set is O(1) |
| Min or max element | `heapq` | Repeated `sorted()` | Sorting each time is O(n log n); heap push/pop is O(log n) |
| Counting occurrences | `Counter` | Manual `dict` with `get` | Counter is more readable and optimized |
| Ordered dict (insertion order matters) | `dict` (Python 3.7+) | `OrderedDict` | Regular dict preserves insertion order since 3.7 |
| Immutable record | `@dataclass(frozen=True)` | `tuple` | Frozen dataclass has named fields |

```python
# WRONG — O(n) membership check in a hot loop
seen_ids = []
for record in stream:
    if record.id in seen_ids:  # O(n) on every iteration
        continue
    seen_ids.append(record.id)

# CORRECT — O(1) membership check
seen_ids: set[int] = set()
for record in stream:
    if record.id in seen_ids:  # O(1)
        continue
    seen_ids.add(record.id)
```

---

## 7. Vectorization and Performance (ML-Specific)

**Replace all explicit Python loops over arrays with NumPy or Pandas vectorized operations.** Python loops over arrays are 10–100x slower than equivalent NumPy operations.

```python
# WRONG — Python loop, O(n) with high constant factor
result = []
for i in range(len(prices)):
    result.append(prices[i] * quantities[i] * (1 - discounts[i]))

# CORRECT — vectorized, same O(n) but ~50x faster in practice
result = prices * quantities * (1 - discounts)  # NumPy element-wise
```

**Profile before optimizing. Never optimize based on intuition alone.** Use `cProfile` for function-level profiling, `line_profiler` for line-level:

```python
# Add to any script to profile:
import cProfile
cProfile.run("your_function(args)", sort="cumulative")

# Or use the decorator for line-level:
# pip install line_profiler
# Add @profile decorator and run: kernprof -l -v script.py
```

Document the bottleneck found in a comment next to the optimization:
```python
# Profiler finding (2024-01-15): this loop consumed 87% of total runtime for n=100k.
# Replaced explicit loop with np.where vectorization: 45x speedup confirmed.
result = np.where(condition_array, value_if_true, value_if_false)
```

**For large datasets, always consider chunking, streaming, or lazy evaluation before loading everything into memory:**

```python
# WRONG — loads entire dataset into memory
df = pd.read_csv("huge_file.csv")
result = process(df)

# CORRECT — stream in chunks
chunk_size = 10_000
results = []
for chunk in pd.read_csv("huge_file.csv", chunksize=chunk_size):
    results.append(process(chunk))
final = pd.concat(results)
```

---

## 8. Anti-Patterns — Always Refuse These

**Never reimplement what `itertools`, `collections`, `heapq`, or `bisect` already provides.** Document which standard library function was used instead.

```python
# WRONG — manual sliding window
windows = []
for i in range(len(seq) - k + 1):
    windows.append(seq[i:i+k])

# CORRECT — use zip with slicing (for small k), or document why manual is needed
from itertools import islice
def sliding_window(seq, k):
    it = iter(seq)
    window = tuple(islice(it, k))
    if len(window) == k:
        yield window
    for x in it:
        window = window[1:] + (x,)
        yield window
```

**Never use a list as a stack for performance-critical code.** Use `collections.deque` if popping from the left; use `list` with `append()`/`pop()` only if appending and popping from the right.

**Never concatenate strings in a loop.** String concatenation is O(n²) due to immutability.

```python
# WRONG — O(n²)
result = ""
for word in words:
    result += word + " "

# CORRECT — O(n)
result = " ".join(words)
```

**Never sort to find min or max.** Sorting is O(n log n); `min()` and `max()` are O(n).

```python
# WRONG
smallest = sorted(values)[0]

# CORRECT
smallest = min(values)

# For k-smallest: use heapq.nsmallest (O(n log k)), not sort (O(n log n))
import heapq
k_smallest = heapq.nsmallest(k, values)
```

**Never use `range(len(x))` when you can use `enumerate(x)`.** Never use manual index tracking when Python provides a cleaner idiom.
