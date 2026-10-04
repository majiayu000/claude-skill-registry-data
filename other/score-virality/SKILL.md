---
name: score-virality
description: Analyze a clip's virality potential with scoring across multiple dimensions. Uses Web Worker for real-time scoring.
---

# Score Virality

Analyze a ProAnimate clip's viral potential using both client-side heuristic scoring (instant, free) and AI-powered deep analysis (Gemini with Google Search grounding).

## Purpose

Score a clip across multiple virality dimensions (hook strength, pacing, trend relevance, emotion, visual quality, rewatch value) to help creators optimize their content for maximum engagement. The system provides actionable improvement suggestions.

## Steps

1. **Understand the two scoring modes**:
   - **Client-side heuristic** (`viralityScoreWorker.ts`): instant, free, runs in a Web Worker. Scores across 9 weighted factors totaling 0-100 points.
   - **AI-powered deep analysis** (`viralityScorer.ts`): uses Gemini with Google Search grounding for trend matching. Costs credits. Returns per-dimension scores (0-100) and specific improvement suggestions.
   - **Fast client analyzer** (`viralityAnalyzer.ts`): intermediate analysis with dimension-level scoring (hook, pacing, emotion, engagement, platform fit, shareability) computed from store data.

2. **Client-side scoring breakdown** (max 100 points):
   - Hook strength (0-15): text/CTA in first 3 seconds, opening visual present.
   - Pacing (0-10): cuts/transitions detected (scene changes).
   - Captions (0-10): captions enabled (any style except 'none').
   - Audio (0-15): voice audio present + background music present.
   - Aspect ratio (0-10): 9:16 for short-form platforms.
   - Duration (0-10): optimal range 15-60 seconds.
   - Text overlays (0-10): at least one text overlay present.
   - Character animation (0-10): at least one character.
   - B-roll / media variety (0-10): stock media or SVG objects present.

3. **Gather clip metadata** for scoring:
   - `ClipMetadata` interface requires: `durationSeconds`, `dialogueCount`, `characterCount`, `textOverlayCount`, `hasCTA`, `hasHook`, `captionStyle`, `aspectRatio`, `hasMusic`, `templateCount`, `svgObjectCount`, `stockMediaCount`, `topics[]`.
   - Extended fields: `hookStrengthFirstThreeSeconds` (0-100), `cutsPerMinute`, `averageLineDuration`, `hasOpeningVisual`, `trendKeywords[]`.
   - Metadata is extracted from Zustand stores: `useMultiCharacterStore`, `useTextOverlayStore`, `useMediaStore`, `useHTMLTemplateLayerStore`, `useSVGObjectStore`, `useTimelineStore`.

4. **State hashing for change detection** (`viralityStateHash.ts`):
   - `computeProjectStateHash()` computes a lightweight djb2 hash of project state.
   - Includes: dialogue count/text, overlay count/types, character count, duration, template IDs, media IDs.
   - Re-scoring only triggers when the hash changes, avoiding unnecessary API calls.
   - Hash is sub-millisecond performance.

5. **Run AI-powered scoring** (`viralityScorer.ts`):
   - `scoreClipVirality(metadata, prompt)` calls Gemini with the clip metadata.
   - Uses `responseMimeType: 'application/json'` for structured output.
   - Enables `tools: [{ googleSearch: {} }]` for real-time trend matching.
   - Returns: `overall` (0-100), `dimensions` (hook, pacing, trend, emotion, visual, rewatch), `suggestions[]`.
   - Gated by credit system via `withCreditGate('virality-score', ...)`.

6. **Run fast client analysis** (`viralityAnalyzer.ts`):
   - `ViralityAnalysisInput` is gathered from stores.
   - Scores per dimension:
     - Hook strength: penalizes generic openers ("hey", "welcome"), rewards questions, numbers, bold claims.
     - Visual pacing: scene changes per 10 seconds (optimal 2-5), template usage, stock media presence.
     - Emotional arc: emotion variety count (4+ is best), mood shift detection.
     - Engagement: CTA presence, caption style, dialogue line count.
     - Platform fit: aspect ratio and duration vs. platform requirements.
     - Shareability: topic keywords analysis.
   - Returns `ViralityAnalysis` with dimensions, improvements, and overall score.

7. **Interpret improvement suggestions**:
   - Each `ViralityImprovement` has: `dimension`, `priority`, `description`, `estimatedImpact`.
   - Improvements are sorted by priority (highest impact first).
   - Common suggestions: add a text hook in first 2 seconds, include trending topic reference, add CTA, increase visual variety.

## Key Files

| Purpose | Path |
|---------|------|
| Client-side heuristic scorer | `src/services/viralityScoreWorker.ts` |
| AI-powered scorer (Gemini) | `src/services/viralityScorer.ts` |
| Fast client analyzer | `src/services/viralityAnalyzer.ts` |
| State hash for change detection | `src/services/viralityStateHash.ts` |
| Virality types | `src/types/virality.ts` |
| Orchestrator ViralScore type | `src/types/orchestrator.ts` |
| Virality store | `src/stores/useViralityStore.ts` |
| Virality panel UI | `src/components/panels/ViralityPanel.tsx` |
| Virality score panel UI | `src/components/panels/ViralityScorePanel.tsx` |
| Auto virality score hook | `src/hooks/useAutoViralityScore.ts` |
| Server virality analysis | `server/routes/viralityAnalysis.ts` |

## Common Issues

- **Score always 0 or very low**: The clip has minimal content. Check that dialogue, characters, and text overlays exist in the stores.
- **State hash does not change**: The hash only checks specific store fields. Adding a shape or changing a color may not trigger re-scoring.
- **Gemini scoring fails**: API key missing (`VITE_GEMINI_API_KEY`) or quota exceeded. Falls back to client-side scoring.
- **Google Search grounding unavailable**: Not available in all regions. The scorer still works without it but cannot match trending topics.
- **Score seems inaccurate**: Client-side heuristics are rule-based and cannot evaluate content quality. Use AI-powered scoring for nuanced analysis.
- **Web Worker not responding**: The Web Worker may have crashed. Check browser console for worker errors. Terminate and re-create the worker.

## Examples

Run client-side scoring:
```ts
import { scoreClientSide } from '@/services/viralityScoreWorker'
const result = scoreClientSide({
  durationSeconds: 30, dialogueCount: 5, characterCount: 1,
  textOverlayCount: 2, hasCTA: true, hasHook: true,
  captionStyle: 'word-by-word', aspectRatio: '9:16',
  hasMusic: true, templateCount: 1, svgObjectCount: 0,
  stockMediaCount: 2, topics: ['AI', 'productivity'],
  hookStrengthFirstThreeSeconds: 80, cutsPerMinute: 6,
  averageLineDuration: 3, hasOpeningVisual: true, trendKeywords: ['AI tools'],
})
console.log('Score:', result.score.overall, 'Factors:', result.factors)
```

Check if re-scoring is needed:
```ts
import { computeProjectStateHash } from '@/services/viralityStateHash'
const hash = computeProjectStateHash()
// Compare with previously stored hash to detect changes
```
