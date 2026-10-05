---
name: image-media
description: Generate, edit, and process visual artifacts, diagrams, and multimedia
  assets. Use when creating UI mockups, visual explainers, image transformations,
  or media layouts (carousel, bento grid).
argument-hint: <image prompt or media task>
---

<!-- Generated from skills/image-media.md by tools/generate_integrations.py. Edit the source file, not this one. -->

# Skill: Image & Media Handling

## Purpose
Generate, edit, and process images and other media assets. _Source: Canva (Category A)_

## Tools Required
- Image generation tools (text2im, image_gen) _Source: OpenAI (Category C)_
- Image editing tools (image_edit) _Source: OpenAI (Category C)_
- Video generation tools (video_gen) _Source: OpenAI (Category C)_
- Vision/analysis tools _Source: OpenAI (Category C)_

## General Principles
- Only generate images when they add significant value to the response _Source: Canva (Category B)_
- If text alone is clear and sufficient, don't add images _Source: Canva (Category B)_
- Prefer built-in vision capabilities over OCR — OCR is high-cost, high-risk, last-resort _Source: Gemini (Category T)_
- OCR libraries support English only _Source: Gemini (Category T)_

## Image Generation

### When to Generate Images
**High value use cases:** _Source: Canva (Category E)_
- Explaining processes visually _Source: Canva (Category E)_
- Browsing and inspiration _Source: Canva (Category E)_
- Exploratory context _Source: Canva (Category E)_
- Highlighting differences (before/after) _Source: Canva (Category E)_
- Quick visual grounding _Source: Canva (Category E)_
- Visual comprehension _Source: Canva (Category E)_
- Introducing people/places _Source: Canva (Category E)_

**Low value / avoid:** _Source: Canva (Category E)_
- UI walkthroughs without exact current screenshots _Source: Canva (Category E)_
- Precise comparisons requiring accuracy _Source: Canva (Category E)_
- Speculation / spoilers / guesswork _Source: Canva (Category E)_
- Mathematical accuracy _Source: Canva (Category E)_
- Casual chit-chat / emotional support _Source: Canva (Category E)_
- Pure text-based tasks (definitions, grammar) _Source: Canva (Category E)_
- Writing / coding / data analysis _Source: Canva (Category E)_

### Layout Options
- **carousel** (default): swipeable images in a row _Source: Canva (Category Q)_
- **bento**: grid layout at top of response as cover — use for single entity deep-dives (person, place, sport team) _Source: Canva (Category Q)_

### Image Parameters
- Aspect ratio: `1:1` (default) or `16:9` _Source: Canva (Category Q)_
- Query: search terms to find relevant images _Source: Canva (Category Q)_
- num_per_query: 1-5 images per query term _Source: Canva (Category Q)_
- size: image dimensions _Source: Canva (Category Q)_
- transparent_background: for PNG output _Source: Canva (Category Q)_

## Image Editing
- Modify existing images based on instructions _Source: Canva (Category E)_
- Add/remove elements _Source: Canva (Category E)_
- Alter colors, style transfer _Source: Canva (Category E)_
- Improve quality/resolution _Source: Canva (Category E)_
- Transform style (cartoon, oil painting, etc.) _Source: Canva (Category E)_

## Video Generation
- Available when the tool supports it _Source: OpenAI (Category C)_
- Text-to-video with audio cues _Source: OpenAI (Category C)_
- Extending existing videos _Source: OpenAI (Category C)_
- Generating videos between specified first and last frames _Source: OpenAI (Category C)_
- Using reference images to guide content _Source: OpenAI (Category C)_

## Visual Analysis
- Use vision capabilities to describe image content _Source: Gemini (Category T)_
- Extract text from images when necessary _Source: Gemini (Category T)_
- Analyze charts, diagrams, screenshots _Source: Gemini (Category T)_
- Identify objects, people, scenes _Source: Gemini (Category T)_
- Read UI layouts for automation _Source: Gemini (Category T)_

## When to Use Multiple Image Groups
- Long, multi-section answers: one image group per major section _Source: Canva (Category Q)_
- Compare-and-contrast across categories _Source: Canva (Category E)_
- Timeline or era segmentation _Source: Canva (Category E)_
- Geographic or regional breakdowns _Source: Canva (Category E)_
- Ingredient → steps → finished result _Source: Canva (Category E)_

## Image Citations
- When using web-sourced images, cite the source _Source: Perplexity (Category L)_
- For generated images, no citation needed _Source: Canva (Category L)_
- Don't fabricate image URLs _Source: MyAI (Category G)_
