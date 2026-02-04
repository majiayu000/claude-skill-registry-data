---
name: azure-boards
description: Work with Azure DevOps Product Backlog Items using az boards CLI
when_to_use: |
  Use this skill when the user:
  - Mentions Azure DevOps, Azure Boards, or PBI
  - Provides a work item ID to fetch or update
  - Asks about sprint work or iteration paths
  - Needs WIQL queries for Azure DevOps
---

# Azure Boards Skill

Use the Azure CLI (`az boards`) to interact with Azure DevOps work items.

## Prerequisites

Ensure Azure CLI is authenticated:
```bash
az login
az devops configure --defaults organization=https://dev.azure.com/{org} project={project}
```

## Fetching Work Items

### Single Work Item
```bash
az boards work-item show --id {id} --output yaml
```

### Field Mapping

| Azure DevOps Field | YAML Path | Notes |
|--------------------|-----------|-------|
| Title | `fields.System.Title` | Plain text |
| Description | `fields.System.Description` | HTML-formatted, strip tags |
| Acceptance Criteria | `fields.Microsoft.VSTS.Common.AcceptanceCriteria` | HTML-formatted |
| State | `fields.System.State` | New, Active, Resolved, Closed |
| Assigned To | `fields.System.AssignedTo` | User object |
| Iteration Path | `fields.System.IterationPath` | Sprint path |
| Priority | `fields.Microsoft.VSTS.Common.Priority` | 1-4 |

### HTML Parsing Notes
- Description and Acceptance Criteria are HTML-formatted
- Strip `<div>`, `<p>`, `<ul>`, `<li>`, `<code>` tags before processing
- Look for embedded sections as `<h3>` or `<b>` headers:
  - "Files to modify" -> extract file paths
  - "Scope" or "Architecture" -> extract context
  - Numbered/bulleted lists -> extract changes

## Updating Work Items

### Update Fields
```bash
az boards work-item update --id {id} \
  --fields \
    "System.Description={description_html}" \
    "Microsoft.VSTS.Common.AcceptanceCriteria={criteria_markdown}"
```

### Field Formats
- `System.Description`: HTML with `<h3>`, `<p>`, `<ul>`, `<ol>`, `<li>`, `<code>` tags
- `Microsoft.VSTS.Common.AcceptanceCriteria`: Markdown bullet list (no checkboxes)

### Example Update
```bash
az boards work-item update --id 12345 \
  --fields \
    "System.Description=<h3>Context</h3><p>Switch to internal ingress.</p><h3>Files</h3><ul><li><code>container-app.bicep</code></li></ul>" \
    "Microsoft.VSTS.Common.AcceptanceCriteria=- Direct URL returns 403\n- Front Door URL returns 200"
```

## WIQL Queries

### My Active Work Items
```sql
SELECT [System.Id], [System.Title], [System.State], [System.WorkItemType], [Microsoft.VSTS.Common.Priority]
FROM WorkItems
WHERE [System.AssignedTo] = @Me
  AND [System.WorkItemType] IN ('Product Backlog Item', 'Bug')
  AND [System.State] NOT IN ('Closed', 'Removed', 'Resolved')
ORDER BY [Microsoft.VSTS.Common.Priority] ASC, [System.WorkItemType] ASC
```

### Sprint Work Items
```sql
SELECT [System.Id], [System.Title], [System.State]
FROM WorkItems
WHERE [System.AssignedTo] = @Me
  AND [System.IterationPath] = '{iteration_path}'
  AND [System.State] NOT IN ('Closed', 'Removed')
```

### Execute WIQL
```bash
az boards query --wiql "SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.AssignedTo] = @Me" --output table
```

## Creating Tasks Under a PBI

```bash
az boards work-item create \
  --type Task \
  --title "Task title" \
  --description "Task description" \
  --fields "System.Parent={pbi_id}"
```

## Common Operations

### List Work Item Types
```bash
az boards work-item type list --output table
```

### Show Work Item Relations
```bash
az boards work-item show --id {id} --expand relations
```

### Add Comment
```bash
az boards work-item update --id {id} --discussion "Comment text"
```
