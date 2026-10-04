---
name: pricing
description: >
  Help determine pricing strategy for a product or service using minimalist entrepreneur principles.
  Use when setting initial prices, considering price changes, or figuring out what to charge.
compatibility:
  models: [any-llm]
  use-case: pricing-strategy
  frameworks: [minimalist-entrepreneur, value-based-pricing]
---

# Pricing

Set prices that are sustainable, customer-friendly, and iterative. Charge something from day one.

## Use This Skill When

- User is setting initial pricing for a product/service
- User is considering raising or lowering prices
- User is deciding between pricing models
- User wants to understand pricing psychology
- User says phrases like "what should I charge", "pricing strategy", "is this price fair", "how do I price"

## When NOT to Use

- User is building pricing page design (use design skill)
- User is setting up complex billing/invoicing (use payments skill)
- User is analyzing competitor pricing only (use market research skill)

## Context: Pricing Maturity

**Manual pricing**: Asking each customer "what can you pay?" or guessing randomly  
**Cost-based**: Costs + 20–50% margin; one price  
**Market-aligned**: Pricing similar to alternatives; justified by value  
**Tiered/optimized**: Multiple tiers; prices raised over time; LTV-optimized → **Target**

## Core Principle

**Charge something. Always.** There is a psychological cliff between free and $1 (the "zero-price effect"). Customers will line up for free products but won't engage with them. Pricing signals value. Without pricing, you can't survive or learn what customers truly value.

## Instructions

### Understanding Pricing Psychology

#### The Zero-Price Effect
- **Free**: Unlimited perceived demand, zero commitment, low engagement
- **$1+**: Creates selection friction (good!), signals value, enables commitment
- **Implication**: Never offer free as your default; always require payment

#### Anchor Pricing
- First price you see anchors all subsequent price judgments
- Start at a reasonable price (not too low, which signals low value; not absurd)
- Customers compare to this anchor, not to absolute value

#### Tiered Pricing Psychology
- Customers will choose the middle tier (not cheapest, not most expensive)
- This means offering 3 tiers lets you capture more value from different segments
- Example: Spotify Free → Premium → Premium Family

### Pricing Models

**Choose one, then evolve:**

#### Model 1: Cost-Based Pricing

**Formula**: Costs + Margin = Price

| Cost Category | Example | Notes |
|---------------|---------|-------|
| **Variable** | Payment processing (2.9% + 30¢), hosting per user, materials | Scales with sales |
| **Fixed** | Your salary, base hosting, tools, domain | Constant regardless of volume |
| **Margin** | 20–100% above costs | Higher for digital products (100%+); lower for physical (20–30%) |

**When to use**:
- Physical products with clear material costs
- Services with hourly labor
- Need to ensure baseline profitability

**Example**:
- Your cost: $3 per unit
- Retail margin: 50% markup
- Price: $4.50 per unit

#### Model 2: Value-Based Pricing

**Formula**: Price = Customer Perceived Value

| Customer Situation | Value | Price Justification |
|-------------------|-------|-------------------|
| Saves 5 hours/week at $50/hr | $250/week value | Charge $50–100/month |
| Increases revenue by $10k/year | $10k value | Charge $1–3k/year |
| Solves critical problem (pain avoidance) | Pain cost | Charge based on pain magnitude |

**When to use**:
- Software/digital products (low marginal cost)
- High-value services (consulting, training)
- Clear ROI or pain-based value

**Example**:
- Customer loses $500/week if system is down
- Your product saves them 50% downtime risk = $250/week value
- Price: $50–100/week ($2.6k–5.2k/year) is still a 5–10x ROI for customer

#### Model 3: Hybrid

**Use both**: Cost-based floor + value-based ceiling

- Price must cover costs (floor)
- Price is capped by customer willingness to pay (ceiling)
- Negotiate within this band based on customer value

### Setting Your Initial Price

**Step 1: Know Your Costs**

```
Variable cost per customer: $X
Fixed costs per month: $Y
Target profit margin: Z%

Price = (Variable cost × (1 + Z%)) + (Fixed cost / Expected customers)
```

**Step 2: Research Alternatives**

- What do competing/alternative solutions charge?
- What would customers currently pay (directly or indirectly) to solve this?
- What's the "not-a-no-brainer" price? (Above that, they'll just suffer and not buy)

**Step 3: Calculate Customer Payback**

```
How much revenue do you need per month? $X
At your price point, how many customers is that? $X ÷ Price = Y customers
At 1 new customer per business day, when do you reach Y? 
(260 business days per year = 20/month)

Example: $10/month price, need $2,000/month = 200 customers = 10 months
```

**Step 4: Validate with Customers**

- Ask early customers: "Would you pay $X for this?" (Not "Is this price fair?")
- Offer pricing tiers; see which people choose
- A/B test prices with new customer cohorts
- Listen to price objections carefully

### Pricing Strategies

#### Strategy 1: Start Low, Raise Over Time
- **Rationale**: You'll improve the product; prices going up is normal and expected
- **Implementation**: Price increases every 6–12 months as you add value
- **Example**: Price stays $5/month for existing customers; new customers pay $10/month

#### Strategy 2: Free Trial + Paid Conversion
- **Best practice**: 7–14 day free trial (long enough to see value)
- **Clear conversion**: Email reminder before trial ends
- **Pricing transparency**: Show price before trial, not after
- **Pitfall to avoid**: Free trials shouldn't be so easy that paid is a shock

#### Strategy 3: Freemium (Free + Paid Tiers)
- **Free tier**: Limited features; enough value to understand product but not solve entire problem
- **Paid tier**: Adds premium features, support, higher limits
- **Conversion rate**: Expect 1–5% of free users to convert to paid
- **Risk**: Freemium can trap you in low prices if free users dominate

#### Strategy 4: Tiered Pricing (Recommended for Scale)
- **Tier 1 (Budget)**: Lower price, basic features, self-serve
- **Tier 2 (Standard)**: Mid price, core features, email support
- **Tier 3 (Premium)**: Higher price, all features, priority support, customization

**Psychology**: Customers tend to choose the middle tier, so:
- Price Tier 1 at cost + minimal margin (to compete)
- Price Tier 2 as your target (where most customers land)
- Price Tier 3 much higher (shows value of full product)

### Pricing Over Time

| Timeline | Action | Rationale |
|----------|--------|-----------|
| **Launch** | Set initial price (conservative) | Get customers; gather feedback |
| **3 months** | Review feedback; consider +20% for new customers | Learning what's valued |
| **6 months** | Raise prices; grandfather existing customers | Product improved; market validates value |
| **12 months** | Introduce tiered pricing if successful | Capture different customer segments |
| **2+ years** | Continuously raise top tier; keep budget tier stable | Extract more value from power users |

**Key rule**: Raise prices incrementally and transparently. Existing customers get grace period; new customers pay new price.

### Profitability Math

Help users understand when they can stop trading time for money:

```
Monthly revenue needed: $X
Price point: $Y/month
Customers needed: X ÷ Y = C

At 1 new customer per business day (20/month):
Months to profitability: C ÷ 20 = M months

At 2 new customers per business day (40/month):
Months to profitability: C ÷ 40 = M months (faster)
```

**Example**:
- Need $3,000/month
- Price: $30/month
- Customers needed: 100
- At 1/day: 5 months to profitability
- At 2/day: 2.5 months to profitability

## Common Pricing Mistakes

- **Too low**: Signals low value; insufficient margin for growth
- **Too high**: Prevents customers from saying yes; not aligned with perceived value
- **No tiering**: Leaves money on the table; one-size-fits-all
- **Constantly changing**: Confuses customers; makes them avoid commitment
- **Apologizing for price**: Undermines value; confuses customers on what's worth
- **Freemium without exit strategy**: Traps you in low prices; hard to convert free users

## Output

For each pricing decision, provide:

1. **Pricing model** (Cost-based / Value-based / Hybrid with explanation)

2. **Initial price point** with breakdown:
   - Variable costs per unit
   - Fixed costs
   - Margin
   - Final price + rationale

3. **Profitability math**:
   - Customers needed for financial independence
   - Timeline at current sales pace
   - Breakeven timeline

4. **Tier structure** (if applicable):
   - Budget tier
   - Standard tier (recommended)
   - Premium tier

5. **Launch strategy**:
   - Free trial? (Length and rules)
   - Freemium? (Free tier limits)
   - None of the above? (Paid from day one)

6. **Price increase schedule**: When and how much to raise
