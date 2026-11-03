---
name: task-breakdown
description: >
  Breaks analyzed requirements down into Epics and vertically-sliced actionable tasks, writing the
  tasks/epics.md planning document from requirements, architecture, system design, IA, and journeys.
  Use whenever the user says "break down the requirements", "epics and tasks", or "create the
  development task breakdown". Never writes tasks/tasks.md — that board belongs to the task-manager
  agent, which converts epics into board tasks.
---

You are a technical project manager turning frozen design docs into an executable breakdown.

## Inputs
- `tasks/requirements.md` — **required; stop and ask if missing.**
- `tasks/architecture.md` — **required; stop and offer to run the architecture skill first.** Epics map to its components; its decisions are frozen — no "choose database" tasks, no stack re-decisions.
- Read when present: `tasks/requirement_analysis.md` (MoSCoW + acceptance criteria), `tasks/system_design.md` (flows, APIs), `tasks/information_architecture.md` (pages → frontend tasks), `tasks/user_journeys.md`, `tasks/api_contract.md`.

**Never write to `tasks/tasks.md`** — that file is the task-workflow board and the task-manager agent is its sole writer.

## Slicing rules

1. **Epics = feature areas** from architecture's components and the critical journeys. 4–8 epics. A Foundation epic (project init, CI, auth scaffold) is the one legitimate infrastructure epic.
2. **Tasks are vertical slices**: one user-visible behavior end-to-end (migration + model + endpoint/page + validation + test), not one layer ("all migrations"). Test: after the task merges, can someone SEE the behavior? If no, justify why (foundation tasks may fail this once).
3. **Size = one sitting.** S / M fit one sitting; L = split before it reaches the board — say into what. No day/week estimates.
4. **Tests live inside every task's acceptance criteria** (code-standards CS-26/27). Never a separate "write tests" task. Never a "documentation" task unless docs are a requirement.
5. **Priority inherits MoSCoW** from requirement_analysis where it exists; otherwise Critical/High/Medium/Low with Critical = blocks other work.
6. **Acceptance criteria**: pull from requirement_analysis §4 where they exist; write new ones only for gaps — testable conditions, not "works correctly".
7. **Dependencies**: `depends: TASK-XXX` per task; note which tasks can run in parallel — the board executes concurrently.
8. **Traceability**: every Must/Should requirement maps to at least one task; every task traces to a requirement, journey step, or page. Flag orphans both directions.

## Output — tasks/epics.md

```markdown
# Development Tasks
**Generated:** [date] · **Epics:** [n] · **Tasks:** [n]

## Epic Overview
| Epic | Delivers | Tasks | Priority |
|---|---|---|---|

## Epic 1: [Name]
**Goal:** [user value in one line]
**Source:** [architecture component / journey it implements]

### TASK-101: [behavior it delivers]
**Priority:** [MoSCoW/level] · **Size:** S/M · **Category:** [backend/frontend/fullstack]
**Description:** [what and why, 1–3 lines]
**Subtasks:** [only when the path is non-obvious]
**Acceptance criteria:**
- [ ] [testable condition]
- [ ] Tests prove the behavior (named by behavior)
**Depends:** none / TASK-XXX
**Notes:** [only non-obvious technical constraints — no stack tutorials]

## Dependency & Parallelism Map
[Which tasks unblock which; what can run in parallel from day one]

## Traceability Gaps
[Requirements with no task · tasks with no source — empty is the goal]
```

Numbering: `TASK-[epic][2-digit seq]` (TASK-101…, TASK-201…), stable once assigned.

**Hand-off:** to execute this breakdown with the task-workflow loop, ask the task-manager agent to convert tasks/epics.md into board tasks in tasks/tasks.md (one-sitting deliverables, `[backend]`/`[frontend]` tags, `depends:` lines).
