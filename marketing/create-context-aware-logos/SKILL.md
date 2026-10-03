---
name: create-context-aware-logos
description: Design original, scalable logos and production-ready asset sets for a specific usage context. Use when Codex needs to create or refine a logo, symbol, wordmark, app icon, repository identity, CLI mark, website brand, social preview, or Codex skill/plugin icon; adapt concepts, formats, dimensions, variants, and delivery checks to the target platform instead of producing a context-free image.
---

# Create Context-Aware Logos

Design the smallest coherent identity that works in the places where the logo will actually appear.

## Establish the Brief

Infer what is already clear. Ask only for missing information that would materially change the design:

- name and optional tagline;
- product purpose and audience;
- target context;
- desired character and explicit dislikes;
- required brand colors or existing assets;
- concepts, marks, or competitors to avoid.

If the target context is known, do not ask the user to choose file formats or dimensions. Read
[references/scenario-deliverables.md](references/scenario-deliverables.md) and select them.

## Choose the Delivery Scope

Default to the MVP identity:

1. three genuinely different concept directions;
2. one selected direction refined into a primary mark;
3. monochrome, light-background, and dark-background variants;
4. the minimum asset set for the target context;
5. usage snippets or placement instructions;
6. technical and visual QA.

Expand beyond the MVP only when the user requests a full identity system, many campaign assets,
animated marks, physical mockups, or a presentation showcase.

## Design the Concepts

For each direction:

- connect the geometry to the product idea;
- make the silhouette distinct at small size;
- avoid decorative complexity that disappears below 32 px;
- avoid relying on color to make the mark recognizable;
- avoid generic AI brains, sparkles, chat bubbles, and copied industry symbols unless the brief
  specifically justifies them;
- avoid confusing similarity to named brands or platform owners.

Prefer SVG for geometric marks and wordmarks. Use a bitmap image generator only when the requested
identity is illustrative, textured, photographic, or intentionally organic. Do not trace generated
bitmap output into meaningless vector paths.

Show concepts together with a short rationale and the main tradeoff of each. Do not present minor
parameter changes as separate concepts.

## Refine the Selected Direction

After the user chooses a direction:

1. normalize geometry, spacing, stroke behavior, and optical alignment;
2. define a compact color palette with accessible foreground/background pairs;
3. create the scenario-specific variants and exports;
4. add concise alt text and usage guidance;
5. preserve an editable SVG source of truth.

If the user explicitly delegates selection, choose the concept that best satisfies small-size
recognition, distinctiveness, context fit, and reproduction simplicity.

## Validate

Check the mark at 16, 24, 32, 64, and 256 px. Inspect it on light and dark backgrounds and in
monochrome. Confirm that text remains legible, clear space is consistent, and no element is clipped.

Run:

```powershell
python scripts/validate_logo_assets.py <asset-directory>
```

Fix errors before delivery. Treat warnings as review prompts, not automatic failures.

Do not claim trademark clearance. When commercial risk matters, run a separate name and similarity
search and recommend professional legal review for unresolved conflicts.

## Deliver

Lead with the chosen direction and why it fits. Provide:

- editable source files;
- platform-ready exports;
- color values;
- minimum-size and clear-space guidance;
- placement or markup snippets where useful;
- validation results;
- known limitations and any assets that require platform-side upload.

Keep generated showcases separate from production assets.