---
name: market-analyzer
description: 'Comprehensive market analysis and sizing engine that goes beyond TAM/SAM/SOM to include growth drivers, risk factors, segment dynamics, and investment-grade market maps. Use when: market analysis, market sizing, market research, industry analysis, segment analysis, market opportunity, market landscape, how big is this market.'
---

# Market Analyzer (SCOPE Framework)

Full-spectrum market analysis producing investment-grade market maps with sizing, growth drivers, risk factors, and segment-level deep dives. Goes beyond basic TAM/SAM/SOM.

## When to Use
- New market entry decisions
- Board/investor market briefings
- Product strategy validation
- Fundraising market slides
- Annual strategic planning

## What You'll Need
**Critical inputs (ask if not provided):**
- Market or product category to analyze
- Geographic scope (global, US, EMEA, etc.)
- Time horizon (current year + forecast period)

**Nice-to-have:**
- Whitespace Finder output (opportunities to size)
- Signal Radar output (trends affecting the market)
- Existing market data or analyst reports

## Process

### Step 1: Market Definition
Before sizing, rigorously define the market boundaries:
- **Category definition**: What products/services are included? What is excluded?
- **Buyer definition**: Who purchases? (roles, company types, segments)
- **Use case definition**: What problems does this market solve?
- **Adjacent markets**: What related markets overlap or compete for budget?

### Step 2: SCOPE Analysis
Analyze the market across 5 structural dimensions:

| Dimension | What It Covers | Key Questions |
|-----------|---------------|---------------|
| **S**ize & Growth | TAM/SAM/SOM + growth trajectory | How big? How fast growing? Top-down AND bottom-up? |
| **C**ompetitive Density | Number and strength of competitors | How crowded? Any dominant players? Fragmented or consolidated? |
| **O**pportunity Windows | Timing-sensitive opportunities | What market shifts create openings? What is the window duration? |
| **P**ower Dynamics | Who holds power in the value chain | Buyer power? Supplier power? Platform dependencies? Regulatory influence? |
| **E**conomic Drivers | What drives market growth or contraction | Macro trends? Technology adoption curves? Budget cycle patterns? |

### Step 3: Multi-Method Sizing
Use THREE methods and triangulate:

**Method 1: Top-Down**
- Start with total industry spend (from analyst reports, government data)
- Apply relevant filters (geography, segment, use case)
- Result: TAM -> SAM -> SOM

**Method 2: Bottom-Up**
- Count addressable accounts/users in target segments
- Multiply by expected annual contract value
- Apply realistic penetration rates (year 1: 1-3%, year 3: 5-10%)
- Result: Revenue potential by segment

**Method 3: Value-Theory**
- Calculate the economic value your product creates for customers
- Estimate what percentage of that value you can capture as price
- Multiply by addressable customer count
- Result: Value-based market ceiling

**Triangulation**: Compare all 3 methods. If they are within 30% of each other, confidence is HIGH. If 30-60% apart, confidence is MEDIUM. Over 60% apart, revisit assumptions.

### Step 4: Segment Deep Dives
For each major segment, produce:
- Segment size and growth rate
- Segment-specific competitive landscape
- Segment-specific buyer behavior
- Segment attractiveness score (1-10): size x growth x accessibility x fit
- Strategic recommendation: Enter / Monitor / Avoid

### Step 5: Risk and Sensitivity
Identify the top 5 assumptions driving the sizing and test each:
- What if growth rate is 50% lower than projected?
- What if a major platform changes pricing/policy?
- What if a new entrant disrupts the category?
- What if regulatory changes shrink the addressable market?

For each risk, estimate: probability (%), impact on sizing (%), and mitigation.

## Output
Save to `outputs/market-analysis-[market]-[YYYY-MM-DD].md`

### Deliverables:
1. **Market Map**: Visual landscape showing segments, competitors, sizing, and growth with your positioning
2. **Sizing Summary**: TAM/SAM/SOM via 3 methods with triangulation confidence score
3. **Segment Scorecards**: Per-segment analysis with attractiveness scores and strategic recommendations
4. **Risk Register**: Top 5 assumptions with sensitivity analysis and mitigation strategies
5. **Executive Brief**: 2-page summary suitable for board/investor presentations

## Chain Connections
- **Next skill**: Run `journey-architect` to map how customers in your target segments actually buy
- **Also feeds**: `budget-allocator` (market size informs spend levels), `position-lock` (segment dynamics shape positioning)
- **Enhanced by**: Run after `whitespace-finder` (size the specific opportunities discovered)
