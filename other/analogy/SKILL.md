---
name: analogy
description: Forced Analogy / Structural Transplant — map the problem onto a structurally similar system from a distant domain (immune system, air-traffic control, restaurant kitchen, jazz ensemble) and transfer its mechanisms back. Use when a solution works but feels derivative, when the industry playbook is exhausted, or when a system in nature or another trade already solves this shape of problem. Triggers include "analogy", "forced analogy", "how would a hospital/kitchen/airport handle this", "transplant from another industry", "structurally similar system". Do NOT use for analytical work like debugging, code review, or implementation tasks.
---

# Forced Analogy (Structural Transplant)

## What this technique does

Take the problem, strip it down to its bare structure — who the actors are, what flows between them, where it jams — and find a system in a distant domain that has the same shape. An immune system, an air-traffic control tower, a restaurant kitchen at dinner rush. Then ask what that system *does* about the jam that you don't, and carry the mechanism back as a concrete idea. The point is distance: the further the source domain sits from your problem, the more its solutions will look nothing like the ones already on your whiteboard.

Source: Synectics (William J.J. Gordon, *Synectics: The Development of Creative Capacity*, 1961), specifically the "direct analogy" operation; widely used in biomimicry and TRIZ-adjacent practice.

## Workflow

### Step 1: Confirm the target

A valid target is a concrete creative or design problem: how to grow something, how to route something, how to redesign a process or a system. If it is unclear, ask one focused question — "What's the system you're trying to reshape, and where does it jam?"

Refuse requests to *perform* analytical work — debugging, reviewing code, implementing a change — and suggest an analytical approach instead. Redesigning or ideating about such a process is a valid creative target: "reinvent our code-review ritual" is in scope; "review this PR" is not.

### Step 2: State the problem's structure in one sentence

Reduce the target to actors, flows, and the bottleneck. No domain vocabulary, no solution language — just the shape. For example: "many independent producers, one congested channel, quality varies." This sentence is the load-bearing part of the whole technique; if it still names your industry, it is not abstract enough yet.

### Step 3: Draw 3-5 domains whose structure rhymes

Pull from [`references/domain-pool.md`](references/domain-pool.md). Choose domains whose structural property matches the sentence from Step 2, not domains that sound related to your problem. **Mix at least one biological, one operational, and one social/cultural** so the transplants come from genuinely different logics. Never run more than five in a batch.

### Step 4: Per domain, map roles then transfer a mechanism

For each domain, do two things in order:

1. **Map the roles.** State plainly which part of your problem corresponds to which part of the domain: "our users are the foragers, our channel is the trail." If the mapping is clean, one line does it.
2. **Ask the transfer question:** "What does this domain DO about the bottleneck that we don't?" Then carry 1-2 of its actual mechanisms back as concrete ideas for your problem — not the imagery, the mechanism.

### Step 5: Meta-pattern scan

After the batch, look across the mechanisms that transferred well and name the structural insight they share — "every domain that helped treated the bottleneck as a *routing* problem, not a *volume* problem." State it explicitly. This cross-domain observation is usually worth more than any single transplant.

### Step 6: Honest ranking, no closure pressure

Pick the sharpest transplants. Say which are weak and why. Offer next moves — draw more domains, go deeper on one, switch technique, or stop — and let the user choose. Never push the user to commit.

## Honesty mechanics

**One-forced-role rule.** A clean mapping costs you one metaphorical leap. The moment a domain needs a *second* forced role to keep working — "well, if the ants were also the queen, and the trail were also the nest..." — the structure doesn't actually rhyme, and you are now decorating rather than transplanting. Abandon it visibly and say why.

**Surface analogies are named and dropped.** A domain that shares *vocabulary* with your target but not *structure* is the most seductive trap and the most useless. Call it out as surface-level and drop it. A batch where every domain transfers cleanly is a tell that the output is being retrofitted; expect at least one honest abandonment.

**When no domain rhymes.** If every domain needs a second forced role, the fault is usually the Step 2 sentence, not the domains. Rewrite it once. If the rewrite still names no bottleneck, stop drawing domains — name the diagnosis, suggest the technique that fits it as the user's next move, and stop there rather than running it yourself:

- The structure sentence keeps coming out as a solution rather than a shape → suggest `concept-fan`, which climbs until the real problem appears.
- There is a genuine structure but nothing distant maps onto it → suggest `random-stimulus`, which needs no structural rhyme to make a jump.

## What NOT to do

- **Don't pick domains that share vocabulary with the target.** Software-to-marketplace, app-to-platform — too close. The shared words hide the fact that no real transfer happened. The whole value is distance.
- **Don't transfer aesthetics instead of mechanisms.** "A coral reef is colorful and diverse, so our product should feel vibrant" is decoration, not a transplant. Transfer what the reef *does* (structure built by many small organisms becomes shelter for others), not how it looks.
- **Don't run more than 5 domains per batch.** Returns diminish and the mappings blur together.
- **Don't rescue a domain that needs more than one forced role.** Drop it and move on.

## References

- [`references/domain-pool.md`](references/domain-pool.md) — structurally rich source domains to draw from, with the transferable property of each
- [`references/worked-example.md`](references/worked-example.md) — a real session showing the full shape, one genuine abandonment included
