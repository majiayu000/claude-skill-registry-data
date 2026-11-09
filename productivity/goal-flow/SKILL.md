---
name: goal-flow
description: Manage explicitly requested Hephaera goals as automated multi-task delivery flows with automatic per-task PR creation and required post-PR QA.
engines: [AGNOSTIC]
---

## When to use
Use when the user explicitly requests a `goal`, says `goal flow`, or a task planning artifact marks `Goal Flow: enabled` or `Flow: goal`.

Do not activate goal flow from the generic `## Goal` section in a normal `TASK.md`. That section describes task intent; it is not the automated goal feature.

Do not activate or create goal flow while repository-root `BRAINSTORM.md` is active. Brainstorm must be explicitly closed and converted into a plan first.

## Output
- goal file path under `../.hephaera/.cache/goals/<goal_name>/GOAL.md`
- ordered goal task list
- task flow mode marked as `goal`
- per-task PR readiness report generated with goal automation enabled
- automatic PR creation after each completed task
- post-PR QA evidence before advancing to the next goal task
- branch-chain records when later work depends on earlier unmerged PR branches
- final goal completion report with PR links in approval order

## Notes
- Goal task publication is one scoped exception to the normal human PR readiness prompt. The other is work-unit progress publication under an explicitly approved Gauntlet contract; Gauntlet promotion remains human-gated.
- Goal flow does not skip validation, PR creation evidence, issue linkage, or post-PR QA.
- Goal flow never implies auto-merge, merge approval, or auto-merge enablement.
- If a later goal task depends on an earlier task or would likely create merge conflicts when based on the original base branch, base the later task branch on the previous task branch or PR head and record the dependency.
- When every goal task has completed post-PR QA, generate `GOAL_REPORT.md` with ordered PR links, branch dependencies, QA evidence, and merge-conflict risk notes for human approval.
- Stop automatic advancement if local validation fails, PR creation fails, post-PR QA fails, or a task requires a human decision not covered by the goal plan.
- The project-manager role owns goal decomposition, task ordering, and any parallel sub-agent lane decisions within a goal task.
- Use `./commands/pr-readiness-check.sh --goal` to create a durable readiness report that records the goal-flow exception.

## Commands
./commands/create-goal-file.sh "<goal_name>" ["Goal Title"] [--dry-run]
./commands/create-goal-completion-report.sh "<goal_name|goal_dir|goal_file>" [--dry-run]
