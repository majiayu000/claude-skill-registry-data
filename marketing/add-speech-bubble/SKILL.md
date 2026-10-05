---
name: add-speech-bubble
description: Add position-accurate speech or thought bubbles with exact text to a supplied image. Use for comics, reaction images, dialogue scenes, or annotations where bubble shape, tail target, stacking, and text legibility matter; do not use for translating existing image text, poster typography, or general caption layout.
---
# Add Speech Bubble
## Catalog
- Display name: Add Speech Bubble
- Categories: Social Media, Layout & Design
- Status: Ready
- Route label: GPT Image 2 overlay
- Tone: blue
- Short description: Add exact dialogue bubbles at the right subjects.
## What this skill does
- Adds oval, cloud, rectangle, starburst, caption, or text-only bubbles.
- Binds each text string, body, and tail endpoint to a declared speaker.
## How to use
Provide image, exact text per speaker, style, and target or location.
#### Add dialogue
```text
Add an oval bubble above the woman, tail at her mouth, exact text: “五分钟后见！”
```
## Workflow
1. Map each exact line to speaker, tail target, placement, style, and reading order.
2. Reserve faces and important objects; choose fill, stroke, font, and contrast.
3. Use `gpt-image` v1.0, GPT Image 2 Medium, original ratio, `batchCount: 1`.
4. Preserve source outside bubble regions; do not invent dialogue or cover faces.
5. Verify copy character by character, tail endpoint, speaker, layer order, legibility, and bubble count.
When this Skill selects GPT Image 2, use `quality: "medium"` and `imageSize: "2K"` by default; change either only when the user explicitly requests another tier.

Every GPT Image 2 call in this Skill defaults to Medium at 2K; use another tier only when the user explicitly requests it.

## User-facing output
- Media type: One annotated image
- Default quantity: 1
- Content per image: Source plus requested bubbles only
- Default layout: Original frame with overlays
- Model policy: GPT Image 2 Medium with agent-led copy and placement verification
- Downstream use: Comics, social posts, and annotations
