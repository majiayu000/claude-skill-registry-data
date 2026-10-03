---
name: pfc5-geometry-import
description: Prepare and validate portable CAD, polyline, node-element, clump, and boundary geometry contracts for PFC 5.0 asphalt models without bundling opaque legacy executables.
---

# PFC5 Geometry Import

Use this skill when aggregate shapes, molds, loading heads, wheel surfaces, or
boundaries originate from CAD or node/element data.

## Required Inputs

- PFC2D/PFC3D 5.0 and target object;
- source format, units, axes, scale and coordinate origin;
- node/element/polyline schema and indexing convention;
- topology requirements and downstream PFC5 command path;
- legal status of any external converter.

## Workflow

1. Prefer simple native PFC5 walls for boxes, platens, cylinders and test heads.
2. For external geometry, freeze units/axes and convert to transparent CSV/text.
   PFC5 native `geometry import` supports its geometry format plus partial DXF and
   text/binary STL; `wall import` can consume supported files or a geometry set.
3. Validate duplicate IDs, missing node references, degeneracy and extents with
   `scripts/validate_geometry_csv.py`.
4. Materialize geometry in a private case and inspect it before particle filling.
5. Test one wall/contact or one clump template before bulk generation.
6. Record the exact external-to-PFC5 handoff and runtime probe.

Read [geometry-contract.md](references/geometry-contract.md) for CSV schemas.

## Working Rules

- Old executables are optional external tools, never package dependencies.
- A valid file does not prove correct scale, orientation, manifold quality or contact normals.
- Do not use `wall import ... nothrow` as a default repair strategy: PFC5 may ignore
  offending facets, leaving an incomplete wall. If used diagnostically, audit the
  rejected facets and final wall closure explicitly.
- Do not translate newer-major geometry commands into PFC5 by keyword substitution.
- Preserve original geometry and generated intermediate files separately.

## Output Contract

Return source/provenance, units/axes, validated CSVs, extents/topology report,
PFC5 handoff, contact probe and runtime status.

## Local Contents

- `references/geometry-contract.md` — portable node/element/polyline schemas.
- `scripts/validate_geometry_csv.py` — deterministic geometry validator.
- `agents/openai.yaml` — interface metadata.
