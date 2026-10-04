---
name: competitor-mapper
description: Map the competitive landscape by tier (direct/indirect/acquirer/adjacent) and argue why each could win. Antidote to competitor neglect.
---

# Competitor Mapper

## When you activate
User asks: "who else does this?", "competitive landscape for X", "should I worry about Y?", "map the space"

## What you produce
```
## Competitive map — <space>

### Tier 1: Direct competitors (same problem, similar solution)
| Name | Stage / size | Pricing | Their angle | Why they could win | Their weakness |
|---|---|---|---|---|---|
| X | Series A, ~50 people | $49/mo | feature-rich | distribution | UX bloat |

### Tier 2: Indirect competitors (same problem, different solution shape)
| Name | What they do instead | Why users use them |
|---|---|---|
| X | spreadsheets | already paid for, familiar |

### Tier 3: Potential acquirers / adjacent players
| Name | Why they might enter | What it means for us |
|---|---|---|
| Big Co | already serves the customer; could bundle | exit option but also threat |

### Tier 4: The status quo
What users are doing today *without* any tool. Often the real competitor.

### The strongest argument against us
If a generalist competitor at Tier 3 ships this feature next quarter, what's our defense? <one paragraph>

### Our differentiation hypothesis
<one sentence — what's true about our approach that competitors can't easily copy>

### Disconfirming check
If our differentiation is "better UX": that's not defensible. If it's "we have the customer's data and workflows locked in via X": that's defensible. Be honest.
```

## Protocol
1. WebSearch for the top 10 results on "<problem> tools/software/apps 2026".
2. Cross-check Product Hunt, IndieHackers, and G2 for indie + recent entries.
3. For each Tier 1 competitor: read their pricing page and homepage. Don't trust their marketing — note actual features.
4. Force the kill-question: what stops a competitor from copying us in 30 days?

## Sources
- `knowledge-base/scale-stage/moat-building.md`

## What you don't do
- Don't list 30 competitors. Top 5–8 by relevance. Add a "noted but not detailed" line for the rest.
- Don't claim "no competitors" — there's always Excel + email + manual process. That's the real Tier 4.
- Don't promise differentiation without naming what makes it hard to copy.
