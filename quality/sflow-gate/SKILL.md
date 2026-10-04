---
name: sflow-gate
description: Run the final deterministic governance gate and explain every blocking check without bypassing it.
disable-model-invocation: true
argument-hint: "[--terminal]"
---
# Run the governance gate

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

1. Run `singularity-flow gate $ARGUMENTS` exactly once.
2. Preserve every configuration, artifact, approval, traceability, conformance, protected-path, quality-command, and remote-state finding.
3. Distinguish a failed gate from a command crash and show the exact remediation supplied by the engine.
4. Do not edit lifecycle state, waive checks, approve, retry repeatedly, or claim merge readiness unless the terminal gate passes.

