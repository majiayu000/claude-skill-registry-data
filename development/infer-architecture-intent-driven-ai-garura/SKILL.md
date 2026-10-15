---
name: infer-architecture
description: Infer logical architecture from an existing codebase — module structure, design patterns, framework conventions, LLD patterns — and write architecture-inference.yaml. Used by tech-architect in the prepare play.
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Grep, Glob, Bash
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# infer-architecture

Model-invocable skill for architecture inference from a codebase.

## Purpose

Given a project root, scan the codebase and infer its logical architecture: conceptual structure, module boundaries and responsibilities, design patterns in use, framework conventions followed, and LLD patterns (DI, error handling, logging, validation). Emit `architecture-inference.yaml`.

tech-architect previously performed this inline with "perform analysis directly" carved out. This skill replaces that path.

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `project_root` | yes | Codebase root |
| `focus_paths` | optional | List of sub-paths to concentrate on (default: top-level source dirs) |
| `ltm_architecture_path` | optional | Path to core LTM architecture knowledge for pattern recognition |
| `output_base` | yes | Directory to write architecture-inference.yaml |

## Process

1. **Enumerate module structure.** Top-level directories + their roles (derived from content, not naming alone).

2. **Identify design patterns.** Grep for signatures: factories, observers, strategies, repositories, facades, adapters. Record each with `location` + `evidence` (specific file/class demonstrating it).

3. **Identify framework conventions.** From imports, config files (`package.json`, `pyproject.toml`, `go.mod`), and directory names, infer framework(s). Record conventions observed (routing structure, middleware layers, test placement, config loading).

4. **Infer LLD patterns.** Walk representative files to characterize:
   - dependency_injection approach
   - error_handling style
   - logging approach
   - validation strategy
   - async/concurrency model

5. **LTM pattern matching.** If `ltm_architecture_path` is provided, cite matching known patterns with their `_index.md` entry.

6. **Emit architecture-inference.yaml:**

   ```yaml
   project_root: "{project_root}"
   logical_architecture: "{one-paragraph conceptual structure}"
   module_structure:
     - path: "{dir}"
       role: "{what this module does}"
       boundaries: "{what it owns, what it delegates}"
   design_patterns:
     - pattern: "{name}"
       location: "{where}"
       evidence: "{file/class/function}"
   framework_conventions:
     - framework: "{name}"
       conventions: [ "{observed}" ]
   lld_patterns:
     dependency_injection: "{approach}"
     error_handling: "{approach}"
     logging: "{approach}"
     validation: "{approach}"
     async_model: "{approach}"
   ltm_matches:
     - pattern: "{name}"
       ltm_ref: "{_index.md entry}"
   produced_at: "{ISO-8601}"
   ```

## Output

```yaml
architecture_inference_path: "{output_base}/architecture-inference.yaml"
module_count: {n}
pattern_count: {n}
status: written
```

## Boundaries

- Read-only against the codebase.
- Report only patterns supported by concrete evidence — no speculation.
- You do not build the dependency graph (that is `build-dependency-graph`'s job) and do not draft `tech.yaml` (that is `draft-tech-spec`'s job).
