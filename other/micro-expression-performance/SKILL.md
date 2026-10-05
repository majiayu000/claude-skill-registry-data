---
name: micro-expression-performance
description: Use for a short character-performance shot where gaze, brows, mouth, breath, hands, tempo, and emotional escalation need controlled direction while identity, scene, dialogue, and camera remain fixed. Unlike make-talking-video (relationship 0.74), choose this for non-lip-sync acting; choose make-talking-video when spoken delivery is primary. Unlike generate-video (0.58), choose this when the acting layer is the result, not general scene motion.
---
# Micro-Expression Performance

## Catalog

- Display name: Micro-Expression Performance
- Categories: Portrait, Video
- Status: Ready
- Route label: Character acting-layer direction
- Tone: purple
- Short description: Direct a restrained emotional performance without changing the existing character, scene, dialogue, or camera intention.
## What this skill does

- Converts an image, script beat, or emotion phrase into observable acting beats.
- Controls gaze, brow, mouth, breath, hands, tempo, peak, and recovery without claiming facial rigging or lip sync.
- Keeps the acting layer subordinate to the supplied scene and camera intent.

## How to use

Provide a character image, script beat, or emotion phrase, plus shot duration and intensity. Canvas-capable Agents may save the approved performance pack there; otherwise they return it in chat or local delivery.

#### Example

```text
让这位角色在 5 秒内听到消息后先屏住呼吸、移开视线、忍住眼泪，最后恢复平静；保留原来的房间和中景机位。
```

## Workflow

1. Lock identity, scene, dialogue, camera, duration, and acting intensity. If duration or intensity is missing, choose a conservative default and state it.
2. Write a compact performance pack with timed gaze, brow, mouth, breath, hand, escalation, and reset beats.
3. After approval, submit one atomic performance shot to `$generate-video`, persist its `operationKey`, and poll the accepted execution ID.
4. Inspect whether the performance reads naturally without changing scene facts or adding speech, new characters, or compositing effects.

## User-facing output

- Media type: One performance prompt pack and one requested MP4 shot
- Default quantity: 1
- Content per video: One restrained emotional performance beat
- Default layout: Source or user-requested ratio
- Model policy: Current catalog-selected performance-capable video route
- Downstream use: Character scenes and drama shots

## Route

- Upstream assets: Character image, script beat, or emotion phrase
- Downstream handoff: `$make-talking-video` only when speech becomes the primary outcome
