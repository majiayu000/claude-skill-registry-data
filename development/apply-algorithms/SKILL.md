---
name: apply-algorithms
description: Use when a problem shape maps to a classic family — dynamic programming, greedy, divide-and-conquer, graph search, or sort-first — and you must pick and justify the algorithm.
---

# Apply Algorithms

Maps a problem's shape to the classic algorithm family that solves it (CLRS), with the complexity that
justifies the choice. Data-structure half of the decision: [choose-data-structure](../choose-data-structure/SKILL.md).

## The families

- **Divide and conquer** — independent subproblems, combine the results (mergesort, binary search).
  Solve the recurrence with the master theorem; often `O(n log n)`.
- **Dynamic programming** — *overlapping* subproblems with optimal substructure: cache the repeated work.
  When a recursive solution recomputes the same subproblem, DP memoises it. `O(n)`–`O(n²)` typical.
- **Greedy** — a locally optimal choice is globally optimal, *only when a greedy-choice proof holds*
  (Huffman coding, Kruskal/Prim MST `O(E log V)`). Never use greedily on a hunch; it is either proven or
  wrong.
- **Graph search** — BFS/DFS `O(V + E)` for reachability, connected components, topological sort;
  Dijkstra `O((V + E) log V)` for non-negative shortest paths only (any negative edge breaks it); Bellman-Ford `O(VE)` for negative edges, and it detects negative cycles;
  Floyd-Warshall `O(V³)` for all pairs.
- **Sort-first** — sort then scan turns many pairwise problems into one pass (`O(n log n)` + `O(n)`).
- **Bounded-integer tricks** — counting/radix/bucket sort reach `O(n)` when keys are small integers.

## 1. Audit (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null | head -20
grep -rn "sort\|recur\|memo\|visited\|queue\|stack\|priority" --include="*.ts" --include="*.rs" --include="*.go" --include="*.py" . 2>/dev/null | head -30
```

State the problem in one line, then name its shape: optimal substructure and overlapping subproblems →
DP; independent subproblems → divide and conquer; a provable local optimum → greedy; nodes and edges or
reachability → graph; "for each pair" → sort-first.

## 2. Pick and justify

- DP: identify the state, the recurrence, and the base case; memoise or bottom-up.
- Greedy: write the exchange/proof argument first; without it, fall back to DP.
- Graph: choose the traversal by the question (reachability, shortest path, cycles, ordering).
- Sort-first: sort by the key that makes the remaining question one linear pass.

## 3. State the complexity and the edge cases

Give the time and space order of the chosen algorithm, and the inputs it fails on: negatives (Dijkstra),
already-sorted (quicksort), a cycle (topological sort), a graph with no path (shortest path).

## Verify

The chosen family matches the named problem shape, the complexity is stated, and the edge case that
breaks the algorithm is handled. A counterexample to a greedy choice fails the proof before it ships.

## When to deviate

- The problem is small: the simplest correct algorithm beats the clever one.
- A well-tested standard-library or framework function already implements it — call it, do not re-implement.
