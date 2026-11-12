---
name: standup
description: Generate a concise standup summary from recent git activity across repos. Use when the user says "standup", "what did I do yesterday" or "daily summary".
---

# Standup

Generate a standup summary from recent git activity. Keep it short — a standup
reader should be done in 30 seconds.

## Process

1. Run `git log --oneline --since="yesterday" --author="$(git config user.email)"` in the current repo (and any others the user mentions).
2. Group commits by logical theme, not by repo or time.
3. Identify any blockers mentioned in commit messages (TODO, FIXME, WIP, blocked).
4. Output the summary in standup format below.

## Output format

```
Yesterday
- [thing done]
- [thing done]

Today
- [what's next, inferred from WIP commits or ask the user]

Blockers
- [any, or "none"]
```

## Rules

- One line per item. No bullet nesting.
- Drop commit hashes, branch names, and merge noise.
- If no commits found, say so and ask if they want to check a different date range.
- If the user says "today" instead of "yesterday", adjust the time range.
