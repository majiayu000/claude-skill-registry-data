---
name: fsi-analysis
description: "Use when analyze fluid-structure interaction effects in a spacecraft or launch vehicle structural assembly per ECSS-E-ST-32 clause 4.6.2.7: identify sloshing loads from propellant or fluid-filled tank motion, determine hydroelastic coupling between structural vibration modes and enclosed fluid volumes, evaluate aerodynamic buffet excitation during atmospheric flight, compute effective added mass and natural frequency shifts caused by fluid-structure coupling, and verify that combined dynamic responses remain within structural margins. Trigger: ecss, e-st-32-structures-scope, fluid-structure-interaction, sloshing, hydroelastic, buffet, propellant-slosh, fsi, dynamic-coupling, launch-loads."
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
  tags: [ecss, e-st-32-structures-scope, fluid-structure-interaction, sloshing, hydroelastic, buffet, propellant-slosh, fsi, dynamic-coupling]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Structures — Fluid-Structure Interaction Analysis (space-systems/ecss/fsi-analysis)

Use when the task is to analyze fluid-structure interaction effects in a
spacecraft or launch vehicle per ECSS-E-ST-32 clause 4.6.2.7 — covering
propellant sloshing in tanks, hydroelastic coupling between structural
modes and enclosed fluid volumes, and aerodynamic buffet excitation during
atmospheric flight.

## Domain quick reference

- Clause 4.6.2.7 identifies three FSI effect families that must be assessed
  for any structure containing fluid or exposed to unsteady aerodynamic
  loading: sloshing (propellant or fluid motion inside a tank that exerts
  dynamic loads on the tank walls and shifts the vehicle's center of mass),
  hydroelastic coupling (interaction between a structural vibration mode and
  the inertia of the enclosed fluid, which lowers the effective natural
  frequency), and buffet (turbulent boundary-layer pressure fluctuations on
  the external skin during launch or atmospheric transit that produce
  broadband dynamic loads).
- Sloshing is characterized by its fundamental lateral frequency, which
  depends on tank radius, fill level, and effective gravity. The sloshing
  fluid can be modeled as an equivalent pendulum whose length is derived from
  that frequency. Low fill fractions (below ~30%) and high fill fractions
  (above ~85%) both require special attention: partial fill maximizes the
  participating sloshing mass at intermediate levels.
- Hydroelastic coupling is significant when the effective sloshing mass
  (approximately 63% of the total fluid mass for a cylindrical tank in the
  fundamental mode) exceeds roughly 5% of the structural dry mass. When
  coupling is significant, the coupled natural frequency is lower than the
  dry structural frequency by a factor of 1/sqrt(1 + added-mass ratio), and
  the reduced frequency must still satisfy the launcher or mission interface
  frequency requirement.
- Buffet loads are estimated from the freestream dynamic pressure, an exposed
  reference area, and an empirical buffet pressure coefficient. The resulting
  RMS force must be compared against the structural allowable for the affected
  panel or component. Buffet is most severe near maximum dynamic pressure
  (max-q) during ascent.

## Workflow

1. Inventory every tank, fluid-wetted volume, and external surface exposed to
   unsteady aerodynamic loading. For each tank, record tank inner radius, fill
   fraction, fluid density, and structural dry mass. For each external surface,
   record the reference area and the dynamic pressure at the critical flight
   condition (max-q).
2. For each tank, compute the fundamental lateral sloshing frequency using the
   cylindrical tank formula (Bessel root chi_11 = 1.8412, effective fluid
   height, and tank radius). Derive the equivalent pendulum length from that
   frequency and confirm it is consistent with the geometric fill level.
3. Compute the effective added sloshing mass using the 63% sloshing-mass
   fraction for the fundamental mode of a cylindrical tank. Compute the
   added-mass ratio (sloshing mass / structural dry mass). Determine whether
   hydroelastic coupling is significant (ratio > 0.05) or negligible.
4. Where coupling is significant, compute the coupled natural frequency:
   f_coupled = f_dry / sqrt(1 + added-mass ratio). Compute the fractional
   frequency shift. Check that f_coupled satisfies the minimum frequency
   requirement from the launcher interface control document or mission
   requirements; flag any case that fails.
5. For each external surface at the critical flight condition, compute the
   RMS buffet load: dynamic pressure x reference area x buffet pressure
   coefficient. Compare against the structural allowable for that surface;
   flag any case that exceeds the allowable.
6. Aggregate findings: a structural case is FSI-compliant only when its coupled
   frequency margin passes and its buffet load margin passes. Report
   non-compliant cases and identify the dominant FSI effect driving the finding.

## Pitfalls

- Applying the dry structural frequency to meet frequency requirements without
  accounting for the coupled (fluid-loaded) frequency — hydroelastic coupling
  can lower the frequency by 10–30% for propellant-heavy configurations, which
  may violate launcher interface requirements that appeared to be met.
- Using total fluid mass instead of the participating sloshing mass in the
  added-mass ratio — the entire propellant load does not slosh; only the
  fraction near the free surface participates, and overestimating this leads to
  unnecessarily conservative frequency corrections.
- Ignoring sloshing at high fill fractions under the assumption that "the tank
  is nearly full so there is no sloshing" — the sloshing frequency increases at
  high fill, but the loads on the tank dome can still be significant and must
  be checked.
- Treating buffet as a static load rather than a broadband dynamic excitation —
  the RMS load is the starting point; if the buffet spectral content overlaps a
  structural mode, dynamic amplification must be included and the peak load can
  substantially exceed the RMS value.

## Behavior contract (gate 3)

The sloshing frequency, added-mass ratio, hydroelastic coupling determination,
buffet load computation, frequency-shift correction, and margin checks are
exercised by the gate 3 contract test:
scripts/test_fsi_analysis.py against scripts/fsi_analysis_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_fsi_analysis.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
