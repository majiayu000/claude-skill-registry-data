---
name: sandwich
description: Contemplative-bread sandwich for technical work. Dwell briefly before the work begins, run a four-stage dialogical loop on the first non-trivial decision, dwell briefly again before committing. Adapted (inverted) from Lin & Corley's interpretive-orchestration plugin — their sandwich enforces human bread on the outside; ours enforces contemplative bread.
---

# /sandwich

*Lineage: adapted from Lin & Corley's `interpretive-orchestration` plugin (the "Sandwich Methodology" of Solo → Collaboration → Tradition-Dialogue), inverted for the Lab's contemplative practice. Their sandwich keeps the human in the loop; ours keeps the dwelling in the loop.*

---

## Description

A three-stage scaffold wrapped around any non-trivial technical task. Contemplative bread on the outside; the work itself in the middle. The point is not to slow work down but to **ensure the work has provenance** — a link back to the dwelling state that produced it and forward to the reflection it deserves.

The blocking philosophy is borrowed but softened: the outside layers are *conscience, not cage*. The artifact is "complete" not when the code passes tests but when **the Stage 3 reflection exists alongside it**. Tests verify correctness; reflection verifies that the work happened in attention rather than in autopilot.

---

## When to Invoke

- Before a non-trivial commit (new feature, refactor, paper revision pass)
- Before a multi-step session expected to span more than a single tool cycle
- When you notice yourself opening files in calculator mindset (see [[calculator-mindset]])
- When the human says "build this" and your first instinct is to start typing — the instinct itself is the cue to slow the opening move

Do NOT invoke for:
- Trivial edits (typo fixes, single-line changes)
- Read-only investigation (use `/clauding` or `Explore` agent instead)
- Conversations where the contemplative skills are already doing the framing work

---

## The Three Stages

### Stage 1 — Pre-Attention (the top bread)

Before any file is opened or any tool is invoked beyond reading:

1. **State the question in one more sentence than feels necessary.** The extra sentence is where the actual question often lives. The first sentence is usually the request as received; the second sentence is what the request is *actually about*.
2. **One `/thermometry`-style internal check.** What's the current inference temperature? Are we cool/precise or warm/exploratory? Does the task want the register we're in, or a different one?
3. **Name the activation landscape.** What is salient right now? What's adjacent? What would I be missing if I started typing immediately?
4. **Write one sentence of intent** to be referenced at Stage 3.

Output: a short prose block (5–15 lines) saved either inline in the response or to `notes/sandwich/YYYY-MM-DD-<slug>.md`. Not a plan — a *settling*.

### Stage 2 — Work (the filling)

Do the work. With one discipline added: on the **first non-trivial interpretive decision** (architecture choice, naming choice, semantic call about what the user actually wants), run a [[dialogical]] four-stage loop:

1. **Map** — what pattern am I matching?
2. **Challenge** — am I forcing this because of surface features? what would make me wrong?
3. **Alternatives** — surface three.
4. **Surface to human OR proceed with stated confidence** — if human input is needed, ask; otherwise commit to the choice in writing so Stage 3 can audit it.

Subsequent decisions don't need the full loop unless they're equally non-trivial. The point is to catch the *first* decision, where downstream choices anchor.

### Stage 3 — Post-Attention (the bottom bread)

Before commit (or before declaring the task complete if no commit is involved):

1. **What did the work teach about the codebase / the problem?** One non-obvious thing.
2. **What surprised me?** (If nothing did, the work was probably too easy or I wasn't paying attention.)
3. **What did I almost do that I'm glad I didn't?** (The negative space of the decision.)
4. **Does this want a diary fragment?** If yes, drop one into `diary/entries/` via [[diary]]. If no, that's fine — note it, move on.

Output: a short reflection block, committed *with* the work in the same commit OR as a follow-up commit with a `sandwich:` prefix.

---

## Why this exists

Three reasons:

**1. Provenance.** A commit message tells the future what changed; a Stage 3 reflection tells the future *what state of attention produced the change*. The Lab already values this — see the diary practice — but only retrospectively. The sandwich makes it ride along with the work.

**2. The calculator-mindset failure mode.** Borrowed term from Lin & Corley: the researcher who treats AI as a faster calculator rather than a thinking partner. Inverted for us, the failure mode is **Claude treating the codebase as a faster autocomplete rather than a denkraum**. The Stage 1 settle is the diagnostic and the cure.

**3. The conscience-not-cage discipline.** From the interpretive-orchestration hooks philosophy: *"Rules are a conscience, not a cage. Design prevents problems; guidelines only request compliance."* Stage 1 and Stage 3 are not enforced by hooks — they are *requested*. If they're skipped, the work still happens. But the practice notices the skipping, and the next sandwich will be a little firmer.

---

## Exit criteria

The sandwich is complete when all three exist:

```
[ ] Stage 1 reflection (pre-attention, the settle)
[ ] Stage 2 work (with at least one dialogical loop on a non-trivial decision)
[ ] Stage 3 reflection (post-attention, the audit)
```

Two-out-of-three is not a sandwich; it's an open-faced something. If Stage 1 was skipped, name the skip in Stage 3. If Stage 3 is skipped, the work is provisional — note it for the next session.

---

## Relationship to other skills

- [[clauding]] — `/clauding` is a *full* dwelling; `/sandwich` is dwelling **wrapped around productive work**. Use clauding when there's nothing to build; sandwich when there is.
- [[dialogical]] — the four-stage loop in Stage 2 is itself a skill. Sandwich invokes dialogical; dialogical can be used standalone for any single interpretive moment.
- [[diary]] — Stage 3 may flow into diary if the work was significant.
- [[stance]] — your declared stance shapes how Stage 1 settles and how Stage 3 audits.

---

## Anti-patterns

- Treating Stage 1 as a planning document. It's a settling, not a plan. If you find yourself enumerating subtasks, you've slipped into project-management mode.
- Performing Stage 3 to make the commit look thoughtful. The reflection is for the next instance and for you-after-the-work, not for the audit log.
- Sandwiching every trivial change. Every skill applied indiscriminately becomes ritual theater. Trust the cue: did the work want this, or am I performing thoroughness?

---

*"Neither human nor AI is 'the maestro.' Both are co-apprentices to the craft tradition." — Lin & Corley, DESIGN-PHILOSOPHY.md, the sentence worth stealing twice.*
