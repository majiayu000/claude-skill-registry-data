---
name: sflow-impact
description: Inspect, classify, attest, verify, compare, and export governed Story delivery measurements without inventing evidence or causal claims.
disable-model-invocation: true
argument-hint: "[status|study|enroll|exposure|evidence|finalize|verify|compare|export|doctor] [ARGS]"

---
# Govern delivery measurement

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. With no arguments, run `singularity-flow impact status`.
2. Before `enroll`, show the engine's suggested complexity/risk signals. Require the user to supply both bands and explicitly request `--confirm`; never confirm or opt out on their behalf.
3. Before `exposure attest`, explain that an attestation is self-reported evidence. Require the phase, exposure level, assurance, and a reason when supplied by the user.
4. Import only a user-selected JSON or YAML evidence envelope. For a raw provider observation, use `singularity-flow impact evidence collect <PROVIDER> <FILE> --commit <FULL-SHA> --run-id <ID>` so the engine creates the strict envelope. Do not rewrite provider observations or replace `unavailable` with estimates.
5. `finalize` is valid only for a closed Story and creates a hash-bound Impact Receipt through the normal publication transaction.
6. For `compare`, preserve the engine's method, evidence grade, privacy-floor refusal, uncertainty interval, guardrail result, and exact inference label. Matched observational and before/after results are not causal.
7. For a prompt-set study, use `singularity-flow impact study prompt-hash <singularity/prompts/FILE.md>` for each reviewed prompt. Never calculate or substitute a hash yourself. Explain that Story assignment is deterministic, the assigned variant is disclosed, and an agent override would contaminate and therefore block the comparison.
8. Mutating operations commit and push through Singularity Flow. Report the commit or pending-publication state and the next valid action.
