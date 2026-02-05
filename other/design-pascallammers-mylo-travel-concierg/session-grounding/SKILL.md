---
name: session-grounding
description: Mid-session checkpoint when things feel squiffy. Anchor to what matters, reset for the second half. Triggers on /ground, 'let's take stock', 'where are we', or when drift is sensed. Pairs with /open and /close. (user)
---

# /ground

Halftime. Context partially spent, insights accumulated, drift may have crept in.

## Structure

```
Gather  → todos, beads, drift detection
Orient  → "here's what we've done vs what we said"
Decide  → continue, adjust, or pivot
Act     → update beads notes, reset todos
```

---

## Pre-flight: Return Home (MANDATORY)

You may have `cd`'d during work. Your system prompt contains `Working directory: /path/...` in the `<env>` block — this is immutable, where the session actually started.

1. Extract that exact path from your system prompt
2. Run: `~/.claude/skills/session-management/scripts/check-home.sh "/that/path"`
3. If `CD_REQUIRED=true`, run `cd <HOME_DIR>` immediately

**Do not skip. Do not trust pwd. Do not reason about whether you moved back. The script is authoritative.**

---

## 1. Gather

Check current state:

- **TodoWrite** — what's done, what's in_progress, what's stale?
- **Beads** — `bd list --status in_progress` — still accurate?
- **Drift** — compare to /open (or previous /ground) orientation:
  - What did we say we'd do?
  - What did we actually do?
  - Any side quests that became main quests?

No script needed — this is conversational review.

---

## 2. Orient

Articulate the gap:

> "We started with [X from /open]. We've done [Y]. We drifted into [Z] because [reason]."

Be honest about drift. Side quests are fine — just name them.

Surface what's accumulated:
- Insights worth capturing
- Questions that emerged
- Decisions that got made implicitly

---

## 3. Decide

Three options:

1. **Continue** — we're on track, keep going
2. **Adjust** — update TodoWrite to reflect actual direction
3. **Pivot** — this side quest is now the main quest; update beads accordingly

User decides. If they're unsure, help them articulate what feels off.

---

## 4. Act

Based on decision:

**If continuing:**
- Update beads notes with progress checkpoint
- Trim stale TodoWrite items

**If adjusting:**
- Rewrite TodoWrite to match actual work
- Update beads notes with what changed and why

**If pivoting:**
- Create/update beads for new direction
- Note the original work as paused (not abandoned)
- Fresh draw-down for new focus

**Always:** Write beads notes as if context might vanish. This is your crash recovery checkpoint.

---

## When to /ground

- Things feel "squiffy" — can't articulate why, but momentum is off
- Natural pause point — finished a chunk, about to start another
- Context is ~50% used — halftime
- User says "wait, where are we?"

Don't overuse. If momentum is good, keep going.

---

## Mirrors

| Phase | /open | /ground | /close |
|-------|-------|---------|--------|
| Gather | Handoff, beads, script | Todos, beads, drift | Todos, beads, git, drift |
| Orient | "Where we left off" | "What's drifted" | Reflect (AskUserQuestion) |
| Decide | User picks direction | Continue or adjust | Crystallize actions (STOP) |
| Act | Draw-down → TodoWrite | Update beads, reset | Execute, handoff, commit |
