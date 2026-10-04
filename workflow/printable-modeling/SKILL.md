---
name: printable-modeling
description: Create or edit geometry intended for FDM printing from uploaded images, existing models or a modeling brief. Choose parametric CAD or organic mesh work, preserve editable source and validate exports.
---

# Modeling for a printed object

Choose the method that can produce the requested shape, then use tools actually available in the current environment. A skill does not install a modeling engine or provide an image-to-3D account. Read [methods.md](references/methods.md) for shape and fabrication judgments.

For installed skills, locate scripts from this actual `SKILL.md` directory and companion skills from its parent. Read adjacent `runtime.local.json` when present for the Python interpreter used during setup, then verify dependencies. Use absolute script/job paths outside the clone; `python skills/...` examples assume the repository root. Blender has its own embedded Python environment and may need separate dependency setup.

| Input and desired result | Route |
|---|---|
| Uploaded image or selected concept image | Preserve the reference and inspect it; use the [image-to-3D route](references/image-to-3d.md) for an organic mesh draft, then repair and adapt it |
| Existing model; resize, reorient, split or change base | Preserve the original; use slicer tools for simple edits, mesh/CAD tools for geometry changes |
| Ribbons, helices, waves or adjustable ornamental forms | Parametric OpenSCAD using continuous curves or sweeps |
| Dimensioned brackets, fits or assemblies | Parametric CAD with dimensions and constraints; export real STEP only when supported by the CAD engine |
| Natural anatomy, expression or fine folds | Blender/mesh sculpting or adaptation of a suitable existing sculpture |

## Uploaded-image shortcut

An uploaded image can replace concept generation. When the user says “make this printable,” save the supplied image in the job's `source/` directory, preserve its original and record which file is selected. If several images were supplied, establish which is the design and which are additional views. Do not force an ImageGen step or redraw an already accepted design. Cropping/background cleanup is optional and should preserve the form.

Inspect the actual image before modeling. A photograph of a sculpture, a drawing and a front-only logo require different interpretation. One image leaves the back and underside unspecified; disclose significant assumptions. A logo or dimensioned silhouette may suit relief/extrusion better than organic image-to-3D. A generated mesh is a draft, not proof of printability.

## Refine and validate the actual mesh

For generated organic meshes or a repair loop, read
[refinement-and-validation.md](references/refinement-and-validation.md).
The official Hunyuan3D 3.1 website provides an optional high-poly draft route
when account access and quota are available. The bundled `hunyuan_shape.py`
provides the 2.1 demo adapter. The separate optional
[official 3.1 adapter](references/hunyuan31-api.md) supports configured API jobs
with explicit recovery. Use [V2](../idea-to-print/references/workflow-v2.md) to
bound attempts and [model_pipeline.py](references/model-pipeline.md) for actual
import/export, six-view rendering and limited regional operations.

Keep visual resemblance independent from topology: a watertight animal can
still have the wrong face or plate-like fur. Use Blender Python, sculpting,
curves/bevels, booleans or Geometry Nodes for the actual observed defect.
Preserve a raw mesh and editable revision; do not replace detailed geometry
with a smooth proxy just to make checks pass.

A configurable `PASS / FAIL / UNKNOWN` geometry report belongs to one exported
mesh and profile hash. Use the companion
`3d-print-workflow/scripts/printability_gate.py` for its supported checks and
retain unsupported checks as unknown. Scope wall/detail/connection targets by
part, nozzle, material and intended handling. Sampling and visually plausible
results do not establish a global minimum or a complete self-intersection test.

## Execute and verify

Keep each job in a user-selected local workspace with `source/`, `work/` and `outputs/`; do not depend on another person's machine paths. Check the local runtime first. Blender is suitable for organic mesh repair; OpenSCAD is optional for parametric forms. Hosted generation uses the remote service's GPU; local Blender CPU repair/rendering does not require a dedicated GPU. Read the image-to-3D reference before uploading or making hardware claims.

1. Translate the brief/reference into silhouette, important views, dimensions and units, contact surface, material and finish. Preserve the user's form instead of silently substituting a geometric approximation for detailed anatomy.
2. Make a coarse editable version first and render front and side/three-quarter views. Inspect back and underside for generated organic meshes. Resolve silhouette and geometry errors before fine detail.
3. Design thickness, attachment paths, stability and access for support removal together. Choose orientation or split points if supports would be enclosed.
4. Export with known units. Use the companion `3d-print-workflow/scripts/print_audit.py mesh` for basic STL topology and bounds, or its configured `printability_gate.py` for a scoped report. Check the actual output's methods and limits; neither establishes every thin connection, self-intersection or stability condition automatically.
5. Compare actual exported-mesh renders with the chosen references in a separate fidelity report. Fix or expose changed anatomy, silhouette, detail and negative space; white geometry previews help distinguish shape from texture.
6. Preserve editable source, exported mesh, previews, revision hashes and assumptions. Hand that revision to `3d-print-workflow` for layer and support inspection; diagnostic slicing can reveal repair needs. Do not label a diagnostic slice ready. Distinguish modeled, checked within scope, sliced and physically tested.

`assets/flow-ribbon.scad` is an original adjustable example with height, twist, thickness and base parameters. Copy it into a job before editing. It demonstrates geometry, not organic sculpting or a validated support-free print. Export evaluated geometry with `openscad -o model.stl --export-format binstl model.scad`; render a real preview with `openscad -o model.png --render --viewall --autocenter model.scad` when the installed OpenSCAD build supports image rendering. Recheck dimensions, thickness and supports after parameter changes.

For a modeling-only request, deliver the usable model and its verification level. Do not infer authorization to print, schedule or queue another object.
