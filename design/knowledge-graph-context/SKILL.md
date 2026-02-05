---
name: Knowledge Graph Context
description: |
  Project context from ChromaDB knowledge graph. Triggers on "how does this project work", "architecture", "where is X", "why was Y chosen", "project structure", "component relationships", "design decisions".
version: 2.0.0
---

# Knowledge Graph Context Skill

Access ChromaDB knowledge graph via `coconut-knowledge-mcp`.

## When to Use

- Understand project architecture before changes
- Find where functionality is implemented
- Understand design decisions and rationale
- Learn component relationships
- Discover integration patterns
- Get project context

## Get Collection Name

**CRITICAL**: Collection = `{author}_{repo}` from git remote.

```bash
git remote get-url origin 2>/dev/null | sed -E 's|.*[:/]([^/]+)/([^/.]+)(\.git)?$|\1_\2|' | tr '[:upper:]' '[:lower:]' | tr '-' '_'
```

## Quick Reference

### Search Knowledge

```
chroma_query_documents(
  collection_name="<collection>",
  query_texts=["your question"],
  n_results=5
)
```

### Filter by Type

```
chroma_query_documents(
  collection_name="<collection>",
  query_texts=["your question"],
  n_results=5,
  where={"type": "architecture"}
)
```

### Get Document Count

```
chroma_get_collection_count(collection_name="<collection>")
```

### Get Specific Documents

```
chroma_get_documents(
  collection_name="<collection>",
  ids=["component-auth-service"]
)
```

## Node Types

| Type | Description |
|------|-------------|
| architecture | System structure, design |
| component | Modules, services |
| workflow | Processes, data flows |
| integration | APIs, databases |
| convention | Patterns, naming |
| decision | Choices with rationale |

## Search Strategies

**Architecture**: `where={"type": "architecture"}`
**Components**: `where={"type": "component"}`
**Decisions**: `where={"type": "decision"}`

## Workflow

1. Get collection name from git remote
2. Check collection exists: `chroma_list_collections`
3. Search for context: `chroma_query_documents`
4. If stale: suggest `/coconut-knowledge:update`

## Add New Knowledge

Use `/coconut-knowledge:add` or:

```
chroma_add_documents(
  collection_name="<collection>",
  documents=["content"],
  ids=["type-name"],
  metadatas=[{"name": "...", "type": "...", "tags": "..."}]
)
```

## Troubleshooting

- **No results**: Check collection exists, try broader terms
- **Stale info**: Run `/coconut-knowledge:update`
- **Not initialized**: Run `/coconut-knowledge:init`
