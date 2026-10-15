---
name: compute-blast-radius
description: Given a change surface (file list) and a dependency graph, compute directly and transitively impacted tests, identify coverage gaps in the change surface, and emit blast-radius.yaml. Used by test-engineer.
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Grep, Glob
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# compute-blast-radius

Model-invocable skill for test blast-radius computation.

## Purpose

Given (a) a list of files that will change, (b) the dependency graph produced by `build-dependency-graph`, and (c) the test surface produced by `map-test-surface`, compute which tests are directly or transitively affected, which tests are at risk of false pass, and where the change surface has no test coverage at all. Emit `blast-radius.yaml`.

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `change_surface` | yes | List of files expected to change |
| `dependency_graph_path` | yes | Path to dependency-graph.yaml |
| `test_surface_path` | yes | Path to test-surface.yaml |
| `transitive_depth` | optional | Max depth for transitive closure (default 3) |
| `output_base` | yes | Directory to write blast-radius.yaml |

## Process

1. **Read inputs.** Deserialize both YAML inputs. Normalize path forms (absolute vs. relative) to match the change-surface list.

2. **Direct impact.** For each file in change_surface, find test files whose `subjects` include that file (via `subjects_index` in test-surface).

3. **Transitive impact.** Walk the dependency graph out to `transitive_depth`. For each reachable module, collect tests covering any file in that module.

4. **Coverage gaps.** Files in change_surface that have ZERO direct or transitive tests — these are the gaps where `specify-baseline-tests` must author new tests.

5. **Risk tiers.** Classify affected tests:
   - `high` — direct subjects match
   - `medium` — transitive within depth 2
   - `low` — transitive within depth 3

6. **Emit blast-radius.yaml:**

   ```yaml
   change_surface: [ ... ]
   generated_at: "{ISO-8601}"
   directly_affected_tests: [ "{test file}" ]
   transitively_affected_tests:
     - test_file: "{path}"
       via_module: "{module}"
       depth: {n}
   risk_tiers:
     high: [ ... ]
     medium: [ ... ]
     low: [ ... ]
   coverage_gaps:
     - file: "{path}"
       reason: no_direct_or_transitive_tests
   summary:
     direct: {n}
     transitive: {n}
     gaps: {n}
   ```

## Output

```yaml
blast_radius_path: "{output_base}/blast-radius.yaml"
direct_count: {n}
transitive_count: {n}
gap_count: {n}
status: written
```

## Boundaries

- Read-only against the codebase.
- Transitive traversal is bounded by `transitive_depth` — do not exceed it (cost explosion on large graphs).
- You do not specify baseline tests for gaps — that is `specify-baseline-tests`'s job.
