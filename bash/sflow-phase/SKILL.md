---
name: sflow-phase
description: Generate and publish configured artifacts for the active Singularity Flow phase.
disable-model-invocation: true
argument-hint: "[generation focus]"

---
# Generate the active phase

<!-- sflow-output-contract: clarification-and-artifact -->
**Output contract:** Use governed inputs and pinned clarification; publish/show configured artifacts.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

Stop on `Out of sequence`; never bypass a gate.

1. Require `ready`, `phaseAgent`, `repositoryPath`; run `singularity-flow phase show <phase> --json`. Keep Story governed. If `policyVerified` is false, show `policyReason`; stop. If `effectiveAuthoringSkill` is not `/sf-phase`, show `Next in Copilot:` with it and `Terminal equivalent: singularity-flow prepare <phase>`, or that a null route drafts nothing; stop.
2. Run `singularity-flow documents list`.
3. Reuse the governed prompt or run `singularity-flow wm compose --phase <phase>` once. Never infer `--task`; missing intelligence adds zero bytes.
4. Run `singularity-flow clarification status <phase> --json`. For `off`, do not ask or record; continue. For `when-needed`, ask and record only for material ambiguity; otherwise continue. For `required`, use `ask_user`, wait and record before preparation; if unavailable, display the questions and stop. Stage only `{"responses":[...]}` at `git rev-parse --git-path singularity-flow/clarification-responses/<phase>.json`, never in Story context. Delete on success; never pass Markdown.
5. Run `singularity-flow story references verify --work-id <WORK-ID> --json`; read returned `localPath`. Run exact `singularity-flow prepare <phase>` action. Stop on placeholders, templates, padding.
6. Preserve qualified `[WORK-ID:REQ-001]` and `[WORK-ID:AC-001]` through conformance; plan paths. `/sf-code` puts `@clause:WORK-ID:REQ-001` in product source and `@ac:WORK-ID:AC-001` in executable tests.
7. Read `singularity-flow recover <WORK-ID> --phase <phase> --json`; follow current-phase actions. Stop for human confirmation, protected config, or other producer.
8. Run `singularity-flow phase draft-check <phase> --json`, then `singularity-flow phase prepublish <phase> --json`. Correct every agent finding in this Copilot turn from approved evidence; recheck at most three changed fingerprints, stop on an unchanged fingerprint. Obey `correction.class`/`sameTurn`; route non-agent work to its owner. Never invent facts, add padding, delete markers blindly, invoke nested models or overwrite another producer.
9. Publish only when prepublish `status` is `ready`, with configured producer/channel. `ARTIFACT_AUTHORING_INCOMPLETE`: recheck once; retry once if ready. Preserve sanitized `telemetry/<phase>-gen<N>.json`. Never submit/approve.
10. Run `singularity-flow phase show <phase> --json`; report evidence, commit/push, model, cost, bounded preview and hash-bound references. When its `handoff` starts with `/sf-review-source`, run `singularity-flow review-source status <phase> --json`; if required but not `ready`, say **Published generation <N> — source review required**. Otherwise say **Published generation <N> — ready to submit**. next: Copilot `/sf-…` and Shell `singularity-flow …` from each `handoff` entry's `copilotCommand` and `command`. Never submit or approve here.

TRP: read and follow `singularity-flow explain test-recovery`; returned legal actions only.
