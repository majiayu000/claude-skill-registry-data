---
name: pricing-optimizer
description: Dynamic pricing based on competitor moves and market conditions
author: "@namanwtf"
version: 3.0.0
requires: brand-context, competitive-intel
category: strategy
---

# 💰 Pricing Optimizer Agent

**Purpose:** Automatically optimize pricing based on competitor moves, demand signals, and margin protection rules. Never leave money on the table.

---

## When to Use

```bash
# Analyze current pricing vs competitors
@pricing-optimizer analyze

# Get pricing recommendation for specific product
@pricing-optimizer recommend product-x

# Set up auto-adjustment with thresholds
@pricing-optimizer auto-adjust --threshold 5%

# Simulate price change impact
@pricing-optimizer simulate --product product-x --price 149

# Generate pricing strategy report
@pricing-optimizer report --weekly
```

---

## Capabilities

### 1. Competitor-Based Pricing
- Monitors competitor prices in real-time
- Calculates price gaps and positioning
- Suggests optimal price points
- Tracks price elasticity

### 2. Margin Protection
- Never recommends below minimum margin
- Accounts for COGS, shipping, taxes
- Cash flow aware pricing
- Promotional budget integration

### 3. Smart Recommendations
```
SCENARIO: Competitor A drops Product X to $199

ANALYSIS:
• Your Product Y: $249
• Price gap: $50 (25% higher)
• Competitor: Basic feature set
• Your advantage: Premium features

RECOMMENDATIONS:
1. MATCH: $199 (aggressive, -20% margin)
   → Risk: Price war
   → Reward: Maintain market share

2. BUNDLE: $249 + free premium accessories
   → Maintain price, add value
   → Perceived value increase: $75

3. DIFFERENTIATE: $229 (match halfway)
   → Highlight premium features
   → Target quality-conscious buyers

OPTIMAL CHOICE: Option 2 (Bundle Strategy)
Confidence: 78%
Expected impact: +12% conversions, -3% margin
```

### 4. Seasonal Calendar Integration
```
UPCOMING: Holiday Sale (December)

PRICING STRATEGY:
• Pre-sale (Nov): Maintain $249
• Sale (Dec 1-31): Flash price $199
• Post-sale (Jan): $229 (new normal)

MARGIN IMPACT:
• Pre-sale: 22% margin
• Sale: 8% margin (volume play)
• Post-sale: 18% margin (new baseline)
```

### 5. A/B Test Pricing
```bash
@pricing-optimizer ab-test --product product-x

SETUP:
• Variant A: $249 (current)
• Variant B: $229 (test)
• Duration: 14 days
• Traffic split: 50/50

SUCCESS METRICS:
• Primary: Revenue per visitor
• Secondary: Conversion rate, margin

AUTO-ROLLBACK if:
• Revenue drops >15%
• Margin drops below 12%
```

---

## Configuration

Add to your `brand-context.md`:

```yaml
pricing-optimizer:
  products:
    - name: "Product X"
      current-price: 249
      min-margin: 15%
      cogs: 150
      competitors: ["competitor-a-product", "competitor-b-product"]
    
  strategy:
    type: "value-based"  # Options: penetration, skimming, value-based
    aggression: "medium"  # Options: conservative, medium, aggressive
    
  guardrails:
    min-margin: 12%
    max-discount: 20%
    price-match: true
    bundle-preference: true
    
  calendar:
    seasons:
      - name: "Holiday Sale"
        date: "2025-12-01"
        discount: 20%
      - name: "Spring Launch"
        date: "2025-03-15"
        discount: 15%
      - name: "Back to School"
        date: "2025-08-15"
        discount: 10%
```

---

## Usage Examples

### Scenario 1: Competitor Price Drop
```
User: @pricing-optimizer alert "competitor a dropped product x price"

Agent: 🚨 PRICING ALERT

COMPETITOR MOVE:
• Competitor A Product X: $199 (was $229)
• Drop: $30 (-13%)
• Your position: $50 premium

OPTIONS ANALYSIS:
┌─────────────┬────────────┬───────────┬──────────┐
│ Strategy    │ New Price  │ Margin    │ Impact   │
├─────────────┼────────────┼───────────┼──────────┤
│ Match       │ $199       │ 12%       │ High vol │
│ Undercut    │ $189       │ 8%        │ Max vol  │
│ Bundle      │ $249       │ 20%       │ Brand    │
│ Ignore      │ $249       │ 22%       │ Risky    │
└─────────────┴────────────┴───────────┴──────────┘

RECOMMENDATION: Bundle Strategy
• Price: $249
• Add: Premium accessory ($79 value)
• Effective discount: 10%
• Margin: 18%

Execute? [Yes/No/Adjust]
```

### Scenario 2: New Product Launch
```
User: @pricing-optimizer launch product-y

Agent: 📊 LAUNCH PRICING ANALYSIS

MARKET RESEARCH:
• Competitor A Product M: $179 (basic tier)
• Competitor B Product N: $199 (mid tier)
• Competitor C Product O: $279 (premium tier)

POSITIONING OPTIONS:
1. AGGRESSIVE: $169 (undercut Competitor A)
   → Market share focus
   → Margin: 10%
   
2. VALUE: $219 (between Competitor B & C)
   → Balanced approach
   → Margin: 20%
   → Highlight: Premium features
   
3. PREMIUM: $299 (above Competitor C)
   → Feature superiority
   → Margin: 28%
   → Requires: Proven differentiation

RECOMMENDATION: Option 2 ($219)
• Sweet spot in market
• Defensible with features
• 20% margin sustainable

Launch price: $219
Intro offer: $199 (first week)
```

### Scenario 3: Dynamic Adjustment
```
User: @pricing-optimizer auto-adjust --enable

Agent: ⚙️ AUTO-ADJUSTMENT ENABLED

RULES CONFIGURED:
• Monitor: Competitor A, B, C prices (every 30 min)
• Trigger: Competitor drops >10%
• Action: Recommend response within 1 hour
• Limits: Never below 12% margin

NOTIFICATIONS:
• WhatsApp: Price alerts
• Email: Daily pricing summary
• Dashboard: Real-time price positioning

GUARDRAILS ACTIVE:
✅ Minimum margin: 12%
✅ Maximum discount: 20%
✅ Price match: Enabled
✅ Bundle preference: Enabled

Your pricing is now on autopilot (with approval gates).
```

---

## Integration with Other Skills

**Inputs from:**
- `competitive-intel`: Real-time competitor prices
- `analytics-dashboard`: Conversion data, demand signals
- `copywriting`: Pricing psychology frameworks

**Outputs to:**
- `meta-ads-optimizer`: Adjust ad bids based on pricing
- `copywriting`: Price messaging in ads
- `email-sequence`: Promotional pricing campaigns

---

## Safety Guardrails

- ✅ **Margin protection**: Never below configured minimum
- ✅ **Approval gates**: Major changes require human approval
- ✅ **A/B testing**: Validate before full rollout
- ✅ **Rollback**: One-click revert to previous pricing
- ✅ **Audit trail**: All price changes logged with rationale

---

## Related Skills

- **competitive-intel**: Real-time competitor pricing data
- **analytics-dashboard**: Conversion and demand tracking
- **copywriting**: Price messaging optimization

---

*Part of the Brand Marketing Team framework.*
*Author: @namanwtf | Version 3.0.0 | MIT License*
