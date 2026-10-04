---
name: weekly-review
category: cadence
description: >
  Scans the vault for updates from the past week, surfaces what changed, and flags what
  needs attention. Produces a structured weekly review. Use when the user says "weekly review",
  "week in review", "what happened this week", "weekly summary", "end of week review",
  or at the end of a work week.
---

# Weekly Review

Scan the week. Surface what matters. Plan what's next.

## Workflow

1. **Scan vault changes** — Find all files in `~/broomva-vault/` modified in the last 7 days:
   - New notes created
   - Existing notes modified (check git or file timestamps)
   - Group by folder/project

2. **Scan git activity** — Run across all repos under `~/broomva/`:
   - `git log --since="7 days ago" --oneline --stat`
   - Count commits per repo
   - Identify PRs merged, branches created

3. **Extract completed items** — Find tasks marked done this week:
   - `- [x]` items with recent modification dates
   - Completed items in project trackers

4. **Find open items** — Surface things that need attention:
   - Overdue tasks (`- [ ]` with past dates)
   - Stale PRs or branches
   - Notes tagged with urgency markers
   - Items promised in last week's review that aren't done

5. **Identify themes** — What patterns emerge from the week's activity:
   - What projects got the most attention?
   - Any new projects or ideas that emerged?
   - Any projects that went silent?

6. **Generate next week's priorities** — Based on:
   - Unfinished items from this week
   - Upcoming deadlines
   - Momentum (what's hot, what's stalled)

## Output Format

```markdown
## Weekly Review — [Week of YYYY-MM-DD]

### Week at a Glance
- **Commits**: [N] across [M] repos
- **Notes created**: [N]
- **Notes modified**: [N]
- **Tasks completed**: [N]
- **Tasks still open**: [N]

### What Got Done
- [Completed item] — [[Project]]
- [Completed item] — [[Project]]

### What's Still Open
**Overdue**
- [ ] [item] — due [date] — [[Project]]

**In Progress**
- [ ] [item] — [[Project]]

**Stalled** (no activity this week)
- [ ] [item] — last touched [date] — [[Project]]

### Project Activity
| Project | Commits | Notes | Status |
|---------|---------|-------|--------|
| [name] | N | N | Active / Quiet / New |

### Themes & Observations
- [What dominated the week]
- [Any surprising patterns]
- [Things to watch]

### Next Week's Priorities
1. [Priority] — why: [reason]
2. [Priority] — why: [reason]
3. [Priority] — why: [reason]

### Carry-Forward
- [ ] [Item from this week that must continue]
```

## Vault Integration

- Save to: `~/broomva-vault/reviews/weekly-review-[YYYY-MM-DD].md`
- Link back to project notes referenced
- If prior weekly reviews exist, reference the most recent one for continuity

## Behavior

- Be factual about what happened — don't editorialize
- Highlight things that slipped without judgment
- The "next week's priorities" should emerge from the data, not be invented
- If the vault is sparse, focus on git activity
- Keep the whole review scannable in under 3 minutes
