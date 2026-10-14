---
name: e1009-time
description: "Use when define the time scale and epoch for each spacecraft reference frame under ECSS E-ST-10C §5.4.4: select from TAI, UTC, UT1, TT, TDB, TCB, TCG, or GPS for inertial (ECI, GCRS), Earth-rotating (ECEF, ITRS), or barycentric (BCRS, HCI) frames; identify the standard epoch (J2000.0, J1950.0, B1950.0, or MJD) used as the time origin; verify each frame–time-scale pairing is consistent with its motion description; and convert between time scales using the TAI–TT constant offset or a supplied leap-second count for UTC. Trigger: ecss, e-st-10-system-scope, time-scales, epochs, tai, utc, tt, tdb, j2000, reference-frames."
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
  tags: [ecss, e-st-10-system-scope, time-scales, epochs, tai, utc, tt, tdb, j2000, reference-frames]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS E-ST-10C — Time Scales and Epochs (space-systems/ecss/e1009-time)

Use when the task is to select and verify the time scale and epoch
associated with each reference frame in a space mission, following
ECSS E-ST-10C §5.4.4. This leaf covers the eight standard time
scales (TAI, UTC, UT1, TT, TDB, TCB, TCG, GPS), the standard
epochs (J2000.0, J1950.0, B1950.0, MJD epoch), and the rules
binding each frame to its recommended scale.

## Domain quick reference

- **TAI** (International Atomic Time) is the primary uniform atomic
  scale. All other scales are derived from or referred to TAI.
- **TT** (Terrestrial Time) equals TAI + 32.184 s exactly. It is the
  scale used for geocentric ephemerides and is the defining scale for
  the J2000.0 epoch.
- **UTC** (Coordinated Universal Time) equals TAI minus an integer
  count of leap seconds broadcast by IERS. It is the civil broadcast
  time and is used with Earth-rotating frames (ECEF, ITRS) whose
  orientation depends on Earth rotation angle.
- **UT1** (Universal Time 1) tracks the actual angle of Earth's
  rotation. It differs from UTC by DUT1, which stays within ±0.9 s
  by IERS convention. UT1 is required when converting Earth-rotating
  frame orientations to inertial frames at high precision.
- **TDB** (Barycentric Dynamical Time) is used for solar-system
  ephemerides and barycentric frames (BCRS, HCI). Its mean rate
  matches TT; the periodic difference stays within ±2 ms.
- **TCB** and **TCG** are SI-second coordinate time scales at the
  solar-system barycentre and Earth geocentre respectively. They
  drift from TT/TDB by a secular rate (~1.48 × 10⁻⁸) and are used
  when relativistic rigour is required.
- **GPS time** equals TAI − 19 s, a constant offset established at
  the GPS epoch (1980-01-06). GNSS receiver outputs must be converted
  to TAI or UTC before ingestion into frame computations.
- **J2000.0** is defined as 2000 January 1, 12:00:00 TT
  (JD 2451545.0 TT). It is the standard reference epoch for modern
  inertial frames. J1950.0 (JD 2433282.5 TT) and B1950.0
  (Besselian) are legacy epochs retained for historical catalogues.
- **Modified Julian Date (MJD)** equals JD − 2 400 000.5 and is
  commonly used in AOCS and GNSS systems to avoid large integers.

## Frame–time-scale pairing rules

Each reference frame requires a specific time scale for its
orientation or position computation. The table below is paraphrased
from §5.4.4 of ECSS E-ST-10C; use it as the selection guide.

| Frame | Recommended scale(s) | Notes |
|-------|----------------------|-------|
| ECI   | TT, TAI              | Inertial; avoids leap-second discontinuities |
| GCRS  | TT, TCG              | Geocentric relativistic RS |
| ECEF / ITRS | UTC, UT1   | Orientation tied to Earth rotation angle |
| TEME  | UTC, TAI             | Two-Line Element propagation convention |
| BCRS  | TDB, TCB             | Solar-system barycentre |
| HCI   | TDB, TCB             | Heliocentric inertial |
| RTN / LVLH | UTC, TAI, TT  | Relative frames; inherits from parent inertial or rotating |

Using a rotating-frame scale (UTC/UT1) with an inertial frame (ECI,
GCRS) or a barycentric scale (TDB) with an Earth-fixed frame is a
procedural error that will produce incorrect frame-to-frame rotation
matrices.

## Workflow

1. Identify every reference frame used in the mission (ECI, ECEF,
   BCRS, etc.) and record each frame's motion description (inertial,
   Earth-rotating, barycentric).

2. For each frame, select the recommended time scale from the pairing
   table above. Reject any scale that is not in the recommended set
   for that frame; flag the pairing as inconsistent and require
   engineering justification to proceed.

3. Assign a standard epoch to each frame definition. Prefer J2000.0
   for modern inertial and barycentric frames. State the epoch's
   Julian Date and its reference time scale (J2000.0 is defined in TT).

4. For any data source using GPS time or UTC: convert to TAI first
   (GPS → TAI: add 19 s; UTC → TAI: add the current leap-second count
   from the IERS bulletin), then propagate to TT or TDB as required
   by the target frame.

5. When computing frame-orientation matrices (e.g. GMST, GAST, or
   precession–nutation for ECI↔ECEF), confirm the time argument is
   in the scale required by the transformation algorithm (GMST uses
   UT1; precession–nutation models use TT).

6. Document the time scale and epoch for every state vector, attitude
   quaternion, and ephemeris product in the mission data dictionary;
   leave no product with an unspecified or assumed time tag.

## Pitfalls

- Supplying UTC seconds to an algorithm that expects TT seconds
  without converting through TAI. The error accumulates by one second
  per leap-second event and is invisible until a leap second occurs
  in-flight.
- Treating TDB and TT as interchangeable in orbit propagation. The
  periodic TDB–TT difference (up to ~1.6 ms) is negligible for most
  mission phases but reaches tens of metres in position error for
  high-precision interplanetary trajectories.
- Applying the GPS–TAI offset of 19 s to a UTC-tagged timestamp
  instead of the current leap-second count. UTC and GPS diverge
  because UTC accumulates leap seconds while the GPS offset does not.
- Leaving the epoch scale implicit. J2000.0 is defined in TT; if a
  tool internally uses TCB and labels its epoch "J2000.0", the
  secular drift between TT and TCB will cause position errors that
  grow with mission duration.
- Mixing MJD (which truncates the JD integer) with JD in arithmetic
  without accounting for the 2 400 000.5 day offset, causing
  single-day or half-day biases in time-tagged products.

## Behavior contract (gate 3)

The time-scale validation, epoch lookup, frame–time-scale
compatibility, and conversion logic are exercised by the gate 3
contract test: scripts/test_e1009_time.py against
scripts/e1009_time_logic.py (stdlib unittest, offline). Run:

```
python3 scripts/test_e1009_time.py
```

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
