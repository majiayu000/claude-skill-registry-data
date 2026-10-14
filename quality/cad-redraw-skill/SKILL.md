---
name: cad-redraw-skill
description: >-
  Rebuild and validate 2D CAD drawings on Linux — exact redraw from a source
  DXF/DWG, PDF-to-DXF conversion, or image-to-CAD reconstruction with
  evidence-aware specs. Triggers: dwg redraw, redraw dxf, image to dxf, pdf
  to dxf, drawing fingerprint, raster to cad, redraw validation.
license: Apache-2.0
compatibility: opencode
category: CAD & Hardware Design
metadata:
  protocol: opencode-skill
  pattern: clean-room-port
---

# CAD redraw and validation (Linux / ezdxf)

Provenance: the workflow methodology follows
[pengxiaoan/autocad-dwg-redraw-skill](https://github.com/pengxiaoan/autocad-dwg-redraw-skill)
(evidence levels, fingerprint-first redraw, visual-vs-dimensional separation).
That repository ships no license, so no code was copied — this skill is a
clean-room reimplementation on ezdxf for Linux. The installed files are the
runtime source of truth.

## Purpose

Reconstruct an editable, validated 2D CAD drawing from one of three input
types, entirely on Linux with no AutoCAD and no Windows:

- **Mode A — source redraw**: a trustworthy DXF (or DWG) exists. Fingerprint
  it, rebuild it, and prove the rebuild with a fingerprint diff.
- **Mode B — PDF-to-DXF**: a PDF exists but no CAD source. Extract vector
  paths into an auditable intermediate DXF, labeled PDF-derived — never
  claimed as original-CAD-exact.
- **Mode C — image-to-CAD**: only a raster reference (photo, scan,
  screenshot). Build an evidence-aware spec, draw from it, and compare
  visually without ever asserting dimensional accuracy from pixels.

## Use this skill when

The user asks for a dwg redraw, to redraw dxf content, convert image to dxf,
pdf to dxf, raster to CAD, or to fingerprint and validate a drawing rebuild.
For 3D solids hand off to `the cad-generation-skill (load via skill tool)`;
this skill is 2D only. `the cad-dxf-skill (load via skill tool)` generates
new parametric drawings; this skill reconstructs existing ones.

## Non-negotiable rules

1. Resolve geometry in this order: explicit user requirements, readable
   dimensions, derived constraints, calibrated measurements, labeled visual
   estimates. Image pixels never override a written dimension.
2. Track every important value as `known`, `scaled`, `inferred`, or
   `unreadable`.
3. Visual similarity never proves dimensional accuracy. Comparison output is
   labeled "visual only".
4. Conflicting dimensions are never silently resolved: record the conflict
   and return `needs_review` or `blocked`.
5. Never overwrite the source file. Always write to a new output path.
6. PDF-derived and image-derived outputs are labeled as such. An intermediate
   is never presented as an exact original CAD source.

## Profiles

Choose by input quality; the profile sets the evidence bar:

- `strict-dimensioned`: engineering deliverable. Requires readable units and
  enough known/calibrated anchors to constrain the geometry; otherwise block.
- `general`: balanced default for plans, sketches, screenshots.
- `hybrid`: dimensions where available, calibrated proportions elsewhere,
  inferred geometry labeled.
- `visual-trace`: reproduce visible linework without asserting real-world
  scale.
- `geometry-only`: keep geometry and construction layers; omit dimensions,
  leaders, notes, table text.

No unit or scale anchor → choose `visual-trace` or a `unitless` spec. Never
default to millimeters because a drawing looks technical.

## Mode A — source redraw

1. **Fingerprint** the source:
   `python scripts/fingerprint.py --source input.dxf --output reports/input`
   (DWG input is converted first — see *DWG input/output*). Review the
   generated `<prefix>-redraw-prompt.md`: entity counts, layer table, block
   inventory, styles, annotation inventory, risk notes.
2. **Rebuild**: copy entities into a fresh document (ezdxf importer) or
   round-trip through the DXF converter; write to a new output path.
3. **Validate**:
   `python scripts/fingerprint_diff.py --source reports/input-fingerprint.json --target reports/output-fingerprint.json`
   Exit 0 required. Missing dimensions or leaders in the target when the
   source has them is a validation failure, not a warning.
4. **Preview and hand off** (see *Handoff*).

## Mode B — PDF-to-DXF

1. Inspect the PDF: page count, size, producer, extractable text, embedded
   raster, vector paths. Prefer vector extraction over raster tracing.
   `python scripts/pdf_vector_to_dxf.py --pdf input.pdf --output intermediate.dxf`
2. Raster or mixed pages become Mode C evidence at high DPI; text is written
   as real `TEXT`/`MTEXT` only when extractable — otherwise it stays traced
   geometry marked uncertain.
3. Label the intermediate PDF-derived, then run the full Mode A flow on it.
4. Report conversion limits: vector paths vs tracing vs OCR vs inference,
   unreadable text, approximate curves, scale assumptions.

## Mode C — image-to-CAD

1. **Preflight**:
   `python scripts/preflight_image.py --image input.jpg --mode general --output reports/preflight.json`
   A quality warning becomes a blocker only when the profile requires
   evidence the image cannot provide.
2. **Spec**: author `redraw-spec.json` per
   `references/redraw-spec.md` — stable entity IDs, views with independent
   calibration, evidence levels, constraints.
3. **Validate the spec**:
   `python scripts/spec_to_dxf.py --spec redraw-spec.json --check-only --report reports/spec-validation.json`
   Resolve all errors before drawing.
4. **Draw**:
   `python scripts/spec_to_dxf.py --spec redraw-spec.json --output outputs/redraw.dxf`
   (`--geometry-only` for the geometry-only profile.)
5. **Inspect and render**:
   `python scripts/render_preview.py --dxf outputs/redraw.dxf --png reports/preview.png`
6. **Compare**:
   `python scripts/compare_visual.py --source input.jpg --cad-preview reports/preview.png --anchors anchors.json --output-dir reports/comparison`
   Use the comparison to find omitted/shifted geometry — never to validate
   physical dimensions.
7. **Iterate**, then issue exactly one disposition per
   `references/validation.md`: `pass`, `pass_with_warnings`, `needs_review`,
   `blocked`, or `fail`.

## Validation contract

Deterministic checks over eyeballing: entity counts by type and space, layer
membership, closed flags on cut profiles, extents, and every dimension the
user supplied — via `fingerprint_diff.py` and ezdxf queries. The fingerprint
diff is reported even when it passes. Acceptance policies and dispositions:
`references/validation.md`.

## Handoff

After creating or modifying drawings, ALWAYS hand the explicit file path(s)
to `the cad-viewer-skill (load via skill tool)` when installed and include
its live viewer link(s) in the final response. If it is unavailable, report
that and rely on the deterministic checks instead of silently omitting the
handoff. Final responses include: generated files, viewer links, validation
actually run, evidence-level summary, assumptions, and the disposition.

## DWG input/output

DWG works as both input and output: input is read through the external
converter chain below; output is written by `scripts/to_dwg.py` when the ODA
File Converter is installed. `fingerprint.py` reads `.dwg` sources through
the external converter chain (ODA File Converter via `odafc`, then LibreDWG
`dwg2dxf`) with automatic fallback; see `references/linux-toolchain.md` for
install guidance, converter precedence, fidelity reporting, and the
degradation caveats (proxy objects, SHX text, annotative dimensions, dynamic
blocks). For DWG **output**, `scripts/to_dwg.py` converts a validated DXF to
DWG via the ODA File Converter (target version flag included) when ODA is
installed — DXF remains the default deliverable; produce and validate it
first, then run the writer when a DWG file is mandatory.

## Runtime requirements

Python 3.10+. Required: `ezdxf`. Optional (import-guarded with named install
hints): `odafc` + ODA File Converter or LibreDWG for DWG, `pillow`/`numpy`/
`opencv-python` for image preflight and comparison, `pymupdf` for PDF
extraction, `matplotlib` for preview rendering. Run scripts with the active
project Python from the workspace that owns the artifacts.
