---
name: banner-design
description: Design platform-ready banners, covers, display ads, website heroes, and print headers with clear hierarchy, safe zones, responsive crops, accessible.
---

# Banner Design

Create a focused communication asset, not a miniature webpage. Resolve skill-dir to this skill folder and read references/banner-sizes-and-styles.md when exact dimensions or safe zones matter.

## Workflow

1. Define the job.
   - Identify platform, placement, dimensions, audience, message, call to action, brand constraints, and required variants.
   - If dimensions are unknown, verify the current platform requirement or label the proposed size as a working assumption.

2. Establish hierarchy.
   - One primary message, one supporting line when needed, one primary action.
   - Preserve legibility at thumbnail size.
   - Keep logos and essential text inside the safest common crop.

3. Propose 2-3 meaningfully different art directions.
   - Change composition, imagery, type treatment, or visual metaphor.
   - Do not produce cosmetic color swaps as separate concepts.
   - Explain the audience and placement fit of each direction.

4. Select and build.
   - Use the active host's available image-generation, design, browser, or code tools.
   - If image generation is unavailable, create a tool-neutral prompt, SVG/CSS composition, or production-ready design specification.
   - Never require a named model or another skill's fixed installation path.

5. Adapt variants from one source composition.
   - Recompose for each aspect ratio; do not stretch.
   - Keep type scale, spacing, color, imagery, and CTA treatment consistent.
   - Record intentional content differences between placements.

6. Validate.
   - Check contrast, safe zones, crop behavior, text accuracy, logo clear space, file size, and export dimensions.
   - Inspect at actual size and thumbnail size.
   - Check that the CTA and important content survive mobile and desktop crops.

## Output contract

Provide:

- chosen direction and rationale;
- exact dimensions and variant list;
- copy hierarchy;
- color, type, image, and layout specification;
- editable source or implementation artifact when requested;
- validation results and any unverified platform constraint.

## Guardrails

- Do not invent current social-platform dimensions; verify when freshness matters.
- Do not place essential text near crop-prone edges.
- Do not use generated text inside imagery when accurate typography is required; overlay real text in the layout.
- Do not mix unrelated styles or more than one primary CTA.
- Do not use provider or model names unless the user chose one.
