---
name: compare-models
description: Side-by-side comparison of image generation outputs across different AI providers. Use after rendering the same prompt through multiple providers to evaluate quality, style accuracy, and cost.
---

# Compare AI Model Outputs

Analyze and compare interior design renders from different AI providers to help the user choose the best output or provider for their needs.

## Pre-flight Checks (MANDATORY — run before comparison)

**Before comparing**, check what renders and data are available.

```
!ls projects/${PROJECT_NAME}/renders/*.png 2>/dev/null | head -20 && echo "HAS_RENDERS=true" || echo "HAS_RENDERS=false"
```

```
!ls projects/${PROJECT_NAME}/renders/ 2>/dev/null | grep -c '.png' && echo "RENDER_COUNT above"
```

```
!ls projects/${PROJECT_NAME}/references/preprocessed/depth_map.png 2>/dev/null && echo "HAS_DEPTH=true" || echo "HAS_DEPTH=false"
```

```
!ls projects/${PROJECT_NAME}/references/*.{jpg,jpeg,png,webp} 2>/dev/null && echo "HAS_REFERENCE=true" || echo "HAS_REFERENCE=false"
```

```
!ls projects/${PROJECT_NAME}/style-config.yaml 2>/dev/null && echo "HAS_STYLE_CONFIG=true" || echo "HAS_STYLE_CONFIG=false"
```

```
!ls projects/${PROJECT_NAME}/notes.md 2>/dev/null && echo "HAS_NOTES=true" || echo "HAS_NOTES=false"
```

### Decision Logic

```
HAS_RENDERS=false OR RENDER_COUNT < 2?
└── STOP. Need at least 2 renders to compare. Run /render with multiple providers first.

HAS_DEPTH=true AND HAS_REFERENCE=true?
└── Include "Layout Preservation" criterion in comparison.
    Auto-run /validate-layout for each render and include SSIM scores in the table.

HAS_DEPTH=false AND HAS_REFERENCE=true?
└── Layout comparison available but depth map missing.
    Suggest running /preprocess-room first for quantitative layout scoring.
    OR skip layout criterion if user doesn't care about layout fidelity.

HAS_STYLE_CONFIG=true?
└── Read style-config.yaml — use configured colors, materials, style as ground truth for "Style Accuracy" scoring.
    Don't judge style accuracy by memory — check against the config.

HAS_NOTES=true?
└── Read notes.md — check for previous comparison results and feedback trends.
    Append new comparison results to notes.md.

No reference photo (text-to-image only)?
└── Skip "Layout Preservation" criterion entirely — not applicable.
```

**Data-driven comparison > subjective comparison.** Use project config as ground truth wherever possible.

## Input

- Multiple rendered images from `/render` (or image paths provided by user)
- The original prompt used
- The target design style

## Comparison Criteria

Evaluate each provider's output on:

### 1. Style Accuracy
- Does it match the requested interior design style?
- Are style-specific materials, colors, and furniture correct?
- Rate: Excellent / Good / Partial / Poor

### 2. Photorealism
- Does it look like a real photograph?
- Texture quality and material rendering
- Lighting naturalness
- Rate: Photorealistic / Near-photo / Illustrated / Artificial

### 3. Composition
- Camera angle and framing
- Spatial depth and perspective accuracy
- Room proportions and scale of furniture
- Rate: Professional / Adequate / Awkward

### 4. Detail Quality
- Fine details: fabric patterns, wood grain, reflections
- Consistency: no floating objects, impossible geometry, weird artifacts
- Text/watermark issues
- Rate: High detail / Medium / Low / Artifacts present

### 5. Color Fidelity
- Does the color palette match the design brief?
- Color harmony and balance
- Lighting effect on colors (warm/cool cast)

### 6. Practical Value
- Could this image be used in a client presentation?
- Would it work as a design reference?
- Does it communicate the design intent clearly?

### 7. Layout Preservation (when comparing against reference photo)
- Does the generated image maintain the original room's spatial layout?
- Depth SSIM score (from `/validate-layout`): quantitative layout fidelity metric
- Wall positions, window placements, furniture depth ordering preserved?
- Rate: Identical / Good / Fair / Distorted

## Output Format

```
## Model Comparison: [Style] [Room]

| Criteria         | Gemini | OpenAI | Stability | Grok |
|-----------------|--------|--------|-----------|------|
| Style Accuracy  |   ★★★★ |  ★★★★  |   ★★★★    | ★★★  |
| Photorealism    |   ...  |  ...   |   ...     | ...  |
| Composition     |   ...  |  ...   |   ...     | ...  |
| Detail Quality  |   ...  |  ...   |   ...     | ...  |
| Color Fidelity  |   ...  |  ...   |   ...     | ...  |
| Layout Fidelity |   ...  |  ...   |   ...     | ...  |

### Best For:
- **Client presentation**: [provider] — [reason]
- **Design exploration**: [provider] — [reason]
- **Quick iteration**: [provider] — [reason]
- **Budget-conscious**: [provider] — [reason]

### Recommendations:
- [Specific refinement suggestions per provider]
```

Suggest `/refine` for the most promising output to iterate further.

## Session Relevant Skills

- `/refine` — after identifying the best provider output, use /refine to iterate on that specific prompt+provider combination. Pass the original prompt and specific feedback from the comparison.
- `/render` — if the comparison reveals all outputs are poor, consider re-rendering with adjusted prompts. Go back to /generate-prompt if the prompts themselves need rework.
- `/generate-prompt` — if comparison shows systematic prompt issues (wrong style keywords, bad composition across all providers), the prompts need regeneration, not refinement.
- `/style-guide` — reference when evaluating style accuracy. Use the style's specific keywords/materials/colors as the ground truth for scoring.
- `/edit-design` — if one render is close but needs specific changes (swap a piece of furniture, adjust lighting), /edit-design can target those changes rather than re-rendering from scratch.
- `/validate-layout` — provides quantitative SSIM scores for layout comparison. Run on each provider's output to get objective layout fidelity metrics.
- `/preprocess-room` — the source of truth for the original room's depth map used in layout comparison.

## Gotchas

- **Compare apples to apples**: Ensure all images used the same (or equivalent) prompt. Different prompts produce different styles — that's a prompt issue, not a provider issue.
- **Don't compare more than 4-5 providers at once**: The comparison table becomes unwieldy. Focus on 2-3 most promising providers.
- **Provider strengths are style-dependent**: Stability excels at textured/rustic styles, DALL-E at clean modern, Midjourney at atmospheric/dramatic. A provider ranking for Scandinavian may be reversed for Baroque.
- **Practical value matters most**: A slightly less photorealistic image that clearly communicates the design intent is more useful than a photorealistic image with wrong style elements.
- **Layout comparison only applies when there's a reference photo**: For text-only generations (no reference room), skip the layout criterion entirely.
- **Different providers have different layout control capabilities**: Stability AI structure control and Gemini image editing can preserve layout; DALL-E and Midjourney cannot. Factor this into comparisons.
