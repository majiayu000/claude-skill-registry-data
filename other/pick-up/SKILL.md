---
name: pick-up
description: Resume work on a specific topic from a previous session. Searches session digests, git history, build queue, and MemPalace to reconstruct where you left off. Use when user says /pick-up [topic], "where did we leave off with X", "continue the Y work", "resume Z", or starts a session mentioning a specific past project.
---

# PICK-UP (Resume Specific Work Thread)

## Purpose

When the user wants to continue a specific piece of work from a previous session, quickly reconstruct the full context: what was done, what's left, what's blocking, and what to do next.

## Procedure

### Phase 1: Identify Topic

Parse the user's request for the topic keyword(s). Examples:

- "/pick-up lifecycle" -> lifecycle intelligence work
- "/pick-up ticketing" -> ticketed events feature
- "/pick-up PIE" -> pricing intelligence engine
- "/pick-up wiring" -> orphan connection passes

### Phase 2: Gather Context (parallel)

Search ALL of these sources for the topic:

1. **Git log:** `git log --oneline --all --grep="[topic]" -20`
2. **Build queue:** grep `docs/UNIFIED-BUILD-QUEUE.md` for topic
3. **Session digests:** grep `docs/session-digests/` for topic
4. **Specs:** find matching specs in `docs/specs/`
5. **Memory:** check MemPalace or memory files for topic context
6. **Session log:** grep `docs/session-log.md` for topic
7. **Build state:** check `docs/build-state.md` for related status

### Phase 3: Reconstruct Timeline

Build a timeline:

```
## [Topic] - Work Thread

### Last Activity
- Date: [when]
- What was done: [summary]
- Commit: [hash]

### Current State
- Build queue status: [PARTIAL/SPEC-READY/etc]
- Files touched: [key files]
- Tests: [passing/failing/none]
- Migrations: [applied/pending/none]

### What's Left
1. [next step]
2. [next step]
3. [next step]

### Blockers (if any)
- [blocker]
```

### Phase 4: Recommend Next Action

Based on state:

- If PARTIAL: "Ready for /sweep verification"
- If code exists but untested: "Needs test coverage"
- If spec exists but unbuilt: "Ready for /dispatch"
- If blocked: "Blocked on [X], here's how to unblock"
- If done: "This work is complete. Mark DONE?"

## Constraints

- Never guess or hallucinate past context. Only report what's in git/docs/memory.
- If topic not found: "No prior work found for '[topic]'. Did you mean [suggestions]?"
- Present findings, then ask "Pick up from here?" before building anything
- This is a RESEARCH skill, not a BUILD skill. Present context, let user decide next step.
