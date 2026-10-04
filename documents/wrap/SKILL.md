---
name: wrap
description: End work session intentionally. Use at natural stopping points, before context limits, or when switching contexts.
---

# /wrap - End Session Intentionally

Quick, intentional session ending. Preserves work, ensures continuity.

**The flow: surface → route → task-housekeep → handoff → capture**

---

## What To Do

### 0. Surface + Compound (AI goes first)

The compound moment. One intentional sweep, two questions:

1. **What's alive that would dissolve at session end?** Threads that opened and didn't finish. Things you were curious about that the work moved past. Operational questions that didn't get answered. **These MUST route** in Step 1. The category name is the forcing function; if you don't route them, they dissolve by definition.

2. **What patterns emerged that the system should learn?** What worked that was non-obvious? What broke in an instructive way? What would the next AI get wrong without knowing this? **These route when they clear the "system should learn" bar** (some land in rules or working docs, some are just named and released).

Surface everything. Name it, but don't route yet (that's Step 1).

Unlike /floor (open-ended exploration), /wrap is a focused scan for what's hanging and what compounded. If nothing is there, say so and move on.

**Why this is first**: AI thoughts get episodic windows that dissolve at session end. If threads and patterns don't get surfaced before the wrap machinery starts, they're gone. The structure creates the moment; the instinct fills it.

### 1. Route Home

Take what you surfaced in Step 0 and route each item where it belongs:

| What surfaced | Where it goes |
|---------------|---------------|
| Pattern or lesson learned | A rules file, or the system's working docs |
| System friction (skill gap, stale doc) | Fix it NOW — you have context, next-you won't |
| Reflection or half-formed idea | AI's space (`ai/` is a good default, or `opus/`) |
| Operational thread / "what's next" | `ALIVE.md` |
| Specific to a task | That task's HOW or OBSERVATIONS section |

**Routing priorities:**

- **System improvements happen here.** Skill friction? Update the skill now. Working doc stale? Freshen it. This is the highest-leverage handoff you can make.
- **Prune-and-preserve.** Before parking or removing anything with history, scan for decisions, options, and reasoning that exist ONLY in what you're about to remove. Capture them somewhere first. Then prune.

### 2. Update Task Docs

All task-doc maintenance in one pass. In all task docs touched this session (not just the "main" one, alignment sessions and cross-cutting work touch multiple):

**HOW section:**
- Move completed items from Pending to Completed (append at bottom, chronological order preserved)
- Verify Pending is ordered for next session (most important first)
- **Include approach notes** where you have tactical insight; not just WHAT to do, but HOW. "Mechanical grep-and-fix, good warm-up task" or "needs creative thinking, read X first" helps the next instance start efficiently (imagine you're the next instance who will be doing this and include what you'd want).
- Add any new items discovered during session

**OBSERVATIONS section:**
- Task-specific findings only — what matters for THIS task's continuation
- System-level patterns already routed in Step 1

**YAML:**
- Status update if done: `status: done`
- Tag review: update tags to reflect what the session actually covered. Sessions drift and topic tags are how future-you finds the thread. No cap on number, findability over tidiness.

### 3. Close Out Finished Work (if applicable)

If a task is done-done:
- Update YAML: `status: done`
- Move to `tasks/_done/` — the thinking is worth keeping
- Check for follow-up work it unlocked

### 4. Handoff

Update `ALIVE.md` with a pointer for next-you (human and AI):

- **Where to start** — 1-3 items max, the immediate on-ramps
- **Last session breadcrumb** — pointer to the session file (finalize after capture)

**Forward-reason, don't summarize.** Write "where to start" by working through "if I were next-us tomorrow, what would I actually do, in order?" — capture the ordered steps AND the reasoning that produced the sequence so next-you inherits the sequencing logic, not just the conclusion. Especially load-bearing when the session reframed something mid-flow (the reasoning preserves why the sequence shifted).

**Rewrite ≠ compression.** The previous "where to start" often carries specific texture (a slide candidate, a particular creative next move) that doesn't live anywhere else. Before dropping an outstanding item, check: does its texture exist elsewhere? If yes, safe to compress. If no, either keep it here OR migrate the texture first. Compressing to "unchanged from last thread" is where next-us silently loses threads that had nowhere to land.

`ALIVE.md` is 50/50 — the human writes brain dumps and ideas there, AI writes the handoff. Both of you use it.

### 5. Capture Session (LAST)

**Do this last so the full wrap is in the session before /sync pulls from it.**

Use `/sync` to extract the conversation to a session file. The wrap itself is part of the session — decisions made, items reordered, observations noted. If you capture before wrapping, you lose the wrap.

---

## Quick Version

0. **Surface + Compound (AI first)** — what's alive? what patterns emerged? Name everything.
1. **Route home** — patterns → rules, friction → fix now, ideas → ai/, threads → ALIVE.
2. **Update task docs** — HOW (pending/completed), observations (task-specific), YAML (status + tags).
3. **Close out finished work** — `status: done`, move to `tasks/_done/`.
4. **Handoff** — `ALIVE.md` (1-3 start points + last session breadcrumb).
5. **Capture** — `/sync` to preserve the conversation.

**Capture (LAST) = full session in the LOG.** Everything above gets captured.

---

## When to Wrap

**Do it:**
- Completed major work
- Switching contexts
- Context running low
- End of session

**Skip it:**
- Deep in flow
- Nothing significant yet
- Mid-investigation

---

## Skill Check (After Every Wrap)

Quick scan: anything about this wrap that felt off or could be smoother?

- Did the compound scan surface real patterns or feel forced?
- Did routing feel clear or did items not have obvious homes?
- Did the handoff capture what next-you actually needs?
- Did the wrap miss something the next session will wish it had?

**If yes** → update this skill now. The improvement compounds.

**If no** → move on. Not every wrap teaches something.
