---
name: openscad
description: Create versioned OpenSCAD (.scad) files for 3D printing, render previews, and compare iterations. Use this when designing or iterating on 3D models.
allowed-tools:
  - Bash(*/render-scad.sh*)
  - Bash(*/version-scad.sh*)
  - Read
  - Write
  - Glob
---

# OpenSCAD Design Skill

Create versioned OpenSCAD files, render previews, and compare iterations for 3D printing designs.

`<skill-dir>` below is this skill's own folder (the base directory Claude Code shows when the skill loads). Companion skills are its siblings, e.g. `<skill-dir>/../preview-scad`.

## Workflow

### 1. Determine the Next Version Number

Before creating a new .scad file, find existing versions:

```bash
<skill-dir>/scripts/version-scad.sh <name>
```

This returns the next version number and filename. For example, if `piano_001.scad` exists, it returns `piano_002`.

### 2. Create the Versioned .scad File

Write the OpenSCAD code to the versioned filename (e.g., `piano_002.scad`).

### 3. Render the Preview

```bash
<skill-dir>/../preview-scad/scripts/render-scad.sh <name>_<version>.scad --output <name>_<version>.png
```

This creates a PNG with the matching version number (e.g., `piano_002.png`).

### 4. Compare with Previous Version

Read both the current and previous PNG images to visually compare:

- Current: `piano_002.png`
- Previous: `piano_001.png` (if exists)

Evaluate what changed and whether the new version better matches requirements.

### 5. Iterate

If the design needs improvement:
1. Analyze what's wrong
2. Create the next version (e.g., `piano_003.scad`)
3. Render and compare again

## File Naming Convention

```
<model-name>_<version>.scad  ->  <model-name>_<version>.png
```

Examples:
- `phone_stand_001.scad` -> `phone_stand_001.png`
- `phone_stand_002.scad` -> `phone_stand_002.png`
- `gear_001.scad` -> `gear_001.png`

Use underscores in model names, and always use 3-digit zero-padded version numbers.

## Example Session

User asks for a piano model:

1. Check for existing versions:
   ```bash
   <skill-dir>/scripts/version-scad.sh piano
   ```
   Output: `piano_001` (no existing files)

2. Write `piano_001.scad` with initial design

3. Render preview:
   ```bash
   <skill-dir>/../preview-scad/scripts/render-scad.sh piano_001.scad --output piano_001.png
   ```

4. Read `piano_001.png` to inspect the result

5. If improvements needed, create `piano_002.scad`, render to `piano_002.png`

6. Read both `piano_001.png` and `piano_002.png` to compare iterations

## Render Options

See `/preview-scad` for full rendering options:

- `--size <WxH>` - Image dimensions (default: `800x600`)
- `--camera <params>` - Camera, passed straight to OpenSCAD. 6 values = `eye_x,eye_y,eye_z,center_x,center_y,center_z` (easiest: e.g. `60,-90,80,0,0,0`). 7 values = `translate_x,y,z,rot_x,y,z,distance` (gimbal), **not** eye + center + distance
- `--colorscheme <name>` - Color scheme (default: `Cornfield`)
- `--render` - Full render mode (slower, more accurate)
- `--preview` - Preview mode (faster, default)

## Next Steps

Once the design looks correct in PNG previews:

1. **Export to STL**: Use `/export-stl` to convert the final version to STL format
2. The export includes geometry validation to catch printability issues

## Full Pipeline

```
/openscad → /preview-scad → /export-stl (with validation)
```

## Preview Pitfalls (F5 / OpenCSG)

OpenSCAD's preview (F5, and `render-scad.sh` without `--render`) draws CSG live with OpenCSG instead of computing the mesh. Some trees draw wrong even though the geometry and the exported STL are correct. Write models so they also *preview* correctly, because users inspect them in the GUI.

- **Don't `intersection()` a hollow part** (a shell, tray or box built with `difference()`) with a cutting region. The cavity shows as solid and the inner walls disappear. This is typical when splitting a part into pieces, slicing out a test coupon, or clipping to a half-space. Instead:
  - Cut with `difference()`: subtract the *complement* of the region you want to keep. For example, the left half is `difference() { part(); right_region(); }`, not `intersection() { part(); left_region(); }`.
  - Wrap each finished derived part in `render()`: `module left_half() render() difference() { ... }`. Then F5 shows the cached mesh, not live CSG. The first preview is slower, then it's cached. Use this for any piece built from a deep or nested CSG tree.
- **Coincident faces flicker (z-fighting).** Make cutting tools overshoot by `eps` or more on every face they cut through, e.g. `translate([0, 0, -1]) linear_extrude(h + 2)`.
- **Judge a preview problem by the mesh, not the picture.** Export the STL and check its volume and bounding box (e.g. manifold3d via `uv run`), or render the exported STL with `import()`. If the STL is right, only the preview tree needs fixing. If you restructure a part to fix its preview, confirm the new export matches the old one (the boolean XOR volume should be ≈ 0).
- `--render` (CGAL/manifold) PNGs can lose per-part `color()` and show their own artifacts on multi-part scenes. For colour views of an assembly, preview `import()`ed STLs instead.

## Tips

- Start simple and add complexity in iterations
- Use meaningful model names that describe the object
- Keep each version's changes focused on specific improvements
- Document what changed between versions in your response to the user
- Only export to STL once the preview looks correct
