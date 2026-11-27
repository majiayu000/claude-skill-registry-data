---
name: porters-five-forces-analyzer
description: "Performs a rigorous Porter's Five Forces analysis: industry structure, supplier power, buyer power, threat of new entrants, substitutes, and rivalry intensity, with quantified pressure scoring and a strategic-positioning recommendation. Use when entering a new market, defending an existing position, evaluating an industry's structural attractiveness, advising on Mergers and Acquisitions (M&A) in a new vertical, or preparing a competitive strategy memo."
---

# Porter's Five Forces Analyzer

> Industry-structure analysis that explains why some markets are profitable and others aren't.

## What this skill is

A workflow that applies the Five Forces framework developed by Michael Porter with quantitative pressure scoring (1-5 per force) and the structural drivers behind each score. It surfaces the dominant force, identifies where the company can move the structure in its favor, and produces a positioning recommendation that goes beyond "the industry is attractive or unattractive."

## What it solves

- Industry analysis that stops at "competition is intense" without identifying which force matters most
- Strategy memos that ignore supplier or buyer power
- Treating substitutes only as direct competitors (missing adjacent threats)
- Static analysis with no view on how forces are evolving
- Recommendations disconnected from the structural levers identified

## When to invoke

- Entering a new vertical, geography, or product category
- Pre-Mergers and Acquisitions (M&A) diligence in an unfamiliar industry
- Defending current strategy when challenger dynamics shift
- Annual strategic plan industry-context refresh
- Board memo justifying a market exit or entry

## Phase 1: Define the industry boundary

Industries are not obvious - and a bad boundary choice invalidates the analysis. Decide:
- **Product or service scope** - what's in, what's out (e.g., "Business-to-Business (B2B) fleet telematics" vs. "vehicle hardware")
- **Geography** - global, regional, country-specific
- **Customer segment** - enterprise versus small and medium business; consumer versus industrial
- **Value chain stage** - manufacturer, distributor, retailer, service provider

Different boundaries can produce different forces. Document the choice explicitly.

## Phase 2: Force 1 - Supplier power

Score 1 (weak) to 5 (strong) and explain drivers:

| Driver | Pushes power UP | Pushes power DOWN |
|--------|-----------------|-------------------|
| Supplier concentration | Few, dominant suppliers | Many fragmented suppliers |
| Switching costs | High (proprietary inputs) | Low (commodity) |
| Forward integration threat | Credible | Not feasible |
| Importance of industry to supplier | Small customer for them | Large customer |
| Substitute inputs | None | Many viable |
| Differentiation of inputs | Highly differentiated | Commoditized |

Cite specific suppliers when known (e.g., Taiwan Semiconductor Manufacturing Company (TSMC) for advanced silicon).

## Phase 3: Force 2 - Buyer power

| Driver | Pushes power UP | Pushes power DOWN |
|--------|-----------------|-------------------|
| Buyer concentration | Few large buyers | Many small buyers |
| Switching costs | Low for buyer | High (lock-in, contracts) |
| Backward integration threat | Credible | Not feasible |
| Price sensitivity | Product is large percent of buyer's cost | Small share |
| Product differentiation | Commoditized | Highly differentiated |
| Buyer information | Full price transparency | Asymmetric |

Sub-segment buyers - enterprise behaves differently from small and medium business.

## Phase 4: Force 3 - Threat of new entrants

| Barrier | High barrier | Low barrier |
|---------|--------------|-------------|
| Economies of scale | Required | Not required |
| Capital requirements | Heavy | Light |
| Network effects | Strong | None |
| Switching costs for buyers | High | Low |
| Access to distribution | Locked up | Open |
| Brand and customer loyalty | Strong | Weak |
| Regulatory licenses | Required, scarce | None |
| Proprietary technology or data | Defensible | Replicable |
| Incumbent retaliation | Credible | Unlikely |

Score the **net entry barrier** 1 (low → high entry threat) to 5 (high → low threat).

## Phase 5: Force 4 - Threat of substitutes

Substitutes are alternative solutions to the same customer job - not direct competitors. Examples:
- Video conferencing → in-person meetings, asynchronous video, written documents
- Ride-sharing → public transit, walking, owning a car, working from home

| Driver | Pushes threat UP | Pushes threat DOWN |
|--------|------------------|--------------------|
| Substitute price-performance | Improving | Degrading |
| Buyer propensity to substitute | High | Low (entrenched habits) |
| Cost of switching to substitute | Low | High |

Map the **performance trajectory** of substitutes over the next 3-5 years.

## Phase 6: Force 5 - Rivalry intensity

| Driver | Higher rivalry | Lower rivalry |
|--------|---------------|---------------|
| Competitor concentration | Many similarly-sized | Few, with clear leader |
| Industry growth | Slow or declining | Fast |
| Fixed costs or capacity | High (drives price competition) | Low |
| Product differentiation | Low | High |
| Exit barriers | High (forces stay-and-fight) | Low |
| Strategic stakes | High for multiple players | Low |

## Phase 7: Aggregate and dominant force

| Force | Score (1-5) | Dominant drivers | Trajectory (3 years) |
|-------|------------:|------------------|----------------------|
| Supplier power | x | | ↑↓→ |
| Buyer power | x | | ↑↓→ |
| New entrants | x | | ↑↓→ |
| Substitutes | x | | ↑↓→ |
| Rivalry | x | | ↑↓→ |

Identify:
- **Dominant force** - the one most depressing industry profitability
- **Industry attractiveness** - sum scores; under 12 attractive, 12-18 moderate, over 18 difficult
- **Direction of travel** - net force pressure trajectory

## Phase 8: Strategic implications

The point of the Five Forces is not just "what's the industry like?" but **what to do about it**. For each force, identify the strategic lever:

| Force | Strategic moves |
|-------|-----------------|
| Supplier power | Vertically integrate, multi-source, build alternatives, build internal capability |
| Buyer power | Differentiate, raise switching costs, segment, build ecosystem |
| Entrants | Raise barriers (scale, network effects, intellectual property), preempt, M&A consolidation |
| Substitutes | Improve relative price-performance, redefine the job, partner with substitutes |
| Rivalry | Differentiate, segment, consolidate via M&A, signal credibly to discourage price wars |

## Output

- Five-force scorecard with drivers cited
- Industry boundary statement and trajectory of each force
- Dominant force identification and reasoning
- Industry attractiveness rating
- Strategic recommendation: where to invest to reshape the forces in your favor
- 3 leading indicators to monitor that would change the analysis

## Operating rules

**Always**
- State the industry boundary explicitly
- Score each force on a 1-5 scale with drivers cited
- Identify the dominant force, not a generic "competition"
- Project a 3-year trajectory per force
- Translate analysis into specific strategic moves

**Never**
- Treat the Five Forces as a static one-time exercise
- Confuse substitutes with direct competitors
- Conflate industry attractiveness with company performance
- Skip the boundary definition
- Stop at description without recommending action
