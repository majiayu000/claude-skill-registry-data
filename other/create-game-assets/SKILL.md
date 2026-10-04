---
name: create-game-assets
description: Plan, generate, source, normalize, and validate cohesive visual game assets. Use for art direction, style bibles, sprites, tilesets, backgrounds, UI art, icons, textures, concept art, or 3D asset briefs.
---

# Create Game Assets

Turn a game's visual intent into a consistent, engine-ready asset set. Treat image generation as
one production tool inside a controlled pipeline, never as proof that an asset is shippable.

## Core workflow

1. **Inspect before inventing.** Find existing screenshots, concept art, sprites, models, fonts,
   import settings, camera framing, target resolution, and naming conventions. Preserve a coherent
   existing direction unless the user asks for a redesign.
2. **Lock the technical frame.** Record engine, 2D/3D, camera/view, native display size, asset
   dimensions, world scale, transparency, palette, filtering, animation frames, texture budget,
   and target platforms. Use `assets/art-direction-brief.md` as a copyable brief.
3. **Name the visual system.** Define shape language, silhouette priorities, value structure,
   palette roles, materials, lighting, detail density, edge treatment, and motion character. Use
   concrete visual properties; do not substitute a living artist's name for an art direction.
4. **Make an asset manifest.** Copy `assets/asset-manifest.json`, then list every required asset,
   state, variant, size, pivot, collision role, source, license, and approval status. Separate
   production assets from disposable greybox placeholders.
5. **Approve one visual target.** Create or select a representative hero asset or small style
   board before producing a full set. Judge it at actual game scale and against a gameplay
   background. If the user delegated the choice, pick the strongest viable direction and record
   the decision instead of blocking.
6. **Produce related assets as families.** Reuse the approved target as an edit/reference input.
   Keep palette, view, proportions, lighting, outline, and texture density invariant. Generate
   small coherent batches; avoid unrelated one-off prompts that drift.
7. **Normalize deterministically.** Crop, size, anchor, slice, name, compress, and check alpha with
   ordinary image/DCC tools. Never trust generated grids, transparency, seams, pivots, topology,
   or dimensions without inspection. Use the bundled scripts for raster QA and contact sheets.
8. **Import with engine-native settings.** Set filtering, mipmaps, pixels-per-unit/world scale,
   color space, compression, sprite slicing, texture types, materials, and collision deliberately.
   Read the relevant engine skill before editing engine files.
9. **Validate in context.** Inspect a contact sheet and the actual game at native resolution.
   Check silhouette, scale, animation stability, seams, legibility, palette, collision fit, memory,
   and compression artifacts. Iterate on the source asset, not only on runtime compensations.
10. **Record provenance.** Keep the source URL/tool, license or generation note, edit history, and
    restrictions beside the manifest. Preserve embedded provenance metadata when the pipeline can.

## Choose the production path

| Need | Default path |
|------|--------------|
| Existing asset needs a controlled change | Edit the original/reference; state what must remain unchanged |
| New 2D visual family | Approve seed → generate/source family → normalize → preview → import |
| True pixel art | Use generated work as a draft; enforce grid, palette, clusters, and frames with pixel tools |
| Tileable surface or tileset | Produce a small family; repair seams; test repeated 3×3 before approval |
| UI art or icons | Keep text and interaction code-native; prefer SVG/vector for simple geometric symbols |
| 3D model or material | Use concepts as reference; author/clean in a DCC; validate topology, UVs, scale, pivots, and LODs |
| No generation/edit tool is available | Build the brief and manifest; source licensed assets or keep explicit greybox placeholders |
| Audio asset | Route sound implementation and mixing to `audio-design`; still track source/license in the manifest |

## Image-generation handoff

When a capable image generation or editing tool is installed, use it for live visual creation. If
the workspace exposes an `imagegen` skill, read and follow it for the actual generation/edit call;
this skill owns the game-art brief, constraints, normalization, and acceptance gates.

Build prompts from these blocks:

```text
ROLE/PURPOSE: production asset for [gameplay role]
SUBJECT: [specific object/character and action]
VIEW: [orthographic/top-down/side/three-quarter], [camera and facing]
ART DIRECTION: [shape language], [palette roles], [materials], [edge treatment]
GAME-SCALE READ: [silhouette and focal details that must survive at WxH]
TECHNICAL OUTPUT: [dimensions/aspect], [transparent or scene background], [frame/slot count]
LOCKS: preserve [identity, proportions, palette, costume, lighting, line weight]
EXCLUDE: text, labels, mockup frames, scenery, duplicate objects, cropped edges, signatures
```

For edits, say both what changes and what stays fixed. Ask for transparent output through the
tool's native transparency option when available, then verify the alpha channel—prompt wording
alone does not guarantee transparency.

## Raster QA recipes

Inspect constraints and emit a machine-readable report:

```bash
python scripts/asset_report.py assets/player-idle.png \
  --expect-size 64x64 --require-alpha --max-colors 48 --json
```

Build a nearest-neighbor contact sheet over a checkerboard:

```bash
python scripts/build_preview_sheet.py output/player/*.png \
  --out output/player-preview.png --columns 4 --cell-size 192
```

Run script paths relative to this skill directory, or resolve the installed skill path first.
Both scripts require Python 3.10+ and Pillow. Install the only dependency with
`python -m pip install -r scripts/requirements.txt` when it is not already available.

## Quality gates

- **Cohesion:** related assets share palette roles, line/edge treatment, view, light direction,
  scale, and detail density.
- **Gameplay read:** silhouettes and state changes remain clear at native resolution, in motion,
  and over real backgrounds.
- **Technical fit:** exact size/frame count, usable alpha, stable anchors/pivots, correct color
  space/filtering, no clipped content, no accidental labels or baked mockup chrome.
- **Animation:** identity, volume, proportions, costume, facing, and baseline do not drift; timing
  and anticipation read in an in-engine preview.
- **Tiles/backgrounds:** required edges tile without seams; repetition is tolerable; parallax
  layers have intentional depth and no baked collision cues.
- **3D:** transforms, scale, pivot, normals, UVs, materials, topology, rig, collision proxies,
  LODs, and runtime format are checked rather than inferred from a render.
- **Rights:** every shipped file has recorded provenance and terms compatible with the project.

Do not call an asset production-ready from a prompt result alone. Approval requires the relevant
technical checks plus an in-engine or native-scale visual inspection.

## References

- For visual-system decisions and maintaining consistency, read
  `references/art-direction.md`.
- For sprites, animation strips, tiles, backgrounds, UI art, and engine import settings, read
  `references/raster-pipeline.md`.
- For concept-to-mesh, textures, glTF/GLB, LOD, collision, and runtime validation, read
  `references/three-d-pipeline.md`.
- For licenses, generated-media records, and provenance, read
  `references/provenance.md`.

## Related skills

- `game-ui-ux` for layout, navigation, readability, and accessible interaction.
- `game-feel`, `shader-programming`, and `audio-design` for presentation after the source art fits.
- Engine import/rendering skills such as `godot-tilemap`, `unity-tilemap-2d`,
  `pixijs-rendering`, and `threejs-gltf-loading`.
