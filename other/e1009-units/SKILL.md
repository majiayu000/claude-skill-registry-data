---
name: e1009-units
description: "Use when verify that every coordinate and derived quantity in a space-system interface document or software parameter list states its unit as the SI standard or an explicitly listed stated exception, per ECSS-E-ST-10-09C §5.4.3. For each parameter: determine the quantity type (distance, angle, time, angular rate, velocity, mass, force, pressure, temperature, frequency, acceleration), identify the prescribed SI unit, check whether the actual stated unit is SI or appears on the stated-exception list, and flag any parameter whose unit is neither. Output a per-parameter verdict (si, stated_exception, or non_compliant) and a summary of all findings. Trigger: ecss, e-st-10-system-scope, units, SI-units, coordinates, reference-frames, stated-exceptions, quantity-types, parameter-verification."
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
  tags: [ecss, e-st-10-system-scope, units, SI-units, coordinates, reference-frames, stated-exceptions, quantity-types]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Reference Frames — Unit Assignment (space-systems/ecss/e1009-units)

Use when the task is to verify that every coordinate and derived quantity
in a space-system interface document or software parameter list carries
a compliant unit — either the SI standard unit or an explicitly listed
stated exception — per ECSS-E-ST-10-09C §5.4.3.

## Domain quick reference

- §5.4.3 requires that each coordinate or derived quantity state its
  unit. The default is the SI base or coherent derived unit for that
  quantity. A unit that is not SI is only permitted when explicitly
  identified as a stated exception in the document; any other non-SI
  unit is non-compliant.
- Quantity types covered: distance (SI: m; exception: km), angle
  (SI: rad; exceptions: deg, arcmin, arcsec), time (SI: s; exceptions:
  min, h, day, yr, JD, MJD), angular rate (SI: rad/s; exceptions:
  deg/s, rpm, deg/h), velocity (SI: m/s; exception: km/s), mass
  (SI: kg; exception: g), force (SI: N), pressure (SI: Pa; exceptions:
  kPa, MPa), temperature (SI: K; exception: degC), frequency
  (SI: Hz; exceptions: kHz, MHz, GHz), acceleration (SI: m/s²;
  exception: km/s²).
- A stated exception must be traceable to an explicit entry in the
  standard or the project's unit declaration table. An undeclared
  non-SI unit is non-compliant regardless of how common it is in
  practice.
- The verdict for each parameter is one of three values: si
  (the parameter's unit matches the SI standard unit), stated_exception
  (the unit appears on the listed exception table), or non_compliant
  (the unit is neither SI nor a stated exception). An unknown quantity
  type also produces a finding and must be resolved before the
  parameter can be accepted.

## Workflow

1. Collect every quantity from the interface document or parameter
   list. Each entry must carry a quantity type label and an explicit
   unit string.
2. For each entry, look up the quantity type in the unit table. If the
   type is not found, record it as unknown and flag it — it cannot be
   assessed until the type is identified.
3. Compare the stated unit against the SI unit for that quantity type.
   If they match, record status as si. If the unit appears in the
   stated-exception set for that type, record stated_exception. If
   neither, record non_compliant with the expected SI unit and the
   available exceptions.
4. Aggregate the per-parameter verdicts. Report counts for si,
   stated_exception, non_compliant, and unknown_quantity. The
   parameter list is fully compliant only when non_compliant and
   unknown_quantity counts are both zero.
5. For each non-compliant finding, provide the offending unit, the
   correct SI unit, and the permitted exceptions so the author can
   correct the document.

## Pitfalls

- Accepting a commonly used unit without checking whether it appears
  on the stated-exception list. Frequent use in the industry does not
  make a unit compliant; only an explicit entry in the exception table
  does.
- Treating an unknown quantity type as implicitly SI-compliant. An
  unknown type must be resolved; it cannot be passed without a lookup
  result.
- Confusing unit prefixes with stated exceptions. Prefixed variants
  (km, kPa, MHz) are compliant only when explicitly listed for that
  quantity type. The base SI unit is always compliant; a prefix is not
  automatically a stated exception.
- Using degrees and radians interchangeably without recording which one
  the parameter document declared. Both are in the table, but the
  stated unit must match whatever the document actually writes. Mixing
  them silently is the most common numerical error in reference-frame
  implementations.

## Behavior contract (gate 3)

The unit-table lookup, SI check, stated-exception check, and
parameter-list aggregation logic is exercised by the gate 3 contract
test: scripts/test_e1009_units.py against scripts/e1009_units_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_e1009_units.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
