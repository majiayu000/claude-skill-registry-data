---
name: smart-cut
description: Detect and remove silences, filler words, and dead space from video/audio using AI silence detection.
---

## Purpose

Analyze audio to detect silence regions and filler words ("um", "uh", "like", "you know", etc.), then remove them from the timeline. This tightens pacing and improves viewer retention. Two detection systems work together: RMS energy analysis for silences and word-matching against alignment timestamps for fillers.

## Steps

1. **Prepare audio for analysis.** Decode the audio blob into an `AudioBuffer` using `decodeAudioBlob(blob)` from `silenceDetection.ts`. This uses the Web Audio API's `AudioContext.decodeAudioData()`.

2. **Run combined detection.** Call `detectAll(audioBuffer, words, settings)` from `silenceDetection.ts` which runs both detectors and merges results:
   - **Silence detection**: `detectSilences(audioBuffer, settings)` analyzes 50ms windows of RMS energy. Regions where energy falls below `silenceThresholdDb` (default -40dB) for longer than `minSilenceDuration` (default 0.4s) are flagged.
   - **Filler word detection**: `detectFillerWords(words, fillerList)` matches word timestamps against a configurable filler list. Supports single-word ("um") and multi-word ("you know") fillers.

3. **Configure detection settings.** The `DetectionSettings` object controls:
   - `silenceThresholdDb`: dB below peak to consider as silence (default -40)
   - `minSilenceDuration`: minimum silence duration in seconds (default 0.4)
   - `fillerWords`: array of filler words/phrases to detect (default includes: um, uh, uhm, hmm, like, you know, basically, actually, so, right, i mean)

4. **Review detected regions.** Results are `SilenceRegion[]` with `id`, `type` ('silence' or 'filler'), `startTime`, `endTime`, `word` (for fillers), and `enabled` (toggle for inclusion). The store provides filtering by mode: 'all', 'silence', or 'fillers'.

5. **Preview and toggle regions.** Use `useSmartCutStore`:
   - `toggleRegion(regionId)` -- enable/disable individual regions
   - `toggleAll(enabled)` -- bulk enable/disable
   - `setFilterMode(mode)` -- filter display by type

6. **Apply smart cut.** Call `useSmartCutStore.getState().applySmartCut()` which:
   - Sorts enabled regions by start time
   - Trims dialogue lines that contain removed regions
   - Cascades frame shifts -- subsequent content shifts earlier by cumulative removed duration
   - Reduces total timeline frames
   - Clears regions after applying

7. **Alternative: SilenceRemovalService.** For transcript-based removal (using Whisper word timestamps), use `getSilenceRemovalService().analyzeTranscript(words, mode, fps)` from `silenceRemoval.ts`. This offers three speed modes:
   - `natural`: threshold 1.5s (only long pauses)
   - `fast`: threshold 0.8s (noticeable pauses)
   - `extra-fast`: threshold 0.3s + filler word removal
   - Returns `AnalysisResult` with `silences`, `fillers`, `totalRemovedSec`, and `edits` (TimelineEdit[] for direct timeline application)

## Key Files

- `src/services/silenceDetection.ts` -- detectSilences(), detectFillerWords(), detectAll(), decodeAudioBlob(), SilenceRegion, DetectionSettings, DEFAULT_SETTINGS
- `src/services/silenceRemoval.ts` -- SilenceRemovalService, analyzeTranscript(), RemovalMode, TimelineEdit
- `src/stores/useSmartCutStore.ts` -- analyzeAudio(), toggleRegion(), applySmartCut(), detection state management
- `src/components/panels/SmartCutPanel.tsx` -- Smart cut UI
- `src/components/panels/SilenceRemovalPanel.tsx` -- Silence removal panel UI

## Common Issues

- **Threshold too aggressive**: Default -40dB catches most silences. For noisy recordings, lower to -35dB or -30dB. For clean studio audio, -45dB or -50dB works better.
- **Short silences missed**: Increase `minSilenceDuration` threshold. Natural speech has ~200ms pauses between words that should not be removed.
- **Filler detection false positives**: Words like "so" and "like" have legitimate uses. Review detected fillers before applying. The `enabled` toggle lets users exclude false positives.
- **Frame shift cascading**: After applying cuts, all subsequent content shifts earlier. This affects dialogue lines, text overlays, and any frame-based elements. Only dialogue lines are auto-adjusted; other elements may need manual repositioning.
- **Minimum gap preserved**: `SilenceRemovalService` keeps a 75ms gap (`MIN_GAP_SEC`) between clips after removal for natural breathing room.

## Examples

```typescript
// Web Audio-based detection
import { detectAll, decodeAudioBlob, DEFAULT_SETTINGS } from '@/services/silenceDetection'

const audioBuffer = await decodeAudioBlob(audioBlob)
const regions = detectAll(audioBuffer, wordTimestamps, {
  ...DEFAULT_SETTINGS,
  silenceThresholdDb: -35,
  minSilenceDuration: 0.5,
})

// Transcript-based detection
import { getSilenceRemovalService } from '@/services/silenceRemoval'

const service = getSilenceRemovalService()
const result = service.analyzeTranscript(whisperWords, 'fast', 30)
// result.totalRemovedSec, result.edits (TimelineEdit[])

// Store-based workflow
const store = useSmartCutStore.getState()
await store.analyzeAudio(audioBlob, wordTimestamps)
// Review regions, toggle as needed, then:
store.applySmartCut()
```
