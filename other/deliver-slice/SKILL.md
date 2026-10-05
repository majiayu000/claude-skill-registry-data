---
name: deliver-slice
description: Implement and finalize one ready rolling-wave slice in one invocation while preserving the lifecycle boundary between implementation and independent review. Use when the user wants a slice delivered end to end without manually invoking implement-slice and finalize-slice, wants main-local implementation by default with workers only when delegation pays, followed by mandatory fresh-context finalization, or says deliver, implement and finalize, or take the slice through review.
---

# Deliver Slice

## Core Invariants

- Preserve phase ownership and statuses: `implement-slice` ends at `ready for review`; `finalize-slice` moves it to and leaves it `in review`.
- Never mark the slice `done`; `complete-slice` remains user-owned.
- Follow `implement-slice` execution routing: main-local for small or cohesive work; Terra workers only for genuine parallelism, large mechanical/discovery work, or specialist value.
- Use a fresh-context agent for finalization so implementation assumptions are not treated as review evidence.
- Stop when implementation remains `in progress`, user input is required, or finalization finds a genuine external blocker.

## Workflow

1. Resolve one slice using `implement-slice` rules.
   - Accept only a `ready` slice for a new delivery.
   - If the named slice is already `ready for review` or `in review`, skip implementation and continue with finalization.
   - If it is `in progress`, resume through `implement-slice`; finalize only after it reaches `ready for review`.

2. Read both phase skills completely.
   - Read `../implement-slice/SKILL.md` and every reference it requires for this slice.
   - Read `../finalize-slice/SKILL.md` and every reference it requires for this slice.
   - Treat both phase contracts as authoritative. This skill only orchestrates them.

3. Execute implementation.
   - Follow `implement-slice` without weakening its execution-routing, human handoff, scope, note, or status rules.
   - When workers are used, wait for them, integrate their disjoint changes, and close them.
   - After implementation completes, run one batched root checkpoint: confirm local or worker completion gates, implementation notes, slice/roadmap status, target base, and current `HEAD`. Inspect only missing, conflicting, or integration-sensitive evidence; do not run a second broad implementation review.
   - If implementation does not reach `ready for review`, stop. Report remaining work; do not start finalization.

4. Preserve the review checkpoint.
   - Confirm slice and roadmap statuses are `ready for review`.
   - Capture implementation notes before finalization starts.
   - Create a minimal immutable handoff with project path, slice path, target branch, current `HEAD`, implementation-note location, and prior verification commands plus exact results.
   - Do not precompute changed paths, diff stat, worktree status, or untracked paths solely for the handoff. Mutable review-surface discovery belongs to the fresh finalizer and should happen once.
   - Keep the handoff factual. Do not pass implementation conclusions, recommendations, or suspected findings as facts.

5. Execute finalization in fresh context.
   - Spawn one fresh subagent with `fork_turns: "none"` and the parent model inherited.
   - Give it repository instructions, the immutable handoff, and: `Use $finalize-slice to finalize this slice completely.`
   - Dispatch it immediately after the batched root checkpoint and minimal handoff are complete.
   - Tell it that other agents may have edited the worktree, not to revert unrelated changes, and to preserve user changes.
   - Treat the fresh finalizer as the primary independent reviewer. Default to zero additional reviewers.
   - Let it add one or two focused reviewers only for concrete unresolved uncertainty, specialist risk, high semantic complexity, or explicit adversarial review. File count and mechanical relocation size alone do not justify another reviewer.
   - Require it to report status, resolved findings, accepted gaps, changed files, and any material decision needing user input.
   - Close the finalizer after its result is captured.

6. Finish.
   - Confirm final slice and roadmap status from artifacts instead of trusting the subagent report alone.
   - Leave clean delivery `in review`.
   - Leave user completion and learning capture to `complete-slice`.

## Completion

Report implementation files, resolved finalization findings, accepted gaps or risks, and resulting status. If finalization needed no fixes, preserve its exact `No findings.` result inside the delivery summary.
