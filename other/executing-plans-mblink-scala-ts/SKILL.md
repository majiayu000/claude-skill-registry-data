---
name: executing-plans
description: Execute implementation plans task-by-task with verification checkpoints. Use when implementing a plan written with the writing-plans skill.
---

# Executing Plans

1. Read the whole plan and check it before starting: paths current, referenced `TsModel` cases and `TsImports` helpers still exist, order is model → parser → generator → tests. Fix the plan first if it's wrong.
2. Execute each task's CDD steps (type → confirm errors → pin output → implement → verify) in **batches of 3**; after each batch report what was done and any deviations, and ask the human to continue, adjust, or stop.
3. Stop and consult the human when type errors say the plan's type design is wrong, a change alters generated output the plan didn't predict, a task is much bigger than planned, or you need files the plan doesn't list. Any deviation: document what changed and why, and check later tasks' assumptions still hold; continue if minor, stop and consult if it changes the plan's architecture.
4. Finish with `verification-before-completion`.
