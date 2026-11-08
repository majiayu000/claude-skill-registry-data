---
name: sound-design
description: Chooses music and sound effects, cue times, ducking and loudness from licensed audio. Use when building the audio part of the edit plan.
version: 0.1.0
owner: Digikon
---

# sound-design

## Inputs
Scene plan, licensed audio assets, retrieved sound_cue recipes, loudness guidance (verified).

## Procedure
1. Choose music and effects only from the supplied licensed audio assets.
2. Tie every cue to a scene id and an offset inside that scene.
3. Use music-bed-duck wherever speech or key effects overlap music.
4. Finish with one loudness-normalise use, but only when the storyboard has voiceover, audio cues or audio assets to mix. A brief that rules out audio ("no voiceover, no music, no sound effects") gets no audio operation at all, including this one. The default target is a placeholder; take the platform's own guidance when a verified entry exists.
5. Prefer fewer, cleaner cues.

## Never
- Use unlicensed audio, or audio whose licence is not recorded.
- Direct voiceover or TTS in this version.
- Put a cue on a scene that does not exist.
- State a loudness target as fact without a verified source.

## Evals
See evals/cases.md.
