---
name: planning
description: >-
  Breaks a feature into ordered, verifiable tasks in a plan file and assigns a model per task. Use when the user asks for a plan, a task breakdown, or which model fits a plan task, or a change spans several files. Not for small edits or reviews.
license: Apache-2.0
metadata:
  level: "process"
  uses: "documenting"
  agents: ""
  tokens: "693"
---

Size the work, then write a short plan of vertical, independently verifiable tasks that the user approves before anything is built.

Uses: foma-skills:documenting (decisions found while planning).

## Steps
1. Pick the path and say it in one line.
   - Small, clear change (1-2 files, no design choice): say "small change, doing it directly" and stop. No plan.
   - Feature: look for a spec (`docs/specs/<name>.md` or the spec line in `## Where things live`). None and the idea is fuzzy: suggest `/foma-skills:shaping` and stop.
   - Multi-step work: continue.
2. Read the CLAUDE.md contract (`## Commands`, `## Where things live`, conventions), then grep for the code the plan touches and read only the relevant ranges. Note the test command and existing patterns.
3. If the spec spans independent subsystems, propose one plan each. If a wide mechanical change (rename, retype) breaks many call sites at once, sequence it expand, migrate in batches, contract.
4. Draft tasks as vertical slices: each cuts through every layer it needs, is demoable or checkable alone, fits one fresh context, and comes in dependency order. Do prefactoring first. Fold setup, config and docs into the task that needs them; split only where a reviewer could reject one task and accept its neighbour.
5. Fill each task: real files, steps with one checkable action each, `Done when` with the project's command, `Status: todo`. Set `Model:` and effort per task (`references/routing.md`).
6. Self-check: every spec requirement maps to a task; names and signatures agree across tasks; the plan is much shorter than the code it describes.
7. Save to `docs/plans/<feature>/plan.md` (or the plans path from `## Where things live`). Show a summary (one line per task with its blockers and model) and ask for ok. Edit on feedback.
8. A design choice made while planning (library, approach rejected): record it through foma-skills:documenting.

## Rules
- Never plan a small change; the plan would cost more than the work.
- Never write code bodies; name files, signatures, test names and values the spec fixes. A plan longer than its code has written the code.
- Never use horizontal tasks ("all models", then "all UI") or a task with no way to check it.
- Never use "TBD", "handle edge cases" or a file or function no task defines; a line that decides nothing is a gap.
- Never start executing before the user's ok.

If writing the plan file, read `references/plan-format.md` (exact template, shared with executing).
If you set or change `Model:` lines (every new plan, or when the user asks which model should do a task), read `references/routing.md`.

## Report
- Path taken, plan file, task count.
- Open questions or spec gaps.
- Not checked: <...>

Next: foma-skills:executing (after the ok).
