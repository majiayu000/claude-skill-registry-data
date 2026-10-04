---
name: parametric-cad-design
description: Use when designing, revising, validating, documenting, or rendering mechanical CAD parts with Shapr3D .shapr archives, STEP/Parasolid references, OpenSCAD, CadQuery/build123d/OCP, FreeCAD, Blender, STEP/STL/DXF/SVG/PDF exports, print-fit compensation, versioned artifacts, exact B-rep regeneration, optical holders, C-mount/OpenHI threads, PCB/sensor holders, or old STEP reference measurements.
---

# Parametric CAD Design

Use this skill for agent-assisted mechanical design where the deliverable should remain editable and reproducible, not just a one-off mesh.

## Core Workflow

1. Inspect source files before designing. Prefer `.shapr` package metadata, STEP labels, measured bounding boxes, datasheets, and old README notes over visual guesses.
2. For asymmetric modules, define the source face, mating face, optical axis, PCB long axis, PCB short axis, and sign convention before changing geometry. Write the source-to-holder transform explicitly.
3. Decide the mode: exact B-rep regeneration, surgical print-fit variant, or new clean parametric design. Do not mix these silently.
4. Keep dimensions in named parameters. Do not globally scale a whole part to tune fit.
5. Preserve prior project runs inside the same design folder. Use `runs/run-N-human-readable-info-YYYYMMDDTHHMMSSZ/` for archived runs and keep the root `artifacts/` directory as the latest checked output.
6. Export editable source, decomposed STEP bodies, assembly STEP, printable STL, and full-view render PNG. Add exploded/detail renders when geometry is hard to inspect.
7. Validate STEP import, solid count, bounding box, mesh watertight/component count, and render before committing.
8. Put one directly usable final STEP at the design root as `USE_THIS_<design>.step` when there are many artifact STEP files. Keep reference/cutter/smooth variants under `artifacts/`.
9. When the user asks for Nutstore sync, or when generating final LabCanvas CAD handoff artifacts, copy the final root `USE_THIS_*.step` or final `*_assembly.step`/`*_assembled.step` to `/home/lachlan/Nutstore Files/Projects/LabCanvas` with its descriptive filename intact.

When Shapr3D archives, OpenHI/Nature geometry, C-mount, optical holders, or sensor/PCB holders are involved, read `references/shapr3d-cad-patterns.md` after this file.
When a PCB photo, sketch, rear view, component view, or mating face controls an asymmetric holder, also read `references/pcb-sensor-mating-face-orientation.md`.
When joining round OpenHI/4F tubes inside a thin square envelope, also read `references/openhi-square-tube-connectors.md`.

## Geometry Discipline

- Pick one datum and keep every related feature aligned to it. For optical parts, the optical axis should drive C-mount bores, sensor packages, board pockets, and renders.
- For a finite-thickness lens, never silently use one number for both the optical surface datum and the mechanical seat. Record the inward optical-axis surface vertex, inward annular support contact, outward annular support contact, and external flange plane separately. Apply the requested focal distance to the chosen optical datum; derive the fully inserted holder/cap cavity from the two annular contacts plus named axial clearance. Do not add the lens thickness or an internal threaded insertion depth a second time to the `2f`/`4f` chain unless the source flange contract actually places it outside that chain.
- For a standard 30 mm optical cage, rod centers are at `x/y = +/-15 mm` from the optical/sample center. Use nominal 6 mm rods with a named printed clearance such as `6.4 mm` unless a specific reference says otherwise; do not move cage holes toward a wider holder's outer corners.
- When adding clearance to a pocket or sink, add it symmetrically around the selected datum. If a printed part shows one side smaller than the other, first check whether an intentional datasheet offset is still valid; if not, make a new centered sibling variant and document the offset removal.
- Keep mating bodies editable. Export separate STEP/STL bodies for sockets, plates, inserts, thread cutters, boards, and fixtures when the user may edit them in Shapr3D or FreeCAD.
- Avoid accidental connector geometry. If the user asks for direct contact, remove bridge blocks and middle cylinders; do not replace one unwanted bridge with another.
- Bound threads inside their parent length. A thread cutter for a socket from `x=0` to `x=H` should start after a small lead-in and end before `H`; then clip/intersect the swept thread so no tooth overflows beyond either end.
- For a full first and last tooth, sweep both male and female thread profiles about half a pitch beyond each true end, then intersect with the exact parent-length clipping solid. Extending construction geometry is useful; exporting overflow is not.
- Build difficult off-axis threads in a known-stable axis frame, complete all thread booleans and bore cuts there, and rigidly rotate the finished solid onto its assembly axis. A valid standalone sweep does not prove that a direct off-axis boolean survived in the final body.
- Audit threads in the final exported solid, not only in thread cutters or construction bodies. Record the expected axial interval and require helical face evidence there after STEP round-trip; a valid one-solid STEP can still contain only a smooth pilot/root cylinder when OCCT silently classifies a helical region away.
- When a circular bore nearly fills a square body, do not place radial set screws at the face center by habit. Calculate engagement over the complete thread crest, then offset the hole tangentially toward a corner if needed. Preserve a named outer ligament and verify adjacent-face clearance.
- For an internal tube stop printed along the tube axis, prefer an annular triangular ridge with straight chamfers over an unsupported right-angle shelf. Keep the optical opening explicit. "Straight fillet" should be interpreted as a chamfer or bevel, not a rounded fillet.
- Document the contact plane between independent bodies, for example `socket x=0..12`, `plate x=12..19`.
- Use clearance holes and pockets for real protrusions such as pin headers, solder joints, cables, screws, and printed-fit errors. Keep those clearances named and visible in the manifest.
- Prefer simple, clean solids over decorative or overly coupled boolean shapes. If Shapr3D reports invalid geometry when editing, split the part into independent adjacent bodies and bounded cutters.
- For large flat printed parts, add removable anti-warp ears by default unless the user explicitly wants a clean outline. After the 2026-07 dock print feedback, default to stronger/larger ears: about `0.8-1.0 mm` sacrificial Z thickness, weak breakaway overlap, two side pulls, and a diagonal full-corner pull tab from the true corner to a wider/larger tail pad. Use `0.5 mm` only when easy removal is more important than hold-down strength. The diagonal pull matters because side tabs mostly hold the adjacent edges, not the actual corner.
- When a design is ready to print, create a timestamped run folder inside the design, such as `runs/run-N-short-name-print-ready-YYYYMMDDTHHMMSSZ/`, and put the direct print outputs there instead of leaving them only in root `artifacts/`. Also make a clean Nutstore print folder such as `/home/lachlan/Nutstore Files/Projects/LabCanvas/<design>/run-N-short-name-print-ready-YYYYMMDDTHHMMSSZ/` with `PRINT_THIS_*.stl`, `PRINT_THIS_*.step`, `PRINT_THIS_*.3mf`, manifest, README, separate part STEP files when relevant, and render PNGs for both the final single assembly and the exact direct-print layout. Loose STEP copies are useful for Shapr handoff, but print-ready folders prevent choosing the wrong run.
- Do not expose source assembly coordinates or a multi-object edit package as the default slicer file. Rigidly orient every `PRINT_THIS` model, center it in XY, place its true printable base at `Z=0`, and package one intended print as one 3MF model/build object. When the source B-rep stores thread teeth and roots as overlapping solids, boolean-union them only in the print copy and verify one valid watertight solid; keep the exact multi-solid STEP unchanged. Validate `min_z = 0`, at least one triangle crossing the first layer, one 3MF build item, and a rendered build-plate view. Keep source-coordinate/multi-solid evidence under `artifacts/` or an archived run.

## Layer-Shift Triage

When a physical print develops a lateral staircase, do not assume the CAD was
generated with shifted layers. Separate model evidence from printer motion:

1. Inspect both the exported 3MF and the slicer-resaved project. Resolve 3MF
   component indirection, then count mesh objects, components, build items, and
   transforms. A constant build-plate translation is normal.
2. Compare vertex count, triangle count, triangle indices, and centered vertex
   coordinates. Serialization-scale rounding is not a geometric shift.
3. Sample horizontal mesh sections at the intended layer height and measure
   each section bounding-box center. For threaded parts, allow the small
   periodic envelope change caused by the helix; flag millimetre-scale
   discontinuities separately.
4. If the source and slicer project are straight, the base remains attached,
   and repeated attempts shift at different heights or a different number of
   times, treat the result as intermittent XY step loss. Check nozzle/support
   collisions, blobs or warp, belt and pulley fastening, rail binding,
   cable/filament snags, and only then motor-driver/electrical causes.
5. Inspect the actual saved slicer profile. Very high acceleration and travel,
   dense infill, or aggressive automatic supports can expose a marginal motion
   system or create collision opportunities even when other prints succeed.
6. Run one conservative diagnostic reslice of the same verified mesh. Do not
   regenerate correct geometry merely to address a physical layer shift.

Preserve a short diagnosis with mesh hash, topology, layer-stack measurements,
slicer settings, failure photograph, and the remaining limitation when actual
G-code or printer logs are unavailable.

## Shapr3D And STEP Intake

Read the `.shapr` archive directly first. It is a zip whose `workspace` member is
SQLite, and most of the design knowledge is readable without Shapr3D: body and
folder names, sketch planes and every sketch curve in millimetres, the ordered
operation history with decoded distances/angles/enums, imported-body placement
transforms, and Parasolid/schema versions. Only the solid bodies themselves are
opaque Parasolid blobs. Never tell the user a `.shapr` cannot be used until a
STEP arrives; decode it, reconstruct sketch-driven parts parametrically, and use
STEP only as the exact B-rep for imported or face-edited bodies.

Full native decode (Markdown or JSON):

```bash
python ~/.codex/skills/parametric-cad-design/scripts/shapr_native_decoder.py /path/to/design.shapr --markdown
python ~/.codex/skills/parametric-cad-design/scripts/shapr_native_decoder.py /path/to/design.shapr --json --out design.decoded.json
```

Quick triage of `.shapr` plus STEP folders together:

```bash
python ~/.codex/skills/parametric-cad-design/scripts/inspect_shapr_step_sources.py \
  --shapr /path/to/design.shapr \
  --step /path/to/step-folder \
  --markdown
```

If run from `../LazySkills`, replace the script path with `skills/parametric-cad-design/scripts/inspect_shapr_step_sources.py`.

Interpretation rules:

- Sketch curves are UTF-8 JSON in metres: type `0` line, `1` arc, `2` circle,
  `3` B-spline, `4` interpolating spline, `5` ellipse. Operation parameters are
  typed msgpack values: `[12, [[1,1], v]]` is a length in metres, `[12, [[2,1], v]]`
  an angle in radians, `[7, id]` a HistoryName reference, `[10, id]` a sketch,
  `[11, id]` an imported body. See `references/shapr3d-cad-patterns.md`.
- `HistoryTreeNodes` type `2` nodes decode into Shapr operation names such as `Extrude`, `OffsetFace`, `Transform`, `Revolve`, `Boolean`, `Split`, and `MaterializeImportedBodies`.
- Many `HistoryImportedBodies` plus zero/few `Shapes` means the `.shapr` is mostly imported B-rep, not a recoverable feature tree.
- Many `OffsetFace` operations usually mean physical print-fit tuning; translate those into named clearance/tolerance parameters in new code.
- Many `Transform` or `Align` operations usually mean the file is an assembly; preserve placement transforms and local part frames.
- Exact regeneration should preserve the STEP/Parasolid B-rep and prove equivalence by source path, body labels, solid count, bbox, face/surface evidence, and render.
- Physical fit changes should be sibling variants from the exact baseline. Do not overwrite exact regeneration folders.
- When old B-rep booleans leave thread shells, transparent Shapr regions, slow Shapr repair, or invalid geometry, preserve the stable source body and replace only the fragile region with clean analytic sleeves/sockets. Validate the exported STEP itself, not only the in-memory CAD object.
- An imported male thread may be split across two STEP solids: a low-volume helical tooth solid and a root cylinder embedded in the neighboring main body. When changing its pivot diameter, rebuild only the tooth and add only a thin annular sleeve to the root body. Replacing the tooth solid with a complete threaded cylinder duplicates material while still appearing superficially valid.

## Print-Fit Measurement

When adapting old 3D-printed parts:

- Measure old STEP solids by named BRep labels such as `Thread camera 24.4`.
- Record male and female values separately. A male part that inserts into another part is usually kept smaller; the receiving hole/socket/pocket is enlarged.
- Maintain a table for all mating fits: threaded parts, slip-fit pockets, square modules, pins, holes, and optical holders.
- Use a test coupon for uncertain threads before printing large parts.
- When horizontal female threads are part of the print, provide both a true-helical version and a smooth tap-ready pilot version. Export one single fit-test male screw before a full grid.
- Do not confuse standard C-mount with the user's larger OpenHI lens/BS/top thread family. C-mount is `1"-32 UN`, nominal major diameter `25.4 mm`, pitch `0.79375 mm`. The OpenHI lens/BS/top family is near 30 mm and should not be converted to 25.4 mm unless the user explicitly asks for a new C-mount adapter.
- For standard-like printed female C-mount sensor holders, treat `25.4 mm` as the nominal internal thread/groove maximum, not the smooth pilot. Prefer a `25.0 mm` female pilot/root and a `25.4 mm` nominal cutter maximum; avoid a `25.4 mm` pilot plus larger groove unless the user wants a loose high-clearance experiment.
- For the exact OpenHI six-file family measured from `OpenHI_STEP`, the local helical profile has `0.8 mm` pitch and `0.4 mm` radial tooth height, so crest/groove diameter is pivot plus `0.8 mm`. The coordinated fit revision changes old `29.6/30.2` male/female pivots to `29.8/30.0`, and old `29.8/30.2` pivots to `30.0/30.0`. Preserve the `25.5 mm` lens seats and the source transition chamfers. Do not reuse the older `0.2 mm` radial-height coupon table for this exact source family.
- When a regenerated OpenHI receiver looks messy after a fill-and-recut operation, assume old threaded B-rep faces may remain as internal slivers. Prefer trimming the old receiver away at a stable datum, rebuilding the receiver as a clean adjacent solid, and then unioning it back. Validate that no exposed fill-cylinder shell remains and that helical B-spline faces start only at the intended thread start.
- When the original OpenHI part contains a working internal receiver, recover its exact void from a bounded source solid and subtract that void from the new body instead of approximating it with a lead-in chamfer. Compare the expected and generated voids inside the same bounded domain in both directions, verify nonzero thread relief beyond a smooth pilot, and record the minimum remaining radial wall.
- If Shapr3D takes a long repair pass, drops threads, or shows transparent faces, count B-spline faces in the exported STEP. Helical B-spline thread faces are a common cause. For Shapr-target files, replace fragile helical threads with bounded analytic ring-groove previews, and also export a smooth editable STEP with no thread preview so Shapr native threads or physical tapping can be used later.
- When a Z-axis helical cutter exports as a split STEP or loose fragment, construct the helix in a stable axis frame that already works for another variant, rotate it into place, then verify the final STEP re-import has one connected solid.
- `Nature.shapr` and the flattened `cad/extracted/OpenHI_STEP/` exports can describe the same bodies. On Ubuntu, exact regeneration should usually preserve the exported STEP B-rep, because the `.shapr` often stores imported Parasolid bodies rather than editable feature history.

For helical threads made from a swept triangle, document:

- root diameter and crest diameter;
- pitch or gap;
- tooth height;
- tooth base width;
- thread hand and viewed-from direction;
- thread length and unthreaded lead-in length.

## Sensor, PCB, And Optical Holder Rules

- Use the board or sensor module as the source of truth: outline, mounting holes, active center, component side, socket side, wire exit, protrusions, PCB thickness, and adhesive thickness.
- Label every directional measurement with a face and axis. Bare words such as left, right, top, bottom, front, and back are not geometry contracts.
- Treat source-view to mating-view placement as an explicit transform. Apply it to the derived PCB-face features, not automatically to an already-correct C-mount, optical axis, plate, or depth stack.
- Use photos to resolve orientation and physical meaning; use measured values or datasheets to control dimensions. Do not add visible daughterboards, connectors, notches, or housings unless the requested holder actually needs their envelopes.
- When the user says a feature is almost correct or needs a slight adjustment, calculate and report the delta from the accepted run before rebuilding. A small correction must not silently become a large absolute translation.
- Keep the optical axis and sensor active center explicit. The PCB geometric center is often not the sensor center.
- Reliefs for sockets and wires must extend to the holder edge when the plug needs insertion/removal clearance.
- If a PCB is recessed, socket relief height is measured from the PCB top surface, not from the bottom of the holder.
- Treat connector housings and PCB-side solder tails as separate envelopes. If through-hole tails face the holder, cut their relief on the PCB seating face; for closely pitched rows, join overlapping clearance holes into one continuous slot so thin webs cannot foul the pins.
- To recess a PCB without moving an established sensor/thread datum, preserve the structural seating plate and add the pocket depth as a raised perimeter outside the PCB footprint. Validate the installed PCB top plane relative to the new rim.
- Keep C-mount socket, sensor plate, board proxy, sensor proxy, thread cutter, and final assembly as separate STEP bodies when practical.
- Keep visualization proxies separate from printable geometry. A richer assembly render must not make the holder itself more complicated.
- Preserve accepted geometry with regression invariants: unchanged envelope, named datums, seating plane, thread limits, and unaffected parameters. Compare solid count, bounding box, and volume with the accepted baseline after a narrow orientation fix.
- For light valves and apertures, make the active aperture a through-cut and support the device only on a shallow retaining ledge around the active area.

## Useful Commands

Inspect `.shapr` and STEP sources:

```bash
python ~/.codex/skills/parametric-cad-design/scripts/inspect_shapr_step_sources.py \
  --shapr cad/extracted/Nature.shapr \
  --step cad/extracted/OpenHI_STEP \
  --markdown
```

Inspect a full Shapr backup folder:

```bash
python ~/.codex/skills/parametric-cad-design/scripts/inspect_shapr_step_sources.py \
  --shapr-dir "/home/lachlan/Nutstore Files/Projects/shapr3d/BACKUP/BATCHEXPORT" \
  --markdown
```

Generate OpenSCAD STLs:

```bash
openscad -D 'part="tube"' -o artifacts/v2/tube.stl model.scad
openscad -D 'part="holder"' -o artifacts/v2/holder.stl model.scad
```

Generate STEP/drawings with a repo-local CAD Python kernel:

```bash
cad/.conda/cad-python/bin/python path/to/generate_support_artifacts.py
```

Render with Blender:

```bash
blender --background --python path/to/blender_render.py
```

Validate meshes:

```bash
cad/.conda/cad-python/bin/python - <<'PY'
import trimesh
mesh = trimesh.load("artifacts/v2/assembly.stl", force="mesh")
print(mesh.is_watertight, len(mesh.split(only_watertight=False)), mesh.bounds[1] - mesh.bounds[0])
PY
```

Validate STEP bounds:

```bash
cad/.conda/cad-python/bin/python - <<'PY'
import cadquery as cq
shape = cq.importers.importStep("artifacts/v2/assembly.step")
bb = shape.val().BoundingBox()
print(bb.xlen, bb.ylen, bb.zlen)
PY
```

Validate Shapr-friendly STEP topology:

```bash
cad/.conda/cad-python/bin/python - <<'PY'
import cadquery as cq
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_BSplineSurface
from OCP.TopAbs import TopAbs_FACE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS

path = "USE_THIS_design.step"
shape = cq.importers.importStep(path).val()
exp = TopExp_Explorer(shape.wrapped, TopAbs_FACE)
bspline_faces = 0
while exp.More():
    face = TopoDS.Face_s(exp.Current())
    if BRepAdaptor_Surface(face, True).GetType() == GeomAbs_BSplineSurface:
        bspline_faces += 1
    exp.Next()
bb = shape.BoundingBox()
print("solids", len(shape.Solids()), "valid", BRepCheck_Analyzer(shape.wrapped).IsValid())
print("bbox", bb.xlen, bb.ylen, bb.zlen)
print("bspline_faces", bspline_faces)
PY
```

Sync final assembly STEP to Nutstore LabCanvas:

```bash
mkdir -p "/home/lachlan/Nutstore Files/Projects/LabCanvas"
find . artifacts -maxdepth 1 -type f \( -name 'USE_THIS_*.step' -o -name '*_assembly.step' -o -name '*_assembled.step' \) \
  -exec cp -f {} "/home/lachlan/Nutstore Files/Projects/LabCanvas/" \;
```

## Completion Report

Report the source model path, current artifact folder, STL/STEP/3MF/DXF/SVG/PDF/PNG outputs, measured bounds, watertight/component checks, 3MF zip validation, render path, Nutstore LabCanvas assembly STEP copy when performed, commit hash, push status, and any remaining physical fit checks.
