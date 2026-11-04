---
name: dxf
description: Generate, regenerate, and validate 2D DXF drawings from Python ezdxf sources. Use for DXF files, gen_dxf() sources, 2D profiles, outlines, templates, gaskets, panels, flat patterns, laser/plasma/waterjet cut layouts, and 2D drawing exports of CAD geometry.
---

# DXF generation and validation

Provenance: maintained in [earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad).
Use the installed local skill files as the runtime source of truth; the
repository link is only for provenance and release review.

## Purpose

Create or modify 2D DXF drawings from natural-language requirements or from CAD geometry, generate validated `.dxf` artifacts, and return checked outputs. DXF sources are Python files defining `gen_dxf()` returning an `ezdxf` document; the CLI owns output paths.

Two source shapes are supported:

- **Standalone drafting**: a Python source defining only `gen_dxf()`. Use for pure 2D outputs — gaskets, panels, templates, cut layouts — with no 3D model behind them.
- **CAD projection**: a `gen_dxf()` added to a CAD generator source that also defines `gen_step()`. Use when the DXF is a drawing or profile of a 3D part; create and validate the STEP geometry with `$cad` first, then add the projection in the same source file.

## Use this skill when

Use this skill when the user asks for DXF files, 2D drawings, profiles, outlines, templates, gaskets, panels, flat patterns, or cut layouts for laser, plasma, waterjet, or CNC routing.

Use `$cad` for the 3D part or assembly a DXF derives from. Use `$sendcutsend` for SendCutSend-specific upload preflight.

## Defaults

Use these defaults unless the user specifies otherwise:

- Units: millimeters; set them explicitly on the document (`doc.units = ezdxf.units.MM`).
- Geometry lives in modelspace at 1:1 scale.
- Cut profiles are closed polylines or closed line/arc loops; open contours only for engraving or reference geometry.
- For CAD-backed parts, prefer deriving DXF cut contours from the actual STEP/solid topology in the same generator script: build the 3D shape, select/project the real planar faces, unfold them into flat coordinates, and emit closed contours from those projected face wires. Use hand-drawn parametric outlines only when there is no reliable 3D topology to project.
- Layers carry intent: keep cut geometry and bend/fold lines on separate layers, and include "bend" in bend-layer names so downstream tools classify them as bends rather than cuts.
- DXF layers are drawing structure, not STEP part/assembly structure.

## Tool

The launcher lives in the DXF skill directory:

```bash
python scripts/dxf targets... [flags]
```

Use the active project Python interpreter; treat `python` as an interpreter placeholder, and use `--help` for the full interface. Target paths resolve from the command's current working directory; run from the workspace that owns the artifacts with cwd-relative target paths. Keep a DXF output and its Python generator in the same directory with the same basename unless the user requests otherwise.

A DXF target is a Python source defining:

```python
def gen_dxf():
    ...
    return document
```

Plain generated Python targets write sibling `.dxf` outputs. Use `-o`/`--output` only with one plain generated Python target, or use `SOURCE.py=OUTPUT.dxf` positional pairs for per-target custom outputs. Do not put output paths in the `gen_dxf()` return value.

`scripts/dxf` is a generator; it does not inspect existing `.dxf` files. For existing DXF inspection, use `ezdxf` for entity/layer checks and `$cad-viewer` for visual review.

## Workflow

1. Convert the request into a short brief: outline dimensions, holes and slots, layers, units, output path, and validation targets.
2. For CAD projections, generate and validate the STEP geometry with `$cad` first, then add or update `gen_dxf()` in the same source. When possible, derive the DXF from in-memory STEP/solid topology rather than duplicating geometry formulas, so the DXF remains a direct projection/unfold of the part being exported.
3. Write or edit the Python source with meaningful dimensions as named parameters.
4. Run `scripts/dxf` on explicit Python source targets only; do not run directory-wide generation.

```bash
python scripts/dxf path/to/source.py
python scripts/dxf path/to/source.py -o path/to/output.dxf
python scripts/dxf path/to/a.py=out/a.dxf path/to/b.py=out/b.dxf
```

5. Validate the generated DXF deterministically, then hand off and report.

## Validation

Verify the generated file with targeted `ezdxf` checks instead of eyeballing: entity counts by type and layer, closed flags on cut profiles, drawing extents, and every dimension the user specified.

```python
import ezdxf

doc = ezdxf.readfile("path/to/output.dxf")
msp = doc.modelspace()
profiles = [e for e in msp.query("LWPOLYLINE") if e.closed]
holes = msp.query('CIRCLE[layer=="0"]')
```

Report only checks that actually ran.

## Handoff

After creating or modifying `.dxf` artifacts, you must ALWAYS hand the explicit file path(s) to `$cad-viewer` when that skill is installed and include its live viewer link(s) in the final response. If `$cad-viewer` is unavailable or startup fails, report that and rely on `ezdxf` checks instead of silently omitting the handoff.

Final responses should include generated files, returned viewer links, validation actually run, and assumptions.
