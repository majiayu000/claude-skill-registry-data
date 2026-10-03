---
name: pfc-postprocessing
description: Post-process PFC 5.0 asphalt CSV and image exports into reproducible curves, fields, rose diagrams, animations, and summary tables without relying on a local PFC installation.
---

# PFC 5 Asphalt Post-processing

Use this skill after a PFC 5.0 asphalt run has exported CSV data or ordered image frames. It is intentionally file-based: no newer-version object API or saved-state bridge is bundled.

## When To Use

- plot stress-strain, Marshall load-flow, creep/recovery, or rut-depth curves;
- audit intersection-rutting time maps, vertical/horizontal reaction tracking,
  face-deformation asymmetry, lateral heave and shear-depth profiles;
- render displacement, velocity, stress, or porosity fields;
- draw fracture/contact orientation rose diagrams;
- order exported PNG frames and assemble GIF/MP4 animations;
- convert the bundled legacy text exports into stable CSV contracts;
- generate summary tables and publication-ready figures.

Use `pfc-vedo-postprocess` for 3D particle/force-chain scenes. Return physical interpretation and acceptance decisions to `pfc5-asphalt-workflow`.

## Required Inputs

- case/test name, PFC2D/PFC3D 5.0, units, and stage;
- actual exported files and column meanings;
- requested plots/tables and output formats;
- sign conventions, coordinate scaling, and any smoothing/transformation rule;
- standard edition if a normative test metric is requested.
- for a surrogate rutting case, the signed coordinate/tensor convention, physical-to-
  solver time map, reaction commands, boundary case and measure-region definition.

## Script-First Workflow

1. Read `references/script-catalog.md` and the selected script.
2. Validate inputs against `references/data-contract.md`.
3. Preserve raw values; write transformed values to separate columns and disclose the rule.
4. Run the smallest matching script before adapting it.
5. Save source data, figure outputs, summary tables, and the exact command.
6. Confirm units, peak/rut/flow calculation, frame order, and file existence.

## Router

| Need | Script |
| --- | --- |
| global curve and peak summary | `scripts/plot_curves.py` |
| rut/time/vector-reaction/asymmetry/shear evidence | `scripts/plot_rutting_evidence.py` |
| particle/stress/porosity fields | `scripts/plot_fields.py` |
| orientation rose diagram | `scripts/plot_rose.py` |
| normalize image-frame order | `scripts/export_animation_frames.py` |
| build GIF/MP4 | `scripts/export_animation.py` |
| legacy ball/contact text to CSV | `scripts/convert_legacy_*_export.py` |
| public smoke test | `scripts/run_demo.py` |

The public demo uses deterministic CSV files under `examples/minimal_case/data/` and does not require PFC:

```bash
python scripts/run_demo.py
```

Validate only the bundled inputs when plotting dependencies are unavailable:

```bash
python scripts/run_demo.py --check-only
```

## Working Rules

- Do not infer missing columns or units silently.
- Do not derive normative Marshall/车辙 metrics without the selected standard formula and coefficients.
- Do not replace equivalent physical time with solver time or solver cycles. Preserve
  all three columns and the declared `lambda` convention.
- Keep vertical/horizontal command and signed reaction separate. A friction-demand
  ratio, contact friction and measured reaction ratio are different quantities.
- A shear profile must retain tensor component, axes/sign, measure radius, weighting,
  overlap and sampling state; do not plot an undefined absolute “shear stress”.
- Keep seven-position/approved normative deformation separate from deepest rut,
  face asymmetry and lateral-heave diagnostics.
- Keep global color limits fixed across animation frames.
- Treat screenshots as presentation outputs, not numerical source data.
- Keep output directories user-selected for production work; the demo alone may recreate its own `examples/demo_outputs/`.

## Output Contract

Deliver the input manifest, units/sign conventions, command used, source/transformation table, requested figures/animations, metric summary, and any pending physical or standard-validation gate.

## Local Contents

- `references/data-contract.md` — stable CSV contracts.
- `references/script-catalog.md` — executable route map.
- `references/animation-workflow.md` — frame ordering and animation rules.
- `examples/minimal_case/data/` — deterministic public demo data.
- `scripts/` — executable post-processing tools.
- `LICENSE` and `NOTICE.md` — retained MIT terms and upstream provenance.
