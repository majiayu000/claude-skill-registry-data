---
name: stp-attacks
description: Use when assessing Spanning Tree Protocol on an authorized
  network or lab. Covers STP root takeover, BPDU guard review, and
  topology manipulation. Also use when reviewing switch hardening on
  enterprise or campus networks.
version: 1.0.0
domain: network
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [vlan-hopping, nmap-methodology]
tools:
  - name: Python
    version: "3.12"
  - name: Wireshark
    version: "4.4"
---

Spanning Tree elects a root bridge to prevent loops, and it trusts
BPDU messages from any port: an attacker who becomes root sees
traffic and can reshape the topology. This skill covers authorized
lab testing: observing STP, attempting root takeover, and reviewing
the guards that stop it. Lab switches or written authorization only;
STP games on production can take the network down.

## Quick Workflow

1. Observe STP passively: capture BPDUs and note the current root.
2. Review the switch configs: root guard, BPDU guard, and priority
   settings.
3. In the lab, attempt root takeover with a superior BPDU.
4. Verify the impact: traffic paths change, and the attacker sees
   more.
5. Test the guards: does BPDU guard shut the port as configured.
6. Check for STP manipulation as a MITM primitive in the report.
7. Restore the lab topology and confirm the real root returns.
8. Recommend the guard configuration per port role.

## 1. Observation and root takeover (lab)

```bash
# Capture BPDUs and identify the root bridge
sudo tshark -i eth0 -Y "stp" -a duration:20 | head -10
# Note: root bridge ID, root path cost, and which port you are on
```

```bash
# Lab: send a superior BPDU to claim root (Yersinia or scapy as tooling)
# yersinia stp -attack 2 -interface eth0
# Then re-capture: if your bridge ID is now root, the takeover worked
sudo tshark -i eth0 -Y "stp" -a duration:20 | grep -i "root" | head -5
```

```bash
# Verify traffic impact in the lab: paths reconverge through you
# (measure with traceroute between lab hosts before and after)
traceroute 192.168.1.20
```

## 2. Guard review

```bash
# Config review checklist per port:
# - access ports: BPDU guard ON (shuts port on any BPDU)
# - uplinks to real switches: root guard ON (blocks superior BPDUs)
# - core: explicit root priority set (4096), never left to election
# - unused ports: shutdown
grep -i -A2 "spanning-tree" /tmp/switch_config.txt | head -30
```

## Edge cases

- The network runs RSTP or MSTP. The attack shape is the same;
  verify the guard names in the vendor syntax.
- BPDU guard err-disables your test port. That is the control
  working; recover the port per the runbook and note the success.
- Wireless or virtual switches in the path. They may not speak STP;
  the wired edge is still where you test.

## Escalation

- Takeover works in the lab: the finding is the missing guards;
  recommend per the checklist and retest.
- Production review only: grade configs without sending BPDUs.

## Detection and defender view

Defenders see STP attacks as topology changes, root bridge flaps,
and BPDU guard err-disable events. Detect with SNMP traps on STP
changes and monitoring of the root bridge identity. The durable fix
is the guard trio: BPDU guard on access ports, root guard on
distribution uplinks, and a pinned root priority on the intended
core.

## Key references

- IEEE 802.1D/802.1w: STP/RSTP standards.
- CWE-923 (Improper Restriction of Communication Channel).
- Vendor STP hardening guides.
