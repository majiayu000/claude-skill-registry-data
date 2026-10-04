---
name: stable-audio-3
description: Adapt music, stem, ambience, Foley, sound effect, audio-to-audio, inpainting, or continuation cues into Stable Audio 3 prompts with source, action, production character, duration, and model mode.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Stable Audio 3 Prompting

## Choose model path

- `medium`: higher-quality music and general audio
- `small-music`: fast music
- `small-sfx`: sound effects

## Music

Describe genre, important instruments, mood and energy, and BPM when useful. Stable Audio 3 is for instrumental or non-intelligible vocal textures, not dialogue.

## Stem or solo instrument

Start with `TrackType: Instrument` when isolation matters. State instrument, genre context, technique, mood, tempo, recording environment, and effects.

## SFX

State:

1. physical source
2. exact triggering action
3. duration or decay behavior
4. distance and microphone perspective
5. room or exterior character
6. processing only when needed

`TrackType: SFX` is useful for isolated effects.

## Existing audio

For audio-to-audio, inpainting, or continuation, preserve source-file identity and record the intended edit region or influence strength as execution metadata. Keep the prompt plausible relative to surrounding audio.

## Output

Save under `04_generation/prompts/stable-audio-3/<cue-id>.md` with `MODEL`, `MODE`, `DURATION`, `PROMPT`, and optional `NEGATIVE_PROMPT`.

## Done

The prompt names a physically or musically coherent source and duration, and does not ask Stable Audio 3 to produce intelligible spoken dialogue.
