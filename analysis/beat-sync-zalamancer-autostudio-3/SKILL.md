---
name: beat-sync
description: Synchronize video cuts, transitions, and animations to audio beats using beat detection and tempo analysis.
---

## Purpose

Detect beats in audio, estimate BPM, and synchronize visual elements (text, shapes, media) to the beat grid. Two levels of beat sync exist: a service-level system for the timeline (`beatSync.ts` in services) and an engine-level system for the animation engine (`beatSync.ts` in engine). The beat detection service uses Web Audio API spectral flux analysis.

## Steps

1. **Analyze audio for beats.** Call `detectBeatsFromUrl(audioUrl)` from `beatDetection.ts`. This:
   - Fetches and decodes the audio into an `AudioBuffer`
   - Computes spectral flux using energy-based analysis (2048 FFT, 512 hop)
   - Detects onsets via adaptive thresholding (local average * 1.5, min 100ms gap)
   - Estimates BPM using inter-onset interval histogram (60-200 BPM range)
   - Builds a phase-aligned beat grid by testing 16 phase offsets against detected onsets
   - Computes energy segments (4-second windows) with average and peak energy
   - Returns `BeatAnalysis` with `bpm`, `beats[]` (seconds), `onsets[]`, `segments[]`, `duration`

2. **Fine-tune detection.** Use `redetectWithSensitivity(audioUrl, sensitivity, manualBpm?)` to adjust:
   - `sensitivity` (0-1): Higher = more beats detected (lower onset threshold). Default 0.5.
   - `manualBpm`: Override auto-detected BPM while keeping phase alignment
   - The store also supports `beatGridOffset` to shift all beat positions

3. **Configure per-object sync.** In `useBeatSyncStore`, set up `ObjectBeatSyncConfig` for each canvas element:
   - `objectRef`: `{ objectType, objectId }` -- which element to sync
   - `effect`: 'scale-pulse', 'opacity-flash', or 'bounce'
   - `subdivision`: 1 (every beat), 2 (every other), or 4 (every 4th)
   - `offset`: time offset in seconds
   - `intensity`: effect strength (0-1)

4. **Apply beat sync keyframes.** Call `useBeatSyncStore.getState().applyObjectBeatSync(configs, fps, clipRanges)`. This:
   - Converts beat timestamps to frame numbers
   - Reads base property values from native stores (text size, shape dimensions, etc.)
   - Generates keyframes using `generateObjectBeatKeyframes()` from `beatSync.ts` (service)
   - Writes keyframes to `useKeyframeStore` tagged with `'beat-sync'` for easy removal
   - Stores the FPS used for later recalculation on FPS changes

5. **Engine-level beat sync.** The animation engine (`src/engine/beatSync.ts`) provides lower-level utilities:
   - `detectBeats(audioBuffer, { sensitivity, minInterval })` -- simple energy-based beat detection
   - `estimateBPM(beats)` -- median-interval BPM estimation
   - `generateBeatsFromBPM(bpm, durationSeconds, offset)` -- generate beats from known BPM
   - `generateBeatKeyframes(beats, objectRef, config, fps)` -- create keyframes with effect types: 'scale-pulse', 'opacity-flash', 'bounce'
   - `snapToBeat(frame, bpm, fps)` -- snap a frame to nearest beat position
   - `beatsToFrames(beats, bpm, fps)` -- convert musical beats to frame count
   - `getBeatFramesInRange(start, end, bpm, fps, subdivision, offset)` -- get all beat frames in a range

6. **Visualize beats.** Set `useBeatSyncStore.showBeatMarkers = true` to display beat markers on the timeline. The store also pre-computes `waveformData` (downsampled to 400 points) for visualization.

7. **Bridge to animation engine.** `beatAnalysisToEngineBeats(analysis)` in `soundDesigner.ts` converts `BeatAnalysis` to the engine's `Beat[]` format, enriching with strength from energy segments and marking downbeats using BPM-derived measure positions.

## Key Files

- `src/services/beatDetection.ts` -- detectBeats(), detectBeatsFromUrl(), redetectWithSensitivity(), computeFrequencyBands(), BeatAnalysis, BeatSegment
- `src/services/beatSync.ts` -- snapToNearestBeat(), generatePulseKeyframes(), generateObjectBeatKeyframes(), BeatSyncOptions (service-level)
- `src/engine/beatSync.ts` -- detectBeats(), estimateBPM(), generateBeatKeyframes(), snapToBeat(), beatsToFrames(), getBeatFramesInRange(), Beat, BeatSyncConfig (engine-level)
- `src/stores/useBeatSyncStore.ts` -- analyzeAudio(), applyObjectBeatSync(), clearObjectBeatSync(), sensitivity/BPM/offset controls, FPS recalculation
- `src/services/soundDesigner.ts` -- beatAnalysisToEngineBeats() bridge function
- `src/components/panels/BeatSyncPanel.tsx` -- Beat sync configuration UI

## Common Issues

- **BPM detection inaccurate**: The histogram-based approach works best for rhythmic music. For ambient/non-rhythmic audio, manually set BPM via `setManualBpm()`.
- **Beat grid misaligned**: Use `setBeatGridOffset(seconds)` to shift all beats. Small adjustments of 0.05-0.1s often fix phase issues.
- **Too many/few beats**: Adjust sensitivity (0-1). Default 0.5 is balanced. Higher values detect more subtle beats.
- **FPS changes break sync**: The store subscribes to `usePlaybackStore` and auto-recalculates beat frame positions when FPS changes via `recalculateBeatFramesForFps()`.
- **Keyframe conflicts**: Beat-sync keyframes are tagged with `'beat-sync'`. Call `clearObjectBeatSync(objectRefs)` to remove them without affecting manually-placed keyframes.
- **Two detection systems**: `beatDetection.ts` (service) is more sophisticated (spectral flux, phase alignment, segments). `engine/beatSync.ts` is simpler (energy-only) for real-time use. Use the service for analysis, the engine for runtime.

## Examples

```typescript
// Full pipeline via store
const store = useBeatSyncStore.getState()
await store.analyzeAudio(musicAudioUrl)
// store.analysis.bpm, store.analysis.beats, etc.

// Apply to a text overlay
await store.applyObjectBeatSync(
  [{
    objectRef: { objectType: 'text', objectId: 'text-1' },
    effect: 'scale-pulse',
    subdivision: 1,
    offset: 0,
    intensity: 0.7,
  }],
  30, // fps
  { 'text:text-1': { startFrame: 0, endFrame: 300 } }
)

// Engine-level: snap a frame to beat
import { snapToBeat } from '@/engine/beatSync'
const snapped = snapToBeat(currentFrame, 120, 30) // 120 BPM, 30 fps
```
