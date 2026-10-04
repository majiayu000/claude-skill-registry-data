---
name: sflow-release
description: Prepare a release-readiness artifact with deployment, observability, rollback, communication and a final readiness decision, for the release step or any step that chose this skill.
disable-model-invocation: true
argument-hint: "[target environment or release window]"

---
# Release readiness

<!-- sflow-output-contract: clarification-and-artifact -->
**Output contract:** Use governed inputs and pinned clarification; publish/show configured artifacts.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

1. For the Boundary `phase` with exact `phaseAgent` readiness, run `singularity-flow phase show <phase> --json`. If `policyVerified` is false, show `policyReason`; stop. Continue only if `effectiveAuthoringSkill` is `/sf-release`, or `/sf-phase` with `authoringSkill` null and `<phase>` = `release`; else show `Next in Copilot:` `effectiveAuthoringSkill` and `Terminal equivalent: singularity-flow prepare <phase>`, or that a null route drafts nothing; stop. Its governed workflow is Story context.
2. Run `singularity-flow wm compose --phase <phase> --evidence`; use its complete prompt and available release/operations/security grounding. Missing/unreachable/stale WM means zero-context evidence and ordinary repository access. Show returned recovery as optional; never run it here or block release on it. Never derive `--task` from Story prose.
3. Read the approved inputs the composed prompt names and the deployment locations selected by the grounding package. Obey `singularity-flow clarification status <phase> --json` before preparation.
4. Run `singularity-flow prepare <phase>`; complete the release report and every artifact-set member it returns. When the step declares a `verification/` member, bind the approved Verification generation, exact paths/hashes, observed results, and gaps in its `evidence-index.md`; otherwise list evidence gaps. Never invent evidence.
5. Include preconditions, deployment steps, migrations, flags, configuration, validation, metrics, alerts, success criteria, rollback triggers and steps, communication, ownership, and support escalation.
6. Run `singularity-flow phase draft-check <phase> --json`, then `singularity-flow phase prepublish <phase> --json`. If unready, run read-only `singularity-flow recover <WORK-ID> --phase <phase> --json`; stay in this phase. Correct every agent finding now from governed evidence only when `correction.sameTurn`; otherwise route to its owner/regenerator. Recheck up to three changed fingerprints and stop on an unchanged fingerprint. Never blindly delete markers, invent facts or padding, invoke a nested model, or overwrite another producer.
7. Only when prepublish `status` is `ready`, publish with its exact configured producer/channel. Race-time `ARTIFACT_AUTHORING_INCOMPLETE`: recheck once, retry once if ready, never loop. Never submit or approve.
8. Run `singularity-flow phase show <phase> --json`; retain `displayBinding` and `reviewBinding`. Reuse bodies only from a complete visible same-chat display with exactly matching non-null `displayBinding`. Otherwise reproduce every published text document in full: ID/kind/path/bytes/generation/SHA-256 and `--- BEGIN <path> ---` / `--- END <path> ---`. New chat, changed/null binding, omissions or truncation require full display. Tool output or summaries are not review. Binary: path/metadata/open instruction. Show the current `reviewBinding`; body reuse never reuses approval consent.
9. Do not submit or approve automatically. End with each returned `handoff`: `Next in Copilot: /sf-…` from its `copilotCommand`, then `Terminal equivalent: singularity-flow …` from its `command`.
