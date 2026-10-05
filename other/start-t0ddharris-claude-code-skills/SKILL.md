---
name: start
version: 1.2.0
description: "Start a new session. Trigger with /start at the beginning of a conversation. Reads the session brief, checks git status, summarizes where things stand, and increments the session number."
---

# Session Start

Run this at the beginning of every new session. It gives you and the user a shared understanding of where things left off and what's in play.

## Steps

### 1. Read the Session Brief

Read `brief/session-brief.md` in full. This is the primary source for what happened last session, what decisions were made, and what's still open.

### 2. Check Git Status

Run `git status` and `git log --oneline -5` to see:
- Any uncommitted changes from the last session
- The most recent commits for context

### 2.5. Sync Skills to .agents/ (opt-in projects only)

If the project has an `.agents/` directory, run the project-level sync from the `sync-skills` skill (hardlink `.claude/skills/` → `.agents/skills/`). Do not prompt for scope — project only. Only mention it if something was added or removed.

If there is no `.agents/` directory, skip silently — never create one. To opt a project in, run `/sync-skills` once manually and add `.agents/` to its `.gitignore`.

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
- Do NOT push the user toward the next topic while they're still working through the current one — wait for them to signal they're ready to move on
- If the brief is missing or empty, say so and ask the user what they'd like to work on
- If there are uncommitted changes, mention them but don't commit — the user decides

## Learnings

<!-- Updated by /reflect. Promote stable patterns to the main skill body. -->

- **[MEDIUM]** If the brief is missing, orient from project continuity artifacts (RESUME blocks, recent commits) instead, say the brief is missing, and offer to backfill it. *(Session 2, 2026-06-10)*
- **[MEDIUM]** At session start, verify the live state (PR merged? Linear issue Done?) of the top 1–2 carryover items rather than trusting the brief — the brief snapshots a moment that may be stale by next session. *(Session 56, 2026-06-11)*
- **[MEDIUM]** If any PR is open at session start, run `gh pr checks` on it — a red CI run reframes session priorities before any planned work begins. *(Session 66, 2026-07-03)*
