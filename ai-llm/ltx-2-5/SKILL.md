---
name: ltx-2-5
description: Adapt shot briefs into LTX 2.5 prompts with shot scale, scene and light, physical action, character detail, camera movement, dialogue, ambience, music, and explicit cut continuity for multi-shot generations.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# LTX 2.5 Prompting

## Single-shot mode

Use for a continuous take, performance, or image-to-video shot.

1. Write one flowing paragraph in present tense.
2. Establish shot scale and composition.
3. Set environment, lighting, palette, texture, and atmosphere.
4. Describe action as a clear physical sequence.
5. Describe recurring characters with the same canon identifiers.
6. State camera movement relative to the subject, including how framing changes after the move.
7. Describe ambience, effects, speech, singing, and music. Put spoken dialogue in quotation marks. When visible-dialogue sync is required, preserve the exact speaker, mouth-visibility intent, cut policy, and measured timing from the source brief without paraphrasing the line.
8. Preserve source capture behavior as visible optical/operator behavior. If `end_frame.required` is present, finish the chronological action in that explicit state.
9. A normal single-shot prompt is often about 4 to 8 descriptive sentences, adjusted for complexity.

## Multi-shot mode

Use only when the source brief intentionally requests cuts inside one generation.

1. Prefer 2 to 4 shots.
2. Write the scene chronologically as prose.
3. Name every transition in natural language: hard cut, match cut, dissolve, or another intended edit.
4. After each cut, re-establish shot scale, angle, subjects, and changed light.
5. Re-identify recurring subjects with the same visual identifiers.
6. State whether dialogue, ambience, or music continues or changes across each cut.

## Reliability rules

- Prefer one continuous take for first-frame image-to-video unless the planned shot explicitly cuts away.
- Keep one coherent lighting logic per shot.
- Keep critical on-screen text short and plan to verify it in post.
- Simplify chaotic physics when reliability matters.
- Save under `04_generation/prompts/ltx-2-5/<shot-id>.md`.

## Done

The prompt has one unambiguous chronological visual and audio path, with every cut and continuity carry stated explicitly.
