---
type: Skill
name: design-team-management
description: Manage organizational teams and professional roles in the NV oOS Pro Toolkit. Covers team creation, profession definitions, role assignments, and organizational structure. Use when setting up teams, defining professional roles, assigning users to teams, or managing organizational hierarchy.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# NV oOS Pro Toolkit Team Management

The Pro Toolkit Team Management system provides organizational structure
built on WordPress Custom Post Types. It defines the hierarchy: **professions
(specialties) → teams (organizational units) → users (team members)**. All
entities are stored as CPT records accessible via the `toolkit_cpt` MCP tool.

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for team management operations. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai cron` | Check team sync cron events (user-to-team assignments, role propagation) |
| `wp mcp-ai queue` | Inspect team import/export background jobs |
| `wp mcp-ai health` | Verify team structure integrity, orphaned members, missing professions |
| `wp mcp-ai log` | View team assignment and role change logs |
| `wp user list --role=<role>` | List WordPress users by role for team assignment planning |

## When to use this skill

Trigger when ANY of the following is true:

- Creating, updating, or deleting teams (organizational units).
- Defining or modifying professional roles and specialties.
- Assigning users to teams or professions.
- Reviewing organizational structure — which teams exist, who belongs to them.
- Searching for teams by name, profession, or membership.
- Building team hierarchies (parent/child teams, departments, divisions).
- Onboarding new staff — creating their profession record and team assignment.
- Auditing team composition for role coverage gaps.
- Managing profession metadata like thumbnails, descriptions, and required skills.

## Mental model — Teams and professions

The team management system is organized around two entity types in a
many-to-many relationship:

```
PROFESSION ──(defines role)──→ USER ←──(belongs to)── TEAM
     │                                                    │
     ├── title (specialty name)                          ├── title (team name)
     ├── editor (rich description)                       ├── editor (team description)
     └── thumbnail (icon/badge)                          └── members (via user meta or CPT links)
```

**Relationships:**
- A **Profession** (`mcp_ai_profession`) represents a role, specialty, or job function
  (e.g., "Cardiologist", "Frontend Developer", "Project Manager").
- A **Team** (`mcp_ai_team`) represents an organizational unit, department, or
  project group (e.g., "Cardiology Department", "Engineering Team Alpha").
- **Users** are WordPress user accounts. Team membership and profession are typically
  stored as user meta or linked via additional CPT relationships.
- One user can belong to multiple teams and hold one or more professions.
- Teams can have hierarchical relationships (parent/child) for departments and
  sub-teams, managed via the standard WordPress `post_parent` field.

## Team Management Entity Types

All team management entities are managed through the **`toolkit_cpt`** MCP tool.
Use the appropriate `post_type` slug for each entity:

| CPT Slug | Label | Purpose | Supported Fields |
|---|---|---|---|
| `mcp_ai_team` | Teams | Organizational units, departments, project groups | `title`, `editor` (content), `post_parent` (hierarchy) |
| `mcp_ai_profession` | Professions | Professional roles, specialties, job functions | `title`, `editor` (content), `thumbnail` (featured image) |

### Team Fields (detailed)

| Field | Type | Description | Example |
|---|---|---|---|
| `title` | string | Team name | `"Cardiology Department"`, `"Engineering Team Alpha"` |
| `content` | string | Team description, mission, or charter | Rich text describing the team's purpose and scope |
| `post_parent` | integer | Parent team ID for hierarchy | `15` (parent team post ID) |
| `status` | string | Post status | `"publish"`, `"draft"` |
| `author_id` | integer | WordPress user ID of the team lead or creator | `7` |

### Profession Fields (detailed)

| Field | Type | Description | Example |
|---|---|---|---|
| `title` | string | Profession name | `"Cardiologist"`, `"Senior Frontend Developer"` |
| `content` | string | Role description, responsibilities, required qualifications | Rich text describing the role |
| `thumbnail` | integer | Featured image attachment ID (badge, icon, or photo) | `205` |
| `status` | string | Post status | `"publish"`, `"draft"` |
| `author_id` | integer | WordPress user ID of the role creator | `1` |

## Available Tools

All team management operations use the **`toolkit_cpt`** MCP tool. This is the
single interface for all team and profession CRUD operations.

### Discovery

```
# List all available team management post types
toolkit_cpt(action: "list_types")

# Get field schema for teams or professions
toolkit_cpt(action: "get_schema", post_type: "mcp_ai_team")
toolkit_cpt(action: "get_schema", post_type: "mcp_ai_profession")
```

### Reading records

```json
// List all teams
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "list_items",
    "post_type": "mcp_ai_team",
    "orderby": "title",
    "order": "ASC",
    "per_page": 50,
    "page": 1
  }
}

// Search teams by name
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "list_items",
    "post_type": "mcp_ai_team",
    "search": "Cardiology"
  }
}

// List all professions
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "list_items",
    "post_type": "mcp_ai_profession",
    "orderby": "title",
    "order": "ASC",
    "per_page": 50
  }
}

// Search professions by name
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "list_items",
    "post_type": "mcp_ai_profession",
    "search": "Developer"
  }
}

// Get a single team or profession
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "get_item",
    "post_type": "mcp_ai_team",
    "item_id": 42
  }
}
```

### Creating records

```json
// Create a new team
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "create_item",
    "post_type": "mcp_ai_team",
    "fields": {
      "title": "Cardiology Department",
      "content": "The Cardiology Department provides comprehensive cardiac care including diagnostics, interventional procedures, and long-term heart health management.",
      "status": "publish"
    }
  }
}

// Create a child team (sub-team under a parent)
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "create_item",
    "post_type": "mcp_ai_team",
    "fields": {
      "title": "Interventional Cardiology Unit",
      "content": "Specialized unit within Cardiology handling catheter-based procedures.",
      "status": "publish",
      "post_parent": 42
    }
  }
}

// Create a new profession
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "create_item",
    "post_type": "mcp_ai_profession",
    "fields": {
      "title": "Interventional Cardiologist",
      "content": "Board-certified cardiologist specializing in catheter-based treatment of structural heart diseases. Requires fellowship training in interventional cardiology.",
      "status": "publish"
    }
  }
}
```

### Updating records

```json
// Rename a team
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "update_item",
    "post_type": "mcp_ai_team",
    "item_id": 42,
    "fields": {
      "title": "Cardiology & Vascular Department"
    }
  }
}

// Update a profession's description and thumbnail
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "update_item",
    "post_type": "mcp_ai_profession",
    "item_id": 88,
    "fields": {
      "title": "Senior Interventional Cardiologist",
      "content": "Updated: Requires 5+ years post-fellowship experience. Leads complex structural heart interventions including TAVR and MitraClip procedures."
    }
  }
}

// Re-parent a team (move under a different parent)
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "update_item",
    "post_type": "mcp_ai_team",
    "item_id": 55,
    "fields": {
      "post_parent": 99
    }
  }
}
```

### Deleting records

```json
// Delete a team
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "delete_item",
    "post_type": "mcp_ai_team",
    "item_id": 42
  }
}
```

**⚠️ Warning:** Deleting a team is permanent. Before deleting, reassign any
member users and re-parent any child teams. Consider archiving via `status: "draft"`
instead, to preserve organizational history.

## Common Workflows

### Setting up organizational structure

```
1. Define professions:    create_item(mcp_ai_profession) for each role in the organization.
2. Create top-level teams:  create_item(mcp_ai_team) for departments or divisions.
3. Create sub-teams:        create_item(mcp_ai_team, post_parent: <parent_id>) for units.
4. Verify hierarchy:        list_items(mcp_ai_team, orderby: "title")
                            → Review the parent-child structure for correctness.
5. Assign users:            Link WordPress users to teams via user meta or assignment CPT.
6. Set team lead:           update_item(mcp_ai_team, author_id: <user_id>) for the team lead.
```

### Onboarding a new team member

```
1. Verify profession:    get_item(mcp_ai_profession, item_id: <profession_id>)
                         If the role doesn't exist yet: create_item(mcp_ai_profession).
2. Verify team:          get_item(mcp_ai_team, item_id: <team_id>)
3. Assign user:          Link the WordPress user to the team (via user meta or CPT).
4. Set profession:       Assign the user's profession (user meta or role assignment CPT).
5. Document:             Add user details to team's content or a team membership log.
```

### Organizational audit

```
1. List all teams:         list_items(mcp_ai_team, per_page: 50)
2. List all professions:   list_items(mcp_ai_profession, per_page: 50)
3. Check for gaps:         Identify teams with no assigned members or vacant professions.
4. Check for orphans:      Find child teams whose post_parent references a deleted team.
5. Review stale records:   Find unpublished (draft/trash) teams and professions — archive or clean up.
```

### Restructuring — merging teams

```
1. Identify source team:   get_item(mcp_ai_team, item_id: <source_id>)
2. Identify target team:   get_item(mcp_ai_team, item_id: <target_id>)
3. Reassign child teams:   For each child of source, update_item(post_parent: <target_id>)
4. Reassign members:       Move all users from source team to target team.
5. Archive source:         update_item(mcp_ai_team, item_id: <source_id>, status: "draft")
                           OR delete_item if the team is truly obsolete.
```

## Critical Rules

- **Always use `get_schema` first** before creating or updating a record to verify available field keys and types.
- **Team names must be unique within the same parent** — two sibling teams cannot share the same `title`.
- **`post_parent` creates hierarchy** — use it for departments → units, not for loose organizational tags. The parent must exist before a child references it.
- **Profession `title` should be singular and descriptive** — use "Cardiologist" not "Cardiology" (that's a team name) and not "Cardiologists" (that's a plural).
- **Do not delete a team that has children** — re-parent child teams first, or delete children bottom-up.
- **`status` field controls visibility** — use `"publish"` for active teams/professions and `"draft"` for planned, inactive, or archived ones.
- **`thumbnail` (featured image) on professions must be a valid attachment ID** — verify the attachment exists before referencing it.

## Common Mistakes

```
WRONG — deleting a team that has child teams
{ "action": "delete_item", "post_type": "mcp_ai_team", "item_id": 42 }
// Child teams with post_parent: 42 are now orphaned — they point to a deleted parent.

RIGHT — re-parent children before deleting
1. list_items(mcp_ai_team, filters: [{key: "post_parent", value: "42"}])
2. For each child: update_item(mcp_ai_team, item_id: <child_id>,
     fields: { "post_parent": <new_parent_id> })
3. Then: delete_item(mcp_ai_team, item_id: 42)

WRONG — creating a profession with a team name
{ "action": "create_item", "post_type": "mcp_ai_profession",
  "fields": { "title": "Cardiology Department" } }
// "Cardiology Department" is a team/organizational unit, not a profession.
// Profession should be: "Cardiologist"

RIGHT — use distinct, role-oriented names for professions
{ "action": "create_item", "post_type": "mcp_ai_profession",
  "fields": { "title": "Cardiologist",
  "content": "Medical doctor specializing in diagnosing and treating diseases of the cardiovascular system." } }

WRONG — using non-standard status values
// "active", "inactive", "archived" — these are not valid WordPress post statuses.

RIGHT — use standard WordPress statuses
// "publish" for active, "draft" for planned/inactive/archived.

WRONG — referencing a post_parent that doesn't exist
{ "post_parent": 99999 }  // This team ID doesn't exist — the hierarchy is broken.

RIGHT — verify parent exists before assigning
1. get_item(mcp_ai_team, item_id: <parent_id>) — confirm it returns a valid record.
2. Then: create_item or update_item with the confirmed post_parent.
```

## Cross-References

- Run `design-crm` to link team members to CRM contacts, leads, and company relationships.
- Run `design-pro-workflow-builder` to automate team onboarding workflows and role-based task routing.
- Run `design-pro-schedule-manager` to schedule recurring team syncs, reviews, and roster updates.
- Run `design-communications` to set up team-specific communication channels and contact groups.
- Run `wp-security-audit` on any team assignment code — team membership controls access and must be properly authorized.

## What This Skill Does NOT Cover

- WordPress user account creation and role management — use WordPress admin or WP-CLI (`wp user create`) for user accounts.
- User-to-team assignment mechanics — the specific meta keys or CPT relationships linking users to teams vary by implementation. This skill covers the Team and Profession CPTs themselves.
- Frontend team directory display — this skill covers data management; rendering is a theme concern.
- Permission and capability configuration — use WordPress role/capability APIs for access control based on team membership.
- External HR system integration — use `ezuite_erp` or custom REST endpoints for HR data sync.
