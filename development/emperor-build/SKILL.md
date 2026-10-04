---
name: emperor-build
description: >-
  Emperor Time — BUILD. Smallest change that makes the work-order probe pass.
  Use when implementing, writing code, or executing a work-order task.
  Failing probe first. Tripwires observed before flags/APIs/paths are asserted.
license: MIT
metadata:
  version: 0.4.30
  part-of: emperor-time
---

# Emperor Build (G3 wrapper)

1. Refuse to build if `scripts/gate.sh g2 <task-dir>` has not passed.
   G2 runs `scripts/lib/work_order.py` (plan header **and** Task-N structure).
   Soft skeleton → `scripts/emperor work-order --reject-no-tasks` / `--reject-tbd`.
2. For standard/heavy tasks: open `skills/emperor-worktree/isolation-checklist.md`
   and/or run `scripts/emperor iso` before mutating the client's checkout.
   Trivial tasks may skip with `worktree: skipped (trivial)` ledgered.
3. Open the **current work-order task only**. Do not reload sibling aspects.
4. Open `skills/emperor-tdd/red-green-refactor.md` and/or run `scripts/emperor tdd`
   (TDD / STEP / MUST card). Write / run the failing probe. Quote the FAIL
   tail. Prediction first (`references/scientific-method.md` at first claim).
5. Smallest change. Observe tripwires (`--help`, read the file) before using them.
6. Re-run the probe. Quote the PASS tail.
7. Log divergences from the work order; if design changed, re-open G2.
8. Run `scripts/gate.sh g3 <task-dir>`.
9. If enlisting another agent, stop and load `skills/emperor-dispatch/SKILL.md`.
10. If something broke, load `skills/emperor-heal/SKILL.md` (Holy Chain).

## MUST — executing-plans checklist for inline plan runs

When executing a work-order / plan *inline* (client chose inline execution, or
no subagent tool) — before Task 1 and between tasks — open
`skills/emperor-build/executing-plans-checklist.md`
(Chain Jail leaf from Superpowers `executing-plans` → Continuous execution /
Four stops / Rulings not stalls / Task Loop / Completion contract only)
and/or run `scripts/emperor execute` (prints the mechanical EXECUTE / STEP /
MUST card).

No check-in theater between tasks. Stop only for the four named stops.
Do not load whole `executing-plans` or `subagent-driven-development`;
ET + emperor-build orchestrate.

## MUST — subagent-driven checklist for subagent plan runs

When executing a work-order / plan with *independent tasks* and a subagent
tool is available (client did **not** choose inline) — before Task 1 and
between tasks — open
`skills/emperor-build/subagent-driven-checklist.md`
(Chain Jail leaf from Superpowers `subagent-driven-development` → Fresh
subagent per task / Task review after each / Fix loop R of 5 / Final
whole-branch review only)
and/or run `scripts/emperor subagent` (prints the mechanical SUBAGENT / STEP /
MUST card).

Fresh implementer per task. Task review (spec + quality) before the next task.
Controller coordinates; does not implement or skip review.
Do not load whole `subagent-driven-development` or its prompt templates;
ET + emperor-build orchestrate. Inline path stays `emperor execute`.


## MUST — plan-scoped SDD task lifecycle (mutating)

Deepens execute/subagent from print-cards into mechanics. Plan-scoped under
`.emperor/sdd/<plan-slug>/` (NOT `.superpowers/`):

| Command | Role |
|---|---|
| `emperor task-brief <work-order> N` | Extract `### Task N` → brief file (exit ≠0 if missing/empty) |
| `emperor task-start <work-order> N` | Write brief + record BASE; prints `brief:` + `base:` |
| `emperor task-done <work-order> N --probe '…'` | Append progress only on green probe + non-empty BASE..HEAD |
| `emperor sdd-workspace <work-order>` | Resolve/create plan workspace (collision marker) |
| `emperor sdd-review-pack <work-order> BASE HEAD` | Plan-scoped review package (ancestor + non-empty guards) |

Cards (`emperor execute` / `emperor subagent`) may still print; lifecycle is mechanical.
Never vendor whole Superpowers prompts/templates.
