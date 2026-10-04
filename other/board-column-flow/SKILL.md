---
name: board-column-flow
category: pm
description: Use when moving tasks or reporting status - the kanban column semantics, which columns are human/architect/QA gates, and where the PM actually acts
---
# Board Column Flow

## Overview

The board has more columns than the PM acts in. Knowing which columns belong to the human, the architect, and QA keeps you from moving a task through a gate that isn't yours.

## The columns

Two spines — a given task only passes through the columns its type needs:

```
task / bug:  backlog → todo → in_progress → code_review → ready_for_qa
             → in_qa → pm_uat → human_uat → done → released

analiz:      backlog → todo → in_progress → analiz_review → done → released

need_revision ← any gate that rejects (code_review, in_qa, pm_uat, human_uat, analiz_review)
              → back to in_progress' owner, then forward again from where it left

blocked ← parked here automatically while any blocked_by task is open
        → released automatically when the last one lands
```

`task_type: "technical"` (no user-facing behaviour) skips `pm_uat` — QA routes it straight to `human_uat`. `need_revision` is not a stage in the line — it is where every gate sends work back, and the PM is not dispatched there: act on a `need_revision` task only if the stakeholder raises it in chat. `done → released` is release-engineer's step, not yours.

## Who owns each gate

| Column | Owner | PM action? |
|--------|-------|-----------|
| backlog | PM | Yes — create tasks here by default; stakeholder prioritizes |
| todo | assignee agent (auto) | Move approved tasks here to start them |
| in_progress | developer | No |
| **analiz_review** | **human** | **No** — the human approves the architect's plan (→ done) or rejects it (→ need_revision) |
| code_review | system-architect | No — architect advances to ready_for_qa or need_revision |
| ready_for_qa | QA (queue — QA takes it into in_qa) | No |
| in_qa | QA (testing in progress) | No |
| need_revision | developer / architect | Not dispatched here; act only if the stakeholder asks in chat |
| **pm_uat** | **PM** | **Yes** — verify against AC by walking each flow yourself in the browser or on a device; QA's evidence is a cross-check, not a substitute (see pm-uat-review). Skipped for `task_type: "technical"`. |
| human_uat | stakeholder | No — stakeholder reviews |
| done / released | — | Terminal; released per project convention, by release-engineer |

## PM action points (only these)

- **backlog:** create tasks here; the stakeholder reviews/prioritizes before agents pick them up.
- **todo:** move approved tasks here to trigger the assignee.
- **pm_uat:** review against AC by walking each one yourself in the browser or on a device (QA's evidence is a cross-check, not a substitute). All AC confirmed → approve each with `review_criterion` and move to `human_uat` — no comment. Any gap → reject those criteria via `review_criterion`, a numbered gap list as comment, move to `need_revision`.

Everything else (analiz_review, code_review, QA columns, human_uat) is another actor's gate — don't move tasks through them.

## Common Mistakes

- Moving an analiz task out of `analiz_review` — that's the human's approval gate.
- Advancing a task in `code_review` — that's the architect's.
- Approving in `pm_uat` by reading code, or on QA's evidence alone, instead of walking the flow yourself.
- Acting on a `need_revision` task uninvited — you are not dispatched there.

## Red Flags

- You moved a task through a column not in the PM action-points list.
- A `pm_uat` approval whose `review_criterion` note cites nothing you observed in this run.

## Board mechanics

- Claiming a task and moving it between columns takes seconds and announces what you are doing; it produces nothing by itself. Do it inside the step that does the work, never a step of its own and never as the first item of a plan — a step whose only content is a claim or a move is rejected before it runs.
- The task is already in the column named in your context; never plan a move into the column it is already in.
- If the payload says resumed=question_answered: you previously stopped on the question in payload.question and the human replied in payload.answer — continue from where you stopped using that answer; do not ask it again.
