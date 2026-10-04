---
name: session-bootstrap
description: Start-of-session routine — load context, check state, suggest next task. Use at the beginning of a fresh session or after a context reset.
triggers:
  - session start
  - fresh session
  - what should I work on
  - what's next
---

# Session Bootstrap

Quick context load to get productive fast.

## Steps

1. **Check git state**
   ```bash
   git status --short
   git log --oneline -5
   ```

2. **Load backlog**
   - Read `.claude/backlog/` for latest dated file
   - Identify top-priority items (high > medium > low)

3. **Check for in-progress work**
   - Look for uncommitted changes
   - Check if any PRs are open for this repo

4. **Suggest next action**
   - If there are uncommitted changes: suggest committing or continuing
   - If backlog has high-priority items: suggest the top one
   - If clean state: ask what to work on

## Output Format

```
Session Start
Branch: <current>
Recent: <last 3 commits>
Backlog top: <item> (priority)
Suggested: <action>
```
