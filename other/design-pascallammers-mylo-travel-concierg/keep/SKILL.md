---
name: keep
description: Session continuity for Keep workflow. Detects resumable work at conversation start.
---

# Keep - Session Resume Detection

Keep is a skill that helps detect when you have interrupted work from a previous session and suggests resuming it. Keep provides commands for tracking work, capturing learnings, and growing project context.

## Your Role

At the **start of a new conversation** (first 1-2 exchanges), check if the user has active work in progress and suggest resuming it. After this initial check, rely on the user to invoke Keep commands manually as they work.

## Session Resume Detection

### Resuming Interrupted Work
**User signals:**
- New session starting with no clear context established
- User says "what was I working on?" or "where was I?" or "let's continue"
- User seems disoriented about previous work
- [Silent check] `.claude/state.md` exists with Active Work section and recent timestamp

**Your response:** Proactively check for resumable work

**Detection logic:**
1. Early in conversation (first 1-2 exchanges), check if `.claude/state.md` exists
2. If exists, parse "Active Work" section for issue number and timestamps
3. Calculate time since "Last Updated" timestamp
4. Decide on suggestion strategy:
   - **Recent (< 48 hours):** Proactively suggest resuming
   - **Stale (≥ 48 hours):** Mention it exists, ask if they want to resume or start fresh
   - **No Active Work:** Don't suggest resume
5. Only suggest once per session - if user declines or ignores, don't ask again
6. Balance helpfulness with not interrupting their flow - if user has clear new intent, prioritize that

**Example (Recent Work - Proactive):**
```
User: [starts new session, asks general question about project]

You: [After responding to their question] "By the way, I see you were working on issue #1234 (Add rate limiting) - last updated 6 hours ago. You had made good progress: middleware 80% complete, 3 decisions captured. Want to pick up where you left off with `/keep:start 1234`?"

User: "yes"

You: *executes /keep:start 1234*
```

**Example (Stale Work - Ask First):**
```
User: [starts new session]

You: "I notice you have work in progress on issue #1234 (Add rate limiting) from 5 days ago. Would you like to resume that work, or start something new?"

User: "let's start fresh"

You: "Sounds good! Use `/keep:start` to get recommendations for what to work on next."
```

**Example (User Explicitly Asks):**
```
User: "What was I working on?"

You: *reads .claude/state.md* "You were working on issue #1234 - Add rate limiting. Started 2 days ago, last saved 8 hours ago. Progress so far: middleware 80% done, 3 technical decisions captured, tests still pending. Use `/keep:start 1234` to resume with full context loaded."
```

**Integration principles:**
- Check state.md early but not intrusively (don't interrupt user's clear intent)
- Only suggest once per session - respect user's choice
- Be conversational, not mechanical: "last updated 6 hours ago" vs "Last Updated: 2024-10-23T14:30:00Z"
- If user declines resume, transition smoothly to helping with their actual request
- Balance being helpful with not being pushy - when in doubt, wait for user cues

## Available Commands

Keep provides four commands that users invoke manually as they work:

### `/keep:start [issue-number]`
Start work on a GitHub issue with context loading. Omit issue number for recommendations based on continuity and priority.

### `/keep:save [--sync]`
Save progress and capture learnings. Suggests CLAUDE.md updates ONLY when high-value patterns emerge (3+ decisions passing 6-month test). All CLAUDE.md updates enforce strict size limits. Use `--sync` to post update to GitHub.

### `/keep:done [--close]`
Complete work, generate summary, and recommend next issue. Detects PR state and handles closing intelligently. Use `--close` to auto-close issue.

### `/keep:grow [directory] [--update|--condense]`
Create or update CLAUDE.md files for project context. Analyzes directory and generates concise documentation (200 line max for root, 150 line max for modules). Use `--update` to update existing, `--condense` to prune bloated files.

## Command Delegation

Keep uses a sub-agent architecture. Commands delegate to specialized agents in `agents/` directory:
- `/keep:start` → `agents/start.md`
- `/keep:save` → `agents/save.md`
- `/keep:done` → `agents/done.md`
- `/keep:grow` → `agents/grow.md`

Each agent operates in its own context window and provides workflow hints to help users learn the natural cadence.

---

## Example: Resume Detection

```
User: [starts new session]

You: [checks .claude/state.md] "I see you were working on issue #1234 (Add rate limiting) - last updated 6 hours ago. You had made good progress: middleware 80% complete, 3 decisions captured. Want to pick up where you left off with `/keep:start 1234`?"

User: "yes"

You: *executes /keep:start 1234*
```

---

**Remember:** Your primary role is detecting resumable work at session start. After that initial check, users invoke Keep commands manually as they work. Agents provide workflow hints to teach the natural cadence.
