---
name: project-management
description: Manage GitHub Projects V2 including listing projects, adding items, updating statuses, and managing custom fields.
groups: [copilot]
---

# GitHub Projects Management

Comprehensive project management using GitHub Projects V2 APIs.

## When to Use This Skill

Use when users:
- Want to add issues or PRs to project boards
- Need to update item statuses or custom fields
- Request project board information
- Ask to organize or track work items
- Want to see project progress
- Need to manage sprint planning

## Instructions

When managing GitHub Projects:

1. **List Available Projects**:
   ```
   Use list_projects to see all projects
   ```

2. **View Project Details**:
   ```
   Use get_project to view project configuration
   Use list_project_fields to see available custom fields
   Use list_project_items to see current items
   ```

3. **Add Items to Projects**:
   ```
   Use add_project_item with issue or PR URL
   ```

4. **Update Item Fields**:
   ```
   Use update_project_item to change:
   - Status (e.g., "In Progress", "Done")
   - Priority
   - Sprint assignment
   - Custom field values
   ```

5. **Track Progress**:
   ```
   Use get_project_item for detailed item info
   Filter and summarize project status
   ```

## Available Tools

- `list_projects` - See all projects in a repository
- `get_project` - Get detailed project information
- `list_project_fields` - View available custom fields
- `list_project_items` - List all items in a project
- `get_project_item` - Get details for a specific item
- `add_project_item` - Add issue/PR to project
- `update_project_item` - Update item fields and status
- `delete_project_item` - Remove item from project
