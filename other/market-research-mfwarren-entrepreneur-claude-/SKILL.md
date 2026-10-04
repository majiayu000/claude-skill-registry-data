---
name: market-research
version: 1.0.0
category: Product & Strategy
domain: market-research
author: Matt Warren
license: MIT
status: production
updated: 2026-02-07
activation_triggers:
  - "market research"
  - "market size"
  - "TAM SAM SOM"
  - "target market"
  - "customer research"
  - "market analysis"
  - "industry analysis"
  - "customer persona"
  - "ideal customer"
  - "ICP"
tools: []
---

# Market Research

TAM/SAM/SOM analysis, customer persona development, survey design, and market sizing for new products, markets, or pivots.

## Purpose

Make better business decisions by understanding the market before you build. This skill structures market research into actionable outputs — not academic reports. Focus on information that changes what you'd do.

## Workflow

### Step 1: Define the Research Question

Ask the user:
- What decision are you trying to make? (launch, pivot, expand, price, position)
- What market or industry?
- What do you already know? What's your current assumption?
- What would change your mind?

### Step 2: Market Sizing (TAM/SAM/SOM)

**TAM (Total Addressable Market):**
- Total revenue if you captured 100% of the market
- Top-down: Industry reports, government data, analyst estimates
- Bottom-up: Number of potential customers x average revenue per customer

**SAM (Serviceable Addressable Market):**
- The segment of TAM you can actually reach with your product/channel/geography
- Apply filters: location, company size, industry vertical, tech stack, budget

**SOM (Serviceable Obtainable Market):**
- Realistic share you can capture in 1-3 years
- Based on: competitive landscape, your current resources, growth rate
- Typically 1-5% of SAM for a new entrant

Present as a funnel:
```
TAM: $X billion (total market)
 └─ SAM: $X million (your segment)
     └─ SOM: $X million (your realistic capture)
```

### Step 3: Customer Persona / ICP

Build an Ideal Customer Profile:

| Dimension | Details |
|-----------|---------|
| Demographics | Age, location, income, job title |
| Company (B2B) | Size, industry, revenue, tech stack |
| Pain points | Top 3 problems they're trying to solve |
| Current solution | What they use today (including "nothing") |
| Buying triggers | What event makes them start looking |
| Objections | Why they'd say no |
| Where they hang out | Communities, platforms, publications |
| Budget | What they currently spend on this problem |

### Step 4: Competitive Landscape

Map the competitive landscape:
- **Direct competitors:** Same product, same market
- **Indirect competitors:** Different product, same problem
- **Alternatives:** Including "do nothing" and DIY

For each competitor, identify:
- Positioning (what they claim)
- Pricing (public or estimated)
- Strengths and weaknesses
- Customer complaints (reviews, forums, social media)
- Gaps they don't address

### Step 5: Survey / Interview Design (if requested)

Design a customer discovery survey (5-10 questions):
- Open with behavior questions (what they do), not opinion questions (what they think)
- Ask about the last time they experienced the problem
- Ask what they've tried and what failed
- Ask about willingness to pay (Van Westendorp or direct)
- Close with "What would make this a no-brainer for you?"

### Step 6: Synthesize into Decision Framework

Deliver a summary that directly answers the user's research question:
- Here's what the data says
- Here's what's uncertain
- Here's what I'd recommend investigating further
- Here's the decision this supports

## Output Format

```markdown
## Market Research: [Topic]

### Research Question
[What we're trying to answer]

### Market Size
- TAM: $X
- SAM: $X
- SOM: $X
[Supporting logic]

### Ideal Customer Profile
[ICP table]

### Competitive Landscape
[Competitor comparison]

### Key Findings
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

### Recommendation
[Direct answer to the research question]

### What to Investigate Further
- [Open question 1]
- [Open question 2]
```

## Constraints

- Always distinguish between data and assumptions — label which is which
- Market size estimates should show the math, not just a number
- Don't fabricate competitor data — note when information is estimated vs. verified
- Focus on actionable insights, not comprehensive coverage
- If the user's market is too niche for reliable data, say so and suggest proxies
