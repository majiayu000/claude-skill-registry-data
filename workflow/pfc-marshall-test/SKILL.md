---
name: pfc-marshall-test
description: Adapt and audit a PFC 5.0 asphalt Marshall stability/flow simulation using the external fistPkg26 dc.fis two-head controller as a starting skeleton; use for curved-head geometry, PFC5 wall/contact kinematics, load-deformation histories, peak stability, edition-specific flow processing, and validation against laboratory data.
---

# PFC5 Marshall Stability and Flow

Use this skill after a load-ready specimen exists. The PFC5 fistPkg `dc.fis`
controller can provide a two-head setup/loading skeleton, but Marshall is not converted
into a validated test merely by replacing planar platens, and it must not be interpreted
as a Brazilian tensile-strength calculation.

## When to use

- create or audit curved Marshall loading heads in PFC5;
- adapt a private fistPkg26 DiamCompTest working copy;
- extract load-deformation histories, peak load and edition-correct flow;
- compare PFC results against a laboratory Marshall test;
- diagnose wall IDs, axes, sign, head contact, smoothing or stopping logic.

Use `pfc-asphalt-mixture` for specimen generation and `pfc5-asphalt-workflow` for the
complete case.

## Required inputs

- PFC2D/PFC3D 5.0 and the unit system;
- legal `<FISTPKG_ROOT>` plus a passing dependency check/baseline run;
- governing standard edition, method ID and clauses;
- specimen dimensions, conditioning and test temperature;
- head geometry/radius/width and PFC5-compatible wall representation;
- prescribed loading rate/control mode and stop condition;
- head-particle contact properties and friction;
- definition/correction procedure for stability and flow;
- laboratory curve/targets, tolerances and desired crack/failure outputs.

For current work use JTG 3410-2025 T 0709-2025, effective 2025-10-01, and trace the
specimen to the selected T 0702-2025 forming route. JTG E20-2011 T0709 is retained only
for declared legacy reproduction. Do not mix current curve correction/reporting rules
with legacy apparatus or conditioning values.

## Audited fistPkg26 contract

The inspected `dc.fis`:

- calls `_dcMakeWalls` during `dcSetupPhase`;
- expects head pointers `dcWp0` and `dcWp1`, normally found from wall IDs 1 and 2;
- uses the second coordinate as axial position/velocity;
- initializes wall-force and wall-strain callbacks;
- can stop after force falls to a fraction of the recorded peak.

`_dcMakeWalls` is the minimum geometry hook. A complete adapter must also verify:

1. wall IDs/pointers and head initial gap;
2. curved-facet orientation, head translation and prohibited rotations;
3. PFC5 wall import/generation syntax;
4. current and future grain-head contact laws;
5. suitability of `ft_SmoothGrainWallInterface`;
6. force, displacement and sign conventions in 2D/3D;
7. peak capture, sampling rate and post-peak termination;
8. edition-specific flow correction and unit conversion.

## Workflow

1. Run the unmodified fistPkg DiamCompTest baseline in a PFC5.0 runtime.
2. Copy the project privately and preserve an upstream/change manifest.
3. Replace the planar-head construction through a separately documented override.
4. Run a no-particle/head-motion probe, then a small-particle contact probe.
5. Install the actual specimen, remove unintended overlap without altering the intended
   fabric, equilibrate and save the pre-load state.
6. Initialize independent reaction-force and head-separation/displacement histories.
   PFC5 `wall.force.contact` is the global-coordinate sum of contact forces acting on
   each wall; keep both heads and verify their equal/opposite balance before deriving
   a scalar load. Set a displacement reference explicitly because `wall.disp` is an
   accumulated wall displacement and is writable.
7. Load at the edition-specific rate; retain enough post-peak data for the selected stop
   and flow procedure.
8. Preserve the raw curve, apply the selected edition's origin correction, and branch
   explicitly when the peak is not obvious; never replace the current correction with
   raw peak displacement or a fixed post-peak fraction.
9. Compare the full curve, peak/flow and failure pattern against laboratory data and run
   seed/resolution/rate sensitivity.

## Working rules

- Keep all case commands PFC5-pure; newer geometry/FISH syntax requires an explicit port.
- Do not claim `dc_wfa`/`dc_wda` automatically equal final normative stability/flow;
  independently audit sign, units, sampling and correction.
- Do not add the signed forces from two opposed heads and call the cancellation a
  specimen load. Resolve both forces on the declared loading axis, compare magnitudes,
  and state the scalar-load convention.
- Treat dry stability, immersed stability and vacuum-saturation stability as distinct
  protocols. A dry DEM solve cannot be relabeled as water sensitivity.
- Do not claim that `_dcMakeWalls` is the only required change.
- Keep setup, equilibrated pre-load and loaded milestone saves.
- If the standard text or runtime is unavailable, deliver the raw curve and mark the
  normative result/runtime gate pending.

## Output contract

- PFC2D/PFC3D 5.0, units, standard edition/method/clause and source manifest;
- specimen/head geometry and audited PFC5 head construction;
- wall/contact/control/stop parameter tables;
- baseline, no-particle and contact-probe results;
- load-deformation history, raw peak load/displacement and standard-corrected metrics;
- equilibrium and sensitivity evidence;
- laboratory validation and `runtime_validated` status.

## Local contents

- `references/overview.md` — legacy fistPkg dc.fis parameters and adapter notes.
- `references/jtg-t0709-note.md` — legacy 2011 checklist; not a current numeric source.
- `references/jtg-3410-2025-t0709.md` — current method chain, raw/corrected curve contract and PFC5 mapping.
- `../pfc5-asphalt-workflow/references/standards-policy.md` — current/legacy policy.
- `scripts/marshall_head_contact_pilot.p3dat` — executable curved-head PFC3D 5.0 contact pilot; not a normative Marshall model.
- `dependencies.json` — package-level sibling-skill assets required for the complete workflow.
- `agents/openai.yaml` — Agent metadata.
