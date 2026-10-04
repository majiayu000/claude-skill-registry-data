---
name: image
description: "Invoke when a user shares a reference image and wants new images with the same \"feel\" — composition, color palette, lighting, style, or mood — but different content. Analyzes the image across 10 aesthetic dimensions, collapses into 3 axes (Form / Aesthetic / Mood), then generates using a model matched to the original's origin with adapted prompt style. Supports iterative refinement. Trigger on: \"r"
version: 0.7.9
changelog:
  - "0.7.9 (2026-07-03): Initial conversion from MiniMax Hub"
author: "Toqsick + Yuno (Hub→Hermes conversion)"
license: "MIT"
platforms:
  - linux
  - macos
  - windows
metadata:
  hermes:
    source: "minimax-hub"
    hub_skill_id: "image-remix"
    category: "image"
    domain: "multimedia"
    converted_at: "2026-07-03T23:19:32.982629"
  tags:
    - "hub"
    - "conversion"
    - "multimodal"
triggers:
  - "image-remix"
---
> **Hub Origin:** Convexed from MiniMax Hub skill `image-remix` (version 0.7.9). Original Hub-SKILL.md is preserved at `scripts-originals/SKILL.md.hub`, original meta.yaml at `scripts-originals/meta.yaml.hub`. All Hub-specific paths (e.g. `~/.hub-global/skills/image-remix/`) translated to Hermes-equivalent references in `references/`.
# Image Remix — Image Inspiration Remix Assistant

The user sends a reference image; analyze what makes it "good," then generate images that retain the core feel but with entirely new content.

## Core Philosophy

- **Origin-Driven Generation**: First determine which model/camera/hand-drawn the original came from, then directly call the corresponding model + matching prompt style — MJ uses keyword stacking, Flux uses natural language long sentences. Origin, tool, and writing style are unified as one
- **10D -> 3D Collapse**: Internal 10-dimension analysis, collapsed into 3 user-visible dimensions: Form / Aesthetic / Mood, precisely locating the "soul dimension"
- **Preserve Feel, Replace Content**: Remix = swap content, keep the soul
- **Ultra-Lightweight Operation**: Send one image + say one sentence -> get output, results first then iterate

## Conventions

- Intermediate artifacts are stored in `./.image-remix/{session_name}/` (session_name derived from image filename, lowercased with special characters removed)
- **No collages/grids**: Each generation call produces only 1 image. Never include "grid," "collage," "2x2," etc. in prompts
- ⚠️ **MJ Four-Grid Note**: MJ always outputs a 2x2 four-grid; the user crops it on the canvas themselves
- ⚠️ **Do NOT pass reference images to text-to-image tools**: The reference image is only used for Phase 1 analysis; generation relies entirely on text prompts to avoid copyright risks

---

## Pipeline

```
Phase 0: Input  →  Phase 1: Decompose  →  Phase 2: Quick Select  →  Phase 3: Generate  →  Phase 4: Iterate  →  Phase 5: Output
```

---

## Phase 0: Input

Supported: local path / URL (download with `import_images`) / search description (use `image_search`).

Multiple images: analyze separately -> extract each image's soul dimension -> merge into a combined prompt (e.g., "Image A's composition + Image B's color palette") -> inform the user then generate.

File structure:
```
.image-remix/{session_name}/
├── decompose.json       # Phase 1 analysis results
├── generation_log.md    # Generation log
└── outputs/             # Generated images v1_01.png …
```

---

## Phase 1: Decompose

### 1a. Origin Tracing

Use `read_media` to analyze the original image's origin, cross-referencing visual fingerprints in `references/model-fingerprints.md`:

```
read_media(
  file_path=reference image path,
  question="Determine which AI model / camera / hand-drawn this image most likely comes from.
  Cross-reference the visual fingerprints in model-fingerprints.md one by one.
  Focus on: skin rendering, highlight reflections, edge blending quality, color tendencies, overall AI feel.
  Output: model_guess, confidence(0-1), clues(at least 3 specific pieces of evidence),
          alt_guess, is_ai_generated, is_photo, is_illustration"
)
```

### 1b. 10-Dimension Analysis

```
read_media(
  file_path=reference image path,
  question="Deeply analyze this image across the following 10 dimensions, providing for each:
  description (English technical description), summary (Chinese summary), score (0-1 salience):
  1.Composition 2.Art Style 3.Color (including palette hex values) 4.Lighting 5.Atmosphere
  6.Texture 7.Subject 8.Narrative 9.Post-processing Style 10.Medium/School"
)
```

### 1c. Collapse to Form / Aesthetic / Mood

| Dimension | Underlying Components | Meaning |
|-----------|----------------------|---------|
| **Form** | Composition + Subject | What is depicted and how it's arranged |
| **Aesthetic** | Art Style + Color + Texture + Post-processing + Medium | What painting style and tonal quality |
| **Mood** | Atmosphere + Lighting + Narrative | What feeling and emotion |

Take the weighted average of sub-dimension scores to identify 1-2 soul dimensions (the most distinctive ones).

### 1d. Write to decompose.json

Merge origin + dimensions + collapsed + soul fields and write to file.

---

## Phase 2: Quick Select

### Display Origin Conclusion (mandatory)

```
📍 Origin Conclusion
  Image Source: [model_guess] (confidence [confidence])
  Evidence: [2-3 most critical clues]
  Soul Dimension: [soul_summary]

🎯 Direct Call: [matched tool] — [one-sentence explanation why]
  Prompt Style: [writing strategy for this model]
  Fallback: [what to use if tool is unavailable]
```

**Origin -> Tool + Prompt Style Mapping Table** (origin directly determines which tool and style to use; the two are inseparable):

| Origin Source | Tool to Call | Prompt Style | Fallback |
|--------------|-------------|--------------|----------|
| Seedream | Seedream image generation tool | Realistic long description, precise facial features/clothing materials, refined lighting and atmosphere | `all_in_one`, keep style |
| Kolors | Kolors image generation tool | Realistic description, emphasize highlight-material contrast | `all_in_one` |
| Hunyuan | Hunyuan image generation tool | Realistic + Chinese aesthetic vocabulary, concise with breathing room | `all_in_one` |
| Jimeng | Jimeng image generation tool | Direct description, explicit style keywords, write out saturation levels | `all_in_one` |
| Wanx / Tongyi Wanxiang | Wanx image generation tool | Concise description, avoid overly dense detail stacking | `all_in_one` |
| Midjourney v5/v6 | MJ image generation tool | Keyword stacking + style tags, concise and not verbose | `all_in_one`, keep keyword style |
| Flux.1 | Flux image generation tool | Natural language long sentences, detailed lighting and material description | `all_in_one`, keep long description |
| Stable Diffusion | SD image generation tool | Supports weight syntax `(word:1.3)`, negative prompt written separately | `all_in_one`, remove weights and switch to natural language |
| DALL-E 3 | DALL-E image generation tool | Natural language, straightforward description, avoid over-stylization | `all_in_one` |
| Ideogram | Ideogram image generation tool | Specify text content and layout requirements clearly | `all_in_one` |
| Real photograph | High-realism image generation tool | Photography terminology dominant, lens parameters + film stock | `all_in_one`, keep photography terminology |
| Hand-drawn / Illustration | Illustration image generation tool | Medium + school as anchor | `all_in_one`, keep medium description |
| Generic AI / Hard to determine | `all_in_one_image_generation` | Keywords + natural language hybrid | No fallback needed |
| Completely uncertain | Multiple tools, one image each for comparison | Use each tool's optimal prompt style | — |

**Fallback rule when tool is unavailable**: Fall back to `all_in_one_image_generation`, but **keep the original tool's prompt writing style unchanged**, preserving the style DNA as much as possible.

### Generation Path Selection (must ask)

Ask the user via Q&A:

- **Text-to-Image (recommended)**: Pure text prompt, zero copyright risk
- **Image-to-Image**: Reference image passed as image_ref, higher fidelity, user must confirm copyright risk

### Content Direction Confirmation

Directly ask the user "What do you want to create?" — a single sentence is enough to proceed to generation.

If the user has no direction (only says "help me remix"), recommend 3 replacement directions based on the soul dimension for selection.

**Quick Commands**: `Reskin` (swap subject only) / `Extract Style` (preserve Aesthetic) / `Extract Composition` (preserve Form) / `Extract Mood` (preserve Mood)

---

## Phase 3: Generate

### Branch A: Text-to-Image

Strictly prohibit passing the reference image to the generation tool. The prompt is entirely reconstructed based on Phase 1 analysis.

**Prompt Construction**:
```
[New content subject]. [English description of preserved dimensions]. single subject, one image only, no grid, no collage, no text, no watermark
```

**Dimension -> Prompt Focus**:

| Preserved Dimension | Prompt Emphasis |
|--------------------|-----------------|
| Form | Camera angle, shot scale, subject position, depth layers |
| Aesthetic | Art school, hex values/color relationships, medium description, color grading reference |
| Mood | Emotion adjectives, light source description, cultural/era references, metaphorical language |

### Branch B: Image-to-Image

Reference image passed as `image_ref`; prompt focuses on describing the new content direction, with style description as supplementary guidance.

### Generation Parameters

Ask the user for size: **Follow Original** (default, measure with ffprobe then map) / 1:1 / 16:9 / 9:16

"Follow Original" mapping rules: ratio > 1.5 -> 16:9; 0.8~1.2 -> 1:1; < 0.8 -> 9:16. **Must measure first then write to task_description; guessing is prohibited.**

Default generation: **4 variants**, each called separately, with slight prompt variations to maintain diversity.

Save output to `.image-remix/{session_name}/outputs/v{version}_{index}.png`, and synchronously update `generation_log.md`.

---

## Phase 4: Iterate

After displaying results, ask about satisfaction: **Satisfied, finish** / **Fine-tune** / **Change direction** / **Switch model**.

Fine-tuning adjusts at the prompt level directly, without going back to Phase 1 for re-analysis:

| Feedback | Action |
|----------|--------|
| "Make the colors cooler" | Fine-tune color prompt words |
| "Change composition to close-up" | Adjust camera parameters |
| "Style is too different" | Strengthen style description or switch model |
| "This one's composition + that one's color" | Combine dimensions from two images and regenerate |

---

## Phase 5: Output

Delivery checklist: file location / total generated / iteration rounds / soul dimension / origin source / prompt writing strategy

Optional: CDN upload / style library entry (save to `.image-remix/style-library/{style name}.md`) / continue generating variants

**Style library format** (see `references/analysis-example.md` for an example):
```markdown
# {Style Name}
## Origin
- Image source / tool called / prompt writing strategy
## Soul Dimension
- Soul: {Form/Aesthetic/Mood} — {soul_summary}
## Successful Prompt
{complete English prompt}
## Dimension Snapshot
- Form / Aesthetic / Mood
```
