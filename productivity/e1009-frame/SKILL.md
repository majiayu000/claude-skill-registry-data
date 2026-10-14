---
name: e1009-frame
description: "Use when define and validate a spacecraft reference frame under ECSS-E-ST-10C §5.4.1: establish the frame origin and three orthogonal right-handed axes, label each axis with a physical direction reference, determine whether the frame is inertial or time-varying (body-fixed, orbit-referenced, or planet-fixed), supply an epoch for inertial frames, confirm the name follows the ECSS uppercase-alphanumeric convention, and verify that any child frame traces an unbroken chain back to a root inertial frame. Trigger: ecss, e-st-10-system-scope, reference-frame, coordinate-frame, axes, right-handed, inertial, body-fixed, orbit-referenced, frame-naming."
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
  tags: [ecss, e-st-10-system-scope, reference-frame, coordinate-frame, axes, right-handed, inertial, body-fixed]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS System Engineering — Reference Frames (space-systems/ecss/e1009-frame)

Use when the task is to define or validate a spacecraft coordinate reference
frame under ECSS-E-ST-10C §5.4.1 — specifying origin, axis orientations,
handedness, time-dependence classification, naming, and frame-chain traceability.

## Domain quick reference

- A reference frame is uniquely described by (a) its origin — a physically
  identifiable point such as the spacecraft centre of mass or a sensor focal
  point — and (b) three mutually orthogonal unit vectors that form a
  right-handed coordinate triad (x, y, z such that z = x × y).
- Frames are categorized by their time-dependence:
  - **Inertial** — origin and axes are fixed relative to the celestial sphere;
    must carry an epoch (e.g. J2000.0); used as the root of the frame tree.
  - **Body-fixed** — axes rotate with the spacecraft structure; time-varying
    (changes with attitude); traced to an inertial root via the attitude
    rotation sequence.
  - **Orbit-referenced** — axes aligned with orbital position/velocity vectors
    (e.g. radial–transverse–normal); time-varying and mission-phase-dependent.
  - **Planet-fixed** — axes rotate with a planetary body (e.g. ECEF for Earth);
    time-varying relative to inertial space.
  - **Topocentric** — origin at a ground station or landing site; time-varying
    due to planetary rotation.
- Naming: ECSS §5.4.1 requires names to be unambiguous, uppercase
  alphanumeric with underscores, starting with a letter, and ≤ 64 characters
  (e.g. `SC_BODY`, `ECI_J2000`, `RTN_ORB`).
- Every non-root frame must reference a parent frame; the chain from any
  leaf frame to the inertial root must be traceable without gaps.

## Workflow

1. **Identify the origin**: Record a physically identifiable anchor point
   (e.g. spacecraft centre of mass, instrument aperture centre, ground-station
   reference mark). Reject any frame whose origin is vague or
   unverifiable from documentation.
2. **Assign axis directions**: Specify three unit vectors. Each must have
   magnitude 1.0 (within numerical tolerance). The pair (x, y) must be
   orthogonal (x · y = 0). Derive z = x × y and confirm the result matches
   the declared z axis; flag any deviation above tolerance.
3. **Categorize by time-dependence**: Assign the frame type from the
   enumeration above (inertial, body-fixed, orbit-referenced, planet-fixed,
   topocentric). Inertial frames must carry an explicit epoch. Body-fixed and
   orbit-referenced frames must be flagged as time-varying. Inertial frames
   must be flagged as time-independent.
4. **Apply naming convention**: Validate the frame name against the ECSS
   convention — uppercase letters and digits, underscores allowed,
   must begin with a letter, max 64 characters.
5. **Establish parent linkage**: For every non-root frame, record the name
   of its parent frame. Confirm the parent name appears in the defined
   frame set. Flag any frame whose parent is undefined.
6. **Produce the frame record**: Emit a complete frame definition record
   with origin description, axis unit vectors, frame type, time-dependence
   flag, epoch (if inertial), parent frame (if non-root), and name. A frame
   record is complete only when all fields above are present and validated.

## Pitfalls

- Using non-unit direction vectors (e.g. direction cosines not normalized)
  leads to incorrect rotation matrix computation downstream; always normalize
  and re-verify magnitude before recording.
- Omitting the epoch from an inertial frame makes the frame ambiguous across
  precession epochs (e.g. J2000.0 vs. J2050.0 differ by non-negligible
  amounts for high-precision pointing); treat a missing epoch as an error,
  not a default.
- Marking a body-fixed or orbit-referenced frame as time-independent
  conflates its instantaneous snapshot with the frame definition itself and
  silently breaks any downstream attitude propagation that reads the
  time-dependence flag.
- Leaving a non-root frame without a declared parent frame severs the
  traceability chain; transformation from that frame to any other frame
  becomes undefined and must be flagged as unresolved.
- Using lowercase or mixed-case frame names in a mixed-tool chain causes
  silent mismatches in attitude software that performs case-sensitive name
  lookups; enforce the uppercase convention at ingestion.

## Behavior contract (gate 3)

The origin-description, axis orthogonality/handedness, time-dependence
consistency, naming convention, and frame-chain traceability logic is
exercised by the gate 3 contract test:
scripts/test_e1009_frame.py against scripts/e1009_frame_logic.py
(stdlib unittest, offline).  Run:
python3 scripts/test_e1009_frame.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
