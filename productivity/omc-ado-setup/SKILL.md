---
name: omc-ado-setup
description: "Set up or troubleshoot the Azure DevOps integration for this project (.omg/config.json connection). Not for triage, sprint planning, PR review, Azure cloud service config, or GitHub repos (omc-gh-setup)."
role: config-writer
scope: .omg/**
---

# OMC ADO Setup

Configure Azure DevOps integration for the current project. Detects the ADO org and project from the git remote URL, verifies authentication, and writes `.omg/config.json` with all required settings.

**When this skill is invoked, immediately execute the workflow below. Do not only restate or summarize these instructions back to the user.**

## Trigger Patterns

- "setup ado"
- "configure azure devops"
- "ado setup"
- "connect to azure devops"
- "omc-ado-setup"

## Prerequisites

Before running the main workflow, verify all prerequisites are present. If any fail, report the issue and stop with actionable remediation steps.

### Check 1: az CLI installed

```bash
az --version 2>&1 | head -1
```

If this fails: tell the user to install the Azure CLI from https://aka.ms/installazurecli.

### Check 2: azure-devops extension installed

```bash
az extension show --name azure-devops --query name -o tsv 2>&1
```

If output is not `azure-devops`: run `az extension add --name azure-devops` to install it.

### Check 3: az authentication status

```bash
az account show --query "{name:name, id:id, tenantId:tenantId}" -o json 2>&1
```

If this fails or returns an error: tell the user to run `az login` and retry.

### Check 4: az devops configured defaults

```bash
az devops configure --list 2>&1
```

Show the output to the user so they can see existing defaults (org, project).

---

## Step 1: Detect ADO Remote

Inspect the git remote URL to determine if the repo is hosted on Azure DevOps.

```bash
git remote -v 2>&1
```

Azure DevOps remote URLs follow these patterns:
- `https://dev.azure.com/{org}/{project}/_git/{repo}`
- `https://{org}.visualstudio.com/{project}/_git/{repo}`
- `git@ssh.dev.azure.com:v3/{org}/{project}/{repo}`

Parse the remote URL to extract:
- `org` — the ADO organization name
- `project` — the ADO project name
- `repo` — the repository name

If no ADO remote is detected, inform the user and ask whether they want to configure manually (prompt for org, project, repo values).

---

## Step 2: Probe Existing Configuration

Check if `.omg/config.json` already exists:

```bash
node -e "const f=require('fs');try{process.stdout.write(f.readFileSync('.omg/config.json','utf8'))}catch{console.log('NOT_FOUND')}"
```

If it exists and contains `ado` settings, ask the user whether to update or keep the existing configuration (use AskUserQuestion).

---

## Step 3: Verify ADO Connection

Confirm the detected org and project are accessible with the current authentication:

```bash
az devops project show --project "{project}" --org "https://dev.azure.com/{org}" --query "{id:id, name:name, state:state}" -o json 2>&1
```

If this fails, the user may need to configure their PAT or re-authenticate:

```bash
# Option: configure a PAT
az devops configure --defaults organization=https://dev.azure.com/{org}
```

---

## Step 4: Discover Optional Settings

Ask the user (via AskUserQuestion) for optional configuration. Defaults are shown in brackets.

**Question:** "Configure optional ADO settings? (Press Enter to accept defaults)"

For each item, probe the available values from ADO to help the user choose:

### Work Item Type

```bash
az boards work-item type list --project "{project}" --org "https://dev.azure.com/{org}" --query "[].name" -o tsv 2>&1
```

Common values: `User Story`, `Bug`, `Task`, `Issue`. Default: `User Story`.

### Area Path

```bash
az boards area project list --project "{project}" --org "https://dev.azure.com/{org}" --query "children[].path" -o tsv 2>&1
```

Default: `{project}` (root area).

### Iteration Path

```bash
az boards iteration project list --project "{project}" --org "https://dev.azure.com/{org}" --query "children[].path" -o tsv 2>&1
```

Default: `{project}` (root iteration, i.e. no sprint filter).

---

## Step 5: Write `.omg/config.json`

Create or update the config file. Preserve any existing non-ADO keys.

First, ensure the `.omg/` directory exists:

```bash
node -e "require('fs').mkdirSync('.omg',{recursive:true});console.log('Ensured .omg/')"
```

Write `.omg/config.json` using the Write (or Edit) tool. The schema is:

```json
{
  "ado": {
    "org": "https://dev.azure.com/{org}",
    "project": "{project}",
    "repo": "{repo}",
    "workItemType": "User Story",
    "areaPath": "{project}",
    "iterationPath": "{project}",
    "configuredAt": "{ISO timestamp}"
  }
}
```

### Configuration Schema Reference

| Key | Type | Description |
|-----|------|-------------|
| `ado.org` | `string` | Full org URL: `https://dev.azure.com/{org}` |
| `ado.project` | `string` | ADO project name (case-sensitive) |
| `ado.repo` | `string` | ADO repository name |
| `ado.workItemType` | `string` | Default work item type for queries (e.g. `User Story`) |
| `ado.areaPath` | `string` | Area path filter (e.g. `MyProject\TeamA`) |
| `ado.iterationPath` | `string` | Iteration path filter (e.g. `MyProject\Sprint 5`) |
| `ado.configuredAt` | `string` | ISO 8601 timestamp of when setup ran |

### Example output

```json
{
  "ado": {
    "org": "https://dev.azure.com/contoso",
    "project": "Widgets",
    "repo": "widgets-api",
    "workItemType": "User Story",
    "areaPath": "Widgets\\Backend",
    "iterationPath": "Widgets\\Sprint 22",
    "configuredAt": "2026-03-09T12:00:00Z"
  }
}
```

---

## Step 6: Verify Connection

Run a smoke test by listing the most recent 5 work items assigned to the current user:

```bash
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.AssignedTo] = @Me AND [System.TeamProject] = '{project}' ORDER BY [System.ChangedDate] DESC" --project "{project}" --org "https://dev.azure.com/{org}" -o table 2>&1 | head -20
```

If the query returns results: report success and show the items.
If the query fails with an auth error: suggest `az login` or PAT configuration.
If the query returns 0 items: that is normal — confirm setup is complete.

---

## Step 7: Report and Next Steps

Report a summary of what was configured:

```
ADO Setup Complete

Organization : https://dev.azure.com/{org}
Project      : {project}
Repository   : {repo}
Work Item Type: {workItemType}
Area Path    : {areaPath}
Iteration    : {iterationPath}
Config file  : .omg/config.json

Next steps:
  /oh-my-copilot:omc-ado-triage   — run a full triage of work items and PRs
```

---

## Error Reference

| Error | Likely cause | Fix |
|-------|-------------|-----|
| `az: command not found` | Azure CLI not installed | Install from https://aka.ms/installazurecli |
| `ERROR: Please run 'az login'` | Not authenticated | Run `az login` |
| `Extension 'azure-devops' not installed` | Missing extension | Run `az extension add --name azure-devops` |
| `ResourceNotFound` on project show | Wrong org/project | Verify the remote URL and re-run |
| `TF400813: Resource not available` | PAT missing or expired | Create a PAT in ADO → User Settings → Personal Access Tokens |
