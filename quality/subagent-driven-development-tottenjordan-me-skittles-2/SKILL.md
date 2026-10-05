---
name: subagent-driven-development
description: Use when executing an implementation plan whose tasks are mostly independent, in the current session, with a fresh subagent per task and a two-stage (spec then quality) review after each.
---

# Subagent-Driven Development

## Overview
Execute an implementation plan by dispatching a fresh subagent per task, then a mandatory two-stage
review — spec compliance first, code quality second. Core principle: **fresh subagent per task +
two-stage review (spec then quality) = high quality, fast iteration.**

## When to Use
- You have a written plan (e.g. from `writing-plans`) with mostly independent tasks
- You want to stay in the current session (no parallel-session handoff)
- You want fresh context per task (no pollution) plus layered review

Use `executing-plans` instead when tasks are tightly coupled or you prefer batch execution in a
separate session.

## The Process
### Setup
1. Read the plan once, yourself (the controller).
2. Extract each task's full text + surrounding context.
3. Create one `TaskCreate` entry per task.

### Per-task loop
1. Dispatch ONE implementer subagent — Agent tool, `subagent_type: "general-purpose"` — using
   `implementer-prompt.md`. Paste the task text inline; **never make the subagent read the plan file.**
   Subagents follow `test-driven-development` for each task.
2. If it asks questions → answer fully → re-dispatch.
3. It implements, tests, commits, self-reviews, and reports.
4. Dispatch the spec reviewer (`general-purpose`, read-only) using `spec-reviewer-prompt.md`.
   Issues → implementer fixes (per `receiving-code-review`) → re-review until ✅.
5. Dispatch the code-quality reviewer (`general-purpose`, read-only) using
   `code-quality-reviewer-prompt.md` (aligned with `requesting-code-review`'s `code-reviewer.md`).
   Issues → implementer fixes → re-review until ✅.
6. Mark the task complete (`TaskUpdate`).
7. Next task.

### After all tasks
- Dispatch a final reviewer over the whole diff (base..HEAD) via `requesting-code-review`.
- Complete the work with `finishing-a-development-branch`.

## Spec vs Quality review (separate, ordered)
| Stage | Purpose | Checks |
|---|---|---|
| Spec compliance (first) | Built what was asked? | Missing features, extra/unrequested additions, misunderstandings |
| Code quality (second) | Well-built? | Naming, structure, magic numbers, test coverage |

**Never start the quality review before spec compliance is ✅ — order matters.**

## Conventions
- `subagent_type` for the implementer AND both reviewers = `general-purpose`; reviewers report
  only, never edit.
- Track tasks with whichever task tool the harness provides, one entry per plan task.
- Restate the project's standing constraints in every dispatch — tooling, lint/format commands,
  commit message conventions, what may be staged, and whether pushing is allowed. Subagents start
  with fresh context and will not infer them.

## Common Mistakes (Red Flags)
Never: skip a review stage; proceed with open review issues; run parallel implementers; make a
subagent read the plan file; omit scene-setting context; ignore subagent questions; accept
"close enough" on spec; skip re-review after fixes; treat implementer self-review as a substitute for
the review stages. **If a task fails:** dispatch a fix subagent with specific instructions rather than
fixing by hand.

## Integration
| Skill | Role |
|---|---|
| `writing-plans` | Creates the plan this skill executes |
| `test-driven-development` | Subagents use this for each task |
| `requesting-code-review` | Template for the reviewer subagents |
| `receiving-code-review` | How the implementer responds to review |
| `finishing-a-development-branch` | Completes the work after all tasks |
| `executing-plans` | Alternative for parallel-session batch execution |
| `writing-skills` | How this skill itself was authored |
