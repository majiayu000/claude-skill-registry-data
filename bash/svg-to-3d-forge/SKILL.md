---
name: svg-to-3d-forge
description: Create simple SVG assets locally and turn them into STL, OBJ, or GLB model files with an explicit Blender-based extrusion workflow.
---

# SVG To 3D Forge

Use this skill when the user wants a local Mac workflow for creating simple vector assets and turning them into basic 3D model files without pretending there is a magic one-click CAD pipeline behind it.

Default product shapes:
- a compact menu-bar utility that keeps SVG scaffold, extrusion settings, and export actions in one calm surface
- a deterministic local helper that can scaffold simple SVG templates and extrude them through Blender into STL, OBJ, or GLB

## Quick Start

1. Confirm whether the user wants a starter SVG, a 3D export from an existing SVG, or a real menu-bar utility surface.
2. Run `python skills/svg-to-3d-forge/scripts/svg_to_3d_forge.py doctor` to confirm Blender availability first.
3. Use `python skills/svg-to-3d-forge/scripts/svg_to_3d_forge.py scaffold --preset badge --text AC --output badge.svg` for a deterministic starter SVG.
4. Use `python skills/svg-to-3d-forge/scripts/svg_to_3d_forge.py extrude --input badge.svg --output badge.stl --format stl` to create a local mesh export.
5. Use `--depth`, `--bevel`, and `--size` to control extrusion thickness and export scale.
6. Use the SwiftUI starter in `prototype/` when the user wants a reusable Mac utility shell around the same pipeline.

## Accepted Inputs

- an existing SVG file with paths, shapes, or text already outlined the way the user wants
- a request for a simple scaffolded SVG asset such as a badge, coin, plaque, or keycap face
- desired output format: `stl`, `obj`, or `glb`
- extrusion depth, bevel, and approximate overall size
- whether the export is for quick visual mockups, slicer-ready prototypes, or app asset packaging

## Workflow

### Keep the boundary explicit

- Treat the SVG as the source of truth for the 2D asset.
- Use Blender locally for curve import, extrusion, mesh conversion, and export.
- If Blender is missing, stop with a clear dependency message instead of claiming the conversion worked.
- Keep the skill focused on simple vector-to-mesh work; do not present it as full mechanical CAD or a guarantee of print-ready topology.

### Prefer deterministic vector starts

- Use the scaffold command when the user needs a simple starter mark rather than a blank file.
- Keep scaffolded SVGs template-driven and editable.
- Encourage users to convert decorative text to outlines in their design tool if exact typography matters before extrusion.

### Validate the right thing

- Use STL for slicer or fabrication-oriented handoff.
- Use OBJ when another DCC tool needs a simple mesh file.
- Use GLB when the user wants a lightweight packaged 3D asset for viewers or web surfaces.
- If watertight geometry or tolerance matters, validate the result in Blender, a slicer, or CAD after export.

## Local Helper

Use `scripts/svg_to_3d_forge.py` for deterministic local workflows:

```bash
python skills/svg-to-3d-forge/scripts/svg_to_3d_forge.py doctor
python skills/svg-to-3d-forge/scripts/svg_to_3d_forge.py scaffold --preset badge --text AC --output badge.svg
python skills/svg-to-3d-forge/scripts/svg_to_3d_forge.py scaffold --preset keycap --text GO --subtitle layer --output keycap.svg
python skills/svg-to-3d-forge/scripts/svg_to_3d_forge.py extrude --input badge.svg --output badge.stl --format stl --depth 3.2 --bevel 0.25 --size 80
python skills/svg-to-3d-forge/scripts/svg_to_3d_forge.py extrude --input mark.svg --output mark.glb --format glb --depth 2.0 --size 100 --keep-driver
```

The helper can:
- check for Blender and report the exact binary path it found
- scaffold editable SVG files from a few practical presets
- generate a Blender driver script and run it locally to import the SVG, extrude curves, join the meshes, scale them, and export the chosen model file

## Guardrails

- Do not invent cloud conversion services, parametric CAD features, or automatic repair that the local toolchain does not provide.
- Keep the UI and workflow compact: source SVG, extrusion settings, output format, export.
- If the SVG is too complex, self-intersecting, or text-heavy, say so and recommend outline cleanup before extrusion.

## Prototype

- SwiftUI starter files live in `prototype/`.
- The prototype sketches a menu-bar shell with SVG intake, preset scaffolds, extrusion controls, and a one-click export flow.

## Example Prompts

- `Use $svg-to-3d-forge to scaffold a simple badge SVG and export it as an STL with a shallow bevel for 3D printing.`
- `Use $svg-to-3d-forge to turn this existing logo SVG into a GLB file with clean local Blender export steps.`
- `Use $svg-to-3d-forge to build a compact macOS menu-bar utility for SVG scaffold, extrusion preview settings, and STL or GLB export.`

## Resources

- `scripts/svg_to_3d_forge.py`: local doctor, scaffold, and Blender export helper
- `prototype/`: menu-bar-first SwiftUI starter for a compact SVG-to-3D utility shell
