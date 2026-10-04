---
name: analyze-shopify-app-reviews
description: Analyzes Shopify App Store review sentiment, complaint themes, feature requests, switching triggers, and merchant language using current and historical review data from Applora MCP. Use for voice-of-customer research, product prioritization, churn analysis, support diagnosis, or category-wide sentiment studies.
---

# Analyze Shopify App Reviews

Convert verbatim public reviews into traceable product decisions. Do not invent sentiment percentages or themes without reading the underlying review text.

## Required connection

Use the Applora MCP server at `https://applora.ai/mcp`:

- `get_app({ handle, includeChanges?, includeCategoryRanks?, changeTypes?, limit? })`
- `get_app_reviews({ handle, rating?, usageDuration?, hasContent?, cursor?, limit? })`
- `live_get_app_reviews({ handle, page?, sortBy?, rating?, hasContent?, limit? })` for current Pro verification
- `get_category({ handle, includeRankedApps?, rankedAppsLimit? })` for category-level sampling
- `get_store({ id, appHandle?, maxRating?, limit? })` only when a review's store context matters

## Sampling workflow

1. Define the decision and time sensitivity. A product-priority study needs a different sample from a support incident check.
2. Fetch the app profile to establish rating and review-count context.
3. Pull bounded, stratified samples:
   - 1–2 star reviews for failures and churn triggers;
   - 3 star reviews for tradeoffs and missing features;
   - 4–5 star reviews for must-preserve value.
4. Use `hasContent: true`. Page only until themes stabilize; state the exact sample size.
5. For category research, select a transparent set of leading apps and repeat the same sampling rule.
6. Code each review into concrete themes such as reliability, setup, compatibility, support, billing, missing capability, or outcome achieved.
7. Count mentions within the sample. Do not present sample frequency as the share of all customers.
8. Support each important theme with a short representative quote and app/rating context.
9. Distinguish recent operational incidents from recurring structural problems. Use a live call if freshness matters.

## Analysis rules

- Keep praise, complaint, request, and switching trigger separate.
- Treat sarcasm and mixed reviews carefully; preserve ambiguity.
- Never expose private contact fields.
- Public review-inferred store relationships are signals, not confirmed current installs.
- Flag selection bias: reviewers are not the full customer base.

## Output

Lead with the three most decision-relevant findings. Then provide:

1. sample and method;
2. theme frequency within the sample;
3. representative evidence;
4. severity versus prevalence;
5. product, support, and messaging actions;
6. confidence and limitations.

Prefer a small evidence matrix over a long narrative or raw review dump.
