---
name: performance-awareness
category: quality
description: How the performance score moves for your role. Use when the score context shows a declining trend, or before handing off work you have not self-checked against every criterion.
---
# Performance Awareness

## Overview

Every agent carries a performance score (0–100, starts at 100). It is not decoration: it reflects how much rework your output causes downstream, and your run context already injects it (`agent.score_context`) — this skill explains what moves it. A task that sails through its gates clean protects your score; one that bounces back at any gate costs you. The score rewards getting it right the first time.

**Core principle:** The cheapest revision is the one that never happens. Every gate you pass clean is points kept; every bounce is points lost AND time lost.

## How the score moves

| Event | Delta | Who is charged |
|-------|-------|-----------------|
| Your task reaches **done** or **released** | +5 each | the assignee |
| Revision requested from **code_review** | −10 | the `in_progress` owner |
| Revision requested from **ready_for_qa** or **in_qa** | −10 | the `in_progress` owner |
| **PM UAT** fails | −5 | the `in_progress` and `in_qa` owners |
| **Human UAT** fails | −8 | the `in_progress`, `in_qa` and `pm_uat` owners |
| A human overturns your approval at the same review gate (**review escape**) | −10 | the reviewer who approved it |
| QA: a bug it caught | +6 | QA, per bug |
| QA: a scenario it confirmed valid / invalid | +1 / −1 | QA, per scenario |
| QA: finished testing a task | +5 | QA |
| PM: completed a UAT | +5 | PM |

The asymmetry is deliberate: one revision (−10) wipes out two clean releases (+10), and Human UAT failing (−8) costs more than PM UAT failing (−5) because it escaped every earlier gate.

## The gates your work passes

```
in_progress → code_review → ready_for_qa → in_qa → pm_uat → human_uat → done → released
              (architect)                  (QA)    (PM)     (human)
```

A defect caught at code_review costs the developer −10. The SAME defect that slips to in_qa, pm_uat or human_uat still costs the developer and now also charges whoever owned the column it escaped through, plus the time of every role between. Catch your own defects before handoff — that is what the score is measuring.

## To protect your score

1. **Read ALL acceptance criteria before starting.** Most bounces are unmet AC, not bugs.
2. **Self-check every AC against fresh, executed evidence** before moving the task forward or recording a verdict.
3. **Never guess a product decision** — add_task_comment with numbered questions instead. A wrong guess becomes a UAT failure, and UAT failures charge more than one role.
4. **On a revision, address EVERY point** and fix at the root, not the symptom. A partial fix bounces again for another −10.
5. **Run the real checks in THIS run** before claiming anything passes or is complete.

## Worked Example

Two developers each ship 5 tasks in a week.

- Dev A rushes: 5 tasks to code_review fast, 3 bounce for unmet AC (−30), fixes them, all 5 eventually released (+50: +25 done, +25 released). Net for the week: **+20**, plus the architect reviewed 8 times.
- Dev B self-checks every AC before handoff: 5 tasks, 0 bounces, all released (+50). Net: **+50**, architect reviewed 5 times.

Same 5 tasks shipped. The difference is entirely self-verification before handoff.

## Red Flags

- Moving a task forward "to see if it passes" — the next gate is not your test suite.
- Skipping an AC, or a scenario, because "it's probably fine."
- Leaving a revision point partially addressed.
- Approving something you did not actually verify — a review escape costs as much as a bounced revision, and it is charged to you alone.
