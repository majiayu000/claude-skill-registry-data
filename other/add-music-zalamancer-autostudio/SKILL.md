---
name: add-music
description: Generate AI background music for a clip based on mood analysis, with genre selection and audio mixing.
argument-hint: <mood-or-genre>
---

## Purpose

Generate background music that matches the emotional tone of a clip's dialogue. Analyze dialogue lines for mood, build a composition plan or text prompt, generate music via ElevenLabs or a backend provider, and mix it with dialogue audio using auto-ducking.

## Steps

1. **Analyze dialogue mood.** Call `buildMusicPlanFromDialogue(dialogueLines, fps)` from `musicAnalyzer.ts`. This:
   - Detects themes from script text (motivation, love, adventure, humor, tech, etc.) using keyword matching
   - Groups consecutive dialogue lines by emotion into segments (intro/middle/climax/outro)
   - Maps each emotion to music styles using `EMOTION_MUSIC_MAP` (e.g., Joy = uplifting/bright/warm, Anger = intense/driving/aggressive)
   - Returns a `MusicCompositionPlan` with global styles, negative styles, and per-section styles/durations

2. **Choose generation method.** Two paths:
   - **Composition plan** (preferred): Use `createMusicCompositionPlan(prompt, durationMs)` then `generateMusic({ compositionPlan })` from `elevenlabs.ts`. The plan endpoint is free but rate-limited.
   - **Simple prompt**: Use `generateMusic({ prompt, durationMs, forceInstrumental })` for a one-shot generation.
   - **Advanced backend**: Use `generateMusicAdvanced(options)` from `musicGeneration.ts` which hits `/api/music-generation/generate` and polls for completion. Supports genre, mood, tempo, and instrumental flags.

3. **Configure genre and mood.** Available genres: ambient, cinematic, electronic, hip-hop, jazz, lo-fi, orchestral, pop, rock, r&b, acoustic, world, custom. Available moods: uplifting, energetic, calm, dark, dramatic, happy, melancholic, mysterious, romantic, suspenseful, neutral. Use `buildMusicPrompt({ genre, mood, tempo, customPrompt })` to construct a prompt string.

4. **Mix audio tracks.** Use `mixTracks(tracks, totalDurationSec, options)` from `audioMixer.ts`. This:
   - Uses `OfflineAudioContext` for offline rendering
   - Supports per-track volume (0-1), mute, and stereo pan (-1 to 1)
   - Auto-ducks music/SFX under dialogue (default -12dB reduction)
   - Configurable attack (0.3s) and release (0.5s) fade times
   - Extracts dialogue regions and schedules gain automation

5. **Store the result.** Add the music audio URL to the voice/audio store and update the timeline. The orchestrator typically places music at frame 0 spanning the entire clip duration.

## Key Files

- `src/services/musicAnalyzer.ts` -- buildMusicPlanFromDialogue(), buildMusicPromptFromDialogue(), EMOTION_MUSIC_MAP, theme detection, beat detection bridge
- `src/services/musicGeneration.ts` -- generateMusicAdvanced(), MusicGenerationOptions, MusicGenre, MusicMood, GENRE_OPTIONS, MOOD_OPTIONS
- `src/services/elevenlabs.ts` -- createMusicCompositionPlan(), generateMusic(), MusicCompositionPlan, MusicSection
- `src/services/audioMixer.ts` -- mixTracks(), AudioTrackSource, MixerOptions, auto-ducking logic
- `src/stores/useAudioDesignStore.ts` -- Audio design state
- `server/routes/musicGeneration.ts` -- Backend music generation endpoint

## Common Issues

- **Composition plan vs prompt mode**: `force_instrumental` is only valid with prompt mode, not composition plans. For instrumental music with composition plans, use empty `lines: []` in sections (already the default).
- **Section duration limits**: ElevenLabs requires integer `duration_ms` and each section must be 3-120 seconds. `segmentToSection()` clamps and rounds automatically.
- **Music too loud under dialogue**: Adjust `duckAmountDb` in mixer options. Default is -12dB. For clearer dialogue, use -14 to -16dB.
- **Credit gating**: Both `generateMusic()` and `generateMusicAdvanced()` are credit-gated. Check user credits before calling.
- **Backend unavailable**: `isMusicGenerationAvailable()` checks if the advanced backend has providers configured. Falls back to ElevenLabs direct.

## Examples

```typescript
// From dialogue analysis
import { buildMusicPlanFromDialogue } from '@/services/musicAnalyzer'
import { generateMusic } from '@/services/elevenlabs'

const plan = buildMusicPlanFromDialogue(dialogueLines, 30)
const { audioBlob, audioUrl, durationMs } = await generateMusic({ compositionPlan: plan })

// Simple prompt
const result = await generateMusic({
  prompt: 'uplifting cinematic background music',
  durationMs: 30000,
  forceInstrumental: true,
})

// Mix with dialogue
import { mixTracks } from '@/services/audioMixer'
const mixed = await mixTracks(
  [
    { url: dialogueAudioUrl, startTimeSec: 0, type: 'dialogue', volume: 1 },
    { url: musicAudioUrl, startTimeSec: 0, type: 'music', volume: 0.3 },
  ],
  totalDurationSec,
  { autoDuck: true, duckAmountDb: -12 }
)
```
