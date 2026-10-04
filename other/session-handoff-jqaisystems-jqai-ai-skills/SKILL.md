---
name: session-handoff
description: Write a start-here handoff document at the end of a work session capturing state, decisions, next steps, and gotchas, so the next session (or the next person) resumes in minutes instead of re-deriving everything. Use when the user says "wrap up", "handoff", "end of session", "write a handoff note", or "where did we leave off" at the start of a new session.
---

# Session Handoff

Context dies between sessions. The next session re-reads files, re-discovers decisions, and re-hits the same trap that cost an hour last time. This skill freezes the session's working state into one document built to be read cold.

## Step 1: Mine the session

Extract from the current conversation, not from memory of what should have happened:

- **What was accomplished**: only things actually finished and verified. Half-done work is listed as half-done.
- **Decisions made and why**: especially decisions that reversed an earlier approach. The "why" is the part the next session cannot reconstruct.
- **What is in progress**: exact state, which file, which step.
- **Next steps**: concrete and ordered, with the first one precise enough to start typing immediately.
- **Gotchas**: everything that failed and how it was fixed, environment quirks, commands that need specific flags, things that look broken but are fine.
- **Key paths and commands**: the files that matter and the exact commands to run (build, test, deploy, resume).

## Step 2: Write the handoff

Default target: `START_HERE.md` in the project root (or append a dated section to an existing one, newest at the top). Format:

```markdown
# Start Here: <date>

## TL;DR
Two sentences: where the project is, and the single next action.

## Done this session
## In progress
Exact state, file, and step for each item.

## Next steps (in order)
1. The first one must be executable immediately, with the exact command or file.

## Decisions and why
## Gotchas
What burned time this session, so it does not burn time again.

## Key paths and commands
```

## Step 3: Verify readability cold

Reread the document as someone with zero context: no session shorthand, no "the fix we discussed", no codenames invented mid-conversation. Every reference names its file. If a next step depends on a decision, the decision is in the document too.

## On resume

When a new session starts with "where did we leave off": read `START_HERE.md`, confirm the state still matches reality (files may have changed since), and start on next step 1. Flag divergence instead of following a stale plan.

## Rules

- Facts only. If tests were not run, the handoff says so.
- Never include secrets, tokens, or credentials, even ones seen during the session.
- No em dashes in any output.

## Output

A `START_HERE.md` (or dated section) that gets the next session productive in minutes.
