---
name: s32ds-workspace-health-check
description: Perform a comprehensive health check of the entire S32DS workspace. Lists all projects, retrieves global problems (errors/warnings across all projects), performs per-project analysis (build state, SDK attachments, .mex presence), verifies SDK compatibility, and generates a summary health report. Use this for an overview of workspace state or to diagnose systemic issues affecting multiple projects.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, workspace, health-check, diagnostics, problems]'
---
# Workspace Health Check

Perform a comprehensive health check across all projects in the workspace - detect errors, warnings, and potential issues.

## Tools Used
- `search_actions` - call FIRST to discover available actions; the returned catalog includes each action's input schema
- `execute_action` - invoke any discovered action via `execute_action(action_name="X", params={...})`; the static `start_tool` action brings the IDE up if it is not running
- The `waitForJob` action (via `execute_action`) - blocks until a named async job completes

##  Before You Start
Call `search_actions(query="...")` first to discover all available actions, their descriptions, and input schemas (a parameterless `search_actions()` browses everything). Use the returned catalog to determine correct action names and required/optional parameters before calling `execute_action`.

## Guardrails

**Scope**
- This skill is read-only reporting across all projects. Never auto-fix, build, or modify any project as part of the health check; recommend fixes and hand off to the relevant skill.

**Resource limits**
- Summarize from workspace/project queries; do not open or build every project to gather data. Cap deep per-project inspection to the projects that actually show problems.

**Refuse-and-escalate**
- If an individual project cannot be read (e.g. closed or errored), note it in the report and continue rather than halting the entire health check.

## When to Use
- User asks "are there any problems in my workspace?"

- Before a release or commit, to ensure everything is clean
- After importing or updating multiple projects
- General workspace diagnostics

## Steps

### 1. List All Projects
Get a full inventory of workspace projects:
```
execute_action(action_name="listProjects")
```
Note which projects are open vs. closed. Closed projects won't have problems reported.

### 2. Check Global Problems
Get all problems across the entire workspace:
```
execute_action(action_name="getProblems", params={"severity": "error", "limit": 500})
```
Then check warnings:
```
execute_action(action_name="getProblems", params={"severity": "warning", "limit": 100})
```

### 3. Per-Project Analysis
For each project with issues, get detailed info:
```
execute_action(action_name="getProjectInfo", params={"projectName": "<project_name>"})
```
Check for:
- Missing natures or builders (corrupted project config)
- Invalid build configurations
- Missing referenced projects

### 4. Verify SDK Attachments
For projects with build errors, check SDK status:
```
execute_action(action_name="getProjectSdks", params={"projectName": "<project_name>"})
```
Missing or mismatched SDKs often cause cascading build errors.

### 5. Generate Health Report
Summarize findings in a structured format:
- **Critical**: Projects with errors (list count per project)
- **Warnings**: Non-blocking issues
- **Clean**: Projects with zero problems
- **Closed**: Projects not checked (they are closed)

### 6. Open Relevant IDE Views (optional)
List and open IDE views for deeper diagnostics:
```
execute_action(action_name="listViews")
```
Then open a specific view (e.g., Problems, Console, Memory):
```
execute_action(action_name="openView", params={"viewId": "org.eclipse.ui.views.ProblemView"})
```
Useful when directing the user to visually inspect errors or console output.

### 7. Suggest Fixes
For each category of problem found, suggest resolution:
- Build errors -> clean and rebuild, check SDKs
- Missing references -> verify project dependencies
- Config issues -> check project properties

## Tips
- Run this after `execute_action(action_name="cleanProject", params={"projectName": "<name>"})` + `execute_action(action_name="buildProject", params={"projectName": "<name>"})` for accurate results
- A project with 0 errors but many warnings may still need attention
- Use `execute_action(action_name="getProblems", params={"resourcePath": "Project/src/file.c"})` to drill into specific files
