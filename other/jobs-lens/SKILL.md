---
name: jobs-lens
description: >-
  Review pitch and product copy through the lens of how Steve Jobs communicated,
  built from short sourced quotes from his launches, interviews and letters. Use
  on product one-liners, taglines, launch posts, deck lines, landing-page heroes
  and investor messages when the user asks for the Jobs view, or whether a line
  is clear, memorable or too abstract. Returns pass or fail per check and a
  rewrite. Independent framework, not affiliated with or endorsed by Steve Jobs,
  his estate or Apple.
---

# Jobs lens

Built from Steve Jobs's public statements. Independent framework: not an authorized adaptation, not a simulation of him, and not affiliated with or endorsed by Steve Jobs, his estate or Apple.

Asks one question of every line: **can the reader immediately picture what they get?** Source material: [references/quotes.md](references/quotes.md). Read it before the first use in a session and cite quotes by number in a verdict.

A check exists only where at least two verified quotes show it.

## The checks

| # | Check | Fails when | In his words |
|---|---|---|---|
| 1 | **Describe the result in the user's life.** The strongest descriptions let the listener imagine ownership or use. Quotes 2, 3, 32. | A hero that names only the technology, architecture or product category. | “music collection in your pocket” (2) |
| 2 | **Make a category claim only when the product visibly changes the category.**  Quotes 1, 5, 16. | Calling a minor improvement a revolution without explaining the change. | “entirely new category of devices” (5) |
| 3 | **Define what is being challenged.** Sometimes the target was a dominant rival; sometimes Apple's own execution. Quotes 14, 15, 17. | “We're better” without identifying what is actually inadequate. | “not our finest hour” (17) |
| 4 | **Give marketing a belief, not merely features.**  Quotes 7, 25, 27. | A values paragraph filled with interchangeable adjectives or a feature list pretending to be a mission. | “marketing's about values” (25) |
| 5 | **Work backward from experience, then explain the machinery.**  Quotes 2, 21, 26. | Opening with internal technology that the customer cannot yet connect to a benefit. | “customer experience” (26) |
| 6 | **Use actual numerical comparisons.**  Quotes 10, 11, 13, 31, 33. | “Massive opportunity,” “industry-leading” or “much faster” without a baseline. | “five times as many songs” (13) |
| 7 | **Engineer the reveal.** Set up comprehensible pieces, then show the synthesis. Quotes 3, 22, 23. | A long preamble that reveals the answer before the audience understands why it matters. | “one device” (23) |
| 8 | **Make technical changes understandable by comparison.** Technical explanation is allowed. Quotes 18, 19, 20, 21. | Either unexplained jargon or an analogy so vague that nothing technical remains. | “like trucks” (20) |
| 9 | **Make selectivity part of the promise.**  Quotes 24, 26, 29. | Pitching every possible customer, feature, vertical and use case simultaneously. | “saying no” (24) |
| 10 | **Distinguish ambition from compulsory grandiosity.**  Quotes 6, 9, 35. | Claiming every useful product will necessarily change civilization. | “don't have to change the world” (9) |
| 11 | **Use a superlative only when its dimension is testable.**  Quotes 4, 5, 13, 30. | “The best AI platform ever” without a category, measurement or demonstration. | “world’s thinnest notebook” (4) |

Two common beliefs about Jobs fail against the sources: that he never talked about technology (check 8) and that he always led with a sweeping mission (check 10).

Which checks apply: a one-line product description must pass 1, 5 and 11. A market or competitor line must pass 3 and 6. A tagline must pass 2 and 11. A whole message must pass 9.

## Order: ambition, context or plain product first

Four launches, classified by the first substantive argument (sources in quotes.md):

| Launch | Opens with |
|---|---|
| Macintosh 1984 | history of the category: "only been two milestone products" (46), Mac as the third (1) |
| iPod 2001 | strategy and market (the digital hub, music), then the product (2) |
| iPhone 2007 | "a revolutionary product", then three familiar products, then the reveal (3, 23) |
| iPad 2010 | "magical and revolutionary" teaser, then the gap between phone and laptop (5) |

Ambition-first is well supported. An opaque tagline first is NOT: his ambition openings always had a referent the audience already knew (the computer industry, an iPod, a phone, a laptop), and his own stated rule is to start from the customer experience (26). Test: can the first sentence be understood without the second? If not, swap the order or give the first sentence a known referent. A stage reveal also assumes an audience that cannot leave; a cold message does not have that.

## The limit

The lens never licenses a claim that is not true today. Superlatives need a testable dimension (check 11); category claims need a visible change (check 2).

## What not to copy

- Ridiculing established competitors (14, 15). Name the real weakness, not their taste.
- Announcing the death of a whole category (16). Say which use cases move and why.
- Claiming a new category without a product that shows it (1, 5).
- Holding the reveal late (3, 23). In a deck or cold email the reader leaves first.
- Reading "customers don't know what they want" (28) as permission to ignore them; he also said to start from the customer experience (26).
- Downplaying money (35). Investors still need the business model.
- His words. Copy the shape, never the sentences.

## Output

```
"<line>"
check 1 result in user's life   PASS | FAIL  <five words why>
...
verdict: PASS | REWRITE
rewrite: "<line>"   (only when REWRITE; every claim true today)
```

Only the checks that apply. No essay. If the user supplied the line in their own words, keep their beats and change only what fails.

## Where it sits

Next to musk-lens and thiel-lens. Musk asks "what is the breakthrough and why does it work", Thiel asks "what do you own and why does it last", Jobs asks "what do I get". When the lenses disagree, report the split; do not average it.
