---
name: signal-radar
description: 'Continuous macro-market signal detection and classification engine that surfaces emerging trends, threats, and whitespace opportunities. Use when: market signals, market intelligence, trend analysis, emerging threats, market monitoring, what is changing in our market.'
---

# Signal Radar (PULSE Framework)

Detect, classify, and score macro-market signals before competitors act. Surfaces technology shifts, regulatory changes, buyer behavior evolution, and ecosystem dynamics.

## When to Use
- Quarterly strategic planning
- Pre-launch market assessment
- Competitive threat monitoring
- New market entry evaluation
- Board-level market briefings

## What You'll Need
**Critical inputs (ask if not provided):**
- Industry/market to monitor
- Product category or domain
- Known competitors (top 3-5)

**Nice-to-have:**
- Recent analyst reports or news
- Internal customer feedback themes
- Current strategic priorities

## Process

### Step 1: Signal Collection
Classify every market signal into 5 vectors:

| Vector | What It Tracks | Examples |
|--------|---------------|----------|
| **T-Signals** (Technology) | New protocols, platforms, standards, AI capabilities | "New foundation model released", "New API standard adopted" |
| **R-Signals** (Regulatory) | Compliance mandates, policy changes, industry standards | "GDPR enforcement update", "AI regulation passed" |
| **B-Signals** (Buyer behavior) | Purchasing patterns, channel preferences, budget shifts | "Buyers demanding self-serve trials", "CFO approval now required" |
| **E-Signals** (Ecosystem) | Partner moves, supply chain changes, platform updates | "Company A acquires competitor", "Company B launches competing service" |
| **C-Signals** (Cultural) | Workforce trends, social attitudes, macro-economic shifts | "Remote work permanent", "AI trust concerns rising" |

For each signal found, document:
- Signal description (what happened)
- Source and date
- Vector classification (T/R/B/E/C)
- Initial relevance assessment

### Step 2: PULSE Scoring
Score each signal on 5 dimensions (1-10):

| Dimension | What It Measures | Scoring Guide |
|-----------|-----------------|---------------|
| **P**attern | Is this a one-off or repeating pattern? | 1=isolated event, 5=emerging trend, 10=established pattern |
| **U**rgency | Time horizon before impact | 1=years away, 5=6-12 months, 10=imminent (under 3 months) |
| **L**everage | How much can we exploit this? | 1=no fit, 5=moderate advantage, 10=perfect strategic fit |
| **S**cope | How many segments/geos affected? | 1=niche, 5=our core market, 10=entire industry |
| **E**vidence | Quality of supporting data | 1=rumor, 5=multiple credible sources, 10=confirmed with data |

**PULSE Composite** = (P x 0.15) + (U x 0.25) + (L x 0.25) + (S x 0.15) + (E x 0.20)

**Classification:**
- 7.5+ = **Critical Watch** (act now or prepare immediately)
- 5.0-7.4 = **Monitor** (track weekly, prepare contingencies)
- Below 5.0 = **Archive** (log for future reference)

### Step 3: Convergence Mapping
Overlay all Critical Watch signals to find convergence zones:
- Where do 3+ signals from DIFFERENT vectors intersect?
- Convergence zones represent the highest-opportunity (or highest-threat) areas
- Document each convergence with the contributing signals and the combined implication

### Step 4: Implication Chains
For each Critical Watch signal, trace cascading effects:
- **1st order**: Direct impact on our market/product
- **2nd order**: How customers/competitors will respond
- **3rd order**: New opportunities or threats that emerge from responses

Format: IF [signal] THEN [1st order] THEREFORE [2nd order] WHICH MEANS [3rd order]

## Output
Save to `outputs/signal-radar-[YYYY-MM-DD].md`

### Deliverables:
1. **Signal Dashboard**: Table of all signals with PULSE scores, sorted by composite score, with trend arrows
2. **Convergence Map**: Visual overlay showing where multiple vectors intersect, highlighting whitespace or threat zones
3. **Implication Chains**: For each Critical Watch signal, the IF-THEN-THEREFORE chain
4. **Executive Summary**: 1-page brief with "Act Now / Prepare / Watch" categorization

## Chain Connections
- **Next skill**: Run `whitespace-finder` with these signals to discover specific product opportunities
- **Also feeds**: `battle-scanner` (signals inform competitive threat landscape), `demand-engine` (signals identify timing windows)
- **Enhanced by**: Run after `jtbd-extractor` to overlay customer jobs onto signal analysis
