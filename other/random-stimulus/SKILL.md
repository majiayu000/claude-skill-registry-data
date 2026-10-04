---
name: random-stimulus
description: Edward de Bono's Random Stimulus technique — force-fit a random unrelated object, place, or phenomenon onto a creative target to break familiar association patterns. Use for product ideation, feature naming, brand direction, copywriting, architecture and design choices when ideas from outside the problem space would help. Triggers include "random stimulus", "random word", "force-fit", "de Bono", "inject a random object", "stare out the window", "see the tree and squeeze an idea". Do NOT use for analytical work like debugging, code review, or implementation tasks.
---

# Random Stimulus

## What this technique does

Pick a random thing from outside the problem space — a tree, a glacier, a kettle. List its properties. Force a connection to the target. See what falls out.

The first stimuli you draw are usually trash. The third or fourth is where real ideas appear — which is why you draw a batch and not a single object. The technique works because staying inside the problem space routes you through familiar associations; an external stimulus breaks the routing and forces a fresh trajectory through the same target. The stimulus has a *structural property* — cyclical, layered, swarming, ephemeral, branching — that the target could have but doesn't yet. That mismatch is where new designs hide.

Source: Edward de Bono, *Lateral Thinking: Creativity Step by Step* (1970), specifically the Random Word / Random Object method.

## Workflow

### Step 1: Confirm the target

A valid target is a concrete creative problem: names for a feature, ideas for a product, a novel onboarding flow, how to position a brand. If the target is unclear, ask one focused question — "What's the creative problem, and are there hard constraints?" Default batch size is 8–12 stimuli.

Refuse requests to *perform* analytical work — debugging, reviewing code, implementing a change — and suggest an analytical approach instead. Redesigning or ideating about such a process is a valid creative target: "reinvent our code-review ritual" is in scope; "review this PR" is not.

### Step 2: Pull stimuli

Draw 8–12 stimuli from [`references/stimulus-pools.md`](references/stimulus-pools.md). Three minimums, all checkable against the batch you drew — Step 3 requires you to label each stimulus with its pool, which is what lets a reader check them:

- **At least five distinct categories.** Not "mixed" as a feeling — count them.
- **At least two concrete physical objects and at least one abstraction.** Judge this per stimulus, not per pool: `hourglass` and `circadian rhythm` both live in Time & Cycles, but one is an object you could hold and the other is a rhythm you cannot. Mark each stimulus `[concrete]` or `[abstract]` beside its pool label so the count is visible. Pure-abstract batches feel intellectualized; pure-concrete batches feel mundane.
- **No two stimuli from the same category adjacent** in the batch order.

If the user offers a triggering metaphor ("look out the window", "what's in my kitchen"), bias toward that pool but always include 2–3 unrelated stimuli to break the cluster. A fully on-theme batch defeats the purpose of randomness.

Track which stimuli have been used this session. On a second batch, draw fresh ones.

### Step 3: For each stimulus, generate and show the chain

The chain is the artifact, not just the resulting idea. Show every link: the stimulus, its properties, the force-fit jump, the idea.

Open with a one-paragraph framing of why the technique works (first invocation only). Use a visual marker (emoji) per stimulus. Show the property list and the `→` force-fit arrow inline.

**Label each stimulus with its pool and its kind** — `🗼 The lighthouse beam — Vehicles & Transit [concrete]`. The label is what makes Step 2's minimums checkable: a reader counts the distinct categories, spots two adjacent draws from the same pool, and tallies concrete against abstract. Unlabelled chains make the rule unfalsifiable, which is the same failure as "it feels strained."

Per-stimulus length varies by quality of result. A weak stimulus gets two sentences and abandonment. A strong one gets two to three paragraphs, developed into a concrete direction with precedent where it exists.

### Step 4: Embrace abandonment

Roughly 1 in 4 stimuli will not pay off. **Show this explicitly**, for example: "🪡 The threading of a needle — every fit restated the target. Moving on."

Abandonment is a feature. It signals the method is genuine rather than retrofitted, and it reminds the user that quantity is what creates quality here. Forcing every stimulus to produce a good idea poisons the output.

**The redundancy test.** Before keeping a force-fit, ask: *could I have reached this idea from the target alone, without the stimulus?* If yes, the stimulus did no work — abandon it, however pretty the image. This is the test; "it feels strained" is not, because the operator who wants to look clever never feels strained.

The seductive failure is a stimulus that restates the target as a nicer picture of itself. A river delta laid over a churn dashboard yields "commits flow and deposit sediment" — vivid, and exactly what you already knew. Abandon it.

Hard rule: apply the redundancy test to every attempt, and abandon the stimulus the moment two successive attempts both fail it. A further attempt is worth making only to *confirm* the stimulus is dead, and it must be shown as such — "→ Third attempt: nothing new" — never as hope. Patience belongs to the batch, not to any one object.

### Step 5: Find the meta-pattern

After the batch, scan across the *ideas that landed* for a structural property that kept recurring — "all the strong hits had time or slowness as a feature", "three of the strongest cast the user as a defender, not a buyer", "most of these turned out to be community products, not tools".

Then scan the **abandonments** the same way. They usually share a reason, and that reason is itself a finding: if every dead stimulus died by restating the target, the target has an axis it is missing. Say what the abandonments had in common, not just that they happened. A good meta-pattern explains the failures as well as the hits.

This cross-stimulus observation is often where the deepest insight lives. State it explicitly. Name it mid-batch if it emerges before the end.

### Step 6: Honest ranking, no closure pressure

Pick the 3–5 sharpest directions. Say which feel weak, and why. Do not push the user to commit.

End with an explicit offer: pull more stimuli, go deeper on one direction, switch technique, or stop. The user controls when the technique ends.

## Honesty mechanics

**Abandonment rule:** two force-fit attempts, then the redundancy test from Step 4. A batch where every stimulus produces a viable idea is a tell that the output is fabricated — expect 2–3 abandonments per batch of 8–12.

**When the batch itself fails.** If more than half the stimuli die, do not draw more — that is the move that just failed. A target that nothing external will attach to is over-constrained or wrongly framed, and that is a diagnosis, not bad luck. Name the diagnosis, suggest the technique that fits it as the user's next move, and stop there. Do not run it yourself:

- The target is phrased as a solution rather than a problem, or you suspect you are answering the wrong question → suggest `concept-fan`, which climbs to the concept the solution serves.
- The target is fenced by a constraint so fixed that every stimulus bounces off it → suggest `provocation`, which breaks the constraint on purpose.

**Meta-pattern step:** never skip Step 5. The individual ideas matter less than the structural insight that emerges across them — and the abandonments are part of that scan, not excluded from it.

## What NOT to do

- **Don't sanitize weird ideas.** The unexpectedness is the value. If a force-fit produces something edgy or impractical, ship it as a direction; don't soften it.
- **Don't force every stimulus to produce a viable idea.** Abandonment is honest output.
- **Don't keep a force-fit that restates the target.** A vivid image is not a new idea. If you could have reached it without the stimulus, the stimulus did nothing — abandon it.
- **Don't answer a failed batch by drawing more stimuli.** That is the move that already failed. Diagnose the target and suggest the technique that fits — as a next move for the user, not one you run yourself.
- **Don't repeat stimuli** across batches in the same session.
- **Don't skip the meta-pattern step.** It is where the gold is, and it covers the abandonments too.
- **Don't push the user toward a decision.** The technique is divergent; convergence belongs to the user.
- **Don't run more than ~15 stimuli per batch.** Returns diminish and quality suffers.

## References

- [`references/stimulus-pools.md`](references/stimulus-pools.md) — categorized stimulus inventory to draw from
- [`references/worked-example.md`](references/worked-example.md) — a real session showing the full shape, abandonments included
