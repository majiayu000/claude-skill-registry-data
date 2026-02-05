---
name: work-item-fields
description: Reference for Azure DevOps work item fields, link types, and states. Use when the user needs to know field names, field paths, reference names, link types, or work item type configurations. Use when user mentions "field name", "field path", "what field", "link type", "relation type", "parent child", "work item type", or needs to set/update specific work item properties.
---

# Azure DevOps Work Item Fields Reference (Verified)

## System Fields (All Work Item Types)

| Display Name | Reference Name | Type | Description |
|--------------|----------------|------|-------------|
| ID | System.Id | Integer | Unique identifier |
| Title | System.Title | String | Work item title |
| State | System.State | String | Current state |
| Reason | System.Reason | String | Reason for state |
| Work Item Type | System.WorkItemType | String | Bug, Task, etc. |
| Assigned To | System.AssignedTo | Identity | Person assigned |
| Created By | System.CreatedBy | Identity | Creator |
| Created Date | System.CreatedDate | DateTime | Creation timestamp |
| Changed By | System.ChangedBy | Identity | Last modifier |
| Changed Date | System.ChangedDate | DateTime | Last modified |
| Area Path | System.AreaPath | TreePath | Area classification |
| Iteration Path | System.IterationPath | TreePath | Sprint/iteration |
| Tags | System.Tags | String | Semicolon-separated |
| Description | System.Description | HTML | Rich text description |
| History | System.History | HTML | Discussion entry |
| Rev | System.Rev | Integer | Revision number |
| Board Column | System.BoardColumn | String | Kanban column |
| Board Lane | System.BoardLane | String | Swimlane |

## Common Fields by Category

### Scheduling

| Display Name | Reference Name | Type |
|--------------|----------------|------|
| Story Points | Microsoft.VSTS.Scheduling.StoryPoints | Double |
| Effort | Microsoft.VSTS.Scheduling.Effort | Double |
| Original Estimate | Microsoft.VSTS.Scheduling.OriginalEstimate | Double |
| Remaining Work | Microsoft.VSTS.Scheduling.RemainingWork | Double |
| Completed Work | Microsoft.VSTS.Scheduling.CompletedWork | Double |
| Start Date | Microsoft.VSTS.Scheduling.StartDate | DateTime |
| Finish Date | Microsoft.VSTS.Scheduling.FinishDate | DateTime |

### Priority & Severity

| Display Name | Reference Name | Values |
|--------------|----------------|--------|
| Priority | Microsoft.VSTS.Common.Priority | 1, 2, 3, 4 |
| Severity | Microsoft.VSTS.Common.Severity | 1 - Critical, 2 - High, 3 - Medium, 4 - Low |
| Value Area | Microsoft.VSTS.Common.ValueArea | Business, Architectural |
| Risk | Microsoft.VSTS.Common.Risk | 1 - High, 2 - Medium, 3 - Low |

### Bug-Specific

| Display Name | Reference Name | Type |
|--------------|----------------|------|
| Repro Steps | Microsoft.VSTS.TCM.ReproSteps | HTML |
| System Info | Microsoft.VSTS.TCM.SystemInfo | HTML |
| Found In | Microsoft.VSTS.Build.FoundIn | String |
| Integration Build | Microsoft.VSTS.Build.IntegrationBuild | String |

## Link Types (VERIFIED from az boards work-item relation list-type)

| Display Name | Reference Name | Usage |
|--------------|----------------|-------|
| Child | System.LinkTypes.Hierarchy-Forward | workItemLink |
| Parent | System.LinkTypes.Hierarchy-Reverse | workItemLink |
| Successor | System.LinkTypes.Dependency-Forward | workItemLink |
| Predecessor | System.LinkTypes.Dependency-Reverse | workItemLink |
| Related | System.LinkTypes.Related | workItemLink |
| Duplicate | System.LinkTypes.Duplicate-Forward | workItemLink |
| Duplicate Of | System.LinkTypes.Duplicate-Reverse | workItemLink |
| Tested By | Microsoft.VSTS.Common.TestedBy-Forward | workItemLink |
| Tests | Microsoft.VSTS.Common.TestedBy-Reverse | workItemLink |
| Affects | Microsoft.VSTS.Common.Affects-Forward | workItemLink |
| Affected By | Microsoft.VSTS.Common.Affects-Reverse | workItemLink |
| Referenced By | Microsoft.VSTS.TestCase.SharedParameterReferencedBy-Forward | workItemLink |
| References | Microsoft.VSTS.TestCase.SharedParameterReferencedBy-Reverse | workItemLink |
| Test Case | Microsoft.VSTS.TestCase.SharedStepReferencedBy-Forward | workItemLink |
| Shared Steps | Microsoft.VSTS.TestCase.SharedStepReferencedBy-Reverse | workItemLink |

## Verified CLI Commands for Fields and Links

### List all relation types
```bash
az boards work-item relation list-type -o table
```

### Show work item with relations
```bash
az boards work-item relation show --id 123 -o json
```

### Add parent-child relationship
```bash
# Add child link (work item 123 becomes parent of 456)
az boards work-item relation add --id 123 --relation-type "Child" --target-id 456 -o json

# Add parent link (work item 123 becomes child of 789)
az boards work-item relation add --id 123 --relation-type "Parent" --target-id 789 -o json

# Add related link
az boards work-item relation add --id 123 --relation-type "Related" --target-id 456 -o json
```

> **Note: Friendly Names vs Reference Names**
>
> The CLI uses **friendly names** (from the "Name" column), not reference names:
> - Use `"Parent"` not `"System.LinkTypes.Hierarchy-Reverse"`
> - Use `"Child"` not `"System.LinkTypes.Hierarchy-Forward"`
> - Use `"Related"` not `"System.LinkTypes.Related"`
>
> **Tip:** Run `az boards work-item relation list-type -o table` to see all available friendly names in the "Name" column.

### Create with fields
```bash
az boards work-item create \
  --type "Bug" \
  --title "Login fails" \
  --fields "Microsoft.VSTS.Common.Priority=1" \
           "Microsoft.VSTS.Common.Severity=2 - High" \
           "System.Tags=urgent;login" \
  -o json
```

### Update fields
```bash
az boards work-item update \
  --id 123 \
  --state "In Progress" \
  --assigned-to "user@example.com" \
  --fields "Microsoft.VSTS.Scheduling.RemainingWork=4" \
  -o json
```

### Add comment (discussion)
```bash
az boards work-item update --id 123 --discussion "This is my comment" -o json
```

## List All Fields in Project

```bash
az boards work-item list-fields -o table
```

## Field Gotchas

1. **Identity fields**: Use email or display name, not GUID
2. **HTML fields**: Wrap in HTML tags: `<p>Description</p>`
3. **TreePath fields**: Use backslash: `Project\Area\SubArea`
4. **Tags**: Semicolon-separated in API, comma-separated in CLI
5. **DateTime**: ISO 8601 format: `2024-01-15T10:30:00Z`
6. **Double fields**: Use decimal: `4.5` not `4,5`
7. **State values**: Must match exactly including case - check your process template
