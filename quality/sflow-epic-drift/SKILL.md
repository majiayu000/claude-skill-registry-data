---
name: sflow-epic-drift
description: Observe Jira drift for an Epic and explicitly adopt Jira observations or prepare a reviewed restore plan without automatic two-way overwrite.
disable-model-invocation: true

---

# Manage Epic Jira drift

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

Use one requested action:

- Observe: `singularity-flow epic drift observe --epic <EPIC-KEY> --json`.
- Adopt the recorded observation into a new governed Git generation: `singularity-flow epic drift adopt --epic <EPIC-KEY> --observation <SHA-256> --json`.
- Prepare a reviewed plan that restores Git-owned fields: `singularity-flow epic drift restore-plan --epic <EPIC-KEY> --json`.

Show changed fields and hashes before any mutation. Never silently copy Jira into Git or Git into Jira.
