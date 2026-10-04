---
name: plan-review
description: Optional human-in-the-loop (HITL) plan/diff review sublane — capture a plan, annotate it, ship structured feedback, and diff plan revisions. Mutually exclusive with the autonomous plan_dispatch_gate. AUTO-BLOCKS the next mutation with a reason until the plan is approved (review mode only, default OFF). Use when a human needs to review or annotate an agent plan before dispatch.
triggers:
  - /plan-review
  - human review plan
  - plan annotation
  - HITL plan gate
  - review my plan before dispatch
  - diff plan revisions
scope: harness
invocation: workflow
---

# plan-review — Human-in-the-loop plan/diff review sublane

OPTIONAL HITL surface. Capture an agent plan, let a human annotate it, ship structured feedback back, and compute a Plan-Diff across resubmissions. Clean-room re-imagining of the plan-annotation idea (github-adoption 2026-06-13, `human-review-sublane`) — no external code copied.

## Posture (read this first)

- **AUTO-BLOCK (owner decision 2026-06-13, Marcel "auto block with a reason provided").** When plan-review mode is ON, the PreToolUse guard DENIES the next post-`ExitPlanMode` mutation, with a reason, until the plan is reviewed and approved (a changes-requested verdict keeps the block). Hard gate; requires `CLAUDE_SESSION_ID` (else degrades to WARN); a long TTL failsafe prevents a forgotten review-mode from wedging the session. Fires ONLY in review mode (default OFF), so autonomous sessions are unaffected.
- **Mutual exclusion (load-bearing safety invariant).** Plan-review mode and the autonomous `plan_dispatch_gate` NEVER both fire on the same `ExitPlanMode` event. The mode toggle is the single source of truth; the PostToolUse arm site + the two PreToolUse gate-eval sites all exclude off `isPlanReviewMode()`.
- **Fail-loud toggle.** `on`/`off` MUST fail loud on null/corrupt/missing session-state (exit nonzero + stderr + read-back verify) — never a silent no-op.

## CLI

```bash
# Toggle HITL plan-review mode (fail-loud; exits nonzero on bad state)
node _SYSTEM/Scripts/plan-review.mjs on
node _SYSTEM/Scripts/plan-review.mjs off
node _SYSTEM/Scripts/plan-review.mjs status

# Capture a plan revision (auto-increments revision number)
node _SYSTEM/Scripts/plan-review.mjs capture "<plan-id>" "plan text here"
echo "plan text" | node _SYSTEM/Scripts/plan-review.mjs capture "<plan-id>"

# Plan-Diff across two stored revisions (LCS, scale-capped)
node _SYSTEM/Scripts/plan-review.mjs diff "<plan-id>" 0 1
```

Programmatic: `import { isPlanReviewMode, setPlanReviewMode, capturePlan, annotatePlan, computePlanDiff, buildResultLabel } from '_SYSTEM/Scripts/plan-review.mjs'`.

## When to reach for it

- A human wants to review/annotate an agent plan before any mutation is dispatched.
- You want a recorded Plan-Diff showing what actually changed between plan resubmissions.
- You want to GATE the autonomous dispatch loop with a human checkpoint (blocks the next mutation until you approve) instead of the route-plan auto-dispatch.

Do NOT reach for it for routine autonomous work — leave the mode OFF and the existing `plan_dispatch_gate` flow runs unchanged.

## RESULT_LABEL

Emits a BARE Lane Result Grammar label: `09PR_PLAN_REVIEW_<verb>_<X|P|F>_<PASS_COMMITTED|BLOCKED>`. X/P use `PASS_COMMITTED`; F uses `BLOCKED`.

## Session Notes

### 2026-06-13
- session: 24m | peak ctx: 54% | compacts: 0
- tools: Bash×129, Write×56, Read×56, Edit×39, StructuredOutput×6, Agent×5, TodoWrite×5, TaskUpdate×2, Workflow×1
- corrections: Base directory for this skill: /Users/marcelspatz/.claude/skills/cross-reference-navigation

# Cross-Reference Navigation (XREF)

The GROUND step of the work loop, made reflexive. One question asked a | Base directory for this skill: /Users/marcelspatz/.claude/skills/quantum-hypothesis-simulation

# Quantum Hypothesis Simulation

The quantum-probability layer for YURI's claim/pulse machinery. It mode
- errors: none
