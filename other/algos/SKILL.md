---
name: algos
description: "Combined knowledge base from \"The Algorithm Design Manual\" (Skiena) and \"Algorithms, 4th Edition\" (Sedgewick & Wayne). Use when choosing or analyzing an algorithm or data structure — complexity analysis, sorting, searching/symbol tables, heaps, graphs, shortest paths, strings, dynamic programming, greedy, backtracking, NP-completeness — when modeling a problem to a known algorithm, or when looking up the best-known approach for a problem."
allowed-tools:
  - Read
  - Grep
argument-hint: [topic, algorithm name, or chapter number]
---

# Algorithms — Skiena + Sedgewick (combo)
**Authors**: Steven Skiena (*The Algorithm Design Manual*) + Robert Sedgewick & Kevin Wayne (*Algorithms, 4th Ed.*) | **Pages**: ~1,708 | **Chapters**: 12 (topic-merged) | **Generated**: 2026-06-07

## How to Use This Skill

- **Without arguments** — load the Core Frameworks below for design/analysis judgment.
- **With a topic** — ask about `dijkstra`, `red-black trees`, `dynamic programming`, `union-find`; use the Topic Index to find the chapter, then read that `chapters/chNN-*.md` before answering.
- **With a chapter** — ask for `ch06`; load that file.
- **"What's the best algorithm for X?"** — check `chapters/ch12-algorithm-catalog.md` (Skiena's 75-problem lookup) first.

The two books are complementary, and the chapters preserve the contrast:
**Sedgewick** = precise Java implementations, exact APIs, empirical/tilde cost analysis (reach for it to *implement and measure*).
**Skiena** = problem modeling, when-to-use judgment, war stories, the catalog (reach for it to *recognize what kind of problem you have and pick an approach*).

---

## Core Frameworks & Mental Models

### 1. Analyze before you optimize (complexity)
- **RAM model + Big-Oh/Ω/Θ** (Skiena) for *classification*; **tilde `~` + order-of-growth** (Sedgewick) for *prediction*. Big-Oh is only an upper bound — use `~` or Θ for tight claims, and the **doubling-ratio test** (`T(2N)/T(N) → 2^b ⇒ order N^b`; ratio ≈ 8 ⇒ cubic) to validate empirically.
- **Dominance ladder** (memorize): `n! ≫ 2ⁿ ≫ n³ ≫ n² ≫ n lg n ≫ n ≫ lg n ≫ 1`. Logs appear whenever you repeatedly halve the domain (binary search, balanced trees, divide & conquer).

### 2. Pick the right data structure first
- **Contiguous (arrays) vs linked** (Skiena): arrays give O(1) random access + cache locality; linked structures give O(1) splice + unbounded growth. Resizing arrays amortize to O(1) append.
- **Symbol table = the workhorse.** Sedgewick's cost summary: ordered BST → ~1.39 lg N avg but O(N) worst; **red-black BST → guaranteed ~lg N for all ordered ops**; **hash tables → O(1) average** (separate chaining or linear probing) but lose order. Default to a hash table for pure lookup, a balanced BST when you need ordered operations (floor/ceiling/range).
- **Priority queue (binary heap)**: insert/del-max in ~lg N; the engine behind heapsort, Dijkstra, Prim, and "top-k" selection. Use an **indexed PQ** when you must decrease-key.

### 3. The five design techniques (Skiena Part I — the heart of design)
- **Divide & conquer**: split, recurse, combine; analyze with the recurrence (e.g. mergesort `T(n)=2T(n/2)+n = Θ(n lg n)`).
- **Dynamic programming**: when subproblems overlap and the problem has optimal substructure. Recipe: (1) define the recurrence/objective, (2) order subproblems so dependencies come first, (3) memoize or fill a table bottom-up. Canonical: edit distance, longest increasing subsequence. DP trades space for re-computation.
- **Greedy**: take the locally best choice; only correct when an **exchange argument** proves it (MST, Dijkstra, Huffman are provably greedy). Verify correctness or find a counterexample — greedy is wrong far more often than it looks.
- **Backtracking**: systematic DFS over the solution space (subsets, permutations, paths) with **pruning**; the general skeleton tests partial solutions and abandons dead branches early.
- **Reduction**: transform your problem into a solved one. Skiena's Take-Home Lesson: *don't design novel graph algorithms — design graphs that let you call classical ones.* Network flow subsumes bipartite matching; topological sort solves ordering-under-constraints.

### 4. Graphs are a modeling language
- Choose **adjacency list** (sparse, `E ≈ V`) vs **matrix** (dense, O(1) edge test). **BFS** → shortest unweighted paths, bipartite check, connected components. **DFS** → topological sort (reverse postorder), cycle detection, articulation points, strong components (Kosaraju/Tarjan). Weighted: **MST** (Prim eager `~E log V`, Kruskal `~E log E` + union-find), **shortest paths** (Dijkstra `O(E log V)` *no negative edges*; Bellman-Ford `O(VE)` handles negatives + detects negative cycles; DAG relaxation `O(E+V)`; Floyd-Warshall `O(V³)` all-pairs).

### 5. Know when to stop (intractability)
- If your problem reduces *from* a known NP-complete problem (SAT, vertex cover, independent set, clique, Hamiltonian cycle, TSP), **stop hunting for a polynomial algorithm**. Switch to: approximation algorithms (with a proven ratio), heuristics (local search, simulated annealing), or exponential backtracking with hard pruning on small instances. Reduce in the **correct direction** (known-hard ⇒ yours) to prove hardness.

---

## Chapter Index

| # | Title | Key topics |
|---|-------|-----------|
| [ch01](chapters/ch01-complexity-analysis.md) | Complexity & Analysis | RAM model, Big-Oh/Ω/Θ, tilde, growth rates, doubling test |
| [ch02](chapters/ch02-data-structures.md) | Fundamental Data Structures | arrays vs linked, stacks/queues/bags, dictionaries, hashing, ADTs/iterators |
| [ch03](chapters/ch03-sorting.md) | Sorting | selection/insertion/shell, mergesort, quicksort (3-way), lower bound, system sorts |
| [ch04](chapters/ch04-searching-symbol-tables.md) | Searching & Symbol Tables | binary search, BST, 2-3 & red-black trees, hash tables, cost summary |
| [ch05](chapters/ch05-priority-queues-heaps.md) | Priority Queues & Heaps | binary heap, swim/sink, heapsort, indexed PQ |
| [ch06](chapters/ch06-graphs.md) | Graphs — Representation & Traversal | adjacency list/matrix, BFS, DFS, topological sort, components, bipartite, SCC |
| [ch07](chapters/ch07-weighted-graphs.md) | Weighted Graphs | MST (Prim/Kruskal), shortest paths (Dijkstra/Bellman-Ford/Floyd), network flow, matching |
| [ch08](chapters/ch08-strings.md) | Strings | LSD/MSD/3-way string sort, tries/TST, KMP/Boyer-Moore/Rabin-Karp, regex/NFA, Huffman/LZW |
| [ch09](chapters/ch09-divide-conquer-dynamic-programming.md) | Divide & Conquer + Dynamic Programming | recurrences, memoization, optimal substructure, edit distance, LIS |
| [ch10](chapters/ch10-greedy-backtracking-heuristics.md) | Greedy, Backtracking & Search | exchange arguments, backtracking skeleton, pruning, local search, simulated annealing |
| [ch11](chapters/ch11-intractability-np.md) | Intractability & NP-Completeness | P/NP/NP-complete, reductions, SAT, Cook-Levin, approximation |
| [ch12](chapters/ch12-algorithm-catalog.md) | Algorithm Catalog (lookup) | Skiena's 75-problem "what to use" reference table |

## Topic Index

- **Amortized analysis / resizing arrays** → ch01, ch02
- **Approximation algorithms** → ch11
- **Articulation vertices / cut nodes** → ch06
- **Backtracking** → ch10
- **Bellman-Ford** → ch07
- **Big-Oh / Ω / Θ notation** → ch01
- **Binary search** → ch01, ch03, ch04
- **Binary search trees (BST)** → ch04
- **Bipartite detection / matching** → ch06, ch07
- **Boyer-Moore** → ch08
- **Breadth-first search (BFS)** → ch06
- **Connected / strong components (Kosaraju, Tarjan)** → ch06
- **Cost model / tilde notation** → ch01
- **Depth-first search (DFS)** → ch06
- **Dijkstra's algorithm** → ch07
- **Divide & conquer / recurrences** → ch09 (analysis ch01, ch03)
- **Dynamic programming (edit distance, LIS)** → ch09
- **Edit distance / approximate string matching** → ch09, ch08
- **Floyd-Warshall (all-pairs)** → ch07
- **Greedy algorithms / exchange argument** → ch10 (applied ch07)
- **Hash tables (chaining, linear probing)** → ch02, ch04
- **Heaps / heapsort** → ch05, ch03
- **Huffman / LZW compression** → ch08
- **Knuth-Morris-Pratt (KMP)** → ch08
- **Kruskal's algorithm** → ch07
- **Linked lists vs arrays** → ch02
- **Local search / simulated annealing** → ch10
- **Lower bound for sorting (N lg N)** → ch03
- **Minimum spanning tree (MST)** → ch07
- **NP-completeness / reductions / SAT** → ch11
- **Network flow (Edmonds-Karp, residual graph)** → ch07
- **Priority queues / indexed PQ** → ch05
- **Problem-to-algorithm lookup** → ch12
- **Quicksort (incl. 3-way)** → ch03
- **Rabin-Karp** → ch08
- **Red-black / 2-3 trees** → ch04
- **Regular expressions / NFA** → ch08
- **Shortest paths** → ch07 (unweighted: ch06)
- **Sorting (selection, insertion, shell, merge, quick)** → ch03
- **Stacks / queues / bags** → ch02
- **String sorts (LSD/MSD/3-way radix)** → ch08
- **Symbol tables / dictionaries** → ch04, ch02
- **Topological sort** → ch06
- **Tries / TST** → ch08
- **Union-find (weighted quick-union)** → ch07, ch02

## Supporting Files

- [glossary.md](glossary.md) — ~65 terms with definitions and chapter refs
- [patterns.md](patterns.md) — algorithmic design patterns (when / how / trade-offs)
- [cheatsheet.md](cheatsheet.md) — master complexity tables + "which algorithm when"

---

## Scope & Limits

Covers the two source books only. Every complexity bound and API in the chapter files was synthesized directly from the extracted text; specifics the source did not state are marked `*(not found in source slice)*` rather than guessed. For language-specific standard-library behavior or problems beyond these books, verify against current references. For implementation in a specific codebase, combine with project tooling.
