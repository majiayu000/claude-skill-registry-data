---
name: memory-mcp
description: How to use the Memory MCP server to store and retrieve knowledge graph entities, relations, and observations.
---

# Memory MCP Server

The `memory` MCP server provides a persistent knowledge graph memory system for Antigravity. It allows you to store, retrieve, and manage entities, their observations, and their active voice relations to better maintain context across tasks and sessions.

## Configuration

Ensure the server is configured in `mcp_config.json`:

```json
"memory": {
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-memory"
  ]
}
```

## Core Concepts

The Memory MCP operates on a Knowledge Graph consisting of:
- **Entities**: Core concepts, files, components, user preferences, or architectural decisions. Each entity has a `name` and `entityType`.
- **Observations**: Specific facts, notes, or descriptive points attached to an entity.
- **Relations**: Directed connections between entities, describing how they interact. Relations must always be in **active voice** (e.g., `implements`, `depends_on`, `controls`).

## Available Tools

### 1. Discovering and Retrieving Knowledge
- `read_graph`: Read the entire knowledge graph. Use this to get an overview of all stored memory.
- `search_nodes`: Search for nodes based on a text query. Crucial when the graph is large and you need to find specific context quickly.
- `open_nodes`: Retrieve specific nodes by their exact names.

### 2. Storing and Updating Knowledge
- `create_entities`: Create multiple new entities. You must provide `name`, `entityType`, and an array of `observations`.
- `add_observations`: Append new factual observations to existing entities. Useful when learning new details about a known component.
- `create_relations`: Create new relationships between entities. Provide the source (`from`), the destination (`to`), and the `relationType` (in active voice).

### 3. Managing and Pruning Knowledge
- `delete_entities`: Remove entities and all their associated relations. Clean up outdated or incorrect context.
- `delete_observations`: Remove specific observations from an entity.
- `delete_relations`: Remove specific relationships between entities.

## Best Practices for Usage

1. **Search Before Creating**: Always use `search_nodes` before creating a new entity to avoid duplicates (e.g., "Database" vs "DB").
2. **Descriptive Observations**: Treat observations as concise, factual statements. Instead of "is good", use "handles pagination requests using UNION ALL".
3. **Semantic Relations**: Use relations to build an architectural map. For instance, link a UI component to its database table using a `reads_from` or `writes_to` relation.
4. **Iterative Memory Management**: When refactoring code, update the memory graph. If you rename a component or discover a new dependency, use `add_observations` and `create_relations` to keep the persistent context accurate.
