---
name: sflow-revision
description: Inspect installed Revision Loop capabilities, activation state, or attachment boundaries without starting a loop.
disable-model-invocation: true
argument-hint: "capabilities | activation | attachments"
---

# Inspect Revision Loop readiness

<!-- sflow-output-contract: concise-relay -->
**Output contract:** Relay requested CLI fields or output faithfully; preserve warnings/errors and only the explanations required below.
<!-- sflow-execution-boundary -->
**Boundary:** machine-local; no repository or Story required. Use explicit arguments or SFlow-returned paths; never search `$HOME` or infer a repository.

1. Require exactly one explicit action: `capabilities`, `activation`, or `attachments`. Do not infer a mutating action from a question.
2. For `capabilities`, run `singularity-flow revision capabilities --json`. This is a machine-local, read-only description of the installed execution profile.
3. For `attachments`, run `singularity-flow revision attachments capabilities --json`. This describes supported intake only; it does not require or register a Story attachment.
4. For `activation`, run `singularity-flow workspace current --json`. Use only a returned `repositoryPath` as cwd, then run `singularity-flow revision activation --json`. If no repository is selected, report that exact prerequisite and stop; never search for one.
5. Relay the result and stop. `eligible: true` means only that this installed guarded profile passed its declared checks; it grants no publication, approval, merge, or deployment authority. Never preview/register/remove attachments, create a Candidate, execute a revision, modify opt-in configuration, publish, approve, commit, or push.
