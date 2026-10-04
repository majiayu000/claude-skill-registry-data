---
name: napkin
description: Build throwaway code that answers exactly one design question — a tiny terminal app to feel out logic/state models, or several radically different UI variants switchable on one route. Use when the user wants to "prototype", "mock up", "sketch", "try a few versions", "see what it'd look like", "feel out this state machine", or is stuck choosing between designs they can only judge by seeing or driving them. Also used by the whiteboard skill for napkin-type tickets.
---

# Napkin

A napkin is **throwaway code that answers one question**. Not a v1, not a head start — a question with a run command. The question decides everything, so it comes first.

## The gate: write the question down

Before any code, one sentence at the top of the entry file or README:

> QUESTION: Does a three-state model (draft → active → archived) survive the "un-archive with pending edits" case?

Can't phrase a single question? You're not sketching — you're building without a plan. Stop and run a hot-seat pass to find the question. Napkins that answer the wrong question are pure waste, and "wrong question" only becomes visible after the code exists — the written line is what makes it visible.

## Pick a branch

- **"Does this logic / state model / data shape hold up?"** → [references/logic.md](references/logic.md). Tiny terminal app; the user drives the state model through cases too slippery to reason about on paper.
- **"What should this look like on screen?"** → [references/ui.md](references/ui.md). Several radically different variants on one route, switchable via URL param + floating bar.

Wrong branch = wasted napkin. Ambiguous and the user's not around? Default by neighborhood — near a backend module → logic; near a page or component → UI — and state the assumption next to the QUESTION line.

## House rules (both branches)

1. **Visibly throwaway.** Lives near the code it's sketching for, but named so nobody mistakes it for production — `napkin` or `prototype` in the path.
2. **One command to run.** Wired into the project's existing task runner. Nobody remembers a path.
3. **No persistence.** State lives in memory — persistence is usually the thing being *tested*, not a thing to lean on. Question explicitly about a DB? Scratch store, named "NAPKIN — wipe me".
4. **Zero polish.** No tests, no error handling past runnability, no abstractions, no "what if we later". One question, then it dies.
5. **Show the state.** Full relevant state after every action / on every variant switch. The payoff is the user saying "wait, that shouldn't be possible" — they can only say it about state they can see.
6. **Timebox.** A napkin that costs more than the real thing is a failed napkin. Ballooning = question too big. Split it, sketch the sharpest piece.

## Done = captured, then destroyed

The **answer** is the only thing that survives. Capture it next to the question, somewhere that outlives the code (commit message, ADR via connotation-cop, the whiteboard ticket that spawned it, or NOTES.md):

```md
QUESTION: <what was tested>
ANSWER: <the verdict>
EVIDENCE: <the case that decided it — "un-archive with pending edits forced a fourth state">
```

Then delete the napkin, or absorb the validated piece into real code — **rewritten properly**; napkin code was written under napkin rules and doesn't get promoted as-is. A napkin rotting in the repo confuses every future reader. A deleted napkin with no captured answer is worse: it looked like work and taught nothing durable.

User not around for the verdict? Leave the block with ANSWER blank — whoever returns fills it in before cleanup.
