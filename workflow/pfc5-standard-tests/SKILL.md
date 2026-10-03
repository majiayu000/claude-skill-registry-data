---
name: pfc5-standard-tests
description: Plan, audit, and post-process PFC 5.0 asphalt calibration tests, including compression, diametral loading, direct tension, creep-recovery, test geometry, histories, peak metrics, stiffness, and fistPkg handoff.
---

# PFC5 Standard Tests

Use this skill for PFC5 material/calibration tests that support asphalt specimen
and contact-model validation. Prefer the legal external fistPkg baseline when its
test family fits.

## Required Inputs

- PFC2D/PFC3D 5.0, units and sign convention;
- test type, geometry, boundary/contact assumptions and the complete standard method
  chain, including specimen forming, density/void method and performance method;
- load/displacement/rate/hold/recovery path;
- required stress/strain definitions and experimental targets;
- external fistPkg root when used.

## Workflow

1. Select compression, diametral, direct tension, or creep-recovery.
   For JTG 3410-2025 work, distinguish T 0713/T 0714 compression, T 0738 dynamic
   modulus, T 0742 shear, T 0715 flexure, T 0716 splitting and T 0745 repeated
   compression; do not infer one test from a generic controller name.
2. Run the unmodified external fistPkg baseline when applicable.
3. Prove boundary motion, wall IDs, axes and sign with a small pilot.
4. Initialize duplicate force/displacement measures and histories before loading.
5. Retain pre-load, peak/hold and final/recovery states.
6. Export a stable CSV and run `scripts/extract_test_metrics.py`.
7. Compare the full curve and failure/deformation mode, not peak alone.
8. Run seed, resolution, rate, timestep and boundary sensitivity.

Read [test-contracts.md](references/test-contracts.md) for measurement contracts.

## Working Rules

- Marshall remains in `pfc-marshall-test`; wheel tracking remains in `pfc-rutting-test`.
- Do not call a diametral controller a Marshall model without the Marshall geometry and metric contract.
- Test formulas require declared dimensional thickness/area conventions.
- The laboratory-method value, project acceptance threshold and DEM calibration target
  are separate records even when they share a symbol.
- Offline metric extraction does not validate the PFC solve.

## Output Contract

Return test definition, geometry/boundaries, histories, CSV schema, extracted
metrics, experimental comparison, sensitivity evidence and runtime status.

## Local Contents

- `references/test-contracts.md` — PFC5 calibration-test contracts.
- `../pfc5-asphalt-workflow/references/standards-method-map.md` — method-chain and standard-role routing.
- `scripts/extract_test_metrics.py` — deterministic curve/peak/stiffness extractor.
- `agents/openai.yaml` — interface metadata.
