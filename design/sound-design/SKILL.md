---
name: sound-design
description: Add sound effects to a clip using Freesound API search and AI sound design placement.
argument-hint: <sound-description>
---

## Purpose

Add sound effects to a clip using two sources: searching Freesound.org's 500K+ Creative Commons library, or generating sound effects via ElevenLabs. Includes an intelligent auto-SFX system that detects scene events (text reveals, transitions, shape entrances) and places appropriate sound effects automatically.

## Steps

1. **Choose a source: search or generate.**
   - **Search (Freesound)**: Use `getFreesoundService().search({ query, pageSize, filter })` to find sounds. Results include `previews['preview-hq-mp3']` for playback and `id`, `name`, `tags`, `duration`, `license` metadata. Filter by duration with `filter: "duration:[0 TO 5]"`.
   - **Generate (ElevenLabs)**: Use `generateSoundEffect({ text, durationSeconds, promptInfluence })` from `elevenlabs.ts` to AI-generate a sound effect from a text description.

2. **Preview sounds.** The `useSoundEffectStore` manages preview state. Call `store.preview(hit)` to play a Freesound result (uses `preview-hq-mp3` URL). Call `store.stopPreview()` to stop. The store tracks `previewingId` and `previewUrl`.

3. **Download and import.** For Freesound results, use `getFreesoundService().downloadAsBlob(previewUrl)` to get a Blob. Falls back to a server proxy (`/api/proxy/audio`) if CORS blocks direct download. For generated SFX, the result already includes `audioBlob` and `audioUrl`.

4. **Place on timeline.** Add the sound to the appropriate timeline position. The orchestrator uses `ClipPlanSoundEffect` objects with `prompt`, `source` ('search' or 'generate'), `startPercent`, `durationSeconds`, and `volume`.

5. **Auto-SFX with presets.** Use `applySoundDesignPreset(plan, presetId, fps)` from `soundDesigner.ts` to auto-enrich a clip plan. Available presets:
   - `corporate` -- clean, professional (click transitions, text-reveal SFX)
   - `energetic` -- punchy, high-energy (whoosh transitions, accent hits)
   - `dramatic` -- cinematic, intense (cinematic transitions, ambient bed)
   - `chill` -- mellow, no transitions
   - `horror` -- dark, eerie (glitch transitions, ambient wind)
   - `comedy` -- playful (click transitions, notification sounds)
   - `educational` -- clean, minimal (subtle transitions, notifications)
   - `cinematic` -- film-quality (cinematic transitions, room tone ambient)
   - `retro` -- synthwave (glitch transitions, accent hits)
   - `minimal` -- barely-there audio

6. **Detect scene events.** `detectSceneEvents(plan, fps)` analyzes a clip plan for events that should trigger SFX: text-enter, text-exit, media-transition, scene-change, dialogue-start, dialogue-end, shape-enter. Events are sorted by frame.

7. **Generate auto SFX.** `generateAutoSfx(events, preset, existingSfx)` maps events to SFX prompts based on the preset's `autoSfxTypes`. `generateTransitionAudio(events, preset)` creates transition sounds (whoosh, click, glitch, etc.) limited to max 8 per clip.

## Key Files

- `src/services/soundDesigner.ts` -- SoundDesignPreset, SOUND_DESIGN_PRESETS, detectSceneEvents(), generateAutoSfx(), generateTransitionAudio(), applySoundDesignPreset(), enhanceMusicPrompt(), validateAudioMix()
- `src/services/freesound.ts` -- FreesoundService class, search(), downloadAsBlob(), FreesoundHit type
- `src/services/elevenlabs.ts` -- generateSoundEffect(), GenerateSoundEffectResult
- `src/stores/useSoundEffectStore.ts` -- SFX search state, preview playback, generate prompt state
- `src/components/panels/SoundEffectsPanel.tsx` -- Sound effects browser UI

## Common Issues

- **Freesound API key**: Must be set as `VITE_FREESOUND_API_KEY`. Use `hasFreesoundService()` to check availability.
- **CORS on Freesound previews**: Direct fetch may fail. The service auto-falls back to `/api/proxy/audio` server proxy.
- **Rate limiting**: Freesound returns HTTP 429 when rate-limited. The service throws a user-friendly error.
- **SFX overlap with dialogue**: `validateAudioMix()` in `soundDesigner.ts` checks for SFX-dialogue timing conflicts and suggests shifting SFX to natural pauses.
- **Auto-SFX deduplication**: `generateAutoSfx()` tracks used frame positions to avoid placing multiple SFX at the same timestamp.

## Examples

```typescript
// Search Freesound
const service = getFreesoundService()
const results = await service.search({
  query: 'whoosh transition',
  pageSize: 10,
  filter: 'duration:[0 TO 3]',
})

// Generate SFX with ElevenLabs
const sfx = await generateSoundEffect({
  text: 'dramatic impact hit with reverb',
  durationSeconds: 2,
  promptInfluence: 0.5,
})

// Apply sound design preset to a clip plan
const enrichedPlan = applySoundDesignPreset(clipPlan, 'cinematic', 30)
```
