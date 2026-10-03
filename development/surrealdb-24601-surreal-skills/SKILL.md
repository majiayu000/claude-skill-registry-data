---
name: surrealdb
description: "Expert SurrealDB 3 skill. Use when working with SurrealDB, SurrealQL queries, multi-model data modeling (document, graph, vector, time-series, geospatial), schema design, graph traversal, vector search, security and permissions, deployment and operations, performance tuning, SDK integration, Surrealism WASM extensions, SurrealMCP, Surrealist IDE, Surreal-Sync migrations, SurrealFS, SurrealKit, or ecosystem integrations such as n8n and CodeMirror."
argument-hint: "[query or topic, e.g. 'graph traversal patterns' or 'vector search with HNSW']"
---

# SurrealDB 3 Expert Skill

Expert-level SurrealDB 3 architecture, development, and operations for GitHub Copilot.

## When Copilot Should Use This Skill

Activate automatically when the user:
- Writes or asks about SurrealQL queries
- Works with `.surql` files
- Designs database schemas for SurrealDB
- Configures SurrealDB deployment or Docker
- Uses SurrealDB SDKs (JavaScript, Python, Go, Rust, Java, Kotlin, .NET, C, PHP, Swift, Ruby)
- Works with graph relationships (RELATE, traversal)
- Implements vector search or RAG patterns
- Configures security, permissions, or access control
- Builds Surrealism WASM extensions
- Migrates data to SurrealDB from other databases
- Connects SurrealDB to MCP hosts, n8n, AI frameworks, or custom editors

## Rules Reference

This skill contains 18 detailed rule files. Read the relevant rule file when
the user's request matches its domain:

| Rule File | When to Load | Domain |
|-----------|-------------|--------|
| [surrealql.md](../../../rules/surrealql.md) | Writing or debugging SurrealQL queries | Full SurrealQL language reference |
| [data-modeling.md](../../../rules/data-modeling.md) | Designing schemas, choosing field types, record IDs | Multi-model schema design patterns |
| [graph-queries.md](../../../rules/graph-queries.md) | RELATE, graph traversal, path expressions | Graph edge and traversal patterns |
| [vector-search.md](../../../rules/vector-search.md) | HNSW indexes, similarity search, embeddings | Vector search and RAG pipelines |
| [security.md](../../../rules/security.md) | Permissions, auth, JWT, access control | Row-level security and auth flows |
| [deployment.md](../../../rules/deployment.md) | Installing, configuring, running SurrealDB | Storage engines, Docker, Kubernetes |
| [performance.md](../../../rules/performance.md) | Slow queries, index strategy, EXPLAIN | Performance tuning and optimization |
| [sdks.md](../../../rules/sdks.md) | Using SurrealDB from application code | JS, Python, Go, Rust, Java, Kotlin, .NET, C, PHP, Swift, Ruby patterns |
| [surrealism.md](../../../rules/surrealism.md) | Writing WASM extensions | Rust to WASM extension development |
| [surrealml.md](../../../rules/surrealml.md) | Working near SurrealML | Preview .surml boundary and native dependency warning |
| [surrealmcp.md](../../../rules/surrealmcp.md) | Connecting AI hosts | MCP tool catalog and deployment |
| [editor-tooling.md](../../../rules/editor-tooling.md) | Editor / IDE support | LSP, tree-sitter, CodeMirror, editor extensions |
| [langchain.md](../../../rules/langchain.md) | LangChain RAG | Python vector store API |
| [ecosystem-integrations.md](../../../rules/ecosystem-integrations.md) | n8n / framework pointers | n8n, AI framework docs, Spectron boundary, Agent Skills |
| [surrealist.md](../../../rules/surrealist.md) | Using the Surrealist IDE/GUI | IDE features and schema designer |
| [surreal-sync.md](../../../rules/surreal-sync.md) | Migrating from other databases | CDC sync from Postgres, Mongo, etc. |
| [surrealfs.md](../../../rules/surrealfs.md) | AI agent filesystem operations | Virtual FS backed by SurrealDB |
| [surrealkit.md](../../../rules/surrealkit.md) | Schema sync, rollouts, seeds, and declarative tests | Desired-state schema management for SurrealDB apps |

## Quick Reference

### SurrealQL Essentials

```surql
-- Create records
CREATE person:alice SET name = 'Alice', age = 30;

-- Graph edges
RELATE person:alice->follows->person:bob SET since = time::now();

-- Traverse graph
SELECT ->follows->person.name AS following FROM person:alice;

-- Vector search (HNSW)
DEFINE INDEX idx_embed ON document FIELDS embedding HNSW DIMENSION 1536 DIST COSINE;
SELECT * FROM document WHERE embedding <|10,40|> $query_vector;

-- Row-level permissions
DEFINE TABLE post SCHEMALESS PERMISSIONS
  FOR select WHERE published = true OR user = $auth.id
  FOR create, update WHERE user = $auth.id;

-- Live queries
LIVE SELECT * FROM person WHERE age > 25;
```

### Key Concepts

- **Record IDs**: `table:id` (e.g., `person:alice`) -- first-class citizens, no JOINs needed
- **Multi-model**: Document + Graph + Vector + Time-series + Geospatial in one DB
- **Graph operators**: `->` (outgoing), `<-` (incoming), `<->` (bidirectional)
- **KNN operator**: `<|K,EF|>` where K=neighbors, EF=search parameter (NOT distance metric)
- **Storage engines**: memory, RocksDB, SurrealKV (time-travel), TiKV (distributed)
- **WASM extensions**: New in v3 -- write Rust, compile to WASM, register with DEFINE MODULE

### Scripts

```bash
# Health check
uv run scripts/doctor.py

# Schema introspection
uv run scripts/schema.py introspect

# Check upstream for updates
uv run scripts/check_upstream.py
```

## Security Notes

- Examples use `root/root` for local development only. Use scoped credentials in production.
- Scripts connect to user-specified endpoints only. No third-party network calls.
- Table names are validated against `[a-zA-Z_][a-zA-Z0-9_]*` before query interpolation.
- Prefer package-manager or container installs over remote shell installers.
