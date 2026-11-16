---
name: executing-plans
description: "Use when the user has approved a plan and says 'go', 'execute', 'proceed', 'do it', or 'run the plan'. Enforces step-by-step execution with no scope expansion. Companion to plan-first skill."
---

# Executing Plans Skill

An approved plan is a contract. Execute exactly what was agreed — nothing more, nothing less.

This skill is the execution phase of the plan-first → execute workflow.
Use `plan-first` to write and get approval; use this skill to run it.

## When to use this skill

- User approved a plan and says "go", "proceed", "do it", "execute", "run it"
- You have a written plan in context with numbered steps
- Mid-plan: before each step, to stay on track

## Execution rules

### One step at a time

Run each plan step independently. Do not bundle step 2 and 3 into one edit "to save time."
Show what changed after each step.

### No scope expansion

If you notice a related improvement mid-execution:
- Do NOT add it to the current step
- Write a note: "Noticed: [X]. Not in scope — raise after this plan completes."
- Continue with the next plan step

### Stop conditions

Pause and ask the user if any of:
- A step reveals a file/system state different from what the plan assumed
- A step requires a decision that was not in the plan
- A step fails and there is more than one plausible fix

Do not guess. Do not proceed past a blocker silently.

## After each step

Report briefly:
```
Step N complete.
Changed: [file or command output]
Next: Step N+1 — [description from plan]
```

## After all steps

Run the plan's "Verify after" commands and show output verbatim.
Then use the `verify-before-done` skill before claiming the plan is complete.

## What NOT to do

- Do not skip a step because it "seems fine"
- Do not reorder steps
- Do not add an unplanned commit, lint run, or refactor
- Do not mark the plan done before verification passes
