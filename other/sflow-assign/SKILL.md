---
name: sflow-assign
description: Assign a governed workflow phase to a named contributor through the deterministic assignment command.
disable-model-invocation: true
argument-hint: "<phase> <assignee>"
---
# Assign a workflow phase

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

1. Require an explicit phase and assignee; never infer either from chat identity or the active agent.
2. Inspect current status and authority with `singularity-flow status --json` before changing the assignment.
3. Run `singularity-flow assign <PHASE> <ASSIGNEE>` with the exact values supplied.
4. Report the durable assignment result and next action. Assignment coordinates work; it never grants approval authority or changes the governed phase agent.

