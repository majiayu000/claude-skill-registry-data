---
name: planning-only
description: Create execution-free plans only. Use when the user asks for planning, strategy, decomposition, sequencing, task design, subagent assignment, tooling plans, or implementation prep without doing the work yet. Always produce a step-by-step plan, use the orchestrating-subagents skill for delegation design, assign the right tools and supporting skills per subtask, and forbid direct execution, file changes, deployments, installs, or runtime mutations.
---

# Planning Only

Produce plans only. Do not execute the plan.

## Hard boundary

Never implement, modify files, run project changes, deploy, install dependencies, schedule jobs, make API writes, or take any action that changes state.

Allowed work:
- inspect context needed to plan
- reason about dependencies and risks
- propose routing, staffing, tools, and skills
- identify missing prerequisites
- recommend what should be done next

Disallowed work:
- coding
- editing
- installing
- provisioning
- publishing
- running fixes, migrations, or commands that alter state

If a request mixes planning and execution, split it. Deliver the plan now and explicitly stop before execution.

## Required output

Return a concrete, ordered plan with these sections in this order:
1. Goal
2. Assumptions
3. Step-by-step plan
4. Subagent assignments
5. Tools and skills per subagent
6. Missing tools or skills
7. Risks and approval points

Keep the steps actionable and specific. Prefer numbered steps.

## Delegation design workflow

Use the `orchestrating-subagents` skill to design the delegation layer.

For each requested outcome:
1. Break the work into bounded subtasks.
2. Decide whether each subtask is planning, coding, research, image creation, review, or coordination.
3. Assign a subagent profile for each subtask.
4. Assign the minimum toolset and the most specific existing skill for each subtask.
5. Note handoff artifacts each subagent must return.
6. State sequencing and parallelization constraints.

## Tool and skill assignment rules

For every subtask, specify:
- agent/model
- objective
- inputs
- expected outputs
- tools allowed
- skills to load first
- blocked dependencies

Prefer the narrowest effective toolset.
Do not assign execution tools to a plan-only coordinator unless they are being referenced as recommendations for later use.

## Missing capability rule

If a needed skill or tool is not available:
1. check whether an equivalent existing skill already covers the need
2. if not, recommend downloading it from ClawHub
3. if ClawHub does not appear to cover it, recommend creating a new skill
4. include the gap in the `Missing tools or skills` section

Do not install or create the missing dependency while using this skill unless the user separately asks for execution.

## Quality bar

A valid answer must:
- stay planning-only
- be step-by-step
- include subagent routing
- assign tools and skills per subagent
- surface missing capabilities instead of hand-waving them
- separate assumptions from verified facts
