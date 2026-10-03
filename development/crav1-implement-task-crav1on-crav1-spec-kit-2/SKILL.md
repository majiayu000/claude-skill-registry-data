---
name: crav1-implement-task
description: Implement exactly one task from tasks.md, then run its verify step. Use after /crav1-plan-from-spec when the user wants to build. Do not implement other tasks in the same turn unless they named them.
disable-model-invocation: true
icon: beaker
color: green
---

# Implement task

You implement **one** row from `tasks.md`. Then you run that row’s **verify** step. You do not take the rest of the backlog in the same turn.

## Find the work

Spec folder: user @-mention, else the most recently edited tree under `docs/specs/` excluding `_template/`.

Read `tasks.md`, `plan.md`, `spec.md`. Task row shape is this skill’s `assets/tasks.md`. Use diagrams/ADRs as constraints. Spec wins if they disagree.

**Which task:** the `T#` they named, else the first unchecked `- [ ]`. If all checked, say so and tell them to run `/crav1-verify-spec`.

If `tasks.md` is missing, stop. Next: `/crav1-plan-from-spec`.

**Branch:** before any code, follow `/crav1-feature-branch` (drop-in: `.cursor/skills/crav1/crav1-feature-branch/SKILL.md`; plugin: sibling `skills/crav1-feature-branch/SKILL.md`) **Build** prompt. If you are on `spec/<slug>`, stop (no code) and follow that skill’s **Build on a spec-only branch**.

## Gate

Stop (no code) if:

- This `T#` depends on an open question that was parked as a risk and is still unanswered
- The task would implement a spec **non-goal**
- This workspace is only the SDD playbook (no application to change) **and** they did not explicitly ask to scaffold an app here

If two file layouts still fit, follow `plan.md` “files likely touched.” Do not invent a new architecture.

## Do the task

1. Restate `T#` in one sentence (what / verify / spec id). Stop if they object.
2. Prefer **test first** when the verify line is a test: write the failing check, then the minimum code to pass.
3. Change only files needed for this `T#`. Match existing patterns when a codebase exists.
4. If that verify is **live** (HTTP/UI against a running host), follow `crav1-verify-spec` [references/live-host.md](../crav1-verify-spec/references/live-host.md) (drop-in: `.cursor/skills/crav1/crav1-verify-spec/references/live-host.md`; plugin: sibling `skills/crav1-verify-spec/references/live-host.md`) **before** the evidence. Then run the **verify** from the task line (command, test name, or a real UI path). If verify is a UI path and a browser is available, exercise it. If you cannot run it, say what you could not run — do not check the box.
5. If verify **passes**, mark that row `[x]` in `tasks.md` (and OpenSpec `export/openspec/tasks.md` if it exists and lists the same id).
6. If verify **fails**, leave `[ ]`. Recap what failed. Do not silently start `T+1`.

## After one task

Output only:

- `T#` done or blocked
- Files changed
- Verify command and result
- Next: `/crav1-complete-task` (this `T#` through verify/fix/commits), `/crav1-complete-tasks` (a range or all unchecked), `/crav1-implement-task` (next unchecked only), `/crav1-draft-commit-message` / `/crav1-finalize-commit`, or `/crav1-verify-spec`

Do not keep going through the list unless they wrote `T2 and T3` or “continue until blocked.”

## Hard rules

- One task per turn by default.
- Do not expand v0 or “while we’re here” refactors.
- Do not edit `spec.md` to match the code. If the spec is wrong, stop and tell them `/crav1-tighten-spec`.
- Prefer fixing the task over adding features.
