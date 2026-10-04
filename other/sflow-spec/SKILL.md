---
name: sflow-spec
description: Inspect and maintain specification indexes, claims, coverage, acceptance evidence, and traceability.
disable-model-invocation: true
argument-hint: "analyze|claims|coverage|acceptance|tasks|trace"
---
# Work with specification traceability

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

1. Inspect the active work item and approved specification before selecting a subcommand.
2. Use read-only `singularity-flow spec analyze|coverage|trace` directly. State when `analyze --assisted` requests optional model help.
3. Preview index, acceptance, or task-map writes with `--dry-run` when that form is supported, then require the user to request the mutation.
4. Preserve every `SPEC-nnn`, `AC-nnn`, test tag, missing claim, stale evidence reason, and output path.
5. Do not treat generated indexes or model candidates as approved requirements.

