---
name: sflow-watch
description: Watch a governed work item for remote lifecycle changes without modifying its branch or state.
disable-model-invocation: true
argument-hint: "[WORK-ID] [--once]"
---
# Watch governed work

<!-- sflow-output-contract: concise-relay -->
**Output contract:** Relay requested CLI fields or output faithfully; preserve warnings/errors and only the explanations required below.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. Prefer `singularity-flow watch $ARGUMENTS --once --fetch` for one bounded refresh.
2. Start continuous watching only when the user explicitly asks for it and preserve the requested interval.
3. Relay remote phase, approval, publication, and completion changes without inventing progress.
4. Watching is read-only. Do not check out, reset, merge, approve, or repair a branch.

