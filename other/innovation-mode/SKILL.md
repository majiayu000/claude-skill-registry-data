---
name: innovation-mode
description: Runs an 8-phase divergent-thinking protocol that reframes a problem, searches distant conceptual fields, generates 30+ candidate approaches, strips out fake novelty, stress-tests the survivors adversarially, and designs the cheapest experiment that would change your mind. Use this whenever the user wants ideas that are NOT the standard playbook — triggers include "innovation mode", "think differently", "what's non-obvious", "unconventional", "what is everyone missing", "I don't want the usual advice", "blue sky", "what would nobody else do", "creative options", or any sign they're frustrated that suggestions feel generic, templated, obvious, or already tried. Also use for open-ended strategy, product, pricing, marketing, growth, or system-architecture questions where the conventional answer is already known and the value lies in finding overlooked options. Do NOT use it to choose between options that are already defined (that's decision analysis) or to execute a build (that's a delivery workflow).
---

# Innovation Mode

A search procedure, not a brainstorm. The goal is to surface **non-obvious, mechanistically plausible, testable** possibilities that a competent domain expert would initially miss — and to be honest about which ones are speculation.

Success is not an impressive-sounding document. Success is 3 ideas worth spending real money to test, at least one of which the user had not considered.

## Step 1 — Fill in the [fields]

The protocol is in `references/prompt-template.md`. Read it before anything else. The template ships with a `## Problem` field marked `[Describe the problem...]` — filling that in well determines the quality of everything downstream.

Build the problem statement from what the user gave you plus conversation context. A usable statement contains:

- **the actual situation** (not the abstraction of it),
- **what "better" means** — the outcome being optimized, ideally measurable,
- **hard constraints**: capital, time, headcount, regulation, licensing, physics,
- **what has already been tried or is industry standard**, so the protocol knows what counts as obvious.

If two or more of those are missing, ask **up to three questions in a single batch**, then proceed regardless of how completely they answer. This is idea generation, not a requirements interview — one round of questions only. If the user says "just go," go, and mark the gaps as assumptions.

Then restate the filled-in problem in 3–5 lines and start. Do not ask permission to begin.

## Step 2 — Run the phases

Work through all eight phases in `references/prompt-template.md`. They are sequenced deliberately: divergence (1–3) must finish before filtering (4–5), because early filtering is what collapses this into ordinary consulting output.

Load `references/lenses.md` at Phase 2 for the lens bank and the provocation questions that keep each lens genuinely different. Load `references/quality-gates.md` at Phase 4 and keep it open through Phase 8 — it holds the fake-novelty detector, the adversarial checklist, and the experiment spec.

Phase enforcement — these are the rules that make the difference between a real search and a performance:

- **Phase 1**: at least 10 assumptions, sorted into real constraints (physics, math, law, licensing) versus inherited ones (convention, customer expectation, org habit). The single highest-value output of this whole protocol is usually one "real" constraint correctly reclassified as inherited. Say explicitly which category each falls in and how confident you are.
- **Phase 3**: 30 candidates, one line each — `Idea → mechanism → why it might matter`. Two distinctness tests: (a) if swapping the industry noun for another industry leaves the idea intact, it's generic filler, and (b) if two ideas share the same causal mechanism, they are one idea. Hit the quotas honestly — 10 unconventional, 5 that sound unreasonable at first, 5 that *delete* a requirement rather than improve it, 5 that change the business model, incentives, or workflow rather than the product.
- **Phase 4**: name at least five ideas you are killing and why. Killing nothing means the filter did not run. Never carry forward anything whose novelty is "the existing thing, plus AI."
- **Phase 6**: for each finalist, state the specific observation that would falsify it. "It might not work" is not a falsifier. "If fewer than 3 of 20 customers accept the offer at that price, the thesis is dead" is.
- **Phase 8**: experiments must be runnable within weeks at low cost by the user as they exist today — not by a version of them with a team and funding.

Do not narrate the phases as you go. Run them, then report.

## Step 3 — Report

Write the deliverable to a markdown file when a filesystem is available, and give the user the final five sections in chat. Otherwise put everything in chat.

Structure — keep this order:

```
## Reframe
Conventional framing, then the assumption table (real vs inherited), then the 5 alternative
formulations. Compact.

## Search log
One line per lens (8+). One line per candidate idea (30+), grouped by lens.
Then the kill list from Phase 4 with reasons.

## Finalists
The 5 that survived selection, with the Phase 6 critique and Phase 7 radical version folded in.

## Final output
1. Most important reframing
2. Three strongest opportunities — concept / insight / mechanism / why non-obvious /
   why disproportionate value / biggest reason it fails
3. Most contrarian hypothesis
4. Cheapest high-information experiment
5. What we may still be missing
```

The search log is evidence that the search was wide, so keep it — but at one line per item. Everything else earns its length or gets cut.

## Standing rules

**Separate what you know from what you're guessing.** Tag any load-bearing claim that rests on inference rather than knowledge. Where an idea depends on a regulation, a cost figure, a market size, or a technical spec you don't actually have, say so plainly and name what would need to be looked up — an invented number destroys the value of the whole exercise. Search the web when a current figure or rule is cheap to verify and the idea hinges on it.

**Eloquence is not insight.** Before an idea ships, strip its adjectives. If the remaining sentence doesn't name a specific mechanism and a specific effect, it's a phrase, not an idea.

**Causal mechanism, not analogy.** "Like Netflix did for DVDs" is a gesture. The mechanism is *why* the thing produces the effect — what changes, in what order, for whom, and why that changes the outcome.

**Preserve strange ideas long enough to evaluate them.** At least one of the three finalists should be something you'd personally put under 35% odds of working, provided its downside is small and its information value is high. This protocol is explicitly not selecting on probability of success — it selects on limited downside + cheap validation + large upside + high learning.

**Don't defend your own output.** In Phase 6 you're the skeptic, not the author. If a finalist doesn't survive, say so and promote the next candidate rather than propping it up.

**Novelty is not the objective; overlooked value is.** If the honest answer is that the conventional approach is close to optimal and the real opportunity is executional, say that — and spend the search on the narrow places where it isn't. A protocol that manufactures exotic ideas for a problem that doesn't have them has failed.
