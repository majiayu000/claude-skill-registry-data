---
name: edit-design
description: Edit an existing interior design image — analyze objects, style, materials, then generate targeted prompts for specific changes. Use when the user sends a reference image and wants modifications (change style, swap furniture, adjust colors, add/remove elements).
---

# Edit Interior Design Image

Analyze a reference interior design image, identify what the user wants to change, and generate targeted prompts that preserve unchanged elements while modifying specific aspects.

## Auto-Preprocessing (MANDATORY — run before any analysis)

**Before ANY analysis**, run these checks to determine what's available:

```
!ls projects/${PROJECT_NAME}/references/preprocessed/depth_map.png 2>/dev/null && echo "HAS_DEPTH=true" || echo "HAS_DEPTH=false"
```

```
!ls projects/${PROJECT_NAME}/references/preprocessed/canny_edge.png 2>/dev/null && echo "HAS_CANNY=true" || echo "HAS_CANNY=false"
```

```
!ls projects/${PROJECT_NAME}/references/preprocessed/semantic_analysis.json 2>/dev/null && echo "HAS_SEMANTIC=true" || echo "HAS_SEMANTIC=false"
```

```
!ls projects/${PROJECT_NAME}/references/preprocessed/segmentation.png 2>/dev/null && echo "HAS_SEGMENTATION=true" || echo "HAS_SEGMENTATION=false"
```

```
!ls projects/${PROJECT_NAME}/references/masks/*.png 2>/dev/null && echo "HAS_MASKS=true" || echo "HAS_MASKS=false"
```

### Decision Logic

```
HAS_DEPTH=false OR HAS_SEMANTIC=false?
└── Run /preprocess-room on the reference image AUTOMATICALLY (do NOT ask user).
    Wait for completion before proceeding to analysis.

HAS_SEMANTIC=true?
└── Read semantic_analysis.json — use it for Scene Inventory (Step 1) instead of re-analyzing manually.
    This gives you accurate style, materials, colors, lighting from Gemini Vision.

User wants specific element change (sofa, walls, floor)?
├── HAS_SEGMENTATION=true → Use segmentation to identify element boundaries
├── HAS_MASKS=true for that element → Reuse existing mask
└── Neither → Run /mask-room for target element

User wants full style change?
└── Use structure control (depth map) for rendering — HAS_DEPTH must be true

User wants minor adjustment (color, lighting)?
└── Inpainting with broad mask may suffice
```

**This step is silent** — just do it, don't explain to the user unless they ask.

## Input Requirements

Gather from the user (ask if not provided via `$ARGUMENTS`):
1. **Reference image**: the image to edit (user must provide)
2. **Desired changes**: what to modify — can be free-form (e.g., "make it Japandi", "swap the sofa for a sectional", "warmer lighting")
3. **Target provider**: Gemini, OpenAI/DALL-E, Grok, Stability AI, Midjourney, or "all"
4. **Preserve list** (optional): elements the user explicitly wants to keep unchanged

## Analysis Process

### Step 0 — Preprocess (auto, silent)
- Run `/preprocess-room` if `references/preprocessed/` is empty or stale
- If user requests element-specific change → run `/mask-room` for target element
- Store paths for use in Step 3 prompt generation

### Step 1 — Scene Inventory

Analyze the reference image and document:

```
## Scene Inventory

### Room
- Type: [bathroom / living room / bedroom / etc.]
- Dimensions feel: [compact / medium / spacious]
- Layout: [L-shaped / rectangular / open-plan / etc.]

### Objects
- [object 1]: [description, position, material, color]
- [object 2]: [description, position, material, color]
- ...

### Surfaces
- Walls: [material, color, finish]
- Floor: [material, color, pattern]
- Ceiling: [material, color, height feel]

### Style
- Primary: [identified style]
- Secondary influences: [if any]
- Era/mood: [modern luxury / rustic warmth / etc.]

### Materials Palette
- [material 1]: [where used]
- [material 2]: [where used]

### Color Palette
- Dominant: [color]
- Secondary: [color]
- Accents: [color]

### Lighting
- Type: [natural / artificial / mixed]
- Sources: [windows / recessed / pendant / LED strip / etc.]
- Mood: [warm / cool / dramatic / soft]
- Direction: [overhead / side / backlit / etc.]

### Camera
- Angle: [eye-level / elevated / low / bird's eye]
- Lens feel: [wide-angle / standard / telephoto]
- Composition: [centered / rule-of-thirds / diagonal]
```

### Step 2 — Change Analysis (Diff)

Compare user's request against the scene inventory:

```
## Change Diff

### KEEP (unchanged)
- [element]: [reason to preserve]
- ...

### MODIFY (change in place)
- [element]: [current state] → [target state]
- ...

### ADD (new elements)
- [element]: [description, placement]
- ...

### REMOVE
- [element]: [reason]
- ...

### STYLE SHIFT (if applicable)
- From: [current style] → To: [target style]
- Keywords changing: [old keywords] → [new keywords]
- Materials changing: [old] → [new]
- Colors changing: [old] → [new]
```

### Step 3 — Generate Edit Prompts

Generate prompts per provider, incorporating the diff. Use style keywords from `/style-guide` for the target style.

**IMPORTANT — Visual Context for Gemini**: When rendering via Gemini, the `/render` skill will automatically attach all available preprocessed maps (depth, segmentation, masks) alongside the original image. Your edit prompt should reference these maps when relevant:
- If depth map exists → mention "preserve the spatial layout shown in the depth map"
- If segmentation exists → mention specific zones by name (e.g., "change only the wall zones visible in the segmentation map")
- If masks exist → mention "apply changes only to the masked area"

This gives Gemini multimodal context to understand room structure beyond just the photo.

#### Full Re-render Prompt

For providers without edit/inpainting APIs — generate a complete prompt that describes the final desired result, preserving unchanged layout/composition while incorporating all changes.

Follow the provider-specific prompt structures from `/generate-prompt`:
- **OpenAI**: Under 400 chars, explicit photorealism
- **Gemini**: Structured sections (Features/Atmosphere/Style) — prompt can reference depth/segmentation context since those images are sent alongside
- **Stability AI**: Positive + Negative prompt, keyword style
- **Midjourney**: Flowing description + parameters
- **Grok**: Structured with mood/lighting sections

#### Inpainting / Edit Prompt (when supported)

For providers with edit APIs (OpenAI DALL-E edit, Stability AI inpainting):

```
## Inpainting Prompt

### Region to edit: [description of area — e.g., "the wall behind the vanity"]
### Edit instruction: [what to change in that region]
### Context preservation: [surrounding elements to keep consistent]
```

## Output Format

```
## 1. Scene Analysis
[Scene inventory from Step 1]

## 2. Edit Plan
[Change diff from Step 2]

## 3. Generated Prompts

### [Provider Name]

#### Full Re-render:
[complete prompt for generating the modified design from scratch]

#### Inpainting (if supported):
[targeted edit prompt for modifying specific regions]

## 4. Style Keywords Applied
- From `/style-guide` [target style]: [keywords used]

## 5. Recommendations
- [Which approach works best: full re-render vs inpainting]
- [Which provider handles this type of edit best]
- [Potential issues to watch for — e.g., "style blending may produce inconsistent furniture"]
```

## Tips

- When changing style but keeping layout: emphasize spatial description and camera angle in the prompt to maintain composition
- When swapping single objects: inpainting is preferred over full re-render for consistency
- When adjusting colors/lighting only: minimal prompt changes needed — focus on atmosphere section
- For adding plants/decor: be specific about placement relative to existing objects
- Reference `/style-guide` for accurate style vocabulary when shifting between styles

## Session Relevant Skills

- `/render` — after generating edit prompts, use /render to execute them. For inpainting edits, ensure the provider supports edit APIs (OpenAI DALL-E edit, Stability inpainting).
- `/style-guide` — critical when changing styles. Use the target style's exact keywords, materials, and colors from the guide. Style shifts with wrong vocabulary produce hybrid-mush.
- `/generate-prompt` — used internally for prompt format reference. Follow the same provider-specific structures when generating edit prompts.
- `/refine` — if the first edit render doesn't match expectations, use /refine to iterate. Pass both the original image context and the edit feedback.
- `/compare-models` — if editing across multiple providers, compare which one best preserved the unchanged elements while applying the edits.
- `/design-consult` — if the user wants a complete redesign rather than targeted edits, redirect to /design-consult. Edit-design is for surgical changes, not ground-up rethinking.

## Gotchas

- **Inpainting vs full re-render**: For small changes (swap one object, adjust color), inpainting preserves consistency. For style shifts or major layout changes, full re-render is more reliable.
- **Scene inventory must be exhaustive**: Missing an element in the inventory means the re-render prompt won't describe it, and it disappears. List everything visible.
- **Camera angle preservation is critical**: If the re-render changes the camera angle, the edit feels like a different room, not a modified one. Always explicitly describe the original camera angle and lens feel.
- **Don't edit what should be redesigned**: If the user wants to change style + furniture + colors + lighting, that's a redesign. Redirect to /design-consult → /generate-prompt flow.
- **Reference image quality matters**: Low-res or heavily compressed reference images produce poor scene inventories. Ask for the best quality available.
