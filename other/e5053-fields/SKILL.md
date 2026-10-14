---
name: e5053-fields
description: "Define the ordered field set a packet transfer protocol data unit is built from. Use when an ECSS-E-ST-50-53C clause 5.4.1.1 sender and receiver have to agree on where every boundary falls: lay out the target logical address, protocol identifier, reserved and user application octets in order after any path-address bytes, close with the self-delimiting packet, compute each field offset and the shortest unit that can carry them, split a received unit back into named fields, and audit a declared field sequence for a missing field, an invented one or a swapped pair. Refuses a repeated field name and a unit too short to hold the set. Trigger: ecss, e-st-50-53c, packet-transfer-unit-field-order, protocol-data-unit-field-offsets, positional-field-layout, minimum-unit-length, field-sequence-audit."
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
  tags: [ecss, e-st-50-53-packet-transfer-scope, e5053-fields, packet-transfer-unit-field-order, protocol-data-unit-field-offsets, positional-field-layout, minimum-unit-length, field-sequence-audit, unit-encode-decode-round-trip]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Packet Transfer — Unit Fields (space-systems/ecss/e5053-fields)

Use when the task is the field set of ECSS-E-ST-50-53C clause 5.4.1.1 --
not what any one octet means, but which fields the unit is made of, in
what order they appear, and what follows from that being the only thing
that fixes the boundaries.

## Domain quick reference

- The unit is five fields: the target logical address, the protocol
  identifier, the reserved octet and the user application identifier,
  each a single octet in that order, then the packet, which takes the
  rest of the unit.
- Path-address bytes are prepended by the sender and consumed by the
  routers. They are not fields of the unit in the same sense, but they
  shift every offset after them, so the layout is stated relative to the
  path length rather than absolutely.
- The structure is positional from end to end. No field carries a
  length, a tag or a delimiter, so nothing in the unit marks where one
  field stops and the next begins except the count of octets.
- That makes a missing or extra octet uniquely dangerous here. The unit
  does not fail to parse -- it parses into a different, complete,
  entirely plausible unit, and every field after the fault is read from
  the wrong place.
- The packet closes the unit because it is the only field whose length
  is not fixed. It states its own length internally, so placing it last
  is what lets the four octets before it stay positional.
- There is a shortest legal unit: the four single-octet fields plus the
  smallest packet that can exist. A unit below it cannot carry the set
  whatever its contents, and that check costs nothing.
- A declared layout is worth auditing against the required order even
  when the octets parse. A sender that documents its fields in the wrong
  order will eventually build them in that order too.

## Workflow

1. Take the path length and compute the offset of each single-octet
   field and the start of the packet from it. Refuse a negative or
   non-integer path length rather than assuming none.
2. Compute the shortest unit the layout permits and reject anything
   below it before reading a single field.
3. On the build side, write the path bytes first, refusing any that a
   router would keep rather than consume, then the four single-octet
   fields in order, then the packet.
4. Refuse a packet too short to carry its own primary header -- the last
   field is the only one whose length is not fixed, so it is the only
   one that can be silently wrong.
5. On the receive side, check the length, check the declared path bytes
   really sit in the path range, then split the unit into named fields
   at the computed offsets.
6. Audit any declared field sequence separately: report a missing field,
   a field that is not part of the unit, and a pair in the wrong order,
   and keep that verdict distinct from whether the octets decoded.

## Pitfalls

- Trusting that a unit which parses is a unit that was sent correctly. A
  positional structure with no delimiters always parses; the question is
  whether the boundaries were where the sender put them.
- Treating the path bytes as part of the fixed layout. Their number
  varies with the route, so a layout stated in absolute offsets is
  correct for exactly one topology.
- Putting the packet anywhere but last. It is the only variable-length
  field, so any field after it would have no computable offset at all.
- Skipping the minimum-length check. It is the one test that catches a
  truncated unit before the field reads start returning octets from
  whatever followed.
- Reporting a layout audit and a decode as one verdict. A unit can
  decode cleanly while the sender's documented field order is wrong, and
  collapsing the two hides the defect until it is built that way.

## Behavior contract (gate 3)

The field order, offset computation, minimum unit length, unit encoding
and decoding round trip, and the declared-sequence audit are exercised
by the gate 3 contract test: scripts/test_e5053_fields.py against
scripts/e5053_fields_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e5053_fields.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
