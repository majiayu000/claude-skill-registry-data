---
name: generate-voice
description: Generate TTS voiceover with ElevenLabs, including phoneme alignment, viseme mapping, and emotion-based mouth curvature for lip sync.
argument-hint: <text-or-dialogue>
---

## Purpose

Generate a spoken voiceover from text using ElevenLabs TTS, extract phoneme alignment data, convert phonemes to visemes for lip sync, and build an emotion timeline from inline `[emotion]` cues. This is the core pipeline that turns a script into an animated talking character.

## Steps

1. **Prepare the script with emotion cues.** Inline cues like `[happy]`, `[sad]`, `[angry]` are placed before the words they apply to. These get converted to ElevenLabs v3 expressive annotations (e.g., `[happy]` becomes `<cheerfully>`). The mapping lives in `EMOTION_V3_MAP` inside `elevenlabs.ts`.

2. **Select a voice.** Call `getElevenLabsService().getVoices()` to list available voices. Each voice has a `voice_id`. The user picks one from `VoicesPanel.tsx` or the orchestrator assigns one.

3. **Generate speech with alignment.** Call `generateWithAlignment(text, voiceId, settings)` on the `ElevenLabsService` singleton. This hits the `/text-to-speech/{voiceId}/with-timestamps` endpoint and returns:
   - `audioBlob` / `audioUrl` -- the MP3 audio
   - `alignment` -- an `ElevenLabsAlignment` object with `characters`, `character_start_times_seconds`, `character_end_times_seconds`, and optionally `phonemes`, `phoneme_start_times_seconds`, `phoneme_end_times_seconds`
   - `duration` -- total audio duration in seconds

4. **Convert alignment to viseme timeline.** Use `getLipSyncProcessor(fps).processAlignment(alignment)` from `lipSync.ts`. The processor:
   - Prefers phoneme-based mapping (ARPAbet phonemes via `PHONEME_TO_VISEME`)
   - Falls back to character-based mapping (`CHAR_TO_VISEME`) when phonemes are unavailable
   - Merges consecutive identical visemes
   - Adds smooth transitions between viseme shapes (2-frame intermediate visemes)
   - Returns `VisemeEvent[]` with `viseme`, `startTime`, `endTime`, `startFrame`, `endFrame`

5. **Build the emotion timeline.** Call `buildEmotionTimeline(rawScript, wordTimeline)` from `emotionTimeline.ts`. This:
   - Parses `[emotion]` cues from the raw script using regex
   - Maps each cue to a word index in the clean (cue-stripped) text
   - Looks up frame positions from the word timeline
   - Returns `EmotionEvent[]` with `emotion`, `startFrame`, `endFrame`

6. **Map emotion to mouth curvature.** The emotion determines which set of 8 viseme sprites to use (3 curvatures x 8 visemes = 24 total sprites). Store the generated voice data in `useVoiceStore` and the dialogue line in `useMultiCharacterStore`.

## Viseme Reference Table

| Viseme | Mouth Shape          | Phonemes (ARPAbet)             |
|--------|----------------------|--------------------------------|
| Rest   | Closed, relaxed      | SIL, SP, K, G, NG, HH          |
| Aa     | Wide open            | AA, AE, AH, AY, AW             |
| Ee     | Wide smile           | EH, EY, IY, IH                 |
| O      | Rounded medium       | AO, OW, OY                     |
| U      | Pursed lips          | UH, UW                         |
| M      | Lips pressed         | M, B, P                        |
| F      | Teeth on lower lip   | F, V                           |
| L      | Tongue tip           | L, TH                          |
| D      | Tongue behind teeth  | D, T, N, DH                    |
| R      | Rounded retracted    | R, ER                          |
| S      | Teeth close          | S, Z, SH, ZH, CH, JH           |
| W      | Rounded tight        | W, Y                           |

## Mouth Curvature by Emotion

| Curvature | Emotions                                      |
|-----------|-----------------------------------------------|
| Upward    | Joy, Satisfaction, Amusement, Laughter         |
| Neutral   | Anger, Sternness, Indignation, Surprise, Shock |
| Downward  | Sadness, Fear, Disgust, Grief, Melancholy      |

## Key Files

- `src/services/elevenlabs.ts` -- ElevenLabsService class, TTS generation, emotion cue conversion, voice listing, voice cloning
- `src/services/lipSync.ts` -- LipSyncProcessor, PHONEME_TO_VISEME mapping, IPA_PHONEME_TO_VISEME, viseme transition logic
- `src/services/emotionTimeline.ts` -- buildEmotionTimeline(), getEmotionAtFrame(), expression cue parsing
- `src/stores/useVoiceStore.ts` -- Voice/TTS state, caption config
- `src/stores/useMultiCharacterStore.ts` -- Multi-character dialogue state, dialogue lines
- `src/types/voice.ts` -- Viseme, VisemeEvent, WordEvent, ElevenLabsAlignment types
- `src/types/nanoBanana.ts` -- CurvedVisemeKey, MouthCurvature (24-sprite system)

## Common Issues

- **Missing API key**: The ElevenLabs API key must be set as `VITE_ELEVENLABS_API_KEY` in the environment. Check `hasElevenLabsService()` before calling.
- **No phoneme data**: Some ElevenLabs models or languages may only return character-level alignment. The processor falls back to `CHAR_TO_VISEME` automatically, but viseme quality is lower.
- **Emotion cues not stripped before TTS**: The raw script with `[emotion]` cues is sent to ElevenLabs, which converts them to v3 annotations. The cues are not spoken words -- they only affect delivery style.
- **Credit gating**: `generateWithAlignment` is wrapped in `withCreditGate('elevenlabs-tts', ...)`. Ensure the user has sufficient credits.
- **IPA phonemes for non-English**: Use `mapIpaPhonemeToViseme()` from `lipSync.ts` for non-English languages that return IPA instead of ARPAbet.

## Examples

```typescript
// Generate voice with alignment
const service = getElevenLabsService()
const { audioUrl, alignment, duration } = await service.generateWithAlignment(
  '[happy] Hey everyone! [excited] Welcome to my channel!',
  'pNInz6obpgDQGcFmaJgB', // voice ID
  { stability: 0.5, similarityBoost: 0.75 }
)

// Convert to viseme timeline
const processor = getLipSyncProcessor(30) // 30 fps
const visemeTimeline = processor.processAlignment(alignment)

// Build emotion timeline
const emotionTimeline = buildEmotionTimeline(
  '[happy] Hey everyone! [excited] Welcome to my channel!',
  wordTimeline
)

// Query at a specific frame
const viseme = processor.getVisemeAtFrame(visemeTimeline, 45) // e.g. 'Ee'
const emotion = getEmotionAtFrame(emotionTimeline, 45) // e.g. 'Happy'
```
