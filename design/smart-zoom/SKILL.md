---
name: smart-zoom
description: Apply AI-powered Ken Burns zoom effects with automatic focus detection and subject tracking.
---

## Purpose

Automatically generate camera zoom keyframes at emphasis points in a video, creating dynamic Ken Burns-style zoom effects. Uses a combination of rule-based heuristics (sentence starts, punctuation, topic transitions) and optional AI analysis (Gemini-based semantic emphasis detection) to find the best moments to zoom.

## Steps

1. **Transcribe the audio.** Smart zoom requires a transcript with word-level timestamps. Use Whisper/Deepgram/AssemblyAI via `transcribeAudio()` from `whisperTranscript.ts` to get `WhisperSegment[]` and `WhisperWord[]`.

2. **Configure zoom settings.** Create a `SmartZoomConfig` object:
   - `style`: zoom animation style -- 'smooth' (ease-in-out), 'crash' (instant jump), 'expo' (accelerating), or 'linear'
   - `frequency`: how many zooms -- 'conservative' (top 20%), 'moderate' (top 50%), 'aggressive' (top 80%)
   - `intensity`: global intensity multiplier (0-1)
   - `maxZoom`: maximum zoom level (e.g., 1.3 = 130%)
   - `useAI`: enable Gemini-based semantic analysis (optional)
   - `includeEmphasis`, `includePunctuation`, `includeTopicTransitions`, `includeSpeakerChanges`: toggle heuristic detectors

3. **Analyze for zoom points.** Call `getSmartZoomService().analyzeForZoom(segments, words, config, fps)`. This runs heuristic detection then optionally AI detection:

   **Heuristic detectors** (`smartZoomHeuristics.ts`):
   - `detectSentenceStarts()` -- zoom at segment boundaries (intensity 0.5)
   - `detectExclamations()` -- zoom on `!` marks (intensity 0.9)
   - `detectQuestions()` -- zoom on `?` marks (intensity 0.6)
   - `detectKeywords()` -- zoom on configurable keyword list (intensity 0.7)
   - `detectTopicTransitions()` -- zoom when gap > 2s between segments (intensity 0.6)
   - `detectSpeakerChanges()` -- zoom on speaker changes (intensity 0.3)

   **AI detector** (`smartZoomAI.ts`):
   - Sends transcript text to Gemini asking for 5-10 most dramatic moments
   - Returns timestamps with intensity (0.5-1.0) and reasons
   - Merges with heuristic points, deduplicates within 1 second

   **Post-processing**:
   - Deduplicates points within 1 second (keeps higher intensity)
   - Enforces minimum 2-second spacing between zooms
   - Filters by frequency setting (keeps top N% by intensity)

4. **Generate camera keyframes.** Call `service.generateCameraKeyframes(zoomPoints, config, fps, totalFrames)`. Each zoom point produces keyframes based on the selected style:
   - **smooth**: 500ms ease-in-out zoom, 330ms hold, 660ms ease-in-out return
   - **crash**: 1-frame instant jump, 170ms hold, 500ms ease-out return
   - **expo**: 330ms accelerating zoom, 170ms hold, 660ms ease-out return
   - **linear**: 660ms linear zoom, 330ms hold, 660ms linear return
   - Each zoom includes a subtle random pan offset (+-3%) for visual interest

5. **Apply to camera store.** Write the generated `CameraKeyframe[]` to `useCameraStore`. Keyframes include `frame`, `zoom`, `panX`, `panY`, `rotation`, `easing`, and are tagged with `'smart-zoom'` for easy identification and removal.

## Key Files

- `src/services/smartZoom.ts` -- SmartZoomService class, analyzeForZoom(), generateCameraKeyframes(), zoom style keyframe generation
- `src/services/smartZoomAI.ts` -- detectEmphasisWithAI(), Gemini-based semantic analysis
- `src/services/smartZoomHeuristics.ts` -- detectAllHeuristic(), sentence/punctuation/keyword/topic/speaker detection functions
- `src/types/smartZoom.ts` -- ZoomPoint, SmartZoomConfig, ZoomStyle, ZoomTriggerType types
- `src/stores/useCameraStore.ts` -- Camera keyframe state, CameraKeyframe type
- `src/components/panels/SmartZoomPanel.tsx` -- Smart zoom configuration UI

## Common Issues

- **Too many zooms**: Use 'conservative' frequency or increase minimum spacing. Max 1 zoom per 2 seconds is enforced by default.
- **AI detection fails**: Falls back silently to heuristics only. Requires `VITE_GEMINI_API_KEY`. The catch block logs a warning but does not throw.
- **Zoom too intense**: Lower `config.intensity` (0-1 multiplier) or reduce `config.maxZoom` (1.0 = no zoom). The actual zoom is calculated as `1 + (maxZoom - 1) * point.intensity * config.intensity`.
- **Crash zoom too jarring**: Switch to 'smooth' or 'expo' style. Crash zooms are 1-frame instant and work best for high-energy content.
- **No transcript available**: Smart zoom requires word-level timestamps. Transcribe the audio first using the transcript service.

## Examples

```typescript
import { getSmartZoomService } from '@/services/smartZoom'

const service = getSmartZoomService()

// Analyze transcript for zoom points
const zoomPoints = await service.analyzeForZoom(segments, words, {
  style: 'smooth',
  frequency: 'moderate',
  intensity: 0.7,
  maxZoom: 1.25,
  useAI: true,
  includeEmphasis: true,
  includePunctuation: true,
  includeTopicTransitions: true,
  includeSpeakerChanges: false,
}, 30)

// Generate camera keyframes
const keyframes = service.generateCameraKeyframes(zoomPoints, config, 30, totalFrames)
// Apply to camera store
```
