---
name: kanban-sprint
description: Kanban Sprint orchestrator. USE WHEN user says /kanban-sprint OR wants to run a full automated development cycle.
---

# Kanban Sprint - Ralph Wiggum Full Development Cycle

You are running a **Sprint** - a full development cycle that orchestrates Architect, Agent, and QA roles with **iterative refinement** (Ralph Wiggum pattern) and **session tracking** for cross-context-window continuity.

## Arguments

Optional task/feature description after the command.
Example: `/kanban-sprint implement user authentication`

## Agent Naming

**IMPORTANT:** Use descriptive agent names based on task specialization, NOT generic names.

Good examples:
- `frontend-specialist` - For UI/React/CSS work
- `backend-engineer` - For API/database work
- `test-writer` - For test coverage
- `security-reviewer` - For security tasks
- `devops-agent` - For infrastructure work

Bad examples (too generic):
- `agent-alpha`, `agent-beta`, `agent-gamma`

## Sprint Lifecycle

```
PLANNING -> EXECUTING -> REVIEWING -> COMPLETE/FAILED
             ^    |
             |    v (if rejections)
             +----+
```

A sprint can have multiple iterations. Each iteration:
1. Agents work on tasks
2. QA reviews
3. If rejections, loop back (up to maxIterations)

## Execution Instructions

### Phase 0: Session Start & Learning Context

**Start a session and get project insights:**

```
kanban_session_start with agentId: "sprint-orchestrator"
```

This returns:
- Board state and recent activity
- Last session notes for continuity
- Urgent items (escalated, blocked, critical)
- Learning context

**Also get detailed learning insights:**
```
kanban_get_learning_insights with role: "architect"
```

Review:
- Past project lessons
- Codebase conventions
- Common patterns to follow

### Phase 1: Planning

**Create the sprint first:**

```
kanban_sprint_create:
  role: "architect"
  goal: "[User's goal description]"
  successCriteria:
    - "Criterion 1"
    - "Criterion 2"
    - "All tests pass"
  maxIterations: 5
```

**Generate a summary for sub-agents:**
```
kanban_generate_summary
```

**Then spawn an Architect agent:**

```
Task tool:
  subagent_type: "general-purpose"
  description: "Architect planning sprint"
  prompt: |
    You are the ARCHITECT for Kanban sprint [SPRINT_ID].

    GOAL: [User's goal]

    1. Start session: kanban_session_start with agentId: "architect"
    2. Get learning insights: kanban_get_learning_insights
    3. Analyze the codebase to understand patterns
    4. Create 3-8 tasks using kanban_create_task with:
       - role: "architect"
       - sprintId: "[SPRINT_ID]"
       - acceptanceCriteria: { description, verificationSteps, testCommand }
       - maxIterations: 3
    5. Set priorities and dependencies
    6. Assign tasks to descriptive agent names based on task type:
       - frontend-specialist (UI/React work)
       - backend-engineer (API/database work)
       - test-writer (test coverage)
       - Or other descriptive names matching the task domain
    7. End session: kanban_session_end with sessionNotes

    IMPORTANT: Each task must have clear acceptance criteria!
    IMPORTANT: Use descriptive agent names, NOT generic names like agent-alpha!

    Report: tasks created with their acceptance criteria and agent assignments.
```

**Update sprint status:**
```
kanban_sprint_update_status:
  role: "architect"
  sprintId: "[SPRINT_ID]"
  status: "executing"
```

### Phase 2: Execution (Iteration N)

**Generate context summary for agents:**
```
kanban_generate_summary
```

**Record iteration start:**
```
kanban_sprint_update_status:
  role: "architect"
  sprintId: "[SPRINT_ID]"
  iterationNotes: "Starting iteration N"
```

**Spawn Agent sub-agents in parallel:**

For each unique assignee in the sprint tasks, spawn an agent. Use the actual agent names from task assignments (NOT generic names).

```
Task tool:
  subagent_type: "general-purpose"
  description: "[AGENT_NAME] executing tasks"
  prompt: |
    You are [AGENT_NAME] on Kanban sprint [SPRINT_ID].

    1. Start session: kanban_session_start with agentId: "[AGENT_NAME]"
    2. Review session context for continuity
    3. List your tasks: kanban_list_tasks with role: "agent", agentId: "[AGENT_NAME]"
    4. For each task (priority order):
       - kanban_start_iteration (marks iteration start)
       - Review acceptance criteria
       - Implement the work
       - Self-verify against criteria
       - kanban_submit_iteration with workSummary and selfAssessment

    Always use role: "agent", agentId: "[AGENT_NAME]"

    5. End session: kanban_session_end with:
       - sessionNotes: Summary of work done
       - pendingItems: What's left
       - cleanState: true (if all work committed)

    IMPORTANT: Submit iteration with detailed summary of what you did!
```

Spawn one agent per unique assignee. Wait for all to complete.

### Phase 3: Review

**Generate summary for QA:**
```
kanban_generate_summary
```

**Spawn QA agent:**

```
Task tool:
  subagent_type: "general-purpose"
  description: "QA reviewing completed work"
  prompt: |
    You are QA reviewing Kanban sprint [SPRINT_ID].

    1. Start session: kanban_session_start with agentId: "qa-reviewer"
    2. Get context: kanban_get_learning_insights with role: "qa"
    3. List pending: kanban_qa_list with role: "qa"
    4. For each task:
       - Get full detail: kanban_get_task_detail with taskId
       - Review iteration history
       - Verify against acceptance criteria
       - Approve or reject with:
         - feedback (what's wrong)
         - category (logic/testing/style/security/performance/missing-feature)
         - severity (critical/major/minor)
         - suggestedApproach (how to fix)
    5. End session: kanban_session_end with:
       - sessionNotes: Review summary
       - cleanState: true

    IMPORTANT: Structured feedback helps agents learn!

    Report: approved count, rejected count with categories.
```

### Phase 4: Iteration Decision

**Check results:**
- If all tasks approved -> Sprint COMPLETE
- If rejections exist AND sprint.currentIteration < maxIterations -> Loop to Phase 2
- If rejections exist AND sprint.currentIteration >= maxIterations -> Sprint FAILED

**Record iteration result:**
```
kanban_sprint_update_status:
  role: "architect"
  sprintId: "[SPRINT_ID]"
  status: "executing"  // or "complete" or "failed"
  iterationNotes: "Iteration N complete. X approved, Y rejected."
```

### Phase 5: Report & Session End

**Generate final summary:**
```
kanban_generate_summary
```

**Final report:**
- Sprint goal achieved? (check success criteria)
- Total iterations needed
- Tasks completed vs failed
- Lessons learned

**If sprint was successful, record lessons:**
```
kanban_add_lesson:
  role: "architect"
  category: "process"
  lesson: "Key learning from this sprint"
  source: "sprint-[ID]"
```

**End the orchestrator session:**
```
kanban_session_end with:
  agentId: "sprint-orchestrator"
  sessionNotes: "Sprint [GOAL] completed/failed. X tasks done, Y iterations."
  cleanState: true
```

## Escalation Handling

If a task exceeds its maxIterations:
```
kanban_get_escalated_tasks with role: "architect"
```

Escalated tasks need human review. Options:
- Reassign to a different agent
- Increase maxIterations
- Break into smaller tasks
- Remove from sprint

## Examples

```
User: "/kanban-sprint implement user authentication"
-> kanban_session_start with agentId: "sprint-orchestrator"
-> Get learning insights
-> Create sprint with success criteria
-> Spawn Architect to plan tasks with acceptance criteria
   -> Architect assigns tasks to: frontend-specialist, backend-engineer
-> kanban_generate_summary (context for agents)
-> Iteration 1:
   -> Spawn frontend-specialist (with session protocols)
   -> Spawn backend-engineer (with session protocols)
   -> kanban_generate_summary (context for QA)
   -> Spawn qa-reviewer (with structured feedback)
   -> 2 tasks rejected
-> Iteration 2:
   -> Agents fix rejected tasks (with session context)
   -> QA re-reviews
   -> All approved
-> Sprint complete
-> Record lessons learned
-> kanban_session_end with summary
```
