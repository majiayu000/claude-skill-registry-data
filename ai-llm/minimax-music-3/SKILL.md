---
name: minimax-music-3
description: Adapt score or song cues into MiniMax Music 3 prompts using vivid English musical sentences plus explicit genre, mood, vocals, instruments, BPM, lyrics, and structure fields.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# MiniMax Music 3 Prompting

Target model: `music-3.0`.

## Prompt grammar

Write the main prompt as vivid English sentences, not a comma-only tag list.

A useful order is:

1. mood and genre or subgenre
2. tempo when important
3. vocal character, or state that it is instrumental
4. narrative or scene function
5. atmosphere
6. two or three important instruments and production details

Use structured fields alongside the prose prompt when available: `genre`, `mood`, `vocals`, `instruments`, `bpm`, `key`, `tempo`, `structure`, and `references`.

For songs, keep lyrics in the lyrics field with clear section markers. For film score, use instrumental mode unless the cue explicitly calls for vocals.

## Rules

- Describe vocals as an audible character, not only "male" or "female".
- Give the track a scene or dramatic function.
- Keep the instrument list selective.
- Use English for the main generation prompt unless the target workflow explicitly benefits from another language. Lyrics remain in their intended language.
- Save under `04_generation/prompts/minimax-music-3/<cue-id>.md`.

## Done

The musical brief is readable by a musician and every structured field agrees with the prose prompt.
