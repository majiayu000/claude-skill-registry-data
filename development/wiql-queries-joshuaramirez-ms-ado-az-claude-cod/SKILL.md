---
name: wiql-queries
description: Build and execute WIQL (Work Item Query Language) queries for Azure DevOps. Use when the user wants to query work items, find bugs, list tasks, search by assignee, filter by state, find items in a sprint, or build custom work item queries. Use when user mentions "query", "find work items", "list bugs", "my tasks", "assigned to", "in sprint", or "WIQL".
---

# WIQL Query Reference (Verified)

## CRITICAL LIMITATIONS - READ FIRST

1. **NO TOP CLAUSE** - WIQL does NOT support `SELECT TOP N` like SQL Server. Limit results with shell:
   ```bash
   az boards query --wiql "..." -o table | head -10
   ```

2. **Use explicit project name** - The `@project` macro is unreliable in CLI:
   ```sql
   -- UNRELIABLE:
   WHERE [System.TeamProject] = @project

   -- RELIABLE:
   WHERE [System.TeamProject] = 'YourProjectName'
   ```

3. **Only flat queries supported** - The CLI only supports flat queries, not tree/hierarchical queries.

4. **NO LIKE OPERATOR** - WIQL does NOT support SQL-style LIKE patterns. Use CONTAINS instead:
   ```sql
   -- DOES NOT WORK:
   WHERE [System.Title] LIKE '%keyword%'

   -- USE THIS INSTEAD:
   WHERE [System.Title] CONTAINS 'keyword'
   ```

5. **CANNOT ORDER BY System.Parent** - Sorting by parent ID is not supported:
   ```sql
   -- DOES NOT WORK:
   ORDER BY [System.Parent]

   -- WORKAROUND: Filter by parent IDs with IN clause, sort client-side
   WHERE [System.Parent] IN (1234, 1235, 1236) ORDER BY [System.Id]
   ```

## Basic Query Syntax

```bash
az boards query --wiql "SELECT [fields] FROM workitems WHERE [conditions]" -o table
```

## Verified Working Examples

### Query all work items in project
```bash
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State] FROM workitems WHERE [System.TeamProject] = 'ProjectName'" -o table
```

### Query by state
```bash
az boards query --wiql "SELECT [System.Id], [System.Title] FROM workitems WHERE [System.State] = 'In Progress' AND [System.TeamProject] = 'ProjectName'" -o table
```

### Query by work item type
```bash
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State] FROM workitems WHERE [System.WorkItemType] = 'Bug' AND [System.TeamProject] = 'ProjectName'" -o table
```

### Query by assignee
```bash
az boards query --wiql "SELECT [System.Id], [System.Title] FROM workitems WHERE [System.AssignedTo] = 'user@domain.com' AND [System.TeamProject] = 'ProjectName'" -o table
```

### Query with ORDER BY (most recent first)
```bash
az boards query --wiql "SELECT [System.Id], [System.Title], [System.ChangedDate] FROM workitems WHERE [System.TeamProject] = 'ProjectName' ORDER BY [System.ChangedDate] DESC" -o table
```

### Query by iteration (sprint)
```bash
az boards query --wiql "SELECT [System.Id], [System.Title] FROM workitems WHERE [System.IterationPath] = 'ProjectName\\Sprint 1' AND [System.TeamProject] = 'ProjectName'" -o table
```

### Query by area path
```bash
az boards query --wiql "SELECT [System.Id], [System.Title] FROM workitems WHERE [System.AreaPath] UNDER 'ProjectName\\TeamArea'" -o table
```

### Query with multiple conditions
```bash
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State] FROM workitems WHERE [System.WorkItemType] = 'Task' AND [System.State] <> 'Done' AND [System.TeamProject] = 'ProjectName' ORDER BY [Microsoft.VSTS.Common.Priority]" -o table
```

### Query with tags
```bash
az boards query --wiql "SELECT [System.Id], [System.Title] FROM workitems WHERE [System.Tags] CONTAINS 'urgent' AND [System.TeamProject] = 'ProjectName'" -o table
```

### Unassigned items
```bash
az boards query --wiql "SELECT [System.Id], [System.Title] FROM workitems WHERE [System.AssignedTo] = '' AND [System.State] = 'New' AND [System.TeamProject] = 'ProjectName'" -o table
```

## Common Field Names for SELECT/WHERE

| Field | Reference Name |
|-------|----------------|
| ID | System.Id |
| Title | System.Title |
| State | System.State |
| Type | System.WorkItemType |
| Assigned To | System.AssignedTo |
| Created By | System.CreatedBy |
| Area | System.AreaPath |
| Iteration | System.IterationPath |
| Created | System.CreatedDate |
| Changed | System.ChangedDate |
| Priority | Microsoft.VSTS.Common.Priority |
| Severity | Microsoft.VSTS.Common.Severity |
| Tags | System.Tags |
| Story Points | Microsoft.VSTS.Scheduling.StoryPoints |

## WIQL Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equals | `[System.State] = 'Active'` |
| `<>` | Not equals | `[System.State] <> 'Closed'` |
| `>`, `<`, `>=`, `<=` | Comparison | `[Microsoft.VSTS.Common.Priority] <= 2` |
| `CONTAINS` | Contains text | `[System.Tags] CONTAINS 'urgent'` |
| `NOT CONTAINS` | Does not contain | `[System.Title] NOT CONTAINS 'test'` |
| `IN` | In list | `[System.State] IN ('Active', 'New')` |
| `NOT IN` | Not in list | `[System.State] NOT IN ('Closed', 'Removed')` |
| `UNDER` | Under path | `[System.AreaPath] UNDER 'Project\Team'` |
| `AND`, `OR` | Logical operators | `[A] = 'x' AND [B] = 'y'` |

## Macros (Use With Caution)

| Macro | Description | Reliability |
|-------|-------------|-------------|
| `@Me` | Current user | Usually works |
| `@Today` | Today's date | Works |
| `@Today - N` | N days ago | Works |
| `@project` | Current project | UNRELIABLE - use explicit name |
| `@CurrentIteration` | Current sprint | May not work in CLI |

## Output Formats

- `-o table` - Human readable table
- `-o json` - Full JSON output
- `-o tsv` - Tab-separated values

## Tips

1. **Always quote string values**: `'Active'` not `Active`
2. **Use brackets around field names**: `[System.State]` not `System.State`
3. **Escape single quotes by doubling**: `'It''s working'`
4. **Path separators use backslash**: `'Project\Team\SubArea'` (double in bash: `'Project\\Team'`)
5. **Always include project filter**: Add `[System.TeamProject] = 'Name'` for reliable results

## Parent Filtering Pattern

Since ORDER BY [System.Parent] is not supported, use the IN clause to filter by parent:

```bash
# Find all children of specific parents
az boards query --wiql "SELECT [System.Id], [System.Title], [System.Parent] FROM WorkItems WHERE [System.Parent] IN (1234, 1235, 1236) AND [System.TeamProject] = 'ProjectName'" -o table
```

This works well for:
- Finding all tasks under specific features
- Listing child items for a set of parent work items
- Building hierarchies by querying children of known parents
