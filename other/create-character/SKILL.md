---
name: create-character
description: Generate a 2D character with sprite sheets, viseme mapping, and emotion heads using NanoBanana2 and Vertex AI.
argument-hint: <character-description>
---

# Create 2D Character

Generate a complete 2D animated character with sprite sheets for body, head, hair, visemes (lip sync), eyes, eyebrows, and clothing using the NanoBanana2 (NB2) pipeline powered by Gemini image generation.

## Purpose

Create all the sprite assets needed for a fully animated 2D character: a concept image, body sprite, head sprite, hairstyle grid, viseme mouth grid (for lip sync), eye variant grid, eyebrow variant grid, and clothing grid. The pipeline runs 8 sequential AI generation steps.

## NB2 Pipeline Steps

The `runNB2Pipeline()` function in `nanoBanana2.ts` runs these steps sequentially:

| Step | Part Type | Output | Grid Size |
|------|-----------|--------|-----------|
| 1 | `concept` | Full character concept image | Single image |
| 2 | `body` | Body sprite (no head/hair, T-pose) | Single image |
| 3 | `head` | Featureless head sprite (no hair) | Single image |
| 4 | `hair` | Hairstyle grid | 4x3 (female) or 6x4 (male) |
| 5 | `viseme-sheet` | Mouth shapes for lip sync | 3x9 (all-at-once) or 3x3 per curvature |
| 6 | `eye-strip` | Eye variants grid | 3x2 (6 variants) |
| 7 | `eyebrow-strip` | Eyebrow variants grid | 3x2 (6 variants) |
| 8 | `clothing` | Clothing grid (shirt/pants/shoes) | 3x3 (proportional rows: 40%/50%/10%) |

Each step calls the `/api/nb2/generate` endpoint, which uses Gemini image generation (Vertex AI).

## 24-Viseme Sprite System (3 Curvatures x 8 Visemes)

Characters support 24 mouth sprites for emotionally-aware lip sync:

**Mouth Curvatures:**
- **Upward** -- happy emotions (Joy, Amusement, Satisfaction, Laughter)
- **Neutral** -- anger/surprise emotions (Anger, Surprise, Alert)
- **Downward** -- sad emotions (Sadness, Fear, Disgust, Grief)

**8 Viseme Types:**

| Viseme | Mouth Shape | Phonemes |
|--------|------------|----------|
| REST | Closed, relaxed | Silence |
| AI | Wide open | AH, EYE |
| E | Wide smile, teeth | EE |
| O | Rounded open | OH |
| U | Pursed lips | OO, W |
| MBP | Lips pressed | M, B, P |
| FV | Lower lip under teeth | F, V |
| LTH | Tongue between teeth | TH, L |

Viseme generation supports two modes:
- **All-at-once**: Single API call generates a 3x9 grid (all 3 curvatures x 9 viseme cells)
- **Part-by-part**: Three separate API calls, one per curvature (3x3 grid each)

## Eye and Eyebrow Variants

6 eye variants: `neutral`, `happy`, `angry`, `sad`, `surprised`, `closed`
6 eyebrow variants: `neutral`, `happy`, `angry`, `sad`, `surprised`, `raised`

These are auto-selected based on the current emotion during playback.

## Post-Processing

Each generated image goes through post-processing:
1. **Grid line removal** -- Gemini often renders grid lines despite instructions; these are algorithmically removed
2. **Chroma key removal** -- Green/blue screen backgrounds are converted to transparent
3. **Grid slicing** -- Grid images are sliced into individual sprites using canvas manipulation
4. **SVG-aware slicing** -- If the AI returns SVG, viewBox manipulation preserves vector quality

## Key Files

| Purpose | Path |
|---------|------|
| NB2 pipeline | `src/services/nanoBanana2.ts` |
| NB2 prompt templates | `src/services/nb2Prompts.ts` |
| NB2 quality validation | `src/services/nb2QualityValidation.ts` |
| NB2 store | `src/stores/useNB2Store.ts` |
| Character config store | `src/stores/useCharacterConfigStore.ts` |
| Character parts store | `src/stores/useCharacterPartsStore.ts` |
| Saved characters store | `src/stores/useSavedCharactersStore.ts` |
| NB2 controls panel | `src/components/panels/NB2ControlsSection.tsx` |
| NB2 image viewer | `src/components/canvas/NB2ImageViewer.tsx` |
| Grid reference generator | `src/services/gridReferenceGenerator.ts` |
| Viseme types | `src/types/nanoBanana.ts` |
| Emotion head types | `src/types/emotionHeads.ts` |
| Server route | `server/routes/nanoBanana2.ts` |
| Character composite renderer | `src/components/canvas/CharacterComposite.tsx` |

## Pipeline Options

```ts
interface NB2PipelineOptions {
  prompt: string              // Character description
  styleReference: string | null  // Style reference image (base64)
  layoutReference: string | null // Layout reference image (base64)
  resolution?: NB2Resolution     // '512' | '1024' | '2048'
  aspectRatio?: NB2AspectRatio   // '1:1' | '3:4' | '16:9' | '3:2'
}
```

Grid sizes and prompt overrides can be customized per step. The pipeline also accepts an `AbortSignal` for cancellation.

## Character Rendering

The 4-layer character composite renders:
1. **Body** -- base torso
2. **Head** -- emotion/expression variant (mapped from emotion timeline)
3. **Viseme (mouth)** -- lip sync sprite (selected by `LipSyncProcessor` from phoneme data)
4. **Hair** -- hair overlay

Layers have independent position, rotation, scale, and visibility. Draw order is customizable. Cascading transforms: body-to-head-to-hair, body-to-viseme.

## Common Issues

- **Pipeline step fails**: Each step is independent; the pipeline continues and marks failed steps as errors. Users can re-run individual steps via `runSingleNB2Step()`.
- **Grid not slicing correctly**: Verify grid size settings match the generated image layout. Default grid sizes vary by gender (male hair: 6x4, female: 4x3).
- **Viseme mapping wrong**: After generation, visemes must be mapped in the `VisemeMappingPanel`. The `buildVisemeSpriteMapFromCurved()` utility auto-maps from curved viseme data.
- **Transparent backgrounds**: Post-processing removes green/blue screen via chroma key. If the AI generates a non-standard background color, manual background removal may be needed.
- **Credit gating**: Each NB2 generation step consumes credits (`nb2-generate` operation type).

## Example

Description: "A friendly wizard with a blue robe, long white beard, and a pointed hat"

The pipeline will:
1. Generate a concept image of the wizard
2. Extract the body (no head/hair, T-pose in underwear)
3. Extract the featureless head
4. Generate a 4x3 grid of 12 hairstyle/beard options
5. Generate a 3x9 viseme sheet with 24 mouth shapes (3 curvatures x 8 visemes)
6. Generate a 3x2 grid of 6 eye variants
7. Generate a 3x2 grid of 6 eyebrow variants
8. Generate a 3x3 clothing grid (3 robes, 3 pants, 3 shoe styles)

Result: A fully rigged 2D character ready for lip sync animation in the editor.
