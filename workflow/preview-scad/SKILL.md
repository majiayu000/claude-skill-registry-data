---
name: preview-scad
description: Render OpenSCAD (.scad) files to PNG images for visual verification. Use this after creating or modifying .scad files to see the 3D result and self-correct if needed.
allowed-tools:
  - Bash(*/render-scad.sh*)
  - Read
---

# OpenSCAD Preview Skill

Render OpenSCAD files to PNG images so you can visually verify your work.

`<skill-dir>` below is this skill's own folder (the base directory Claude Code shows when the skill loads).

## Usage

```
/preview-scad <file.scad> [options]
```

## Workflow

1. After creating or editing a `.scad` file, run this skill to render a preview
2. Read the generated PNG image to visually inspect the result
3. If the result doesn't look right, fix the code and re-render
4. Repeat until the design matches the requirements

## Running the Render Script

```bash
<skill-dir>/scripts/render-scad.sh <input.scad> [options]
```

### Options

- `--output <path>` - Custom output path (default: `<input>_preview.png`)
- `--size <WxH>` - Image dimensions (default: `800x600`)
- `--camera <params>` - Camera (default: auto-center). 6 values = eye x,y,z + center x,y,z (e.g. `60,-90,80,0,0,0`); 7 values = translate x,y,z + rotate x,y,z + distance (gimbal)
- Preview mode can draw `intersection()` of hollow parts as solid; see "Preview Pitfalls" in the `openscad` skill
- `--colorscheme <name>` - Color scheme (default: `Cornfield`)
- `--render` - Full render mode (slower, more accurate)
- `--preview` - Preview mode (faster, default)

## Example

After creating `phone_stand.scad`:

```bash
<skill-dir>/scripts/render-scad.sh phone_stand.scad
```

Then read the generated `phone_stand_preview.png` to see the result.

## Visual Feedback Loop

When working on OpenSCAD designs:

1. Write/edit the .scad file
2. Render preview with this skill
3. Read the PNG image to see what was created
4. Evaluate: Does it match what the user asked for?
   - If yes: You're done
   - If no: Identify what's wrong, fix the code, and repeat from step 2

This iterative process helps ensure the final design meets requirements.

## Next Steps

Once the preview looks correct:

1. **Export to STL**: Use `/export-stl` to convert to printable format with geometry validation

## Full Pipeline

```
/openscad → /preview-scad → /export-stl (with validation)
```
