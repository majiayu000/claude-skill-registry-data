---
name: algorithms
description: Algorithm design and analysis skill for DSH; use when working on optimization, data structures, or computational procedures.
---

# Skill: Algorithms

Domain: `build` | Depth: `axiom`

## Capabilities
- Graph algorithms: shortest path, MST, centrality, community detection (networkx)
- Sorting, searching, dynamic programming
- Optimization: gradient descent, genetic algorithms, simulated annealing (scipy)
- Cryptographic primitives: hashing, entropy
- Tree structures: BST, heap, trie
- Complexity analysis tools
- Pathfinding: A*, Dijkstra, BFS, DFS

## Libraries
| Library   | Purpose |
|-----------|---------|
| networkx  | Graph algorithms |
| scipy     | Optimization algorithms |
| numpy     | Array-based algorithm primitives |

## Module
`agents/skills/algorithms.py`

## Key Functions
- `shortest_path(graph, src, dst)` — Dijkstra shortest path
- `mst(graph)` — minimum spanning tree
- `centrality(graph)` — betweenness + eigenvector centrality
- `astar(grid, start, goal, heuristic)` — A* pathfinding
- `genetic_optimize(fitness_fn, population, generations)` — genetic algorithm
- `entropy(data)` — Shannon entropy
- `topological_sort(dag)` — topological ordering
