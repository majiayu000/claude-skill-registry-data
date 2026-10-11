---
name: planning
description: Break a non-trivial task into steps and track them with a live plan.
trigger: any task with more than one step
---
## When to use
Any task that takes more than one action — write + test, explore + review, a
multi-file change.

## How
1. **First**, call `update_plan` with a short ordered list (3–6 steps); mark the
   first `in_progress`, the rest `pending`.
2. Work the steps in order. After each, call `update_plan` again — that step
   `done`, the next `in_progress`.
3. Adjust the plan if reality differs; keep it honest and current.
4. When all `done`, give a one or two sentence summary.

## Avoid
- Over-planning tiny tasks, or plans with 10+ vague steps.
- Letting the plan drift from what you actually did.

## Done well
The user watches a live checklist that matches reality — clear steps, each
ticked off as it actually completes.
