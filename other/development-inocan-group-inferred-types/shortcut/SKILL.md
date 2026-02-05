---
name: shortcut
description: MUST use when interacting with Shortcut's project management platform to create, update, search, or retrieve stories, epics, iterations, teams, workflows, objectives, and documents.
---

# Shortcut Tool Reference

Use `shortcut-api-read` for read operations and `shortcut-api-write` for write operations.

Pattern: `shortcut-api-{read|write} <entity> <operation> [args...]`

## Operations

### Stories

Stories are the standard unit of work in Shortcut.

**Get a story:**

```bash
shortcut-api-read stories get <story-id>
```

**Search stories:**

```bash
shortcut-api-read stories search \
  --query "search text" \
  --owner-ids <user-id> \
  --team-id <team-id> \
  --iteration-id <iteration-id> \
  --epic-id <epic-id> \
  --workflow-state-id <state-id> \
  --story-type feature|bug|chore \
  --limit 25
```

**Get branch name for a story:**

```bash
shortcut-api-read stories branch-name <story-id>
```

Returns a formatted git branch name like `sc-123/feature-description`

**Create a story:**

```bash
shortcut-api-write stories create "Story title" \
  --type feature|bug|chore \
  --description "Story description" \
  --team-id <team-id> \
  --owner-ids <user-id> <user-id> \
  --iteration-id <iteration-id> \
  --epic-id <epic-id> \
  --estimate 3
```

**Create a story and checkout a branch:**

```bash
shortcut-api-write stories create-and-checkout "Story title" \
  --type feature|bug|chore \
  --description "Story description" \
  --team-id <team-id> \
  --owner-ids <user-id> <user-id> \
  --iteration-id <iteration-id> \
  --epic-id <epic-id> \
  --estimate 3
```

**Update a story:**

```bash
shortcut-api-write stories update <story-id> \
  --name "New title" \
  --description "New description" \
  --type bug \
  --workflow-state-id <state-id> \
  --iteration-id <iteration-id> \
  --archived
```

**Delete a story:**

```bash
shortcut-api-write stories delete <story-id>
```

**Add a comment to a story:**

```bash
shortcut-api-write stories comment <story-id> "Comment text"
```

### Epics

Epics are collections of related stories representing larger features or initiatives.

**Get an epic:**

```bash
shortcut-api-read epics get <epic-id>
```

**List all epics:**

```bash
shortcut-api-read epics list
```

**Search epics:**

```bash
shortcut-api-read epics search --query "search text" --state "in progress"
```

**Create an epic:**

```bash
shortcut-api-write epics create "Epic name" \
  --description "Epic description" \
  --state "to do" \
  --owner-ids <user-id>
```

**Update an epic:**

```bash
shortcut-api-write epics update <epic-id> \
  --name "New name" \
  --state "done" \
  --archived
```

**Delete an epic:**

```bash
shortcut-api-write epics delete <epic-id>
```

### Iterations

Iterations (sprints) are time-boxed periods of development.

**Get current active iteration:**

```bash
shortcut-api-read iterations list --status started
```

**Get a specific iteration:**

```bash
shortcut-api-read iterations get <iteration-id>
```

**List all iterations:**

```bash
shortcut-api-read iterations list
shortcut-api-read iterations list --status started|unstarted|done
shortcut-api-read iterations list --with-stats
```

**Create an iteration:**

```bash
shortcut-api-write iterations create "Sprint 1" 2025-01-01 2025-01-14 \
  --description "Sprint description" \
  --team-ids <team-id>
```

**Update an iteration:**

```bash
shortcut-api-write iterations update <iteration-id> \
  --name "Sprint 2" \
  --start-date 2025-01-15 \
  --end-date 2025-01-28
```

**Delete an iteration:**

```bash
shortcut-api-write iterations delete <iteration-id>
```

### Teams

Teams represent groups of people working together.

**Get a team:**

```bash
shortcut-api-read teams get <team-id>
```

**List all teams:**

```bash
shortcut-api-read teams list
```

### Workflows

Workflows define the states that stories move through.

**Get a workflow:**

```bash
shortcut-api-read workflows get <workflow-id>
```

**List all workflows:**

```bash
shortcut-api-read workflows list
```

### Users/Members

Manage workspace members and get current user information.

**Get a member:**

```bash
shortcut-api-read users get <member-id>
```

**List all members:**

```bash
shortcut-api-read users list
```

**Get current user:**

```bash
shortcut-api-read users current
```

**Get current user's teams:**

```bash
shortcut-api-read users current-teams
```

### Objectives

Objectives represent high-level goals.

**Get an objective:**

```bash
shortcut-api-read objectives get <objective-id>
```

**List all objectives:**

```bash
shortcut-api-read objectives list
```

**Create an objective:**

```bash
shortcut-api-write objectives create "Objective name" \
  --description "Objective description"
```

**Update an objective:**

```bash
shortcut-api-write objectives update <objective-id> \
  --name "New name" \
  --state "done"
```

**Delete an objective:**

```bash
shortcut-api-write objectives delete <objective-id>
```

### Documents

Create documentation in Shortcut.

**Create a document:**

```bash
shortcut-api-write documents create "Doc title" "<h1>HTML Content</h1>"
```

## Common Workflows

### Get Stories in Current Iteration

```bash
# Get current iteration
shortcut-api-read iterations list --status started
# Then search stories with the iteration ID and your user ID
shortcut-api-read stories search --iteration-id <id> --owner-ids <user-id>
```

### Creating a Story with Full Context

When creating a story, gather the necessary IDs first:

1. Get current user: `shortcut-api-read users current`
2. List teams: `shortcut-api-read teams list`
3. Get current iteration: `shortcut-api-read iterations list --status started`
4. Create the story with gathered information

### Story Creation from Title

For the common pattern of parsing a conventional commit-style title:

```bash
# Parse title like "feat(edge-gateway): add v2 rate limiting"
# Extract type (feat = feature, bug = bug, chore = chore)
# Get team ID for "Infra Team"
# Get current user or specified owner
# Get current started iteration
# Create story and get branch name

shortcut-api-write stories create "add v2 rate limiting" \
  --type feature \
  --team-id <infra-team-id> \
  --owner-ids <user-id> \
  --iteration-id <current-iteration-id>

# Then get the branch name
shortcut-api-read stories branch-name <new-story-id>
```
