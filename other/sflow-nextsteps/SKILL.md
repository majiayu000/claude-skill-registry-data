---
name: sflow-nextsteps
description: Show ordered next actions from the current workflow state.
---
# Show next actions

<!-- sflow-output-contract: guided-actions -->
**Output contract:** Use read-only CLI evidence, preserve warnings and ordered actions, and change nothing unless explicitly requested.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. In the Boundary repository run `singularity-flow nextsteps <WORK-ID> --json` when the user supplied an ID; otherwise run `singularity-flow nextsteps --json`. A ready Story session is not required for repository initialization, start, resume, or explicit-ID guidance.
2. Present every returned action in order, preserving its `NOW`, `THEN`, or `ALTERNATIVE` timing, `/sf-*` skill, CLI command, and reason.
3. If the repository is not initialized, show initialization followed by start. If no work item is active, show start and resume choices.
4. If publication is pending, show `singularity-flow sync` first because later transitions are blocked.
5. For an active phase, include generation, submission, approval/rejection, and the following phase or completion checks as applicable.
6. Keep this operation read-only. Do not execute any returned action unless the user separately asks to perform it.
7. If the user wants the first valid action executed, point them to the explicitly mutating `/sf-next` command.
