---
name: arinc664-afdx
description: "Use when sizing an AFDX network, writing a virtual link configuration table, or reviewing a network design against bandwidth, jitter, and latency budgets for certification. Size and validate ARINC 664 Part 7 Avionics Full-Duplex Switched Ethernet (AFDX) network configurations for civil avionics: compute virtual link bandwidth from the BAG and the maximum frame size, check that the virtual link set fits the 100 Mbps link, bound frame transmission time, verify jitter against the tolerance, estimate end-to-end latency through the switched network, and select the largest legal BAG that still delivers a required bandwidth. Trigger: AFDX, ARINC 664, virtual link, BAG, jitter, end system, avionics network, switched ethernet."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: arinc-664
    reference-only: true
gated: false
domain: avionics
pack: avionics
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: avionics
  subdomain: data-bus
  tags: [afdx, arinc-664, virtual-link, bag, jitter, end-system, switched-ethernet, avionics-network, bandwidth, latency, redundancy, full-duplex]
  version: 0.1.0
  author: Aero Agent Skills
---

# ARINC 664 AFDX Switched Network (avionics/data-bus/arinc664-afdx)

Use when the task is the ARINC 664 Part 7 Avionics Full-Duplex Switched
Ethernet (AFDX) network for civil avionics: virtual link definition and
bandwidth, the bandwidth allocation gap (BAG), the 100 Mbps link
budget, frame transmission time, jitter, end-to-end latency through the
switched network, and dual redundant network design. The module is
data-driven: you supply the virtual link list with BAG and maximum
frame size, and the functions validate bounds, compute bandwidth,
check the link budget, and size the timing margins.

## Domain quick reference

- ARINC 664 Part 7 (AFDX) is deterministic switched Ethernet for civil
  avionics: end systems connect by full-duplex 100 Mbps links to
  switches, typically dual redundant over two independent networks A
  and B.
- A virtual link (VL) is a unidirectional logical path from one source
  end system to one or more destination end systems, defined by a
  bandwidth allocation gap (BAG) and a maximum frame size.
- Legal BAG values are 1, 2, 4, 8, 16, 32, 64, and 128 ms; frames range
  from 64 to 1518 bytes.
- VL bandwidth: max_frame_bytes x 8 / bag_seconds. Worked: 1518-byte
  frames at BAG 4 ms give 3.036 Mbps; at BAG 128 ms, 94.875 kbps.
- Link budget: the sum of all VL bandwidths on one network must not
  exceed the 100 Mbps link. Worked: 30 VLs at 3.036 Mbps use 91.08 Mbps
  (utilization 0.9108); 33 such VLs need 100.188 Mbps, an
  oversubscribed configuration that does not fit.
- Frame transmission time: frame_bytes x 8 / 100 Mbps. Worked:
  1518 bytes serialize in 121.44 us; 64 bytes in 5.12 us.
- Jitter is the variation of frame delivery against the BAG period; a
  typical budget is 500 us. Slack = budget minus measured maximum.
  Worked: measured 420 us leaves 80 us slack; 620 us is a 120 us
  violation.
- End-to-end latency: transmitting end system serialization, plus
  store-and-forward switch delay per switch, plus receiving end system
  serialization. Worked: 1518-byte frame through 2 switches at 150 us
  each totals 542.88 us.
- BAG selection: choose the largest legal BAG whose VL bandwidth still
  meets the requirement, to conserve link capacity. Worked: 1 Mbps with
  1518-byte frames selects BAG 8 ms (1.518 Mbps); 13 Mbps cannot fit any
  BAG at 1518 bytes because the 1 ms BAG caps at 12.144 Mbps.
- Redundancy: the same VL is transmitted on both network A and network
  B, so each network carries the full VL set and the link budget check
  applies per network.
- The exact Part 7 configuration rules, timing budgets, and integrity
  mechanisms are revision-specific standard data; confirm them against
  the current revision before freezing a VL configuration table.

## Workflow

1. List every virtual link with its source and destination end systems
   and its intended BAG and maximum frame size (or its required
   bandwidth).
2. Compute each VL bandwidth with vl_bandwidth(bag_ms,
   max_frame_bytes); an illegal BAG or an out-of-range frame size raises
   ValueError immediately.
3. Check the whole set against the link with
   link_utilization(vl_specs); an oversubscribed set raises ValueError
   and must be re-tuned by enlarging BAGs, shrinking frames, or removing
   VLs.
4. Size the BAGs with largest_bag_for_bandwidth(bandwidth_bps,
   max_frame_bytes) to conserve link capacity.
5. Bound the timing: transmission_time(frame_bytes) for serialization,
   jitter_slack(measured_max_jitter_us, jitter_budget_us) for the
   jitter verdict (negative slack is a violation), and
   end_to_end_latency_us(frame_bytes, switch_count, switch_delay_us)
   for the worst-case one-way latency.
6. Verify redundancy: the VL set fits each of the A and B networks
   independently, with the utilization check run per network.
7. Record the VL configuration table (BAG, max frame size, computed
   bandwidth, jitter slack, end-to-end latency) for the certification
   package and the network integrator.

## Pitfalls

- Routing this leaf: AFDX is the switched data network; ARINC 429 word
  encoding (octal label, SDI, BNR/BCD, odd parity) routes to
  arinc429-protocol, and MIL-STD-1553 command/response buses route to
  mil-std-1553. A 429 label decode or a 1553 command word is not an
  AFDX question.
- Routing network timing here: AFDX jitter and latency budgets are this
  leaf; equipment immunity to conducted or radiated RF (CS114, RS103)
  routes to do160/radio-frequency-susceptibility, and equipment power
  characteristics (voltage limits, sag/surge) route to do160/power-input.
- Confusing the data network with the electrical power bus: the word
  "bus" in AFDX means the switched network path (the virtual link), not
  the aircraft electrical power distribution bus; power bus architecture
  and protection questions belong to the electrical certification and
  power leaves, not here.
- BAG must be a power of two from 1 to 128 ms: 3 ms or 5 ms is invalid.
- Frame sizes outside 64-1518 bytes are invalid for AFDX; do not apply
  802.3 jumbo frame sizes to a VL configuration.
- Oversubscription is a configuration error: the sum of VL bandwidths
  must fit the 100 Mbps link on each redundant network; a set that
  needs more capacity must be re-tuned, not force-fitted.
- BAG selection direction: pick the LARGEST legal BAG that still meets
  the required bandwidth; a smaller BAG only wastes link capacity.
- Jitter and latency are different budgets: jitter bounds the variation
  of frame delivery against the BAG period; latency bounds the total
  one-way delivery time. A configuration can meet one and violate the
  other.
- Treating the VL configuration as fixed: BAG-to-bandwidth assignments,
  timing budgets, and integrity rules are revision-specific standard
  data; confirm every value against the current revision before
  freezing the interface.

## Behavior contract (gate 3)

The VL bandwidth, link utilization, transmission time, jitter slack,
end-to-end latency, and largest-BAG selection helpers are exercised by
the gate 3 contract test: scripts/test_arinc664_afdx_logic.py against
scripts/arinc664_afdx_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_arinc664_afdx_logic.py

## Compliance

- Standards referenced, not reproduced: the governing ARINC 664 Part 7
  text is proprietary (ARINC/SAE ITC) and is not yet in
  standards-map.yaml; this leaf keys to the closest existing map entry,
  arinc-429 (data-bus family sibling), listed reference-only. Summary
  only per standards-map.yaml.
- The module implements the sizing and timing helpers from common
  engineering practice; no standard table is embedded in the code or
  this page.
- compliance: STANDARDS-REF, gated: false.
