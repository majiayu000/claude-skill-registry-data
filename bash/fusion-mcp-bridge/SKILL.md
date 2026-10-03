---
name: fusion-mcp-bridge
description: |-
  Use when driving Fusion 360 from Claude Code through the local MCP-Bridge (HTTP server on 127.0.0.1:7654 with bearer-token auth, single-threaded Custom-Event handler). Covers the API quirks that consistently bite without a documented protocol: component activation before geometry, single-revolve over loft+combine-join, cut-before-shell sequencing, tool-body combine-cut for complex cuts, boolean-union before cuts on multi-body components, bridge timeout/lock recovery, screenshot setup, and the `fusion` CLI that replaces curl boilerplate. Trigger on phrases like "Fusion 360 via MCP", "fusion-mcp-bridge", "Fusion Custom-Event", "run Fusion API script", or any `fusion` CLI command. Do NOT load for general parametric CAD (use `cad-construction`), mechanical-design rules (use `mechanical-design-principles`), or OpenSCAD/FreeCAD (use `cad-api-scripting`).

---

# Fusion 360 via MCP-Bridge

A localhost HTTP bridge between Claude and Fusion 360, plus the small `fusion` CLI that wraps it. This skill documents the API patterns that recurrently fail without explicit guidance.

## When to use

- Driving Fusion 360 geometry from a Claude session through the MCP-Bridge
- Writing Python scripts that will be executed via `/execute` against the bridge
- Debugging why a build script "ran" but produced no visible geometry change (silent-failure patterns)
- Recovering from a hung or unresponsive bridge

## When NOT to use

- General Fusion modelling discussion → `cad-construction`
- General Python CAD scripting (OpenSCAD, FreeCAD) → `cad-api-scripting`
- Manufacturing or wall-thickness rules → `mechanical-design-principles`
- Brainstorming a design (no CAD work yet) → `design-first-iteration`

## Setup

The bridge is a Fusion AddIn (`<your-projects>/fusion360-mcp-bridge/fusion-addin/`) that exposes three HTTP endpoints on `127.0.0.1:7654`:

- `GET /health` — bridge alive + active document info
- `POST /execute` — body `{"script": "<python>"}` runs script in Fusion, returns `{"result": "<stdout>"}`
- `POST /screenshot` — body `{"direction": "<dir>", "width": w, "height": h}` returns `{"screenshot": "<base64-png>"}`

Bearer token from `~/.fusion-mcp-secret` is required on all endpoints.

The `fusion` CLI wraps these endpoints. **Always prefer the CLI over raw curl** — it's shorter, error-handled, and consistent. Curl examples in this skill are fallbacks for when the CLI is unavailable.

```bash
fusion check                           # pre-flight
fusion run /tmp/build.py               # execute a script
fusion eval "print(1+1)"               # inline expression
fusion screenshot --direction front --out f.png
fusion components                      # list components + volumes
fusion volume "Hauptgehaeuse"          # specific body volume
```

## Pre-flight protocol

Before every Fusion build session, run:

```bash
fusion check
```

This confirms: bridge alive, bearer token loaded, active document with a Design product. If any of these fail, the bridge will hang or scripts will silently no-op — fix the prerequisite first.

If `fusion check` fails with timeout: see *Bridge recovery protocol* below.

## Core API patterns

These nine patterns cover the silent-failure modes that produced multiple wasted iterations on the a tall-cylinder speaker housing build.

### 1. Component activation before geometry operations

**Always** activate the target occurrence before creating sketches, features, or planes inside its component:

```python
occ_sockel.activate()
comp = occ_sockel.component
assert app.activeProduct.activeComponent.name == "01-Sockel"
# Now sketches/features land in 01-Sockel's timeline
```

**Failure mode without activate:** `comp.sketches.add(...)` may appear to succeed, but features land in the **root component's timeline**, not the target component. Browser tree shows them under root, not under the named component. Later edits, body queries, and STL exports all break. Fusion gives no warning.

### 2. Single-revolve > Loft + combine-join

For rotationally-symmetric bodies with a curved profile (e.g. vase shape with integrated dome top), prefer **one revolve** of a 2D side profile that contains both the spline curve and the dome arc, over **loft of cross-section circles + separate revolve-join for the dome**.

```python
# Side profile in xZ sketch:
# - sketchFittedSplines.add(<R,Z control points>) for the body curve
# - sketchArcs.addByThreePoints(p_start, p_mid, p_end) for the top dome
# - lines to close the profile (axis + bottom)
prof = sk.profiles.item(0)

rev_input = comp.features.revolveFeatures.createInput(
    prof, comp.zConstructionAxis,
    adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
)
rev_input.setAngleExtent(False, adsk.core.ValueInput.createByString("360 deg"))
comp.features.revolveFeatures.add(rev_input)
```

**Failure mode of loft+join:** `combineFeatures.createInput(target, [tool_body]).operation = JoinFeatureOperation` often returns silently with no merge — `target.volume` unchanged, tool body remains as orphan. Even after `app.documents.add()` to a fresh document, the failure persists. Treat `JoinFeatureOperation` via combine as unreliable for this case.

### 3. Cut-before-Shell sequence

If a component will be hollow with cuts (e.g. side ports through walls), perform the **cuts on the solid body**, **then** Shell:

```
Loft / Revolve  →  solid body
Combine-Cut     →  solid body with port-cuts
Shell           →  hollow body with bottom face open
```

**Failure mode of cut-after-shell:** Combine-Cut on a Shell-derived body silently succeeds (tool body consumed, feature added to timeline) but **no material is removed**, even when the cut tool clearly intersects wall material. Suspected cause: surface-surface intersection issues with thin shell + spline outer surfaces.

### 4. Tool-Body → Combine-Cut pattern

For complex cut shapes (ovals, irregular footprints, cuts that span multiple walls), do not use `ExtrudeFeatures.createInput(prof, CutFeatureOperation)` directly. Instead:

```python
# 1. Extrude the cut shape as a NEW body (separate tool body)
ext_input = comp.features.extrudeFeatures.createInput(
    profile,
    adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
)
ext_input.setOneSideExtent(...)
ext = comp.features.extrudeFeatures.add(ext_input)
tool_body = ext.bodies.item(0)

# 2. Combine-Cut: target minus tool
tools = adsk.core.ObjectCollection.create()
tools.add(tool_body)
comb_input = comp.features.combineFeatures.createInput(target_body, tools)
comb_input.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
comb_input.isKeepToolBodies = False
comp.features.combineFeatures.add(comb_input)
```

**Why this pattern:** direct `CutFeatureOperation` extrudes silently fail when the sketch profile sits inside the body cavity (e.g. on a plane through the center axis). Tool-Body + Combine-Cut is robust because the tool exists as its own solid before cutting.

### 5. Boolean-union before cuts on multi-body components

If a component contains multiple bodies (e.g. main wall + 4 ribs from a circular pattern), **union them all first** with `JoinFeatureOperation`, then do cuts. Silent-failure orphan bodies appear otherwise.

```python
tool_coll = adsk.core.ObjectCollection.create()
for rib in [b for b in comp.bRepBodies if b.name.startswith("Rippe")]:
    tool_coll.add(rib)

comb = comp.features.combineFeatures.createInput(main_body, tool_coll)
comb.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
comb.isKeepToolBodies = False
comp.features.combineFeatures.add(comb)
# now main_body is a single solid - cuts will work cleanly
```

### 6. Verification pattern: volume + body count

Visual screenshots can deceive. After every geometry-changing step, verify with the API:

```bash
# Volume check
fusion volume "Hauptgehaeuse"
# Body count + per-component summary
fusion components
```

If `volume` is unchanged after a Combine-Cut, the cut silently failed — do not move to the next step.

The CLI prints volumes in cm³. Internal Fusion units are always cm.

### 7. Visual style + camera setup for fresh documents

Fresh documents (created via `app.documents.add()`) often start in **wireframe display style**. Screenshots taken before fixing this look unhelpful:

```bash
fusion shaded                              # set display to ShadedVisualStyle
fusion view iso-top-right                  # set camera + fit
fusion screenshot --direction current --out img.png
```

Without `fit`, the camera may be set to a default distance unrelated to the body — the object appears tiny in a sea of background.

### 8. API version mismatch — saveAsImageFile

Older bridge code calls `Viewport.saveAsImageFileWithOptions(filename, w, h, True)` which **does not exist** in current Fusion versions (2702+). The current API is `Viewport.saveAsImageFile(filename, w, h)` — three positional arguments.

If `fusion screenshot` fails with `TypeError: takes 2 positional arguments but 5 were given`, patch the bridge's `_handle_screenshot` to use `saveAsImageFile`. The patched bridge file is at:

```
~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/FusionMCPBridge/FusionMCPBridge.py
```

### 9. xZ-Sketch convention: sketch-Y is INVERTED vs world-Z

When creating a sketch on `comp.xZConstructionPlane`, the 2D sketch's Y-axis is **inverted** relative to world-Z:

```
sketch (R, sketchY=-19, 0)  →  world (R, 0, +19)
sketch (R, sketchY=+19, 0)  →  world (R, 0, -19)
```

**Easy to miss** — bbox extent looks correct (still ±19.5 on world-Z), but a body revolved from the profile ends up 180°-X-flipped vs intended. The wide-end (Sockel) lands at the *opposite* world-Z direction.

**Diagnosis**: read the actual 3D coords of a sketch point and compare to what you specified in 2D:

```python
pt_2d = spline.fitPoints.item(0).geometry          # what you sketched
pt_3d = spline.fitPoints.item(0).worldGeometry     # where it ended up
print(f"sketch ({pt_2d.x}, {pt_2d.y}) -> world ({pt_3d.x}, {pt_3d.y}, {pt_3d.z})")
```

**Fix pattern** for revolve profiles defined in (R, world-Z) — negate the Z for sketch coords:

```python
def world_to_sketch(r, world_z):
    return (r, -world_z)   # negate Z for xZ-plane sketch-Y convention

for r_world, z_world in PROFILE_WORLD:
    r_sk, y_sk = world_to_sketch(r_world, z_world)
    spline_pts.add(P3D(r_sk, y_sk, 0))
```

**Note**: `xYConstructionPlane` (sketch-Y maps to world-Y) and `yZConstructionPlane` (sketch-Y maps to world-Z) have *different* conventions — always verify with `worldGeometry` on the first sketch you make on a new plane.

This was the root cause of the a tall-cylinder mesh-vs-solid 180°-X-misalignment: the silhouette spline was extracted in (R, world-Z) form and pasted into an xZ-sketch verbatim, producing a Solid with Sockel at +Z while the mesh had Sockel at -Z.

### 10. Bridge timeout / lock recovery protocol

When `fusion health` hangs (TCP accepts but bridge doesn't reply within timeout), Fusion's main thread is blocked. This commonly happens after:

- Many rapid Custom-Event invocations
- A modal dialog opening behind another window (Save-As prompt, error dialog, migration warning)
- Long-running script that hit an internal deadlock

**Recovery sequence:**

1. **Bring Fusion 360 to foreground** — the dialog might be hidden but blocking the UI thread
2. **Dismiss any modal dialog** — even an "OK"-only error
3. **AddIn restart** — Tools → Add-Ins → FusionMCPBridge → Stop, then Run
4. **Last resort** — restart Fusion completely (save your work first; ungespeicherte v3-Iterationen sind heute schon einmal verloren gegangen)

After step 1 or 2, `fusion check` usually responds again without further intervention.

## Convex profile validation (rotationally-symmetric bodies)

For revolve profiles with a "bulge" (max radius somewhere above z=0), the spline must be **convex throughout** — no waist (concave middle section). Mathematically: `dR/dz` must monotonically decrease (become more negative) past the bulge maximum.

Quick validation: compute slopes between consecutive control points. If any post-bulge slope is **less negative** than the previous one, you have a waist:

```python
slopes = [(z2-z1, r2-r1, (r2-r1)/(z2-z1)) for (z1,r1),(z2,r2) in zip(pts, pts[1:])]
# After the max-bulge index, dR/dz values should be monotonically decreasing
```

For the a tall-cylinder speaker housing build, the original spline `[(7.0,0), (7.5,1.5), (8.0,4.0), (7.4,9.0), (6.5,16), (5.8,22), (5.5,25.5)]` produced a visible concave waist between z=4 and z=9. The corrected v4 spline `[(7.0,0), (7.5,1.5), (7.7,4.0), (7.3,10.0), (6.4,18), (5.7,24), (5.5,25.5)]` is convex throughout.

## Anti-patterns (do not do)

- **Calling `comp.features.something.add()` without `occ.activate()` first** — features land in root, not in component
- **Combine-Join via revolve `JoinFeatureOperation` parameter for a separate dome body** — use single-revolve with arc in profile, or accept that it may silently fail
- **Cut-after-Shell** — perform cuts on solid, then Shell
- **Direct CutFeatureOperation extrude with sketch profile in empty space** — use Tool-Body + Combine-Cut
- **Cut on multi-body component without union first** — orphan bodies will appear, cuts won't reach intended geometry
- **Trusting visual screenshots alone after a Combine-Cut** — verify with `fusion volume`
- **`app.documents.add()` repeatedly during debugging** — accumulates unsaved documents and contributes to bridge lock
- **Ignoring a hanging `fusion health`** — always recover the bridge before continuing; the next script will hang too

## Handover checklist

Before declaring a Fusion-MCP build session complete:

- [ ] `fusion check` returns OK
- [ ] All target components have expected body count and non-zero volume
- [ ] Browser tree shows features under named components, not under root
- [ ] Visual style is shaded + camera is fitted (for screenshots that go into the vault)
- [ ] Fusion document has been saved with Cmd+S (manual step — bridge cannot save)
- [ ] Build script committed to git (versionable record of what produced the current state)

## Related

- `<your-projects>/fusion360-mcp-bridge/cli/` — the `fusion` CLI source + install
- `<your-projects>/fusion360-mcp-bridge/fusion-addin/` — the Fusion AddIn (Python HTTP server)
- `~/.fusion-mcp-secret` — bearer token (created by `quickstart-mac.sh`)
- `cad-construction` — the CAD workflow this bridge operates within
- `mechanical-design-principles` — design rules that inform the geometry being built
