---
name: refine
description: Iteratively refine image generation prompts based on feedback about previous renders. Use when the user wants to improve a generated interior design image.
---

# Iterative Prompt Refinement

Improve interior design renders through systematic prompt refinement based on user feedback.

## Preprocessing Check (MANDATORY — run before refining)

**Before refining any prompt**, check for preprocessed control maps and masks. This affects refinement strategy.

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
└── STOP. Run /preprocess-room FIRST. Cannot refine properly without knowing if layout control is available.

HAS_CONTROL_MAPS=true BUT previous prompt was text-to-image (no structure keywords)?
└── This is a ROOT CAUSE issue — the original prompt ignored available control maps.
    Don't patch the prompt. Rebuild it in STRUCTURE CONTROL MODE:
    - Remove room geometry descriptions (depth map handles this)
    - Add "preserving room layout", "maintaining spatial structure"
    - Focus prompt on style, materials, colors, atmosphere
    - Suggest re-rendering via structure control API instead of text-to-image

HAS_MASKS=true BUT previous render used full generation (not inpainting)?
└── Suggest switching to INPAINTING MODE for targeted changes instead of refining the full prompt.

HAS_CONTROL_MAPS=true AND previous prompt already uses structure mode?
└── Refine normally, but keep structural keywords intact. Focus refinement on style/material/color/lighting only.
```

**Mode-aware refinement is automatic.** If control maps exist but weren't used, that's the real problem — not the prompt wording.

## Input

Gather from user or `$ARGUMENTS`:
- **Previous prompt**: the prompt that generated the current image
- **Provider**: which AI provider was used
- **Feedback**: what to improve (can be free-form)
- **Reference image path** (optional): the current render to improve upon

## Refinement Categories

Guide the user through specific feedback if their input is vague:

### Style Adjustments
- "More/less [style element]" — adjust style keyword intensity
- "Add [style] influences" — blend in secondary style elements
- "Wrong period/era" — correct historical references

### Color Corrections
- "Too warm/cool" — adjust color temperature keywords
- "More contrast/muted" — modify saturation descriptors
- "Wrong dominant color" — restructure color priority in prompt

### Composition Changes
- "Different angle" — modify camera/perspective keywords
- "Closer/wider view" — adjust focal length descriptors
- "Show more of [area]" — reframe composition focus

### Detail Improvements
- "More texture detail" — add specific material descriptors
- "Furniture looks wrong" — specify exact furniture styles
- "Lighting is off" — adjust lighting keywords (golden hour, diffused, dramatic)

### Realism Boost
- "Looks too AI-generated" — add photography-specific terms
- "Proportions are off" — add scale references
- "Missing shadows/reflections" — add rendering quality keywords

## Refinement Process

1. **Analyze feedback** against the original prompt
2. **Identify weak areas** in the prompt that caused the issue
3. **Generate refined prompt** with tracked changes (show diff)
4. **Explain changes**: why each modification should improve the result
5. **Suggest provider switch** if the issue is provider-specific (e.g., "Stability handles textures better for this style")

## Output

```
### Original Prompt:
[original]

### Feedback Applied:
- [change 1]: [reason]
- [change 2]: [reason]

### Refined Prompt:
[new prompt]

### Expected Improvement:
[what should be different in the new render]
```

Offer to `/render` the refined prompt immediately, or generate additional variations.

## Refinement History

Track refinement iterations so the user can see progression:
- Iteration 1: original prompt
- Iteration 2: [feedback] → [changes]
- Iteration 3: [feedback] → [changes]

This history helps identify patterns in what works for specific styles and providers.

## Session Relevant Skills

- `/render` — after generating the refined prompt, use /render to execute it. Always render with the same provider as the original unless suggesting a provider switch.
- `/compare-models` — if refinement isn't working with one provider, render the refined prompt across multiple providers via /render, then /compare-models to find a better fit.
- `/generate-prompt` — if after 3+ refinement iterations the result is still poor, the base prompt may be fundamentally flawed. Go back to /generate-prompt to rebuild from scratch rather than patching.
- `/style-guide` — reference when feedback involves style accuracy. "It doesn't look Japandi enough" → check /style-guide for missing Japandi keywords.
- `/edit-design` — if feedback is about specific objects ("the sofa looks wrong", "add a plant in the corner"), /edit-design with inpainting may be more effective than prompt refinement.
- `/mood-board` — if the render consistently misses the "feel" of the space, the issue may be upstream. A mood board captures atmosphere better than prompt keywords alone.

## Gotchas

- **Don't refine forever**: After 3-4 iterations with diminishing returns, either switch providers or rebuild the prompt from scratch via /generate-prompt. Prompt patching has limits.
- **Track what changed**: Always show the diff between old and new prompts. Without tracked changes, refinement becomes random prompt mutation.
- **Provider switch is a valid refinement**: Sometimes the issue isn't the prompt — it's the provider. Stability handles textures differently than DALL-E. Suggest switching when the feedback pattern matches a known provider weakness.
- **Refinement is not editing**: /refine adjusts the prompt for a fresh render. If the user wants to keep 90% of an existing image and change 10%, that's /edit-design territory.
- **Feedback must be specific**: "It doesn't look good" is unusable. Guide the user through the refinement categories (style, color, composition, detail, realism) to get actionable feedback.
