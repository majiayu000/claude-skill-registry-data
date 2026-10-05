---
name: networkx-python
description: Use for writing, reviewing, debugging, testing, or optimizing Python NetworkX graph construction and algorithms. Trigger on Graph, DiGraph, MultiGraph, MultiDiGraph, nodes, edges, attributes, paths, connectivity, DAGs, centrality, communities, graph conversion, or NetworkX backend work. Do not use for rustworkx-only, graph-database query languages, neural-network graph tensors, or ordinary tabular joins.
argument-hint: "[NetworkX task, graph contract, code, or error]"
---

# NetworkX Python

Produce NetworkX code whose graph kind, node identity, edge multiplicity,
direction, attribute schema, weight semantics, and algorithm preconditions are
explicit and tested.

## Boundary

Use this skill when the project uses `networkx` or the user requests it. Do not
introduce NetworkX into a library-neutral data task without a graph-shaped
problem. Route a rustworkx implementation to its own skill; conversion between
the two is in scope only when NetworkX remains an interface boundary.

## Choose the graph object first

| Object | Meaning | Select it when |
|---|---|---|
| `Graph` | Undirected simple graph; self-loops allowed, parallel edges collapsed. | Edge direction and parallel identity do not matter. |
| `DiGraph` | Directed simple graph. | `(u, v)` and `(v, u)` differ. |
| `MultiGraph` | Undirected graph with edge keys. | Parallel relationships must remain distinct. |
| `MultiDiGraph` | Directed graph with edge keys. | Direction and parallel relationships both matter. |
| graph/node/edge attributes | Mutable Python mappings attached to topology. | Metadata belongs to the graph contract. |
| graph view | Live, read-only-ish projection over a graph. | Filter or inspect without copying; remember later mutations are visible. |

Nodes are hashable identifiers, not row positions. In multigraphs, an edge is
identified by `(u, v, key)`, not only `(u, v)`. NetworkX objects are mutable and
hold arbitrary Python objects, so copying depth and attribute aliasing are part
of the contract. Read [the object and data model](references/object-model.md)
before changing graph class, copying, subgraphing, or converting.

## Ordered workflow

1. State directedness, parallel-edge policy, self-loop policy, and node identity.
2. Define required node/edge attributes, defaults, and the exact weight key.
3. Construct or convert the graph without silently merging nodes or edges.
4. Check the chosen algorithm's graph-type, connectivity, weight, and DAG
   preconditions before calling it.
5. Make tie-breaking and output order explicit; do not treat set/dict/view order
   as a mathematical guarantee.
6. Test empty, singleton, disconnected, cyclic, duplicate-edge, missing-weight,
   and equal-cost cases that can falsify the contract.

## Route intent to the API family

| Intent | Prefer | Guard |
|---|---|---|
| Build incrementally | `add_node(s)_from`, `add_edge(s)_from` | Tuple arity differs for data and multigraph keys. |
| Convert supported data | `nx.from_*`, `nx.to_*`, `nx.to_networkx_graph` | Specify directed/multigraph semantics; conversions may lose attributes or keys. |
| Inspect topology | `G.nodes`, `G.edges`, degrees, neighbors | Views are live; materialize only for a stable snapshot. |
| Traverse or find paths | `nx.bfs_*`, `nx.dfs_*`, `nx.shortest_path*` | Choose weighted versus unweighted and source/target reachability. |
| Analyze a DAG | `nx.is_directed_acyclic_graph`, `topological_sort`, DAG algorithms | Validate acyclicity; topological order may be non-unique. |
| Components/connectivity | weak/strong/connected component families | Match directedness and decide whether disconnected input is valid. |
| Rank or partition | centrality/community algorithms | Confirm weight meaning, randomness, convergence, and disconnected behavior. |
| Preserve only a projection | subgraph/restricted views | Copy before independent mutation. |

Read [the operation and algorithm map](references/operations.md) for return
shapes, generators, multigraph edges, weight callbacks, randomness, and
conversion loss.

## Canonical anchor

```python
import networkx as nx


def cheapest_route(
    edges: list[tuple[str, str, float]], source: str, target: str
) -> tuple[list[str], float]:
    graph = nx.DiGraph()
    graph.add_weighted_edges_from(edges, weight="cost")
    if source not in graph or target not in graph:
        raise KeyError("source and target must be graph nodes")
    path = nx.shortest_path(graph, source, target, weight="cost")
    return path, nx.path_weight(graph, path, weight="cost")
```

The graph is directed because route direction matters. The same attribute name
is passed to construction, path selection, and path scoring. If parallel routes
must remain distinct, use `MultiDiGraph` and define how an algorithm chooses
among edge keys; do not change classes without revisiting return semantics.

## High-risk rules

- Never infer directedness from data ordering. Make it a constructor decision.
- Do not use `Graph` when duplicate edges carry independent events, capacities,
  or provenance; the later edge updates the existing relationship.
- Do not use an arbitrary numeric attribute as a weight. State whether smaller
  means cheaper, whether negative values are legal, and what a missing value
  means. Dijkstra-family algorithms require nonnegative weights.
- Treat `NodeNotFound`, `NetworkXNoPath`, disconnected input, cycles, and
  non-convergence as domain outcomes or explicit failures, not empty results.
- `topological_sort` returns one valid order, not the unique order. Use a
  lexicographical variant or a domain tie-breaker when reproducibility matters.
- A shortest-path generator, component generator, or view is not a list. Keep
  it lazy for one pass or materialize deliberately if it must be reused.
- Subgraphs and filtered views can share attribute mappings with the original.
  Copy when independent mutation is required, and test that ownership boundary.
- For randomized generators or algorithms, accept/pass a seed and test
  invariants rather than one accidental sample.
- Drawing is presentation, not graph analysis. Keep layout coordinates and
  rendering dependencies outside the graph's semantic result.
- For large graphs, establish scale before promising NetworkX performance.
  Backends or rustworkx may change supported algorithms or object semantics;
  benchmark the actual workload and preserve the public boundary.

## Version grounding and completion

Check the installed version with `networkx.__version__` and inspect the chosen callable's signature
when backend dispatch, return type, keyword, algorithm availability, or
conversion behavior can drift. The authoring baseline is the official NetworkX
3.6.1 stable reference, not proof of the caller's environment. Use
[verification and API grounding](references/verification.md) for the local evidence steps.

Do not declare completion until graph kind and identity rules match the domain;
attribute and weight contracts are explicit; algorithm preconditions are
checked; exceptional/disconnected/ambiguous cases are handled; output type and
order meet the caller; and tests cover a counterexample rather than only the
happy path.

## References

- [Object and data model](references/object-model.md)
- [Operation and algorithm map](references/operations.md)
- [Verification and API grounding](references/verification.md)
