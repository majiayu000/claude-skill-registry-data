---
name: jira-ticket-creator
description: |
  Create Jira tickets from meeting notes, user stories, or quick lists. Use this skill when:
  - User says "create tickets", "make Jira tickets from", "push to Jira"
  - User has meeting action items to convert to tickets
  - User has user stories from a spec to push to the backlog
  - User wants to batch-create tasks, stories, or bugs
---

# Jira Ticket Creator

Parse any input into structured Jira tickets. Works with meeting action items, user stories from specs, or free-text lists.

## Input Sources

- Meeting action items
- User stories from spec files
- Free-text lists ("Create tickets for: X, Y, Z")
- Sprint planning output

## Field Mapping

| Field | Source | Default |
|-------|--------|---------|
| Summary | First line or action item text | Required |
| Description | Context, acceptance criteria if available | Empty |
| Type | Infer from content | Story |
| Priority | From context | Medium |
| Story Points | Estimate from complexity | Blank |
| Assignee | Match name to team directory | Unassigned |
| Epic | Link if specified in input | None |
| Sprint | Specified or current sprint | Current |

**Type inference:**
- Contains "bug", "fix", "broken", "error" -> Bug
- Contains "investigate", "research", "spike" -> Task
- Everything else -> Story

## Workflow

1. **Parse** — extract individual ticket items from input
2. **Enrich** — add type, priority, assignee, epic from context
3. **Present** — show ticket table to user for confirmation
4. **Confirm** — user reviews, edits, approves
5. **Create** — create tickets via Jira REST API
6. **Log** — report created tickets with keys

## Confirmation Format

```
| # | Summary | Type | Priority | Assignee | Points | Epic |
|---|---------|------|----------|----------|--------|------|
| 1 | Implement feature X | Story | High | [name] | 5 | [Epic] |
| 2 | Fix login bug | Bug | Medium | [name] | 1 | [Epic] |

Total: 2 tickets, 6 story points
Proceed? (y/n/edit)
```

## Rules

- Maximum 15 tickets per batch (split larger lists)
- Always confirm before creating
- Show total story points in confirmation

## Anti-Patterns

- Don't create tickets without user confirmation
- Don't guess assignees — ask if unclear
- Don't create more than 15 tickets at once

## Quality Checklist

- [ ] Every ticket has a clear summary
- [ ] Type correctly inferred or specified
- [ ] User confirmed before creation
- [ ] Total story points shown
