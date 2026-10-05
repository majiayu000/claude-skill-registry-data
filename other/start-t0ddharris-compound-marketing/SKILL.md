---
name: start
version: 1.1.0
description: "Start a new session. Trigger with /start at the beginning of a conversation. Reads the session brief, checks git status, summarizes where things stand, and increments the session number."
---

# Session Start

Run this at the beginning of every new session. It gives you and the user a shared understanding of where things left off and what's in play.

## Steps

### 1. Read the Session Brief

Read `brief/session-brief.md` in full. This is the primary source for what happened last session, what decisions were made, and what's still open. In a git worktree, read it from main (`git show main:brief/session-brief.md`); the worktree's copy may be sessions stale.

### 2. Check Git Status

Run `git status` and `git log --oneline -5` to see:
- Any uncommitted changes from the last session
- The most recent commits for context

If `brief/session-brief.md` itself shows as modified, the previous `/brief` never committed. Flag it so it gets preserved as its own commit before the next `/brief` overwrites it.

### 2.5. Sync Skills

Run the `sync-skills` skill with **project** scope (no prompt) so the secondary runtime's skills mirror the primary's (direction comes from `.compound-marketing.yml`). Only mention it if something was added or removed.

### 2.7. Verify Carryover State

The brief is a snapshot. Before listing open items, check the live state of the top 1–2 (PR merged? issue closed?). If a PR is open, run `gh pr checks` on it; a red CI run reframes the session's priorities.

### 3. Check the Date

Note the current date and compare it to the session brief date. If significant time has passed (more than a few days), flag it — some carryover items may be stale or already handled.

### 4. Deliver the Session Summary

Output a concise summary for the user with these sections:

```
## Session [N+1] — [Current Date]

### Last Session Recap
[2-3 sentence summary of what happened]

### Open Items
[Bulleted list of carryover tasks, prioritized by urgency/relevance]

### Uncommitted Changes
[List any uncommitted files, or "Clean working tree" if none]

### Ready when you are.
```

Keep it tight. The user has already read the brief if they want detail — this is the quick orientation.

### 5. Increment the Session Number

Note the new session number based on the brief's session number. When the user runs `/brief` at the end of this session, use the incremented number.

## Rules

- Do NOT modify any files during /start — this is read-only, except the skills sync (step 2.5)
- Do NOT start working on carryover items automatically — wait for the user to direct
- Do NOT push the user toward the next topic while they're still working through the current one
- If the brief is missing or empty, say so, orient from recent commits instead, and ask the user what they'd like to work on
- If there are uncommitted changes, mention them but don't commit — the user decides
