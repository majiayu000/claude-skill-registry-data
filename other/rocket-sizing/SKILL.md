---
name: rocket-sizing
description: "Use when you must size launch-vehicle propulsion with the rocket equation: calculate delta-v from specific impulse and the initial and final masses, derive the mass ratio from a delta-v requirement, compute the propellant mass, and sum the delta-v across the stages of a multistage launch vehicle. Produces the stage delta-v, the mass ratio, and the propellant mass that gate the vehicle sizing. Applies to each stage of the launch vehicle in consistent SI units. Trigger: rocket equation, delta-v, mass ratio, propellant mass, staging, specific impulse."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: ecss
    reference-only: true
gated: false
domain: propulsion
pack: propulsion
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: propulsion
  subdomain: rocket
  tags: [rocket-equation, delta-v, mass-ratio, propellant-mass, staging, specific-impulse]
  version: 0.1.0
  author: Aero Agent Skills
---

# Rocket Sizing (propulsion/rocket/rocket-sizing)

Use when the task is launch-vehicle propulsion sizing with the
rocket equation: delta-v, mass ratio, propellant mass, and
multistage delta-v summation.

## Domain quick reference

- The ideal rocket equation gives delta-v = g0 * Isp * ln(m0 / mf),
  with g0 = 9.80665 m/s^2.
- Units: specific impulse in seconds, masses in kg, delta-v in m/s.
- The mass ratio is m0 / mf; the propellant mass is m0 - mf.
- A multistage vehicle sums the delta-v of its stages, each computed
  with its own stage masses and specific impulse.
- ECSS space-systems standards frame the launch-vehicle engineering
  context.

## Workflow

1. Collect stage specific impulse and the initial and final masses.
2. Compute stage delta-v with rocket_equation_delta_v.
3. Derive the mass ratio with mass_ratio_from_delta_v.
4. Compute the propellant mass with propellant_mass.
5. Sum the stage delta-v with total_stage_delta_v.

## Pitfalls

- Confusing mass ratio (m0 / mf) with propellant fraction
  ((m0 - mf) / m0).
- Summing delta-v without recomputing the rocket equation per stage
  with that stage's own masses.
- Using a zero final mass (or mf >= m0), which breaks the logarithm.

## Behavior contract (gate 3)

The delta-v, mass ratio, propellant, and staging logic is exercised
by the gate 3 contract test: scripts/test_rocket_sizing.py against
scripts/rocket_sizing_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_rocket_sizing.py

## Compliance

- Standards referenced, not reproduced: ECSS is a free ESA download
  (ecss.nl/standards); the rocket equation is common propulsion
  methodology, summary-only per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
