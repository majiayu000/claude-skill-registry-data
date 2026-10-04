---
summary: "Optimize in-app purchase and upgrade moments for increased revenue."
---

# Paywall/Upgrade CRO Skill

This skill focuses on optimizing the conversion rates for in-app purchases, subscriptions, and upgrades. It helps in analyzing paywall effectiveness, testing pricing models, and improving the user journey towards premium features.

## When to use this skill:
Use this skill when you need to:
- Optimize paywalls, subscription pages, or upgrade prompts within an application or website.
- A/B test pricing tiers, feature comparisons, or value propositions.
- Improve the conversion rate from free to paid users or from lower to higher tiers.
- Reduce churn by ensuring users understand the value of their upgrade/subscription.
- Analyze the impact of different messaging and timing for upgrade offers.

## Capabilities:
- **Paywall Analysis:** Identifies friction points and opportunities for improvement within existing paywalls or upgrade flows.
- **Pricing Model A/B Testing:** Supports experimentation with different pricing structures, discounts, and billing cycles.
- **Value Proposition Optimization:** Helps refine the messaging and presentation of premium features to highlight their benefits.
- **Upgrade Path Personalization:** Enables tailoring upgrade offers based on user behavior, usage patterns, or demographics.
- **Performance Tracking:** Monitors key metrics such as conversion rate to paid, average revenue per user (ARPU), lifetime value (LTV), and churn rates specifically related to upgrades.

## Examples:

### Example 1: Analyze a specific paywall page
```
/paywall-upgrade-cro analyze --page-id="premium_feature_paywall"
```
This command analyzes the effectiveness of the specified premium feature paywall.

### Example 2: Suggest A/B tests for subscription pricing tiers
```
/paywall-upgrade-cro recommend-ab-test --element="pricing_tiers" --current-layout="3_tiers_monthly_yearly" --proposals="2_tiers_quarterly_yearly;feature_based_tiers"
```
This command suggests A/B test variations for subscription pricing tiers.

### Example 3: Get conversion rate for a specific upgrade offer
```
/paywall-upgrade-cro get-metrics --offer-id="pro_plan_discount" --metric="conversion_rate" --timeframe="last_60_days"
```
This command retrieves the conversion rate for the 'pro_plan_discount' offer over the last 60 days.
