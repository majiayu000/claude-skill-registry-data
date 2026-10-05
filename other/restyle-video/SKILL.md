---
name: restyle-video
description: Transform the overall visual style of supplied video while retaining timing, motion, subjects, and continuity. Use for whole-video aesthetic transfer or coherent stylization; do not use for technical color correction, one localized effect, footage assembly, object removal, or generating a new shot.
---
# Restyle Video

## Catalog

- Display name: Restyle Video
- Categories: Video
- Status: Ready
- Route label: MiniMax H3 source-video restyling
- Tone: violet
- Short description: Transform the visual treatment of a supplied video while retaining timing, motion, subjects and continuity.

- Similar skills: add-video-effect, correct-video-color, upscale-video
## What this skill does

- Applies one declared style across moving footage rather than a static color filter.
- Uses source video as motion truth and protects shot timing and identity.

## How to use

Provide a video, one target style, preservation priorities, protected text or logos and ratio.

#### Example

```text
Restyle this supplied street clip as hand-painted gouache; preserve every cut, person, motion path and camera move.
```

## Workflow

1. Analyze shot boundaries, subjects, motion, text, logos and temporal invariants.
2. Define one stable palette, texture, line and detail system across frames.
3. Run MiniMax H3, the cataloged model with verified video-editing support, against the source footage; never fake full-video restyling with first-frame animation.
4. Compare timestamps for motion, identity, timing, flicker, drift and accidental changes.

## User-facing output

- Media type: One MP4 video
- Default quantity: 1
- Content per video: The source video in one stable visual style
- Default layout: User-requested delivery format
- Model policy: MiniMax H3 for source-video editing; stop if its current adapter cannot accept the required source instead of inventing another model capability
- Downstream use: Creative video transformations
