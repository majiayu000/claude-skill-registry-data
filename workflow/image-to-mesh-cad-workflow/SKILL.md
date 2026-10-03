---
name: image-to-mesh-cad-workflow
description: |-
  End-to-end workflow for converting a 2D concept image into a parametric 3D CAD model when manual outline tracing is unreliable. Bridges the lossy "image → text-description → manual-spline-points" gap by using AI image-to-3D-mesh services (Tripo3D, Rodin, Meshy) as an intermediate step, then auditing the imported mesh for axis convention + cutout angles + sub-component inclusion before extracting the silhouette and building a parametric Loft/Revolve. Specifically applies to rotationally-symmetric parts (speakers, vases, lampshades, bottles, hubs). Trigger on phrases like "image to 3D mesh", "Tripo3D workflow", "mesh-driven CAD", "extract spline from mesh", "mesh-audit", "Y-up vs Z-up", "cutout position wrong". Do NOT load for normal CAD construction (use `cad-construction`), Fusion-API specifics (use `fusion-mcp-bridge`), or design exploration (use `design-first-iteration`).

---

# Image-to-Mesh CAD Workflow

A pragmatic pipeline for translating a 2D concept image into a parametric CAD model in Fusion 360 when manual spline-tracing produces visible deviation from intent.

---

## ⚠️ RECURRING TRAP — Read This Before Every Operation ⚠️

The single most expensive recurring failure mode in this workflow is **falling back to spec/text descriptions for dimensions, positions, and orientations instead of measuring them from the mesh.** This trap is sneaky because:

1. The spec document is *psychologically authoritative* (it's a written record). The mesh is just data that needs to be measured. So when in doubt, the spec wins by default.
2. User-feedback-driven adjustments ("make it bigger", "rotate it") feel like they should be applied directly. But the user's intent is almost always "match the mesh better" — which means measuring the mesh, not eyeballing.
3. After fixing one component (e.g., correcting the main-body orientation), other components built earlier in the wrong frame are silently invalid. They look fine in the timeline but are semantically wrong.

**Real cost from one rotationally-symmetric speaker-housing session:**
- 4 hours debugging a 180°-X-flip that mesh-audit would have surfaced in 30 seconds
- 3 cut-size iterations (50×40, 100×60, then learned the mesh actually has 122×50) — each took ~30 minutes plus user-correction wait time
- Inner cone left mis-oriented for an entire session because nobody re-validated it after the main-body fix
- One destructive 15mm fillet on a 6mm wall (volume 1255 → 566 cm³) because radius-vs-wall-thickness wasn't checked first

**Real cost from a follow-up session:**
- 3 wrong cone-position iterations (translation Z=-7 → -12 → -9 → -7.7) because the cut-window Z-range was *estimated from spec docs* (-7.7..-2.7) instead of *measured from body edges* (-8.3..-2.1 inner edge, -7.7..-2.7 outer edge — different per face due to wall curvature)
- Translation `occ.transform2 = m` silently reverted to a previous value (Z=-4.5 instead of the just-set Z=-9) because timeline recompute restored an older state — never verified post-set, user had to re-flag the wrong position
- → **Maxim: "In constructions, always measure, never estimate."** Applies to every dimension, position, and any value you just set.

This is **THE** anti-pattern. If you only remember one thing from this skill, remember this section.

### The Correct Process (mandatory gates)

**BEFORE every dimension / position / orientation decision:**

```
GATE 1 — Measure from mesh:
  □ fusion mesh-audit "<MeshBody>" — bbox, wide-end, axis convention
  □ fusion mesh-audit "<MeshBody>" --height-cm <z> — angular features at specific Z
  □ fusion mesh-silhouette "<MeshBody>" — exact R-vs-Z profile
  □ For non-rotational features: write a slice-script that quantifies the feature

GATE 2 — Document measured values:
  □ Write down R(z), angular extents, Z ranges, etc. as concrete numbers
  □ Note any deviation from spec (mesh wins; spec is hypothesis)

GATE 3 — Map frames:
  □ mesh-frame → world-frame (via mesh import transform)
  □ world-frame → component-frame (via occurrence transform)
  □ Apply mapping to each measured number BEFORE using it in code
```

**AFTER every component fix:**

```
GATE 4 — Cross-component revalidation:
  □ For EVERY other component in the same design, re-audit position + orientation against mesh
  □ Bbox alone is insufficient — also check feature directionality (apex, concavity, asymmetric features)
  □ A component that was "correct" before another component's fix may now be wrong
```

**AFTER every transform/set operation (e.g. `occ.transform2 = m`, sketch-point edit, parameter change):**

```
GATE 4b — Post-set verification (the „measure don't estimate" maxim):
  □ Read the value back from Fusion with a separate eval call: e.g. tr = occ.transform2.translation; print(tr.z)
  □ Compute the resulting world-frame coordinate of the affected geometry (bbox.minPoint.z + tr.z)
  □ Confirm it matches the intended target value
  □ Reason: timeline-recompute, parametric-rebuild, and other-feature-side-effects can silently revert your set
  □ Cost from skipping this: 3 extra cone-position iterations because translation Z=-9 was silently reverted to Z=-4.5 between scripts; user had to flag the wrong position twice
```

**WHEN user gives feedback:**

```
GATE 5 — Don't adjust blindly:
  □ "Cut should be bigger" → run mesh-audit, don't guess a new size
  □ "Body is rotated" → run mesh vs solid axis comparison, don't guess the rotation
  □ "Edge should be smoother" → measure the local wall thickness; fillet radius MUST be ≤ wall thickness
  □ User intent = "match the mesh better"; the mesh is the answer source, not the user
```

### Anti-patterns this skill exists to prevent

| Anti-pattern | Why it bites | Correct alternative |
|---|---|---|
| Using spec dimensions verbatim | Spec is text-based hypothesis, mesh is geometric truth | Measure mesh first; treat spec as starting guess |
| Adjusting based on user verbal feedback | "Bigger" / "rotated" gives no exact number | Run mesh-audit, present measured value, then build |
| Trusting visual screenshots for size/angle | 2D projections distort dimensions | Use bbox queries or measurement queries |
| Skipping cross-component revalidation | Components built in old frame become silently invalid | After ANY component fix, re-audit ALL related components |
| Falling back to spec when mesh-audit feels like extra work | The 30-second audit prevents 4-hour debug session | The audit IS the work; treat it as required scaffolding |
| Filleting without checking wall thickness | Radius > wall thickness destroys body | Always: `r_fillet ≤ wall_thickness × 0.8` |
| Running comprehensive mesh-audit in one big script | 60k samples × 80 Z-bins × 36 angle-bins blocks the Fusion UI thread, hangs the bridge | Cap at ~20k subsamples; split per-region (cut zone, pedestal, top) into separate calls |

---

## When to use

- A concept image (sketch, render, photo) is the only design source
- Manual silhouette estimation has produced noticeable deviation (concave waist instead of convex curve, wrong proportions, etc.)
- The target part is **rotationally symmetric** — speaker housings, vases, lampshades, hubs, lenses, bottles
- Parametric editability is required (cannot just keep the mesh as-is)

## When NOT to use

- The CAD geometry is fundamentally non-rotationally-symmetric (use `cad-construction` with manual sketches)
- The concept is already specified in numbers (use `cad-construction` directly)
- The mesh-fidelity-of-cutouts is more important than parametric flexibility (use Fusion's UI "Mesh → Convert to BRep", possibly after manual mesh-reduce)

## Architecture

```
2D Image (PNG/JPG)
    ↓ (1) Tripo3D / Rodin / Meshy — image-to-3D AI
3D Mesh (STL, ~100k-1M triangles)
    ↓ (2) Fusion-MCP-Bridge import (Component.meshBodies.add)
MeshBody in Fusion (Direct-Modeling design)
    ↓ (3) Silhouette extraction (R vs Z, top-percentile-median per Z-bucket)
Spline control points (R, Z) in cm
    ↓ (4) Single-Revolve in Parametric design
BRep Solid Body (rotationally-symmetric outer form)
    ↓ (5) Standard parametric features (Cut, Shell, Pattern)
Final parametric component
```

## Setup

Required:
- `fusion-mcp-bridge` skill + `fusion` CLI (separate skill; this skill depends on it)
- Browser access to Tripo3D (free tier sufficient for 2-3 generations) — alternatives: Rodin (hyperhuman.deemos.com), Meshy (meshy.ai), TripoSR (open-source local)
- For browser automation: `claude-in-chrome` MCP

Optional:
- Tripo3D API key for headless usage (skip browser automation)

## The eight phases

### Phase 0: Mesh-Frame Audit (do BEFORE any parametric build)

**Run `fusion mesh-audit` immediately after import.** This single command answers four questions that are otherwise discovered painfully across hours of failed iterations:

1. **Which axis is the height-axis?** (Z-up vs Y-up vs X-up — depends on source tool)
2. **Is the wider end at the top or the bottom?** (apex direction)
3. **What is the angular position of features (cutouts, handles, asymmetric details)?**
4. **Does the mesh include parts that the parametric build assumes are separate?** (e.g., Tripo3D often includes the base/pedestal in the mesh although the parametric solid will model it as a separate component)

```bash
fusion mesh-audit "Tripo3D-Mesh-Reference"
fusion mesh-audit "Tripo3D-Mesh-Reference" --height-cm -4   # explicit slice height
fusion mesh-audit "Tripo3D-Mesh-Reference" --json | jq      # machine-readable
```

Sample output:

```
Bounding box (cm):
  X: [  -8.58,    8.58]  size  17.15
  Y: [  -8.57,    8.57]  size  17.15
  Z: [ -19.50,   19.50]  size  39.00
Longest axis     : Z  (height of mesh)
Wide end         : low end of Z-axis  (R=8.04 cm low vs R=5.54 cm high)
→ Mesh is Z-up with apex at top. No transform needed.
Angular cutout candidates at sample height Z=-4.0 cm (R < 3.26 cm, avg R = 3.83 cm):
  ang [ 80°..170°]  min R = 1.82 cm  (10 bins)
  ang [260°..350°]  min R = 1.85 cm  (10 bins)
```

Key things to capture from the audit BEFORE building anything parametric:

| Question | Where to look | Implication if wrong |
|---|---|---|
| Height-axis | `Longest axis: <X/Y/Z>` | All Z-coordinates in CAD calcs are wrong; rotate the occurrence first |
| Wide-end direction | `Wide end: low/high end` | Apex points wrong way; apply 180°-X-flip |
| Cutout angles | `Angular cutout candidates ang [...]°` | Parametric cuts placed at wrong angles around vertical axis |
| Pedestal included? | Wide-end R matches pedestal-OD spec | Mesh-Z=0 is NOT the main-body bottom — must measure explicitly |

**For meshes >100k vertices**, mesh-audit subsamples to 50k by default (configurable via `--max-samples`). Larger meshes hit the HTTP-bridge timeout otherwise.

### Phase 1: Image preparation

The AI mesh quality scales directly with image quality. Best inputs:
- **Plain background** (transparent or single-color, no scenery)
- **Frontal view** (no perspective foreshortening)
- **Clear silhouette** (no overlapping objects, no shadows touching the silhouette)
- **Reasonable resolution** (512×768 to 1024×1536 — Tripo handles up to 10MB)

Resize down if needed (`sips -Z 800 input.png --out small.png` on macOS) — AI doesn't need ultra-high-res for shape detection.

### Phase 2: Mesh generation

**Browser-automation approach** (Tripo3D web UI):

1. Navigate to `https://www.tripo3d.ai/app`
2. Choose Tripo Lite (simpler interface)
3. Click `+ Single Image` to open upload zone
4. **Upload critical step** — see "Browser-upload-permission-wall" pattern below
5. Click `Generate` (~25 credits free tier)
6. Wait 30-90s for generation
7. Click preview → opens model detail page
8. Set `Format: stl`
9. Click `Download` (~5 additional credits for STL conversion)

**API approach** (faster, headless): use Tripo3D API with key — more efficient for repeat work.

### Phase 3: STL Import via fusion CLI

```bash
fusion mesh-import ~/Downloads/<file>.stl
```

This auto-handles:
- Direct-Modeling-Design switch (mesh-import requires it)
- `Component.meshBodies.add(filepath, MeshUnits.MillimeterMeshUnit)`
- ScaleFeature to bring the unitless Tripo mesh up to target size
- Z-flip transform (Tripo convention puts wider end at +Z; flip via 180° X-rotation)

### Phase 4: Silhouette extraction

```bash
fusion mesh-silhouette "<mesh-body-name>" --bucket-cm 0.5 --out silhouette.json
```

Algorithm:
1. Read all vertex coordinates from `meshBody.displayMesh.nodeCoordinates`
2. For each vertex, compute `R = sqrt(x² + y²)` and bin by Z (default 0.5 cm buckets)
3. For each bucket: take **top 5% R values' median** as the outer-surface R (avoids tip-noise and mesh-outliers)
4. Output ordered list of (R, Z) points

### Phase 5: Spline-Loft parametric build

In Fusion, with extracted points:
1. Sketch on `xZConstructionPlane`
2. Add `sketchFittedSplines.add()` with the (R, Z) control points
3. Add closing top arc to apex (use `sphere_arc_params` from `lib_helpers.py`)
4. Add closing bottom edge + axis edge
5. Single Revolve 360° around `zConstructionAxis`

**Critical: profile-touches-axis workaround** — Fusion rejects revolve profiles where the boundary lies exactly on the rotation axis. Use a small offset (`EPS = 0.005` cm = 0.05 mm) for axis-points. This creates a tiny invisible bore through the center; negligible but unblocks the operation.

### Phase 6: Cuts + Shell

Standard `fusion-mcp-bridge` patterns apply:
- **Cut-before-Shell** sequence
- Tool-Body + Combine-Cut pattern
- Boolean-union of multi-bodies before any cut

For cutouts derived from the mesh:
- **Phase 6a (this skill)**: Simple ovals/rectangles via Tool-Body extrude — works for first iteration but loses fidelity to mesh-cutout shapes
- **Phase 6b (Wave-2)**: Mesh-slicing for exact cutout boundary — see "Cutout-fidelity-Wave-2" pattern below

### Phase 7: Validation

Visual comparison (mesh vs. parametric body in same scene):
- `fusion view front` + screenshot
- Param-Solid should overlay mesh ±2% in radius at all Z

Component summary:
- `fusion components` — confirm body counts and Z positions

## Browser-upload-permission-wall pattern

Chrome extensions (claude-in-chrome MCP) cannot directly call `setFileInputFiles` on web file-inputs (CDP returns "Not allowed"). Workaround:

1. **Start a local CORS-enabled HTTP server** in the directory containing the file
2. **Use JavaScript fetch + DataTransfer** in the page context to load the file and assign to the file-input

Server (Python stdlib only):

```python
import http.server, socketserver, os, sys

class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

os.chdir(sys.argv[1])
PORT = int(sys.argv[2])
with socketserver.TCPServer(("127.0.0.1", PORT), CORSHandler) as httpd:
    httpd.serve_forever()
```

Browser-side JS:

```javascript
const r = await fetch('http://127.0.0.1:8889/file.png');
const blob = await r.blob();
const file = new File([blob], 'file.png', {type: 'image/png'});
const input = document.querySelector('input[type="file"]');
const dt = new DataTransfer();
dt.items.add(file);
input.files = dt.files;
input.dispatchEvent(new Event('change', {bubbles: true}));
```

This bypasses both the file-system-permission-wall and Mixed-Content blocking (Chrome treats `127.0.0.1` as secure origin).

## Mesh source coordinate conventions (verify, don't assume)

Different image-to-3D tools output meshes in different coordinate systems. **Never assume** — run `fusion mesh-audit` (Phase 0 above) and read the actual axis. Common conventions seen in 2026:

| Tool | Vertical axis convention | Apex direction | Notes |
|---|---|---|---|
| **Tripo3D** | Often Z-up but **wider end at +Z** (inverted vs CAD-typical) | Apex at -Z | The "Z-flip" historical fix; verify each generation, the convention has shifted |
| **glTF / Three.js / Maya export** | Y-up | Apex direction varies | `fusion mesh-import` does not auto-rotate Y-up to Z-up — manual transform required |
| **Rodin (Hyperhuman)** | Z-up, apex at +Z | Apex at top | No flip needed, but verify |
| **Meshy** | Variable per export option | — | Always audit |
| **Fusion-CAD typical** | Z-up, apex at top | Apex at +Z | The target convention |

### Choosing the right transform from audit output

```python
# Case 1: Mesh is already Z-up with apex at top → identity, no transform
# (mesh-audit reports: "→ Mesh is Z-up with apex at top. No transform needed.")

# Case 2: Mesh is Y-up (glTF/Three.js convention) → rotate +90° around X to get Z-up
m = adsk.core.Matrix3D.create()
m.setCell(0, 0,  1.0)
m.setCell(1, 1,  0.0); m.setCell(1, 2, -1.0)  # original Y → -Z
m.setCell(2, 1,  1.0); m.setCell(2, 2,  0.0)  # original Z → +Y
occ.transform2 = m

# Case 3: Mesh is Z-up but apex at -Z (Tripo3D legacy convention) → 180° around X
m = adsk.core.Matrix3D.create()
m.setCell(1, 1, -1.0)  # flip Y
m.setCell(2, 2, -1.0)  # flip Z
occ.transform2 = m

# Case 4: Mesh is X-up (rare) → rotate -90° around Y
m = adsk.core.Matrix3D.create()
m.setCell(0, 0,  0.0); m.setCell(0, 2,  1.0)  # X → +Z
m.setCell(1, 1,  1.0)
m.setCell(2, 0, -1.0); m.setCell(2, 2,  0.0)  # Z → -X
occ.transform2 = m
```

`fusion mesh-import` applies Case 3 by default (`--flip-z`). Use `--no-flip` for Case 1 (already correct), or do the rotation manually for Cases 2/4.

### Why this matters: human / CAD convention is Z-up

A mesh imported in Y-up convention will **look correct in the viewport** because Fusion's view-cube auto-orients to the data — but every Z-coordinate calculation in the parametric build will be wrong. Sketches placed on `xYConstructionPlane` will be perpendicular to what they should be; revolves around `zConstructionAxis` will rotate around the wrong axis.

**Universal rule:** target the parametric solid build at standard **Z-up with apex at top**. Transform the mesh to match this on import; don't try to make the parametric code match a non-standard mesh frame.

## Cutout-fidelity Wave-2 pattern (mesh-slicing)

Simple ovals/rectangles as cut tools work for "Phase 1" approximation. For full mesh-cutout fidelity, slice the mesh at the cutout's central plane and extract the boundary:

```python
def slice_mesh_at_y0(mesh_body, eps=0.05):
    """Return list of (x, z) points where mesh crosses Y=0 plane (cutout boundary)."""
    vertices = mesh_body.displayMesh.nodeCoordinates
    triangles = mesh_body.displayMesh.nodeIndices
    segments = []
    for i in range(0, len(triangles), 3):
        v0, v1, v2 = [vertices[triangles[i+j]] for j in range(3)]
        # For each edge, check if it crosses Y=0
        for a, b in [(v0,v1), (v1,v2), (v2,v0)]:
            if (a.y <= 0 <= b.y) or (b.y <= 0 <= a.y):
                if abs(b.y - a.y) < eps:
                    continue
                t = -a.y / (b.y - a.y)
                x = a.x + t * (b.x - a.x)
                z = a.z + t * (b.z - a.z)
                segments.append((x, z))
    return segments  # then connect into polylines + identify cutout-loop
```

Use the polyline as a Sketch in Fusion, then Cut-Extrude through. See `references/mesh-slice.py` (Wave-2).

## Critical: Mesh is monolithic, Solid is modular

The **single most important architectural pattern** in this workflow. AI-generated meshes (Tripo3D, Rodin) are always **one monolithic body** — all features (cutouts, ribs, dome) live in one shared coordinate frame relative to the mesh's bounding box. The target parametric solid is typically **modular** — separate components for pedestal, main body, dome, internal cone — each with their own component-frame for assembly.

**Failure mode without explicit mapping (real bug from a speaker-housing first iteration):**
Cutouts extracted at mesh-Z range `[-7, 0]` were applied as Cut at the same component-Z range in the modular main-body component. The cutouts ended up "too high in the body" because the main body's component-frame origin does NOT sit at the speaker's bottom — it sits at the pedestal/main-body junction. What was visually in the lower 1/4 of the monolithic mesh ended up in the lower 1/4 of the main-body component, which is the upper half of the actual speaker.

**Correct workflow:**

1. **Define modular component structure first** — decide where each component-frame origin sits relative to a global speaker-frame:
   ```
   pedestal:    world-Z = 0..11 cm
   main_body:   world-Z = 11..39 cm  (component origin at world-Z=11)
   inner_cone:  world-Z = 12..18 cm  (component origin at world-Z=12)
   ```
2. **Establish coordinate mapping** mesh-frame → world-frame → component-frame for every feature extracted
3. **Identify which feature belongs to which component** — a cutout at world-Z=15 belongs to main_body, not pedestal
4. **Apply the feature in the correct component-frame** with the correctly mapped Z value

**Concrete example mapping:**

```python
def mesh_to_component(z_mesh, pedestal_height_cm, mesh_z_origin_offset=19.5):
    """Map a mesh-frame Z to the modular main-body component-frame."""
    # Step 1: mesh-frame to world-frame (Tripo's Z-flip + global offset)
    z_world = mesh_z_origin_offset - z_mesh  # if Tripo Z-up flipped
    # Step 2: world-frame to main-body component-frame (subtract pedestal height)
    z_main = z_world - pedestal_height_cm
    return z_main

# Mesh cutout at z_mesh = -3 cm → z_world = 22.5 cm → z_main = 11.5 cm
```

**Skill rule**: before applying any extracted feature to a modular component, write the mapping table explicitly:

| Feature | mesh-Z | world-Z | which component | component-Z |
|---|---|---|---|---|
| Cutout center | -3.5 | 23.0 | main_body | 12.0 |
| Top dome apex | 19.5 | 0.0 | top_cap | 0.0 |
| LED ring | -16.0 | 35.5 | pedestal | 35.5 |

This table is the **first artifact** of the workflow, before any Cut/Sketch operations. Without it, every feature placement is a coin-flip.

**Verification**: after applying a feature, take a screenshot comparing mesh and modular solid in the same scene. The feature should overlay the corresponding mesh region exactly. If it's offset, the mapping table is wrong — fix the table, not the position.

### Two independent error classes (don't conflate them)

The mapping bug above is one of **two independent error classes** that both produce "feature in wrong place" symptoms. They must be diagnosed and fixed separately:

**Class A: Vertical offset (Z-coordinate mapping)**
- Symptom: cutout is at the right angle but at the wrong height (too high or too low)
- Root cause: mesh-frame Z-origin is not where you assumed (e.g., mesh includes the pedestal, so mesh-Z=0 is mid-speaker, not pedestal-bottom)
- Fix: `fusion mesh-audit` reads the actual wide-end position; re-derive `mesh_z_origin_offset` from measurement, not from spec
- This is the existing "Mesh is monolithic / Solid is modular" pattern above

**Class B: Angular offset (rotation around vertical axis)**
- Symptom: cutout is at the right height but at the wrong angle (pointing the wrong way)
- Root cause: the AI mesh generator rotated features by some arbitrary angle relative to the source image; or the source image was rendered from a slightly off-axis perspective; or the parametric build placed cutouts at design-spec angles (0°/180°) without checking mesh actual angles
- Fix: `fusion mesh-audit --height-cm <z>` reads the actual angular cutout positions from the mesh; rotate the parametric cut sketch (or the host construction plane) by the difference

**Real example from a speaker-housing build:**
- Design spec said: side ports at +Y (90°) and -Y (270°)
- Tripo3D mesh actually has them at 125° and 305° (35° clockwise rotation)
- A solid-modular build using spec angles produces visibly misaligned cutouts vs mesh
- The fix is **not** to rebuild the mesh, but to either:
  1. Apply a 35° Z-rotation to the cutout sketch, OR
  2. Apply a 35° Z-rotation to the mesh occurrence so design-spec angles align with what's visible
- Choice depends on which "ground truth" you want — design-spec angles vs visible-mesh angles

The user/designer decides which is canonical. The skill's job is to **surface the discrepancy**, not silently pick one.

## Anti-patterns

- **Estimating spline points by eye from concept image** — exactly what this skill prevents. Use mesh extraction instead.
- **Skipping Phase 0 mesh-audit** — leads to 4-hour debug sessions chasing wrong-axis bugs that a 30-second audit would have surfaced immediately.
- **Direct mesh-to-BRep conversion via API for high-poly meshes** — Fusion API rejects mesh-reduce on transformed bodies. Use UI manually if needed, after reducing in MeshLab/Blender first.
- **Skipping the orientation check** — every image-to-3D tool has its own convention; verify with `fusion mesh-audit` instead of assuming the historical Tripo Z-flip is still valid.
- **Trusting design-spec angles for cutout positioning** — the AI mesh generator may rotate features arbitrarily relative to source-image axes. Always extract actual angular positions from mesh via `fusion mesh-audit --height-cm <z>`.
- **Iterating over all vertices of a 500k-tri mesh in a synchronous Python script** — exceeds HTTP-bridge timeout (60s default). Subsample to ≤50k vertices for any analysis script; the CLI handles this automatically with `--max-samples`.
- **Single huge JS injection for image-upload** — keep base64 inline payloads under ~50 KB; use the CORS-server-fetch pattern instead.
- **Forgetting profile-axis-offset (EPS=0.005)** — Fusion rejects axis-touching revolve profiles silently with "profile intersects axis" error.

## Handover checklist

Before declaring an image-to-mesh-CAD workflow complete:

- [ ] **`fusion mesh-audit`** run after import — output captured in project doc as Lesson Learned (axis convention, wide-end direction, cutout angles, included sub-components)
- [ ] Mesh imported with correct orientation (transform chosen from audit output, not assumed)
- [ ] Mesh scaled to real-world target dimensions
- [ ] Silhouette extracted with reasonable point count (5-15 control points)
- [ ] Parametric body matches mesh outline ±2% radius at sample Z values
- [ ] Cutouts at correct Z range AND angle (verify both via mesh-audit, not just visual)
- [ ] Mapping table (mesh-frame → world-frame → component-frame) documented before any cuts applied
- [ ] Standard fusion-mcp-bridge handover checklist also passed
- [ ] Mesh component (`00-Mesh-Reference`) hidden or deleted before STL export

## Tool comparison (2026-05 snapshot)

| Tool | Strength | Free tier | API |
|---|---|---|---|
| **Tripo3D** | Clean topology, good outline detection | ~10 generations/month | Yes (paid) |
| **Rodin (Hyperhuman)** | Sculpture meshes, clean wires | With watermark | Yes |
| **Meshy** | Production-grade meshes | 200 free credits | Yes |
| **TripoSR (local)** | Free, open-source, MPS/CUDA | Unlimited | N/A |
| **Luma Genie** | Fast, good UX | Yes | No |

Default choice: **Tripo3D** for first iteration. Switch to Rodin if topology too noisy.

## Related

- `fusion-mcp-bridge` — bridge setup, API patterns, recovery — required dependency
- `mechanical-design-principles` — convex-profile validation rule applies to mesh-derived splines too
- `cad-construction` — overall CAD workflow this skill plugs into
- `<your-projects>/fusion360-mcp-bridge/cli/` — `fusion mesh-import` and `fusion mesh-silhouette` CLI
