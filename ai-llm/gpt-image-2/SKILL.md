---
name: gpt-image-2
description: Advanced image generation and editing with reasoning capabilities, editing tools and platform-specific settings. Use when creating or editing images with an AI image model.
---

# GPT Image 2 (AI Image Generation)

Produce and edit images with an image model using structured, platform-aware prompts.

## Generation workflow
1. **Intent** — subject, purpose and platform (IG, YouTube, blog header...).
2. **Prompt structure** — write prompts as: `[subject] + [action/pose] + [environment] + [composition/camera] + [lighting] + [style/medium] + [mood] + [negative constraints]`.
3. **Reasoning step** — before prompting, reason about what visually communicates the message (symbols, setting, expression) instead of literal depiction.
4. **Platform settings** — set aspect/size per target: IG post 1080x1080, reel/story 1080x1920, YouTube thumb 1280x720, X header 1500x500, Dribbble 400x300.
5. **Iterate** — refine one parameter at a time; keep a prompt log.

## Editing workflow
- Addition / removal / replacement: describe precisely what changes and what must stay identical (lighting, perspective, grain).
- Inpainting: specify the region; outpainting: specify extension direction and content continuity.

## Quality rules
- One clear subject; specify camera (e.g. "85mm portrait", "isometric", "top-down flat lay").
- Always declare text that must appear in-image, in quotes, short (models garble long text).
- Check hands, text, reflections and logos in every output before delivering.

## Output
Final image(s) + the exact prompt used + suggested variations.
