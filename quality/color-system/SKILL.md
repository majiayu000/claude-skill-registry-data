---
name: color-system
description: Define a brand color system with functional roles, accessible combinations, tonal scales, dark or light context, reproduction guidance, and consistent application across media.
---
# Brand Color System

Use when a brand needs a color palette that works as a system rather than a list of swatches.

## Procedure
1. Start from brand positioning and real use cases, then identify roles such as primary, accent, neutral, background, foreground, status, data, or illustration colors.
2. Build tonal ranges only where needed for hierarchy, interaction, surfaces, or illustration; avoid generating dozens of unused shades.
3. Define approved foreground and background combinations and verify contrast for text, controls, focus, and non-text information where accessibility applies.
4. Test colors in light and dark or alternate environments, screens with different calibration, print or process constraints, and imagery overlays relevant to the brand.
5. Define semantic use so color meaning remains consistent and does not conflict with product status conventions.
6. Provide values in the formats needed by downstream systems and document conversions or gamut limits rather than assuming hex values solve every medium.
7. Ensure important meaning is not communicated by color alone.
8. Validate representative brand applications before freezing the palette.

## Decision rules
- A palette becomes a system when colors have jobs and relationships.
- Do not expand tonal scales beyond actual usage needs.
- Accessible color combinations must be evaluated in context, not from palette swatches alone.
- Print and digital color are related but not identical production spaces.

## Quality gate
The color system is ready when roles and combinations are explicit, important accessibility constraints are satisfied, meaning does not depend on color alone, digital and print application differences are documented, and representative artifacts demonstrate coherent use.