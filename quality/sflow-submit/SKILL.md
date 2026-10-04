---
name: sflow-submit
description: Validate and submit the active Singularity Flow phase for human approval, registering changed artifacts and running configured quality commands.
disable-model-invocation: true
argument-hint: "[--skip-checks only when explicitly authorized]"

---
# Submit

<!-- sflow-output-contract: governed-review -->
**Output contract:** Show artifacts, hashes, warnings, and confirmation before a decision.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

`Out of sequence`: stop; humans confirm soft warnings.

1. Run `singularity-flow status <WORK-ID> --submission-readiness --json`. Require `resultType: sflow-submission-readiness`, matching work/phase, `draftExists`, `draftModified`, `publicationRecorded`, `nextSkill`, `nextCommand`. Trust `lifecycleReady`; equal generation while `in_progress` is ready. Never republish.
2. Generation zero: **Seeded draft — not published**. `lifecycleReady: true`: **Published generation <N> — ready to submit**. Otherwise disable Submit; `classification: generation-required`: **Generate and publish <Phase>**, returned `nextSkill`, stop. Never generate/publish here.
3. Specification/planning: `singularity-flow review-source status <phase> --json`. Unless `not-required`/`ready`, stop; show findings and `/sf-review-source <phase>` / `singularity-flow review-source context <phase> --json`. Corrections need publication; reviewer reports are not approval.
4. `confirmationRequired: true`: show full warning and returned Work-ID-pinned command; human provides `continue`.
5. Convergence: never generic `singularity-flow submit`. Run returned `singularity-flow story advance` without `--confirm`; show review/digest, stop on unresolved dispositions. Human confirms exact `--confirm sha256:<DIGEST>` once. Changed digest requires fresh review.
6. Run returned Work-ID-pinned submit command. `--skip-checks` requires authorization.
7. On failure show `requiredTestExecution` argv/cwd, exit, bounded stderr/report and guidance. Nonzero exit fails despite passing JUnit. Use `/sf-recover`: authorized environment repair permits retry without republishing unchanged source; changed source/artifacts need reviewed rollover and producer publication. Preserve untracked `.sflow/results/**`; tracked/staged changes require review. Fingerprint refusal plus artifact/check hashes and diagnosed runtime evidence. Stop on an unchanged condition or after three distinct repairs. Never loop quality commands or waive tests/integrity/policy.
8. Run `singularity-flow phase show <phase> --json`; retain `reviewBinding`/`displayBinding`. Reuse bodies only from a complete visible same-chat display with exactly matching non-null `displayBinding`; show fresh `reviewBinding`, checks/warnings. Body reuse never reuses approval consent. Otherwise render all documents/briefs: ID/kind/path/bytes/generation/SHA-256, `--- BEGIN <path> ---` / `--- END <path> ---`. Tool output or summaries are not review. Binary: path/metadata.
9. New chat, changed/null binding, omissions or truncation require full display. Fetch omissions: `singularity-flow documents view <DOCUMENT-ID> --json`; incomplete review cannot offer approval.
10. Report commit/push/hashes/checks/cost; offer `/sf-approve <PHASE-ID> --work-id <WORK-ID>` with real IDs; never approve.

TRP: follow `singularity-flow explain test-recovery`.
