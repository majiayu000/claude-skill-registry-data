---
name: sflow-visual
description: Inspect visual-assurance status or compare expected and actual governed visual evidence.
disable-model-invocation: true
argument-hint: "status | compare --expected <record> --actual <record>"
---
# Inspect visual assurance

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

1. Run `singularity-flow visual status --json` for a read-only inventory.
2. For comparison, require explicit expected and actual records and run `singularity-flow visual compare --expected <EXPECTED> --actual <ACTUAL> --json`.
3. Preserve profile, viewport, source hashes, thresholds, mismatches, evidence paths, and readiness exactly.
4. Never claim a screenshot comparison proves functional correctness. Use `/sf-mcp` when evidence must first be captured or attested.

