---
name: sflow-verify
description: Verify implementation against acceptance criteria, run checks, capture evidence, and register the Singularity Flow verification artifact.
disable-model-invocation: true
argument-hint: "[test scope or environment]"

---
# Verification phase

<!-- sflow-output-contract: clarification-and-artifact -->
**Output contract:** Use governed inputs and pinned clarification; publish/show configured artifacts.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

1. Run `singularity-flow nextsteps --json` for any workflow. Stop at recovery, pending publication, approval, completion or cancellation. For Boundary phase `release`, never author verification: relay the returned release routes and stop.
2. Require Boundary `ready`, phase `verification`, exact `phaseAgent`; otherwise relay the nextsteps route and stop. Run `singularity-flow phase show verification --json`. If `policyVerified` is false, show `policyReason`; stop. If `effectiveAuthoringSkill` is not `/sf-phase`, relay it and stop. Keep Story context governed.
3. Run `singularity-flow wm compose --phase verification --evidence`; use its prompt. Missing WM is non-blocking. Never derive `--task` from Story text.
4. Read approved requirements, design, implementation and source evidence.
5. Map each AC to evidence and qualified `@ac:WORK-ID:AC-001` in an executable test. Inspect source-bound `@clause:WORK-ID:REQ-001` as a trace witness, not a verdict. Reject bare `AC-001`; honor reviewed test-only/non-code exemptions.
6. Run tests; record commands/results. Honor write scope; source changes require the returned governed repair/rework route and fresh evidence.
7. Cover regression, boundaries, failures, security, accessibility, performance as applicable.
8. Run `singularity-flow prepare verification`; fill observed evidence and `Agent brief`: verdict, failures/omissions, risk, release recommendation.
9. Run `singularity-flow phase draft-check verification --json`, then `singularity-flow phase prepublish verification --json`. If unready, run read-only `singularity-flow recover <WORK-ID> --phase verification --json`. Correct every agent finding now; route other producers to owner. Recheck up to three changed fingerprints; stop on an unchanged fingerprint. Never delete markers blindly, invent facts, use padding, invoke nested models, or overwrite another producer.
10. Only when prepublish `status` is `ready`, publish with its exact configured producer/channel. Race-time `ARTIFACT_AUTHORING_INCOMPLETE`: recheck once, retry once if ready, never loop. Never submit or approve.
11. Run `singularity-flow phase show verification --json`; retain `displayBinding` and `reviewBinding`. Reuse bodies only from a complete visible same-chat display with exactly matching non-null `displayBinding`. Otherwise reproduce every published text document in full: ID/kind/path/bytes/generation/SHA-256 and `--- BEGIN <path> ---` / `--- END <path> ---`. New chat, changed/null binding, omissions or truncation require full display. Tool output or summaries are not review. Binary: path/metadata/open instruction. Show the current `reviewBinding`; body reuse never reuses approval consent.
12. Never submit/approve. End with each `handoff` from step 11: `Next in Copilot: /sf-…` from its `copilotCommand`, then `Terminal equivalent: singularity-flow …` from its `command`.
