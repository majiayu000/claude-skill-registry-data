---
name: sflow-review
description: Perform an independent Singularity Flow review, record actionable findings, and register the review decision.
disable-model-invocation: true
argument-hint: "[review emphasis]"

---
# Portable review bundle and independent review

<!-- sflow-output-contract: governed-review -->
**Output contract:** Show governed artifacts, hashes, identity warnings, and the exact confirmation before recording any decision.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

First run `singularity-flow review`; show its artifact, provenance, checks, decisions, source changes, usage, evidence. For portable HTML use `singularity-flow review --format html --out <file>`.

1. Run `singularity-flow status --json`; use its governed workflow. Without a `review` phase, review the active phase via the bundle.
2. Run `singularity-flow wm compose --phase review --evidence`; use its complete prompt. Missing/unreachable/stale WM means zero-context evidence and repository access; recovery is optional, not prerequisite. Never derive `--task` from Story text. Use available architecture, development, testing, and security evidence.
3. Read approved requirements, design, implementation summary, verification evidence, the actual diff, and selected source evidence.
4. Review correctness, acceptance coverage, maintainability, architecture alignment, security, failures, observability, rollout, rollback, and tests.
5. Rank findings by severity and include file/line references when available.
6. Do not silently fix findings unless explicitly asked.
7. If configured, prepare and complete review, then run `singularity-flow phase draft-check review --json` and `singularity-flow phase prepublish review --json`. If unready, run read-only `singularity-flow recover <WORK-ID> --phase review --json`; stay in this phase. Correct every agent authoring finding now from governed evidence only when `correction.sameTurn`; route other producers to their owner. Recheck up to three changed fingerprints and stop on an unchanged fingerprint. Never blindly delete markers, invent facts or padding, invoke a nested model, or overwrite another producer. Substantive review findings still require a separate fix decision.
8. Only when prepublish `status` is `ready`, publish with its exact configured producer/channel. Race-time `ARTIFACT_AUTHORING_INCOMPLETE`: recheck once, retry once if ready, never loop. Never submit or approve.
9. If published, run `singularity-flow phase show review --json`; retain `displayBinding` and `reviewBinding`. Reuse bodies only from a complete visible same-chat display with exactly matching non-null `displayBinding`. Otherwise reproduce every published text document in full: ID/kind/path/bytes/generation/SHA-256 and `--- BEGIN <path> ---` / `--- END <path> ---`. New chat, changed/null binding, omissions or truncation require full display. Tool output or summaries are not review. Binary: path/metadata/open instruction. Show the current `reviewBinding`; body reuse never reuses approval consent.
10. If published, end with `Next in Copilot: /sf-submit review` and `Terminal equivalent: singularity-flow submit review`; do not submit or approve.
