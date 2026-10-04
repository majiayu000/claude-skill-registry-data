---
name: find-shopify-store-leads
description: Finds and prioritizes relevant Shopify stores using public app-review relationships, competitor dissatisfaction, geography, and app-stack signals from Applora MCP. Use for account research, competitor-user discovery, integration prospecting, partner targeting, or preparing respectful personalized outreach.
---

# Find Shopify Store Leads

Turn public Shopify App Store review signals into a small, relevant research list. This skill identifies evidence for targeting; it does not send messages.

## Required connection

Use the Applora MCP server at `https://applora.ai/mcp`:

- `get_app_reviews({ handle, rating?, usageDuration?, hasContent?, cursor?, limit? })`
- `search_stores({ search?, country?, cursor?, limit? })`
- `get_store({ id, appHandle?, maxRating?, limit? })`
- `search_apps({ query?, categoryHandles?, pricing?, builtForShopify?, minRating?, maxRating?, sort?, cursor?, limit? })`
- `get_app({ handle, includeCategoryRanks?, limit? })`

Store relationships come from public reviews. They indicate that a store reviewed an app at some point, not a confirmed current installation.

## Workflow

1. Define the ideal customer profile, geography, relevant competitor or complementary app, and the problem your offer solves.
2. Resolve exact competitor handles.
3. Pull recent reviews with merchant IDs:
   - 1–3 star for dissatisfaction-led targeting;
   - 4–5 star for complementary integration or partnership targeting.
4. Fetch store profiles only for candidates matching the research thesis. Filter by app and maximum rating where useful.
5. Look for:
   - an explicit complaint your product solves;
   - relevant app-stack or category signals;
   - geography fit;
   - review recency and specificity;
   - multiple signals rather than one vague review.
6. Score fit, timing, evidence quality, and personalization potential.
7. Produce a bounded shortlist with the public evidence and a respectful outreach angle.

## Privacy and outreach guardrails

- Do not expose or use email, phone, or address fields returned by any source.
- Do not claim a current install, contract, budget, or buying intent.
- Do not automate outreach, scraping, or enrichment without separate user authorization and applicable consent.
- Avoid sensitive inference, spam tactics, and manipulative personalization.
- Cite public review evidence accurately and avoid quoting personal details.

## Output

Return:

1. targeting thesis and filters;
2. prioritized shortlist with store name, country, evidence, and confidence;
3. why each store is relevant now;
4. a one-sentence, non-creepy personalization angle;
5. limitations and suggested manual verification.

Prefer 10 strong candidates over hundreds of weak leads.
