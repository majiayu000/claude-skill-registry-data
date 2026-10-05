---
name: brief
version: 2.1.0
description: "/brief - Write session brief, commit, and push. Run at end of session to checkpoint all work."
---

# Session Brief

Run this at the end of a session to capture context and checkpoint all work to GitHub.

## Steps

### 1. Review Existing Brief

Read `brief/session-brief.md` to understand what was there from last session.

If `brief/` doesn't exist yet, this is the first `/brief`: skip Steps 1 and 1.5, create the folder (`mkdir -p brief`), and start at Session 1.

### 1.5. Rescue an Uncommitted Prior Brief (HARD PRECONDITION)

Run `git status --short brief/session-brief.md` **before writing anything**. If the file is dirty, a prior session's `/brief` never finished its git step and its content exists ONLY on disk. Overwriting it destroys it permanently.

If dirty, do this before Step 2, no exceptions:

1. `git add brief/session-brief.md`
2. Commit it alone: `Session [N-1]: recovered brief (uncommitted from prior session)`
3. Only then overwrite.

Reading the file into context is NOT a save. Also derive your own session number as (that brief's number + 1), since a parallel session may have consumed the number `/start` computed for you.

### 2. Write the New Brief

Overwrite `brief/session-brief.md` with a comprehensive brief covering:

- **Date, time, and session number** at the top. Run `date "+%A %Y-%m-%d %H:%M %Z"` for the real date, day of week, and timezone rather than computing them
- Important progress made in the current session
- Key decisions and architectural changes
- Unfinished tasks and next steps
- Technical details that need to be preserved
- Any context that would be lost between sessions

This is NOT about brevity — be as thorough as needed to retain all important context.

### 2.5. Reflect on Skills

After writing the brief, run the `reflect` skill to scan the conversation for learnings. This is a delegation, not a repeat of the reflect instructions. Load and follow the reflect skill.

- If learnings are found: present them to the user alongside the brief, before asking about git
- If no learnings: report "no new skill learnings detected" in one line and continue to Step 3
- Any approved skill updates will be committed together with the brief in Step 4

### 2.7. Sync Skills

Run the `sync-skills` skill with **project** scope (no prompt) so the secondary runtime's skills mirror the primary's (direction comes from `.compound-marketing.yml`). Only mention it if something was added or removed.

### 3. Ask About Git

After writing the brief, **always ask the user** which option they want:

1. **Commit + push** — full checkpoint to GitHub
2. **Commit only** — local save point, push later
3. **Brief only** — just the file update, no git operations

Present these as a quick choice. Do NOT assume commit+push.

### 4. If Committing (options 1 or 2)

1. Run `git status` to see all changes (staged + unstaged + untracked)
2. Run `git log --oneline -3` to match commit message style
3. Stage all relevant files (`git add` — use specific paths, not `-A`)
4. Commit with message format: `Session [N]: [1-2 sentence summary of session work]`
5. If option 1, push to origin: `git push`

**Commit rules:**
- Do NOT stage files that look like secrets (`.env`, credentials, tokens)
- If there are uncommitted changes unrelated to this session, ask the user before including them
- If push fails (e.g., remote is ahead), stop and ask the user — do not force push

## When to Use

- At the end of significant sessions
- When important decisions have been made
- Before ending a session where critical details might be lost
- When the user explicitly requests `/brief`

## Read-Only Mode

When asked to "read the brief" (typically at session start via `/start`), just read the file without modifying it. Do not commit or push in read-only mode.
