---
name: dual-color-live-imaging
description: Audit and analyze two-channel fluorescence time-lapse microscopy of elongated structures, including calibrated CZI/OME-TIFF inputs, registration QC, puncta matching, explicit spatial null models, stationary-site persistence, kymographs, and descriptive onset order. Use when reviewing live-imaging claims about colocalization, temporal order, or transport; distinguish measurements from biological inference.
license: MIT
metadata:
  version: "1.0.0"
---

# Dual-color live imaging

Read [the methodology and limits](references/methodology.md) before interpreting results. For installation, CLI options and output definitions, see [usage](references/usage.md). The scripts support exploratory analysis of elongated structures, not every microscopy assay.

The Python tools require Python 3.12+ and the dependencies in the bundled `requirements.txt`. Install them into a dedicated environment before execution. Tested versions are pinned; standalone scripts do not use an AI API key.

## Establish the experiment

Identify the question, channel identities, acquisition sequence, detector range, controls, XY/Z calibration, actual frame times, independent biological units and intended regions. Inspect representative raw frames before choosing segmentation or matching parameters. Do not infer physical units from array dimensions or invent missing metadata.

Use CZI, TIFF or OME-TIFF. Arrays are normalized to `TCZYX` using labeled axes. Unsupported non-singleton scene/sample axes require an explicit export of one scene; do not silently flatten them. Square XY pixels are required. A single Z plane is analyzed in 2D. Metadata overrides require verified acquisition records and are saved in the results.

Start with `scripts/audit_acquisition.py`. Check saturation, drift, intensity changes, common field of view and channel registration. Image-derived channel offsets are diagnostics: independent bead calibration is needed to separate chromatic misregistration from biology. For sequential channel/Z acquisition, inspect channel/plane timing separately before interpreting short delays; a shared frame timestamp cannot correct those delays.

## Analyze and inspect

1. Use `scripts/run_pipeline.py` with explicit channel indices and a fresh output directory. Specify physically justified segmentation, peak separation and matching tolerances. The default segmentation favors elongated structures; `--structure any` only relaxes shape rejection and still uses a tubular-response mask.
2. Inspect retained masks, excluded regions and detection overlays or coordinates. The automatically excluded area is candidate background, not verified cell-free background. If unsuitable, stop and revise the assay/export/ROIs rather than treating generated counts as valid.
3. Keep bleaching correction opt-in. Increasing intensity, recruitment and changing focus can be flattened by a multiplicative correction. Independently calibrated B-channel shifts use `--channel-shift-px DY DX`; do not automatically align different biological labels to maximize overlap.
4. Report both channel-specific matched fractions and the paired fraction with its denominator. The maximum-cardinality assignment is one-to-one. Run the seeded uniform-mask spatial null only as the hypothesis actually implemented, and evaluate alternative nulls where density, clustering or geometry matter.
5. Use `scripts/run_onset_order.py` for detected onset, per-frame count matching and all-frame raw half-range crossings at detection-selected sites. Inspect censoring, intensity traces, noise, spatial site merges and timestamp resolution. These descriptive checks do not establish recruitment or resolve selection bias.
6. Generate PNG/PDF figures with `scripts/make_report_figures.py`. Review them against raw data. Kymograph distances follow an estimated skeleton path, and times follow actual frame timestamps. The two channels have independent display contrast.

## Bound the conclusions

- Colocalization at optical resolution does not establish molecular interaction. Ratio strata are relative intensity groups, not single-label controls or evidence of cell identity.
- Tracking uses a conservative stationary-site heuristic. First-to-last observed spans can include a missed frame and are censored at recording boundaries; they are not kinetic lifetimes.
- Along-path cross-correlation measures profile shift, not verified cargo speed. Positive displacement follows the estimated root-to-tip direction, whose root is geometric rather than biologically established.
- Sites, branches and frames within a recording are nested observations. Report independent biological replicates and use an appropriate hierarchical or replicate-level analysis before inferential claims. Do not add significance stars from site-level counts.
- Archive parameters, calibration provenance, actual times, software versions, exclusions and manual review decisions. Generated reports are descriptive and need experiment-specific validation.

The bundled synthetic-data generator exercises the software without using experimental data. Passing it establishes execution and basic invariants, not scientific accuracy on an unseen assay.
