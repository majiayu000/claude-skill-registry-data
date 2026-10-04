---
name: analyze-shopify-app-competitors
description: Produces evidence-backed Shopify app competitor teardowns using listings, pricing, rankings, review sentiment, developer portfolios, and change history from Applora MCP. Use when comparing competitors, finding differentiation, preparing battlecards, tracking market moves, or identifying weaknesses worth building against.
---

# Analyze Shopify App Competitors

Find defensible competitor weak spots rather than producing a feature checklist. Verify every current claim with Applora MCP.

## Required connection

Use the Applora MCP server at `https://applora.ai/mcp`:

- `search_apps({ query?, categoryHandles?, pricing?, builtForShopify?, minRating?, maxRating?, sort?, cursor?, limit? })`
- `get_app({ handle, includeChanges?, includeCategoryRanks?, changeTypes?, limit? })`
- `get_app_changes({ handle, changeTypes?, limit? })`
- `get_app_reviews({ handle, rating?, usageDuration?, hasContent?, cursor?, limit? })`
- `search_developers({ search?, exactName?, cursor?, limit? })`
- `get_developer({ handle, minRating?, pricing?, builtForShopify?, limit? })`
- `live_get_app({ handle, includeDescription?, includePricing?, includeCompatibility? })`

## Workflow

1. Clarify the target customer and decision: positioning, roadmap, sales battlecard, or threat monitoring.
2. Resolve exact app handles with a narrow `search_apps` call.
3. Fetch each app with category ranks and relevant history. Request only needed change types.
4. Verify current listing, pricing, compatibility, or Built for Shopify status live when recency matters.
5. Compare:
   - promise and target customer;
   - pricing and packaging;
   - rating, review momentum, and rank movement;
   - category and keyword visibility;
   - developer portfolio strength;
   - meaningful recent changes.
6. Pull comparable 1–3 star review samples for each app. Find repeated failed promises, not isolated complaints.
7. Classify gaps as product, reliability, onboarding, support, pricing, integration, or positioning.
8. Score each gap by evidence strength, frequency, strategic fit, and ease of exploitation.

## Guardrails

- Never infer revenue, installs, or market share from review count alone.
- Do not call a feature absent unless the current listing or evidence supports it.
- Distinguish a competitor weakness from a segment mismatch.
- Use the same sampling and comparison criteria across apps.
- Mark facts, inferences, and recommendations separately.

## Output

Lead with the single most defensible differentiation opportunity. Then provide:

1. compact competitor matrix;
2. evidence-backed weak spots;
3. threats and strengths not to underestimate;
4. recommended product and messaging wedges;
5. watch signals and confidence.

Include handles so findings can be checked independently; avoid raw JSON.
