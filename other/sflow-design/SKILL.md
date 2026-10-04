---
name: sflow-design
description: Produce and register an architecture and design artifact, grounded in approved inputs and the codebase, for the design step or any step that chose this skill.
disable-model-invocation: true
argument-hint: "[design constraints or emphasis]"

---
# Architecture and design

<!-- sflow-output-contract: clarification-and-artifact -->
**Output contract:** Use governed inputs and pinned clarification; publish/show configured artifacts.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

1. For the Boundary `phase`, run `singularity-flow phase show <phase> --json`. If `policyVerified` is false, show `policyReason`; stop. Continue only if `effectiveAuthoringSkill` is `/sf-design`, or `/sf-phase` with `authoringSkill` null and `<phase>` = `design`; else show `Next in Copilot:` `effectiveAuthoringSkill` and `Terminal equivalent: singularity-flow prepare <phase>`, or that a null route drafts nothing; stop. Its governed workflow is Story context.
2. Run `singularity-flow wm compose --phase <phase>` and use its complete prompt. If WM is missing/unreachable/stale, continue with zero-context evidence and repository access; show recovery as optional, never prerequisite. Never derive `--task` from Story text. Use available architecture/security evidence.
3. Read the approved inputs the composed prompt names and relevant uploads; inspect grounding-selected source.
4. Run `singularity-flow clarification status <phase> --json`. For `off`, do not ask or record; continue. For `when-needed`, ask and record only for material ambiguity; otherwise continue. For `required`, use `ask_user` once, wait and record before preparation; if unavailable, display the questions and stop; even when evidence looks complete, confirm boundaries, contracts, failures, and tradeoffs. Record via `singularity-flow clarification record <phase> --response-file <file>`.
5. Run `singularity-flow prepare <phase>` and complete the returned document.
6. Cover components, interfaces, data flow, alternatives, compatibility, security, privacy, observability, migration, rollout/rollback, risks, and implementation order.
7. State assumptions and tradeoffs. Do not implement production code.
8. Run `singularity-flow phase draft-check <phase> --json`, then `singularity-flow phase prepublish <phase> --json`. If unready, run read-only `singularity-flow recover <WORK-ID> --phase <phase> --json`; stay in this phase. Correct every agent finding now from governed evidence only when `correction.sameTurn`; otherwise route to its owner/regenerator. Recheck up to three changed fingerprints and stop on an unchanged fingerprint. Never blindly delete markers, invent facts or padding, invoke a nested model, or overwrite another producer.
9. Only when prepublish `status` is `ready`, publish with its exact configured producer/channel. Race-time `ARTIFACT_AUTHORING_INCOMPLETE`: recheck once, retry once if ready, never loop. Never submit or approve.
10. Run `singularity-flow phase show <phase> --json`; retain `displayBinding` and `reviewBinding`. Reuse bodies only from a complete visible same-chat display with exactly matching non-null `displayBinding`. Otherwise reproduce every published text document in full: ID/kind/path/bytes/generation/SHA-256 and `--- BEGIN <path> ---` / `--- END <path> ---`. New chat, changed/null binding, omissions or truncation require full display. Tool output or summaries are not review. Binary: path/metadata/open instruction. Show the current `reviewBinding`; body reuse never reuses approval consent.
11. Report commit and tokens. End with each returned `handoff`: `Next in Copilot: /sf-…` from its `copilotCommand`, then `Terminal equivalent: singularity-flow …` from its `command`; do not submit or approve.
