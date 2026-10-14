---
name: nozzle-design
description: "Use when you must design a rocket engine nozzle from the chamber conditions: compute the exit Mach number for a target area ratio, the choked mass flow through the throat, the exit velocity and the exit static pressure, and the ideal thrust with the pressure term. Produces the nozzle area ratio, exit Mach number, mass flow, exit velocity, and thrust, plus the expansion verdict against the ambient pressure, all in consistent SI units (Pa, K, kg/s, m/s, N). Trigger: nozzle design, area ratio, exit mach, mass flow, ideal thrust, expansion ratio, choked throat."
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
  tags: [nozzle-design, nozzle, area-ratio, exit-mach, mass-flow, ideal-thrust, expansion-ratio, choked-throat]
  version: 0.1.0
  author: Aero Agent Skills
---

# Nozzle Design (propulsion/rocket/nozzle-design)

Use when the task is rocket nozzle design from the chamber conditions:
isentropic area ratio, exit Mach number, choked mass flow, exit
velocity, and ideal thrust with the expansion verdict.

## Domain quick reference

- The isentropic area-Mach relation links A/A* to the exit Mach
  number; the supersonic branch (M > 1) is monotonic.
- A choked throat fixes the mass flow from the chamber pressure and
  temperature alone, independent of the downstream pressure.
- Ideal thrust combines the momentum term mdot * ve with the pressure
  term (Pe - Pa) * Ae.
- Overexpanded means Pe < Pa (the pressure term subtracts);
  underexpanded means Pe > Pa; Pe = Pa is optimum.
- Units: every pressure in Pa (chamber P0, exit static Pe, ambient Pa),
  temperature in K, areas in m^2, mass flow in kg/s, velocity in m/s,
  thrust in N.
- ECSS space-systems standards frame the rocket propulsion context.

## Workflow

1. Collect the chamber pressure P0, chamber temperature T0, gamma,
   and specific gas constant R.
2. Pick the target area ratio and solve the exit Mach number with
   exit_mach_from_area_ratio.
3. Compute the choked mass flow with mass_flow.
4. Compute the exit velocity with exit_velocity.
5. Assemble the thrust with ideal_thrust and judge the expansion with
   optimum_expansion.

## Pitfalls

- Inverting the expansion verdict: overexpanded means Pe < Pa, and the
  pressure term (Pe - Pa) * Ae is negative.
- Mixing pressure units (Pa vs MPa) across the chamber, exit, and
  ambient inputs.
- Taking the subsonic root of the area-Mach relation instead of the
  supersonic branch.
- Letting the exit pressure exceed the chamber pressure.
- Dropping the pressure term when the nozzle is not matched to the
  ambient.

## Behavior contract (gate 3)

The area ratio, mass flow, exit velocity, thrust, and expansion logic
is exercised by the gate 3 contract test:
scripts/test_nozzle_design_logic.py against
scripts/nozzle_design_logic.py (stdlib unittest, offline). Run:
python3 skills/propulsion/rocket/nozzle-design/scripts/test_nozzle_design_logic.py

## Compliance

- Standards referenced, not reproduced: ECSS is a free ESA download
  (ecss.nl/standards); isentropic nozzle flow is standard compressible
  flow methodology, summary-only per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
