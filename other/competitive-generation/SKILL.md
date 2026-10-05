---
name: competitive-generation
description: Generate two or three isolated candidate solutions for a high-value task, evaluate them against one shared evidence-based rubric, and integrate only the.
license: MIT
---

# Competitive Generation

Competition is useful only when the value of independent alternatives exceeds coordination cost.

## Entry gate

Use for a consequential architecture choice, difficult optimization, ambiguous UX direction, or high-risk implementation with multiple plausible approaches. Stay single-path for small fixes, tightly coupled work, or tasks with one obvious implementation.

## Workflow

1. Write one candidate-neutral contract: goal, constraints, immutable files, security boundary, acceptance tests, cost/time budget, and scoring rubric.
2. Create two candidates by default; use three only when the approaches are meaningfully distinct.
3. Obtain diversity through explicit strategies, assumptions, decompositions, or algorithms. Use the active host's current model/session capabilities. A different provider/model is optional and requires authorization when it changes cost or data handling.
4. Isolate candidates in separate worktrees/directories or make them read-only proposals. Never allow concurrent writes to shared state.
5. Run the same deterministic build/tests/benchmarks against every candidate in the same environment.
6. Score blindly where practical. Reject any candidate that violates a hard constraint, even if its aggregate score is high.
7. Inspect diffs and evidence, then choose, combine compatible insights deliberately, or conclude that none passes.
8. Re-run the full validation after integration; a winning isolated candidate can still fail when merged.

## Rubric

Weight task-specific criteria such as correctness, acceptance-test passage, security, behavior preservation, performance with variance, accessibility, maintainability, dependency/risk surface, diff size, and migration/rollback. Do not use a subjective "looks smarter" score. Record ties and uncertainty.

## Safety

The parent task's authority applies to every candidate. Do not push, deploy, publish, spend externally, or message anyone merely to evaluate a candidate. Remove abandoned worktrees only after verifying no user work exists there.

## Deliverable

Report candidate strategies, costs, commands, raw scores, disqualifications, selected result, runner-up insights, integrated diff, final validation, and rollback. If no candidate passes, preserve evidence and do not select the least-bad one silently.
