---
name: ramjet-cycle
description: "Use when you must analyze the ideal ramjet cycle: compute the flight stagnation temperature from the speed of sound and Mach number, the total temperature ratio across the combustor from the fuel air ratio and lower heating value, the specific thrust from the Mach number and total temperature ratio, the total thrust from the captured mass flow, and the specific impulse and thermal efficiency from the fuel flow. Produces the specific thrust, thrust, specific impulse, and thermal efficiency that gate the airbreathing hypersonic engine assessment. Trigger: ramjet, fuel air ratio, total temperature ratio, specific thrust, specific impulse."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: far-33
    reference-only: true
gated: false
domain: propulsion
pack: propulsion
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: propulsion
  subdomain: ramjet
  tags: [ramjet-cycle, ideal-ramjet, specific-thrust, fuel-air-ratio, total-temperature-ratio, specific-impulse, thermal-efficiency]
  version: 0.1.0
  author: Aero Agent Skills
---

# Ramjet Cycle (propulsion/ramjet/ramjet-cycle)

Use when the task is ideal ramjet cycle evaluation: stagnation
temperature, total temperature ratio, specific thrust, total thrust,
specific impulse, and thermal efficiency for an airbreathing hypersonic
engine.

## Domain quick reference

Units are SI throughout:

- Static temperature in K, speeds in m/s.
- Mass flow in kg/s, thrust in N, specific thrust in N/(kg/s).
- Fuel air ratio f dimensionless, LHV in J/kg, cp in J/(kg K).
- Specific impulse in seconds, efficiencies dimensionless.

The ideal ramjet cycle (isentropic inlet, constant-pressure heat
addition, fully expanded nozzle, perfect gas):

- Speed of sound a0 = sqrt(gamma * R * T0), with gamma = 1.4 and
  R = 287 J/(kg K) for air.
- Flight stagnation temperature Tt0 = T0 * (1 + (gamma - 1)/2 * M0^2).
- Combustor total temperature ratio tau_lambda = Tt4 / Tt0 = 1 +
  eta_b * f * LHV / (cp * Tt0).
- Specific thrust F / m_dot_a = a0 * M0 * (sqrt(tau_lambda) - 1),
  from the fully expanded jet speed v9 = v0 * sqrt(tau_lambda).
- Total thrust F = m_dot_a * (F / m_dot_a).
- Specific impulse Isp = (F / m_dot_a) / (f * g0), with g0 = 9.80665
  m/s^2.
- Thermal efficiency eta_th = (F / m_dot_a) * v0 / (f * LHV).
- Ramjet cycle practice sits in the FAR-33 engine design context.

## Workflow

1. Collect the static temperature, gas properties, and Mach number;
   compute the speed of sound and the stagnation_temperature.
2. Collect the fuel air ratio, LHV, cp, and combustor efficiency;
   compute the total_temperature_ratio.
3. Combine speed of sound, Mach number, and total temperature ratio
   into the specific_thrust.
4. Multiply by the captured mass flow for the thrust and by the fuel
   air ratio for the fuel_mass_flow.
5. Compute the specific_impulse and thermal_efficiency from the fuel
   flow terms.
6. Gate the airbreathing engine assessment on the four outputs.

## Pitfalls

- Using a total temperature ratio at or below 1.0; the ideal ramjet
  needs heat addition, so sqrt(tau_lambda) - 1 turns negative.
- Confusing static and stagnation temperature; the combustor ratio
  and the energy balance use Tt0 from the flight Mach number.
- Using total thrust where specific thrust belongs; specific impulse
  divides specific thrust by the fuel flow per unit air, not the
  total fuel flow.
- Reporting thermal efficiency above 1.0; thrust power cannot exceed
  the fuel chemical power input.

## Behavior contract (gate 3)

The stagnation, ratio, thrust, impulse, and efficiency logic is
exercised by the gate 3 contract test: scripts/test_ramjet_cycle.py
against scripts/ramjet_cycle_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_ramjet_cycle.py

## Compliance

- Standards referenced, not reproduced: FAR-33 is US government work
  (public domain); the ideal ramjet relations are common propulsion
  methodology, summary-only per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
