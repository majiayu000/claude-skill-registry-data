---
name: session-opening
description: Start a session with context from previous work. Triggers on /open, 'what were we working on', 'where did we leave off', or session start. Pairs with /ground and /close. (user)
---

# /open

Orient to previous work, then act on what's next.

## Structure

```
Gather  → script + optional beads gate
Orient  → "here's where we left off"
Decide  → user picks direction
Act     → draw-down to TodoWrite
```

---

## 1. Gather

Run the context gathering script (from the session-management skill directory):

```bash
~/.claude/skills/session-management/scripts/open-context.sh
```

Script outputs: HANDOFF, GIT, BEADS (if present), UPDATE_NEWS context.

**Gate check:** If `GATE_REQUIRED=true` and beads skill is available:
```
Skill(beads)
```
Do not proceed until loaded. This ensures draw-down patterns are available.

---

## 2. Orient

Synthesize what matters from script output:

- **Lead with handoff** — Done, Next, any Gotchas
- **Surface commands** — if Commands section exists, offer to run them
- **Note scope mismatches** — if handoff "Next" doesn't match `bd ready`, flag it
- **Beads ready** — what's unblocked

Keep it brief. Orientation, not full briefing.

---

## 3. Decide

User picks direction:
- A specific bead from ready list
- Continue from handoff's "Next"
- Something else entirely

---

## 4. Act

**Draw-down is mandatory.** When user picks a bead:

1. `bd show <bead-id> --json` — read design and acceptance criteria
2. Create TodoWrite items from acceptance criteria
3. Show user: "Breaking this down into: [list]. Sound right?"
4. Mark bead in_progress: `bd update <id> --status in_progress`

**No TodoWrite items = No work.** This creates checkpoints where drift gets caught.

---

## Graceful Degradation

Not all features require all dependencies:

| Component | If missing... |
|-----------|---------------|
| Handoff archive | Skip handoff section |
| Beads/bd | Skip beads section, no gate required |
| Update news | Skip news section |

The core pattern (Gather → Orient → Decide → Act) works with just git status.

---

## Mirrors

| Phase | /open | /ground | /close |
|-------|-------|---------|--------|
| Gather | Handoff, beads, script | Todos, beads, drift | Todos, beads, git, drift |
| Orient | "Where we left off" | "What's drifted" | Reflect (AskUserQuestion) |
| Decide | User picks direction | Continue or adjust | Crystallize actions (STOP) |
| Act | Draw-down → TodoWrite | Update beads, reset | Execute, handoff, commit |
