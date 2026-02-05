---
name: board-status
description: Check GitHub Project board status for the monorepo. Use when user asks about board status, what's in progress, sprint status, or issue tracking.
allowed-tools: Bash, Read
---

# Board Status Skill

## Purpose

Automatically fetch and summarize GitHub Project board status when the user asks about sprint progress, what's being worked on, or issue tracking. This is a read-only skill.

## When Claude Should Use This

- User asks "what's in progress?"
- User asks "board status"
- User asks "sprint status"
- User asks "what's next to work on?"
- User asks "what's blocked?" or "what's awaiting review?"
- User mentions project tracking

## Instructions

### Get All Board Items

```bash
# Using GraphQL (more reliable - doesn't require read:org scope)
gh api graphql -f query='
  query {
    organization(login: "rollercoaster-dev") {
      projectV2(number: 11) {
        items(first: 100) {
          nodes {
            id
            fieldValueByName(name: "Status") {
              ... on ProjectV2ItemFieldSingleSelectValue { name }
            }
            content {
              ... on Issue { number title assignees(first: 5) { nodes { login } } }
              ... on PullRequest { number title }
            }
          }
        }
      }
    }
  }'
```

### Get Items by Status

Parse the JSON output and filter by status field name (e.g., "In Progress", "Blocked").

## Board Configuration

**Project:** Monorepo Development (#11)
**URL:** https://github.com/orgs/rollercoaster-dev/projects/11

### Status Columns

| Status      | Description                                 | Color  |
| ----------- | ------------------------------------------- | ------ |
| Backlog     | Not yet ready (needs triage/prioritization) | Gray   |
| Next        | Ready to pick up - dependencies met         | Blue   |
| In Progress | Currently being worked on                   | Yellow |
| Blocked     | PR created, awaiting review                 | Purple |
| Done        | Merged to main                              | Green  |

### Project IDs (for updates - use agents, not this skill)

- Project ID: `PVT_kwDOB1lz3c4BI2yZ`
- Status Field ID: `PVTSSF_lADOB1lz3c4BI2yZzg5MUx4`

Status Option IDs:

- Backlog: `8b7bb58f`
- Next: `266160c2`
- In Progress: `3e320f16`
- Blocked: `51c2af7b`
- Done: `56048761`

## Output Format

```markdown
## Board Status

### In Progress (<count>)

- #X: <title> (@assignee)

### Blocked (<count>)

- #X: <title> - PR #Y (awaiting review)

### Next (<count>)

- #X: <title>

### Recently Done (<count>)

- #X: <title> - Merged <date>
```

## Note

This skill is **read-only**. To update board status, use the `atomic-developer`, `pr-creator`, or `review-handler` agents which have write permissions.
