---
name: build-minecraft-model-from-image
description: Turn a 2D picture of an object into a Minecraft-style 3D model, a few clean cuboids with pixel textures in the Blockbench look, never fine jagged voxels. Exports GLB, a viewer and renders. Use for "make this photo a Minecraft model", "block model from an image", "turn this object into blocks", "voxel from a picture", "từ ảnh làm khối 3D minecraft", "voxel từ ảnh", "biến ảnh đồ vật thành block", "làm model minecraft".
license: MIT
---

# Build a Minecraft-style model from a picture (Dựng model kiểu Minecraft từ ảnh đồ vật)

If `references/local.md` exists, read it first: it sets the folders and house rules for this machine.

The agent looks at the picture and writes the model by hand as code. There is no image-to-3D model, no heightmap and no extrusion.

## The look

A fine voxel grid looks jagged and ugly. The target is how Minecraft itself is modelled:

- A few big flat cuboids, about 20 to 110 boxes (a `round` tier takes 5 to 9). Each box or tier is a real part of the object.
- Every face carries a pixel texture at one texel per unit, so all pixels are the same size everywhere.
- Model height is 16 to 40 units. Detail goes in the paint, not in more boxes: eyes, labels, seams, screws, patterns.
- Round things are 2 to 5 stacked tiers of chamfered boxes (`round`, `disc`), never a staircase of tiny cubes.
- Angled parts are one rotated box (`beam`, `rotation=`).
- Palette from the picture, 3 to 5 close ramp steps per material. Low noise on smooth things, a little more on rough ones.

## Steps

`{{SKILL_DIR}}` is this skill's folder and `{{WORK_DIR}}` the folder where projects live. Scripts are in `{{SKILL_DIR}}/scripts`. Put each job in its own folder under `{{WORK_DIR}}`, with the picture as `source.jpg`. The scripts declare their Python dependencies inline, so `uv run` installs them. Blender 5.x does the renders. Set `BLENDER_PATH` if it is not on your PATH.

1. **Look at the whole picture at full size before any tool.** Name each real part, and what is only shadow, reflection or background. Blueprints blur this: on the test run a port's shadow was read as a "dark neck", and a collared shirt as a white bib.
2. **Read it:** `uv run --no-project {{SKILL_DIR}}/scripts/read_image.py source.jpg --blocks 24 --box x0,y0,x1,y1 --out read`. Add `--clear-background 18` on a plain background so holes open up (handles, slats). This writes `mask.png`, `blueprint.png` (block coordinates with a ruler), `palette.png` and `rows.json`. Pick `--blocks` so the thinnest part that must show gets 1 to 2 units.
3. **Write the part sheet** as the object script's docstring: what is visible, what is inferred for the unseen sides and why, what is left out. The camera view comes from measurement, see `references/method.md`, "Reading the view".
4. **Write the object script** with `SOURCE` and `build(kit)`. API and worked patterns: `references/method.md`. Worked examples of four shapes: `examples/`. Their source pictures are not included. Credits are in `README.md` at the repository root.
5. **Build:** `uv run --no-project {{SKILL_DIR}}/scripts/build_model.py object.py --out block --samples 48 --resolution 500`. This writes `model.glb`, `viewer.html`, `checks.json`, `overlay.png`, `compare.png` and `views/*.png` with transparent backgrounds. Add `--turntable 48` for `turntable.mp4`. `--device auto` is the default and goes to the CPU while the GPU is above 40% busy.
6. **Look at `compare.png` and fix what reads wrong**, at least one round. Go through `references/faults.md`. Check the back and side views as hard as the picture's view. That is where a lazy model shows.
7. **Blind read for anything going public:** ask a fresh subagent, or a person, who is not told the object to name it from the renders alone.

## Hard rules

- `build_model.py` exits 1 on floating parts or an extruded model. Fix the model. Do not loosen the check.
- Warnings are real: coplanar overlaps flicker in every viewer, and too many or too tiny boxes mean the model is sliding back into voxels.
- Silhouette overlap is a guide only. Thin frames and photos with perspective score low (a correct chair scores 0.45). Open `overlay.png` rather than chasing the number.
- Rendering uses the GPU. When another job holds it, keep to `--samples 24 --resolution 400`, or use `--no-render` and `viewer.html` until it frees up.
- Prefer pictures with a clear licence if the result is published; for an unclear one, name the risk once and ask the user. Leave third-party logos and brand text out of the model by default and say so; the user can ask for them.
- If the picture is not enough for the unseen sides of a real object, search reference views before inventing them.
- After editing the scripts, run `uv run --no-project {{SKILL_DIR}}/scripts/test_block_model.py` (no GPU needed).
