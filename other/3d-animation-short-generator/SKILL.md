---
name: 3d-animation-short-generator
description: Create one complete story-driven stylized 3D animated short from premise through original character and environment references, continuity-safe multi-shot planning, rendered clips, assembly, and final film QC. Use when the requested deliverable is a finished narrative animation with multiple causally linked shots. Unlike plan-film-storyboard (relationship 0.78), this owns generated assets and final media; use plan-film-storyboard for planning-only delivery. Unlike generate-video (0.62), this owns a complete multi-shot story; use generate-video for one standalone shot. It can consume develop-story (0.55), call generate-video per shot, and hand accepted clips to combine-videos (0.38). Do not use for product-benefit ads, supplied-footage editing, one still, one clip, or imitation of a named studio or living artist.
---
# 3D Animation Short Generator

## Catalog

- Display name: 3D Animation Short Generator
- Categories: Video
- Status: Ready
- Featured: yes
- Route label: Story-to-finished stylized animation composition
- Tone: purple
- Short description: Produce one coherent multi-shot stylized 3D animated short from story lock through final-film QC.
## What this skill does

- Locks one original story, visual system, audio mode, character identities, environments, props, and continuity before paid generation.
- Converts the approved story into atomic timed shots, generates only required references and clips, and carries accepted states across the sequence.
- Assembles one finished film and verifies identity, action, screen direction, speaker/mouth behavior, sound, duration, and technical integrity.

## How to use

Provide the premise or accepted story, intended audience, duration, ratio, original visual direction, silent or dialogue-led audio mode, language, fixed character/world facts, supplied references, required/forbidden content, and desired delivery stage.

#### Example

```text
Create a 30-second 16:9 stylized 3D animated short about a shy cloud learning to make rain for one thirsty flower. Use an original warm handcrafted look, silent storytelling with music and SFX, three recurring character expressions, and deliver the finished film plus its shot manifest.
```

## Workflow

1. Freeze the final deliverable, premise, audience feeling, duration, ratio, original style coordinates, audio mode, language, fixed facts, supplied assets, and prohibited content. Use `develop-story` first only when the premise lacks a causal protagonist, conflict, or ending. Do not imitate a named studio, franchise, character, or living artist.
2. Lock one concise causal story spine with setup, escalating pressure, consequential choice, climax, and earned payoff. For dialogue-led work, finalize exact lines and use one generated speaker per shot; reserve visible reaction shots and keep non-speaker mouths closed. Silent work contains no spoken dialogue or narration.
3. Define a visual bible: original shape language, proportions, materials, palette, lighting, camera grammar, motion behavior, and negative constraints. Create only missing recurring character and environment references through appropriate installed image Atoms. Record stable identity, costume, prop, scale, scene, light, and palette anchors.
4. Build a timed atomic shot manifest totaling the requested duration. Every shot gets one narrative purpose, one continuous action, start/end state, subject positions, prop ownership, screen direction, camera, lighting inheritance, audio beat, speaker and mouth state when relevant, supplied references, generation route, and observable acceptance. Split overloaded action and multi-speaker clips.
5. Continue through the supported generation route without a client-side payment confirmation. Select one current cataloged model per shot: Kling 3.0 for precise one/two-frame control, Kling V3 Omni for several named character/scene references or motion-reference video, Seedance 2.5 for long multimodal/audio-visual/artistic/talking performance, Veo 3.1 for one-source-image premium synchronous dialogue/SFX at 16:9 or 9:16, Seedance 2.0 for routine image-led motion, and MiniMax H3 for justified large-amplitude or natural human action. Never trial models in sequence.
6. Submit one operation per shot with its own durable `operationKey`, require a non-empty `executionId`, poll to terminal state, and retain the exact accepted result. Strip planning labels from generation prompts. Preserve character/scene anchors, one action, camera, start/end state, audio behavior, and forbidden additions.
7. Inspect each terminal-success clip at first, middle, and last frames. Check character identity, proportions, costume, scene, prop state, screen direction, camera, action completion, duration, ratio, unintended text, speaker identity, mouth state, and audio. Repair only the failed shot with a new linked key and error-responsive change; never regenerate accepted clips.
8. Pass accepted clips in manifest order to `combine-videos`. Preserve approved clip audio, and add exact dialogue, captions, titles, credits, or user-supplied/otherwise supported audio through deterministic finishing when generative video cannot guarantee them. Do not claim standalone music or voice generation when no verified route exists.
9. Watch the assembled export end to end and inspect cut boundaries. Confirm causal story clarity, identity and environment continuity, complete actions, screen direction, pacing, sound intelligibility, dialogue ownership, mouth behavior, exact duration/ratio, no blank/corrupt frames, and no planning marks or unintended watermark. Report retained limitations and do not add a client-side publication confirmation; follow the API result.


## User-facing output

- Media type: One final MP4 plus story/visual lock, reference manifest, timed shot manifest, continuity report, and operation receipts
- Default quantity: 1 finished animated short
- Content per video: One original causal story told through multiple continuity-linked stylized 3D animation shots
- Default layout: User-requested ratio, duration, resolution, language, and silent or dialogue-led audio mode
- Model policy: Kling 3 precise frames; Kling Omni complex/motion references; Seedance 2.5 long audiovisual/artistic/performance; Veo source-image synchronous audio; Seedance 2.0 routine; H3 large/natural motion
- Downstream use: Human creative, continuity, audio, safety, and publication review
