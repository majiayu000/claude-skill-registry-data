---
name: next
description: Figure out where the Pieceful project stands and propose (then run, after confirmation) the next step in the workflow. Use when the owner types /next, asks "what now / where were we", or a session starts without a clear task.
---

# /next: what's the next step?

1. **Gather state** (read only what exists):
   - private notes (path in `CLAUDE.local.md`): `planning/progress.md` (Current state), `planning/open-questions.md`, `ideas/inbox.md` (Untriaged), `backlog/README.md`, `planning/design-docs-plan.md` (phases)
   - public: `docs/tasks/README.md` (board), `docs/roadmap.md`, `docs/product/features/README.md`
2. **Pick the most useful next step**, in this priority order:
   1. A task in `review` → remind the owner to review/commit it.
   2. A task in `in-progress` → offer to continue it (`/start-task <id>`).
   3. Open questions that block the current phase → ask them (AskUserQuestion: options + recommendation).
   4. The current phase's deliverables are all drafted but not yet reviewed → offer `/tech-review <phase scope>` before the owner approves the phase.
   5. The current phase's next deliverable (e.g. the next unwritten feature spec, research item, ADR).
   6. Untriaged inbox items → offer to triage them into the backlog or feature specs.
   7. A `todo` task whose dependencies are done → offer `/start-task <id>`.
3. **Report briefly:** where things stand (2–3 lines), the proposed next step, and 1–2 alternatives.
4. **Ask before acting.** On confirmation, do the step, using the matching skill (`/new-task`, `/tech-review`, `/adr`, …) where one exists. `/start-task` can only be run by the owner: tell the owner to type `/start-task <id>`.
