---
name: session-report
description: >
  Generate an Obsidian session report at the end of a coding session.
  Summarizes commits, tests, decisions, blockers, and next steps.
  Triggers on: end session, session report, wrap up, done for today.
---

## Session Report Generator

### Step 1: Gather Context
```bash
git diff --stat HEAD~10 2>/dev/null || git diff --stat
git log --oneline --since="4 hours ago" 2>/dev/null || git log --oneline -10
git branch --show-current
```

### Step 2: Generate Report
Create markdown with frontmatter (date, project, branch, tags) and sections:
- **Summary**: 2-3 sentences of what was accomplished
- **Work Done**: Commit-by-commit summary
- **Tests**: Count added/modified, pass/fail status
- **Decisions Made**: Any architectural choices (link ADRs)
- **Blockers / Open Questions**: Unresolved items
- **Next Steps**: Checklist for next session
- **References**: Ticket IDs, PR links, ADR links

### Step 3: Save
Save to: `~/Obsidian/Dev/Sessions/<YYYY-MM-DD>-<project>-session.md`
If Obsidian MCP is available, use it. Otherwise write directly.

### Step 4: Update Sprint
Update `docs/context/CURRENT_SPRINT.md` with current status.
