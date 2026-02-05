---
name: sunfaded-style
description: "Create UI and graphic design layouts in the sunfaded style: oversized condensed typography, bilingual JP/EN type, high-contrast overlays on photo or illustration, halftone wave bands, and analog grain. Use when a user asks for sunfaded-like aesthetics, bold typographic posters, editorial layouts, or UI screens with this specific visual system."
---

# Sunfaded Style

## Overview

Create UI and graphic layouts with oversized condensed typography, bilingual JP/EN mixing, analog grain, and high-contrast overlays. Favor stark hierarchy and cropped type over delicate ornament.

## Workflow

1. Collect hero text, supporting text, lyric or quote line, credit list, language mix (JP/EN), EN split tokens, arrow direction, image type, target format, accent color, and asset availability.
2. Establish hierarchy: one dominant word or phrase, two to four secondary labels, a JP block, and a micro credits block (6 to 12 lines).
3. Build a strict grid, align edges, and allow type to crop at canvas boundaries. Reserve a band or plate for metadata when the image is busy.
4. Layer type over image or flat field; add a halftone band or strip for rhythm. Consider white bands, label tiles, or oversized arrows for structure.
5. Apply texture (film grain, dust, mild blur) while keeping contrast high and the reading path clear. Use local veils or blur bands to protect micro text.

## Style Pillars

- Typography: Use DIN (condensed/Engschrift if available) uppercase for hero text, pair with bold JP sans. Use micro uppercase for metadata and loosen tracking at small sizes.
- Layout: Scale headlines to edge-crop, repeat words or labels, and mix horizontal and vertical text blocks.
- Texture: Add halftone waves, moire, noise, and light paper wear; keep textures subtle but visible at 100%.
- Color: Prefer monochrome or cool desaturated tones; allow a single vivid accent color.
- Motifs: Use white bands, label tiles, oversized arrows, or fog bands to anchor the grid.
- Readability: Add a 10 to 20 percent dark overlay on photos and use local backplates for small text.

## Typography System

- Hero: DIN Condensed/DIN Engschrift, uppercase, 6x to 12x base size, tracking -0.02em to -0.04em.
- Secondary: DIN Condensed or standard DIN, 1.8x to 3x base, tracking -0.01em.
- Micro: DIN Regular uppercase, 0.6x base, tracking +0.08em to +0.12em, 6 to 12 lines, tight leading (0.9x to 1.1x).
- JP: Bold kaku gothic; use for main JP labels, keep tracking neutral, allow vertical or stacked labels.
- Fallbacks: If DIN is unavailable, use another condensed grotesk and note the substitution.

## Grid and Ratios

- Use a 12-column grid with generous gutters.
- Hero text width: 70 to 90 percent of canvas.
- Crop rule: allow at least one edge crop for the hero word.
- Margins: 5 to 8 percent outer margin; keep micro text aligned to grid.
- Vertical labels: set in a narrow 1-column strip or as a side rail.
- Micro block width: 2 to 4 columns; align to a grid edge and keep a clean block shape.
- Band height: 10 to 20 percent when used as a header or divider.

## Layout Patterns

- Pattern A: Full-bleed image + oversized hero word + micro credits block + halftone band.
- Pattern B: Repeated hero word rows with alternating scale, plus vertical JP tag.
- Pattern C: Left-aligned JP block + right-aligned EN headline, both edge-cropped.
- Pattern D: Photo + oversized hero word + top JP band + micro credits on a white plate.
- Pattern E: White field + halftone wave band + JP/EN blocks + micro credits.
- Pattern F: Oversized arrow crossing the canvas + cropped headline + side credits.

## Texture Recipes

- Grain: 2 to 6 percent opacity, fine noise, uniform across layers.
- Halftone band: diagonal lines warped by a sine curve, placed in lower third or side rail.
- Bloom: slight highlight bloom on bright areas, keep readable text crisp.
- Fold/dust: subtle crease line and dust specks at 1 to 3 percent opacity.

## UI Adaptation

- Hero: Oversized headline plus a small metadata strip; optional vertical side label or white band.
- Navigation: Tight uppercase labels, separators or rules, and minimal iconography.
- Sections: Image-backed panels with overprint type; use halftone bands as dividers.

## Constraints

- Do not copy or embed copyrighted imagery; use user-provided assets or placeholders.
- Preserve readability; avoid more than two heavy type layers in the same area.
- Keep accent colors to a single hue per layout.

## References

Read `references/sunfaded-style.md` when you need layout recipes, scale ratios, or CSS token guidance.
