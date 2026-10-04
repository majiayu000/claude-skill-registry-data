---
name: analyze-trend
description: Detect trending topics and content opportunities using the trend spotter service for content ideation.
---

# Analyze Trends

Detect trending topics and content opportunities for short-form video creation using Gemini with Google Search grounding, with curated fallback defaults per niche.

## Purpose

Help creators discover what topics are trending right now so they can create timely, relevant content. The trend spotter identifies trending topics, provides hashtags, suggests video formats, and generates ready-to-use orchestrator prompts.

## Steps

1. **Choose a niche** for trend detection:
   - Available niches: `general`, `tech`, `business`, `health`, `entertainment`, `education`.
   - Each niche has curated fallback defaults with pre-written topics, hashtags, and orchestrator prompts.
   - Custom niches can also be passed -- Gemini will search for trends in that space.

2. **Fetch trends** via `fetchTrends(niche)`:
   - If `VITE_GEMINI_API_KEY` is set: calls Gemini with Google Search grounding (`tools: [{ googleSearch: {} }]`) to find 5-7 currently trending topics.
   - If no API key: returns curated defaults from `CURATED_DEFAULTS` immediately.
   - The API call is credit-gated via `withCreditGate('gemini-script', ...)`.
   - Uses the proxy URL `/api/proxy/gemini/gemini-3.1-flash-lite-preview` first, falls back to direct Gemini API.

3. **Understand the TrendItem structure**:
   - `topic` -- the trending topic/theme (e.g., "AI Tools Everyone Should Know").
   - `description` -- why it is trending (e.g., "AI productivity tools are reshaping how people work").
   - `hashtags` -- 3-5 relevant hashtags (e.g., `["#AI", "#Productivity", "#Tech"]`).
   - `suggestedFormat` -- recommended video format: `educational`, `entertainment`, `commentary`, `how-to`, `debate`.
   - `trendScore` -- virality/timeliness score (0-100). Higher = more trending.
   - `orchestratorPrompt` -- ready-to-use prompt for the AI orchestrator. Can be directly passed to `useOrchestratorStore.setPrompt()`.

4. **Use trends for content creation**:
   - Select a trend and use its `orchestratorPrompt` directly with the AI Director.
   - Or customize the prompt based on the topic and description.
   - Hashtags can be used for social media publishing metadata.
   - `suggestedFormat` guides the orchestrator's creative direction.

5. **Understand the Brand Director integration**:
   - `brandDirector.ts` extends trend detection with business-specific context.
   - `fetchNicheTrends(keywords, industry, niche)` combines:
     - n8n + Apify scraped data (real YouTube videos with engagement metrics).
     - Fallback: YouTube API + Gemini search grounding.
   - Returns `TrendData` with `items[]` containing author, engagement, and virality evidence.

6. **Curated defaults per niche** (used when API is unavailable):
   - General: AI tools, life hacks, morning routines, money mistakes, science facts.
   - Tech: AI coding assistants, free APIs, open source alternatives, phone tips, wearable tech.
   - Business: side hustles, personal branding, startup mistakes.
   - Health: desk stretches, sleep hygiene, gut health.
   - Entertainment: movie explanations, video game easter eggs, celebrity facts.
   - Education: study techniques, bite-sized history, psychology tricks.

## Key Files

| Purpose | Path |
|---------|------|
| Trend spotter service | `src/services/trendSpotter.ts` |
| Trend store | `src/stores/useTrendStore.ts` |
| Trend panel UI | `src/components/panels/TrendPanel.tsx` |
| Brand director service | `src/services/brandDirector.ts` |
| Brand director store | `src/stores/useBrandDirectorStore.ts` |
| Brand intel page | `src/components/pages/BrandIntelPage.tsx` |
| Brand intel store | `src/stores/useBrandIntelStore.ts` |
| Creative intelligence | `src/services/creativeIntelligence.ts` |

## Common Issues

- **Trends always return defaults**: `VITE_GEMINI_API_KEY` is not set or is invalid. Check the `.env` file.
- **Gemini returns no trends**: The API response parsing failed. The service expects JSON with a `trends` array. If Gemini wraps output in markdown fences, parsing fails.
- **Stale trends**: `TrendResults.fetchedAt` timestamp shows when trends were last fetched. Trends are cached in `useTrendStore` -- call `fetchTrends()` again to refresh.
- **n8n trends fail**: The n8n + Apify integration requires a running n8n instance with the correct workflow configured. Falls back to YouTube API + Gemini.
- **Credit gate blocks trend fetch**: The user has insufficient credits. Curated defaults are returned as fallback.
- **orchestratorPrompt does not produce good results**: The prompts are generic templates. Customize with specific details about target audience, style preferences, or character names.

## Examples

Fetch trending topics:
```ts
import { fetchTrends } from '@/services/trendSpotter'
const results = await fetchTrends('tech')
results.trends.forEach(t => {
  console.log(`[${t.trendScore}] ${t.topic}`)
  console.log(`  Format: ${t.suggestedFormat}`)
  console.log(`  Hashtags: ${t.hashtags.join(' ')}`)
})
```

Use a trend with the orchestrator:
```ts
import { fetchTrends } from '@/services/trendSpotter'
import { useOrchestratorStore } from '@/stores/useOrchestratorStore'

const { trends } = await fetchTrends('general')
const topTrend = trends[0]
useOrchestratorStore.getState().setPrompt(topTrend.orchestratorPrompt)
await useOrchestratorStore.getState().generatePlan()
```

Fetch brand-specific trends:
```ts
import { fetchNicheTrends } from '@/services/brandDirector'
const trendData = await fetchNicheTrends(
  ['SaaS', 'B2B', 'productivity'],
  'software',
  'tech'
)
console.log('Trend items:', trendData.items.length)
```
