---
name: sflow-validate
description: Validate the selected Singularity Flow repository without changing workflow or Git state.
disable-model-invocation: true

---
# Validate the selected repository

<!-- sflow-output-contract: concise-relay -->
**Output contract:** Relay requested CLI fields or output faithfully; preserve warnings/errors and only the explanations required below.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. In the Boundary repository run `singularity-flow validate` exactly once.
2. Report the validation result without rewriting, repairing, initializing, publishing, committing, or pushing anything.
3. If validation refuses, preserve its Shell and Copilot remediation routes. Do not execute either route unless the user separately requests that action.
4. Stop after the read-only result.
