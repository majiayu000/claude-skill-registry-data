---
name: e1011-eva
description: "Use when design EVA and planetary surface activity requirements for a space system under ECSS-E-ST-10-11C §4.7.10: verify suit interface compatibility (operating pressure, thermal envelope, life support endurance), assess tool design parameters (operator force limits, reach envelope, glove compatibility), evaluate crew mobility timelines and terrain trafficability, and compute consumable margins with required reserves for O2, power, and thermal control. Verify abort scenario timelines confirm safe crew return within consumable limits. Trigger: ecss, e-st-10-system-scope, eva, extravehicular-activity, suit-interface, eva-tools, crew-mobility, planetary-activity, consumable-margin."
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
  tags: [ecss, e-st-10-system-scope, eva, extravehicular-activity, suit-interface, eva-tools, crew-mobility, planetary-activity]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Human Factors — EVA and Planetary Surface Activity (space-systems/ecss/e1011-eva)

Use when the task is to design EVA and planetary surface activity
requirements for a space system under ECSS-E-ST-10-11C §4.7.10 --
specifying suit interfaces, EVA tool requirements, crew mobility
envelopes, consumable margins, and abort timelines.

## Domain quick reference

- EVA design covers two environments: orbital microgravity (ISS
  exterior, free-flyer) and planetary surfaces (lunar, Martian).
  Each environment drives different mobility assumptions: handrail
  translation speed and microgravity body positioning for orbital;
  suited walking speed and terrain slope limits for planetary. The
  surface type is determined before any timeline or force assessment.
- Suit interface parameters govern the physical connection between
  crew and system: the suit's operating pressure must be validated
  against the spacecraft cabin pressure to identify whether a pre-
  breathe protocol is required to mitigate decompression sickness
  risk. Life support endurance must cover the planned EVA duration
  plus a 25% reserve. Thermal operating range must bracket the
  expected environment temperatures at both extremes.
- Tool design requirements constrain force, reach, and grip. Suited
  crewmembers are limited in the force they can apply (approximately
  111 N one-handed, 222 N two-handed in typical EVA suits); any tool
  requiring a higher operator force fails the EVA design requirement.
  Reach envelopes and glove compatibility with the tool handle are
  checked separately and are both gateable.
- Consumable margins apply to O2, electrical power, and thermal
  control (metabolic heat removal). Each consumable is checked at
  end-of-EVA against a required reserve fraction (default 25%) of
  total supply. An EVA timeline that leaves any consumable below its
  reserve fraction fails the margin check.
- Abort scenario verification confirms that the crew can return to
  the airlock from the most distant worksite within the safe-return
  time limit using remaining consumables. The abort translation time
  is computed from worksite distance and surface-type translation
  speed; the remaining consumable capacity must cover that return
  duration.

## Workflow

1. Determine the surface type (microgravity, ISS exterior, lunar,
   Martian) for the EVA activity. This sets the translation speed
   and terrain slope limits used in all subsequent calculations.
2. Check suit interface compatibility: confirm that life support
   endurance covers planned duration with 25% margin; flag if suit
   operating pressure is at or above cabin pressure (pre-breathe
   protocol required); confirm environment temperatures fall within
   the suit's thermal operating range. Reject the suit if any life
   support or thermal check fails.
3. Assess each EVA tool: confirm required operator force does not
   exceed the suited operator force limit for the operation class
   (one-hand or two-hand); confirm tool reach meets the task's
   minimum reach; confirm the handle is compatible with the EVA
   pressure glove. Flag every failing parameter as a distinct issue.
4. Evaluate crew mobility: for planetary surfaces, compare terrain
   slope against the surface-type trafficability limit; compute
   estimated translation time from distance and speed; flag if
   estimated time exceeds the allowed timeline allocation.
5. Compute consumable margins at end of planned EVA duration: for
   each consumable (O2 mass, electrical energy, coolant/thermal
   capacity), subtract usage from supply and compare the remainder
   against the required reserve fraction. Flag each consumable that
   falls short.
6. Verify the abort scenario: compute return time from furthest
   worksite to airlock using the surface-type translation speed;
   confirm return time is within the abort time limit; confirm
   consumable remaining at abort trigger covers the return duration.
7. Aggregate all findings. The EVA design is compliant only when
   all suit, tool, mobility, consumable, and abort checks are clear.

## Pitfalls

- Applying ISS translation speed to a planetary surface EVA and
  underestimating return time -- suited walking on lunar or Martian
  terrain is two to four times slower than handrail translation
  in microgravity.
- Checking consumable margin against the remaining quantity at the
  abort trigger instead of at planned end-of-EVA -- the margin
  check applies to the full planned timeline; the abort check is
  a separate verification against remaining capacity at abort time.
- Treating a pre-breathe flag as non-critical -- if suit operating
  pressure is at or above cabin pressure, a pre-breathe protocol
  is operationally required and must be captured in the EVA design
  document; omitting it is a design gap, not a warning.
- Checking force against the operator maximum without also checking
  the class limit -- the suited crewmember's personal force
  capability may exceed the EVA class limit; both bounds must hold.
- Leaving terrain slope unverified for planetary EVAs because no
  specific worksite has been selected -- the design requirement must
  state the maximum slope for which the EVA is designed; if no value
  is on record, flag the gap rather than assume flat terrain.

## Behavior contract (gate 3)

The suit-interface, tool-assessment, mobility-evaluation,
consumable-margin, and abort-timeline logic is exercised by the
gate 3 contract test: scripts/test_e1011_eva.py against
scripts/e1011_eva_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e1011_eva.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
