---
name: e7041-real
description: "Evaluate the real parameter encoding of ECSS-E-ST-70-41C clause 7.3.6, where a floating point value travels in whichever floating encoding the format code names and the width and precision are properties of that choice. Use when a measurement arrives visibly coarser than the sensor that produced it, or when a parameter has to be given an encoding: selecting the narrowest encoding that carries both the required magnitude and the required relative resolution, reporting the rounding a chosen encoding introduces, and refusing a value that would be written out as an infinity code or stored flat as zero. Trigger: ecss, e-st-70-41-packet-utilisation-scope, pus-real-parameter-type, floating-parameter-encoding-choice, parameter-relative-resolution, real-field-overflow-to-infinity, real-field-underflow-to-zero, single-versus-double-parameter-width."
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
  tags: [ecss, e-st-70-41-packet-utilisation-scope, e7041-real, pus-real-parameter-type, floating-parameter-encoding-choice, parameter-relative-resolution, real-field-overflow-to-infinity, real-field-underflow-to-zero, single-versus-double-parameter-width]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Packet Utilisation — Real Parameter Type (space-systems/ecss/e7041-real)

Use when the task is the real parameter type of ECSS-E-ST-70-41C
clause 7.3.6 -- the two normative items that make the floating
encoding an explicit choice carried by the format code, and that put
the burden of range and resolution on that choice rather than on the
value.

## Domain quick reference

- Width and precision come from the encoding, not from the
  parameter. A narrow floating encoding occupies four octets and
  resolves about seven significant decimal digits; a wide one
  occupies eight and resolves about sixteen. Halving the field halves
  nothing gracefully -- it removes twenty-nine bits of mantissa.
- Precision is relative, not absolute. The step between adjacent
  representable values scales with the magnitude, so a narrow
  encoding that resolves a millimetre near one metre resolves only
  metres near a million. A resolution requirement stated in absolute
  units has to be converted at the largest magnitude the parameter
  reaches before the encoding can be chosen.
- Range and resolution are two independent gates. A parameter can
  fit the magnitude of the narrow encoding comfortably and still need
  the wide one purely for resolution, and the reverse also happens.
  Selecting on one gate alone is how a parameter ends up quantised.
- The failure at the top of the range is silent by default. A
  magnitude past what the encoding holds becomes an infinity code,
  which then propagates through every derived calculation as
  infinity or as not-a-number rather than as an out-of-range report.
- The failure at the bottom is worse, because it looks like data. A
  magnitude below what the encoding holds stores as zero, and a
  reading of exactly zero from a sensor that cannot output zero is
  rarely questioned until much later.
- Binary fractions are exact and decimal fractions are not. A value
  like a quarter survives any binary encoding untouched; a tenth does
  not survive the narrow one, so a round trip is the only honest test
  of whether a particular value is carried or approximated.
- Every number here is worked in binary. Scalings go through an exact
  power-of-two operation and encodings through the binary pack
  itself, never through a power of ten or a logarithm, so the same
  bit pattern and the same reported error come back on every machine
  in the ground segment.

## Workflow

1. Convert the parameter's resolution requirement into a relative
   one, evaluated at the largest magnitude the parameter can reach.
   An absolute requirement cannot be tested against an encoding.
2. Walk the offered encodings narrowest first and take the first that
   passes both gates: the magnitude fits its finite range and its
   relative resolution is at least as fine as required. Refuse when
   none passes rather than defaulting to the widest.
3. Treat a requirement sitting exactly on an encoding's resolution as
   met by that encoding. The comparison absorbs representation error
   so the same requirement does not select different encodings on
   different machines.
4. Reject a non-finite value before packing: a real parameter field
   carries a measurement, and an infinity or not-a-number code is a
   symptom rather than a value to transmit.
5. Pack and unpack big endian at exactly the encoding's octet width,
   refusing an octet run of any other length.
6. Report the round trip rather than asserting it. Compare the stored
   value with the original, and categorize the result as exact,
   rounded, overflowing, or underflowing to zero.
7. Where a magnitude falls below the smallest value the encoding
   holds at full precision, say so separately: the quoted resolution
   no longer applies there even when the value is not yet zero.

## Pitfalls

- Choosing the encoding from the magnitude alone. The range gate is
  the easy one to pass; the resolution gate is the one that quantises
  an attitude or a temperature into visible steps.
- Stating the resolution requirement in absolute units and testing it
  against a relative one. The two agree at exactly one magnitude and
  diverge everywhere else, and the divergence is worst at the top of
  the range where it matters most.
- Reading an infinity that arrives in a decoded parameter as a very
  large measurement. It is not a measurement; the value overflowed
  the encoding on the way in, and the true magnitude is unrecoverable
  from the packet.
- Accepting a decoded zero from a parameter that cannot physically be
  zero. A magnitude below the encoding's floor stores flat, so the
  zero is an encoding artefact and the reading is lost rather than
  small.
- Assuming a value that round trips on the ground will round trip on
  board. Exactness is a property of the binary fraction, so a test
  set built from halves and quarters proves nothing about the decimal
  constants the flight software actually sends.

## Behavior contract (gate 3)

The encoding table, exact binary resolution, finite-range bounds,
non-finite refusal, big-endian pack and unpack, round-trip error
reporting, two-gate encoding selection and field assessment are
exercised by the gate 3 contract test: scripts/test_e7041_real.py
against scripts/e7041_real_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e7041_real.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
