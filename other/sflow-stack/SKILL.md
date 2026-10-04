---
name: sflow-stack
description: Show or synchronize the dependency-safe Story pull-request and merge stack for an Epic.
disable-model-invocation: true

---

# Govern the Story merge stack

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

For status from a Story repository, run:

`singularity-flow stack status --json`

From the Epic lead repository, refresh live Git state and replicate the resulting stack to every participating repository's orphan state branch:

`singularity-flow stack sync --epic <EPIC-ID> --json`

Display the deterministic order, repository, status, blockers, next Story to merge, unreachable branches, and Epic readiness. Explain that the state branch is a control plane with no application ancestry and must never be merged into `main` or an Epic branch.

Do not merge or force-push. After a Story merge, synchronize the stack again before opening the next pull request.
