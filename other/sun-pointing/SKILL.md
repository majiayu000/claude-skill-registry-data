---
name: sun-pointing
description: "Use when you must evaluate spacecraft sun pointing for the ADCS safe hold: compute the angle between the sun vector and the pointing axis, check it against the pointing tolerance, estimate the solar illumination factor at the sun angle, and size the slew rate to acquire the sun. Produces the sun pointing angle, the safe hold verdict, the illumination factor, and the required slew rate that gate sun acquisition. Trigger: sun pointing, safe hold, sun acquisition, solar illumination, slew rate."
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
  subdomain: adcs
  tags: [sun-pointing, safe-hold, sun-acquisition, solar-illumination, pointing-tolerance, slew-rate]
  version: 0.1.0
  author: Aero Agent Skills
---

# Spacecraft Sun Pointing (space-systems/adcs/sun-pointing)

Use when the task is spacecraft sun pointing for the ADCS safe hold:
sun vector to pointing axis angle, tolerance checks, illumination,
and sun acquisition slew sizing.

## Domain quick reference

- Units: vectors are dimensionless unit vectors; angles are in
  RADIANS; time is in seconds; slew rate is in rad/s; the solar
  illumination factor is dimensionless, = max(0, cos(angle)).
- Sun pointing angle: acos of the clamped cosine between the sun
  direction vector and the spacecraft pointing axis, in radians.
- Safe hold: the sun pointing angle must stay within the pointing
  tolerance for the sun acquisition phase.
- Solar illumination factor: 1.0 at zero angle, 0.5 at 60 degrees,
  and 0 at or beyond 90 degrees (cosine limit).
- Sun acquisition slew: required_slew_rate = angle / time, rad/s.
- Sun pointing geometry follows ECSS-E-ST-60 ADCS practice.

## Workflow

1. Collect the sun direction vector and the spacecraft pointing axis.
2. Compute the angle with sun_pointing_angle.
3. Check the angle with pointing_within_tolerance.
4. Estimate illumination with solar_illumination_factor.
5. Size the acquisition maneuver with required_slew_rate.
6. Gate the safe hold on the tolerance verdict.

## Pitfalls

- Passing angles in degrees to radian-based functions.
- Zero-norm sun vector (uninitialized ephemeris) raising ValueError.
- Demanding illumination beyond the cosine limit: the factor cannot
  exceed 1.0 at zero angle and is zero at 90 degrees and beyond.

## Behavior contract (gate 3)

The sun pointing angle, tolerance, illumination, and slew logic is
exercised by the gate 3 contract test:
scripts/test_sun_pointing.py against scripts/sun_pointing_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_sun_pointing.py

## Compliance

- Standards referenced, not reproduced: ECSS-E-ST-60 text is
  copyright ESA; the sun pointing geometry here is common ADCS
  methodology, summary-only per standards-map.yaml (ecss is a free
  ESA download).
- compliance: STANDARDS-REF, gated: false.
