---
name: vlan-hopping
description: Use when testing VLAN segmentation on an authorized
  network assessment or lab. Covers switch spoofing, double tagging,
  DTP negotiation abuse, and validating that VLANs actually isolate.
  Also use when a flat feeling network claims VLAN separation.
version: 1.0.0
domain: network
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [nmap-methodology, firewall-evasion, zero-trust-networking]
tools:
  - name: Python
    version: "3.12"
  - name: nmap
    version: "7.98"
---

VLANs separate traffic on shared switches, but misconfigurations let
attackers hop between them: trunking negotiated by the attacker, or
double tagged frames the switch forwards to the wrong VLAN. This skill
covers authorized testing in labs or with written permission:
checking switch port configs, attempting the hop techniques, and
proving whether isolation holds. Never test on production networks
without explicit authorization.

## Quick Workflow

1. Get the VLAN map and the switch port configurations under review.
2. Check for DTP: ports that negotiate trunking automatically are the
   classic hole.
3. Test switch spoofing from an authorized test port: try to become a
   trunk.
4. Test double tagging: craft frames with two VLAN tags and see where
   they land.
5. Verify inter VLAN routing: which VLANs can actually reach each
   other through the router.
6. Check native VLAN and unused ports: both are common mistakes.
7. Document every hop that worked with the exact frames.
8. Recommend the hardening: trunk only where needed, DTP off.

## 1. Switch spoofing test

```bash
# From the authorized test host, check if the port negotiates trunking
# (DTP frames tell you; or try to form a trunk with Yersinia in the lab)
# Passive check first: listen for DTP/CDP
sudo tshark -i eth0 -Y "dtp or cdp" -a duration:30 | head -10
# DTP frames visible = the switch speaks DTP on this port
```

```bash
# Lab: attempt trunk formation (authorized lab switch only)
# yersinia dtp -attack 1 -interface eth0
# Then check: ip link show | grep -i vlan, and try tagging frames
echo "if the port becomes a trunk, all VLANs are reachable: critical"
```

## 2. Double tagging test

```python
#!/usr/bin/env python3
"""Double tagged frame crafter (lab/authorized only, scapy as tooling)."""
# Outer tag: your native VLAN; inner tag: the target VLAN.
# Some switches strip only the outer tag and forward on the inner one.
print("frame: eth / dot1q(vlan=NATIVE) / dot1q(vlan=TARGET) / arp who-has")
print("send from the authorized test port, listen on the target VLAN")
print("success = reply arrives: the hop works")
```

```bash
# Inter VLAN routing check: which VLANs route to each other
# From a host in VLAN 10 (authorized), probe VLAN 20 addresses
sudo nmap -sS -T3 --max-retries 1 192.168.20.1-10 -oN /tmp/vlan_route.txt
grep -c open /tmp/vlan_route.txt
# Reachable = routing allowed; compare against the intended policy
```

## Edge cases

- The switch ignores your trunk attempt. Good; verify DTP is off in
  the config and move on.
- Double tagging fails because the native VLAN differs. Adjust to
  the actual native VLAN from the config.
- The test port is 802.1X authenticated. Hopping needs the
  supplicant first; note the 802.1X as the effective control.

## Escalation

- Hop succeeds: demonstrate access to a sensitive VLAN host, then
  stop; the segmentation failure is proven.
- Config review only (no active tests allowed): grade each port's
  config against the hardening checklist and report.

## Detection and defender view

Defenders see VLAN hopping as DTP negotiation from access ports,
frames with unexpected double tags, and MAC addresses appearing on
multiple VLANs. Detect with switch logs, DTP disabled alerts, and
IDS on trunk ports. The durable fix is configuration: DTP off
everywhere except real trunks, explicit trunk allowed lists, unused
ports shut down, and a native VLAN nobody uses.

## Key references

- CWE-923 (Improper Restriction of Communication Channel to Intended
  Spheres).
- VLAN hopping research (Cisco, Black Hat presentations).
- Switch vendor hardening guides.
