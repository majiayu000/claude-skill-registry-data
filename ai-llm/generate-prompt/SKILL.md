---
name: generate-prompt
description: Generate optimized image generation prompts for a specific interior design style and AI provider. Use when the user wants to create prompts for rendering interior designs.
---

# Generate Interior Design Prompt

Create optimized image generation prompts tailored to specific AI providers and design styles.

## Preprocessing Check (MANDATORY — run before generating prompts)

**Before generating any prompt**, detect whether this project has preprocessed control maps. This determines prompt strategy.

```
!ls projects/${PROJECT_NAME}/references/preprocessed/ 2>/dev/null && echo "HAS_CONTROL_MAPS=true" || echo "HAS_CONTROL_MAPS=false"
```

```
!ls projects/${PROJECT_NAME}/references/masks/ 2>/dev/null && echo "HAS_MASKS=true" || echo "HAS_MASKS=false"
```

```
!ls projects/${PROJECT_NAME}/references/*.{jpg,jpeg,png,webp} 2>/dev/null && echo "HAS_REFERENCE=true" || echo "HAS_REFERENCE=false"
```

### Decision Logic

```
HAS_REFERENCE=true AND HAS_CONTROL_MAPS=false?
└── STOP. Run /preprocess-room FIRST. Do NOT generate prompts without control maps when a reference photo exists.

HAS_CONTROL_MAPS=true?
└── STRUCTURE CONTROL MODE:
    - Prompt must include spatial/structural keywords: "preserving room layout", "maintaining spatial structure"
    - Prompt must emphasize materials, colors, furniture OVER room geometry (the depth map handles geometry)
    - Do NOT describe wall positions, window placement, ceiling height — the control map provides this
    - For Stability AI: prompt focuses on style + materials (structure API handles layout)
    - For Gemini editing: pass depth map as reference image alongside the style prompt

HAS_MASKS=true?
└── INPAINTING MODE:
    - Generate TWO prompts: one for the masked region only, one for full scene context
    - Masked region prompt: describe ONLY what goes in the masked area (e.g., "a tufted velvet sofa in navy blue")
    - Full context prompt: describe the whole room for coherence, but mark what changes

Neither (text-to-image)?
└── Standard mode — describe everything including room geometry, layout, spatial arrangement
```

**Mode selection is automatic.** Adjust prompt strategy silently based on what exists.

## Input Requirements

Gather from the user (ask if not provided via `$ARGUMENTS`):
1. **Room type**: living room, bedroom, kitchen, bathroom, office, dining room, etc.
2. **Design style**: reference `/style-guide` for available styles
3. **Target provider**: Gemini, OpenAI/DALL-E, Grok, Stability AI, Midjourney, or "all"
4. **Additional details** (optional): room dimensions, specific furniture, color preferences, lighting mood, camera angle

## Prompt Structure Per Provider

### OpenAI (DALL-E 3 / GPT-4o)
```
[Room type] interior design in [style] style. [Detailed description of furniture, materials, colors].
Lighting: [lighting type]. Camera angle: [angle]. Photorealistic, 8K, interior photography, architectural digest quality.
```
- Keep under 400 characters for DALL-E 3
- Be explicit about photorealism
- Specify camera angle for composition

### Google Gemini (Imagen)
```
A photorealistic interior photograph of a [room type] designed in [style] style.
Features: [materials], [furniture], [colors], [textures].
Atmosphere: [lighting], [mood].
Style: professional interior photography, high resolution, detailed textures.
```
- Gemini responds well to structured, descriptive prompts
- Emphasize "photograph" for realism

### Stability AI (Stable Diffusion)
```
Positive: photorealistic interior design, [room type], [style] style, [materials], [colors], [furniture], [lighting], professional photography, 8k uhd, ray tracing, detailed textures
Negative: cartoon, drawing, sketch, low quality, blurry, distorted, watermark, text
```
- Always include negative prompt
- Use comma-separated keyword style
- Include quality boosters: 8k, ray tracing, detailed

### Midjourney
```
[Room type] interior, [style] design style, [key materials and colors], [lighting mood], professional interior photography --ar 16:9 --v 6 --style raw --q 2
```
- Use `--ar` for aspect ratio (16:9 for wide rooms, 4:3 for detail shots)
- `--style raw` for photorealism
- Keep descriptive, flowing language

### Grok (xAI)
```
Generate a photorealistic image of a [room type] with [style] interior design.
Include: [specific furniture], [materials like marble/wood/fabric], [color palette].
Mood: [warm/cool/dramatic/serene]. Lighting: [natural/artificial/mixed].
```

## Output Format

Present the generated prompts in a clear format:
1. Show the prompt for each requested provider
2. Highlight style-specific keywords used (from style guide)
3. Suggest 2-3 variations (different camera angles, lighting moods, or detail focus)
4. Note any provider-specific limitations or tips

## Session Relevant Skills

- `/render` — the natural next step. Takes these prompts and sends them to AI providers. Suggest specific providers based on the style (e.g., Stability for texture-heavy styles, DALL-E for clean modern looks).
- `/style-guide` — essential reference during prompt generation. Always pull keywords, materials, and colors from the style guide to ensure accuracy. Don't rely on memory — styles have specific vocabulary.
- `/mood-board` — if the user came here without a mood board, the prompts may lack atmospheric depth. Suggest /mood-board first for complex or ambiance-heavy styles (Wabi-Sabi, Bohemian, Biophilic).
- `/design-consult` — if requirements are unclear (no room type, no style, no preferences), redirect to /design-consult rather than guessing.
- `/compare-models` — after /render with multiple providers, /compare-models evaluates which output is best.
- `/edit-design` — if the user has a reference image and wants prompts based on it, redirect to /edit-design which handles scene analysis before prompt generation.

## Gotchas

- **Provider prompt lengths differ wildly**: DALL-E 3 = under 400 chars. Midjourney = flowing description. Stability = comma-separated keywords. Don't use one format for all providers.
- **Negative prompts are not universal**: Only Stability AI uses explicit negative prompts. Don't add negative prompt sections for DALL-E or Gemini — they ignore or misinterpret them.
- **"All providers" is expensive**: Generating for all providers means multiple API calls. Ask the user if they really want all, or suggest 2-3 best providers for their style.
- **Style keywords order matters**: Put the most important style descriptors first. AI models weight earlier tokens more heavily. Room type and style should lead, decorative details follow.
