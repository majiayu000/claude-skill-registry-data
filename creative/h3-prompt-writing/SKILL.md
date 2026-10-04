---
name: h3-prompt-writing
description: "Write MiniMax H3 prompts for T2VA, I2VA, FL2VA, L2VA, and Ref2VA using the required audiovisual fields, keyframe alignment, speaker IDs, dialogue tags, reference labels, and timing."
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# H3 Prompt Writing

This is Story-Film's portable implementation of the current public MiniMax H3 prompt-writing guidance. It is the mandatory formatting layer for every Story-Film MiniMax H3 prompt.

It contains no MiniMax Hub tool calls. Source behavior was reviewed at MiniMax-H3 commit `d21241f0a4b3acbb34c97dae47fa417b7065e438`; see `SOURCES.md`.

## Workflow

1. Identify the actual H3 mode supported by the selected workflow: T2VA, I2VA, FL2VA, L2VA, or Ref2VA.
2. For T2VA/I2VA/FL2VA/L2VA read `references/base-en.txt`.
3. For Ref2VA read `references/ref-en.txt`, and use the base guide for shared shot, camera, speaker, dialogue, and sound conventions.
4. Preserve the required field names, section order, reference labels, shot numbering, and timing notation.
5. Preserve user dialogue, lyrics, and visible scene text exactly in their original language.
6. Hand the structured result back to `minimax-h3` so Story-Film continuity, reference authority, exact-audio, and capture constraints are also enforced.

## Base modes

Final core field order:

1. `integrated_multimodal_description`
2. `overall_soundscape`
3. `non_diegetic_music`

I2VA, FL2VA, and L2VA also require the correct keyframe alignment instruction before the three fields. T2VA does not.

## Ref2VA

Final section order:

1. `subject_definitions`
2. `summary`
3. `retention_analysis`
4. `detailed_description`
5. `overall_soundscape`
6. `non_diegetic_music`

Use stable `<Subject N>`, `<Picture N>`, `<Video N>`, and `<Audio N>` labels. Do not assign a reference a broader authority than the Story-Film source manifest allows.

## Shared output rules

- `[Shot 1]` has no cut timestamp. Later shots use strictly increasing `At MM:SS.mmm` cut times inside the requested duration.
- Vocal sources use stable `(S1)`, `(S2)`, and later IDs.
- Spoken or sung content uses `<d>[Language] exact content</d>`.
- Use `<scenetrans>` when verbal audio crosses a shot boundary and `<cutoff>` only when the requested clip actually truncates speech.
- Describe camera motion as natural shot action. Use motion type, amplitude, and speed only when they matter.
- `overall_soundscape` contains ambience, physical action sounds, and non-verbal human sounds, not repeated dialogue.
- `non_diegetic_music` describes audience-only score. Diegetic music belongs in the shot description.
- Match the written audiovisual timeline to the requested H3 duration, normally 4 to 15 seconds per generated clip.

## Done

The H3 format is exact, every reference label resolves, dialogue and visible text are preserved, and the final timeline matches the requested duration.
