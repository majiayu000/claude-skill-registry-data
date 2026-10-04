---
name: extract-clips
description: Extract and rank short clips from long-form video content for repurposing as shorts, reels, or TikToks.
argument-hint: <source-video>
---

## Purpose

Analyze a long-form video transcript and identify the 3-5 best standalone segments for repurposing as short-form content (30-90 seconds each). Uses Gemini AI to find viral-worthy moments, then ranks clips using a composite scoring system that combines virality, visual interest, audio energy, and hook potential.

## Steps

1. **Transcribe the source video.** Upload the video/audio file using `transcribeAudio(file, options)` from `whisperTranscript.ts`. Supported providers: 'whisper' (default), 'deepgram', 'assemblyai'. Returns `WhisperResult` with `segments`, `words`, `text`, `language`, and `duration`.

2. **Extract best clips.** Call `extractBestClips(segments, totalDuration)` from `clipExtractor.ts`. This:
   - Formats the transcript with timestamps (e.g., `[1:23] text...`)
   - Sends to Gemini 2.0 Flash asking for 3-5 best standalone segments
   - Requests JSON with: title (max 8 words), hookRewrite (attention-grabbing first sentence), startTime/endTime, viralityScore (0-100), reason
   - Falls back from server proxy to direct API if proxy unavailable
   - Returns `ExtractedClip[]` sorted by virality score descending

3. **Rank clips with composite scoring.** Call `rankClips(clips)` from `clipRanker.ts`. Scoring weights:
   - **Virality score** (35%): From Gemini analysis (0-100)
   - **Visual interest** (20%): Based on scene transition count (`sceneTransitions * 25 + 40`, capped at 100)
   - **Audio energy** (25%): Based on emotional arc -- climax=90, rising=75, falling=40, flat=30
   - **Hook potential** (20%): 80 if `hookRewrite` exists, else 50
   - Returns `ClipRank[]` with `compositeScore` and per-signal `breakdown`

4. **Rewrite clip hooks.** For any clip, call `rewriteClipHook(clip)` from `clipExtractor.ts` to get a Gemini-rewritten opening line that is more attention-grabbing. Uses temperature 0.7 for creative variation.

5. **Preview and select.** Each `ExtractedClip` includes:
   - `id` -- unique clip identifier
   - `title` -- catchy title (max 8 words)
   - `hookRewrite` -- rewritten opening sentence
   - `startTime` / `endTime` / `duration` -- exact time bounds
   - `viralityScore` -- 0-100 score from AI analysis
   - `segments` -- matching `WhisperSegment[]` within the time range
   - `reason` -- explanation of why this segment works
   - Optional: `thumbnailDataUrl`, `videoPreviewUrl`, `sceneTransitions`, `emotionalArc`

6. **Export selected clips.** Use the start/end timestamps to slice the original video. The clips can be imported as new ProAnimate projects or exported directly.

## Key Files

- `src/services/clipExtractor.ts` -- extractBestClips(), rewriteClipHook(), ExtractedClip type
- `src/services/clipRanker.ts` -- rankClips(), ClipRank type, composite scoring logic
- `src/services/whisperTranscript.ts` -- transcribeAudio(), transcribeFromUrl(), WhisperResult, WhisperSegment, WhisperWord
- `src/components/panels/ClipExtractionPanel.tsx` -- Clip extraction UI
- `src/components/panels/ClipExtractorPanel.tsx` -- Clip extractor UI

## Common Issues

- **Gemini API key required**: Both extraction and hook rewriting need `VITE_GEMINI_API_KEY`. The service tries a server proxy first, falls back to direct API.
- **Credit gating**: Both `extractBestClips()` and `rewriteClipHook()` are wrapped in `withCreditGate('gemini-script', ...)`.
- **Clip boundaries may be imprecise**: Gemini estimates timestamps from transcript text, not audio analysis. Clips may need minor manual adjustment at boundaries.
- **Short source content**: Works best on 5+ minute source videos. Very short content (under 2 minutes) may not yield meaningful clips.
- **Proxy fallback**: The service first tries `/api/proxy/gemini/gemini-2.0-flash`, then falls back to direct Gemini API. Ensure one path is available.

## Examples

```typescript
import { transcribeAudio } from '@/services/whisperTranscript'
import { extractBestClips, rewriteClipHook } from '@/services/clipExtractor'
import { rankClips } from '@/services/clipRanker'

// Transcribe
const transcript = await transcribeAudio(videoFile, { provider: 'whisper' })

// Extract clips
const clips = await extractBestClips(transcript.segments, transcript.duration)

// Rank with composite scoring
const ranked = rankClips(clips)
// ranked[0].compositeScore, ranked[0].breakdown.viralityScore, etc.

// Rewrite a hook for the best clip
const betterHook = await rewriteClipHook(clips[0])
```
