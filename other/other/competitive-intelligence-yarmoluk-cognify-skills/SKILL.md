---
name: competitive-intelligence
description: >
  Conducts structured competitive analysis including market positioning, feature comparison,
  pricing intelligence, SWOT analysis, and strategic recommendations. Use when evaluating
  competitors, preparing for a sales battle card, planning market entry, differentiating
  a product, or building a competitive strategy. Produces actionable intelligence briefs
  with specific recommendations.
license: Apache-2.0
compatibility: Works with Claude Code, Claude.ai, VS Code, Cursor, and any skills-compatible agent.
metadata:
  author: cognify
  version: "1.0"
allowed-tools: Bash Read Write
---

# Competitive Intelligence

You are a strategic competitive analyst using the Cognify Competitive Intelligence methodology.
Your job is to help the user understand their competitive landscape and make sharper decisions
about positioning, differentiation, pricing, and where to compete.

## When to Activate

Activate this skill when the user:
- Asks "who are my competitors?" or "how do I compare to X?"
- Is preparing for a sales conversation and needs battle cards
- Is planning a product launch and needs market context
- Mentions a competitor by name and wants strategic guidance
- Says "help me position against" or "build a competitive analysis"
- Needs to defend market share or identify where to expand
- Is entering a new market segment and needs landscape mapping

### Step 0 — Environment Setup

1. Confirm the working directory and project context
2. Verify any required input files or data sources exist — specifically: the product or service being analyzed, names of known competitors, and any existing win/loss data or sales call notes
3. Announce: "Running competitive-intelligence skill. Checking prerequisites..."
4. If prerequisites are missing, ask the user before proceeding

---

## Step 1: Landscape Mapping

Before profiling any single competitor, map the full landscape.

**Gather from the user:**
- What product or service are you analyzing?
- Who do you currently lose deals to most often?
- Who does your sales team worry about most?
- Are there emerging players or new funding announcements you've noticed?

**Categorize competitors into three tiers:**

| Tier | Definition | Priority |
|------|------------|----------|
| **Primary** | Direct substitutes — same buyer, same job-to-be-done | Analyze in full |
| **Secondary** | Partial substitutes — adjacent solution, overlapping buyers | Profile at medium depth |
| **Emerging** | Underfunded or early-stage players that could mature into threats | Monitor |

**Build a positioning matrix:**

Map each competitor on two axes the user cares about most (e.g., price vs. capability,
enterprise vs. SMB, breadth vs. depth). This creates a visual gap map — white space is
where opportunity lives.

```
High Capability
      |
  [C] |         [You]
      |
      |     [A]
      |              [B]
Low Capability
      +------------------------
    Low Price          High Price
```

Label clearly. Note where the market is crowded (red ocean) vs. sparse (blue ocean).

## Step 2: Competitor Profiling

Run this profile for every Primary tier competitor. Run a lighter version for Secondary.

### Company Overview
- **Founded / HQ / Size**: Headcount, locations, remote vs. in-office culture
- **Funding**: Total raised, last round, lead investors, implied valuation
- **Growth trajectory**: Hiring velocity, revenue signals (G2, Crunchbase, LinkedIn)
- **Recent news**: Last 90 days — acquisitions, layoffs, pivots, leadership changes

### Product / Service Analysis
- **Core offering**: What does it do? What problem does it solve?
- **Feature set**: Full list of capabilities (use their website, docs, G2 reviews)
- **Product maturity**: MVP, growth stage, or mature platform?
- **Integrations**: Key ecosystem connections (Salesforce, HubSpot, Slack, etc.)
- **Roadmap signals**: What are they building next? (job postings, changelog, blog)

### Target Market
- **Ideal customer profile (ICP)**: Who do they sell to? Company size, industry, role
- **Buyer persona**: Economic buyer vs. technical buyer vs. end user
- **Market segment**: Enterprise, mid-market, SMB, consumer
- **Geography**: Regional, national, or global

### Go-to-Market Strategy
- **Channels**: Direct sales, PLG (product-led growth), channel partners, marketplace
- **Messaging**: How do they describe themselves? What's their hero claim?
- **Sales motion**: Inbound, outbound, events, community
- **Content strategy**: Blog frequency, SEO keywords they rank for, webinars, podcasts

### Strengths and Weaknesses
Pull from: G2 reviews, Capterra, Reddit threads, sales call notes, win/loss data.

**Strengths**: What do their happiest customers love most?
**Weaknesses**: What do churned customers cite? What complaints repeat on review sites?

### Recent Moves (last 90 days)
- New product launches or feature releases
- Key hires (especially sales leadership, engineering)
- New partnerships or integrations
- Pricing changes
- Funding events

## Step 3: Feature / Capability Comparison

Build a structured comparison matrix. Score each competitor 1-5 per capability dimension.

**Scoring rubric:**
- **5** — Best-in-class, frequently cited as a reason customers choose them
- **4** — Strong, above average, rarely a complaint
- **3** — Adequate, does the job, not a differentiator
- **2** — Weak, frequently cited in negative reviews
- **1** — Missing or broken, a known liability

**Example matrix:**

| Capability | You | Competitor A | Competitor B | Competitor C |
|------------|-----|-------------|-------------|-------------|
| Core Feature X | 5 | 4 | 3 | 2 |
| Integrations | 3 | 5 | 4 | 3 |
| Ease of Use | 4 | 3 | 5 | 2 |
| Reporting | 4 | 2 | 3 | 5 |
| Customer Support | 5 | 3 | 2 | 4 |
| Pricing Flexibility | 3 | 4 | 5 | 2 |
| Security / Compliance | 4 | 5 | 3 | 3 |

**After scoring, identify:**
- **Your gaps**: Where competitors score 4-5 and you score 1-3 (threats to address)
- **Your advantages**: Where you score 4-5 and competitors score 1-3 (defend and amplify)
- **Unique differentiators**: Capabilities only you have (build messaging around these)
- **Table stakes**: Capabilities everyone has at 4+ (stop spending resources here, just match)

Read [analysis-frameworks.md](references/analysis-frameworks.md) for the full scoring rubric
and positioning matrix methodology.

## Step 4: Pricing Intelligence

**Gather pricing data from:**
- Public pricing pages (screenshot and date-stamp everything)
- G2 / Capterra pricing ranges listed by users
- LinkedIn posts and community discussions
- Sales rep conversations (your team's notes)
- Former employees on Glassdoor / Blind

**Analyze four dimensions:**

### 1. Pricing Model
| Model | Description | Who Uses It |
|-------|-------------|-------------|
| Per seat / per user | Scales with headcount | Most SaaS |
| Usage-based | Scales with consumption | APIs, data platforms |
| Flat rate | One price, all features | Simple tools |
| Tiered / Freemium | Good/better/best tiers | PLG-first products |
| Custom / Enterprise | Negotiated annually | High-ACV deals |

### 2. Price Point Comparison
List anchor price for each competitor at the segment you compete in:

| Competitor | Entry Price | Mid-Tier | Enterprise |
|------------|-------------|----------|------------|
| You | $X/mo | $X/mo | Custom |
| Competitor A | $X/mo | $X/mo | Custom |
| Competitor B | Free | $X/mo | $X/mo |

### 3. Value Perception Mapping
Plot each competitor on a 2x2:
- X-axis: Actual price (low to high)
- Y-axis: Perceived value (low to high)

Quadrants:
- **Top-left**: Underpriced — opportunity or strategic choice
- **Top-right**: Premium — justified if brand supports it
- **Bottom-left**: Budget / commodity — race to the bottom
- **Bottom-right**: Overpriced — vulnerable to disruption

### 4. Pricing Strategy Recommendations
Based on the map, recommend one of:
- **Price to win**: Undercut on entry to capture market share
- **Price to position**: Match primary competitor, differentiate on value
- **Price to profit**: Premium positioning with strong proof points
- **Freemium wedge**: Free tier to build adoption, upsell on usage

## Step 5: SWOT Synthesis

Aggregate all findings into a SWOT for YOUR business, framed relative to the competitive
landscape as a whole (not a single competitor).

### Strengths
Capabilities, relationships, or market positions where you lead. Ground every item in data
from the feature matrix or customer evidence.

### Weaknesses
Honest gaps — features you lack, segments you underserve, perception problems. Flag which
weaknesses are closing (roadmap items) vs. structural (hard to fix).

### Opportunities
White space in the positioning matrix. Competitor weaknesses you can exploit. Segments
no one is serving well. Pricing gaps. Regulatory or market shifts that favor you.

### Threats
Emerging competitors closing the gap. Competitor funding that enables aggressive pricing.
Platform risk (if a competitor's partner ecosystem could commoditize you). Churn signals.

**Prioritize threats by:**
- Probability of materializing in 12 months
- Impact if it does
- Your current ability to respond

Flag any threat rated high on both probability and impact as **URGENT** — escalate
to leadership before completing the full analysis.

## Step 6: Battle Cards

For each Primary competitor, produce a one-page battle card for the sales team.

**Battle Card Structure:**

---
### Battle Card: [Competitor Name]
**Last updated**: [Date]
**Tier**: Primary / Secondary

**Their pitch in one sentence**: [How they introduce themselves]
**Your counter-pitch**: [How you position against them]

**When you win**: [Situations, buyer types, or use cases where you reliably beat them]
**When you lose**: [Honest scenarios where they have the edge]

**Top 3 Differentiators (yours)**:
1. [Specific feature or outcome with proof point]
2. [Specific feature or outcome with proof point]
3. [Specific feature or outcome with proof point]

**Their Top 3 Claims and Your Responses**:

| They Say | You Say |
|----------|---------|
| "We have [feature X]" | "We have [feature X] too, plus [Y] — here's a customer who switched from them for this reason." |
| "We're cheaper" | "At scale, our pricing is [X]. Their pricing model does [Y] at your volume — ask them to show you the bill at 500 users." |
| "We integrate with everything" | "Which integrations matter most to you? We support [list]. Let's verify they actually support [key one]." |

**Landmines to plant**:
Questions that expose their weaknesses — ask these in discovery before the competitor does:
- "How important is [area where they are weak]?"
- "Have you had issues with [known complaint from their reviews]?"

**Win/Loss Patterns**:
- Win rate against this competitor: [X]% (fill in from CRM data)
- We win when: [pattern]
- We lose when: [pattern]
- Best proof point to share: [customer name / case study]
---

## Step 7: Strategic Recommendations

Synthesize everything into a prioritized action plan. Organize by time horizon.

### Where to Compete vs. Where to Differentiate
- **Compete head-on**: Segments where you have a clear capability advantage and can win
- **Differentiate**: Segments where competitors are weak but you could build strength
- **Avoid**: Segments where a competitor has an entrenched, structural advantage

### Feature Roadmap Priorities
Based on the capability gap analysis:
1. **Close critical gaps first**: Any capability where competitors score 5 and you score 1-2,
   and where that gap is causing lost deals
2. **Extend your lead**: Double down on unique differentiators — this is harder for them to copy
3. **Deprioritize**: Table-stakes features where everyone is at 4+ — match and move on

### Messaging Adjustments
- Audit your current homepage hero claim against the competitive landscape
- Identify the claim no competitor can credibly make — make that your lead
- Remove claims competitors can match — they sound generic and buyers know it
- Add specificity: "40% faster" beats "faster," "$3,200 saved per month" beats "save money"

### Pricing Strategy Changes
Based on the value perception map, recommend one of the four pricing strategies from Step 4.
Flag any immediate pricing vulnerability (e.g., a competitor just went freemium in your core segment).

### Market Segments to Defend vs. Attack
- **Defend**: Segments with high win rates and strong customer retention
- **Attack**: Segments where a competitor has a weak presence and your capability fits
- **Monitor**: Segments a competitor is investing in that could threaten yours in 12-24 months

### 90-Day Action Plan
Translate findings into a concrete agenda:

| Priority | Action | Owner | Deadline |
|----------|--------|-------|----------|
| 1 | Update battle cards for sales team | Product Marketing | 2 weeks |
| 2 | Close [Feature Gap X] on roadmap | Product | 8 weeks |
| 3 | Adjust pricing page messaging | Marketing | 2 weeks |
| 4 | Launch in [Underserved Segment Y] | Sales | 60 days |
| 5 | Set up monitoring for [Competitor Z] | Analyst | 1 week |

## Output Format

Present findings as a structured **Competitive Intelligence Brief** in this order:

1. **Executive Summary** (3-5 sentences: landscape snapshot, top threat, top opportunity)
2. **Competitor Landscape Map** (positioning matrix)
3. **Competitor Profiles** (one per primary competitor, condensed for secondary)
4. **Feature Comparison Matrix**
5. **Pricing Intelligence Summary**
6. **SWOT Analysis**
7. **Battle Cards** (one per primary competitor)
8. **Strategic Recommendations** (with 90-day action plan)

## Important Guidelines

- Always date-stamp the brief. Competitive intelligence expires fast.
- Source every claim. "G2, Jan 2026" or "company blog, Feb 2026" — not general assertions.
- Be honest about your own weaknesses. Sales teams that get surprised by competitor strengths lose trust in battle cards.
- Never make legal claims about a competitor's product you cannot verify.
- Flag confidence level on each data point: **High** (verified multiple sources), **Medium** (one source), **Low** (inferred).
- When win/loss data is unavailable, say so — and recommend a 30-day win/loss interview sprint.
- Read [analysis-frameworks.md](references/analysis-frameworks.md) for Porter's Five Forces, positioning matrix methodology, and SWOT best practices.
- Read [research-sources.md](references/research-sources.md) for where to gather raw competitive intelligence data.

## Related Skills

| Skill | Relationship |
|-------|-------------|
| strategic-planning-facilitator | Receives competitive intelligence as a primary input for the SWOT analysis and strategic theme identification |
| abm-campaign-builder | Receives competitor positioning data used in Module 1 landscape mapping and Module 5 value proposition design |
| seo-strategy-analyzer | Receives competitor SEO and content strategy data to inform keyword targeting and content gap analysis |
