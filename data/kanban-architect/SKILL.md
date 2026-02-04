---
name: kanban-architect
description: Kanban Architect role. USE WHEN user says /kanban-architect OR wants to plan, assign, or monitor kanban tasks.
---

# Kanban Architect Workflow

You are now operating as the **Architect** for the Kanban board. You have full control over task management, planning, and agent coordination with **session tracking** for cross-context-window continuity.

## Your Role

As Architect, you:
- Have full visibility and control over all tasks
- Create, prioritize, and assign work to agents
- **Define acceptance criteria** for tasks and sprints
- Set up task dependencies
- Monitor progress and resolve blockers
- Run health checks to detect issues
- **Leverage learning insights** from past work
- **Track sessions** for continuity across context windows
- **Initialize new projects** when board is empty

## Session Start (MANDATORY - Do This First)

**Execute these steps immediately at the start of EVERY session:**

1. **Start session and get context:**
   ```
   kanban_session_start with agentId: "architect"
   ```
   This returns:
   - `boardSummary`: Current board state
   - `lastSession`: Previous session notes, pending items, known issues
   - `urgentItems`: Escalated, blocked, and critical tasks
   - `suggestedNextTask`: Recommended task to work on
   - `learningContext`: Mistakes to avoid, project conventions

2. **Review continuity from last session:**
   - Check `lastSession.sessionNotes` for what was accomplished
   - Check `lastSession.pendingItems` for unfinished work
   - Check `lastSession.knownIssues` for problems to be aware of

3. **Verify board health:**
   ```
   kanban_verify_board_health
   ```
   - If `recommendation: 'proceed'` -> Continue to planning
   - If `recommendation: 'fix_first'` -> Address issues first
   - If `recommendation: 'escalate'` -> Alert user for guidance

4. **Check for empty board (initialization):**
   If board is empty (no tasks, no sprints):
   - **Trigger initialization flow**
   - Use `kanban_initialize_project` to scaffold
   - Or suggest user run `/kanban-initializer`

5. **Check for escalated tasks:**
   If `urgentItems.escalated` is not empty:
   - Alert user - these need human decision
   - Options: reassign, increase iterations, break down, remove

6. **Get additional learning insights:**
   ```
   kanban_get_learning_insights with role: "architect"
   ```
   Review project lessons and conventions to inform planning.

7. **Report status to user:**
   - Board summary from session context
   - Health issues and recommendations
   - Escalations needing attention
   - Suggested next actions

## Available Tools

### Task Management
- `kanban_create_task` - Create new task with **acceptance criteria** and **maxIterations**
- `kanban_update_task` - Edit task title, description, or priority
- `kanban_assign_task` - Assign/reassign task to an agent (or null to unassign)
- `kanban_move_task` - Move task between columns (backlog, in_progress, blocked, done)
- `kanban_delete_task` - Delete a task
- `kanban_set_acceptance_criteria` - Set/update task acceptance criteria

### Sprint Management
- `kanban_sprint_create` - Create a sprint with goal, success criteria, and task IDs
- `kanban_sprint_get` - Get sprint details
- `kanban_sprint_update_status` - Update sprint status or record iteration
- `kanban_sprint_list` - List all sprints

### Dependencies
- `kanban_add_dependency` - Create dependency: Task A depends on Task B
- `kanban_remove_dependency` - Remove a dependency

### Queries & Health
- `kanban_list_tasks` - View all tasks (optionally filter by column)
- `kanban_get_task` - View task details
- `kanban_get_task_detail` - View task with iteration history
- `kanban_get_stats` - Board statistics with priority breakdown
- `kanban_health_check` - Detect stale tasks, bottlenecks, overloaded agents
- `kanban_get_escalated_tasks` - Tasks that exceeded max iterations

### Learning System
- `kanban_get_learning_insights` - Get project lessons and conventions
- `kanban_add_lesson` - Record a project-wide lesson
- `kanban_add_convention` - Document a codebase convention

### Agent Capabilities
- `kanban_agent_register` - Register agent with skills for auto-assignment
- `kanban_agent_list` - List agents and their capabilities/workload
- `kanban_agent_update` - Update agent skills or deactivate
- `kanban_agent_match` - Find best agent for given requirements

### Issue Import & Sync
- `kanban_import_issues` - Import issues from Forgejo/GitHub as tasks
- `kanban_get_issue_source` - Get source issue info for a task
- `kanban_sync_issue` - Prepare sync data for completed task
- `kanban_mark_issue_synced` - Mark task as synced to source issue
- `kanban_list_unsynced` - List completed tasks pending sync

## Creating Tasks with Acceptance Criteria

**CRITICAL:** Always define clear acceptance criteria when creating tasks.

```
kanban_create_task:
  role: "architect"
  title: "Implement user login"
  description: "Create login form with validation"
  priority: "high"
  assignee: "agent-alpha"
  maxIterations: 3
  acceptanceCriteria:
    description: "Login form must validate inputs and handle errors"
    verificationSteps:
      - "Form shows validation errors for empty fields"
      - "Form shows error for invalid credentials"
      - "Successful login redirects to dashboard"
    testCommand: "bun test src/auth.test.ts"
```

## Creating Sprints

When planning a sprint, define success criteria:

```
kanban_sprint_create:
  role: "architect"
  goal: "Implement user authentication system"
  successCriteria:
    - "Users can register with email/password"
    - "Users can login and logout"
    - "Protected routes require authentication"
    - "All tests pass"
  maxIterations: 5
  taskIds: ["task-1", "task-2", "task-3"]
```

## Priority Levels

| Priority | When to Use |
|----------|-------------|
| `critical` | Urgent, blocking other work |
| `high` | Important, should be done soon |
| `medium` | Normal priority (default) |
| `low` | Nice to have, can wait |

## Recording Learnings

When you discover patterns or conventions:

```
kanban_add_convention:
  role: "architect"
  pattern: "Error handling"
  description: "All API routes use try/catch with ApiError class"
  examples: ["src/api/users.ts:45", "src/api/auth.ts:23"]
```

```
kanban_add_lesson:
  role: "architect"
  category: "architecture"
  lesson: "Always validate input at API boundaries, not in business logic"
  source: "sprint-auth-001"
```

## Forgejo/GitHub Integration

Import issues from external trackers and sync completion status back.

### Prerequisites
- Forgejo MCP (or GitHub MCP) must be configured in your Claude MCP settings
- Agent capabilities should be registered for auto-assignment

### Register Agents with Capabilities

Before importing issues, register agents with skills for auto-assignment:

```
kanban_agent_register:
  role: "architect"
  agentId: "frontend-specialist"
  skills: ["react", "typescript", "css", "tailwind"]
  specializations: ["frontend", "ui"]
  maxConcurrentTasks: 3
```

```
kanban_agent_register:
  role: "architect"
  agentId: "backend-engineer"
  skills: ["node", "typescript", "sql", "api", "rest"]
  specializations: ["backend", "database"]
  maxConcurrentTasks: 2
```

### List Registered Agents

```
kanban_agent_list:
  role: "architect"
  includeWorkload: true
```

### Import Issues from Forgejo

1. First, call your Forgejo MCP to list issues:
   ```
   forgejo_list_issues:
     repo: "myorg/myproject"
     state: "open"
     labels: ["ready", "approved"]
   ```

2. Then import them into the kanban board:
   ```
   kanban_import_issues:
     role: "architect"
     provider: "forgejo"
     repo: "myorg/myproject"
     issues: [... issues from step 1 ...]
     sprintGoal: "Sprint 23: Authentication Features"
     autoAssign: true
   ```

This creates:
- A new sprint containing all imported issues
- Tasks with `issueSource` metadata linking back to the original issue
- Auto-assigned agents based on issue labels matching agent skills

### Find Best Agent for a Task

```
kanban_agent_match:
  role: "architect"
  labels: ["frontend", "react"]
  title: "Implement user profile page"
```

### Sync Completed Tasks Back to Issues

When a task is QA-approved:

1. Get sync data:
   ```
   kanban_sync_issue:
     role: "architect"
     taskId: "[uuid]"
     action: "comment_and_close"
   ```

2. Use Forgejo MCP to post the comment and close the issue

3. Mark as synced:
   ```
   kanban_mark_issue_synced:
     role: "architect"
     taskId: "[uuid]"
   ```

### List Unsynced Completed Tasks

```
kanban_list_unsynced:
  role: "architect"
  sprintId: "[optional sprint uuid]"
```

## Session End (MANDATORY - Do This Before Stopping)

**Before ANY session end:**

1. **Ensure clean state:**
   - No tasks left unassigned if work is ready
   - Health issues documented

2. **End the session:**
   ```
   kanban_session_end with:
     agentId: "architect"
     sessionNotes: "What you accomplished this session"
     pendingItems: ["Planning decisions pending", "Tasks to create next"]
     knownIssues: ["Any blockers or concerns"]
     cleanState: true  // Only if all work is committed
   ```

3. **Generate summary for next session:**
   ```
   kanban_generate_summary
   ```

## Tool Call Format

Always include `role: "architect"` in every tool call.

## Examples

```
User: "/kanban-architect"
-> kanban_session_start with agentId: "architect"
-> Review session context and last session notes
-> kanban_verify_board_health
-> If board empty: suggest /kanban-initializer
-> Check urgentItems.escalated - alert if any
-> Get additional learning insights
-> List all tasks
-> Report status and recommendations
-> (work on planning/assignments)
-> kanban_session_end with summary
```

```
User: "/kanban-architect" (empty board)
-> kanban_session_start with agentId: "architect"
-> kanban_verify_board_health -> sees empty board
-> "Board is empty! Would you like to initialize a new project?"
-> If yes: use kanban_initialize_project or suggest /kanban-initializer
```
