---
name: sflow-local
description: Create, inspect, review, publish, or independently audit repository-free local signed deliverables.
disable-model-invocation: true
argument-hint: "[start|list|status|freeze|verify|signer-create|trust-export|review|publish|audit]"
---
# Local signed deliverables

<!-- sflow-output-contract: explicit-selection -->
**Output contract:** Collect every required choice explicitly; never infer or preselect; preserve errors, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** machine-local; no repository or Story required. Use explicit arguments or SFlow-returned paths; never search `$HOME` or infer a repository.

This journey is model-free and repository-independent. It creates a private machine-local Git ledger and, after explicit review, a signed deterministic bundle. It does not create a product branch, call a model, use AST or a world model, or claim semantic correctness.

1. With no action, run `singularity-flow local list --json`. For one known ID, run `singularity-flow local status <LOC-ID> --json`.
2. Before `singularity-flow local start`, collect the exact intent, classification, and every input path. Show that inputs are copied into private local storage and never modified. Run only after confirmation: `singularity-flow local start <NAME> --intent <TEXT> --classification <VALUE> --input <PATH> --json`.
3. Tell the user to create results only in the returned `outputDirectory`. Freeze with explicit output paths when required, then verify the returned exact candidate digest.
4. Create a signer and export its public trust key only to explicit absolute paths. Never display, copy, or export the private key.
5. Before review, show the exact candidate digest and signer. Run `singularity-flow local review` only after the user explicitly approves those values.
6. Before publication, show the exact candidate digest, signer, and destination. Run `singularity-flow local publish` only after confirmation. Preserve create-only and idempotency refusals; never overwrite a different file.
7. Audit with an explicit absolute bundle path, trust-key path, and signer ID. Report integrity, signature trust, evidence binding, historical-policy, completeness, and rerun states separately. Do not convert recorded-integrity evidence into a semantic-correctness claim.
8. Stop on remote-device, rerun, repository-adoption, or external-verifier requests: those levels are not implemented and must not be advertised as available.
