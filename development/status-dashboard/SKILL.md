---
name: status-dashboard
description: Display project status and backlog overview. Use when user asks about current status, what's in progress, what to work on next, or wants a summary of the backlog. Read-only skill that formats backlog.json into a clear dashboard view.
allowed-tools: Read
---

# Status Dashboard

Provide a quick overview of project status and backlog.

## When to Use

Invoke this skill when the user asks:
- "What's in progress?"
- "What's the status?"
- "What should I work on next?"
- "Show me the backlog"
- "What have we completed recently?"
- "Give me a project overview"

## Instructions

### Step 1: Load the Backlog

```
Read: docs/planning/backlog.json
```

If file doesn't exist:
```
No backlog found. Use /feature-capture to start tracking features.
```

### Step 2: Parse and Categorize

Extract from the JSON:
- `summary` object for quick counts
- `items` array for details

Group items by status:
- `in-progress`: Currently being worked on
- `backlog`: Waiting to be started
- `completed`: Recently finished

### Step 3: Calculate Metrics

For in-progress items:
- Time elapsed since `startedAt`

For backlog items:
- Sort by priority (P0 first)
- Note time since `createdAt`

For completed items:
- Show most recent completions (last 5)
- Calculate time from start to completion

### Step 4: Format the Dashboard

```markdown
# Project Status

## Summary
- **In Progress**: [count]
- **Backlog**: [count] (P0: [n], P1: [n], P2: [n])
- **Completed**: [count]

---

## In Progress
[For each in-progress item:]
### [name]
- **ID**: [id]
- **Started**: [startedAt] ([X days] ago)
- **Priority**: [priority] | **Effort**: [effort]
- **Plan**: docs/planning/features/[id]/plan.md

---

## Up Next (Top Priority Backlog)
[Show top 5 by priority:]
| Priority | Name | Effort | Impact | Added |
|----------|------|--------|--------|-------|
| [P0/P1/P2] | [name] | [effort] | [impact] | [X days ago] |

[If more exist:] + [N] more items in backlog

---

## Recently Completed
[Show last 3-5:]
- **[name]** - Completed [completedAt] (took [X days])
```

## Output Format

Keep it scannable:
- Use headers to separate sections
- Tables for lists
- Highlight what needs attention (P0 items, long-running work)

### Compact Format (for quick checks)

If user just wants a quick status:
```
Status: 1 in progress, 5 in backlog (2 P0), 3 completed

In Progress: Dark Mode Toggle (3 days)
Next Up: User Authentication (P0), API Rate Limiting (P0)
```

## Integration Notes

This skill works with:
- `backlog-awareness` skill - For deeper dives into specific items
- `/feature-plan` - Suggest for starting backlog items
- `/feature-ship` - Suggest for finishing in-progress items
