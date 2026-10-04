---
name: networkx
description: "Build, analyze, and visualize networks and graphs using NetworkX (Python). Use this skill whenever the user wants to: create graphs or networks, analyze graph properties, compute centrality measures, find shortest paths, detect communities, run graph algorithms, convert graphs to/from matrices or dataframes, visualize networks with matplotlib, import/export graph files (GML, GraphML, GEXF, edgelist, etc.), work with directed or undirected graphs, weighted or multigraphs, perform social network analysis, or do any graph theory computation. Trigger on keywords: networkx, graph, network, nodes, edges, adjacency, shortest path, centrality, community detection, spanning tree, flow, clique, PageRank, bipartite, DAG, topology, graph analysis, social network."
allowed-tools: Bash Read Write Edit
---

# NetworkX Skill — Create and Manipulate Networks

NetworkX (v3.6+) is the standard Python library for graph analysis. This skill covers everything from basic graph creation to advanced algorithms. When in doubt, prefer simple explicit code over clever one-liners — graphs are complex enough on their own.

**References:**
- [algorithms.md](references/algorithms.md) — Algorithm reference by category (centrality, community, flow, etc.)
- [io.md](references/io.md) — File I/O and format conversion reference

---

## 1. Choosing a Graph Class

Pick the right class first — it cannot easily be changed after construction.

```python
import networkx as nx

G  = nx.Graph()          # undirected, no parallel edges
DG = nx.DiGraph()        # directed, no parallel edges
MG = nx.MultiGraph()     # undirected + parallel edges allowed
MD = nx.MultiDiGraph()   # directed + parallel edges allowed
```

| Need | Class |
|---|---|
| Social networks, protein interactions | `Graph` |
| Web graphs, citation networks, DAGs | `DiGraph` |
| Transport networks (multiple routes) | `MultiGraph` |
| Dependency graphs with typed edges | `MultiDiGraph` |

Convert between types:
```python
DG = G.to_directed()    # Graph → DiGraph (each edge becomes two arcs)
G2 = DG.to_undirected() # DiGraph → Graph
```

---

## 2. Building Graphs

### Add Nodes

Any hashable Python object is a valid node: int, str, tuple, frozenset.

```python
G.add_node(1)
G.add_node("Alice", age=30, role="engineer")   # node with attributes
G.add_nodes_from([2, 3, 4])
G.add_nodes_from([
    ("Bob",   {"age": 25, "role": "designer"}),
    ("Carol", {"age": 35, "role": "manager"}),
])
```

### Add Edges

```python
G.add_edge(1, 2)
G.add_edge("Alice", "Bob", weight=0.9, relation="colleague")
G.add_edges_from([(1, 2), (2, 3), (3, 4)])
G.add_edges_from([
    (1, 2, {"weight": 1.5}),
    (2, 3, {"weight": 0.8}),
])
G.add_weighted_edges_from([(1, 2, 1.5), (2, 3, 0.8)])  # shorthand
```

For MultiGraph, `add_edge` returns the edge key (int):
```python
k = MG.add_edge(1, 2, weight=0.5)   # k=0
k = MG.add_edge(1, 2, weight=0.75)  # k=1 (parallel edge)
```

### Remove Nodes and Edges

```python
G.remove_node(1)
G.remove_nodes_from([2, 3])
G.remove_edge(1, 2)
G.remove_edges_from([(1, 2), (2, 3)])
G.clear()  # remove everything
```

### Graph-Level Attributes

```python
G = nx.Graph(name="Social Network", created="2025")
G.graph["description"] = "Friendship graph"
```

---

## 3. Inspecting a Graph

```python
# Size
G.number_of_nodes()   # or len(G)
G.number_of_edges()   # or G.size()

# Nodes and edges (views, not copies)
list(G.nodes)
list(G.nodes(data=True))                   # with attributes
list(G.nodes(data="weight", default=1.0))  # specific attribute

list(G.edges)
list(G.edges(data=True))       # with attributes
list(G.edges(data="weight"))   # specific attribute

# Adjacency
list(G.neighbors(1))         # undirected neighbors
list(G.adj[1])               # same, dict-style
G.adj[1][2]["weight"]        # edge attribute lookup

# DiGraph-specific
list(DG.successors(n))
list(DG.predecessors(n))
list(DG.in_edges(n))
list(DG.out_edges(n))

# Degree
G.degree(1)               # single node
dict(G.degree())          # all nodes → {node: degree}
dict(G.degree(weight="weight"))  # weighted degree

# MultiDiGraph
MD.in_degree(n)
MD.out_degree(n)
```

### Node/Edge Membership

```python
1 in G           # node membership
(1, 2) in G.edges  # edge membership
G.has_node(1)
G.has_edge(1, 2)
```

---

## 4. Attributes: Read and Write

```python
# Read node attribute
G.nodes[1]["color"]

# Write node attribute
G.nodes[1]["color"] = "red"

# Read edge attribute
G[1][2]["weight"]          # Graph / DiGraph
MG[1][2][0]["weight"]      # MultiGraph (key=0)

# Write edge attribute
G[1][2]["weight"] = 4.7

# Bulk set / get with dict or scalar
nx.set_node_attributes(G, {1: "red", 2: "blue"}, name="color")
nx.set_node_attributes(G, 0.0, name="score")          # same value for all

nx.set_edge_attributes(G, {(1,2): 1.5, (2,3): 0.8}, name="weight")

colors = nx.get_node_attributes(G, "color")           # {node: value}
weights = nx.get_edge_attributes(G, "weight")         # {(u,v): value}
```

---

## 5. Graph Views and Subgraphs

Views are live windows — they reflect changes to the original graph without copying data.

```python
# Node-induced subgraph
sub = G.subgraph([1, 2, 3])   # view
sub = G.subgraph([1, 2, 3]).copy()  # independent copy

# Edge-induced subgraph
esub = G.edge_subgraph([(1, 2), (2, 3)])

# Filter view (no copy)
import networkx as nx
heavy = nx.subgraph_view(G, filter_edge=lambda u, v: G[u][v]["weight"] > 0.5)

# Reverse a DiGraph
R = DG.reverse()         # view
R = DG.reverse(copy=True)

# Add useful structural paths/cycles
nx.add_path(G, [10, 11, 12, 13])
nx.add_cycle(G, [20, 21, 22])
nx.add_star(G, [0, 1, 2, 3])  # 0 is the hub
```

---

## 6. Graph Generators

### Classic

```python
nx.complete_graph(5)           # K5
nx.complete_bipartite_graph(3, 4)
nx.cycle_graph(6)
nx.path_graph(5)
nx.star_graph(4)               # hub + 4 leaves
nx.wheel_graph(6)
nx.petersen_graph()
nx.balanced_tree(r=3, h=2)    # 3-ary tree, height 2
nx.barbell_graph(5, 2)        # two K5 joined by path of length 2
nx.ladder_graph(5)
nx.grid_2d_graph(4, 4)        # 4×4 grid
nx.grid_graph(dim=[3, 4, 5])  # 3D grid
nx.hypercube_graph(3)         # 3-cube
nx.empty_graph(10)
nx.null_graph()
nx.trivial_graph()
```

### Random

```python
nx.erdos_renyi_graph(100, 0.15)           # G(n,p)
nx.gnm_random_graph(100, 300)             # G(n,m) — exactly m edges
nx.barabasi_albert_graph(100, 3)          # preferential attachment, scale-free
nx.watts_strogatz_graph(30, 4, 0.1)      # small-world
nx.newman_watts_strogatz_graph(30, 4, 0.1)
nx.random_regular_graph(3, 20)            # 3-regular, 20 nodes
nx.powerlaw_cluster_graph(50, 2, 0.3)
nx.random_lobster(100, 0.9, 0.9)
nx.random_tree(10)
```

### Social Network Datasets

```python
nx.karate_club_graph()          # Zachary's karate club (34 nodes)
nx.florentine_families_graph()  # Renaissance Florence
nx.les_miserables_graph()       # character co-appearances
nx.davis_southern_women_graph() # bipartite affiliation
```

### Geometric

```python
nx.random_geometric_graph(50, 0.2)   # nodes in unit square, connect if dist < 0.2
nx.waxman_graph(50)                  # internet topology model
nx.geographical_threshold_graph(50, 100)
```

---

## 7. Shortest Paths

Read [references/algorithms.md](references/algorithms.md#shortest-paths) for the full API. Key patterns:

```python
# Unweighted
nx.shortest_path(G, source=1, target=5)         # list of nodes
nx.shortest_path_length(G, source=1, target=5)  # int
nx.has_path(G, 1, 5)

# All paths from one source
paths = nx.single_source_shortest_path(G, source=1)       # {target: path}
lengths = nx.single_source_shortest_path_length(G, source=1)

# All pairs
all_paths = dict(nx.all_pairs_shortest_path(G))
all_lengths = dict(nx.all_pairs_shortest_path_length(G))

# Weighted (Dijkstra)
nx.dijkstra_path(G, 1, 5, weight="weight")
nx.dijkstra_path_length(G, 1, 5, weight="weight")

lengths, paths = nx.single_source_dijkstra(G, source=1, weight="weight")

# Bellman-Ford (handles negative weights, not negative cycles)
nx.bellman_ford_path(G, 1, 5, weight="weight")

# Floyd-Warshall (all-pairs, dense graphs)
dist_matrix = nx.floyd_warshall_numpy(G, weight="weight")  # numpy array

# A* (with heuristic)
def heuristic(a, b): return abs(a[0]-b[0]) + abs(a[1]-b[1])
nx.astar_path(G, (0,0), (3,3), heuristic=heuristic, weight="weight")

# Average path length
nx.average_shortest_path_length(G)
nx.average_shortest_path_length(G, weight="weight")
```

---

## 8. Centrality Measures

Read [references/algorithms.md](references/algorithms.md#centrality) for all ~30 measures. Most return `{node: float}`.

```python
# Degree — fraction of nodes connected to
dc = nx.degree_centrality(G)

# Betweenness — fraction of shortest paths through node
bc = nx.betweenness_centrality(G, normalized=True, weight="weight")
ebc = nx.edge_betweenness_centrality(G, normalized=True)

# Closeness — inverse mean distance to all other nodes
cc = nx.closeness_centrality(G)

# Eigenvector — influence via neighbor influence
ec = nx.eigenvector_centrality(G, max_iter=1000, weight="weight")

# Katz — eigenvector variant with base score
kc = nx.katz_centrality(G, alpha=0.1, beta=1.0)

# PageRank (directed graphs)
pr = nx.pagerank(DG, alpha=0.85, weight="weight")

# Harmonic — handles disconnected graphs
hc = nx.harmonic_centrality(G)

# Sort nodes by centrality
top5 = sorted(bc, key=bc.get, reverse=True)[:5]
```

---

## 9. Community Detection

Read [references/algorithms.md](references/algorithms.md#community) for all methods.

```python
from networkx.algorithms import community

# Louvain (fast, good modularity — best general choice)
comms = community.louvain_communities(G, seed=42)

# Greedy modularity maximization
comms = community.greedy_modularity_communities(G)

# Girvan-Newman (divisive, slow but interpretable)
gn = community.girvan_newman(G)
top_level = next(gn)  # tuple of frozensets, each = a community

# Label propagation (fast, stochastic)
comms = community.label_propagation_communities(G)

# K-clique percolation (overlapping communities)
comms = list(community.k_clique_communities(G, k=3))

# Measure quality
mod = community.modularity(G, comms)
coverage, performance = community.partition_quality(G, comms)

# Convert to node→community dict
node_comm = {}
for i, comm in enumerate(comms):
    for node in comm:
        node_comm[node] = i
```

---

## 10. Graph Analysis Algorithms

### Connectivity

```python
nx.is_connected(G)
nx.number_connected_components(G)
list(nx.connected_components(G))
nx.node_connectivity(G)          # min nodes to disconnect
nx.edge_connectivity(G)          # min edges to disconnect

# Directed
nx.is_strongly_connected(DG)
nx.is_weakly_connected(DG)
list(nx.strongly_connected_components(DG))
list(nx.weakly_connected_components(DG))
```

### Trees and Spanning Structures

```python
nx.is_tree(G)
nx.is_forest(G)

T = nx.minimum_spanning_tree(G, weight="weight")       # Kruskal by default
T = nx.minimum_spanning_tree(G, algorithm="prim")
T = nx.maximum_spanning_tree(G, weight="weight")

list(nx.minimum_spanning_edges(G, weight="weight", data=True))
```

### Cycles and DAGs

```python
nx.is_directed_acyclic_graph(DG)
list(nx.topological_sort(DG))           # linear ordering of DAG nodes
list(nx.all_simple_cycles(DG))
list(nx.simple_cycles(DG))              # directed cycles
nx.find_cycle(G)                        # raises NetworkXNoCycle if none
nx.cycle_basis(G)                       # minimal cycle basis

# DAG operations
nx.ancestors(DG, node)
nx.descendants(DG, node)
nx.dag_longest_path(DG, weight="weight")
nx.transitive_closure(DG)
nx.transitive_reduction(DG)
```

### Cliques

```python
list(nx.find_cliques(G))                    # all maximal cliques (Bron-Kerbosch)
nx.graph_clique_number(G)                   # size of largest clique
list(nx.cliques_containing_node(G, 1))      # cliques containing node 1
nx.node_clique_number(G, 1)                 # size of largest clique with node 1
```

### Flows

```python
flow_value, flow_dict = nx.maximum_flow(G, s=0, t=5, capacity="capacity")
nx.max_flow_min_cut(G, s=0, t=5, capacity="capacity")
nx.minimum_cut(G, s=0, t=5, capacity="capacity")
nx.minimum_cut_value(G, s=0, t=5, capacity="capacity")

# Min-cost flow
nx.min_cost_flow(G)                         # requires demand/capacity/weight attrs
nx.min_cost_flow_cost(G)
```

### Matching

```python
nx.max_weight_matching(G, weight="weight")  # set of (u,v) pairs
nx.maximum_matching(G)
nx.is_perfect_matching(G, matching)
```

### Graph Properties

```python
nx.density(G)                    # edges / possible edges (0.0–1.0)
nx.diameter(G)                   # longest shortest path
nx.radius(G)
nx.center(G)                     # nodes with eccentricity == radius
nx.periphery(G)                  # nodes with eccentricity == diameter
nx.eccentricity(G)               # {node: max shortest path}
nx.average_clustering(G)
nx.transitivity(G)               # fraction of triangles to triples
nx.clustering(G)                 # {node: local clustering coefficient}
nx.triangles(G)                  # {node: number of triangles}

nx.is_bipartite(G)
sets = nx.bipartite.sets(G)      # (top_nodes, bottom_nodes)

nx.is_eulerian(G)
nx.is_planar(G)
nx.is_chordal(G)
nx.is_regular(G)
nx.is_tree(G)
```

### Coloring

```python
colors = nx.coloring.greedy_color(G, strategy="largest_first")
# strategies: largest_first, smallest_last, DSATUR, random_sequential, ...
num_colors = max(colors.values()) + 1
```

### Link Prediction

```python
preds = nx.resource_allocation_index(G, [(1,5), (2,7)])
preds = nx.jaccard_coefficient(G, [(1,5)])
preds = nx.adamic_adar_index(G, [(1,5)])
preds = nx.preferential_attachment(G, [(1,5)])
for u, v, score in preds:
    print(u, v, score)
```

### Graph Operators

```python
nx.compose(G1, G2)                      # union, keep attrs, merge common nodes
nx.union(G1, G2)                        # union, node sets must be disjoint
nx.intersection(G1, G2)                 # edges in both
nx.difference(G1, G2)                   # edges in G1 but not G2
nx.complement(G)                        # all non-edges become edges
nx.cartesian_product(G1, G2)
nx.tensor_product(G1, G2)
nx.strong_product(G1, G2)
nx.power(G, k)                          # connect nodes reachable in k steps
```

### Traversal

```python
list(nx.bfs_edges(G, source=0))
list(nx.dfs_edges(G, source=0))
list(nx.bfs_tree(G, source=0).edges())
list(nx.dfs_tree(G, source=0).edges())
dict(nx.bfs_predecessors(G, source=0))
dict(nx.bfs_successors(G, source=0))
nx.bfs_layers(G, sources=[0])           # generator of node-layers
```

---

## 11. Converting Graphs

```python
# NumPy adjacency matrix
A = nx.to_numpy_array(G, nodelist=sorted(G), weight="weight")
G2 = nx.from_numpy_array(A, create_using=nx.DiGraph)

# SciPy sparse (efficient for large graphs)
S = nx.to_scipy_sparse_array(G, format="csr", weight="weight")
G2 = nx.from_scipy_sparse_array(S)

# Pandas adjacency matrix
df = nx.to_pandas_adjacency(G, weight="weight")
G2 = nx.from_pandas_adjacency(df)

# Pandas edge list
edf = nx.to_pandas_edgelist(G, source="from", target="to")
G2 = nx.from_pandas_edgelist(edf, source="from", target="to",
                              edge_attr=True,
                              create_using=nx.DiGraph)

# Dict of dicts (adjacency dict)
d = nx.to_dict_of_dicts(G)
G2 = nx.from_dict_of_dicts(d)

# Dict of lists
d = nx.to_dict_of_lists(G)
G2 = nx.from_dict_of_lists(d)

# Edge list (list of tuples)
edges = list(G.edges(data=True))
G2 = nx.from_edgelist([(u,v) for u,v,_ in edges])
```

---

## 12. File I/O

Read [references/io.md](references/io.md) for format details and options.

```python
# GraphML (recommended for cross-tool compatibility)
nx.write_graphml(G, "graph.graphml")
G = nx.read_graphml("graph.graphml")

# GML (human-readable)
nx.write_gml(G, "graph.gml")
G = nx.read_gml("graph.gml")

# GEXF (Gephi)
nx.write_gexf(G, "graph.gexf")
G = nx.read_gexf("graph.gexf")

# Edge list (simplest, loses attributes beyond weight)
nx.write_edgelist(G, "edges.txt", data=True)
G = nx.read_edgelist("edges.txt", nodetype=int, data=[("weight", float)])

# Weighted edge list shorthand
nx.write_weighted_edgelist(G, "edges.txt")
G = nx.read_weighted_edgelist("edges.txt", nodetype=int)

# Adjacency list
nx.write_adjlist(G, "adj.txt")
G = nx.read_adjlist("adj.txt", nodetype=int)

# Pajek
nx.write_pajek(G, "graph.net")
G = nx.read_pajek("graph.net")

# JSON (node-link format)
import json
from networkx.readwrite import json_graph
data = json_graph.node_link_data(G)
json.dump(data, open("graph.json", "w"))
G = json_graph.node_link_graph(json.load(open("graph.json")))

# Text for debugging
nx.write_network_text(G)
```

---

## 13. Drawing and Visualization

NetworkX's built-in drawing is for quick exploration — use Gephi or Cytoscape for publication-quality output.

### Basic Drawing

```python
import matplotlib.pyplot as plt

nx.draw(G)
nx.draw(G, with_labels=True, node_color="skyblue", node_size=500,
        font_size=10, edge_color="gray")
plt.savefig("graph.png", dpi=150, bbox_inches="tight")
plt.show()
```

### Layout Algorithms

Choose a layout, then draw with full control:

```python
pos = nx.spring_layout(G, k=0.5, seed=42)        # Fruchterman-Reingold (default)
pos = nx.kamada_kawai_layout(G)                   # aesthetically good, slower
pos = nx.circular_layout(G)                       # nodes on circle
pos = nx.shell_layout(G, nlist=[inner, outer])    # concentric circles
pos = nx.spectral_layout(G)                       # eigenvectors of Laplacian
pos = nx.random_layout(G, seed=42)
pos = nx.planar_layout(G)                         # only if graph is planar
pos = nx.bfs_layout(G, start=0)                   # tree-like layout from BFS
pos = nx.spiral_layout(G)
pos = nx.bipartite_layout(G, nodes=top_nodes)     # two-column layout
```

### Fine-Grained Drawing

```python
fig, ax = plt.subplots(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)

# Color nodes by attribute
node_colors = [G.nodes[n].get("color", "lightblue") for n in G]
node_sizes  = [G.degree(n) * 50 + 100 for n in G]

nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                       node_size=node_sizes, alpha=0.8, ax=ax)
nx.draw_networkx_edges(G, pos, edge_color="gray",
                       width=1.5, alpha=0.6, ax=ax,
                       arrows=True, arrowsize=20)   # arrows for DiGraph
nx.draw_networkx_labels(G, pos, font_size=9, ax=ax)

# Edge labels (e.g. weight)
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                              font_size=7, ax=ax)

ax.set_title("My Network")
ax.axis("off")
plt.tight_layout()
plt.savefig("network.png", dpi=150)
```

### Color Nodes by Centrality

```python
bc = nx.betweenness_centrality(G)
node_color = [bc[n] for n in G]
pos = nx.spring_layout(G, seed=42)

nx.draw_networkx(G, pos, node_color=node_color,
                 cmap=plt.cm.plasma, with_labels=True)
sm = plt.cm.ScalarMappable(cmap=plt.cm.plasma,
                            norm=plt.Normalize(min(bc.values()), max(bc.values())))
plt.colorbar(sm, label="Betweenness Centrality")
```

---

## 14. Common Patterns and Recipes

### Build Graph from Pandas DataFrame

```python
import pandas as pd
df = pd.read_csv("edges.csv")   # columns: source, target, weight
G = nx.from_pandas_edgelist(df, source="source", target="target",
                             edge_attr="weight")
# Add node attributes from a separate dataframe
nodes_df = pd.read_csv("nodes.csv")   # columns: id, label, type
for _, row in nodes_df.iterrows():
    G.nodes[row["id"]].update(row.drop("id").to_dict())
```

### Largest Connected Component

```python
largest_cc = max(nx.connected_components(G), key=len)
G_main = G.subgraph(largest_cc).copy()
```

### Ego Network (Local Neighborhood)

```python
ego = nx.ego_graph(G, node, radius=2)   # node + all neighbors within 2 hops
```

### Bipartite Projection

```python
B = nx.Graph()
B.add_nodes_from(top_nodes, bipartite=0)
B.add_nodes_from(bottom_nodes, bipartite=1)
B.add_edges_from(edge_list)

from networkx.algorithms import bipartite
P = bipartite.projected_graph(B, top_nodes)      # project onto top nodes
P = bipartite.weighted_projected_graph(B, top_nodes)  # with edge weights
```

### Weighted Graph from Co-occurrence

```python
from itertools import combinations
G = nx.Graph()
for group in groups:   # groups = list of lists
    for a, b in combinations(group, 2):
        if G.has_edge(a, b):
            G[a][b]["weight"] += 1
        else:
            G.add_edge(a, b, weight=1)
```

### Export Summary Statistics

```python
stats = {
    "nodes": G.number_of_nodes(),
    "edges": G.number_of_edges(),
    "density": nx.density(G),
    "connected": nx.is_connected(G),
    "components": nx.number_connected_components(G),
    "avg_clustering": nx.average_clustering(G),
    "avg_degree": sum(d for _, d in G.degree()) / G.number_of_nodes(),
}
if nx.is_connected(G):
    stats["diameter"] = nx.diameter(G)
    stats["avg_path_length"] = nx.average_shortest_path_length(G)
```

---

## 15. Performance Tips

- For large graphs (>100k nodes), prefer `nx.generators` over building node-by-node.
- `nx.to_scipy_sparse_array()` is much faster than `nx.to_numpy_array()` for sparse graphs.
- `nx.betweenness_centrality(G, k=200)` uses sampling for faster approximation on big graphs.
- Use `G.subgraph(nodes)` (view, no copy) instead of `.copy()` when read-only access is enough.
- For all-pairs operations, check if the graph is connected first — disconnected graphs return `inf` distances, which crashes `average_shortest_path_length`.
- Set `seed=` on random generators and layout algorithms for reproducibility.
- `nx.is_directed()`, `nx.is_weighted()`, `nx.is_empty()` are fast graph-property checks.

---

## Installation

```bash
pip install networkx
pip install networkx[default]   # includes matplotlib, scipy, numpy, pandas
pip install networkx[extra]     # adds pydot, lxml, gdal
```

Import convention:
```python
import networkx as nx
from networkx.algorithms import community  # community detection
from networkx.algorithms import bipartite  # bipartite tools
```
