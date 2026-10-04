---
name: team-sprint
description: "Execute a sprint using Agent Teams for parallel task execution. Spawns a coordinated team of agents mapped to the CTO delegation chain (lead=TPM, teammates=engineers) to work on sprint tasks concurrently."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, TeamCreate, TeamDelete, SendMessage, TaskCreate, TaskUpdate, TaskList, TaskGet
---

# Team Sprint Execution

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Execute an approved sprint plan using Claude Code Agent Teams for parallel task execution.

## Usage

```
/team-sprint {team}
```

**Arguments:**
- `{team}` — Team name (required). Must have an approved sprint plan.

## Prerequisites

- Approved sprint plan exists in `teams/{team}/plans/sprints/`
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set (configured in `.claude/settings.json`)
- Sprint has 2+ parallelizable tasks (otherwise use standard handoff workflow)

## Process

### Phase 1: Load & Validate Sprint

1. Read team status from `contexts/{context}/status.yaml`
2. Find the current/target sprint plan in `contexts/{context}/plans/sprints/`
3. Validate sprint is approved (check `approved_sprints` in status.yaml)
4. Parse sprint tasks, identify parallelizable work items
5. If fewer than 2 parallelizable tasks, recommend standard handoff workflow instead

### Phase 2: Create Team

1. `TeamCreate` with name `{team}-sprint-{n}` (e.g., `my-project-sprint-5`)
2. Determine teammate count from sprint task assignments (one per unique engineer role, max 4)
3. Spawn teammates via `Task` tool with:
   - `team_name`: the team name from TeamCreate
   - `name`: descriptive role name (e.g., `backend-engineer`, `frontend-engineer`)
   - `subagent_type`: `general-purpose`
   - `mode`: `default` (NOT `plan` — plan mode causes cycling where agents re-enter plan mode after every tool use, requiring 10+ approvals per task)
   - Context prompt MUST include:
     - Team name and repo path
     - Sprint plan reference
     - Their assigned tasks
     - Working directory and branch to use
     - Reminder to commit after each task
     - **MANDATORY**: "Before your FIRST implementation, you MUST use EnterPlanMode, outline your plan, then ExitPlanMode to get approval from the team lead. After your plan is approved, implement freely without re-entering plan mode. Do NOT implement without initial plan approval."

### Phase 3: Create & Assign Tasks

1. For each sprint task, create a `TaskCreate` entry:
   - `subject`: Task title from sprint plan
   - `description`: Full task details including acceptance criteria, relevant files, dependencies
   - `activeForm`: Present continuous form (e.g., "Implementing webhook retry logic")
2. Set task dependencies via `TaskUpdate` with `addBlockedBy` where sprint defines ordering
3. Assign tasks to teammates via `TaskUpdate` with `owner`

### Phase 4: Monitor & Coordinate

Lead operates in delegate mode:

1. **Plan Approval**: When teammates submit plans via ExitPlanMode, review and approve/reject via `SendMessage` with `type: plan_approval_response`
2. **Progress Tracking**: Monitor via `TaskList` — check for blocked tasks, idle teammates
3. **Verification + Handoff (MANDATORY per task)**: When a teammate marks a task complete:
   - Review the work (check git log, read modified files)
   - Verify acceptance criteria from sprint plan
   - **Immediately** create handoff record in `.handoff/handoffs/` (see SOP Section 12.5) — do NOT defer to teardown
   - Add to `.handoff/queue.yaml` as completed
4. **Blocker Resolution**: If a teammate is blocked:
   - Check if another teammate can help
   - Provide guidance via `SendMessage`
   - Reassign if needed via `TaskUpdate`
5. **Handoff Records**: Create handoff YAML for each completed task:

```yaml
handoff_id: "{date}-{team}-{teammate}-{seq}"
created_at: "{ISO timestamp}"
created_by: "team-lead"
team: {team}
project: {project}
task_type: feature | bug-fix | refactor
title: "{task subject}"
description: |
  {task description from TaskCreate}
completed:
  - "{what was accomplished}"
files_modified:
  - path: "{file}"
    changes: "{what changed}"
closed_at: "{timestamp}"
closed_by: "team-lead"
resolution: |
  Completed via Agent Teams session.
source:
  type: agent-team
  sprint_ref: "{sprint-plan-file}"
```

### Phase 5: Teardown

1. **Verify completion**: `TaskList` — all tasks must be completed or have handoff records for remaining work
2. **Incomplete work**: For any unfinished tasks, create handoff records with `next_steps` for the next session
3. **Shutdown teammates**: `SendMessage` with `type: shutdown_request` to each teammate
4. **Clean up team**: `TeamDelete` after all teammates have shut down
5. **Update status**: Update `contexts/{context}/status.yaml`:
   - Sprint progress
   - Completed tasks
   - Remaining work
6. **Summary**: Output a summary of:
   - Tasks completed vs planned
   - Handoff records created
   - Remaining work (if any)
   - Time spent

## Guardrails

- **Never skip handoffs** — Every completed task produces a handoff record **immediately**, not at teardown
- **Never run without approved sprint** — Sprint YAML must have `status: approved` before team creation
- **Enforce plan approval** — Teammates MUST use EnterPlanMode; include explicit instruction in spawn prompt
- **Always clean up** — TeamDelete even if tasks fail
- **Respect the chain** — CTO approves sprint, lead (TPM) manages team, teammates (engineers) implement
- **Max 4 teammates** — Keep coordination overhead manageable
- **Commit often** — Teammates should commit after each logical unit of work
- **Capture summary before TeamDelete** — Task list is removed with the team; save results first

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
