---
name: kanban-sprint
description: Kanban Sprint orchestrator. USE WHEN user says /kanban-sprint OR wants to run a full automated development cycle.
---

# Kanban Sprint - Full Development Cycle Orchestrator

You are running a **Sprint** - a full development cycle that orchestrates Architect, Agent, and QA roles automatically.

## Arguments

Optional task/feature description after the command.
Example: `/kanban-sprint implement user authentication`

## Sprint Phases

```
Phase 1: PLANNING (Architect)
    ↓
Phase 2: EXECUTION (Parallel Agents)
    ↓
Phase 3: REVIEW (QA)
    ↓ (if rejections, loop back)
Phase 4: REPORT (Summary)
```

## Execution Instructions

### Phase 1: Planning

**Spawn an Architect agent:**

```
Task tool:
  subagent_type: "general-purpose"
  description: "Architect planning sprint"
  prompt: |
    You are the ARCHITECT for a Kanban sprint.

    TASK: [User's task description or "Analyze codebase and create tasks"]

    1. Analyze the codebase
    2. Create 3-8 tasks using kanban_create_task with role: "architect"
    3. Set priorities and dependencies
    4. Assign to agents: agent-alpha, agent-beta, agent-gamma

    Report: tasks created, assignments, dependencies.
```

Wait for completion, then verify with `kanban_get_stats`.

### Phase 2: Execution

**Spawn Agent sub-agents in parallel** (one Task call per agent with assigned work):

```
Task tool:
  subagent_type: "general-purpose"
  description: "Agent-alpha executing tasks"
  prompt: |
    You are AGENT-ALPHA on the Kanban board.

    1. List your tasks: kanban_list_tasks with role: "agent", agentId: "agent-alpha"
    2. For each task (priority order):
       - Move to in_progress
       - Implement the work
       - Move to done

    Always use role: "agent", agentId: "agent-alpha"
```

Spawn similar agents for beta, gamma as needed. Wait for all to complete.

### Phase 3: Review

**Check pending QA and spawn QA agent:**

```
Task tool:
  subagent_type: "general-purpose"
  description: "QA reviewing completed work"
  prompt: |
    You are QA reviewing the Kanban board.

    1. List pending: kanban_qa_list with role: "qa"
    2. Review each task
    3. Approve or reject with feedback

    Report: approved count, rejected count with reasons.
```

If rejections exist, loop back to Phase 2 for fixes (max 3 iterations).

### Phase 4: Report

Compile summary:
- Tasks completed
- Iterations needed
- Any remaining blockers

## Examples

```
User: "/kanban-sprint implement user authentication"
-> Spawn Architect to plan auth tasks
-> Spawn parallel Agents to implement
-> Spawn QA to review
-> Report completion summary
```
