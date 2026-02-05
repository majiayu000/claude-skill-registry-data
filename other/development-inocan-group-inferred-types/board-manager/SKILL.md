---
name: board-manager
description: Manage GitHub Project board items - add issues, update status, move between columns. Use when user asks to add issues to board, change status, or organize the project.
allowed-tools: Bash, Read
---

# Board Manager Skill

## Purpose

Add issues to the project board and update their status. This skill has **write permissions** for board operations.

## When Claude Should Use This

- User asks "add this issue to the board"
- User asks "move #X to In Progress"
- User asks "update status of issue"
- User asks "put this in the backlog"
- After creating a new issue (auto-add to board)
- After completing work (move to Done)

## Project Board Configuration

**Project:** Monorepo Development (#11)
**URL:** https://github.com/orgs/rollercoaster-dev/projects/11

### IDs Reference

| Resource        | ID                               |
| --------------- | -------------------------------- |
| Project ID      | `PVT_kwDOB1lz3c4BI2yZ`           |
| Status Field ID | `PVTSSF_lADOB1lz3c4BI2yZzg5MUx4` |

### Status Option IDs

| Status      | Option ID  | Description                 |
| ----------- | ---------- | --------------------------- |
| Backlog     | `8b7bb58f` | Not ready / needs triage    |
| Next        | `266160c2` | Ready to pick up            |
| In Progress | `3e320f16` | Currently being worked on   |
| Blocked     | `51c2af7b` | PR created, awaiting review |
| Done        | `56048761` | Merged to main              |

## Helper Functions

These reusable functions simplify board operations:

### Get Item ID for Issue

```bash
get_item_id_for_issue() {
  local issue_number=$1
  gh api graphql -f query='
    query {
      organization(login: "rollercoaster-dev") {
        projectV2(number: 11) {
          items(first: 100) {
            nodes {
              id
              content { ... on Issue { number } }
            }
          }
        }
      }
    }' | jq -r ".data.organization.projectV2.items.nodes[] | select(.content.number == $issue_number) | .id"
}
```

### Update Board Status (with validation)

```bash
update_board_status() {
  local item_id=$1
  local option_id=$2
  local status_name=$3

  RESULT=$(gh api graphql \
    -f projectId="PVT_kwDOB1lz3c4BI2yZ" \
    -f itemId="$item_id" \
    -f fieldId="PVTSSF_lADOB1lz3c4BI2yZzg5MUx4" \
    -f optionId="$option_id" \
    -f query='mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $fieldId
        value: { singleSelectOptionId: $optionId }
      }) {
        projectV2Item { id }
      }
    }' 2>&1)

  # Validate response - check for GraphQL errors
  if echo "$RESULT" | jq -e '.errors | length > 0' > /dev/null 2>&1; then
    echo "ERROR: Board update failed (GraphQL error)"
    return 1
  elif echo "$RESULT" | jq -e '.data.updateProjectV2ItemFieldValue.projectV2Item.id' > /dev/null 2>&1; then
    echo "Board Update: Issue moved to '$status_name'"
    return 0
  else
    echo "ERROR: Board update failed (unexpected response)"
    return 1
  fi
}
```

## Commands

### Add Issue to Project Board

```bash
gh project item-add 11 --owner rollercoaster-dev --url https://github.com/rollercoaster-dev/monorepo/issues/<number>
```

### Get Item ID for an Issue

```bash
# Using GraphQL (more reliable - doesn't require read:org scope)
gh api graphql -f query='
  query {
    organization(login: "rollercoaster-dev") {
      projectV2(number: 11) {
        items(first: 100) {
          nodes {
            id
            content { ... on Issue { number } }
          }
        }
      }
    }
  }' | jq -r '.data.organization.projectV2.items.nodes[] | select(.content.number == <issue-number>) | .id'
```

### Update Issue Status

```bash
# Use GraphQL mutation (avoids OAuth scope issues with gh project item-edit)
gh api graphql \
  -f projectId="PVT_kwDOB1lz3c4BI2yZ" \
  -f itemId="<item-id>" \
  -f fieldId="PVTSSF_lADOB1lz3c4BI2yZzg5MUx4" \
  -f optionId="<option-id>" \
  -f query='mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
    updateProjectV2ItemFieldValue(input: {
      projectId: $projectId
      itemId: $itemId
      fieldId: $fieldId
      value: { singleSelectOptionId: $optionId }
    }) {
      projectV2Item { id }
    }
  }'
```

### Remove Issue from Project

```bash
gh project item-delete 11 --owner rollercoaster-dev --id <item-id>
```

## Workflow Examples

### Add New Issue and Set Status

```bash
# 1. Add to project using GraphQL mutation
ISSUE_NODE_ID=$(gh issue view 123 --json id -q .id)
gh api graphql -f query='
  mutation($projectId: ID!, $contentId: ID!) {
    addProjectV2ItemById(input: {
      projectId: $projectId
      contentId: $contentId
    }) { item { id } }
  }' -f projectId="PVT_kwDOB1lz3c4BI2yZ" -f contentId="$ISSUE_NODE_ID" 2>/dev/null || true

# 2. Get item ID and set status using helper functions
ITEM_ID=$(get_item_id_for_issue 123)
update_board_status "$ITEM_ID" "266160c2" "Next"
```

### Move Issue to In Progress

```bash
# Using helper functions
ITEM_ID=$(get_item_id_for_issue <issue-number>)
update_board_status "$ITEM_ID" "3e320f16" "In Progress"
```

### Move Issue to Blocked (after PR creation)

```bash
ITEM_ID=$(get_item_id_for_issue <issue-number>)
update_board_status "$ITEM_ID" "51c2af7b" "Blocked"
```

### Move Issue to Done (after merge)

```bash
ITEM_ID=$(get_item_id_for_issue <issue-number>)
update_board_status "$ITEM_ID" "56048761" "Done"
```

## Status Mapping

| Action               | Status      | Option ID  |
| -------------------- | ----------- | ---------- |
| New issue, not ready | Backlog     | `8b7bb58f` |
| Ready to work        | Next        | `266160c2` |
| Started work         | In Progress | `3e320f16` |
| PR created           | Blocked     | `51c2af7b` |
| PR merged            | Done        | `56048761` |

## Output Format

After operations, confirm:

```markdown
**Board Update:** Issue #X moved to [Status]
**URL:** https://github.com/orgs/rollercoaster-dev/projects/11
```

## Query Current IDs (if they change)

```bash
gh api graphql -f query='
query {
  organization(login: "rollercoaster-dev") {
    projectV2(number: 11) {
      id
      field(name: "Status") {
        ... on ProjectV2SingleSelectField {
          id
          options { id name }
        }
      }
    }
  }
}'
```
