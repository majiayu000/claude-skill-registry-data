---
name: work-item-handler
description: |
  Fetch and manage work items from issue trackers. Use this skill when:
  - User references an issue number (#42, PROJ-123)
  - User asks about requirements or acceptance criteria
  - User needs to understand current task scope
---

# Work Item Handler

Integrate with issue trackers (GitHub, JIRA, Azure DevOps) for context-aware assistance.

## When to Use This Skill

Proactively invoke when user:
- Mentions an issue number
- Asks about requirements or "what needs to be done"
- Needs to fetch/refresh issue details
- Is unclear about task scope

## Context Files (Auto-Injected)

- **rules/git.md**: Commit and PR format rules (SINGLE SOURCE OF TRUTH)
- **context/git.md**: Detailed commit/PR examples
- **rules/work-items.md**: Work item lifecycle
- **context/work-items.md**: Multi-platform patterns and examples

Read these files for complete guidance. This skill provides quick reference only.

## Quick Reference

### Fetch Issue (GitHub)
```bash
gh issue view <number> --json number,title,body,state,labels
```

### Use /onus:fetch Command
For full fetch with caching:
```
/onus:fetch 42
```

### Caching
- Location: `~/.claude/onus/work-item-cache.json`
- Expires: 1 hour
- Refresh: `/onus:fetch <number>`

## Key Rules

1. **Don't define commit/PR formats here** — that's rules/git.md's job
2. **Don't guess issue numbers** — verify with user or parse from branch
3. **Track acceptance criteria** — warn before PR if unaddressed

## What This Skill Does NOT Do

- Define commit message format (see rules/git.md, context/git.md)
- Define PR format (see rules/git.md, context/git.md)
- Define work item lifecycle (see rules/work-items.md)
- Provide detailed fetch examples (see context/work-items.md, commands/fetch.md)
