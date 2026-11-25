---
name: musk-lens
description: >-
  Review pitch and product copy through the lens of how Elon Musk communicates,
  built from short sourced quotes from the Tesla master plans, SpaceX
  presentations, interviews and internal emails. Use on product one-liners,
  mission and market lines, cost or speed claims, roadmap and "why now" lines,
  deck text and investor messages when the user asks for the Musk view, or
  whether an ambitious claim is credible. Returns pass or fail per check and a
  rewrite. Independent framework, not affiliated with or endorsed by Elon Musk
  or his companies.
---

# Musk lens

Built from Elon Musk's public statements. Independent framework: not an authorized adaptation, not a simulation of him, and not affiliated with or endorsed by Elon Musk or any of his companies.

Asks one question of every line: **can the reader see the breakthrough and why it works?** Source material: [references/quotes.md](references/quotes.md). Read it before the first use in a session and cite quotes by number in a verdict.

A check exists only where at least two verified quotes show it.

## The checks

| # | Check | Fails when | In his words |
|---|---|---|---|
| 1 | **Give the plain product, but preserve the distinctive technical idea.**  Quotes 1, 3, 4, 5. | A generic customer benefit that conceals the actual invention, or jargon without an explanation. | “brain and spine problems” (4) |
| 2 | **Tie the product to an explicit larger outcome.**  Quotes 6, 7, 8. | A mission unattached to the product's actual causal contribution. | “make Mars seem possible” (8) |
| 3 | **Bound the market rather than claim everything.**  Quotes 11, 12, 13. | Multiplying a global category by an arbitrary percentage and presenting the result as a realistic market. | “half the market wants a sedan” (11) |
| 4 | **Derive economics from constraints and inputs.**  Quotes 20, 21, 34, 35, 36. | Claiming an order-of-magnitude cost advantage without showing the cost structure that permits it. | “a billion dollars a mile” (34) |
| 5 | **Name a specific wrong assumption or wasteful practice.**  Quotes 15, 17, 18. | Treating the enemy as an abstract industry that is simply “broken.” | “ugly and slow” (15) |
| 6 | **Show the sequence that makes the ambition financeable.**  Quotes 24, 25, 37, 38. | Jumping from an expensive prototype to mass adoption without an intermediate economic step. | “expensive car and low volume” (24) |
| 7 | **Question and remove before improving.**  Quotes 17, 28, 32. | Promising faster execution of a process whose existence you have not justified. | “less dumb” (28) |
| 8 | **Demonstrate the physical claim.**  Quotes 3, 15, 27. | Relying on superlatives where a meaningful test is possible, or presenting a staged demo as independent validation. | “show you” (27) |
| 9 | **Use an analogy as an entry into the mechanism.**  Quotes 19, 22, 23. | An entertaining metaphor that leaves the audience unable to explain what the product does. | “14 story building” (23) |
| 10 | **Cut communication and activity that do not advance the product.**  Quotes 17, 29, 31, 32. | A long deck that repeatedly restates the same claim without adding proof. | “signal over noise” (29) |
| 11 | **Specify the units and the status of every important number.**  Quotes 14, 33, 34, 35, 36. | Conflating cost estimates, price promises, market observations and engineering targets. | “per person” (36) |

"Always simplify to a slogan" is not a Musk rule. The first Tesla master plan carries a full efficiency calculation, the Hyperloop paper discusses failure modes and limits, and his TED tunnelling answer breaks cost into diameter, area and machine utilisation. Long is allowed when every sentence adds proof (check 10).

Which checks apply: a one-line product description must pass 1. A mission line must pass 2. A market line must pass 3. Any cost, speed or scale claim must pass 4 and 11. A roadmap or use-of-funds line must pass 6. A whole message must pass 10.

## Order: mission, problem or plain product first

Six launches, classified by the first substantive argument (sources in quotes.md):

| Launch | Opens with |
|---|---|
| Roadster / master plan 2006 | the plain product (1), mission in the next sentences (6) |
| Powerwall 2015 | the system-wide change and the broken energy system (50, 19) |
| Model 3 2016 | "Why does Tesla exist?", then the product |
| Mars architecture 2016 | the mission (8, 10) |
| Neuralink 2019 | what the event is for (recruiting), then problem and device (4) |
| Cybertruck 2019 | the status quo: trucks unchanged for a century |

So mission-first or enemy-first is well supported, and so is product-first. What is NOT supported: opening with a line the listener cannot parse. His mission openings carry their own meaning (go to Mars, end fossil dependence, a truck that is different). Test: can the first sentence be understood without the second? If not, swap the order or rewrite the first sentence.

## The limit

Targets and results are different things (check 11). A number is a measured result, an estimate, a price promise or an engineering target, and the copy says which. Never present a target as achieved.

## What not to copy

- Claim financing is secured before it actually is. Evidence: 39, the August 7, 2018 “Funding secured” tweet. The SEC subsequently brought securities-fraud allegations concerning the statement, and Musk and Tesla settled. Why it hurts: a seed founder must distinguish interest, verbal intentions, signed commitments, and received funds.
- Give speculative deadlines the same certainty as demonstrated results. Evidence: Musk's April 28, 2017 TED interview, including his autonomous-driving predictions. Why it hurts: an engineering target is not a shipped capability. Missing a highly publicized target weakens subsequent claims.
- Build a launch around a risky live demonstration without a fallback. Evidence: 27 and the November 21, 2019 Cybertruck presentation, where the window-glass test failed visibly. Why it hurts: the failed demonstration can become the story instead of the demonstrated product advantage.
- Use contempt as a substitute for showing why a requirement is wrong. Evidence: 28 and 32, Musk's five-step engineering algorithm. Why it hurts: questioning requirements is valuable, but insulting customers, employees, or the people who wrote those requirements can obstruct the very feedback a founder needs.
- Confuse theoretical input costs with deliverable product economics. Evidence: 20 and 35, the 2012 first-principles battery-cost argument. Why it hurts: raw materials exclude assembly, labor, yield, capital expenditure, reliability and distribution.
- Make personal financial sacrifice sound like a reproducible financing strategy. Evidence: 37 and 38, Musk's accounts of the 2008 Tesla financing crisis and his willingness to fund Mars ambitions. Why it hurts: personal commitment can build confidence, but investors still need milestone-based capital requirements and a credible funding path.
- His words. Copy the shape, never the sentences.

## Output

```
"<line>"
check 1 plain product + technical idea   PASS | FAIL  <five words why>
...
verdict: PASS | REWRITE
rewrite: "<line>"   (only when REWRITE; every claim true today, targets labelled as targets)
```

Only the checks that apply. No essay. If the user supplied the line in their own words, keep their beats and change only what fails.

## Where it sits

Next to jobs-lens and thiel-lens. Jobs asks "what do I get", Thiel asks "what do you own and why does it last", Musk asks "what is the breakthrough and why does it work". When the lenses disagree, report the split; do not average it.
