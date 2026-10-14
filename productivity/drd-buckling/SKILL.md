---
name: drd-buckling
description: "Use when determine the structural buckling capacity of load-bearing members for an ECSS-E-ST-32C Annex M buckling report: categorize each member by geometry (column, flat plate, or shell), resolve the effective length factor from its boundary conditions, compute the critical buckling stress using the Euler formula for slender columns or the Johnson parabolic formula for intermediate columns, apply a knock-down factor for initial geometric imperfections, evaluate the margin of safety against the applied compressive stress, and confirm that every member achieves a non-negative margin of safety. Trigger: ecss, e-st-32c, buckling, column-buckling, plate-buckling, euler, johnson, knock-down, margin-of-safety, structural-report."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: ecss
    reference-only: true
gated: false
domain: space-systems
pack: space-systems
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: space-systems
  subdomain: ecss
  tags: [ecss, e-st-32c, e-st-32-structures-scope, buckling, column-buckling, plate-buckling, knock-down, margin-of-safety]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Structures — Structural Buckling Report (space-systems/ecss/drd-buckling)

Use when the task is preparing or verifying the structural buckling report
required by ECSS-E-ST-32C Annex M — categorizing every load-bearing member by
geometry, computing its critical buckling stress with the appropriate formula,
applying knock-down factors for imperfections, and confirming a non-negative
margin of safety for each member.

## Domain quick reference

- Annex M of ECSS-E-ST-32C defines the content and analysis procedure for
  the structural buckling report (SB report). Each structural member must be
  categorized into one of three geometry families before its buckling capacity
  is assessed: **column** (bar or strut in pure axial compression), **flat
  plate** (thin sheet element under in-plane compressive or shear load), or
  **shell** (curved panel or cylinder under axial, bending, or lateral
  pressure). Members that do not fit one of these three families require an
  explicit justification in the report before a custom buckling model is
  applied.

- For **column members**, the analysis selects between two stress formulae
  depending on the slenderness ratio KL/r:
  - *Euler range* (long, slender columns): critical stress is proportional to
    E/(KL/r)², governed by elastic instability.
  - *Johnson range* (intermediate columns): critical stress is reduced
    parabolically below the yield stress, accounting for the interaction
    between material yielding and elastic buckling. The transition slenderness
    is π√(2E/σ_y).

- The **effective length factor K** encodes the rotational and translational
  end-fixity of the column. Standard values are: pin-pin = 1.0, fix-fix = 0.5,
  fix-pin ≈ 0.699, fix-free = 2.0, fix-guided = 1.0. A boundary condition not
  in this set must be justified by analysis before a K value is adopted.

- For **flat plates**, the critical stress is proportional to the plate
  buckling coefficient k (a function of aspect ratio and boundary conditions),
  E, and (t/b)²; Poisson's ratio enters through the (1−ν²) denominator. The
  coefficient k is taken from established plate-buckling charts cited in the
  report.

- **Knock-down factors** (γ < 1) reduce the theoretical critical stress to
  account for initial geometric imperfections, residual stresses, and
  manufacturing deviations. Applying γ = 1.0 (no knock-down) is only
  acceptable when a test-verified perfect-geometry assumption is documented.
  Knock-down values below 0.5 for shell structures are common and must be
  justified by imperfection-sensitivity analysis.

- **Margin of safety**: MS = σ_cr / σ_applied − 1. A negative MS is a buckling
  failure finding. A MS exactly equal to zero means the member is at the limit.
  The report must show MS ≥ 0 for every member after knock-down is applied.

## Workflow

1. Inventory every load-bearing structural member subject to compressive or
   in-plane shear loads and assign each to one geometry category: column,
   flat plate, or shell. Record the member ID, category, material (E, σ_y, ν),
   and geometry (L, r or t/b and aspect ratio) for each.

2. For each column member, record its end-fixity conditions (from the
   structural drawing or boundary-condition analysis) and look up or justify
   the effective length factor K. Compute the slenderness ratio KL/r and
   compare with the transition slenderness π√(2E/σ_y) to determine whether the
   Euler or Johnson formula applies.

3. Compute the theoretical critical buckling stress for each member:
   - Column, Euler: σ_cr = π²E / (KL/r)²
   - Column, Johnson: σ_cr = σ_y [1 − σ_y(KL/r)² / (4π²E)]
   - Flat plate: σ_cr = k π²E / [12(1−ν²)] × (t/b)²
   - Shell: use the appropriate knock-down-modified formula referenced in the
     report (shell buckling is geometry-specific; the DRD requires the formula
     source to be cited).

4. Apply the knock-down factor γ to every theoretical critical stress:
   σ_cr,reduced = γ × σ_cr. Justify each γ value by citing the source
   (test correlation, imperfection survey, design allowable, or standard
   knock-down table). Flag any γ = 1.0 assumption for explicit approval.

5. Retrieve the applied compressive stress σ_applied for each member from the
   design load case (limit or ultimate, as required by the DRD). Compute the
   margin of safety: MS = σ_cr,reduced / σ_applied − 1.

6. Confirm MS ≥ 0 for every member. Collect all members with MS < 0 as
   buckling findings. A member with no knock-down justification on record is
   also a finding, independent of its MS value.

7. Summarise results in the SB report table: member ID, geometry category,
   governing formula, K (columns only), KL/r (columns only), σ_cr theoretical,
   γ, σ_cr reduced, σ_applied, MS, and pass/fail verdict.

## Pitfalls

- Applying the Euler formula to a short, stocky column below the transition
  slenderness — the Euler formula overestimates the critical stress in the
  Johnson range, producing an unconservative MS.

- Omitting the knock-down factor for shells and treating the theoretical
  critical load as the design buckling load — thin-walled shells are highly
  sensitive to initial imperfections and the theoretical value can overestimate
  actual capacity by a factor of 3 or more.

- Using ultimate loads to compute MS when the DRD specifies limit loads, or
  vice versa — mixing load levels invalidates every MS in the report.

- Recording MS ≥ 0 before knock-down and reporting the member as compliant —
  the MS must be evaluated after the knock-down is applied, not from the
  theoretical critical stress alone.

- Leaving boundary conditions undocumented and defaulting to K = 1.0 (pin-pin)
  for a fixed-end connection — that assumption is unconservative and must be
  justified if the actual fixity is higher than pin-pin.

- Treating a member that carries a combined axial and bending load as a pure
  compression column — combined-loading cases require an interaction equation,
  not a uniaxial critical stress comparison.

## Behavior contract (gate 3)

The member-categorization, slenderness selection, Euler/Johnson formula,
knock-down application, and margin-of-safety logic are exercised by the gate 3
contract test: scripts/test_drd_buckling.py against scripts/drd_buckling_logic.py
(stdlib unittest, offline). Run:

```
python3 scripts/test_drd_buckling.py
```

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and paraphrase
  per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
- Reference: ECSS-E-ST-32C Annex M (structural buckling report content).
