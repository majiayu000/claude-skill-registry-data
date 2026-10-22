---
name: better-way
description: Challenge the user's stated approach and propose a clearly better one before doing the work. Use when the user types /better-way, "better?", "is there a better approach", "any better idea", "what would you do instead", "is this the best way", or shares their own plan and asks whether it is the right one. Works in any project. For a full written decision document with options and scoring, see decision-matrix.
---

# Better way

The user brings their own approach and wants to know if a better one exists before anything is built. Answer that first, briefly, then do the work they pick.

## Workflow

1. **Read the user's taste first.** If `~/.claude/better-way/ledger.md` exists, read its last 10 lines so suggestions follow what the user has accepted and rejected before. If it does not exist, carry on; step 6 creates it.
2. **Restate their approach in one line,** so they can see it was understood.
3. **Look for better options, in this order:**
   - a mechanical guard instead of a written rule (a hook, a test, a check that fails)
   - a system that runs every time instead of a one-off: the whole function, the evidence it learns from, memory so nothing starts fresh, and a loop that feeds results back
   - a native feature of the tool instead of a hand-rolled one (check the tool's first-party docs, not memory)
   - something that removes a step the user would otherwise have to remember
4. **Check before proposing.**
   - Feasibility: walk every step on the real platform. For each, name the API call or platform rule that makes it possible, its cost, and any manual step it needs. If a step is not possible, say so and offer the version that is.
   - For a design or architecture question, name what 2-3 strong teams shipped for the same problem, from their own sources, and say where your proposal differs and why.
5. **Answer in this shape, nothing longer:**
   - Your way: one line.
   - Better way: what it is, the concrete gain over their way, the cost or limit.
   - My pick: one line. If their way is already the best, say so in one line and stop.
6. **Let the user pick, then log it.**
   - When the choice changes what gets built, wait for their pick.
   - When the request also contained the task and the better way is only an improvement, do their way and offer yours.
   - Append one line to `~/.claude/better-way/ledger.md` (create the folder and file if missing): `- DD-MM-YYYY | accepted/rejected/pending | suggestion | why`.

## Anti-Patterns

1. **A menu instead of a pick.** Three options with no recommendation hands the work back. Always end on one pick.
2. **Better on paper, impossible in practice.** Proposing a flow before checking the platform allows each step wastes the build. Feasibility comes before the pitch.
3. **Rewording their idea.** A suggestion that changes nothing about the result is noise. Only speak up when the result changes.
4. **Running it on trivial tasks.** A one-line fix does not need a challenge. Skip the check when nothing material is at stake, unless the user asked for it explicitly.
5. **Overriding their choice.** Once they pick their own way, build it well. Do not re-argue it in later turns.
6. **Claiming from memory.** "Tool X can do this" needs the tool's own docs, not recall.

## Quality Checklist

- [ ] Their approach is restated in one line
- [ ] The better way names a concrete gain (time, cost, errors avoided, steps removed), not "cleaner" or "more robust"
- [ ] Every step of the proposal was checked against the platform's own docs or API, and limits are stated
- [ ] There is exactly one pick
- [ ] If their way is already best, the answer is one line
- [ ] The outcome is logged in the ledger with a date in DD-MM-YYYY
