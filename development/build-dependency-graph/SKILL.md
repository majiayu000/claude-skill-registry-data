---
name: build-dependency-graph
description: Systematically enumerate import and call relationships across a codebase, build a structured dependency graph, and emit both dependency-graph.yaml (structured data) and dependency-graph.md (mermaid diagrams + module clusters). Used by tech-architect.
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Grep, Glob, Bash
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# build-dependency-graph

Model-invocable skill for structured dependency-graph artifact authorship.

## Purpose

Walk import/require/use statements across a codebase, collapse to module-level edges, and write a structured graph plus a visual representation. Emit two artifacts: `dependency-graph.yaml` (data) and `dependency-graph.md` (mermaid + narrative).

Previously carved out of tech-architect as a "core architect capability." This skill owns it now.

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `project_root` | yes | Codebase root |
| `focus_paths` | optional | Sub-paths to include (default: all source dirs) |
| `language_hint` | optional | Language(s) present: py, ts, js, go, java, ... (otherwise auto-detect) |
| `output_base` | yes | Directory to write both artifacts |

## Process

1. **Detect language(s).** From extensions + config files (go.mod, pyproject.toml, package.json).

2. **Enumerate import statements.** Grep systematically by language:
   - Python: `^\s*(from|import)\s+`
   - TS/JS: `^\s*import\s.*from|^\s*const\s.*require\(`
   - Go: `^import\s*\(|^\s*"`  (inside `import ( ... )` blocks)
   - Java: `^import\s+`

3. **Build file-level edges.** `source_file → target_symbol` pairs.

4. **Collapse to module-level edges.** Group by top-level package/directory.

5. **Detect cycles.** Tarjan/Kosaraju over the module graph. Record each SCC with >1 node as a cycle.

6. **Identify hubs.** Modules with fan-in or fan-out above configurable thresholds (defaults: fan-in >= 8, fan-out >= 8).

7. **Emit dependency-graph.yaml:**

   ```yaml
   project_root: "{project_root}"
   generated_at: "{ISO-8601}"
   languages: [ ... ]
   modules:
     - id: "{module-path}"
       files: {count}
       fan_in: {n}
       fan_out: {n}
   edges:
     - from: "{module}"
       to: "{module}"
       weight: {count of file-level edges}
   cycles:
     - modules: [ "...", "..." ]
       size: {n}
   hubs:
     - module: "{id}"
       fan_in: {n}
       fan_out: {n}
       reason: high_fan_in | high_fan_out | both
   ```

8. **Emit dependency-graph.md:**

   - Mermaid `graph LR` of module-level edges
   - Cluster diagrams per top-level package
   - Cycle callout sections with offending module list
   - Hub callouts

## Output

```yaml
dependency_graph_yaml_path: "{output_base}/dependency-graph.yaml"
dependency_graph_md_path: "{output_base}/dependency-graph.md"
module_count: {n}
edge_count: {n}
cycle_count: {n}
status: written
```

## Boundaries

- Read-only.
- Module-level aggregation — do not emit per-file edges in the YAML (too noisy); keep them only in internal computation.
- Mermaid diagrams in the `.md` must remain renderable — cap at ~60 nodes; for larger codebases split by top-level package.
