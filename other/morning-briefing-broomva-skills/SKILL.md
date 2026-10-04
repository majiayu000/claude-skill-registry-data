---
name: morning-briefing
category: cadence
description: >
  Reads open action items, this week's priorities, and recent vault updates, then produces
  a focused "start your day" brief. Use when the user says "morning briefing", "daily brief",
  "what's on my plate", "start my day", "what should I focus on today", or at the start of
  a work session.
---

# Morning Briefing

Produce a focused daily brief to start the day.

## Workflow

1. **Scan open action items** — Search the vault for unchecked tasks (`- [ ]`):
   - In project docs, meeting notes, and daily journals
   - Prioritize by: overdue > due today > due this week > no date
   - Cap at 10 most important items

2. **Check this week's priorities** — Look for:
   - `weekly-plan.md` or `weekly-review-*.md` in the vault
   - Any pinned/starred notes
   - Current sprint or milestone items

3. **Scan recent vault changes** — Check files modified in the last 24 hours:
   - New notes created
   - Significant edits to project docs
   - New decisions logged

4. **Check git activity** — Run `git log --since="yesterday" --oneline` across active repos to surface:
   - Commits made yesterday
   - Open PRs or branches

5. **Compose the brief** — Organize into a scannable format.

## Output Format

```markdown
## Morning Briefing — [Day, YYYY-MM-DD]

### Focus Today
1. [Top priority — why it matters]
2. [Second priority]
3. [Third priority]

### Open Action Items ([count] total)
**Overdue**
- [ ] [item] — from [[source note]] (due [date])

**Due Today**
- [ ] [item] — from [[source note]]

**This Week**
- [ ] [item] — from [[source note]]

### What Changed Yesterday
- [vault change or git activity summary]
- [vault change or git activity summary]

### Heads Up
- [Anything requiring attention: upcoming deadlines, blocked items, meetings]
```

## Vault Integration

- Read from: `~/broomva-vault/` (all folders)
- Optionally save the brief to: `journal/briefing-[YYYY-MM-DD].md`

## Behavior

- Keep it concise — the goal is a 2-minute read, not a comprehensive report
- Highlight blockers and overdue items prominently
- If no vault is accessible, generate the brief from git activity alone
- Don't invent priorities — only surface what exists in the vault and git history
