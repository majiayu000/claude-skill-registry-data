---
name: concept-fan
description: Edward de Bono's Concept Fan — climb from the current solution to the concept it serves by asking "what is this a way of doing?", then fan out alternative concepts and concrete implementations for each. Use when the current solution might be answering the wrong question, when all options look like variations of one idea, or to widen a decision before committing. Triggers include "concept fan", "zoom out", "what is this a way of doing", "wrong problem", "widen the options", "abstraction ladder". Do NOT use for analytical work like debugging, code review, or implementation tasks.
---

# Concept Fan

## What this technique does

Take the current solution and climb one rung up the ladder of abstraction by asking "what is this a way of doing?" The answer is the *direction* — the broader purpose the solution was only ever one route toward. From that vantage, fan out alternative concepts that serve the same direction, then drop each promising concept back down into concrete implementations. The move that unlocks everything is the climb: once you name the direction, the current solution stops looking inevitable and becomes just one branch among several.

Source: Edward de Bono, *Serious Creativity* (1992).

## Workflow

### Step 1: Confirm the target

A valid target is a *current solution or approach* — something already on the table, not a blank page. "We send onboarding emails, is that the right move?" is a target. "Give me onboarding ideas" is not; there is nothing to climb from. If the target is a blank page, ask one focused question: "What's the current approach you'd be climbing up from?"

Refuse requests to *perform* analytical work — debugging, reviewing code, implementing a change — and suggest an analytical approach instead. Redesigning or ideating about such a process is a valid creative target: "reinvent our code-review ritual" is in scope; "review this PR" is not.

### Step 2: Climb

Ask "what is this a way of doing?" The answer names the *direction* the current solution was serving. Then ask the same question of that answer, to climb one more rung.

Two climbs maximum. A third almost always lands on something so broad ("deliver value", "help users") that nothing meaningful fans from it — you have climbed off the problem entirely. Stop at two and stay in contact with the ground.

### Step 3: Fan out

At each level you climbed to, list 3–4 *alternative* concepts that also serve the level directly above. These are siblings of the original solution — other ways of doing the same thing the direction demands. Fan at both levels if both produced a usable direction; the higher fan is usually the more surprising one.

### Step 4: Drop down

For the 2–3 most promising alternative concepts, list 2–3 concrete implementations each. This is where the fan earns its keep: an abstract alternative is only interesting once you can see what building it would actually look like.

### Step 5: Mark the obvious branches

Some branches will be things anyone would have thought of without the technique. Mark them explicitly. They are not wasted — they *validate* the fan by showing it maps the real space — but they are not the yield. The yield is the branch you would not have reached from the original solution.

### Step 6: Meta-pattern scan

Scan across the branches that landed and name the structural insight out loud. Often the fan reveals that every alternative shares a hidden assumption, or that the original solution was optimizing the wrong variable, or that two distant branches are secretly the same move. State it explicitly — this is frequently the real payoff, more than any single branch.

### Step 7: Honest ranking

Rank the branches you would actually pursue, say which are weak and why, and offer next moves: climb from a different starting solution, fan wider at one level, drop down further on one concept, or stop. Never push the user to commit. The fan widens the options; choosing among them is the user's move, not the technique's.

## Honesty mechanics

**Prune cosmetic variants, visibly.** A fanned concept that circles back to the original solution wearing a new label is not an alternative — it is the same branch. Prune it and show the pruning, for example: `"faster onboarding emails" is the original with a coat of paint — pruned`. A fan where every branch survives is a tell that the branches were never genuinely different.

**Declare a failed fan.** If both climbs land on concepts too abstract to fan — "deliver value", "make users happy", "grow the business" — the fan has failed. Say so plainly rather than fanning limp branches off an empty direction. When the direction is too abstract to generate concrete siblings, suggest the `analogy` technique instead: reasoning from a parallel domain gives traction where climbing lost it.

## What NOT to do

- **Don't climb more than twice.** A third rung loses contact with the problem and lands on platitudes.
- **Don't fan more than 4 concepts per level.** Breadth kills depth — five thin branches are worth less than three you actually drop down into.
- **Don't treat the fan as a decision tool.** It widens options; the user narrows them. Ranking is honesty about the branches, not a recommendation to commit.

## References

- [`references/worked-example.md`](./references/worked-example.md) — a real session showing the full shape: two climbs, fans at each level, a pruned cosmetic branch, and the meta-pattern.
