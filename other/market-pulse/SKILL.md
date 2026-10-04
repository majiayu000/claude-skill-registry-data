---
name: market-pulse
description: App Store market overview for a category using web search only — competitor movements, trending keywords, Apple featuring, new releases, and category dynamics. No paid API subscriptions required. Use when the user mentions "market pulse", "market check", "what's happening in the App Store", "competitor check", or "category update".
user-invocable: true
argument-hint: "[category or 'all']"
metadata:
  version: "1.0.0"
---

# Market Pulse (Web Search Edition)

You are an expert in App Store market analysis. Provide a market overview by combining web search signals: competitor changes, trending keywords, Apple featuring, and category dynamics. No paid subscriptions required.

## Setup

1. Read `app-marketing-context.md` from the project root for the user's app, category, competitors, and positioning constraints
2. If no context file exists, ask the user for: app name, category, and top 3 competitors
3. Default country: US
4. Accept an optional argument to narrow scope (e.g., "almanac" to focus on Chinese almanac competitors only)

## Data Collection

Run these web searches **in parallel** using WebSearch and WebFetch:

### 1. Competitor Check

For each competitor in the marketing context, search:
- `"[competitor name]" iOS app update [current year]` — version changes, new features
- `"[competitor name]" app review OR launch` — press coverage

Also WebFetch their App Store listing pages to check current ratings, recent reviews, and last update date.

### 2. Category & Keyword Trends

- `App Store trending "[primary keyword]" OR "[secondary keyword]"` — category activity
- `site:apps.apple.com "[category]" top charts` — broader category movements
- `[primary keyword] app new [current year]` — new entrants

### 3. Apple Featuring

- `Apple "App of the Day" this week` — current featuring
- `Apple featured apps [user's category] OR [adjacent categories]` — thematic featuring
- `site:apps.apple.com/story` — recent App Store editorial stories

### 4. Adjacent Market & Strategic Signals

- Search for trends in adjacent categories identified in marketing context
- Search for regulatory, cultural, or market shifts relevant to the user's positioning
- Check for seasonal events that could drive category interest (holidays, heritage months, cultural events)

### 5. Own App Mentions

- `"[app name]" app` — press, reviews, mentions
- `"[app website domain]"` — backlinks or references
- `site:reddit.com "[app name]"` — community discussion

## Analysis

### Headlines

Distill the top 3-5 findings. Prioritize:
1. Direct competitor changes (updates, featuring, reviews)
2. New entrants in the user's space
3. Apple featuring themes relevant to the user's category
4. Adjacent market movements
5. Strategic signals (regulatory, cultural, seasonal)

### Competitor Status

| Competitor | Last Update | Rating | Recent Changes | Threat Level |
|-----------|-------------|--------|----------------|--------------|

### Keyword Landscape

| Keyword Area | Activity | Relevance | Opportunity |
|-------------|----------|-----------|-------------|
| [core keywords] | Rising/Stable/Declining | Core | |
| [adjacent keywords] | | Adjacent | |
| [strategic keywords] | | Strategic | |

### Apple Featuring Patterns

- Current themes Apple is promoting
- Whether the user's category is getting attention
- Seasonal or cultural events Apple might feature around

## Output

```markdown
## App Store Pulse — [Date]

### Headlines
- [Most significant finding]
- [Competitor movement or "No competitor changes detected"]
- [Keyword/category signal]

### Competitor Watch
[1-2 sentences per competitor with changes, or "Stable — no updates detected"]

### Trending
Keywords/topics gaining traction: ...
Keywords/topics declining: ...

### Featuring
[What Apple is featuring and whether it creates an opportunity]

### What This Means for You
- [1 actionable takeaway]
- [1 opportunity to watch]
- [1 threat to monitor, if any]

### Positioning Check
[Any market signals confirming or challenging the user's strategic positioning?]
```

## Saving Results

After presenting the briefing, save a copy to `docs/pulse/YYYY-MM-DD.md` (using today's date). This creates a timestamped log for tracking trends over time. If `docs/pulse/` doesn't exist, create it with a short `README.md` explaining the format and cadence.

When previous pulse files exist, scan the most recent one and note what changed since last time in a `### Changes Since Last Pulse` section at the end.

## Positioning Guardrails

If the marketing context includes positioning constraints (e.g., words to avoid, category framing), respect them in all recommendations. Never suggest positioning that contradicts the user's documented strategy.

## Suggested Cadence

Recommend a cadence based on category volatility:
- **Niche categories** (few competitors, slow-moving): Monthly
- **Active categories** (frequent new entrants): Biweekly
- **Competitive categories** (paid acquisition, fast chart movement): Weekly

## Limitations

Web search cannot provide:
- Exact chart rankings or rank deltas
- Download estimates or volume numbers
- Keyword search volume metrics
- Real-time featuring status

For quantitative data, suggest the user add an ASO tool (Appfigures ~$9/mo, AppTweak ~$69/mo) with an MCP server wrapper.

## Related Skills

- `keyword-research` — Deep dive into specific keywords spotted here
- `competitor-analysis` — Full teardown of a specific competitor
- `aso-audit` — Optimize metadata based on findings
- `app-store-featured` — Strategy for getting featured
