---
name: calculix-linear
description: "Use when running or checking linear static finite element analysis for aircraft structure with CalculiX (ccx): determine margin of safety from allowables versus FEA stresses, validate unit discipline before post-processing, and check von Mises stress results. The skill covers element-basis stress checks, margin computation, and unit conversion discipline so that allowables and computed stresses are compared in consistent units. Trigger: finite element, fea, calculix, ccx, stress analysis, margin of safety, von mises, unit discipline, static analysis."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: far-25
    reference-only: true
gated: false
domain: structures
pack: structures
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: structures
  subdomain: fem
  tags: [finite-element, fea, calculix, ccx, stress-analysis, margin-of-safety, von-mises, unit-discipline, static-analysis]
  version: 0.1.0
  author: Aero Agent Skills
---

# CalculiX Linear Static FEA (structures/fem/calculix-linear)

Use when the task is linear static finite element analysis of
aircraft structure with CalculiX (ccx): stress post-processing,
margin of safety checks against material allowables, and unit
discipline across the analysis chain.

## Domain quick reference

- Margin of safety: MS = allowable / actual - 1.0; a negative MS
  means the structure fails at the applied load.
- Von Mises equivalent stress: sqrt(0.5*((s1-s2)^2 + (s2-s3)^2
  + (s3-s1)^2)); compare it against allowables for ductile metals.
- Unit discipline: allowables and FEA stresses must be compared in
  the same unit. Conversion factors to Pa: kPa 1e3, MPa 1e6, GPa
  1e9, psi 6894.757, ksi 6894757.0.
- FAR-25 structure requirements (25.301-25.307 loads and
  structural proof) set the certification context for the stress
  checks; this skill computes the checks, not the loads.

## Workflow

1. Confirm the analysis is linear static (small displacements,
   linear materials) and record the unit convention of the ccx run.
2. Extract stresses at the element or node of interest from the
   ccx output; record the unit.
3. Convert the FEA stress and the allowable to a common unit with
   stress_to_pa / mos_units_discipline.
4. Compute margin of safety with margin_of_safety and classify
   with mos_status; negative margin = failed structure.
5. Check equivalent stress with von_mises where a scalar
   comparison is needed.
6. Confirm the deterministic checks with the contract test
   scripts/test_calculix.py.

## Pitfalls

- Comparing allowables and FEA stresses in different units
  (silent unit errors); always convert through Pa.
- Treating a negative margin of safety as acceptable; it means the
  applied stress exceeds the allowable.
- Using von Mises for brittle or directionally dependent
  materials without justification.
- Applying linear-static checks to nonlinear or buckling-dominated
  responses.

## Behavior contract (gate 3)

The margin, unit, and von Mises logic is exercised by the gate 3
contract test: scripts/test_calculix.py against
scripts/calculix_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_calculix.py

## Compliance

- Standards referenced, not reproduced: FAR-25 is US government
  work (public domain); summary-only per standards-map.yaml and
  brief 06.
- compliance: STANDARDS-REF, gated: false.
