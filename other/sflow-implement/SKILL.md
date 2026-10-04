---
name: sflow-implement
description: Friendly alias for the canonical task-based Singularity Flow code-generation contract.
disable-model-invocation: true
argument-hint: "[implementation focus]"

---
# Implementation alias

<!-- sflow-output-contract: canonical-delegation -->
**Output contract:** Run the canonical skill once and preserve its result and handoff; do not repeat its preflight, authoring, or publication.
<!-- sflow-execution-boundary -->
**Boundary:** machine-local; no repository or Story required. Use explicit arguments or SFlow-returned paths; never search `$HOME` or infer a repository.


Run `/sflow-code` once with the supplied focus and stop when it returns. The canonical skill owns Story resolution, authoring, test evidence, publication, and the next action. Preserve its final result and Copilot/Shell handoff unchanged; this alias must not publish, submit, or approve again or suggest restarting code generation.
