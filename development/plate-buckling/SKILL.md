---
name: plate-buckling
description: "Use when a wing or fuselage skin panel, spar web or flat panel must be margin-checked against elastic instability in a stdlib-only environment without FEA software. Calculate the elastic buckling of flat plates and skin panels under compression and shear: resolve the plate buckling coefficient k from the edge conditions and the panel aspect ratio (k = 4.0 for a simply supported long plate, 6.97 for a clamped long plate), compute the critical compression buckling stress sigma_cr = k*pi^2*E/(12*(1-nu^2))*(t/b)^2 and the shear buckling stress tau_cr with the shear buckling coefficient k_s, run the combined compression-shear interaction check, and size the effective width of stiffened skin. Units are SI. Trigger: plate buckling, panel buckling, buckling coefficient, shear buckling, skin panel, spar web, critical buckling stress, effective width."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: far-25
    reference-only: true
  - id: cs-25
    reference-only: true
gated: false
domain: structures
pack: structures
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: structures
  subdomain: fem
  tags: [plate-buckling, panel-buckling, buckling-coefficient, compression-buckling, shear-buckling, skin-panel, spar-web, effective-width, critical-buckling-stress, flat-plate]
  version: 0.1.0
  author: Aero Agent Skills
---

# Plate Buckling (structures/fem/plate-buckling)

Use when the task is the elastic stability of a flat plate or skin
panel: resolving the plate buckling coefficient k from the edge
conditions and the panel aspect ratio, computing the critical
compression buckling stress sigma_cr = k * pi^2 * E / (12 * (1 -
nu^2)) * (t / b)^2 and the shear buckling stress tau_cr of a web or
panel, running the combined compression-shear interaction check, and
sizing the effective width of stiffened skin in the post-buckling
range. The logic module is pure Python standard library (no numpy, no
FEA software) and deterministic. Units are SI: E in Pa, t and b in m,
stresses in Pa, a and b in m.

## Domain quick reference

- A flat rectangular plate of thickness t and width b (measured
  across the load direction) buckles elastically when the applied
  edge stress reaches the critical value:

      sigma_cr = k * pi^2 * E / (12 * (1 - nu^2)) * (t / b)^2
      tau_cr  = k_s * pi^2 * E / (12 * (1 - nu^2)) * (t / b)^2

  where E is the Young's modulus, nu the Poisson ratio, and k (or
  k_s) the plate buckling coefficient. The stress scales with the
  square of the thickness-to-width ratio: doubling t / b quadruples
  the critical stress, which is why skin thickness and stringer pitch
  trade directly against each other.

- Compression coefficient, simply supported on all edges (exact,
  minimized over the half-wave count m):

      k = min_m (m / a_r + a_r / m)^2,   a_r = a / b

  The long plate gives k = 4.0. The clamped long plate approximation
  is k = 6.97; short clamped plates have a higher coefficient and
  need tabulated data. Shear coefficient (Timoshenko):

      simply supported:  k_s = 5.34 + 4 / a_r^2    (a_r >= 1)
                         k_s = 5.34 * a_r^2 + 4    (a_r <  1)
      clamped:           k_s = 8.98 + 5.6 / a_r^2  (a_r >= 1)
                         k_s = 8.98 * a_r^2 + 5.6  (a_r <  1)

- Combined compression and shear interacts approximately as

      sigma / sigma_cr + (tau / tau_cr)^2 <= 1

  linear in compression and quadratic in shear: a modest shear
  stress consumes a large share of the buckling capacity.

- Post-buckling: stiffened skin carries load through the von Karman
  effective width b_e = 1.9 * t * sqrt(E / sigma_edge), capped at the
  panel width, valid once the edge stress exceeds the panel buckling
  stress.

Worked anchors (verified by running scripts/plate_buckling_logic.py):
an aluminum skin with E = 70 GPa, nu = 0.33, t = 2 mm, stringer
pitch b = 150 mm and a/b = 2, simply supported, has k = 4.0 (the
m = 2 half-wave gives (1 + 1)^2) and sigma_cr = 45.9 MPa; against an
applied compression of 30 MPa the margin of safety is 0.531. An
aluminum spar web with t = 1.5 mm, depth b = 250 mm and a/b = 2 has
k_s = 5.34 + 4/4 = 6.34 and tau_cr = 14.7 MPa; against 8 MPa of
applied shear the margin is 0.844. With 30 MPa compression and 8 MPa
shear the interaction index is 0.947, stable with margin 0.056. At an
edge stress of 200 MPa the 2 mm skin has an effective width of
71.1 mm. Second anchor: the same skin at a/b = 1.5 gives k = 4.340
and at a/b = 0.5 gives k = 6.25, while the clamped long plate gives
k = 6.97, 74 percent above the simply supported value.

## Workflow

1. Identify the panel geometry: the loaded length a, the width b
   across the load (for a skin panel between stiffeners this is the
   stiffener pitch, for a spar web the web depth), and the thickness
   t. Compute the aspect ratio a_r = a / b.
2. Select the edge condition: 'ssss' for a simply supported panel
   (skin between stringers with flexible attachments) or 'cccc' for a
   clamped panel (heavily restrained edges). Aliases accepted:
   simply-supported, pinned, clamped, fixed.
3. Resolve the coefficient with compression_coefficient(a_r,
   edge_condition) for compression or shear_coefficient(a_r,
   edge_condition) for shear.
4. Compute the critical stress with
   compression_buckling_stress(E, nu, t, b, k) or
   shear_buckling_stress(E, nu, t, b, k_s). Both share the same
   denominator 12 * (1 - nu^2).
5. Run the complete margin check in one call with
   compression_panel_check(E, nu, t, a, b, edge_condition,
   applied_stress) or shear_panel_check(E, nu, t, a, b,
   edge_condition, applied_shear), which return the coefficient, the
   critical stress, the margin of safety and the stable verdict.
   Apply the required factor of safety from the certification basis
   (1.5 ultimate-to-limit per FAR-25.303 / CS-25.303) before
   comparing the applied stress against the critical stress.
6. For combined compression and shear (a shear web carrying bending
   compression plus shear, or a skin panel under shear plus
   compression), run interaction_index(compression_stress,
   compression_critical, shear_stress, shear_critical): stable when
   the index is below 1, margin = 1 / index - 1.
7. For stiffened skin loaded beyond its buckling stress, size the
   effective width with effective_width(E, sigma_edge, t) and cap it
   at the panel width b before re-computing the stiffener load.

## Pitfalls

- Routing column buckling here: buckling-analysis handles 1D columns
  and struts with the Euler load, effective length factor K and
  slenderness ratio; plate-buckling handles 2D flat plates and skin
  panels with the k-coefficient formulas and never uses a slenderness
  ratio or an effective length factor.
- Routing FEA buckling here: a full-model eigenvalue buckling run in
  CalculiX belongs to calculix-linear or calculix-nonlinear;
  plate-buckling is a hand-scale closed-form panel check with no
  stiffness matrix and no software.
- Routing panel sizing here: fuselage-skin-stringer and wing-box-sizing
  (vehicle-design family) close the overall stiffened shell or wing
  box (skin thickness from hoop stress, stringer area, spar cap
  area); plate-buckling only checks the elastic stability of one flat
  panel with known dimensions.
- Routing sandwich panels here: sandwich-panels checks face stress,
  core shear and face wrinkling of a sandwich construction;
  plate-buckling checks monolithic flat skins and webs for elastic
  instability, not a sandwich cross-section.
- Using the column coefficient for a plate: k = 4.0 (simply
  supported) or 6.97 (clamped) applies to flat plates; the Euler
  column result is a different geometry and a different formula.
- Mixing the aspect ratio convention: a is the loaded length and b
  the width across the load; swapping them changes k (a/b = 0.5 gives
  k = 6.25, a/b = 2 gives k = 4.0) and the critical stress.
- Forgetting that clamped short plates are special: the 6.97 value is
  the long-plate clamped approximation; compression_coefficient
  raises ValueError below aspect_ratio 1 where tabulated data is
  required, so do not silently extrapolate.
- Applying the interaction equation wrongly: the compression term is
  linear and the shear term is squared; using (tau / tau_cr) to the
  first power overstates the margin.
- Using effective width below the buckling stress: the von Karman
  width is a post-buckling concept and must be capped at the panel
  width; below the critical stress the full width carries load.
- Mixing units: E in GPa with t and b in mm silently corrupts the
  stress by factors of 1e9 or 1e6; keep everything SI (Pa, m).
- Ignoring imperfections: the ideal flat plate formulas assume a
  perfect plate; initial waviness and eccentric load reduce the real
  buckling stress below sigma_cr, and in-service corrosion or dent
  damage lowers the effective thickness.

## Behavior contract (gate 3)

The plate buckling logic is exercised by the gate 3 contract test:
scripts/test_plate_buckling.py against
scripts/plate_buckling_logic.py (stdlib unittest, offline). It
asserts the worked anchors above, the coefficient boundaries at
aspect ratios 1 and 2, the (t/b)^2 and E scalings, the clamped versus
simply supported ranking, the linear-compression and
quadratic-shear interaction scaling, the effective width dependence,
and the ValueError cases for non-positive, non-finite or unknown
inputs. Run:

python3 scripts/test_plate_buckling.py

## Compliance

- FAR-25 and CS-25 are referenced, not reproduced: standards-map.yaml
  marks them gated: false and reference-only: true; only the summary
  paraphrase above is used, never standard text.
- compliance: STANDARDS-REF, gated: false.
