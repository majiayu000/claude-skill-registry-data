---
name: market-research
description: Conduct market research, competitive analysis, and industry intelligence. Use when the user wants market sizing, competitor comparisons, OSS landscape scans, distribution analysis, or research that informs build-or-skip decisions.
origin: ECC (adapted)
---

# Market Research

Produce research that supports build-or-skip decisions, not research theater.

## When to Activate

- evaluating whether a market is worth entering
- sizing a market opportunity
- comparing competitors, adjacent products, or OSS alternatives
- researching a technology, vendor, or infrastructure choice
- pressure-testing a thesis before building or entering a market
- validating pricing before writing code

## Research Standards

1. Every quantitative claim must have a `[SOURCE: ...]` tag or be labeled `[ESTIMATE]`.
2. Prefer recent data. Flag anything older than 18 months as `[STALE]`.
3. Steel-man the opposite conclusion.
4. Translate findings into a decision, not just a summary.
5. For each key assumption, state what evidence would falsify it.
   Example: "Assumption: ML engineers will pay for managed experiment tracking. Kill condition: >60% of community threads recommend self-hosted and cite cost as primary reason."

## Research Modes

Default to **Market Sizing + Competitive Landscape**. Add other modes only when the question demands them.

### Market Sizing

Three lenses, plain language:

- **TAM** (Total Addressable Market) — everyone who could theoretically use this. The ceiling.
- **SAM** (Serviceable Addressable Market) — the slice you can actually reach with your product's scope and geography.
- **SOM** (Serviceable Obtainable Market) — what you can realistically capture in 1-2 years given your distribution, pricing, and team size.

For each:
- state the number and the assumption behind it
- use top-down data (reports, public datasets) cross-checked with bottom-up math (realistic customer counts x price)

Anchor SOM to the go-to-market motion:
- **Solo/indie**: "How many paying users can I reach through channels I can operate alone, at what price?"
- **B2B/enterprise**: "How many teams can I reach given sales cycle length, integration complexity, and deal size?"

### Competitive & OSS Landscape

Collect:
- product reality, not marketing copy
- OSS alternatives (GitHub activity, contributor health, license, adoption curve)
- funding history if public (signals runway and priorities, not a scorecard)
- traction signals (users, revenue, community size) if public
- pricing and packaging
- strengths, weaknesses, and positioning gaps
- build vs. buy vs. fork trade-off for the user's context

Distribution:
- where target users already congregate (communities, forums, marketplaces, conferences)
- realistic customer acquisition cost for the user's go-to-market motion
- existing distribution moats (integrations, marketplaces, API ecosystems)

### Pricing Analysis

Requires user-provided data (links, screenshots, forum threads) for specifics beyond known market structure.

Analyze:
- what do people currently pay for similar solutions?
- pricing tiers and anchoring in the category
- free vs. paid boundary — what features cross the pay threshold?
- for B2B: typical contract size, procurement friction, budget owner

### Technology / Vendor Research

Collect:
- how it works (architecture, key trade-offs)
- adoption signals and ecosystem health
- integration complexity
- lock-in risk, data portability, and exit cost
- security, compliance, and operational burden
- cost trajectory at scale

## Output Format

Default structure:
1. **Decision summary** — build, skip, or investigate further, in one paragraph
2. **Key findings** — with `[SOURCE: ...]` or `[ESTIMATE]` tags on quantitative claims
3. **Assumptions & falsifiability** — each key assumption with its kill condition
4. **Risks and counterarguments** — steel-manned opposing view
5. **Recommendation** — concrete next step
6. **Sources** — linked and dated

## Quality Gate

Before delivering:
- all numbers are sourced or labeled as estimates
- stale data is flagged
- the recommendation follows from the evidence
- at least one steel-manned counterargument is included
- key assumptions have explicit kill conditions
- the output makes a build-or-skip decision easier
