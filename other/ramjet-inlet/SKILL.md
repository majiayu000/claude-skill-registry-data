---
name: ramjet-inlet
description: "Use when you must analyze the supersonic ramjet inlet: compute the diffuser total pressure recovery at the flight Mach number from the isentropic limit or from the normal shock standing at the cowl lip, convert the freestream stagnation pressure into the diffuser exit total pressure, apply the Kantrowitz starting criterion to the contraction ratio to decide whether the inlet swallows the shock and starts, and report the starting limit Mach number and the maximum startable contraction ratio. Produces the pressure recovery, the exit total pressure, and the start verdict that gate the ramjet intake assessment. Trigger: kantrowitz, supersonic inlet, pressure recovery, diffuser, starting criterion, contraction ratio, normal shock."
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
  tags: [ramjet-inlet, kantrowitz-starting, inlet-pressure-recovery, supersonic-diffuser, normal-shock-recovery, isentropic-diffuser, starting-criterion, contraction-ratio]
  version: 0.1.0
  author: Aero Agent Skills
---

# Ramjet Inlet (propulsion/ramjet/ramjet-inlet)

Use when the task is supersonic ramjet inlet analysis: diffuser
pressure recovery, exit total pressure, and the Kantrowitz starting
verdict for an airbreathing hypersonic engine.

## Domain quick reference

Units are SI throughout: pressures in Pa, Mach number and all ratios
dimensionless, gamma = 1.4 for air:

- Diffuser total pressure recovery pi_d = pt2 / pt0, the ratio of the
  diffuser exit total pressure to the freestream total pressure.
- Isentropic recovery: pi_d = 1.0, the ideal lossless deceleration;
  the reference ceiling, unreachable at a supersonic Mach number.
- Normal shock recovery at the flight Mach number (pitot-type inlet,
  shock standing at the cowl lip), gamma = 1.4:
  pi_d = [6 M^2 / (M^2 + 5)]^3.5 * [6 / (7 M^2 - 1)]^2.5
  with values 0.7209 at M = 2 and 0.3283 at M = 3.
- Freestream total pressure pt0 = p0 * (1 + 0.2 M0^2)^3.5; the exit
  total pressure is pt2 = pi_d * pt0.
- Kantrowitz starting criterion: the inlet with contraction ratio
  CR = Acapture / Athroat starts (swallows the lip shock) only when
  CR <= CR_K(M0), the quasi-steady choked-throat limit:
  CR_K(M) = (1 / M) * pi_d_ns(M) * (1 + 0.2 M^2)^3 * (1.2)^-3
  with pi_d_ns(M) the normal shock recovery at M; CR_K rises from
  1.0 at M = 1 toward about 1.666 as the Mach number grows.
- Starting limit Mach number: the M that solves CR_K(M) = CR for a
  fixed contraction ratio; a contraction above about 1.666 (gamma =
  1.4) can never start at any Mach number.
- Ramjet inlet practice sits in the FAR-33 engine design context.

## Workflow

1. Collect the flight Mach number, the freestream static pressure and
   temperature, and the inlet contraction ratio.
2. Compute the freestream total pressure and the normal shock recovery
   with normal_shock_total_pressure_ratio.
3. Compare against the isentropic limit with isentropic_pressure_recovery
   and select the model with pressure_recovery.
4. Compute the diffuser exit total pressure with exit_total_pressure.
5. Apply the starting criterion: kantrowitz_contraction_limit at the
   flight Mach number, or kantrowitz_limit_mach for a fixed contraction
   ratio, and judge with inlet_starts.
6. Gate the ramjet intake assessment on the recovery and the start
   verdict.

## Pitfalls

- Using isentropic recovery at a supersonic Mach number: the ideal
  deceleration is the ceiling, the normal shock recovery at the flight
  Mach is the achievable value for a pitot-type inlet.
- Reading the starting criterion backwards: a higher contraction ratio
  is not easier to start, it needs a higher Mach number; above CR_K
  the inlet stays unstarted (buzz) until the flow starts.
- Confusing the Kantrowitz limit with the operating recovery: CR_K is
  a startability limit on the contraction ratio, not the diffuser
  total pressure ratio.
- Expecting a contraction above about 1.666 (gamma = 1.4) to start:
  no Mach number starts it, variable geometry or spillage is required.
- Using the normal shock model below M = 1: the normal shock relation
  is defined at supersonic Mach only, the isentropic branch is the
  subsonic limit.

## Behavior contract (gate 3)

The recovery, exit total pressure, and Kantrowitz starting logic is
exercised by the gate 3 contract test: scripts/test_ramjet_inlet.py
against scripts/ramjet_inlet_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_ramjet_inlet.py

## Compliance

- Standards referenced, not reproduced: FAR-33 is US government work
  (public domain); the normal shock relations, the isentropic diffuser
  recovery, and the Kantrowitz starting criterion are common propulsion
  and intake methodology, summary-only per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
