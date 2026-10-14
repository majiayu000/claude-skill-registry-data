---
name: e1009-csys
description: "Use when define coordinate systems for a spacecraft or mission under ECSS-E-ST-10C §5.4.2: select a frame type (inertial, rotating, body-fixed, orbital, or topocentric), confirm that all axes within the chosen representation (Cartesian, spherical, or cylindrical) carry unambiguous direction references, flag every frame whose origin or orientation varies with time as time-dependent, and verify that no frame with an underdefined axis or unresolved parent reference enters the system model. A compliant set has all axes defined, all time-dependent frames explicitly flagged, and every non-root frame referencing a known parent. Trigger: ecss, e-st-10-system-scope, coordinate-systems, reference-frames, time-dependent-frames, frame-definition, axis-definition, spacecraft-geometry."
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
  tags: [ecss, e-st-10-system-scope, coordinate-systems, reference-frames, time-dependent-frames, frame-definition, axis-definition, spacecraft-geometry]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS System Engineering — Coordinate System Definition (space-systems/ecss/e1009-csys)

Use when the task is defining the coordinate systems for a space mission or
spacecraft under ECSS-E-ST-10C §5.4.2 -- selecting reference frame types,
confirming that every coordinate within a chosen frame representation is
unambiguously defined, and flagging every frame whose orientation or origin
changes with time.

## Domain quick reference

- A coordinate system has three parts: a frame type that fixes the physical
  sense of the origin and axes, a coordinate representation that determines
  which coordinate labels are required, and a time-dependence flag that states
  whether the frame's orientation relative to an inertial frame changes over time.
- Five frame types are recognised under §5.4.2: inertial (fixed relative to
  distant stars; e.g., ECI, ICRF), rotating (turns at a known rate relative
  to an inertial frame; e.g., ECEF), body-fixed (tied to the spacecraft or
  another body), orbital (derived from instantaneous orbital elements), and
  topocentric (origin on a body surface, rotating with that body).
- Three coordinate representations are used: Cartesian (axes x, y, z),
  spherical (coordinates r, theta, phi), and cylindrical (coordinates
  rho, phi, z). Each requires every label to have an unambiguous direction
  reference before the coordinate system is considered fully defined.
- Time-dependence is inherent for rotating, orbital, and topocentric frames;
  it must be assessed explicitly for body-fixed frames (a spinning or
  manoeuvring body makes the frame time-dependent); and inertial frames are
  treated as time-independent for mission timescales (precession over
  millennia is outside §5.4.2 scope).
- A coordinate system that references a parent frame (e.g., LVLH defined
  relative to ECI) carries a parent-frame field. Every such reference must
  resolve to a known frame within the registered set before the set is
  accepted.

## Workflow

1. For each coordinate system to be defined, record its name, frame type,
   coordinate representation, origin definition, and axis or parameter
   directions. Reject any entry with an empty name, an unrecognised frame
   type, or an unrecognised coordinate representation immediately.
2. Check that the origin field is non-empty. A frame with no origin
   definition is underdefined and must not proceed to the axis check.
3. Verify that every required coordinate label for the chosen representation
   has a non-empty direction definition. For Cartesian, all three of x, y, z
   must be specified; for spherical, r, theta, phi; for cylindrical, rho,
   phi, z. Any missing or empty label makes the frame underdefined.
4. Determine and record the time-dependence flag. For rotating, orbital, and
   topocentric frame types, the flag is always true and cannot be overridden.
   For inertial frame types, the flag is false unless explicitly set. For
   body-fixed, accept the caller's declaration but default to false when none
   is given; note that a maneuvring or spinning body-fixed frame should be
   flagged true.
5. Validate the parent-frame reference if one is provided. Every non-root
   coordinate system that names a parent must reference a frame already
   present in the registered set. An unresolved reference is flagged as an
   error in the parent-frame chain.
6. After processing all frames, produce a summary: total count, count and
   names of time-dependent frames, count and names of underdefined frames,
   and whether the set is fully compliant (no underdefined frames, no broken
   parent references).

## Pitfalls

- Treating rotating, orbital, and topocentric frames as time-independent --
  these frame types inherently change orientation relative to an inertial
  frame and must always carry the time-dependent flag.
- Accepting a Cartesian frame with only two axis definitions on the grounds
  that the third axis can be inferred from the right-hand rule -- the
  right-hand construction requires both defined axes to be correctly oriented;
  each axis must be stated explicitly so that the direction is unambiguous.
- Leaving a parent-frame reference unresolved and proceeding with the
  coordinate system chain -- a broken reference makes any transformation
  between the child and its ancestors undefined and invalidates any analysis
  that depends on the chain.
- Treating an empty-string axis direction as a valid definition -- an empty
  direction is indistinguishable from a forgotten entry and must be rejected
  as underdefined.

## Behavior contract (gate 3)

The frame-definition, axis-definability, time-dependence, parent-chain, and
registry-summary logic is exercised by the gate 3 contract test:
scripts/test_e1009_csys.py against scripts/e1009_csys_logic.py (stdlib
unittest, offline). Run:
python3 scripts/test_e1009_csys.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
