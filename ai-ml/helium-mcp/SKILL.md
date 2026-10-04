---
name: helium-mcp
description: Search real-time news with bias scoring, get live stock/ETF/crypto data with AI analysis, price options with ML models, and synthesize balanced news perspectives via the Helium MCP server.
compatibility:
  use-case: Market research, news analysis, trading research, media literacy
  frameworks: Helium MCP, financial data APIs, news aggregation
---

# Helium MCP — News, Markets & AI Intelligence

## Use This Skill When

- Searching current news or specific topics
- Analyzing media bias across news sources
- Getting real-time stock, ETF, or crypto prices
- Understanding market sentiment and forecasts
- Pricing options contracts with ML models
- Discovering trending topics across media
- Finding balanced perspectives on controversial topics
- Researching memes and internet culture trends

## When NOT to Use

- Historical financial data (no backtesting)
- Personal investment advice (informational only)
- Real-time trading execution (data only)
- Non-public information (legal/compliance issues)

## Context: Research Intelligence Maturity

**Undeveloped**: Single news source, no bias awareness, manual searching.

**Target**: Multi-source searches with bias scores, balanced perspective synthesis, live market data.

**Optimized**: AI-ranked trading strategies, predictive scenarios, automated watchlists, integrated portfolio analysis.

## Core Principle

**Intelligence comes from multiple perspectives with bias context.** News sources have inherent bias (political, emotional, prescriptive) — understanding that bias enables better decision-making. Market data without context is incomplete.

## Instructions

### Step 1: Configure Helium MCP Server

**Add to MCP settings file** (e.g., `~/.config/Claude/mcp_servers.json`):

```json
{
  "mcpServers": {
    "helium": {
      "url": "https://heliumtrades.com/mcp"
    }
  }
}
```

**Free tier**: 50 queries per day, no signup/API key required.

### Step 2: Search News with Bias Analysis

**Basic news search:**
```
Search: "artificial intelligence regulation"
Returns: 50 most relevant articles with bias scores
```

**Multi-dimensional bias scores include:**
- Political lean (left/center/right)
- Emotionality (factual vs. sensational)
- Factfulness (evidence-based vs. opinion)
- Prescriptiveness (descriptive vs. prescriptive)
- Sensationalism level

**Interpret results:**

```markdown
## News Search Results: "AI Regulation"

### Top Articles (sorted by relevance)

1. **"EU Passes AI Act Requirements"** — Reuters
   - Political Lean: Center (bias score: 0.0)
   - Emotionality: Low (very factual)
   - Factfulness: High (evidence-based)
   - Source Reliability: 9.2/10
   - Date: April 26, 2026
   - URL: [link]

2. **"AI Regulation Will Destroy Innovation"** — TechCrunch
   - Political Lean: Right (bias score: 0.6)
   - Emotionality: High (opinion-heavy)
   - Factfulness: Medium (some opinion)
   - Sensationalism: 6.5/10
   - URL: [link]

3. **"Tech Companies Lobby Against AI Rules"** — CNN
   - Political Lean: Center-Left (bias score: -0.3)
   - Emotionality: Medium
   - Factfulness: Medium
   - URL: [link]

### Bias Comparison
- Reuters: Most neutral and factual ✓
- CNN: Slightly left-leaning, emotional
- TechCrunch: Right-leaning, sensational
```

### Step 3: Get Balanced News Synthesis

**Request AI-synthesized perspective:**
```
get_balanced_news query: "Should tech companies pay taxes?"
```

**Output includes:**
- Left-leaning perspective summary
- Center/neutral perspective
- Right-leaning perspective
- Synthesis identifying common ground
- Key disagreement points

**Example:**

```markdown
## Balanced Perspective: "Tech Company Taxation"

### Left-leaning View
"Tech giants exploit tax loopholes to avoid paying fair share. 
Closing loopholes is necessary for infrastructure funding."

### Center/Neutral View
"Complex tax rules create challenges; need to balance revenue with 
avoiding business flight. International coordination improving."

### Right-leaning View
"Lower corporate taxes drive innovation and job creation. 
Aggressive taxation discourages business investment."

### Common Ground
- Complex tax system needs modernization
- Balance needed between revenue and business health
- International coordination increasing

### Key Disagreements
- Fairness vs. growth priority
- Government revenue needs
- Effectiveness of tax enforcement
```

### Step 4: Analyze Media Sources

**Get bias profile for a specific source:**
```
get_source_bias source: "Fox News"
```

**Returns:**

```markdown
## Fox News — Bias Profile

**Overall Lean**: Right (0.7/1.0)
**Factfulness**: 6.2/10 (Mixed)
**Sensationalism**: 7.1/10 (High)
**Emotional Tone**: Often passionate

**Typical Patterns**:
- Emphasis on conservative policy positions
- Skepticism of progressive initiatives
- Personality-driven opinion shows mixed with news
- Covers stories emphasizing government overreach

**Reliability**: 6.4/10 (Mixed; opinion-heavy content)

**Use for**: Understanding conservative perspective; 
note that opinion shows (high bias) mix with news reports.
```

### Step 5: Get Real-Time Market Data

**Get ticker data with AI analysis:**
```
get_ticker ticker: "AAPL"  # Apple stock
```

**Returns:**

```markdown
## Apple Inc. (AAPL)

**Current Price**: $185.42
**52-Week Range**: $128.50 - $189.95
**P/E Ratio**: 32.1

### AI-Generated Bull Case
"Strong services revenue growth, installed base expansion, 
upcoming product cycles could drive stock higher."

### AI-Generated Bear Case  
"High valuation relative to earnings; China demand uncertainty; 
tech sector regulatory risks."

### Probability-Weighted Scenarios (30-day forecast)

| Scenario | Probability | Target | Rationale |
|----------|-------------|--------|-----------|
| 🟢 Strong momentum | 25% | $195 | Services growth, product cycle |
| 🟡 Consolidation | 45% | $180-185 | Macro uncertainty, valuation |
| 🔴 Correction | 20% | $165 | Tech selloff, China weakness |
| 💥 Black swan | 10% | $150 | Regulatory shock, recession |

**Expected Value**: $183 (probability-weighted)
```

### Step 6: Price Options with ML Models

**Get ML-predicted option value:**
```
get_option_price symbol: "AAPL" strike: 180 expiration: "2026-05-16" side: "CALL"
```

**Returns:**

```markdown
## AAPL Call Option Analysis

**Contract**: AAPL $180 Call (May 16, 2026)

**ML Predictions**:
- Fair Value: $7.82
- Probability ITM: 78.3%
- Breakeven Stock Price: $187.82

**Current Market**:
- Bid: $7.50
- Ask: $8.25
- Implied Volatility: 22%

**Assessment**:
✓ Option is fairly priced (market $7.88 vs. ML $7.82)
✓ High probability ITM (78%)
⚠️ Limited edge if buying now

**Greeks**: Delta 0.78 | Gamma 0.02 | Theta 0.08/day | Vega 0.34
```

### Step 7: Find Top Trading Strategies

**Get AI-ranked options strategies:**
```
get_top_trading_strategies symbol: "SPY" outlook: "neutral"
```

**Returns:**

```markdown
## Top Neutral Strategies for SPY

### Rank 1: Iron Condor (SPY 440/445/455/460)
- **Max Profit**: $300 (if SPY stays between 445-455)
- **Max Loss**: $200
- **Probability Success**: 68%
- **Risk/Reward**: 1:1.5 favorable
- **Ideal Market**: Low volatility, range-bound

### Rank 2: Short Straddle (SPY 450 strike)
- **Max Profit**: $400 (if SPY exactly at 450)
- **Max Loss**: Unlimited (IV crush risk)
- **Probability Success**: 52%
- **Ideal Market**: Expect mean reversion

### Rank 3: Call Spread (450/455)
- **Max Profit**: $200
- **Max Loss**: $300
- **Probability Success**: 60%
- **Ideal Market**: Slight bullish bias
```

## Common Queries

| Use Case | Query |
|----------|-------|
| **Bias check** | `search_news` + `get_source_bias` |
| **Balanced view** | `search_balanced_news` on controversial topic |
| **Stock research** | `get_ticker` then `get_option_price` for key strikes |
| **Trading ideas** | `get_top_trading_strategies` for your outlook |
| **Trending topics** | `get_trending_topics` |

## Output

**Deliver:**

1. **News Search Results** (ranked by relevance, bias scores highlighted)
2. **Bias Analysis** (which sources align, which diverge)
3. **Market Data** (current price + scenarios + AI analysis)
4. **Option Pricing** (fair value + probability + Greeks)
5. **Trading Strategies** (ranked by risk/reward for your outlook)