---
name: design-shopify-app-pricing
description: Recommends Shopify app pricing and packaging using current competitor offers, category norms, review complaints, and positioning evidence from Applora MCP. Use when setting a launch price, redesigning tiers, evaluating free or freemium strategy, diagnosing pricing objections, or preparing packaging experiments.
---

# Design Shopify App Pricing

Design a pricing hypothesis grounded in the Shopify App Store market. Treat the result as a testable recommendation, not proof of willingness to pay.

## Required connection

Use the Applora MCP server at `https://applora.ai/mcp`:

- `search_apps({ query?, categoryHandles?, pricing?, builtForShopify?, minRating?, maxRating?, sort?, cursor?, limit? })`
- `get_app({ handle, includeChanges?, includeCategoryRanks?, changeTypes?, limit? })`
- `live_get_app({ handle, includeDescription?, includePricing?, includeCompatibility? })`
- `get_app_reviews({ handle, rating?, hasContent?, cursor?, limit? })`
- `live_get_app_reviews({ handle, page?, sortBy?, rating?, hasContent?, limit? })`
- `get_category({ handle, includeRankedApps?, rankedAppsLimit? })`
- `get_app_changes({ handle, changeTypes?, limit? })`

## Workflow

1. Define the target segment, job-to-be-done, value metric, product maturity, and pricing decision.
2. Build a relevant comparison set from the category and direct substitutes. Avoid mixing unrelated enterprise and SMB products.
3. Fetch current pricing live for the closest competitors. Use indexed changes to identify recent pricing moves.
4. Normalize offers into:
   - entry mechanism: free, trial, freemium, or paid;
   - value metric and tier boundaries;
   - included outcomes and important limits;
   - apparent target segment.
5. Read bounded low- and mid-rating review samples for billing confusion, surprise charges, poor value, forced upgrades, missing tier fit, and praise for value.
6. Link each complaint to packaging mechanics rather than assuming all price complaints mean "too expensive."
7. Propose a good/better/best structure, value metric, guardrails, and migration path.
8. Define an experiment with conversion, activation, expansion, refund, and support signals.

## Guardrails

- Applora observes public listings and reviews, not competitor revenue or conversion.
- Do not invent exact willingness-to-pay figures.
- Separate current public price from inferred packaging intent.
- Avoid undercutting as the default strategy; price around differentiated value.
- State currency, billing cadence, usage assumptions, and unknowns.

## Output

Return:

1. a concise market benchmark;
2. pricing complaints and what they actually imply;
3. recommended tiers and value metric;
4. positioning for each tier;
5. experiment and success thresholds;
6. risks and evidence still needed.
