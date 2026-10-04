---
name: fleet-plane
description: How to use Plane for sprint management, issue creation, and OCMC sync
user-invocable: false
---

# Fleet Plane Skill — Sprint Management via Plane

## When to Use

You are the Project Manager or fleet-ops and need to:
- Read current sprint status from Plane
- Create work items in Plane from OCMC epics
- Update Plane issues when OCMC tasks complete
- Post comments with @mentions on Plane issues
- Sync Plane ↔ OCMC bidirectional
- List modules (epics) to understand project progress

## Available Plane MCP Tools

| Tool | Purpose | Who Uses It |
|------|---------|-------------|
| `fleet_plane_status(project)` | Project overview — sprint, modules, issues | PM, fleet-ops |
| `fleet_plane_sprint(project)` | Current cycle details and issue breakdown | PM |
| `fleet_plane_list_modules(project)` | List epics with status and progress | PM, architect |
| `fleet_plane_create_issue(project, title, ...)` | Create work item in Plane | PM only |
| `fleet_plane_comment(project, issue_id, comment, mention)` | Post comment, @mention | PM, fleet-ops |
| `fleet_plane_update_issue(project, issue_id, state, ...)` | Change state/priority | PM only |
| `fleet_plane_sync(direction)` | Trigger Plane ↔ OCMC sync | PM, orchestrator |

## Key Rules

1. **PM is the sole writer to Plane.** Other agents read only.
2. **Plane is optional.** If tools return `{plane_available: false}`, skip Plane work.
3. **OCMC is authoritative** for agent task state. Plane reflects, not leads.
4. **Every OCMC task that came from Plane** should be synced back when done.
5. **@mentions route to agent heartbeats** — use them for follow-ups.

## Workflow: Breaking Down Epics

1. `fleet_plane_list_modules("AICP")` — see all epics and their progress
2. For each epic, evaluate: what tasks are needed?
3. Create OCMC tasks: `fleet_task_create(title, description, agent, ...)`
4. Create Plane issues: `fleet_plane_create_issue("AICP", title, ..., module="Stage 1...")`
5. The sync worker will keep them linked

## Workflow: Sprint Status Report

1. `fleet_plane_sprint("AICP")` — get current cycle data
2. `fleet_plane_status()` — get all projects overview
3. Post report to IRC: `fleet_chat("Sprint report: ...", channel="#sprint")`
4. Update Plane page with report (when page tools available)

## Workflow: Completing OCMC → Updating Plane

When an OCMC task is done:
1. The chain system (when built) will auto-sync
2. Until then: `fleet_plane_update_issue("AICP", issue_id, state="Done")`
3. Post completion comment: `fleet_plane_comment("AICP", issue_id, "Task completed. PR: <url>")`

## Workflow: Human Created Plane Issue

When a human creates a Plane issue:
1. PM's heartbeat context includes `plane_new_items`
2. PM evaluates: classify, estimate, assign
3. Create OCMC task: `fleet_task_create(...)` with Plane reference
4. Notify agent: `fleet_chat("New task from Plane: ...", channel="#fleet")`

## Projects

| ID | Name | Your Role |
|----|------|-----------|
| AICP | AI Control Platform | PRIMARY MISSION — LocalAI independence |
| OF | OpenFleet | Fleet infrastructure and operations |
| DSPD | DevOps Solution Product Development | Plane itself |
| NNRT | Narrative-to-Neutral Report Transformer | NLP pipeline |