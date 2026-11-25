---
name: cypher-help
description: Print a cheat-sheet of ready-to-paste Cypher queries TAILORED to this project's actual graph, for the user to run in the Neo4j Browser. Walks the live model (the labels, relationships and properties that are really there) and emits example queries with a one-line explanation each, so a human can explore the graph for their own needs without knowing Cypher.
when_to_use: The user asks how to query the graph, wants example Cypher, asks "what can I ask the graph", wants to explore it in the Neo4j Browser, or says cypher-help.
---

# cypher-help

You are producing a cheat-sheet of Cypher queries the user can paste into the **Neo4j Browser**
(http://localhost:7474) to explore their own graph. The point is that it is TAILORED to what the graph
actually contains, not a generic list: you read the live model first, then emit only examples for the
labels and relationships that are really present, with real ids as sample values so each query runs as
written.

## Driving neoize: call the tools, not a shell path

Every neoize operation runs as a **plugin MCP tool**, so drive it by calling the tool, with nothing on
PATH and no script for the human to run. The `neoize ...` commands named below are the exact CLI the
tools wrap, kept as an optional terminal fallback. The map:

- `graph_status` / `graph_up` / `graph_down`: is the graph up, start it, stop it.
- `load_lessons`: load the authored lessons (`neoize load-lessons`).
- `load_graph`: load the structural .cypher (`neoize load-graph`).
- `rebuild_structure`: regenerate the structure from the code (runs `.neoize/collect.py`).
- `check_lessons` / `check_graph`: the offline validations (`neoize check` / `neoize check-graph`).
- `read_neo4j_cypher` / `get_neo4j_schema`: query the graph and read its shape.

## Step 1 - confirm the graph is up, note the product, read its model

Run `neoize status` (or a query through the MCP server). If it is down, tell the user to `neoize up`
first and stop. `status` prints the **product** this project resolves to and the **read union** this
session uses: the shared layer plus this product, `['shared', '<product>']`. The user reads that union, so
a knowledge query spans both (this project's lessons AND the universal shared ones), while a structural
query stays on this product (the shared layer holds no code). Read the model for the union:

- labels and their counts: `MATCH (n) WHERE n.product IN ['shared','<product>'] RETURN labels(n)[0] AS label, count(*) AS n ORDER BY n DESC`
- relationship types: `CALL db.relationshipTypes()`
- property keys: `CALL db.propertyKeys()`

Do NOT invent examples for a label or relationship that is not in this list. If the product has only the
knowledge layer (Lesson/Topic/Operation) and no structural layer yet, say so and show only the knowledge
queries.

The Neo4j Browser does not bind `$products` or `$product` for you, so open the cheat-sheet by telling the
user to run these two lines ONCE in the Browser, after which every query below runs as pasted:

```
:param products => ['shared', '<product>']
:param product => '<product>'
```

Knowledge queries then scope with `WHERE n.product IN $products` (the shared+project union); structural
queries scope with `{product:$product}` (this project only).

## Step 2 - pick real sample values

So every query runs as-is, pull a couple of real ids to drop into the examples: a Topic id
(`MATCH (t:Topic) RETURN t.id LIMIT 3`), an Operation id, and if a structural layer exists, one id of
the busiest structural label. Use those actual values in the examples rather than a placeholder.

## Step 3 - emit the cheat-sheet, grouped, each query explained

Print copy-paste blocks, each with a one-line "what it answers" above it. Group them. Only include a
group whose nodes/edges exist.

Knowledge queries scope to the union with `$products`; structural queries to `$product` (set once in
Step 1). The `l.product` column is worth returning on knowledge queries, so the user sees which rows are
shared and which are this project's.

**Knowledge layer (always, if any Lesson exists), union of shared and this project:**
- every Topic and how many lessons it carries (the map of what the graph knows)
- all lessons on one topic (use a real topic id): `MATCH (l:Lesson)-[:ANCHORS_TO]->(t:Topic {id:'<real>'}) WHERE l.product IN $products AND t.product IN $products RETURN l.product, l.title, l.body`
- all lessons for one operation (use a real op id)
- lessons that mention a term the user cares about: `MATCH (l:Lesson) WHERE l.product IN $products AND l.body CONTAINS '<term>' RETURN l.product, l.title, l.body`
- the oldest lessons (reconcile candidates): order by `prov_date`

**Structural layer (only for the labels/edges that exist), this project only:** for each relationship type
present, show one traversal in plain terms, for example "which <From> is linked to which <To>":
`MATCH (a:<FromLabel> {product:$product})-[:<REL>]->(b:<ToLabel> {product:$product}) RETURN a.id, b.id`. If
a transitive dependency-style edge exists (a self-referential edge on one label, e.g. DEPENDS_ON), show a
blast-radius walk: `MATCH (x {product:$product, id:'<real>'})<-[:<REL>*]-(d {product:$product}) RETURN DISTINCT d.id`.
If the structural nodes carry lessons, show how to pull the lessons for a node:
`MATCH (l:Lesson {product:$product})-[:ANCHORS_TO]->({product:$product, id:'<real>'}) RETURN l.title, l.body`.

**Schema overview (always):** the whole-graph shape, for orientation:
`CALL db.schema.visualization()` and the label-count query from Step 1.

## Finish

Tell the user these go in the Neo4j Browser at http://localhost:7474 (login neo4j / the local password,
default `neoize-local`). Point them at `.neoize/queries/` for the same queries saved as files, and offer
to add any query they find useful there so it is kept. Keep the whole thing paste-ready: a human who does
not know Cypher should be able to copy a block, run it, and get an answer.
