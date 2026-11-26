---
vendored_from: https://github.com/danielwh2/sprite-stacking
name: sprite-stacking
description: Makes fake-3D rotatable pixel art with sprite stacking. Turns four orthographic views (top, side, front, back) into a visual-hull carved slice strip, checks it, and renders a crisp turntable for web Canvas, Godot, Unity or Phaser. Use when someone asks to "make a rotatable pixel art car", "sprite stacking", "fake 3D pixel art", "pixel art turntable", "stacked slices", "voxel-style 2D sprite", or wants a top-down vehicle, prop, tree or building that turns without drawing every angle.
triggers:
  - sprite-stacking
  - sprite
  - stacking

---

# Sprite stacking

An object is a horizontal strip of flat top-down slices, ground slice on the left, roof on the right. Draw them bottom to top, each rotated by the same angle, squashed vertically for camera pitch, and lifted 1 px per slice. One small sheet gives every angle in crisp pixels.

Never ship a stack you have not rendered and looked at. Paths below are relative to this skill's folder.

## 0. Pick the path

```
What do you have?
├── Slice strip PNG or MagicaVoxel layer export ──▶ Step 3 (Render)
├── 4-view sheet (top, side, front, back) ────────▶ Step 1 gate ─▶ Step 2 (Carve)
└── A prompt or an idea ──────────────────────────▶ Step 1 ─▶ Step 2 ─▶ Step 3
```

In an existing project, read the renderer first: engine, pixel scale, how sprites are drawn and sorted, which objects turn. Fit the stack into that renderer. Never add a second canvas or render pipeline.

## 1. Get a 4-view sheet

The sheet: one 1x4 row in the order TOP, SIDE, FRONT, BACK, on flat white, with clear gaps between views. TOP looks straight down, front pointing down. SIDE has the front pointing left. Same scale in all four.

Pick a tier:

- **Chunky retro:** 15-20 slices, about 25×48 px. Bold silhouettes, 3-4 px stripes, shown at 8-10x.
- **Detailed hi-bit:** 26-44 slices, 36×72 to 46×107 px. Holds vents, logos, spoked rims, glass reflections, raised spoilers.
- **Showcase / 1080p video:** 36-56 slices, 30×30 to 148×148 px, shown at 4-6x integer scale. Avoids chunky silhouette stepping and rotational wobble when tiny sprites are blown up to 7-9x on HD video. Architectural micro-details that read cleanly across 360° (shutters, flower boxes, balcony railings, roof moss, lily pads, lantern posts, cliff tendrils, waterfalls) elevate dioramas without breaking palette discipline.

Choose density from the **closest shot**, not the output file's dimensions. A 50 px hull enlarged to 450 px still has 50 px of design. If a feature cannot be drawn as a connected shape (e.g. a canopy with a frame), redraw the source with room for it or choose a closer composition; don't sharpen or blur an enlargement. Show scale through features of known size: windows → hatch → module → array.

Draw the part that *does* the action. A nozzle needs a lip and opening, a moving panel needs a fixed hinge, a wheel needs a contact patch. Mark the local attachment point and axis when authoring the strip; use that same pivot to place the effect or child part when the stack turns. Apply this to the receiving object too: if two pieces latch, design both mating surfaces. Spend detail there before adding bolts elsewhere.

Then take the first source that applies.

**a. You have an image generation tool.** Use this prompt. Swap the subject, keep the rest verbatim:

```
Chunky pixel art orthographic model sheet of [SUBJECT] with rich 3-tone hue-shifted pixel shading (deep cool-shifted shadows, saturated midtones, bright warm top highlights along ridges and edges), bold 3-4px stripes/accents, and crisp specular pixels on glass. Four views in a clean 1x4 horizontal row (or 2x2 grid) on a completely flat solid white or pale gray background:
1. TOP view looking straight down, front pointing DOWN.
2. SIDE view, front pointing LEFT.
3. FRONT view.
4. BACK view.
Strictly orthographic: zero perspective, zero tilt, zero 3/4 angle. Identical scale across all four views so length, width, and height match pixel for pixel. Bold 1px dark outline around each view, solid flat color clusters, crisp internal panel shading, zero anti-aliasing, zero soft edges, zero cast ground shadows, zero grid lines, zero text, generous empty space between views.
```

**b. The user has a sheet.** Use it.

**c. Neither.** Draw the four views yourself as pixel art in a short Python/PIL script at native resolution, one pixel per art pixel (numpy arrays or `ImageDraw`). Give each view a 1px dark outline, keep length, width and height identical across views, upscale 8x with `Image.NEAREST`, and paste them in one row on flat white with at least 40 px between views. Carve it with `--slices` set to the SIDE view's native height including its outline, so the slices land back on your pixels.

The slicer keeps a voxel only where every view covers it, so for (c):

- Round objects (pots, canopies, domes, wheels seen from above) need a pixel circle in the TOP view. A square TOP carves a box. If a round part is narrower than the widest part (a tower on a wide base, a balloon over its basket), carve with `--round` too, or it comes out square.
- Fins, leaves, wings and any irregular plan need their real outline in the TOP view, or they carve as blocks.
- The SIDE and FRONT silhouettes set the profile: a rectangle makes a cylinder, so round them for a ball.
- Wall detail (windows, doors, panel lines) goes in SIDE, FRONT and BACK. Roof detail goes in TOP.
- Anything that sticks out of a wall (flower box, porch, sign) carves a ledge along that whole wall. Paint small protrusions flat, and give a chimney a flat strip of ridge to stand on.
- Shade with a 3-4 tone hue-shifted ramp: cool deep shadow, saturated mid, warm highlight. No gradients, no anti-aliasing.

- Centre the object: the stack spins about the middle of its bounding box, so a base that reaches further on one side makes it orbit off-axis.

### Gate: look at the sheet before slicing

1. **Orientation:** TOP front points down. SIDE front points left (if right, pass `--side-nose right`).
2. **Proportions:** TOP length = SIDE length, TOP width = FRONT/BACK width, SIDE height = FRONT/BACK height.
3. **Hard edges:** flat fills, crisp outlines. Soft airbrushed edges or thin 1px internal lines smear once slices rotate. Regenerate or redraw rather than salvage.
4. **Holes:** overhangs that show daylight in the SIDE view (a raised rear wing) survive. Cavities hidden from all four silhouettes (truck beds, hollow arches) fill in. Fix those slices by hand after carving.
5. **Lessons:** run down the Lessons table at the end of this file.

## 2. Carve and inspect

`scripts/views_to_slices.py` needs Python 3 with Pillow and NumPy. It removes the background (transparent or flat), strips the 1px view outlines, quantizes to one shared palette, carves the slices, and writes a check sheet and a standalone viewer.

```bash
python3 scripts/views_to_slices.py views.png slices.png \
  --slices 36 --shade 0.2 --preview check.png --html viewer.html
```

| Flag | Default | When to change it |
| --- | --- | --- |
| `--slices N` | auto (36 if the SIDE view is taller than 64 px, else native) | 15-20 chunky, 32-48 hi-bit, native height for drawn sheets, `0` keeps the sheet's raw pixels |
| `--order` | `auto` | `auto` picks TOP and SIDE by matching proportions (TOP length = SIDE length, TOP width = FRONT width, SIDE height = FRONT height); reading order wins ties. `reading` forces TOP, SIDE, FRONT, BACK |
| `--round` | off | Towers, balloons, pots, bottles: clips each slice to the ellipse its SIDE and FRONT spans describe. Leave off for fins, wings and boxes |
| `--side-nose` | `left` | `right` if the SIDE view faces right |
| `--top-nose` | `auto` | Auto reads car cabins. Pass `down` for anything that is not a vehicle, and `up` or `down` if it flips a car |
| `--shade` | `0.2` | 0.12-0.15 for richly shaded views, 0.25 for flat ones, 0 for none |
| `--colours` | `24` | 32-48 for detailed liveries, `0` to keep every colour |
| `--bg-tol` | `28` | Raise a little if JPEG noise leaves a fringe |
| `--dark-thresh` | `70` | `0` to keep outlines on very dark silhouettes |
| `--normals` | *(none)* | Save a matching 3D normal-map slice strip PNG |
| `--emissive` | *(none)* | Save an auto-detected emissive mask strip PNG |

Open `check.png` and look at it right after carving: all four extracted views, four turntable angles and the exploded view. Do this before writing any integration code. `viewer.html` opens in a browser with Turntable, **Scene** (Living Diorama: Neon Street / Meadow Island with procedural stacked props + multi-PNG prop drops), Slice scan, Exploded, and **Play** modes (Drive through infinite Street/Meadow/Grid worlds, Wind, Shatter), live Time of Day (Day → Sunset → Night with auto-emissive glow and projected 3D shadows), **Weather** (Rain with wavy wet reflections & ripples, Snow with `normZ` snow-cap accumulation), and 16-direction PNG export.

## 3. Render: the loop and its numbers

Every renderer runs the same loop, bottom to top:

```js
// sheet: horizontal strip of `count` slices, each w × h, ground slice at z = 0
// pos: ground contact centre, rounded to whole pixels
for (let z = 0; z < count; z++) {
  // 1. rotate the slice around its centre (-floor(w/2), -floor(h/2)) by `turn`
  // 2. scale y by `squash` (camera pitch)
  // 3. lift by -round(z * spacing)
  // 4. translate to whole-pixel `pos`, draw with nearest filtering
}
```

Do not guess these:

- **`spacing = 1.0`** screen px at the art-pixel scale.
- **`squash = 0.75`** for an angled top-down camera. 1.0 looks straight down; below 0.6 roofs flatten to slivers. For a tilting camera, `squash = sin(elevation)`, `spacing = cos(elevation)`.
- **Symmetric rotation centres.** In software/pixel-buffer rasterizers, sample around `(w - 1) * 0.5, (h - 1) * 0.5` with `Math.round(...)` nearest sampling. Using `Math.floor(... + w / 2)` on even-sized slices shifts the centre by 0.5 art px and creates visible rotational wobble across 90°/180°/270° turns.
- **Smooth 60 fps placement.** Keep continuous motion (bobbing, floating, orbiting, parent-to-child projection) in floating-point screen pixels and snap only once at the final 1-screen-pixel blit (`Math.round(dx), Math.round(dy)`) with an integer display `scale`. Never quantize motion to art-pixel steps (`Math.round(...) * scale`) or round child projections independently — both cause harsh multi-pixel jumps and prop-to-ground jitter.
- **Validate strip counts at load time.** Assert `sheet.width % count === 0` (and expected slice dimensions) when slicing a strip so upgrading a strip's slice count never silently slices mid-frame.
- **Nearest-neighbour filtering.** `imageSmoothingEnabled = false` and `image-rendering: pixelated` on the web, Nearest/Point filter in engines.
- **Ground shadow:** for vehicles, the union footprint at z = 0, offset +2, +3 art px, drawn before slice 0. For tall props, project the stacked slices along the sun vector per layer, with Bayer 4×4 dithered edges, not a generic oval.
- **Outline the finished stack once, never per slice.** Per-slice outlines draw seams and speckle through the body. Render into a 1x art-pixel buffer, trace a 1px outline around its alpha, then scale up.
- **Heading:** the sheet's front points down (+y), so `turn = atan2(vy, vx) - PI / 2`. For anything that reverses, drive `turn` from a stored heading, not raw velocity.
- **Y-sort whole stacks by ground point.** Never interleave slices of two objects.
- **Bake static stacks** into plain sprites at load time. 200 trees × 30 slices is 6,000 draws a frame.
- **Animate entrances with slices, not opacity fades.** Fading a stack in mid-air looks flat; grow grounded props bottom-to-top via per-slice `lifts` (slice-bloom with a gentle spring settle and ground ring), and glide airborne/waterborne stacks (clouds, boats) in along their travel arc. Extend the `lifts` reveal frontier past `count` by the per-slice blend width (`mix(start, count + width, ...)`) so the top slices reach full `spacing` before switching `lifts` back to `null` — otherwise the upper slices snap in a single frame. Never blur crisp stacks with `defocus` cuts in video — use continuous camera moves instead.
- **Organic sway, 3D pitch tilt & body undulation via per-slice offsets.** For anchored flexible props (kelp, grass, banners), offset each slice horizontally by `sin(t * freq - z * wave + phase) * amp * (z / (count - 1))²` so `z = 0` stays pinned while tips sway smoothly. For leaping creatures (porpoising dolphins pitching nose-up on breach → level at apex → nose-down on re-entry) or rolling vessels, apply per-slice longitudinal/lateral tilt offsets `(xOffsets, yOffsets)` proportional to `(z - centerZ) * sin(pitchAngle)` along the body axis so pitch and roll read as true 3D tilt rather than a flat vertical lift.
- **Verify native nose axis & depth-attenuate submerged stacks.** Confirm whether each strip's nose faces `+x`, `+y`, or `-y` by visual inspection before binding `turn = atan2(vy, vx) ± PI / 2` so vessels and creatures travel nose-first. For stacks submerged underwater (seafloor props, deep manta, submerged dolphin phase), apply Beer-Lambert depth tinting (desaturating reds toward the water hue) and soften or omit the hard outer outline; drive floating stacks' heave, pitch, and roll from a damped spring-mass response to the shared wave field (not instantaneous wave height).
- **Multi-frame articulated 3D animation strips.** For living creatures (fluke-beating dolphins, wing-flapping mantas, tail-swishing fish, flapping/gliding birds), generate a compact set of full-3D slice strips (`f0..fN-1`, plus distinct pose frames like `leap` or `glide`) that share the exact same `(sliceWidth, sliceHeight, count)` and symmetric pivot `(w - 1) * 0.5, (h - 1) * 0.5` across every frame so switching frames never shifts the center. Give articulated strips extra Z-slice headroom (e.g., 18–20 slices instead of 12–16) so vertical wingbeats and tail flukes never clip the top or bottom slice, and select frames deterministically from the subject's physical motion phase.
- **Spherical bodies, world-space lighting & planetary rings.** A naive equal-radius sphere (`R_z = R_xy`) stretches into a vertical egg when rendered with pitch `squash` and vertical slice `spacing`: compute the exact Cauchy-Schwarz vertical half-height `R_z = R_xy · √(1 − squash²) / spacing` so the projected silhouette is a true circle (or controlled oblateness). For rotating planets and moons, store pure albedo bands/craters in the strip and apply a directional world-space solar terminator at render time so surface features spin while day/night stays locked to the star. For ringed bodies, split planar ring particles into back (`y_local < 0`, drawn before the planet stack) and front (`y_local >= 0`, drawn after) and eclipse particles inside the planet's cylindrical shadow cone.

Open `references/engines.md` when wiring into web Canvas, React, Godot, Unity or Phaser. `scripts/viewer.html` is the complete web reference: buffer, outline, orbit, scan, exploded, export.

### When motion leaves a trace

Pick a trace the material and medium actually support (spray leaving a paddle, dust at a tire, gas leaving a thruster). A still object may need none. Use the same physical event to drive the sprite and its effect: a spacecraft speeds up opposite the expelled gas, then coasts when the valve closes. A turn under torque changes angular velocity; it need not change the center's path.

Emit at the port's **pose at birth**, not its position this frame. Give each packet the port's world velocity (including rotation about the pivot) plus its exit velocity. After release, apply only forces from the medium; don't drag the old trail with the sprite or camera. Seed birth times/directions once, or bake the simulation so scrubbing backwards gives the same frame. Group the particles into a readable shape near the source; let them separate as they travel. More isolated bright dots rarely make a better effect.

## 4. Done when

- [ ] **Delivery-size read:** inspect the closest shot, widest shot and darkest lighting in the *finished composition*, both at native resolution and at the intended viewing width (e.g. 390 px for a phone feed). Without labels, can you identify the subject, its facing direction and the important action/contact? If not, separate silhouettes, change framing or group values before adding detail.
- [ ] **Clean materials in motion:** play through a slow move at delivery size. Keep hull panels, seams and reflections in coherent clusters; if isolated bright pixels crawl like grit, simplify the material or smooth the *normals*, not the final image. Reserve the strongest contrast for functional landmarks. For orbital scenes, a quiet sky and a thin lit limb can sell distance better than full-frame stars or dither. This is a readability test, not a required style or shot sequence.
- [ ] **Cause and response (if animated):** compare three feed-sized frames: before force/contact, during it, and just after release. Is the source attached at two different headings? Do the subject, the material it sheds and the object it touches respond in the right directions? Check one frame by seeking back to it; neither the attachment nor the trail should jump.
- [ ] **Straight down:** at `squash = 1`, `turn = 0`, the render is one slice wide and `sliceHeight + count - 1` px tall.
- [ ] **Pitch and 90°:** 0.75 is visibly shorter than 1.0; at 90° the width equals `sliceHeight`.
- [ ] **Spacing:** 0 draws flat (top slice only), 2.5 separates every layer cleanly.
- [ ] **Clean diagonals:** no horizontal stripes or dark speckle inside the body at 45°.
- [ ] **Heading:** driving a circle keeps the front on the path; reversing holds heading.
- [ ] **Slow turns:** if small sprites look choppy, raise the integer display scale first. Try RotSprite only if long straight edges still crawl, and compare by eye: it rounds off tiny sprites.
- [ ] **Full turn:** watch every angle, not four. A part that appears and disappears is a Lessons row.

## Lessons

When a stack comes out wrong, fix it, then fix the cause where it can't recur: change the slicer so the mistake can't happen, or make it warn with the fix in the message, and add a case to `tests/check.py` built from the real mistake that fails before the change. Only judgment calls code can't see become a rule. Add a row here; delete it once code makes the mistake impossible.

| Date | Mistake | Rule | Enforced by |
| --- | --- | --- | --- |
| 2026-11-20 | 1px posts, ropes and antennas blink in and out as the stack turns | Draw thin parts at least 2px wide | Slicer warning (`thin_runs`), check case 5 |
| 2026-11-20 | A round part narrower than its base (tower, balloon, pot) carves square | Carve with `--round`; it keeps gapped rows like posts square | `--round`, check case 4 |
| 2026-11-20 | Auto `--top-nose` flips anything that is not a vehicle | Pass `--top-nose down` | Rule |
| 2026-11-20 | Something sticking out of a wall carves a ledge along the whole wall | Paint small protrusions flat; give a chimney a flat strip of ridge | Rule |
| 2026-11-20 | Background fully enclosed inside a view (between ropes, fins, legs) carves solid | Every gap must reach the outside of its view | Rule |
| 2026-11-20 | A base that reaches further on one side makes the stack orbit off-axis | Centre the object in its views | Rule |
| 2026-11-20 | Asymmetric `Math.floor(... + w / 2)` rotation sampling causes 0.5-art-px wobble across 90° boundaries | Use symmetric `(w - 1) * 0.5` centres with `Math.round(...)` nearest sampling | Rule |
| 2026-11-20 | Quantizing bobbing, orbiting, or child-prop projection to art-pixel steps (`Math.round(...) * scale`) creates jarring multi-pixel jumps at 60 fps | Keep motion and projection continuous in screen pixels; snap once at the final 1-screen-px blit with integer `scale` | Rule |
| 2026-11-20 | Tiny 12–24px props scaled 7–9× on 1080p video look overly chunky and exaggerate nearest-neighbor rotation stepping | Build denser strips (36–56 slices, 30–148px) and render at 4–6× integer scale for showcase video | Rule |
| 2026-11-20 | Updating a strip's slice count without updating the loader's count silently slices mid-frame | Validate `sheet.width % count === 0` and slice width at load time | Rule |
| 2026-11-20 | Fading stacks in mid-air or using `defocus` cuts blurs/flattens pixel-art dioramas | Bloom grounded props bottom-to-top via per-slice `lifts`, glide orbiters in along their arc, and use continuous camera moves | Rule |
| 2026-11-20 | Stopping a `lifts` reveal frontier at `count` leaves upper slices compressed when switching back to `null`, causing a single-frame top-slice jump | Extend the reveal frontier past `count` by the per-slice blend width (`count + width`) so top slices reach `1.0` before returning `null` | Rule |
| 2026-11-21 | Assuming every strip faces `+y` makes custom-carved ships or fish travel sideways/backward when driven by `atan2(vy, vx) - PI / 2` | Verify each strip's native nose axis (`+x`, `+y`, `-y`) before setting the `turn` offset | Rule |
| 2026-11-21 | Drawing deep underwater stacks with full surface saturation and hard ink outlines breaks depth hierarchy | Shift submerged stacks toward the water hue (Beer-Lambert red loss) and soften/drop hard outlines; couple floating stacks to the surface wave field | Rule |
| 2026-11-21 | Animating living creatures with a single rigid pose (or clipping flapping wings/flukes at slice 0 / `count - 1`) makes wildlife look stiff or truncated | Generate multi-frame strips (`f0..fN-1` + pose frames) with identical `(W, H, count)`, shared symmetric pivots, extra Z-slice headroom, and physics-synced frame selection | Rule |
| 2026-11-21 | Equal-radius spheres (`R_z = R_xy`) stretch vertically into eggs under pitch `squash` and slice `spacing` | Compensate sphere slice half-height with Cauchy-Schwarz projection `R_z = R_xy · √(1 − squash²) / spacing` | Rule |
| 2026-11-21 | Baking directional sun shading into rotating planet or moon strips makes the day/night shadow spin with the surface | Store pure albedo in spherical strips and evaluate world-space directional terminator shading per slice at render time | Rule |
| 2026-11-21 | Drawing planetary rings in a single pass causes rings to float completely in front of or behind a stacked planet | Split planar ring particles into back (`y_local < 0`) before the stack and front (`y_local >= 0`) after, and eclipse particles in the cylindrical shadow cone | Rule |
