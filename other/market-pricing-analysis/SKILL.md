---
name: market-pricing-analysis
description: Automatically analyze product, service, subscription, marketplace, or competitor pricing when the user asks "fiyatı iyi mi", "almaya değer mi", "en ucuz/kaliteli hangisi", "muadili var mı", compares rivals, wants price-quality/value-for-money, total-cost normalization, market positioning, package/feature comparison, willingness-to-pay, or pricing strategy. Verify current official pages and dated offers; normalize currency, tax, shipping, quantity, renewals and contract terms; distinguish independent measured quality from seller, sponsor, affiliate, and advertising claims. Add health-product-evidence-check for health claims. Do not use for security prices, investment targets, or autonomous purchases.
---

# Market Pricing Analysis

Use this for commercial and consumer market analysis, not tradable securities.

Read [references/pricing-method.md](references/pricing-method.md), [references/quality-evidence.md](references/quality-evidence.md), and [references/web-research.md](references/web-research.md). Use `scripts/normalize_prices.py` for comparable price and value calculations.

## Workflow

1. Define the decision: buy, sell, set price, enter a market, compare plans, or evaluate a competitor.
2. Resolve the exact product/service variant, geography, date, currency, package size, taxes, shipping, discounts, contract length, renewal and cancellation terms.
3. Capture current official pages and independent quality evidence. Treat testimonials, rankings, seller claims and affiliate pages as potentially biased.
4. Normalize landed cost and unit price. Do not compare teaser monthly price with full contract cost or different quantities/features.
5. Build a feature and quality matrix. Mark unknowns rather than inventing scores.
6. Segment competitors into budget, value, premium and specialist positions based on evidence, not branding language alone.
7. Explain price gaps through measurable features, service, reliability, brand, distribution, switching cost, or margin—not vague “quality”.
8. Test scenarios for FX, discount expiry, shipping, tax, churn, volume and competitor response when relevant.
9. Return the best value, best quality, cheapest acceptable, and overpriced/weak-evidence options separately.

## Hard rules

- State the page date and country. Prices can vary by account, location and time.
- Include total ownership cost, not sticker price alone.
- Do not convert currencies without a timestamped FX rate supplied or sourced for the same decision date.
- Do not treat review volume as product quality without bias and sample checks.
- Do not scrape or bypass access restrictions; use available public pages and user-provided data.
- Do not recommend a higher price merely because it is premium-branded.

## Output

Start with the buying/pricing decision. Show a compact normalized comparison, quality evidence, key trade-offs, competitor positioning, hidden costs, sensitivity and confidence. Identify which missing fact could change the winner.
