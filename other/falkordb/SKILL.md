---
name: falkordb
description: Vector + graph hybrid database combining Redis-compatible graph queries with vector similarity search for curriculum knowledge graphs and semantic retrieval.
---

# FalkorDB

**Version:** 4.18.11+ | **Last Updated:** 2026-09-26  (verified live via browserbase + github.com/FalkorDB/FalkorDB/releases)
**Latest release:** 2026-06-24 by @swilly22 (commit e78f370)  https://github.com/FalkorDB/FalkorDB/releases/tag/v4.18.11

## Overview

FalkorDB provides hybrid vector-graph capabilities for the Cianfhoghlaim platform, combining Cypher queries with vector similarity search for curriculum knowledge graphs.

| Feature | Description |
|---------|-------------|
| Cypher Queries | Redis Graph compatible |
| Vector Search | Embedded similarity search |
| Hybrid Retrieval | Graph + vector combined |
| Low Latency | Sub-millisecond queries |

## When to Use This Skill

Activate when users need:

- "Query curriculum knowledge graph with Cypher"
- "Combine graph traversal with semantic search"
- "Build hybrid retrieval for RAG"
- "Store embeddings in graph nodes"
- "Fast prerequisite lookups"

## Project Integration

### Infrastructure Location

| Component | Path |
|-----------|------|
| Stack Config | `bonneagar/storage/falkordb/` |
| MCP Config | `.mcp.json` (neo4j entry) |

### Connection Details

```
Host: falkordb.cianfhoghlaim.ie
Port: 7687 (Bolt)
User: falkordb
```

## Core Concepts

### 1. Basic Connection

```python
from falkordb import FalkorDB

# Connect to FalkorDB
db = FalkorDB(host="falkordb.cianfhoghlaim.ie", port=6379)   # canonical Redis RESP port; Bolt optional via /integration/bolt-support.html
graph = db.select_graph("curriculum")
```

### 2. Graph Creation

```python
# Create curriculum nodes
graph.query("""
    CREATE (t:Topic {
        name: 'Algebra',
        subject: 'Mathematics',
        level: 'Junior Cycle'
    })
""")

# Create prerequisite relationship
graph.query("""
    MATCH (a:Topic {name: 'Algebra'})
    MATCH (b:Topic {name: 'Equations'})
    CREATE (a)-[:PREREQUISITE_FOR]->(b)
""")
```

### 3. Vector Embeddings in Nodes

```python
import numpy as np

# Store embedding in node
embedding = get_embedding("Algebra fundamentals")
graph.query("""
    MATCH (t:Topic {name: 'Algebra'})
    SET t.embedding = $embedding
""", {"embedding": embedding.tolist()})

# Create vector index
graph.query("""
    CREATE VECTOR INDEX topic_embedding
    ON (t:Topic)
    FOR (t.embedding)
    OPTIONS {dimension: 1536, similarity_function: 'cosine'}
""")
```

### 4. Hybrid Queries

```python
# Combine semantic search with graph traversal
query_embedding = get_embedding("algebraic expressions")

results = graph.query("""
    CALL db.idx.vector.queryNodes('topic_embedding', 5, $embedding)
    YIELD node, score
    MATCH (node)-[:PREREQUISITE_FOR*1..3]->(related)
    RETURN node.name, related.name, score
    ORDER BY score DESC
""", {"embedding": query_embedding.tolist()})
```

## Cianfhoghlaim-Specific Usage

### Curriculum Knowledge Graph

```python
# Build curriculum graph from specifications
def build_curriculum_graph(specs):
    for spec in specs:
        # Create subject node
        graph.query("""
            MERGE (s:Subject {name: $subject})
        """, {"subject": spec.subject})

        # Create topic nodes with embeddings
        for topic in spec.topics:
            embedding = get_embedding(topic.description)
            graph.query("""
                MERGE (t:Topic {name: $name})
                SET t.level = $level,
                    t.embedding = $embedding
                WITH t
                MATCH (s:Subject {name: $subject})
                MERGE (s)-[:CONTAINS]->(t)
            """, {
                "name": topic.name,
                "level": spec.level,
                "embedding": embedding.tolist(),
                "subject": spec.subject
            })
```

### RAG with Graph Context

```python
async def curriculum_rag(question: str):
    # Step 1: Vector search for relevant topics
    q_embedding = get_embedding(question)
    topics = graph.query("""
    CALL db.idx.vector.queryNodes('Topic', 'embedding', 5, vecf32($embedding_list))
        YIELD node, score
        RETURN node.name, node.level, score
    """, {"embedding": q_embedding.tolist()})

    # Step 2: Expand with graph context
    context = graph.query("""
        MATCH (t:Topic)-[:PREREQUISITE_FOR*0..2]-(related)
        WHERE t.name IN $topics
        RETURN t.name, collect(related.name) as prerequisites
    """, {"topics": [t["node.name"] for t in topics]})

    # Step 3: Generate response with context
    return await generate_response(question, context)
```

## Best Practices

1. **Index frequently queried properties** - Improves Cypher performance
2. **Batch vector operations** - Minimize API calls for embeddings
3. **Use MERGE for idempotency** - Safe concurrent writes
4. **Limit traversal depth** - Prevent expensive queries

## Resources

- **Documentation:** https://docs.falkordb.com
- **Cypher Reference:** https://docs.falkordb.com/cypher
- **MCP Integration:** Configured as `neo4j` in `.mcp.json`
- **Related Skills:** memgraph, lancedb, graphiti

## Graphiti (canonical agentic-memory backend — 2026)

```bash
pip install graphiti-core[falkordb]
```

```python
from graphiti_core import Graphiti
# Canonical URI: falkor://host:port  (Cloud: falkor://your-instance.falkordb.cloud:6379)
graphiti = Graphiti(uri="falkor://falkordb:6379")
await graphiti.build_indices_and_constraints()  # one-time
# Per-tenant isolation (NEW since Wave 1):
graphiti_t1 = Graphiti(uri="falkor://falkordb:6379", graph_name="curriculum_tenant_a")
```

## Vector on relationships (NEW in v4.18.11)

```cypher
CALL db.idx.vector.queryRelationships(
  'PREREQUISITE_FOR', 'text_embedding', 5, vecf32([...])
) YIELD relationship, score
```

## Production drift alert (open since Wave 1)

`infrastructure/stacks/falkordb/compose.yaml` does NOT currently load `vector.so` — vector queries will silently fail in prod until `command: ["falkordb", "--loadmodule", "/etc/falkordb/vector.so"]` is added. Track via `openspec/changes/.../falkordb-vector-so-loadmodule.yaml`.

## Resources  (verified 2026-06-29)

- **Documentation:** https://docs.falkordb.com  (Homepage; primary path `/<section>/<topic>.html`)
- **Cypher Reference:** https://docs.falkordb.com/cypher/indexing/vector-index.html
- **Graphiti integration page:** https://docs.falkordb.com/agentic-memory/graphiti.html
- **Algorithms index:** https://docs.falkordb.com/algorithms/  (10 procedures: BFS, SPpath, SSpath, MSF, PageRank, BetweennessCentrality, HarmonicCentrality, WCC, CDLP, MaxFlow)
- **Releases:** https://github.com/FalkorDB/FalkorDB/releases  (latest v4.18.11 / 2026-06-24)
- **Anchor patterns:**
    - Vector query nodes: `/cypher/indexing/vector-index.html`
    - Vector on relationships: `/cypher/indexing/vector-index.html#query-vector-index` (`queryRelationships` procedure)
    - Agentic memory: `/agentic-memory/graphiti.html`, `/agentic-memory/cognee.html`, `/agentic-memory/mem0.html`
