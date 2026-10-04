---
name: add-broll
description: Get AI suggestions for B-roll footage to fill visual gaps in a video timeline using Pixabay stock media.
---

## Purpose

Automatically detect gaps between dialogue lines where B-roll footage should be inserted, extract visual concepts from surrounding dialogue context using Gemini AI, search Pixabay for matching stock imagery, and place the selected media on the timeline with appropriate transitions.

## Steps

1. **Detect dialogue gaps.** Call `findDialogueGaps(fps, totalFrames)` from `brollIntelligence.ts`. This:
   - Reads all dialogue lines from `useMultiCharacterStore`
   - Sorts by `startFrame` and finds gaps >= 1 second between consecutive lines
   - Also detects trailing gaps after the last line (capped at 3 seconds)
   - Returns `BrollGap[]` with `startFrame`, `endFrame`, `contextBefore`, `contextAfter` (clean dialogue text without emotion cues)

2. **Extract visual concepts.** Call `extractVisualConcepts(dialogueTexts)` from `brollIntelligence.ts`. This:
   - Sends gap context strings (combined before/after dialogue) to Gemini
   - Asks for 2-4 word stock footage search queries per gap
   - Returns `(string | null)[]` -- null for gaps with no clear visual concept
   - Falls back to `null` for all entries if Gemini API key is missing

3. **Search Pixabay.** The `useBrollStore.analyzeTranscript()` action orchestrates the full pipeline:
   - Calls `findDialogueGaps()` and `extractVisualConcepts()`
   - Creates `BrollSuggestion[]` with queries, gap frame ranges, and status
   - Searches Pixabay for each suggestion (rate-limited: 500ms between requests, max 2 concurrent)
   - Results are sorted by score (likes + views/100) and limited to top 5 per suggestion

4. **Review and customize suggestions.** Each `BrollSuggestion` has:
   - `query` -- the search query (editable)
   - `results` -- `BrollSearchResult[]` with thumbnail, preview, download URLs
   - `selectedIndex` -- which result is currently selected
   - `status` -- 'pending', 'accepted', or 'rejected'
   - `transition` -- media transition type (default: 'ken-burns')
   - Actions: `swapSuggestion(id, newIndex)`, `refreshSuggestion(id, newQuery)`, `setSuggestionTransition(id, transition)`

5. **Accept or reject suggestions.**
   - `acceptSuggestion(id)`: Downloads the selected image, adds it to `useMediaStore` as an asset, places it on the canvas at the gap's frame range with the chosen transition
   - `rejectSuggestion(id)`: Marks as rejected, skips placement

6. **Analyze topics (optional).** Call `analyzeSpeakerTopics(dialogueLines)` from `brollIntelligence.ts` for deeper analysis. Groups consecutive lines by topic using Gemini, returning `TopicGroup[]` with `topic`, `lineIndices`, `startFrame`, `endFrame`.

7. **Rank B-roll results.** Use `rankBrollSuggestions(hits, query, role)` from `brollIntelligence.ts` to score Pixabay results by landscape orientation (30%), resolution up to 1920px (40%), and popularity (30%).

## Key Files

- `src/services/brollIntelligence.ts` -- findDialogueGaps(), extractVisualConcepts(), analyzeSpeakerTopics(), rankBrollSuggestions(), BrollGap, TopicGroup types
- `src/stores/useBrollStore.ts` -- analyzeTranscript(), acceptSuggestion(), rejectSuggestion(), refreshSuggestion(), BrollSuggestion, BrollSearchResult types
- `src/services/pixabay.ts` -- Pixabay stock media API, searchImages()
- `src/stores/useMediaStore.ts` -- Media asset storage, addAsset(), addToCanvas()
- `src/components/panels/BrollSuggestionPanel.tsx` -- B-roll suggestion UI

## Common Issues

- **Gemini API key missing**: Visual concept extraction returns null for all entries. Suggestions fall back to generic "stock footage" queries.
- **Pixabay API key missing**: Search will fail. Set `VITE_PIXABAY_API_KEY` in environment.
- **Rate limiting**: Pixabay requests are rate-limited to 500ms intervals with max 2 concurrent. Large numbers of gaps will take time to populate.
- **No gaps detected**: If dialogue is continuous with no gaps >= 1 second, no suggestions are generated. Consider the `SilenceRemovalService` to create gaps by removing silences.
- **Image download CORS**: The `acceptSuggestion()` action downloads from `largeImageURL` directly. If CORS blocks, the download may fail.
- **Transition types**: Default is 'ken-burns'. Available transitions include: 'fade', 'zoom', 'slide', 'ken-burns' from `useMediaStore`.

## Examples

```typescript
// Full pipeline via store
const store = useBrollStore.getState()
await store.analyzeTranscript()

// Review suggestions
const suggestions = store.suggestions // BrollSuggestion[]
// Each has: query, results[], status, transition

// Swap to a different result
store.swapSuggestion(suggestions[0].id, 2) // select 3rd result

// Change search query and refresh
await store.refreshSuggestion(suggestions[0].id, 'sunset beach ocean')

// Accept a suggestion (downloads and places on timeline)
await store.acceptSuggestion(suggestions[0].id)

// Manual gap detection
import { findDialogueGaps, extractVisualConcepts } from '@/services/brollIntelligence'
const gaps = findDialogueGaps(30, totalFrames)
const queries = await extractVisualConcepts(gaps.map(g => g.contextBefore || ''))
```
