---
name: omc-ado-sprint
description: "Azure DevOps sprint planning: manage iterations, check team capacity, groom the backlog, and assign work to sprints. Not for work item triage (omc-ado-triage), PR review, pipeline management, or GitHub repos (omc-gh-project)."
---

# OMC ADO Sprint

Perform a full Azure DevOps sprint planning cycle for the current project. Reads `.omg/config.json` for connection settings, queries iterations and team capacity, reviews the backlog, and helps assign work items to sprints.

**When this skill is invoked, immediately execute the workflow below. Do not only restate or summarize these instructions back to the user.**

## Trigger Patterns

- "ado sprint"
- "sprint planning"
- "plan sprint"
- "manage iterations"
- "check capacity"
- "groom backlog"
- "assign to sprint"
- "omc-ado-sprint"

---

## Step 1: Load Configuration

Read `.omg/config.json`:

```bash
node -e "const f=require('fs');try{process.stdout.write(f.readFileSync('.omg/config.json','utf8'))}catch{console.log('NOT_FOUND')}"
```

Extract from the `ado` key:
- `org` — full org URL (e.g. `https://dev.azure.com/contoso`)
- `project` — ADO project name
- `team` — team name (e.g. `contoso Team`)
- `repo` — repository name
- `areaPath` — area path filter (optional)
- `iterationPath` — current iteration path (optional)

If config is NOT_FOUND or missing the `ado` key: tell the user to run `/oh-my-copilot:omc-ado-setup` first and stop.

---

## Step 2: List Current Iterations

Fetch all iterations assigned to the team to understand the sprint timeline.

MCP (preferred):
```
mcp__azure-devops__work_list_team_iterations
  → project: "{project}"
  → team: "{team}"
```

Also fetch all project-level iterations for reference:
```
mcp__azure-devops__work_list_iterations
  → project: "{project}"
```

az CLI fallback:
```bash
az boards iteration team list \
  --team "{team}" \
  --project "{project}" \
  --org "{org}" \
  -o json 2>&1
```

Present the iterations in a table:

```
### Current Iterations
| Name | Start Date | End Date | Status |
|------|-----------|----------|--------|
| Sprint 22 | 2026-03-01 | 2026-03-14 | current |
| Sprint 23 | 2026-03-15 | 2026-03-28 | future |
```

Identify the **current** iteration (today's date falls within its date range) and the **next** iteration for planning purposes.

---

## Step 3: Check Team Capacity

Fetch capacity for the current and upcoming iterations in parallel.

MCP (preferred):
```
mcp__azure-devops__work_get_team_capacity
  → project: "{project}"
  → team: "{team}"
  → iterationId: "{currentIterationId}"

mcp__azure-devops__work_get_iteration_capacities
  → project: "{project}"
  → team: "{team}"
  → iterationId: "{nextIterationId}"
```

az CLI fallback:
```bash
az boards iteration team show-capacity \
  --iteration "{iterationPath}" \
  --team "{team}" \
  --project "{project}" \
  --org "{org}" \
  -o json 2>&1
```

Present capacity as:

```
### Team Capacity — {iterationName}
| Member | Activity | Capacity/Day | Days Off | Total Capacity |
|--------|----------|-------------|----------|----------------|
| Alice  | Development | 6h | 2 | 60h |
| Bob    | Testing     | 6h | 0 | 84h |

Total Available: {N}h | Committed: {N}h | Remaining: {N}h
```

If capacity data is unavailable (team has not set capacity), note this and continue.

---

## Step 4: Review Backlog

Fetch unassigned backlog items — work items not yet assigned to a sprint.

MCP (preferred):
```
mcp__azure-devops__wit_list_backlog_work_items
  → project: "{project}"
  → team: "{team}"
```

az CLI fallback (WIQL query for items at the root iteration — unplanned):
```bash
az boards query \
  --wiql "SELECT [System.Id],[System.Title],[System.WorkItemType],[System.State],[Microsoft.VSTS.Common.Priority],[Microsoft.VSTS.Scheduling.StoryPoints] \
          FROM WorkItems \
          WHERE [System.TeamProject] = '{project}' \
          AND [System.IterationPath] = '{project}' \
          AND [System.State] NOT IN ('Done','Closed','Removed') \
          ORDER BY [Microsoft.VSTS.Common.Priority] ASC, [System.CreatedDate] ASC" \
  --project "{project}" --org "{org}" -o json 2>&1
```

Present the backlog:

```
### Unplanned Backlog ({N} items)
| ID | Title | Type | Priority | Story Points | State |
|----|-------|------|----------|-------------|-------|
| #1234 | Add export feature | User Story | 1 | 5 | New |
| #1235 | Fix login timeout  | Bug        | 2 | 2 | Active |
```

---

## Step 5: Assign to Sprint

For each backlog item the user wants to assign, update its `IterationPath`.

MCP (preferred):
```
mcp__azure-devops__wit_update_work_item
  → id: {workItemId}
  → fields:
      System.IterationPath: "{project}\\{sprintName}"
```

az CLI fallback:
```bash
az boards work-item update \
  --id {id} \
  --fields "System.IterationPath={project}\\{sprintName}" \
  --org "{org}" \
  -o json 2>&1
```

After assigning, confirm:
```
Assigned #1234 "Add export feature" → Sprint 23
```

When assigning multiple items, batch them in parallel calls where possible.

---

## Step 6: Create New Iteration (Optional)

If the user needs a new sprint that does not yet exist, create it at the project level and then assign it to the team.

**6a. Create the iteration:**

MCP (preferred):
```
mcp__azure-devops__work_create_iterations
  → project: "{project}"
  → name: "{sprintName}"
  → startDate: "{YYYY-MM-DD}"
  → finishDate: "{YYYY-MM-DD}"
```

az CLI fallback:
```bash
az boards iteration project create \
  --name "{sprintName}" \
  --start-date "{YYYY-MM-DD}" \
  --finish-date "{YYYY-MM-DD}" \
  --project "{project}" \
  --org "{org}" \
  -o json 2>&1
```

**6b. Assign the iteration to the team:**

MCP (preferred):
```
mcp__azure-devops__work_assign_iterations
  → project: "{project}"
  → team: "{team}"
  → iterationId: "{newIterationId}"
```

az CLI fallback:
```bash
az boards iteration team add \
  --iteration-id "{iterationId}" \
  --team "{team}" \
  --project "{project}" \
  --org "{org}" \
  -o json 2>&1
```

Confirm creation:
```
Created iteration "{sprintName}" ({startDate} – {finishDate}) and assigned to {team}.
```

---

## Step 7: Update Capacity (Optional)

If the user wants to set or adjust team member capacity for an iteration:

MCP (preferred):
```
mcp__azure-devops__work_update_team_capacity
  → project: "{project}"
  → team: "{team}"
  → iterationId: "{iterationId}"
  → teamMemberCapacities: [
      { teamMember: { id: "{userId}" }, capacityPerDay: {hours}, daysOff: [] }
    ]
```

Note: Capacity updates are not well-supported by the `az` CLI. Use the ADO web interface as fallback if the MCP call fails.

After updating, re-fetch with `work_get_team_capacity` and display the updated capacity table.

---

## MCP Tool Reference

| Tool | Purpose |
|------|---------|
| `work_list_iterations` | List all project iterations |
| `work_list_team_iterations` | List iterations assigned to a team |
| `work_create_iterations` | Create new iteration |
| `work_assign_iterations` | Assign iteration to a team |
| `work_get_iteration_capacities` | Get capacity for an iteration |
| `work_get_team_capacity` | Get team capacity across iterations |
| `work_update_team_capacity` | Update team member capacity |

---

## az CLI Fallback Commands

Use these when MCP tools are not available in the current session:

```bash
# List team iterations
az boards iteration team list \
  --team "{team}" --project "{project}" --org "{org}" -o table

# Show capacity for an iteration
az boards iteration team show-capacity \
  --iteration "{iterationPath}" \
  --team "{team}" --project "{project}" --org "{org}" -o json

# Query unplanned backlog items
az boards query \
  --wiql "SELECT [System.Id],[System.Title],[System.WorkItemType],[System.State],[Microsoft.VSTS.Common.Priority] \
          FROM WorkItems WHERE [System.TeamProject]='{project}' \
          AND [System.IterationPath]='{project}' \
          AND [System.State] NOT IN ('Done','Closed','Removed') \
          ORDER BY [Microsoft.VSTS.Common.Priority] ASC" \
  --project "{project}" --org "{org}" -o table

# Assign a work item to a sprint
az boards work-item update \
  --id {id} \
  --fields "System.IterationPath={project}\\{sprintName}" \
  --org "{org}" -o json

# Create a new iteration
az boards iteration project create \
  --name "{sprintName}" \
  --start-date "{YYYY-MM-DD}" \
  --finish-date "{YYYY-MM-DD}" \
  --project "{project}" --org "{org}" -o json

# Assign iteration to team
az boards iteration team add \
  --iteration-id "{iterationId}" \
  --team "{team}" --project "{project}" --org "{org}" -o json
```

---

## Error Handling

| Error | Action |
|-------|--------|
| `.omg/config.json` missing | Tell user to run `/oh-my-copilot:omc-ado-setup` first |
| `team` not found in config | Prompt user to provide team name; use project name as default |
| `az login` required | Prompt user to authenticate; skip that step and continue with available data |
| Iteration not found | Verify the iteration name/path matches exactly what ADO returns in Step 2 |
| Capacity data unavailable | Note that team has not configured capacity; continue with backlog review |
| Rate limit / 429 | Wait 2 seconds and retry once; if still failing, note the section as unavailable |
| `work_update_team_capacity` fails | Advise user to set capacity via ADO web UI at `{org}/{project}/_sprints/capacity` |
