---
name: cfd-validation
description: "Use when you must validate a computational fluid dynamics result against authoritative reference data: select the validation case for the flow regime and application (NACA 0012 or NACA 4412 airfoil, ONERA M6 transonic wing, DLR-F6 transport wing-body, flat plate boundary layer), compute the relative error, RMS error and max local error, run a Richardson extrapolation grid convergence check, judge pass or fail against tolerance bands, and estimate validation uncertainty. Produces the validation verdict and a validation report skeleton. Trigger: cfd validation, validation case selection, richardson extrapolation, grid convergence, naca 0012 drag, onera m6, dlr f6, error metrics, validation uncertainty, validation report."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: naca-tr-824
    reference-only: true
gated: false
domain: aerodynamics
pack: cfd
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: aerodynamics
  subdomain: cfd
  tags: [cfd-validation, verification-validation, richardson-extrapolation, grid-convergence, error-metrics, naca-0012, naca-4412, onera-m6, dlr-f6, validation-uncertainty, boundary-layer]
  version: 0.1.0
  author: Aero Agent Skills
---

# CFD Validation (aerodynamics/cfd/cfd-validation)

Use when a CFD result must be judged against authoritative reference data
before it can be trusted: which reference case to run, which comparison
metrics to use, whether the agreement is within the acceptance band, and
how to report it. Follows AIAA G-077-1998 (Guide for the Verification and
Validation of CFD Simulations) and ASME V&V 20-2009 (Standard for
Verification and Validation in CFD and Heat Transfer); see
references/vv-guidance.md.

## Domain quick reference

- Verification solves the equations right (code and discretization
  errors); validation solves the right equations (model vs physical
  reality). This skill covers validation; pair it with cfd-convergence for
  residual and mesh checks.
- Validation compares computed quantities against reference data of known
  quality and states PASS or FAIL within a tolerance band. It never proves
  a code, it bounds it for a stated application and condition range.
- Case selection by flow regime and application (implemented in
  select_validation_case):

| Flow regime | Application | Reference case | Key reference values |
|---|---|---|---|
| incompressible | airfoil | NACA 0012 (alt: NACA 4412) | Cd 0.0081 at M 0.30, Re 6e6 (NACA TR 824) |
| transonic | wing | ONERA M6 | CL 0.266, CD 0.0163 at M 0.84, Re 11.72e6, alpha 3.06 deg (AGARD-AR-138) |
| transonic / transport | wing-body | DLR-F6 | CD ~ 0.0299 at CL 0.5, M 0.75, Re 3e6 (AIAA Drag Prediction Workshop) |
| incompressible | flat plate | ZPG flat plate | Cf = 1.328/sqrt(Rex) laminar (Blasius), Cf = 0.074/Rex^0.2 turbulent (Schlichting) |

- Comparison metrics: relative_error for integrated quantities (Cd, Cl);
  rms_error and max_error for distributed quantities (Cp, Cf, u profiles).
- Richardson extrapolation on 3 meshes gives the apparent order p and an
  infinite-grid estimate; the Roache grid convergence index (GCI, safety
  factor 1.25) is the discretization uncertainty on the finest mesh.
- Typical acceptance bands: section drag within 5% of reference, wing-body
  drag within 10% (DPW participant scatter is of this order), Cp within
  0.02 or 5% of local magnitude. State the band before judging.
- Validation uncertainty U_val combines the identified error sources
  (discretization, modeling, numerical, experimental) in quadrature.

## Workflow

1. Select the reference case with
   select_validation_case(flow_regime, application), e.g.
   ("incompressible", "airfoil") -> NACA 0012.
2. Run the CFD analysis on at least three mesh levels and extract the
   quantities of interest at the documented conditions.
3. Compute relative_error on integrated quantities and rms_error plus
   max_error on distributed quantities against the reference.
4. Run richardson_extrapolation on the 3 mesh values; a monotone sequence
   with positive apparent order is required for a sane grid convergence
   statement.
5. Judge with validation_verdict(computed, reference, tolerance); drag
   within 5% of the reference is the default band for section cases.
6. List the error sources and combine them with
   validation_uncertainty(sources) into U_val.
7. Assemble the report with report_skeleton(case, metrics, verdict,
   uncertainty).

## Worked example

NACA 0012 at M 0.30, Re 6e6, alpha 0 deg. Reference Cd 0.0081 (NACA TR
824 classic data).

- Computed Cd 0.0085: relative_error = 0.0004/0.0081 = 0.0494, under the
  5% band. validation_verdict(0.0085, 0.0081, 0.05) -> PASS.
- Computed Cd 0.010: relative_error = 0.2346, over the 5% band.
  validation_verdict(0.010, 0.0081, 0.05) -> FAIL.
- Grid convergence: values [0.0085, 0.0090, 0.0100] on meshes refined by
  r = 2 give apparent order p = 1.0, extrapolated Cd 0.0080, GCI 0.000625.
  The extrapolated value is closer to the reference than the finest mesh
  value, which supports the 5% PASS.
- Uncertainty: sources discretization 0.0002, modeling 0.0003, numerical
  0.0001 combine to U_val = 0.000374, dominated by modeling. The verdict
  band is wider than U_val, so the PASS is robust.

## Pitfalls

- Calling a code validated because one case passes: validation never
  proves a code, it bounds it for a stated application and condition
  range - the verdict from validation_verdict belongs to the case, the
  band, and the flow regime that was run, and a clean residual
  (cfd-convergence) does not make a 23% drag error acceptable.
- Selecting the reference case by convenience instead of regime: the
  incompressible NACA 0012, transonic ONERA M6 and DLR-F6 cases each
  anchor one flow regime and application, so comparing a transonic
  wing-body run against the NACA 0012 Cd band is meaningless.
- Choosing the acceptance band after seeing the error: the 5% section /
  10% wing-body / 0.02 Cp bands are documented typicals that must be
  stated before the comparison, not tuned to force a PASS.
- Using the wrong metric for the quantity: relative_error is for
  integrated quantities (Cd, Cl) while distributed quantities (Cp, Cf,
  u profiles) need rms_error and max_error - a single-point Cp relative
  error hides the profile mismatch.
- Running Richardson extrapolation on a non-monotone mesh sequence:
  three mesh values with no clear trend or a non-positive apparent
  order give no sane grid-convergence statement, so the GCI on the
  finest mesh is not trustworthy.
- Reporting a verdict whose band is narrower than the uncertainty: when
  U_val (0.000374 in the worked example) approaches the tolerance band,
  the PASS is not robust - widen the band or reduce the dominant error
  source before claiming validation.

## Behavior contract (gate 3)

The behavior contract is scripts/test_cfd_validation.py against
scripts/cfd_validation_logic.py (stdlib unittest, offline, deterministic).
Run:

python3 scripts/test_cfd_validation.py

It asserts: NACA 0012 Cd reference 0.0081 at M 0.3 Re 6e6; computed Cd
0.0085 passes the 5% band; computed Cd 0.010 fails; Richardson
extrapolation on 3 meshes yields a sensible extrapolated value (closer to
the reference than the finest mesh); every invalid input raises ValueError.

## References

- references/vv-guidance.md: AIAA G-077-1998 and ASME V&V 20-2009
  summary, case data sources, acceptance-band guidance.
- scripts/cfd_validation_logic.py: the logic module (pure Python, stdlib
  only).
- scripts/test_cfd_validation.py: the behavior contract test.

## Related skills

- cfd-convergence: residual, CFL and mesh refinement verification
  (the verification half of V&V).
- cfd-turbulence-modeling: model choice feeds the modeling uncertainty
  term of U_val.
- cfd-mesh-generation: mesh quality feeds the discretization uncertainty
  term.
- xfoil-analysis: section polars validated against NACA TR 824 data.
- boundary-layer-theory: flat plate skin friction anchors the
  zero-pressure-gradient boundary layer case.

## Compliance

- NACA TR 824 is US government work (public domain); summary and physics
  values only, per standards-map.yaml.
- AIAA G-077-1998 and ASME V&V 20-2009 are referenced as guidance;
  paraphrased summary only in references/vv-guidance.md.
- compliance: STANDARDS-REF, gated: false.
