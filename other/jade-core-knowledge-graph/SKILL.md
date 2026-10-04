---
name: jade-core-knowledge-graph
description: >-
  Core skill that builds a Java Knowledge Graph from `.java` sources using
  tree-sitter-java, enabling impact analysis, rule ordering, and consumer test
  selection in the JADE migration pipeline.
---

# jade-core-knowledge-graph

Universal Java source analyzer that builds a Knowledge Graph from `.java` files using tree-sitter-java. Produces `03.5-knowledge-graph.json` consumed by downstream pipeline phases for impact analysis, semantic verification, rule ordering, and consumer test selection.

## Invocation Contract

```
python .claude/skills/jade-core-knowledge-graph/scripts/build_graph.py --workspace <path> --artifacts-dir <path>
python .claude/skills/jade-core-knowledge-graph/scripts/query_graph.py --graph <path> --query <type> [args...]
```

Exit codes: `0`=success, `1`=partial/no-results, `2`=failure, `3`=env-error.

## Pipeline Phase

**Phase 3.5** -- runs after TOOLING_SCOUT (Phase 3), before SCANNER (Phase 4). Build graph once per migration run.

## Graph Schema

- **Nodes**: One per `.java` file with class_name, package, kind, modifiers, extends, implements, methods (with full signatures), fields, constructors
- **Edges**: 5 types -- `imports`, `extends`, `implements`, `calls`, `type_refs`
- External types (`java.*`, `javax.*`) recorded as edges but never recursed into

## Query Types

| Query | Args | Returns |
|-------|------|---------|
| `dependents` | `--target <file>` | Files importing/referencing target |
| `impact-chain` | `--target <file> --method <name>` | Call sites for a method |
| `rule-scope` | `--files <list>` | `{direct, transitive, total}` |
| `consumer-coverage` | `--files <list> --consumer-map <path>` | Consumer project names |
| `transform-order` | `--rules <list> --rule-files-map <path>` | Topologically sorted rules |

## Python API

```python
from schema import KnowledgeGraph
kg = KnowledgeGraph.load("artifacts/03.5-knowledge-graph.json")
deps = kg.query_dependents("core/AID.java")
calls = kg.query_call_sites("core/Agent.java", "doDelete")
```

## Edge Cases

1. **Parse errors**: File gets partial node (imports via regex fallback). Logged as warning.
2. **Wildcard imports**: Resolved to ALL files in the package (over-approximation).
3. **Overloaded methods**: Call resolution by method name only (conservative).
4. **Anonymous inner classes**: Attached to parent file, not separate nodes.
5. **Generics**: Erased. `List<Agent>` -> type_ref to `Agent`.
6. **Cycles**: Graph is directed, cycles don't break queries.

## Artifact

Writes: `03.5-knowledge-graph.json` to artifacts directory.
Format: `{run_id, generated_at, stats, nodes: {path: {node}}, edges: {type: [edge]}}`.
