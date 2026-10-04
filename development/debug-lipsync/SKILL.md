---
name: debug-lipsync
description: Debug lip sync issues including viseme timing, phoneme alignment, curvature selection, and cross-fade rendering problems.
---

# Debug Lip Sync

Diagnose and fix lip sync issues in ProAnimate's character animation system, covering phoneme-to-viseme mapping, ElevenLabs alignment processing, emotion-driven mouth curvature, and dual-image cross-fade rendering.

## Purpose

ProAnimate uses a 24-viseme sprite system (8 visemes x 3 mouth curvatures) driven by ElevenLabs phoneme alignment data. Issues can occur at any stage: alignment data parsing, viseme mapping, curvature selection from emotions, sprite resolution, or cross-fade rendering.

## Steps

1. **Verify ElevenLabs alignment data exists**:
   - Alignment data comes from ElevenLabs TTS via `elevenlabs.ts`.
   - Check `useVoiceStore.getState().activeVisemeTimeline` -- should be a non-empty `VisemeEvent[]`.
   - If empty, the TTS call did not return alignment data. Verify: the ElevenLabs API key is valid, the voice supports alignment, and the `with_timestamps` option is enabled.
   - Alignment has two data sources:
     - **Phoneme data** (preferred): `alignment.phonemes`, `phoneme_start_times_seconds`, `phoneme_end_times_seconds`.
     - **Character data** (fallback): `alignment.characters`, `character_start_times_seconds`, `character_end_times_seconds`.

2. **Check phoneme-to-viseme mapping** in `LipSyncProcessor`:
   - The `PHONEME_TO_VISEME` map converts ARPAbet phonemes to 12 internal viseme types: Rest, Aa, D, Ee, F, L, M, O, R, S, U, W.
   - Common mapping issues:
     - Unknown phoneme: defaults to `'Rest'`. Check if ElevenLabs returned non-standard phonemes.
     - Missing phoneme in alignment: some words have gaps. `addTransitions()` inserts Rest visemes in gaps.
     - `mergeConsecutiveVisemes()` combines adjacent events with the same viseme to reduce jitter.

3. **Check the 24-viseme sprite resolution** via `resolveVisemeSprite()` in `visemeMapper.ts`:
   - The 12 internal visemes are mapped to 8 display visemes: REST, AI, E, O, U, MBP, FV, LTH.
   - Each display viseme has 3 curvature variants: upward, neutral, downward.
   - Sprite index formula: `curvatureRow * 8 + visemeColumn` (0-23).
   - If the wrong mouth shape appears, check that `resolveVisemeSprite()` returns the correct index.
   - Mapping: Aa->AI, D->LTH, Ee->E, F->FV, L->LTH, M->MBP, O->O, R->O, S->REST, U->U, W->U, Rest->REST.

4. **Check emotion-to-curvature mapping**:
   - Mouth curvature is driven by the active emotion from the emotion timeline.
   - `getCurvatureFromEmotion(emotion)` in `emotionMapping.ts` returns: `'upward'`, `'neutral'`, or `'downward'`.
   - Curvature rules:
     - **Upward** (happy): Satisfaction, Amusement, Joy, Laughter, Happy, Excited, Pleased, Delighted, Content, Cheerful.
     - **Neutral** (intense): Sternness, Indignation, Anger, Rage, Alertness, Wonder, Surprise, Shock, Neutral, Focused, Determined.
     - **Downward** (sad): Disdain, Aversion, Disgust, Revulsion, Concern, Anxiety, Fear, Terror, Dejection, Melancholy, Sadness, Grief.
   - If the curvature does not change with emotions, check that `buildEmotionTimeline()` is producing events from the script's `[emotion]` cues.

5. **Check the emotion timeline**:
   - `buildEmotionTimeline(rawScript, wordTimeline)` parses `[emotion]` cues from the raw script.
   - Cues must match the regex `/\[([\w-]+)\]/g` (e.g., `[happy]`, `[surprised]`).
   - The cue maps to the word that follows it in the script. If the word is not found in the word timeline, the cue is ignored.
   - Each emotion applies from its cue position until the next cue or end of timeline.
   - Emotions are capitalized: `[happy]` becomes `Happy`.

6. **Debug cross-fade rendering** in `CharacterComposite.tsx`:
   - The character uses dual-image cross-fade: two `<img>` elements (slot A and slot B) swap with opacity transitions.
   - `activeVisemeSlot` ref tracks which slot is currently displaying.
   - When the viseme changes, the inactive slot loads the new sprite, then opacity swaps.
   - If the mouth flickers, check that:
     - Viseme timeline events are not too short (< 1 frame).
     - Sprite images are preloaded (no load delay during playback).
     - `mergeConsecutiveVisemes()` is eliminating jitter.

7. **Debug character layer rendering**:
   - Characters are built from layers: body, head (emotion), viseme (mouth), hair, eye, eyebrow, shirt, pants, shoes.
   - Layer draw order is customizable via `layerOrder` in `useCharacterPartsStore`.
   - Cascading transforms: body-to-head-to-hair, body-to-viseme.
   - If the mouth appears in the wrong position, check `transforms.viseme` offset relative to body.

## Key Files

| Purpose | Path |
|---------|------|
| Lip sync processor | `src/services/lipSync.ts` |
| Emotion timeline builder | `src/services/emotionTimeline.ts` |
| Emotion-to-curvature mapping | `src/services/emotionMapping.ts` |
| Extended viseme mapper | `src/services/visemeMapper.ts` |
| Character composite renderer | `src/components/canvas/CharacterComposite.tsx` |
| Character layer (multi-char) | `src/components/canvas/CharacterLayer.tsx` |
| ElevenLabs TTS service | `src/services/elevenlabs.ts` |
| Voice store | `src/stores/useVoiceStore.ts` |
| Character config store | `src/stores/useCharacterConfigStore.ts` |
| Character parts store | `src/stores/useCharacterPartsStore.ts` |
| Viseme types | `src/types/voice.ts` |
| NanoBanana types (curvatures) | `src/types/nanoBanana.ts` |
| Emotion head types | `src/types/emotionHeads.ts` |

## Common Issues

- **Mouth stays on REST**: Viseme timeline is empty. Check that ElevenLabs alignment was returned and `LipSyncProcessor.processAlignment()` produced events.
- **Wrong mouth shape for phoneme**: The `PHONEME_TO_VISEME` map may not cover a phoneme. Check the map in `lipSync.ts`. Unknown phonemes default to Rest.
- **Mouth curvature does not change**: No `[emotion]` cues in the script, or the emotion string is not in the `emotionToMouthCurvature` map. Check `emotionMapping.ts`.
- **Mouth flickers rapidly**: Viseme events are too short (< 30ms). The `mergeConsecutiveVisemes()` and `addTransitions()` functions should smooth this. Check if they are being called.
- **Mouth offset from face**: The viseme layer transform (`transforms.viseme`) is misconfigured. Check position (x, y), scale, and rotation in `useCharacterPartsStore`.
- **Singing lip sync issues**: Singing uses a separate path via `singingLipSync.ts` and `singingAnalyzer.ts`. Check those files for singing-specific viseme mapping.
- **Export lip sync mismatch**: The canvas2dRenderer uses the same viseme lookup logic but from serialized props. Verify `visemeTimeline` is included in `VideoCompositionProps`.

## Examples

Inspect viseme timeline:
```ts
const timeline = useVoiceStore.getState().activeVisemeTimeline
console.log('Events:', timeline.length)
timeline.slice(0, 5).forEach(e => console.log(e.viseme, e.startTime, e.endTime))
```

Test phoneme mapping:
```ts
import { mapPhonemeToViseme } from '@/services/lipSync'
console.log(mapPhonemeToViseme('AA')) // 'Aa'
console.log(mapPhonemeToViseme('M'))  // 'M'
console.log(mapPhonemeToViseme('XY')) // 'Rest' (unknown)
```

Check emotion curvature:
```ts
import { getCurvatureFromEmotion } from '@/services/emotionMapping'
console.log(getCurvatureFromEmotion('Joy'))     // 'upward'
console.log(getCurvatureFromEmotion('Anger'))   // 'neutral'
console.log(getCurvatureFromEmotion('Sadness')) // 'downward'
```
