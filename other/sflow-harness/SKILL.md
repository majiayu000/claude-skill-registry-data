---
name: sflow-harness
description: Inspect the deterministic reference-expansion harness report without changing governed state.
disable-model-invocation: true

---
# Inspect the reference harness

<!-- sflow-output-contract: concise-relay -->
**Output contract:** Relay requested CLI fields or output faithfully; preserve warnings/errors and only the explanations required below.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. Run `singularity-flow harness report --json`.
2. Preserve every reported checker, fixture, failure, and bounded-reference result.
3. If a reference needs expansion, offer `/sf-show`; do not accept an arbitrary repository path.
4. Do not repair fixtures, rewrite reference records, or mutate workflow state.

