---
name: optimize-shopify-app-aso
description: Creates evidence-backed Shopify App Store optimization plans from keyword SERPs, category rankings, competitor listings, and review language using Applora MCP. Use when choosing target keywords, improving an app title or listing positioning, diagnosing discoverability, planning ASO experiments, or tracking ranking gains.
---

# Optimize Shopify App ASO

Build an ASO plan from current search results and tracked rank history. Never claim keyword demand, competition, or rank from memory.

## Required connection

Use the Applora MCP server at `https://applora.ai/mcp`:

- `search_keywords({ search?, minCompetingApps?, maxCompetingApps?, cursor?, limit? })`
- `get_keyword({ handle, includeHistory?, includeRankedApps?, historyLimit?, rankedAppsLimit?, minPosition?, maxPosition? })`
- `research_keyword({ query, limit?, includeSponsored?, minRating? })` to index an unknown keyword
- `live_search_keyword({ query, page?, limit?, includeSponsored?, minRating? })` to verify today's SERP
- `get_app({ handle, includeChanges?, includeCategoryRanks?, changeTypes?, limit? })`
- `live_get_app({ handle, includeDescription?, includePricing?, includeCompatibility? })`
- `get_app_reviews({ handle, rating?, hasContent?, cursor?, limit? })`

Live and unindexed keyword research may require Pro. Relay plan errors directly.

## Workflow

1. Identify the target app, buyer, primary use case, and current listing objective.
2. Fetch the app profile and current listing. Treat indexed keyword estimates as directional unless the source is tracked.
3. Build a small keyword set from the product problem and exact phrases merchants use in reviews.
4. Resolve indexed terms with `search_keywords`. If a critical term is missing, call `research_keyword`; use `live_search_keyword` only when immediate SERP verification changes the decision.
5. For each viable term, request history and the top 10–20 ranked apps. Evaluate:
   - competing app count;
   - ranking stability and page-one churn;
   - incumbent ratings and low-rating ratio;
   - relevance between search intent and the app's promise;
   - sponsored placements separately from organic results.
6. Segment terms into primary, secondary, experimental, and reject.
7. Compare the app's title, subtitle/description language, proof, category, and positioning with the organic leaders.
8. Propose one change per experiment and define the ranking or conversion signal to watch.

## Guardrails

- Do not equate app count with search volume; label it competition, not demand.
- Do not stuff keywords or promise ranking guarantees.
- Preserve accurate product claims and natural language.
- Separate current rank, historical movement, and inferred opportunity.
- Prefer 5–10 defensible targets over a large generic keyword list.

## Output

Return:

1. the ASO diagnosis;
2. a prioritized keyword map with evidence and intent;
3. recommended listing positioning and copy themes;
4. a 30-day experiment plan;
5. measurement criteria and risks.

Quote merchant language sparingly and only when it sharpens positioning.
