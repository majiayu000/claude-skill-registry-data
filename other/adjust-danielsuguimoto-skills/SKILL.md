---
name: adjust
description: "Apply user-requested adjustments to existing code — fixes, improvements, refactors per notes. Interactive: grills the user to clarify the request, then parses, plans, and executes. No shipping, no next steps, no loop."
---

# Adjust

Apply the user's adjustment request to existing code. Works on the current code as it exists — uncommitted, clean, or no VCS at all, all irrelevant. No version control operations, no review threads, no approval-driven next steps.

## Scope Boundary

Act on the request only: fix bugs, apply improvements, refactor per notes. Do NOT:
- Perform any version control operation — commit, push, branch switch, PR, merge
- Reply to review threads (none exist)
- Suggest follow-up work, next steps, or shipping on completion
- Widen scope unless the request explicitly asks

The user ships separately.

## Quick Reference

- Input: `$ARGUMENTS` = user adjustment request (free-form prose, possibly multi-point).
- Workspace: stay in the current working directory.
- Parse `$ARGUMENTS` directly.

## Grilling Discipline

Vague adjustment requests produce wrong changes. Grill before parsing, before planning, before implementing.

- **One question at a time.** Wait for the answer. Never batch.
- **Recommended answer** with each question — one line, no justification.
- **Ground in evidence.** If the codebase can answer it, read the code first; ask only what evidence cannot settle.
- **Cite file:line** when a question references existing code.
- **Stop when the target is met.** Don't interrogate past clarity.
- **AFK** → proceed with recommended answers, state assumptions.

### 1. Capture the Request

Read `$ARGUMENTS` → `<adjust-raw>`. Empty or only a question → STOP, ask for concrete adjustments.

### 2. Grill: Clarify the Request

One question at a time, rotate until each settles:

- **Intent**: what outcome does the user want? Restate it in one line and confirm.
- **Target**: which file(s)/symbol(s)? If the request names them, confirm against the code. If not, locate candidates and ask.
- **Scope**: what is explicitly out of scope? What existing behavior must not change?
- **Priority**: if multi-point, which matters most? Recommend ordering.
- **Conflict check**: does the request contradict an existing invariant, pattern, or design decision? If yes, surface the conflict with the decisive snippet before proceeding.

Store answers as `<request-context>`.

If after one grilling round the intent is still undefined, **stop, list unknowns.** Don't act speculatively.

### 3. Parse Into Actionable Items

Split `<adjust-raw>` + `<request-context>` into discrete `<adjust-item>`s: `id` (`A1`, `A2`, …), `file`, `lines`, `category` (`critical` | `important` | `style`), `suggestion` (one-line imperative), `conflicts-with-design` (`yes` → defend current code, record reason, do NOT apply). Build `<not-applying>` list for `noise`, `question`, or `conflicts-with-design: yes` items.

### 4. Plan Implementation

Fast path: every actionable `<adjust-item>` is a specific code suggestion with no conflicts → `<implementation-plan>` = `trivial`, skip to Step 5. Otherwise: order `critical` → `important` → `style`, then file, then line. Validate each (mark `invalid` if it breaks behavior or contradicts a contract → `<not-applying>`). Map cross-item dependencies → `<dependencies>`.

### 5. Grill: Confirm the Plan

Before implementing, confirm with the user:
- **The plan**: present the ordered `<adjust-item>` list and `<not-applying>` list. Ask: proceed with this plan?
- **Scope check**: restate what will NOT change. Ask: any adjacent behavior to preserve?
- **Rollback**: state how to undo if a change regresses. Recommend keeping changes minimal and isolated.

User declines → return to Step 4, revise. Don't implement an unconfirmed plan.

### 6. Implement

Fix critical items first, follow existing patterns, make minimal edits, no comments unless asked. Store `<changes-count>`.

### 7. Validate Changes

Run the project's lint and test commands. Store `<validation-results>` and `<validation-passing>` (`yes`/`no`).

Confirm changes address the request points. Miss intent → re-implement that item.

### 8. Present Results

Nothing ships. Present a concise summary and stop:
- One line per applied change.
- Validation status (`<validation-passing>` + `<validation-results>` summary).
- `<not-applying>` list with one-line reasons.
- `<changes-count>` if tracked.

No follow-up questions, no refinement loop, no next steps.

STOP. No shipping suggestions. The user invokes other skills to ship.


