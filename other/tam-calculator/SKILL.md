---
name: tam-calculator
description: Calculate TAM, SAM, and SOM for new market segments using top-down and bottom-up methods
tags: [strategy, market-sizing, tam, sam, som, research, planning]
---

# TAM Calculator

Calculates Total Addressable Market (TAM), Serviceable Addressable Market (SAM), and Serviceable Obtainable Market (SOM) for new market segments. Uses both top-down (industry reports, macro data) and bottom-up (unit economics, customer counts) methods, then triangulates the results. Identifies data sources, estimates growth rates, and outputs a market sizing report with full methodology. Useful for evaluating new service lines, geographic expansion, or segment targeting decisions.

## Prerequisites

- `agency.config.json` at repo root with `agency`, `services`, `icp`, and `case_studies` sections
- Target market definition (at minimum: industry + geography + service type)
- WebSearch tool available for market research
- Optional: known data points (current revenue, customer count, average deal size)

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `agency.name` -- for contextualization
   - `services[]` -- to understand the agency's current capabilities
   - `icp.segments[]` -- existing market segments for comparison
   - `case_studies[]` -- for average deal size and revenue benchmarks
3. Accept parameters:
   - `market_definition` -- (required) the target market to size. Object with:
     - `industry` -- target industry (e.g., "D2C ecommerce", "SaaS", "healthcare")
     - `geography` -- target region(s): country, region, or global
     - `service` -- the specific service to size for (e.g., "Shopify CRO", "performance marketing")
     - `company_size` -- target company size range (e.g., "11-200 employees", "$1M-$50M revenue")
   - `known_data` -- (optional) any data points the user already has:
     - `current_revenue` -- agency's current annual revenue
     - `current_customers` -- number of active clients
     - `avg_deal_size` -- average annual revenue per client
     - `win_rate` -- percentage of proposals that close
     - `market_share_estimate` -- rough current market share percentage
   - `growth_horizon` -- years to project. Default: 3
   - `confidence_level` -- `conservative`, `moderate`, `aggressive`. Default: `moderate`

## Phase 1: Market Definition Refinement

Precisely define the market boundaries before sizing. Ambiguity here cascades into unreliable numbers.

**Define each boundary explicitly:**

| Boundary | Question | Example |
|----------|----------|---------|
| Industry | What vertical exactly? | "D2C ecommerce brands on Shopify" not "ecommerce" |
| Geography | Which countries/regions? | "India, US, UK, AU" not "global" |
| Company size | Revenue range? Employee count? | "$500K-$50M annual revenue, 11-200 employees" |
| Service scope | What specific service? | "Shopify CRO and optimization" not "marketing services" |
| Platform | Any platform constraint? | "Shopify only" vs "all ecommerce platforms" |
| Maturity | Stage of company? | "Post-PMF, Series A-C" not "all startups" |

**Exclusions (what is NOT in this market):**
- List specific exclusions: enterprise (500+ employees), pre-revenue, non-English markets, etc.
- Clarity on exclusions prevents inflated numbers

Compile:
```
MARKET DEFINITION:
---
Industry: [specific]
Geography: [countries/regions]
Company size: [range]
Service: [specific service]
Platform: [constraint or "any"]
Maturity: [stage]
Exclusions: [list]
---
```

## Phase 2: Top-Down Sizing

Start from the total market and narrow down. This approach uses industry reports, analyst data, and macro statistics.

**Step 1: Total industry size**

Use WebSearch to find:
- `"{{industry}}" market size {{current_year}} report`
- `"{{industry}}" TAM billion {{geography}}`
- `"{{industry}}" global market value`
- `Shopify merchant count {{current_year}}`
- `"{{geography}}" ecommerce market size`

Record:
- Source name and date
- Total market figure
- Currency
- What the figure includes (important: does it cover your service or the entire industry?)

**Step 2: Apply segmentation filters**

Narrow the total market using each boundary defined in Phase 1:

```
Total industry market: $X
  x Geography filter: [% of global market in target region] = $Y
  x Company size filter: [% of companies in target size range] = $Z
  x Platform filter: [% on target platform] = $A
  x Service relevance: [% who need this specific service] = $B
---
TAM (top-down): $B
```

**Step 3: SAM calculation**

From TAM, apply the agency's reach constraints:
- Language: what % can the agency serve given language capabilities?
- Pricing: what % can afford the agency's pricing tier?
- Channel access: what % can the agency reach through its channels?

```
TAM: $B
  x Language reach: [%]
  x Pricing tier fit: [%]
  x Channel access: [%]
---
SAM (top-down): $C
```

**Step 4: SOM calculation**

From SAM, apply competitive and capacity constraints:
- Competitive intensity: how many competitors serve this segment?
- Win rate: historical or estimated close rate
- Capacity: how many clients can the agency handle?

```
SAM: $C
  x Realistic capture rate (based on competition + capacity): [%]
---
SOM (top-down): $D
```

**Document every assumption and filter percentage with reasoning.**

## Phase 3: Bottom-Up Sizing

Build from unit economics upward. This approach is grounded in the agency's actual numbers.

**Step 1: Count target companies**

Use WebSearch and data sources to estimate the total number of companies matching the market definition:

- `number of Shopify stores in {{geography}} {{current_year}}`
- `"{{industry}}" companies {{geography}} {{company_size_range}}`
- Apollo.io data (if `tools.lead_enrichment` is configured): search the ICP segment and note total results
- LinkedIn search data: companies matching industry + size + geography
- Government business registries, industry association data

Record multiple sources and triangulate:
```
COMPANY COUNT ESTIMATES:
Source 1 ([name]): [number]
Source 2 ([name]): [number]
Source 3 ([name]): [number]
---
Triangulated estimate: [number]
Confidence: [low/medium/high]
```

**Step 2: Estimate serviceable percentage**

Not all counted companies are potential customers:
- What % actually need this service? (vs. handling in-house or not a priority)
- What % have budget for external services?
- What % are not already locked into competitors?

```
Total companies: [N]
  x Need service: [%]
  x Have budget: [%]
  x Accessible (not locked in): [%]
---
Serviceable companies: [M]
```

**Step 3: Apply unit economics**

```
Serviceable companies: [M]
  x Average deal size (annual): $[avg_deal]
---
TAM (bottom-up): $[M * avg_deal]
```

For SAM:
```
TAM (bottom-up): $[X]
  x Reachable through agency's channels: [%]
---
SAM (bottom-up): $[Y]
```

For SOM:
```
SAM (bottom-up): $[Y]
  x Expected win rate: [%]
  x Capacity constraint (max clients/year): [N clients * avg_deal]
---
SOM (bottom-up): $[Z]
```

## Phase 4: Triangulation

Compare top-down and bottom-up results. Discrepancies reveal blind spots.

**Analysis:**

| Metric | Top-Down | Bottom-Up | Variance | Notes |
|--------|----------|-----------|----------|-------|
| TAM | $X | $Y | [%] | [explain variance] |
| SAM | $X | $Y | [%] | [explain variance] |
| SOM | $X | $Y | [%] | [explain variance] |

**If variance > 50%:**
- Identify which assumptions drive the gap
- Research the gap: is top-down inflated (common) or bottom-up too conservative?
- State the final estimate as a range with confidence level

**Final estimates:** use a weighted average, typically bottom-up-weighted (60/40) for agency-scale businesses where unit economics are more reliable than industry macro data.

```
FINAL MARKET SIZING:
---
TAM: $[range] (confidence: [level])
SAM: $[range] (confidence: [level])
SOM: $[range] (confidence: [level])
---
```

## Phase 5: Growth Projections

Project the market forward using available growth data.

**Growth rate estimation:**

1. **Historical growth**: search for CAGR data on the target industry
   - `"{{industry}}" CAGR {{current_year}} forecast`
   - `"ecommerce" growth rate {{geography}}`

2. **Leading indicators**: signals that the market is accelerating or decelerating
   - New company formation rate in the industry
   - VC funding trends in the vertical
   - Platform growth (Shopify merchant growth rate)
   - Job posting trends (are companies hiring for roles the agency supports?)

3. **Apply growth scenarios:**

| Scenario | Growth Rate | Assumption |
|----------|-------------|-----------|
| Conservative | [X%] CAGR | Market matures, competition increases |
| Moderate | [Y%] CAGR | Current trends continue |
| Aggressive | [Z%] CAGR | Tailwinds accelerate (new regulation, tech shift, etc.) |

**Projection table:**

| Year | TAM | SAM | SOM | Notes |
|------|-----|-----|-----|-------|
| Current | $X | $Y | $Z | Baseline |
| +1 | | | | |
| +2 | | | | |
| +3 | | | | |

## Phase 6: Competitive Landscape

Map the competitive dynamics within the sized market.

**Competitor categories:**

| Category | Description | Market Share Est. |
|----------|-------------|-------------------|
| Large agencies | Full-service, premium pricing | [%] |
| Niche specialists | Focused on specific platform/service | [%] |
| Freelancers/solopreneurs | Individual experts | [%] |
| In-house teams | Companies who do not outsource | [%] |
| Unserved | Companies with unmet need | [%] |

**Agency positioning:**
- Where does the agency fit in these categories?
- What is the realistic capture potential given positioning?
- Which competitor category is the primary displacement target?

## Phase 7: Strategic Implications

Translate the numbers into actionable insights.

**Market entry assessment:**

| Factor | Rating (1-10) | Notes |
|--------|--------------|-------|
| Market size attractiveness | | Is SOM large enough to be worth pursuing? |
| Growth trajectory | | Is the market growing fast enough? |
| Competition intensity | | How crowded is the space? |
| Agency capability fit | | Does the agency have the skills? |
| Go-to-market feasibility | | Can the agency reach this market? |
| Revenue per client | | Does the unit economics work? |

**Recommendations:**
- Enter this market? (yes/no with reasoning)
- If yes: priority level (primary, secondary, experimental)
- Suggested go-to-market approach
- Key risks and mitigation strategies
- Resource requirements (team, tools, budget)

## Phase 8: Output

Return structured JSON:

```json
{
  "market_definition": {
    "industry": "D2C ecommerce brands on Shopify",
    "geography": ["India", "US", "UK", "AU"],
    "company_size": "11-200 employees, $500K-$50M revenue",
    "service": "Shopify CRO and optimization",
    "platform": "Shopify",
    "exclusions": ["enterprise 500+", "pre-revenue"]
  },
  "sizing": {
    "tam": {
      "top_down": {"value": 2400000000, "currency": "USD", "methodology": "..."},
      "bottom_up": {"value": 1800000000, "currency": "USD", "methodology": "..."},
      "final": {"value_range": [1800000000, 2400000000], "midpoint": 2100000000, "confidence": "moderate"}
    },
    "sam": {
      "top_down": {"value": 340000000, "currency": "USD"},
      "bottom_up": {"value": 280000000, "currency": "USD"},
      "final": {"value_range": [280000000, 340000000], "midpoint": 310000000, "confidence": "moderate"}
    },
    "som": {
      "top_down": {"value": 5200000, "currency": "USD"},
      "bottom_up": {"value": 4800000, "currency": "USD"},
      "final": {"value_range": [4800000, 5200000], "midpoint": 5000000, "confidence": "moderate"}
    }
  },
  "unit_economics": {
    "total_target_companies": 45000,
    "serviceable_companies": 8500,
    "avg_deal_size_annual": 36000,
    "expected_win_rate": 0.15,
    "max_clients_per_year": 15
  },
  "growth_projections": {
    "cagr_scenarios": {
      "conservative": 0.08,
      "moderate": 0.14,
      "aggressive": 0.22
    },
    "projections": [
      {"year": "current", "tam": 2100000000, "sam": 310000000, "som": 5000000},
      {"year": "+1", "tam": 2394000000, "sam": 353400000, "som": 5700000},
      {"year": "+2", "tam": 2729160000, "sam": 402876000, "som": 6498000},
      {"year": "+3", "tam": 3111242400, "sam": 459278640, "som": 7407720}
    ]
  },
  "competitive_landscape": {
    "competitor_categories": [
      {"category": "Large agencies", "market_share": 0.25, "threat_level": "medium"},
      {"category": "Niche specialists", "market_share": 0.20, "threat_level": "high"},
      {"category": "Freelancers", "market_share": 0.15, "threat_level": "low"},
      {"category": "In-house", "market_share": 0.30, "threat_level": "low"},
      {"category": "Unserved", "market_share": 0.10, "threat_level": "none"}
    ],
    "agency_positioning": "Niche specialist targeting mid-market D2C on Shopify"
  },
  "data_sources": [
    {"source": "Shopify annual report 2025", "data_point": "Merchant count", "reliability": "high"},
    {"source": "Statista ecommerce report", "data_point": "Market size by geography", "reliability": "high"},
    {"source": "Apollo.io search results", "data_point": "Company count in segment", "reliability": "medium"}
  ],
  "assumptions": [
    {"assumption": "30% of Shopify merchants in the size range need external CRO help", "impact": "high", "confidence": "medium"},
    {"assumption": "Average deal size of $36K/year based on agency pricing", "impact": "high", "confidence": "high"}
  ],
  "strategic_recommendation": {
    "enter_market": true,
    "priority": "primary",
    "reasoning": "SOM of $5M is achievable within 2 years given current trajectory. Market is growing at 14% CAGR with an underserved mid-market segment.",
    "key_risks": ["Competition from freelancers on price", "Market concentration in top 3 agencies"],
    "next_steps": ["Validate with 10 prospect conversations", "Build case study in target segment", "Launch targeted content campaign"]
  }
}
```

## Phase 9: Review

Present the market sizing to the user:

1. Show the market definition with boundaries
2. Present TAM/SAM/SOM with both top-down and bottom-up figures
3. Highlight the triangulation and explain any variance
4. Show growth projections across scenarios
5. Present competitive landscape
6. Share strategic recommendation
7. List all assumptions with confidence levels
8. List all data sources with reliability ratings
9. Ask if any assumptions need adjustment

After approval, optionally:
- Feed into `icp-builder` to refine the ICP for the new segment
- Feed into `blog-researcher` to identify content opportunities in the new market
- Feed into `signal-scanner` to start prospecting in the new segment

## Example Usage

Trigger phrases:
- "Size the market for Shopify CRO in India"
- "Calculate TAM for our services in the US D2C market"
- "How big is the opportunity for performance marketing for D2C brands?"
- "Should we expand into the UK market? Size it for me."
- "What is the TAM for Shopify development in Australia?"
- "Calculate market size for a new service line"

```
User: Size the market for Shopify CRO services targeting D2C brands in India and the US
Assistant: [reads config, defines market boundaries, runs top-down analysis with industry data, runs bottom-up with company counts and unit economics, triangulates, projects growth, maps competition, returns full report with strategic recommendation]
```

```
User: Should we add performance marketing as a service? What is the market opportunity?
Assistant: [reads config, sizes the performance marketing market for existing ICP segments, compares unit economics to current CRO service, projects growth, assesses capability gap, returns recommendation with market sizing]
```
