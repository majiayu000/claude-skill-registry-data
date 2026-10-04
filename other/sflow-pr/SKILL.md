---
name: sflow-pr
description: Preview deterministic pull-request text or explicitly create and update the governed Story pull request.
disable-model-invocation: true
argument-hint: "[WORK-ID] [describe|create]"
---
# Prepare or publish a pull request

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

1. Inspect Story status, finalization, remote branch, and pending publication before any PR operation.
2. Use `singularity-flow pr describe <WORK-ID> --format markdown` for deterministic local text.
3. Before a network write, show the exact head, base, title, body, and existing-PR state. Require explicit confirmation, then run `singularity-flow pr <WORK-ID> --create` or `singularity-flow pr describe <WORK-ID> --write --yes` as selected.
4. Report the PR URL and exact head commit. Never merge, force-push, or change the selected base branch. Use `/sf-stack` for Epic dependency order.
