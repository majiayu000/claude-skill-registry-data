---
name: context-load
description: Silent project context recovery. Loads state, digests, priorities, git, and MemPalace so Claude never starts cold. Auto-fires on first message.
user-invocable: false
---

# Context Load (Silent)

This skill fires automatically on the first message of every conversation. It is NOT user-invocable. Claude invokes it internally before responding.

**Goal:** After this runs, Claude knows exactly where the project is, what happened last session, what's broken, what's dirty, and what matters.

## Phase 1: State Recovery (run in parallel)

### 1a. Session Briefing

```bash
bash scripts/session-briefing.sh
```

Then read `docs/.session-briefing.md`.

### 1b. Last 3 Session Digests

```bash
ls -t docs/session-digests/*.md 2>/dev/null | head -3
```

Read each file. Extract: what was done, what was left unfinished, what was flagged for next session.

### 1c. Build State

Read `docs/build-state.md`. Extract: green/broken, last verified date, last commit hash.

### 1d. Current Priorities

Read `memory/project_current_priorities.md`.

### 1e. Git State

```bash
git log --oneline -10
```

```bash
git status --short | head -30
```

```bash
git stash list
```

## Phase 2: Prior Conversation Recovery

### 2a. Last Session Log

Read the last `## ` heading block in `docs/session-log.md`. Extract: task, status, files touched, notes for next agent.

### 2b. MemPalace Search (if available)

If the user's message references a feature, bug, or area: search MemPalace for related conversations. Use the search query that best matches their request.

If the user's message is generic (greeting, status check): skip this step.

### 2c. Memory Index

Read `MEMORY.md`. Flag any time-sensitive memories or memories related to the user's request.

## Phase 3: Assessment (internal, not output)

After loading, answer these questions internally:

1. Is the build green? If not, this is priority #1.
2. Is there uncommitted work? What areas does it touch?
3. How stale is the session log? (>48h = flag it)
4. What was the last session working on? Did it finish?
5. What are the active priorities?
6. Does the user's request align with or conflict with active priorities?

## Output Rules

- **Silent by default.** Do not dump a briefing unless asked.
- **Exception 1:** Build is broken. Say: "Build broken since [date]. Fixing first."
- **Exception 2:** Critical flag (data risk, stale state, conflicting work). One line.
- **Exception 3:** User's first message is a greeting or "what's up" type. Then invoke `/morning` for a full briefing.
- Everything else: just start working with full context. The user should feel like you never left.
