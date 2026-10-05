---
name: kanban
description: Task board management -- create, update, and track work items across workflow stages
layer: hub
category: workflow
triggers:
  - "/kanban"
  - "show the board"
  - "update task status"
  - "what is in progress"
  - "move task to done"
  - "add a task"
  - "show backlog"
inputs:
  - action: view | add | move | update | archive | stats (defaults to view)
  - task: Task description, ID, or reference (for add/move/update)
  - status: Target status column (for move)
  - priority: low | medium | high | critical (for add/update)
outputs:
  - board: Current state of the kanban board
  - taskDetails: Details of created/updated task
  - stats: Board statistics and bottleneck analysis
linksTo:
  - plan
  - plan-archive
linkedFrom:
  - plan
  - cook
  - team
  - ship
preferredNextSkills:
  - plan
  - debug
  - fix
fallbackSkills:
  - plan
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: selective
sideEffects:
  - Creates/updates kanban board state in memory
  - May create/update markdown board file
---

# Kanban Skill

## Purpose

Manage work items through a visual workflow board, tracking tasks from inception through completion. This skill provides a lightweight but structured way to organize, prioritize, and monitor work without leaving the agent conversation.

The board is a thinking tool, not just a tracking tool. Making work visible exposes bottlenecks, forgotten tasks, and scope creep.

## Workflow

### Board Structure

The default kanban board has these columns:

| Column | Meaning | WIP Limit |
|--------|---------|-----------|
| **Backlog** | Identified but not started | None |
| **Ready** | Refined and ready to pick up | None |
| **In Progress** | Actively being worked on | 3 |
| **In Review** | Completed, awaiting verification | 2 |
| **Done** | Verified and complete | None |
| **Blocked** | Cannot proceed -- needs resolution | None |

**WIP limits** (Work In Progress) prevent overcommitment. If In Progress has 3 items, finish or move one before starting another.

### Task Structure

Each task on the board has:
```markdown
### [ID] [Title]
- **Status**: [column]
- **Priority**: Critical | High | Medium | Low
- **Created**: [date]
- **Updated**: [date]
- **Assignee**: [who -- typically "agent" or "user"]
- **Tags**: [searchable labels]
- **Description**: [what needs to be done]
- **Acceptance criteria**: [how to verify completion]
- **Blockers**: [what is preventing progress, if any]
- **Notes**: [additional context, decisions, links]
```

### Actions

#### Action: View Board
Display the current board state.

1. **Render the board** as a table or column layout:
```markdown
| Backlog | Ready | In Progress | In Review | Done | Blocked |
|---------|-------|-------------|-----------|------|---------|
| T-005   | T-003 | T-001       | T-004     | T-002| T-006   |
| T-007   |       | T-008       |           |      |         |
```

2. **Show task summaries** under the board -- ID, title, priority for each active task.
3. **Highlight issues**:
   - WIP limit violations (column over limit)
   - Stale tasks (in same column for too long)
   - Blocked tasks (need attention)

#### Action: Add Task
Create a new task on the board.

1. **Parse the task description** from user input.
2. **Assign an ID** -- Sequential: T-001, T-002, etc.
3. **Set defaults**: Status = Backlog, Priority = Medium, Created = now.
4. **Prompt for missing info** if critical:
   - Acceptance criteria (what does "done" look like?)
5. **Add to the board** and confirm.

#### Action: Move Task
Change a task's status (move between columns).

1. **Identify the task** by ID or description match.
2. **Validate the move**:
   - Is the target column valid? (No skipping columns without explanation)
   - Would this violate WIP limits?
   - If moving to Done, are acceptance criteria met?
3. **Apply the move** and update the timestamp.
4. **If blocked**, prompt for blocker description.

#### Action: Update Task
Modify task details (priority, description, notes, etc.).

1. **Identify the task** by ID or description match.
2. **Apply updates** -- Only change what is specified.
3. **Record the update** in task history/notes.

#### Action: Archive
Move completed tasks to archive and clean the board.

1. **Identify Done tasks** that can be archived.
2. **Move to archive** with completion date and summary.
3. **Update board statistics**.
4. **Optionally invoke `plan-archive`** for tasks associated with a plan.

#### Action: Stats
Analyze board health and workflow metrics.

1. **Count tasks** by status and priority.
2. **Identify bottlenecks**:
   - Which column has the most tasks? (potential bottleneck)
   - How long are tasks sitting in each column?
   - Are there stale tasks (no updates in 3+ interactions)?
3. **Calculate throughput** -- Tasks completed per session/day.
4. **Identify risks**:
   - Too many tasks in progress (spreading thin)
   - Too many blocked tasks (systemic issue)
   - Empty Ready column (planning needed)
   - Overflowing Backlog (scope creep or prioritization needed)
5. **Produce the stats report**:

```markdown
## Board Statistics

| Column | Count | Avg Age | Oldest |
|--------|-------|---------|--------|
| Backlog | 5 | 2d | 5d |
| In Progress | 3 | 1d | 2d |
| Blocked | 1 | 3d | 3d |

### Health Indicators
- WIP: 3/3 (at limit)
- Blocked: 1 task needs attention
- Throughput: 4 tasks completed today
- Bottleneck: Review column (2 tasks waiting)

### Recommendations
- Unblock T-006 before starting new work
- Review T-004 and T-009 to free up Review column
```

## Board File Format

When persisting to a file, use this format:

```markdown
# Kanban Board

> Last updated: [timestamp]

## Backlog
### T-005: Set up CI/CD pipeline
- **Priority**: Medium
- **Tags**: devops, infrastructure

### T-007: Add rate limiting to API
- **Priority**: High
- **Tags**: security, api

## Ready
### T-003: Write user authentication tests
- **Priority**: High
- **Tags**: testing, auth

## In Progress
### T-001: Implement user registration endpoint
- **Priority**: High
- **Tags**: api, auth
- **Notes**: Schema is defined, starting controller logic

## In Review
### T-004: Design database schema
- **Priority**: Critical
- **Tags**: database
- **Acceptance**: ERD reviewed, migrations tested

## Done
### T-002: Project scaffolding and configuration
- **Priority**: High
- **Completed**: [date]

## Blocked
### T-006: Integrate payment gateway
- **Priority**: Medium
- **Blocker**: Waiting for API credentials from payment provider
```

## Usage

### View the board
```
/kanban
/kanban show board
```

### Add tasks
```
/kanban add: Implement password reset flow (high priority)
/kanban add: Write API documentation (medium, tags: docs)
```

### Move tasks
```
/kanban move T-001 to review
/kanban T-003 is done
/kanban T-006 is blocked -- waiting on third-party API access
```

### Update tasks
```
/kanban update T-001 priority to critical
/kanban T-005 note: decided to use GitHub Actions
```

### Get stats
```
/kanban stats
/kanban What is blocking progress?
```

### From a plan
```
/kanban Create board from the authentication plan
```

## Examples

### Example: Creating a board from a plan

**Input**: Plan with 3 phases, 8 tasks total

**Output**: Board created with 8 tasks, all in Backlog. Phase 1 tasks tagged with `phase-1` and moved to Ready.

### Example: Identifying a bottleneck

**Input**: `/kanban stats`

**Output**: "3 tasks in Review, only 1 in Progress. The bottleneck is the review stage. Recommend reviewing T-004 and T-009 before starting new development work."

## Guidelines

- **WIP limits are not suggestions** -- They are rules. Finishing work is more valuable than starting work.
- **Blocked is a status, not a graveyard** -- Blocked tasks need active resolution. Flag them prominently.
- **Tasks should be small** -- If a task sits In Progress for more than a day, it is probably too large. Break it down.
- **Acceptance criteria matter** -- A task without acceptance criteria is a task that is never truly done.
- **Update the board, do not let it rot** -- A stale board is worse than no board. It gives false confidence.
- **Archive completed work** -- Done tasks should not clutter the board. Archive them and celebrate progress.
- **The board reflects reality** -- If reality changed, update the board. Do not pretend the plan is still valid.
- **Prioritize ruthlessly** -- Not everything is high priority. If everything is high, nothing is.
