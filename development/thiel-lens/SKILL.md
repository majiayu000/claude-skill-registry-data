---
name: thiel-lens
description: >-
  Test a company's strategy, moat and pitch through the lens of how Peter Thiel
  argues, built from 52 short sourced excerpts from the WSJ essay "Competition
  Is for Losers", his Stanford CS183B lecture, Zero to One and interviews. Use
  when the user asks for the Thiel view, for "why won't the incumbent or the
  platform owner eat us", "what is our moat", "what is our secret", for market
  definition and first-market choice, and next to jobs-lens and musk-lens on
  deck and investor answers about defensibility. Independent framework, not
  affiliated with or endorsed by Peter Thiel.
---

# Thiel lens

Built from Peter Thiel's public statements and writing. Independent framework: not an authorized adaptation, not a simulation of him, and not affiliated with or endorsed by Peter Thiel, his co-author or his firms.

Asks one question of every strategy line: **what will this company own that nobody else offers, and why does it last?** Source material: [references/quotes.md](references/quotes.md). Read it before the first use in a session and cite quotes by number in a verdict.

Built to the same standard as the Jobs and Musk lenses: a check exists only where at least two verified quotes show it.

Unlike the Jobs and Musk lenses, this one judges the argument, not only the wording. A line can read well and still fail.

## The checks

| # | Check | Fails when | In his words |
|---|---|---|---|
| 1 | **Unique, not better.** The company offers something nobody else offers. Quotes 1, 2, 5, 41. | "like X but better, cheaper or neutral"; a list of competitors it beats. | “no one else is offering” (5) |
| 2 | **Honest market definition.** Neither shrunk to an intersection you win by definition, nor inflated to a union. Quotes 6, 7, 8, 9. | "the X of Y" or "X for Z" as the whole identity; or a giant category as the market. | “the nothing of nowhere” (9) |
| 3 | **An order of magnitude on one named dimension.** Quotes 10, 11, 24, 47. | several modest improvements; no dimension named; no measurement. | “on one dimension they were dramatically better” (24) |
| 4 | **A small first market you can take whole.** A named group, concentrated, with few or no competitors. Quotes 15, 16, 17, 18, 19, 46, 52. | a giant market on day one; no named first group; being the tenth of something. | “about twenty thousand people” (17) |
| 5 | **Sequence outward and avoid head-on fights.** Quotes 20, 21, 35, 36, 37. | a plan that needs to beat an incumbent directly; "disrupt" as the strategy. | “avoid competition as much” (21) |
| 6 | **Last mover, not first.** The position still holds in 10 and 20 years. Quotes 22, 23, 25, 26, 44. | first-mover claims; no account of why a later entrant cannot replace it. | “the last company in a category” (22) |
| 7 | **Name the source of durability and show it strengthens with time.** One of technology, network effects, scale, brand. Quotes 12, 13, 14. | a network effect with no value for the first user; all four claimed at once. | “valuable to the first person” (12) |
| 8 | **A secret.** A specific truth few agree with, which is why nobody else is building it. Quotes 27, 28, 29, 41, 30. | an idea everyone already agrees with; "the market is huge" as the insight. | “what valuable company is nobody building?” (41) |
| 9 | **Distribution is part of the design.** One channel that works. Quotes 31, 32, 33, 42. | "it will spread"; five channels listed; product-only thinking. | “just one distribution channel” (32) |
| 10 | **Capture some of the value created.** Quotes 3, 34, 49. | large value created, no account of who pays or why margins hold. | “capture some of the value” (34) |
| 11 | **Complement people rather than replace them.** Quotes 38, 39. | a pitch built on making people obsolete. | “complements for humans” (39) |

Two beliefs about Thiel fail against the sources: that he tells founders to call themselves a monopoly (he says monopolists hide it, 6, and calls the idea "on the border of what I want to say", 49), and that he praises disruption (43, 21).

Which checks apply: a "why won't X eat us" answer must pass 1, 6 and 7. A market line must pass 2 and 4. A roadmap must pass 5. A "why us" or insight line must pass 8. A go-to-market line must pass 9. A business-model line must pass 10.

## Using it on "why won't the platform owner eat us"

There is no verified Thiel quote about building on someone else's platform (see Gaps in quotes.md). Answer the question with checks 1, 3, 4, 6 and 7 in that order:

1. What does the company offer that the platform owner does not and will not (1)?
2. On which single dimension is it an order of magnitude better than the owner's own version, and where is the measurement (3)?
3. Which small group does it own completely today (4)?
4. Why is it the last company in that category rather than the first (6)?
5. Which one source of durability grows with use, and what did the first user get (7)?

If step 2 has no measurement, say so. The lens does not accept "neutral" or "independent" as an answer to step 1 on its own: that is a position, not a product nobody else offers.

## The limit

The lens never licenses a claim that is not true today. An order-of-magnitude claim needs a number with its source. A secret must be stated as a belief until it is shown.

## What not to copy

- Saying "monopoly" in a pitch. His own account is that real monopolists describe themselves as small players in a big market (6).
- Dismissing competitors entirely. He names the cost of fighting them (35, 36), which is a reason to avoid them, not to pretend they are absent.
- Dated forecasts. "AI feels slightly overhyped" is from 2015 (48).
- His politics and stagnation essays. They are not in the ledger and do not belong in investor copy.
- His words. Copy the shape, never the sentences.

## Output

```
"<line or claim>"
check 1 unique, not better     PASS | FAIL  <five words why>
...
verdict: PASS | REWRITE | MISSING FACT: <the one fact needed>
rewrite: "<line>"   (only when REWRITE; every claim true today)
```

Only the checks that apply. No essay. If the user supplied the line in their own words, keep their beats and change only what fails.

## Where it sits

Next to jobs-lens and musk-lens. Jobs asks "what do I get", Musk asks "what is the breakthrough and why does it work", Thiel asks "what do you own and why does it last". When they disagree, report the split; do not average it.
