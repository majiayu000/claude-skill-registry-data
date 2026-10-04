---
name: build-kg
description: Build a knowledge graph from any topic. Generates an ontology, discovers sources, crawls, chunks, loads, and parses into Apache AGE (PostgreSQL).
argument-hint: [topic]
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
---

Build a knowledge graph for: **$ARGUMENTS**

Activate the virtual environment before every Python command: `. venv/bin/activate && <command>`.

---

## Phase 0: Init

1. Sanitize the topic into a graph-safe name (lowercase, underscores, no special chars).
   Example: "kubernetes networking" becomes `kubernetes_networking`.
2. Create the working directory:
   ```
   mkdir -p kg_builds/$GRAPH_NAME
   ```
3. Update `AGE_GRAPH_NAME=$GRAPH_NAME` in `.env`.
4. Initialize the graph schema:
   ```
   python -m build_kg.setup_graph
   ```

---

## Phase 0.5: Ontology Generation

Design a domain ontology for **$ARGUMENTS**. This is the most important phase.

1. Identify 3-6 **node types** for the core entities. For each:
   - `label`: PascalCase (e.g. `Component`, `Algorithm`)
   - `description`: what this node represents
   - `properties`: key-value pairs with types (`string`, `integer`, `float`, `boolean`, `json`)

2. Identify 3-8 **edge types**. For each:
   - `label`: UPPER_SNAKE_CASE (e.g. `USES`, `DEPENDS_ON`)
   - `source` and `target`: node labels
   - `description`: what the relationship means

3. Choose a `root_node`: the primary node type that maps 1:1 to source fragments.

4. Write the `json_schema`: the exact JSON format the LLM should output.

5. Save as `kg_builds/$GRAPH_NAME/ontology.yaml`:

```yaml
description: "<Topic> knowledge graph ontology"
nodes:
  - label: "NodeType1"
    description: "..."
    properties:
      name: "string"
      category: "string"
  - label: "NodeType2"
    description: "..."
    properties:
      name: "string"
edges:
  - label: "RELATIONSHIP_NAME"
    source: "NodeType1"
    target: "NodeType2"
    description: "..."
root_node: "NodeType1"
json_schema: |
  {
    "entities": [
      {"_label": "NodeType1|NodeType2", "name": "...", "category": "..."}
    ],
    "relationships": [
      {"_label": "RELATIONSHIP_NAME", "_from_index": 0, "_to_index": 1}
    ]
  }
```

6. Reinitialize the graph with the ontology:
   ```
   python -m build_kg.setup_graph --ontology kg_builds/$GRAPH_NAME/ontology.yaml
   ```

---

## Phase 1: Discover Sources

Find 5-15 authoritative sources about **$ARGUMENTS** using web search.

1. Search with multiple queries:
   - `"$ARGUMENTS" official documentation`
   - `"$ARGUMENTS" comprehensive guide`
   - `"$ARGUMENTS" reference manual`
   - `"$ARGUMENTS" tutorial overview`
   - `"$ARGUMENTS" specification`

2. Evaluate each result: Is it authoritative? Does it have substantial text? Is it crawlable?

3. Organize into priority tiers:
   - **P1**: Official docs, specs, reference manuals (depth 2-3, up to 50 pages)
   - **P2**: Tutorials, guides, educational content (depth 1-2, up to 20 pages)

4. Create `kg_builds/$GRAPH_NAME/manifest.json`:
```json
{
  "topic": "$ARGUMENTS",
  "graph_name": "$GRAPH_NAME",
  "sources": [
    {
      "source_name": "descriptive_short_name",
      "url": "https://...",
      "title": "Page Title",
      "authority": "Organization Name",
      "jurisdiction": "",
      "doc_type": "documentation",
      "priority": "P1",
      "depth": 2,
      "max_pages": 50,
      "delay": 1500
    }
  ],
  "defaults": {
    "jurisdiction": "",
    "authority": "",
    "doc_type": "documentation"
  }
}
```

5. Gap analysis: check all ontology node types have source coverage. Search for more if needed.

---

## Phase 2: Crawl

For each source in the manifest:
```
build-kg-crawl --url "$URL" --output kg_builds/$GRAPH_NAME/crawled/$SOURCE_NAME --depth $DEPTH --pages $MAX_PAGES --delay $DELAY --format markdown
```

If a crawl fails, note it and continue. Do not retry more than once.

---

## Phase 3: Chunk

```
build-kg-chunk kg_builds/$GRAPH_NAME/crawled kg_builds/$GRAPH_NAME/chunks --strategy by_title --max-chars 1000
```

---

## Phase 4: Load

```
build-kg-load kg_builds/$GRAPH_NAME/chunks --manifest kg_builds/$GRAPH_NAME/manifest.json
```

---

## Phase 5: Parse

**Small datasets (< 500 fragments) — sync:**
```
build-kg-parse --ontology kg_builds/$GRAPH_NAME/ontology.yaml
```

**Large datasets (500+ fragments) — batch (50% cheaper):**
```
build-kg-parse-batch prepare --ontology kg_builds/$GRAPH_NAME/ontology.yaml --output kg_builds/$GRAPH_NAME/batch_requests.jsonl
build-kg-parse-batch submit kg_builds/$GRAPH_NAME/batch_requests.jsonl
build-kg-parse-batch status $BATCH_ID --watch
build-kg-parse-batch process $BATCH_ID --ontology kg_builds/$GRAPH_NAME/ontology.yaml
```

---

## Phase 6: Report

1. Count nodes by type:
```sql
SELECT * FROM cypher('$GRAPH_NAME', $$ MATCH (n) RETURN label(n) AS type, count(*) AS total $$) AS (type agtype, total agtype);
```

2. Count edges by type:
```sql
SELECT * FROM cypher('$GRAPH_NAME', $$ MATCH ()-[r]->() RETURN type(r) AS rel, count(*) AS total $$) AS (rel agtype, total agtype);
```

3. Show example subgraphs:
```sql
SELECT * FROM cypher('$GRAPH_NAME', $$ MATCH (a)-[r]->(b) RETURN a, type(r), b LIMIT 10 $$) AS (a agtype, rel agtype, b agtype);
```

4. Present: topic, graph name, ontology summary, sources crawled, fragments loaded, node/edge counts by type, example Cypher queries, and cost estimate.
