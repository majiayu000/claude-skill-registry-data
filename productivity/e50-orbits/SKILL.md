---
name: e50-orbits
description: "Derive what a mission's orbits do to its communication links, and check every phase actually declared one, per ECSS-E-ST-50C Rev.2 clause 5.6.5. Use when slant range, propagation delay, Doppler shift and pass duration have to come out of the orbit rather than out of a heritage table: the two normative items are graded apart, so a phase that reaches the link budget with no orbit behind it is reported as a declaration gap and not folded into a margin. Doppler is compared against receiver pull-in, delay and pass length against the phase allowance. Trigger: ecss, e-st-50c-clause-5-6-5, mission-orbit-declaration, space-link-slant-range, orbit-doppler-shift, ground-station-pass-duration, propagation-delay-allowance."
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
  tags: [ecss, e-st-50-communications-scope, e50-orbits, e-st-50c-clause-5-6-5, mission-orbit-declaration, space-link-slant-range, orbit-doppler-shift, ground-station-pass-duration, propagation-delay-allowance]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Communications — Mission Orbits (space-systems/ecss/e50-orbits)

Use when the task is clause 5.6.5 of ECSS-E-ST-50C Rev.2: naming the orbit
flown in each mission phase, and deriving from it the range, delay, Doppler
and visibility the communication system then has to live with.

## Domain quick reference

- Two obligations, graded apart. One is that every phase has an orbit; the
  other is that the communication consequences of those orbits are worked
  out. A mission can derive beautiful numbers for the phases it declared and
  still have a phase with no orbit at all, and a single verdict hides it.
- The orbit is the input to the link budget, not a context note. Slant range
  at the mask elevation sets the path loss and the delay; the orbital speed
  sets the Doppler; the period and the mask set how long the pass lasts.
  None of those can be inherited from a similar mission.
- Range is taken at the mask, not at the sub-satellite point. The worst
  geometry a station will work is the lowest elevation it is allowed to
  work, and the altitude alone understates the path by a large factor at low
  masks.
- Doppler is a receiver requirement before it is a link one. The shift the
  orbit imposes has to sit inside the pull-in range of the receiver at each
  end, and a shift outside it is not a margin shortfall but a receiver that
  never acquires.
- Pass duration decides whether the data volume is deliverable at all. A
  link that closes with margin for six hundred seconds a day still fails a
  phase that needs twenty minutes of contact.
- An orbit declared for a phase the mission does not have is as much a
  declaration defect as a phase with no orbit. It usually means a phase was
  renamed and one of the two documents did not follow.
- The pass model is a bound and has to be labelled as one. Taking the pass
  through the zenith over a non-rotating Earth is the longest pass the
  geometry allows; near synchronous altitude the neglected rotation
  dominates and the number understates real visibility.

## Workflow

1. Take the phase list once into a fixed order, refusing a repeat or a blank
   name, so the declaration and implication checks see the same phases.
2. Difference the phase list against the declared orbits both ways: phases
   with no orbit, and orbits belonging to no phase.
3. For each declared orbit, validate the altitude and the mask elevation,
   refusing a mask at or above ninety degrees.
4. Derive the slant range at the mask, then the one way and round trip
   propagation delays from it.
5. Derive the orbital speed and the largest line of sight rate, then the
   Doppler shift that rate imposes on the declared carrier.
6. Derive the pass duration from the period and the mask, and report it as
   the bound it is.
7. Compare each derived term against its allowance with a relative
   tolerance, and close with a ranked disposition: a declaration gap first,
   an allowance breach second, compliant only when neither stands.

## Pitfalls

- Using the altitude as the range. At a five degree mask the slant range is
  several times the altitude, and a budget built on the altitude closes on
  paper and not in the pass.
- Deriving Doppler from the orbital speed directly. Only the line of sight
  component shifts the carrier, and the full orbital speed overstates the
  shift by a factor that grows with altitude.
- Carrying one orbit for the whole mission. Transfer, operational and
  disposal orbits differ enough that the link that closes in one will not
  close in another.
- Treating a short pass as a margin problem. Contact time multiplies the
  data rate into a volume, and no amount of margin buys a pass that ends.
- Reading the bounding pass as the pass a station gets. It ignores Earth
  rotation and assumes the satellite goes through the zenith, so scheduling
  against it over-promises on every real pass.
- Comparing a derived value with a bare inequality at its limit. An orbit
  sized to sit exactly on a stated delay budget then passes or fails by
  which machine ran the check.

## Behavior contract (gate 3)

Altitude, elevation, carrier and phase list validation, the slant range,
period, range rate, Doppler and bounding pass duration against independently
computed reference values, both directions of the phase-to-orbit difference,
allowance comparison at the exact bound and the ranked disposition are
exercised by the gate 3 contract test: scripts/test_e50_orbits.py against
scripts/e50_orbits_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e50_orbits.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
