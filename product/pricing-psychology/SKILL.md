---
description: Psychological pricing strategies (anchoring, decoys, etc.).
---

# Pricing Psychology Skill

## Strategic Value

The Pricing Psychology Skill leverages decades of behavioral economics research to optimize pricing presentation and structure. By applying cognitive biases like anchoring, decoy effects, and loss aversion, it maximizes perceived value and conversion rates—often without changing actual prices. This skill transforms pricing from guesswork into a precision instrument of persuasion.

## Capabilities

- **Anchoring Optimization:** Strategically positions reference prices to influence perception.
- **Decoy Effect Design:** Creates tiered options that make target prices more attractive.
- **Charm Pricing:** Applies .99, .97, and other psychological price endings.
- **Bundle Optimization:** Structures product bundles to maximize perceived savings.
- **Urgency/Scarcity:** Implements time-limited and quantity-limited pricing tactics.
- **A/B Testing:** Generates pricing variants for empirical testing.

## Limitations

- Cultural variations in price perception require localization.
- Regulatory constraints on pricing practices in some jurisdictions.
- Overuse can diminish trust if perceived as manipulative.

## Examples

### Example 1: SaaS Tier Optimization

**User Prompt:** "We have Basic ($29), Pro ($79), and Enterprise plans. Suggest optimal presentation to boost Pro conversions."

**Strategy Recommendation:**
```json
{
  "strategy": "Decoy Effect + Anchoring",
  "recommendation": "Add a 'Plus' plan at $99 with slightly more features than Pro",
  "presentation_order": [
    {
      "name": "Basic",
      "price_displayed": "$29/month",
      "position": "last",
      "emphasis": "none"
    },
    {
      "name": "Pro",
      "price_displayed": "$79/month",
      "position": "middle (highlighted)",
      "emphasis": "bestseller_badge",
      "anchoring_text": "Save $20 vs Plus plan"
    },
    {
      "name": "Plus",
      "price_displayed": "$99/month",
      "position": "first",
      "thumb_text": "Only $20 more for Pro"
    }
  ],
  "expected_impact": "15-25% increase in Pro tier selection"
}
```

### Example 2: Launch Pricing Strategy

**User Prompt:** "New product launch at $199. Recommend psychological pricing structure."

**Strategy Recommendation:**
```json
{
  "strategy": "Anchoring + Limited Introductory",
  "launch_price": "$149 (Introductory)",
  "anchoring_approach": {
    "original_display": "$249",
    "introductory": "$149",
    "savings_highlight": "Launch Special: Save $100 (40% off)",
    "urgency": "First 500 customers only",
    "timer": "72-hour countdown"
  },
  "charm_pricing": "$149 becomes $147 (3 is more appealing than 9 in this tier)",
  "post_launch": "Revert to $199 MSRP with occasional $169 promotions"
}
```

## Configuration (config.yaml)

```yaml
pricing_strategies:
  decoy_effect:
    enabled: true
    target_tier: "middle"
  anchoring:
    enabled: true
    reference_price_ratio: 1.3  # Anchor is 30% higher than target
  charm_pricing:
    enabled: true
    endings: [99, 97, 95]
    price_thresholds:
      under_100: 97
      under_500: 99
      over_500: 00  # Round numbers signal luxury
  urgency_tactics:
    flash_sale_duration_hours: 24
    scarcity_message: "Only X remaining"
    countdown_timer: true

market_segments:
  premium:
    strategy: "round_numbers"
    messaging: "exclusive"
  value:
    strategy: "charm_pricing"
    messaging: "savings_focused"
  b2b:
    strategy: "anchoring"
    messaging: "roi_focused"
```
