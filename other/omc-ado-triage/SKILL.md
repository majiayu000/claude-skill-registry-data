---
name: omc-ado-triage
description: "Triage Azure DevOps: board status, untriaged work items, active work, open PRs, pipeline failures, and security alerts for a project health overview. Not for sprint planning, PR code review, or GitHub repos (omc-gh-triage)."
---

# OMC ADO Triage

Perform a full Azure DevOps triage cycle for the current project. Reads `.omg/config.json` for connection settings, queries all relevant ADO surfaces (work items, PRs, pipelines, security), and presents a prioritized summary with recommended actions.

**When this skill is invoked, immediately execute the workflow below. Do not only restate or summarize these instructions back to the user.**

## Trigger Patterns

- "ado triage"
- "triage work items"
- "check ado board"
- "ado status"
- "work item triage"
- "omc-ado-triage"

---

## Step 1: Load Configuration

Read `.omg/config.json`:

```bash
node -e "const f=require('fs');try{process.stdout.write(f.readFileSync('.omg/config.json','utf8'))}catch{console.log('NOT_FOUND')}"
```

Extract from the `ado` key:
- `org` — full org URL (e.g. `https://dev.azure.com/contoso`)
- `project` — ADO project name
- `repo` — repository name
- `workItemType` — default type filter (e.g. `User Story`)
- `areaPath` — area path filter (optional)
- `iterationPath` — iteration path filter (optional)

If config is NOT_FOUND or missing the `ado` key: tell the user to run `/oh-my-copilot:omc-ado-setup` first and stop.

---

## Step 2: Gather Triage Data

Run all data-gathering queries in parallel (they are independent). Use MCP tools when available; fall back to `az` CLI commands.

### 2a. Untriaged Work Items

**Priority 0 — items with no State or still in `New` with no sprint assignment.**

MCP (preferred):
```
mcp__azure-devops__wit_my_work_items
  → filter: state = "New", no iteration assigned
```

az CLI fallback:
```bash
az boards query \
  --wiql "SELECT [System.Id],[System.Title],[System.WorkItemType],[System.CreatedDate] \
          FROM WorkItems \
          WHERE [System.TeamProject] = '{project}' \
          AND [System.State] = 'New' \
          AND [System.IterationPath] = '{project}' \
          ORDER BY [System.CreatedDate] ASC" \
  --project "{project}" --org "{org}" -o json 2>&1
```

### 2b. My Active Work Items

Work items assigned to `@Me` that are not Done/Closed/Removed.

MCP (preferred):
```
mcp__azure-devops__wit_my_work_items
```

az CLI fallback:
```bash
az boards query \
  --wiql "SELECT [System.Id],[System.Title],[System.State],[System.IterationPath],[System.AssignedTo] \
          FROM WorkItems \
          WHERE [System.AssignedTo] = @Me \
          AND [System.TeamProject] = '{project}' \
          AND [System.State] NOT IN ('Done','Closed','Removed') \
          ORDER BY [Microsoft.VSTS.Common.Priority] ASC, [System.ChangedDate] DESC" \
  --project "{project}" --org "{org}" -o json 2>&1
```

### 2c. Open Pull Requests

MCP (preferred):
```
mcp__azure-devops__repo_list_pull_requests_by_repo_or_project
  → status: "active"
  → repository: "{repo}"
```

az CLI fallback:
```bash
az repos pr list \
  --repository "{repo}" \
  --project "{project}" \
  --org "{org}" \
  --status active \
  -o json 2>&1
```

For each open PR, check reviewer vote status:
- `-10` = Rejected
- `-5` = Waiting for author
- `0` = No vote
- `5` = Approved with suggestions
- `10` = Approved

### 2d. Recent Pipeline Builds

MCP (preferred):
```
mcp__azure-devops__pipelines_get_builds
  → project: "{project}"
  → maxBuildsPerDefinition: 1
  → statusFilter: "completed"
```

az CLI fallback:
```bash
az pipelines runs list \
  --project "{project}" \
  --org "{org}" \
  --top 20 \
  --query-order FinishTimeDesc \
  -o json 2>&1
```

For each pipeline, use `mcp__azure-devops__pipelines_get_build_status` (or inspect the `result` field from the CLI) to determine:
- `succeeded` — green
- `partiallySucceeded` — yellow
- `failed` — red (action required)

### 2e. Security Alerts

MCP (preferred):
```
mcp__azure-devops__advsec_get_alerts
  → project: "{project}"
  → state: "active"
```

az CLI fallback:
```bash
az security alerts list \
  --project "{project}" \
  --org "{org}" \
  -o json 2>&1
# Note: requires Advanced Security to be enabled; silently skip if unavailable
```

If the MCP call or CLI command returns a permission/feature error, skip this section and note "Advanced Security not enabled or insufficient permissions."

---

## Step 3: Render Triage Summary

Present results using the following structured format. Omit sections that have 0 items (but keep the header with a "(0)" count so the user knows the query ran).

```
## ADO Triage Summary
Project: {project} | Org: {org}
Generated: {timestamp}

---

### Untriaged Work Items ({N})
| ID | Title | Type | Created |
|----|-------|------|---------|
| #1234 | Fix login timeout | Bug | 2026-03-01 |

### My Active Work Items ({N})
| ID | Title | State | Sprint |
|----|-------|-------|--------|
| #1100 | Add export feature | Active | Sprint 22 |

### Open Pull Requests ({N})
| ID | Title | Author | Review Status | Age |
|----|-------|--------|---------------|-----|
| !42 | Add retry logic | alice | Waiting (2 of 3) | 3d |

### Pipeline Status
| Pipeline | Last Run | Result | Branch |
|----------|----------|--------|--------|
| CI | 2026-03-09 08:14 | failed | main |
| Deploy | 2026-03-08 17:02 | succeeded | main |

### Security Alerts ({N})
| Severity | Alert | File |
|----------|-------|------|
| Critical | SQL Injection | src/db/query.ts:42 |

---

### Recommended Actions
1. [Priority] Action description
2. [Priority] Action description
...
```

### Recommended Actions Logic

Build the action list using this priority order:

| Condition | Action |
|-----------|--------|
| Pipeline `failed` | Fix failing pipeline: `{pipeline name}` on `{branch}` |
| Security alert `Critical` or `High` | Address security alert: `{alert title}` in `{file}` |
| PR with reviewer vote `-10` (Rejected) | Address PR rejection: `!{id}` — `{title}` |
| PR with reviewer vote `-5` (Waiting for author) | Respond to PR feedback: `!{id}` — `{title}` |
| Untriaged items > 0 | Triage `{N}` new work items — assign sprint and priority |
| Active items with no sprint | Assign sprint to `{N}` work items missing iteration |
| PR age > 3 days with no votes | Ping reviewers on stale PR: `!{id}` |

---

## Step 4: Optional — Delegate Actions

After presenting the summary, ask the user (via AskUserQuestion):

**Question:** "Would you like me to take action on any of these items?"

**Options:**
1. Fix failing pipeline — delegate to `build-fixer` agent
2. Address PR feedback — open the PR diff and summarize changes needed
3. Triage work items — walk through untriaged items one by one
4. Show details for a specific item — enter work item ID or PR ID
5. No action needed — exit triage

If the user selects option 1, delegate to the build-fixer skill:
```
Skill("oh-my-copilot:build-fix")
```

If the user selects option 4, use `mcp__azure-devops__wit_get_work_item` (or `az boards work-item show --id {id}`) to fetch and display full details.

---

## MCP Tool Reference

| Tool | Purpose |
|------|---------|
| `mcp__azure-devops__wit_my_work_items` | Get work items assigned to current user |
| `mcp__azure-devops__wit_get_work_item` | Read a single work item by ID |
| `mcp__azure-devops__repo_list_pull_requests_by_repo_or_project` | List open PRs for a repo or project |
| `mcp__azure-devops__pipelines_get_builds` | List recent builds per pipeline definition |
| `mcp__azure-devops__pipelines_get_build_status` | Get pass/fail status for a specific build |
| `mcp__azure-devops__advsec_get_alerts` | List active Advanced Security alerts |
| `mcp__azure-devops__advsec_get_alert_details` | Get details on a specific security alert |

---

## az CLI Fallback Commands

Use these when MCP tools are not available in the current session:

```bash
# List my active work items
az boards query \
  --wiql "SELECT [System.Id],[System.Title],[System.State],[System.IterationPath] FROM WorkItems WHERE [System.AssignedTo]=@Me AND [System.State] NOT IN ('Done','Closed','Removed')" \
  --project "{project}" --org "{org}" -o table

# List open PRs
az repos pr list --repository "{repo}" --project "{project}" --org "{org}" --status active -o table

# List recent pipeline runs
az pipelines runs list --project "{project}" --org "{org}" --top 10 --query-order FinishTimeDesc -o table

# Show single work item
az boards work-item show --id {id} --org "{org}" -o json
```

---

## Error Handling

| Error | Action |
|-------|--------|
| `.omg/config.json` missing | Tell user to run `/oh-my-copilot:omc-ado-setup` first |
| `az login` required | Prompt user to authenticate; do not abort the whole triage — skip that section |
| Advanced Security not enabled | Skip security alerts section, note it in summary |
| WIQL query returns 0 results | Show the section with count "(0)" — do not omit the header |
| Rate limit / 429 | Wait 2 seconds and retry once; if still failing, note the section as unavailable |
