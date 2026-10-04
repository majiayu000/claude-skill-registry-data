---
name: create-script
description: Generate an AI script with emotion cues and dialogue formatting using Gemini 2.0 Flash for short-form video content.
argument-hint: <topic-or-prompt>
---

# Create Script

Generate an animated video script with emotion cues, viseme emphasis, and optional sprite timeline using Gemini. Scripts are formatted for the lip sync and emotion systems.

## Purpose

Create spoken dialogue scripts for animated characters that include inline emotion bracket cues (e.g., `[happy]`, `[surprised]`) which drive the character's expression changes during playback. Scripts can also include sprite timeline events for coordinating character part changes with specific moments in the narration.

## Script Generation

The `GeminiService` class in `gemini.ts` sends a structured prompt to Gemini and returns a `GeneratedScript`:

```ts
interface GeneratedScript {
  text: string           // Clean spoken text (no cues)
  cues: ScriptCue[]      // Expression/viseme cues with positions
  rawScript: string      // Full script with [expression] cues inline
  spriteTimeline?: SpriteTimeline[]  // Optional sprite change timeline
}
```

### Generation Options

```ts
interface GeminiGenerateOptions {
  topic?: string        // What the script is about (default: 'introducing yourself')
  style?: 'casual' | 'professional' | 'energetic' | 'calm' | 'dramatic'
  duration?: 'short' | 'medium' | 'long'  // ~10s, ~30s, ~60s
  includeExpressions?: boolean  // Add [emotion] bracket cues
  includeVisemes?: boolean      // Add [mouth-shape] emphasis cues
  character?: string            // Character name/description for context
  spriteNames?: {               // Available sprite names for timeline
    head?: string[]
    viseme?: string[]
    hair?: string[]
    body?: string[]
  }
}
```

### Duration Guide

| Duration | Length | Speaking Time |
|----------|--------|-------------|
| `short` | 1-2 sentences | ~10 seconds |
| `medium` | 3-5 sentences | ~30 seconds |
| `long` | 6-10 sentences | ~60 seconds |

## Emotion Cue System

Scripts use inline bracket cues that the emotion timeline system parses:

```
[happy] Hey everyone! Welcome to my channel.
[excited] Today I'm going to show you something amazing!
[thinking] Now, where did I put that...
[surprised] Oh wow, look at this!
```

Available expressions: `neutral`, `happy`, `sad`, `angry`, `surprised`, `confused`, `thinking`, `excited`, `worried`, `skeptical`

These cues are processed by `emotionTimeline.ts` (`buildEmotionTimeline`) to create frame-based emotion events that drive character expression changes during playback.

## Emotion-to-Character Mapping

The emotion cues map to the 24-emotion head system (6 categories x 4 intensities):

| Cue | Category | Head Variant |
|-----|----------|-------------|
| `happy` | Joy | Amusement (level 2) |
| `excited` | Joy | Joy (level 3) |
| `sad` | Sadness | Melancholy (level 2) |
| `angry` | Anger | Anger (level 3) |
| `surprised` | Surprise | Surprise (level 3) |
| `worried` | Fear | Anxiety (level 2) |
| `thinking` | -- | Custom mapping |

The `emotionMapping.ts` service normalizes arbitrary emotion strings to the standard categories.

## Sprite Timeline

When `spriteNames` are provided, the script includes a timeline of sprite changes:

```json
{
  "spriteTimeline": [
    {"time": "0:00", "head": "neutral", "expression": "neutral"},
    {"time": "0:05", "head": "happy", "expression": "happy"},
    {"time": "0:12", "body": "gesture-point", "expression": "excited"}
  ]
}
```

This allows coordinating character part changes (head swaps, body poses, hair changes) with specific moments in the script.

## Integration with TTS

After script generation, the flow continues:
1. Clean text (`text` field) is sent to ElevenLabs TTS
2. ElevenLabs returns audio + phoneme alignment data
3. `LipSyncProcessor` converts phonemes to viseme events
4. `buildEmotionTimeline` converts bracket cues to frame-based emotion events
5. `CaptionProcessor` generates word-by-word caption timing
6. All timelines are synced to the audio duration

## Key Files

| Purpose | Path |
|---------|------|
| Gemini script service | `src/services/gemini.ts` |
| Emotion timeline builder | `src/services/emotionTimeline.ts` |
| Emotion string mapping | `src/services/emotionMapping.ts` |
| Lip sync processor | `src/services/lipSync.ts` |
| Caption processor | `src/services/captions.ts` |
| Scripts panel | `src/components/panels/ScriptsPanel.tsx` |
| Script+dialogue panel | `src/components/panels/ScriptDialoguePanel.tsx` |
| Voice store | `src/stores/useVoiceStore.ts` |
| Multi-character store | `src/stores/useMultiCharacterStore.ts` |

## Common Issues

- **Gemini API key missing**: Requires `VITE_GEMINI_API_KEY` environment variable.
- **Malformed JSON response**: Gemini occasionally returns invalid JSON. The service uses `responseMimeType: 'application/json'` and temperature 0.8 to improve reliability.
- **Emotion cues not parsed**: Ensure bracket cues use the exact format `[emotion]` (lowercase, no spaces). The `emotionTimeline` parser matches `\[(\w+)\]` regex.
- **Script too long/short**: Use the `duration` option to control length. Gemini is given specific sentence count targets for each duration tier.
- **Credit gating**: Script generation uses `gemini-script` credit type.
- **Retry logic**: Uses `fetchWithRetry` with max 2 retries, 60s timeout, and 1s retry delay.

## Example

Topic: "Top 3 tips for better sleep"
Style: energetic
Duration: medium

Generated script:
```
[excited] Hey there, sleep warriors! Ready to transform your nights?
[happy] Tip number one: put down your phone at least 30 minutes before bed.
[thinking] I know, I know, it's hard. But blue light is your sleep's worst enemy.
[surprised] Tip two might shock you: keep your room at 65 degrees!
[happy] And tip three: try a consistent bedtime, even on weekends.
[excited] Trust me, your body will thank you! Sweet dreams!
```

This produces a `rawScript` with cues, a clean `text` for TTS, and `ScriptCue` entries for each emotion transition.
