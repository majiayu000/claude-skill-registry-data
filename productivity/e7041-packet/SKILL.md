---
name: e7041-packet
description: "Extract the whole space packet a packet-typed parameter carries, under ECSS-E-ST-70-41C clause 7.3.13. Use when a dump report, a forwarded telecommand or a rejection report carries another packet as its value: keeping the contained packet's own primary header rather than stripping it, deriving its size from the packet-length field inside it instead of from any length declared beside it, and splitting a container of back-to-back packets by walking those lengths, so one packet that misstates its own length is caught as a finding before it desynchronises every packet after it. Trigger: ecss, e-st-70-41c, pus-packet-typed-parameter, contained-space-packet-extraction, derived-packet-length-field, packet-store-dump-splitting, forwarded-telecommand-container, container-desynchronisation."
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
  tags: [ecss, e-st-70-41-packet-utilisation-scope, e7041-packet, pus-packet-typed-parameter, contained-space-packet-extraction, derived-packet-length-field, packet-store-dump-splitting, container-desynchronisation]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Packet Utilisation — Packet Data Type (space-systems/ecss/e7041-packet)

Use when the task is the packet data type of ECSS-E-ST-70-41C clause
7.3.13 — the two normative items that let a parameter's value be
another space packet, and everything a reader depends on to find where
that packet ends.

## Domain quick reference

- Some parameters carry neither a number nor a string but another
  packet, whole. A packet-store dump report carries the stored
  packets; a forwarded telecommand carries the command it forwards; a
  report of a rejected request carries the request.
- Nothing is stripped. The contained packet keeps its own primary
  header, and that is what makes it a packet rather than a payload:
  the receiver can identify, route and sequence it exactly as if it
  had arrived on its own.
- Its length is not declared alongside it. It is derived from the
  packet-length field inside the contained packet, in the last two
  octets of its six-octet primary header. That field states the number
  of octets in the data field minus one, so the total is that value
  plus seven.
- The minus-one is not a quirk to work around. A data field of one
  octet states zero, which is why a packet can never be header-only,
  and a sixteen-bit field therefore reaches a data field of 65536
  octets rather than 65535.
- A container of several packets has no table of offsets. The reader
  finds the second packet by having read the length out of the first.
  So a packet that misstates its own length does not corrupt one
  entry: it desynchronises the container, and every packet after it is
  read from the middle of its predecessor.
- A separately declared field length is never trusted over the derived
  one. It is compared with it, and a disagreement is a definition
  defect reported before anything is parsed.
- Trailing octets that are too few for a primary header mean the
  container did not end on a packet boundary. That is a finding about
  the container, not about the last packet.

## Workflow

1. Normalise the value to octets first, refusing anything that is not
   a buffer; a packet parameter parsed out of a text field is already
   a different problem.
2. Read the length field out of the contained packet's own header at
   the offset in hand, refusing an offset with fewer than six octets
   behind it — the length cannot be read at all there.
3. Derive the total as the stated value plus seven, and check it
   against the octets actually remaining before slicing.
4. Return the packet whole, header included, together with the offset
   the next one starts at, so a caller walks the container rather than
   indexing into it.
5. Where a count of contained packets is declared, split the whole
   container and compare, rather than stopping after the declared
   number — a mismatch in either direction is evidence.
6. Where a field length is declared as well, reconcile it against the
   derived length and refuse on disagreement.
7. Report the recovered packets, the octets consumed, the octets
   trailing and every finding together, so a desynchronised container
   is diagnosed once instead of once per packet.

## Pitfalls

- Stripping the contained packet's primary header to save space. What
  is left cannot be identified or routed, and the container has to
  invent the metadata back.
- Trusting a declared field length over the derived one. The derived
  length is what the receiver on board used; the declared one is what
  somebody typed.
- Reading the length field as the data-field size. It is one less, and
  the off-by-one reads every subsequent packet one octet early.
- Stopping a split at the declared count. A container holding more
  than it declares still has the extra octets, and they are evidence
  of the defect rather than padding.
- Treating a truncated packet as one lost entry. Everything after it
  in the container is lost too, because its start was never located.
- Padding a container to an alignment boundary. Trailing octets are
  indistinguishable from the start of a packet whose header was cut.

## Behavior contract (gate 3)

The octet-buffer validation, length-field reading, derived total size,
whole-packet extraction with its next offset, back-to-back container
splitting, declared-count and declared-length reconciliation and the
whole-container assessment are exercised by the gate 3 contract test:
scripts/test_e7041_packet.py against scripts/e7041_packet_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_e7041_packet.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
