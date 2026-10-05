---
name: rustworkx-python
description: Use for writing, reviewing, debugging, testing, or optimizing Python rustworkx graph code. Trigger on PyGraph, PyDiGraph, PyDAG, stable node or edge indices, payloads/weights, rustworkx algorithms, graph conversion, or performance-sensitive Python graph analysis. Do not use for NetworkX-only code, Rust petgraph code, graph databases, or tensor/GNN workloads.
argument-hint: "[rustworkx graph task, code, conversion, or error]"
---

# rustworkx Python

Produce rustworkx code whose graph kind, index lifecycle, payload semantics,
parallel-edge policy, callback contract, and algorithm result mapping are
explicit and tested.

## Core object model

| Object | Meaning | Use it when |
|---|---|---|
| `PyGraph` | Undirected indexed graph. | Direction does not matter. |
| `PyDiGraph` | Directed indexed graph. | Edge orientation matters. |
| `PyDAG` | Directed graph that checks/prevents cycles according to its contract. | Acyclicity is an invariant, not merely an algorithm precondition. |
| node index | Integer handle into graph storage. | Address topology; never confuse it with payload identity. |
| edge index | Integer handle for one edge. | Preserve parallel-edge identity and update/remove exact edges. |
| node/edge payload | Arbitrary Python object, often called “weight” in APIs. | Store domain data; it is not automatically an algorithmic cost. |

Indices are stable for the lifetime of an item but are not guaranteed
contiguous; removals leave holes and later insertions may reuse an index. Keep a
domain-ID→node-index mapping when callers identify nodes by business keys. Do
not use list position or enumerate `graph.nodes()` as an index map. Open
[indices, payloads, and ownership](references/object-model.md) for the mapping rules.

## Ordered workflow

1. State direction, cycle, self-loop, and parallel-edge requirements.
2. Define domain identity separately from integer graph indices.
3. Choose payload shapes and the callback that converts edge payload to a
   numeric cost when an algorithm needs one.
4. Build topology while retaining returned indices/mappings.
5. Select the exact `graph_*` or `digraph_*` algorithm family and verify its
   return type and unreachable-node behavior.
6. Translate index-keyed results back to domain IDs only at the public boundary.
7. Test removals/holes, parallel edges, direction, missing paths, callback
   failures, and equal-cost ambiguity; benchmark only the real workload.

## Decision map

- Use `multigraph=False` only when at most one edge per endpoint pair is the
  domain rule. Adding a duplicate then updates the existing edge payload rather
  than preserving another relationship.
- Use edge indices when parallel edges require later provenance or mutation.
- Use `graph_*` functions for `PyGraph` and `digraph_*` functions for directed
  graphs when the API provides type-specific families. Do not guess symmetry.
- Map an arbitrary edge payload to the numeric cost the algorithm expects. For
  `digraph_dijkstra_shortest_path_lengths`, pass `edge_cost_fn` as the third
  positional argument: the documented signature makes it positional-only. A
  payload named “weight” can still be a dict, object, or label. Inspect other
  algorithm signatures instead of copying this call shape blindly.
- Use conversion only after listing what must survive: domain IDs, graph attrs,
  parallel keys, isolated nodes, direction, and payload identity.
- Use rustworkx for measured performance-sensitive graph computation or an
  existing rustworkx boundary. Prefer NetworkX when its broader API/ecosystem is
  the actual requirement and no performance evidence justifies conversion.

Read [operations and algorithms](references/operations.md) for construction,
result types, mappings, callbacks, conversion, and traversal-control details.

## Canonical anchor

```python
from dataclasses import dataclass

import rustworkx as rx


@dataclass(frozen=True)
class Arc:
    cost: float
    route_id: str


def build_routes(
    route_ids: list[str],
    arcs: list[tuple[str, str, Arc]],
) -> tuple[rx.PyDiGraph, dict[str, int]]:
    graph = rx.PyDiGraph(multigraph=True)
    index_by_id = {route_id: graph.add_node(route_id) for route_id in route_ids}
    for source, target, arc in arcs:
        graph.add_edge(index_by_id[source], index_by_id[target], arc)
    return graph, index_by_id
```

The payload is a domain object; an algorithm must receive `lambda arc:
arc.cost`. The map preserves business identity even if indices have holes.

## High-risk rules

- Never serialize or persist node indices as permanent domain IDs unless graph
  lifecycle and reuse are explicitly controlled.
- Do not assume `nodes()` position equals an index. Use `node_indices()` and
  `get_node_data(index)` or retained mappings.
- Do not assume removing a node compacts the graph. Test any code that iterates
  a numeric range.
- Do not call an algorithm with the payload object where it expects a numeric
  edge cost callback. Define missing, negative, and nonfinite cost policies.
- Keep directed predecessor/successor semantics distinct. Do not convert to
  undirected just to make an algorithm call succeed.
- In a multigraph, endpoint lookup can return several edges. Preserve/select by
  edge index under an explicit rule.
- Callback-heavy algorithms cross the Python boundary; validate callback return
  types and benchmark rather than assuming every rustworkx call is faster.
- Conversion from NetworkX can change identity representation and multigraph
  details. Assert a semantic round trip, not only node/edge counts.
- Traversal visitors can stop or prune traversal through control exceptions or
  return contracts that are version-sensitive. Inspect installed docs.

## Version grounding and completion

The official API index currently labels rustworkx 0.18.1. The package is not
installed in the foundry, so that is a documentation baseline only. Check the
installed version with `rustworkx.__version__`, then inspect graph constructors and the exact algorithm signature
before coding. Read [verification](references/verification.md).

Completion requires graph-class and index-lifecycle correctness; explicit
payload-to-cost semantics; safe result mapping; tests with holes, parallel
edges, no-path/direction cases, and callbacks; and measured evidence for any
performance claim.

## References

- [Indices, payloads, and ownership](references/object-model.md)
- [Operations and algorithms](references/operations.md)
- [Verification and grounding](references/verification.md)
