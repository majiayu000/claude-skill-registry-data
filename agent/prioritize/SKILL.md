---
name: prioritize
description: Pick 2–3 independent ops tasks from active plans and backlog for autonomous execution, weighing impact, feasibility, and project goals.
---

# Ops Prioritize

Given a project's active plans, backlog, and goals, select 2-3 tasks for immediate autonomous execution. The output is a ranked shortlist with execution order — this skill does NOT execute them.

## Context Required

You need the full project overview loaded (MEMORY.md, state, backlog, active plans) plus any newly identified work items from `find-tasks`.

## Selection Criteria

Score each candidate task on these dimensions:

### Impact (weight: high)

How much does completing this task move the project toward its goals?

- **High**: directly advances a primary goal, unblocks other work, or fills a critical knowledge gap
- **Medium**: advances a secondary goal, improves project quality, or creates useful reference material
- **Low**: nice-to-have, minor cleanup, or distant from current priorities

### Feasibility (weight: high)

Can an autonomous agent complete this task without human input or real-world actions?

- **High**: pure research, writing, analysis, or knowledge management — all inputs are available
- **Medium**: mostly feasible, but may need assumptions about preferences or priorities
- **Low**: requires external information the agent can't access, real-world actions, or significant subjective judgment

Tasks with low feasibility should be skipped — they'll end up in the follow-up file anyway.

### Independence (weight: critical)

Can this task be completed without depending on or conflicting with other selected tasks?

- Tasks that modify the same files are NOT independent
- Tasks where one's output is the other's input are NOT independent
- Tasks touching different backlog areas, state files, or reference topics are usually independent

Independence is a hard constraint, not a gradient. If two high-impact tasks conflict, pick the higher-impact one and find an independent alternative for the second slot.

### Effort (weight: moderate)

Prefer a mix of effort levels. A good batch might be:
- 1 medium task (the main contribution of this cycle)
- 1-2 light tasks (quick wins that keep momentum)

Avoid selecting only heavy tasks — the cycle should produce visible progress. Avoid selecting only light tasks — the cycle should produce meaningful progress.

## Process

### Step 1: Inventory

List all candidate tasks from:

1. **Active plans** in `plans/` — these are already approved work
2. **Backlog items** — particularly those marked as high priority or quick wins
3. **Newly identified items** from the latest `find-tasks` run

For each, note: description, source file, estimated effort, and which files it would touch.

### Step 2: Score

Rate each candidate on impact and feasibility. Discard anything with low feasibility.

### Step 3: Select

Pick 2-3 tasks that:

1. Have the highest combined impact × feasibility score
2. Are mutually independent (hard constraint)
3. Include a mix of effort levels (soft preference)
4. Together represent a productive cycle of work

If active plans exist, prioritize them — they represent work the user already approved. Backlog items and newly identified work fill remaining slots.

### Step 4: Prepare

For each selected task, prepare an execution brief:

```markdown
## Selected Tasks

### Task 1: [Title]
- **Source**: [active plan file or backlog file + item]
- **What**: [1-2 sentence description of what the sub-agent should do]
- **Scope**: [which files will be created/modified]
- **Effort**: light / medium / heavy
- **Plan exists**: yes/no — if no, the sub-agent should create one first

### Task 2: [Title]
...
```

If a selected task doesn't have an existing plan file, note that the sub-agent should create one as its first step (following `plan` format).

### Step 5: Order

Determine execution order. Preferences:

1. Tasks with existing plans go first (less setup overhead)
2. Light tasks before heavy ones (quick wins build momentum and context)
3. If a task might inform another (even if independent), put it first

## Rules

- **Always select at least 2 tasks** unless the backlog is nearly empty
- **Never select more than 3** — better to complete a focused batch and reassess
- **Skip tasks that require real-world actions** — no emails, form submissions, API calls to external services, purchases, or social media posts
- **Prefer breadth over depth** — touching multiple project areas in one cycle is better than deep-diving one area, unless one area is clearly the bottleneck
- **Respect the user's priorities** — if MEMORY.md or state files indicate urgency on a topic, weight those tasks higher
