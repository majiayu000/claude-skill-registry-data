---
name: research-shopify-market-opportunities
description: Finds and validates Shopify App Store market opportunities using live and historical category, keyword, app, ranking, and review evidence from Applora MCP. Use when deciding what Shopify app to build, sizing a niche, comparing category whitespace, validating demand, or producing a build/no-build market brief.
---

# Research Shopify Market Opportunities

Turn Shopify App Store data into a ranked opportunity thesis. Ground every market-size, growth, ranking, rating, or competition claim in an MCP result rather than memory.

## Required connection

Use the Applora MCP server at `https://applora.ai/mcp`. Prefer these focused tools:

- `get_market_overview({ includeHistory?, historyLimit?, boardTypes?, leaderboardLimit? })`
- `list_categories({ search?, parentHandle?, cursor?, limit? })`
- `get_category({ handle, includeHistory?, includeRankedApps?, historyLimit?, rankedAppsLimit?, minPosition?, maxPosition? })`
- `search_keywords({ search?, minCompetingApps?, maxCompetingApps?, cursor?, limit? })`
- `get_keyword({ handle, includeHistory?, includeRankedApps?, historyLimit?, rankedAppsLimit?, minPosition?, maxPosition? })`
- `get_app({ handle, includeChanges?, includeCategoryRanks?, changeTypes?, limit? })`
- `get_app_reviews({ handle, rating?, hasContent?, cursor?, limit? })`
- `live_get_category({ handle, page?, limit?, includeSponsored?, minRating? })` for time-sensitive Pro verification

If the tools are unavailable, explain that the skill needs the Applora MCP connection and stop. If a tool reports a plan limit, relay it; do not work around it.

## Workflow

1. Define the decision: target merchant, problem, geography, and whether the user wants a category, keyword, or product opportunity.
2. Establish the market baseline with `get_market_overview`. Request only the relevant boards and at most 30 history points.
3. Resolve exact category or keyword handles with `list_categories` or `search_keywords`.
4. Compare 3–8 candidates with compact report-only calls. Look for:
   - positive review or app growth;
   - page-one churn that makes entry plausible;
   - weak average ratings or an elevated low-rating ratio;
   - meaningful competition without a permanently locked top three.
5. Request ranked apps only for the strongest 2–3 candidates.
6. Inspect the leading apps and a bounded sample of their 1–2 star reviews. Separate a genuine shared unmet need from one app's isolated defect.
7. Use a live call only when the decision depends on today's Shopify state.
8. Rank opportunities with explicit evidence, confidence, risks, and the next cheapest validation step.

## Decision standard

Do not treat low app count alone as opportunity; it can mean no demand. Favor the intersection of demonstrated activity, dissatisfied buyers, contestable rankings, and a specific product wedge.

Distinguish:

- observed fact: returned directly by a tool;
- inference: supported interpretation of several facts;
- unknown: missing demand, revenue, install, or conversion evidence.

## Output

Lead with a build/no-build recommendation. Then provide:

1. a ranked opportunity table;
2. the evidence behind each score;
3. incumbent weaknesses and the proposed wedge;
4. risks and missing evidence;
5. a concrete validation plan.

Keep tool responses narrow and synthesize them. Never dump long app or review lists.
