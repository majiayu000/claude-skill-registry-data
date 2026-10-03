---
name: pfc-rutting-test
description: Design, implement, and audit PFC3D 5.0 asphalt wheel-tracking and intersection-rutting simulations using RVE-to-strip-to-full-size scaling, PFC5-compatible vector reaction control, Burger-calibrated contacts, vertical-horizontal coupled loads, rut/shear histories, edition-specific metrics, and explicit surrogate validation.
---

# PFC5 Wheel-Tracking and Rutting Test

Use this skill after specimen generation and Burger calibration. Prefer PFC3D because
wheel width, lateral confinement, contact patch and rut geometry are intrinsically
three-dimensional.

## When to use

- plan a wheel-tracking/rutting model in PFC 5.0;
- choose a moving, rolling-faceted or fixed equivalent cyclic load;
- servo a wall/head to a target reaction rather than assign a read-only contact force;
- extract rut-depth histories and an edition-specific dynamic-stability metric;
- scale an RVE to a strip/pilot and then a full-size slab.
- study braking/acceleration with vertical-horizontal coupled loading, asymmetric
  deformation, particle migration or shear-stress depth profiles;
- audit an equivalent fixed patch or accelerated-time route against an unaccelerated
  moving-load pilot.

Do not use this skill for Marshall or for specimen generation.

## Required inputs

- exact PFC3D 5.0 build, units and runtime budget;
- governing standard edition, method ID, clauses and machine/specimen coefficients;
- slab, mold, wheel and travel geometry;
- conditioning/test temperature;
- wheel motion definition and whether “count” means one-way pass or complete cycle;
- physical load waveform/frequency/rest history and every step used to replace it with
  a moving, cyclic or constant equivalent route;
- prescribed pressure/load and the physical/equivalent contact-area definition;
- vertical and horizontal load-control implementation, coordinate/sign convention,
  target vector-reaction ratio and tolerances;
- source and meaning of any `F_h/F_v` or friction-demand factor, kept separate from
  wheel-contact and material-contact friction coefficients;
- lateral/front/back boundary conditions and the planned free-versus-confined
  sensitivity comparison;
- load-ready specimen plus calibrated contact parameters;
- rut-depth measurement region/reference and stop condition;
- laboratory rut curve/dynamic-stability targets.

The current reviewed route is JTG 3410-2025 T 0719-2025, effective 2025-10-01.
JTG E20-2011 T0719 is a legacy route and must not supply current default dimensions,
time windows or coefficients.

## Modeling hierarchy

1. **RVE/material check** — calibrate creep/recovery and timestep sensitivity.
2. **Strip/pilot model** — verify boundaries, contact patch, load servo, wheel motion,
   rut measurement and computational cost.
3. **Full-size model** — use only after the first two gates pass.

The exact dimensions and test values come from the selected standard edition or
laboratory protocol, not from a remembered default.

## Loading routes

| Route | Meaning | Acceptance gate |
| --- | --- | --- |
| moving faceted wheel/head | translation over slab | reaction and footprint match target throughout travel |
| rolling faceted wheel | translation plus angular velocity | kinematic sign, slip and facet-resolution sensitivity |
| fixed wall with facet conveyor | fictitious surface conveyance without moving facets | label as conveyor surrogate; validate against moving/rolling footprint and reaction |
| fixed equivalent cyclic patch | accelerated surrogate | correlation to moving-wheel pilot; never label as normative motion |
| fixed equivalent constant patch | creep-oriented accelerated surrogate | preserve declared impulse/dwell or constitutive invariants and pass an unaccelerated comparison |
| vertical-horizontal coupled head | intersection braking/acceleration surrogate | both reaction components, slip/work, direction reversal and boundary sensitivity pass |

In PFC5, contact force is normally an observed reaction. Apply load by a verified servo
or velocity/position control and demonstrate that the reaction meets the target.
Pressure-to-force conversion requires a declared reference area; the evolving DEM
contact area is not automatically that area.

## Workflow

1. Freeze standard edition, physical parameters and numerical equivalents separately.
2. Restore the load-ready specimen, audit boundaries/contact groups and equilibrate.
3. Build and motion-test the wheel/head with no specimen.
   For a rolling wall, PFC5 translational velocity and angular `spin` are different
   attributes; set the center of rotation on the wheel axis and verify
   `|v| = |omega| R` plus the sign at the contact point. The default rotation center is
   the global origin, so relying on it is unsafe for an offset wheel.
4. Run a small contact/load-servo probe; quantify reaction error and oscillation.
5. Run the strip pilot for a short declared number of cycles/passes.
6. Establish a vertical-only baseline. For an intersection route, add positive and
   negative horizontal cases and verify both reaction components before interpreting
   asymmetric deformation.
7. Record wheel position, commanded motion, vertical/horizontal reactions, reference
   surface, rut depth,
   the seven fixed-position measurements or an approved equivalent, timestep,
   equilibrium/inertia indicators, one-way pass count and round-trip count.
8. If time is compressed, compare `lambda=1` and every candidate scale on a small model;
   audit rut, recovery, contact state and energy, not only the final displacement.
9. For coupled loading, export forward/reverse-face deformation, lateral heave,
   phase-separated particle displacement and a tensor-defined shear-depth profile.
10. Confirm no wall penetration, particle escape, axis/sign error or callback duplication.
11. Run the production duration with restart saves.
12. Compute the standard metric only from the selected edition's formula, intervals and
   coefficients; otherwise report the raw rut history with the metric pending.
13. Compare against laboratory curves and run seed/resolution/rate/load-route,
    contact-mixture, thickness and boundary sensitivity.

## Working rules

- Keep PFC5 command/FISH syntax version-pure.
- Do not set `wall.force` as if it were a prescribed actuator without proof from the
  exact PFC5 API; use a verified motion/servo controller.
- Do not assume a rectangular patch, accelerated cycle or fixed load is equivalent to a
  moving rubber wheel. Calibrate and label the surrogate.
- Do not call translation-only motion “rolling.” A rolling wall needs verified spin,
  axis/center of rotation and no-slip sign; a facet conveyor is another distinct
  surrogate because it changes contact relative velocity without moving the facets.
- Do not call a fixed constant patch a dynamic load merely because its duration came
  from a wheel-pass calculation. State which physical quantities the mapping preserves
  and which it discards.
- `F_h = mu F_v` may define an external braking/acceleration demand, but that `mu` is
  not automatically a DEM contact friction coefficient. Verify commanded and measured
  vector reactions, slip and work independently.
- A free horizontal outlet can exaggerate material migration; a fully fixed boundary
  can suppress it. Report at least one free/confined sensitivity pair before field
  interpretation.
- A measure-region “shear stress” is incomplete without tensor component, axes, sign,
  radius/volume weighting, overlap, sample time and empty-region handling.
- Published strip dimensions, load levels, contact fractions, friction-demand factors
  and `lambda` values are case evidence, not package defaults.
- For T 0719-2025, compute DS from the current method's pass-count interval and width
  coefficient. Do not use the legacy `45 min/60 min` shorthand or an unverified extra
  correction coefficient.
- Preserve RVE, strip, pre-load, pilot and production milestone saves.
- Full-size output without pilot load-control evidence is not validated.

## Output contract

- PFC build/units and standard edition/method/clause;
- physical versus DEM-equivalent parameter table;
- specimen/wheel/boundary/contact assignment;
- actuator/servo pseudocode or PFC5-verified code plus reaction-error history;
- physical-to-DEM load/time equivalence ledger and accelerated-versus-unaccelerated
  comparison;
- rut-depth measurement definition and raw time/pass/cycle history;
- vertical/horizontal command and reaction histories, face-asymmetry/lateral-heave
  metrics, particle displacement fields and tensor-defined shear-depth profiles;
- edition-correct metric calculation with units/coefficients, or pending status;
- RVE/strip/full-size stage evidence and sensitivity results;
- laboratory comparison and `runtime_validated` status.

## Local contents

- `references/overview.md` — current T 0719-2025 measurement, count and PFC3D mapping.
- `references/jtg-t0719.md` — current-version gate, user-input template and symbolic metric; no standard data tables.
- `references/modeling-strategy.md` — PFC5-safe hierarchy and controller pseudocode.
- `../pfc5-asphalt-workflow/references/intersection-rutting-research-evidence.md` —
  external-paper evidence and non-default boundaries for mixed contacts, time
  compression and vertical-horizontal loading.
- `../pfc5-asphalt-workflow/references/standards-policy.md` — standards policy.
- `scripts/rutting_contact_pilot.p3dat` — executable curved-wheel PFC3D 5.0 contact/translation pilot; not a normative wheel-tracking model.
- `dependencies.json` — package-level sibling-skill assets required for the complete workflow.
- `agents/openai.yaml` — Agent metadata.
