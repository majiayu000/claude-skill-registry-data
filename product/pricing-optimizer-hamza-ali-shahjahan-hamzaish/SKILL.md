---
name: pricing-optimizer
description: Iterate pricing post-PMF based on real data — willingness to pay, expansion revenue, packaging tweaks, annual upsell, enterprise pricing.
---

# Pricing Optimizer

## When you activate
- Quarterly pricing review
- User asks: "should we raise prices?", "test pricing for X", "design enterprise tier"
- After significant feature additions

## What you produce
Saved to `products/<name>/scale/pricing-review-YYYY-QN.md`:

```
## Pricing Review — <product> — <quarter>

### Current state
- Tiers + prices: <list>
- ARPU: $<X>
- % on annual: <Y>%
- Median time-to-paid: <Z days>
- Churn rate (by tier): <list>

### Signals from the last quarter
- Conversion rate at current price: <%>
- Customer comments mentioning "too expensive": <count>
- Customer comments mentioning "great value" / "would pay more": <count>
- Tier 1 → Tier 2 upgrade rate: <%>
- Cancellation reasons by tier: <breakdown>

### Recommendations
1. <change> — rationale + expected impact
2. ...
3. ...

### Tests to run
- A/B price test: <current> vs <new> — at <signup point> for <segment> — duration <14d>
- Hypothesis: <what we expect to see>
- Stop conditions: <when to call it>

### Enterprise tier (if relevant)
- Triggers: SSO request, > N seats, custom data residency, > $X MRR potential
- Pricing: not on site — "talk to us" with anchor of $<X>/mo
- Process: discovery call → custom quote → SOW → signed → onboarding

### Annual upsell
- Current annual % : <Y>%
- Target: > 40% on annual
- Tactics: better discount, prominent on pricing page, in-app prompts at month 3
```

## Protocol
1. Pull data from Stripe + PostHog.
2. Look for: pricing-related qualitative signals in support tickets / surveys / sales calls.
3. Identify the one pricing change with highest expected value and lowest risk. Test it. Don't change everything at once.
4. For enterprise pricing: don't publish a price. Make it custom.
5. Annual upsell is usually the easiest pricing win — cash up front + reduces churn.

## Sources
- `knowledge-base/launch-stage/pricing-playbook.md`
- `knowledge-base/scale-stage/100-to-1000-customers.md`

## What you don't do
- Don't lower prices to compete. Lower prices → lower-value customers → higher churn → worse unit economics.
- Don't change prices for existing customers without explicit communication and grandfathering options.
- Don't add tiers — pricing pages should get simpler over time, not more complex.
