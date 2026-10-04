---
name: kg-extract
description: Extract entities and relations from source files to build a knowledge graph
argument-hint: "<path>"
allowed-tools: Read Glob Grep mcp__claude-flow__agentdb_hierarchical-store mcp__claude-flow__agentdb_causal-edge mcp__claude-flow__agentdb_semantic-route mcp__claude-flow__agentdb_pattern-store mcp__claude-flow__embeddings_generate Bash
---

# KG Extract

Extract entities (classes, functions, modules, types, concepts) and their relations (imports, extends, implements, depends-on, calls) from source files, then store them as a knowledge graph in AgentDB.

## When to use

When you need to build or update a knowledge graph from source code or documentation. Useful for understanding codebase structure, dependency analysis, and impact assessment.

## Steps

1. **Scan files** -- use `Glob` and `Read` to enumerate and read source files at the given path
2. **Identify entities** -- extract classes, functions, modules, types, and config references from each file
3. **Map relations** -- for each entity, determine its relations to other entities:
   - `imports`: follow import/require statements
   - `extends`: class inheritance
   - `implements`: interface implementations
   - `depends-on`: constructor dependencies, injected services
   - `calls`: function/method invocations
   - `references`: documentation mentions, comments
4. **Store in AgentDB** -- call `mcp__claude-flow__agentdb_hierarchical-store` for each entity with metadata (name, type, file, line, description)
5. **Create edges** -- call `mcp__claude-flow__agentdb_causal-edge` for each relation with source, target, relation type, and weight
6. **Report** -- summarize: total entities by type, total relations by type, files scanned

## CLI alternative

```bash
npx @claude-flow/cli@latest memory store --namespace knowledge-graph --key "entity-NAME" --value "METADATA_JSON"
npx @claude-flow/cli@latest memory search --query "entities in auth module" --namespace knowledge-graph
```
