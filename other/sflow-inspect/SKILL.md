---
name: sflow-inspect
description: Inspect the selected Story, progress, documents, evidence, prompt composition, comprehension, shadow Passport, or deterministic proof diagnostics without mutation.
disable-model-invocation: true
argument-hint: "[WORK-ID] [status|progress|documents|prompt|comprehension|passport|proof|gaps|signals|next]"
---
# Inspect governed work

<!-- sflow-output-contract: guided-actions -->
**Output contract:** Use read-only CLI evidence, preserve warnings and ordered actions, and change nothing unless explicitly requested.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. For an explicit Work ID, run `singularity-flow status <WORK-ID> --json` in the Boundary repository without requiring or changing the active Story. Without an ID, run `singularity-flow session status --json`; if selection is ambiguous, show candidates and stop.
2. Route the requested view to the exact applicable read command: `singularity-flow progress`, `singularity-flow documents list`, `singularity-flow show-prompt`, `singularity-flow report`, `singularity-flow nextsteps`, `singularity-flow change show <WORK-ID> --shadow --json`, or `singularity-flow proof status|gaps|signals <WORK-ID> --json`. For comprehension, use `singularity-flow comprehension regions|check|graph --work-id <WORK-ID> --json`; for an exact trace use `singularity-flow comprehension explain clause|file|symbol|change|refusal|generation|test <SUBJECT> --work-id <WORK-ID> --json`. For Story history use `singularity-flow comprehension replay [all|phase <PHASE>|kind <EVENT-KIND>] --work-id <WORK-ID> --json`; do not confuse it with or invoke SGOS Process replay. Never infer the subject, phase, or event kind. For an exact predicate explanation use `singularity-flow proof explain <WORK-ID> <PREDICATE-ID> --json`; never infer the predicate ID. Describe comprehension, shadow Passport, and GDP-M3 proof output as untrusted observe-only diagnostics; never claim that any grants authority. Signals never satisfy predicates or gates. Missing Candidate, proof, AST, or World Model remains an explicit non-blocking gap. With no view, show status, progress, generated artifacts, approvals, warnings, and next actions.
3. Preserve exact artifact paths, hashes, identities, self-approval warnings, model/token availability, and pending-publication state.
4. Do not prepare, publish, submit, approve, reject, synchronize, or edit files. Offer `/sf-continue` for an explicitly reviewed mutation.
