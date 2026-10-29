---
name: dhcp-attacks
description: Use when assessing DHCP security on an authorized network
  or lab. Covers rogue DHCP servers, DHCP starvation, option
  injection, and DHCP snooping review. Also use when reviewing how
  clients get network configuration on untrusted segments.
version: 1.0.0
domain: network
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [nmap-methodology, arp-spoofing, vlan-hopping]
tools:
  - name: Python
    version: "3.12"
  - name: Wireshark
    version: "4.4"
---

DHCP hands out IP addresses, gateways, and DNS with no authentication:
whoever answers first wins. A rogue server makes itself the gateway
and sees everything; starvation denies addresses to everyone. This
skill covers authorized lab testing: standing up a rogue server,
starving the pool, and reviewing DHCP snooping. Lab or written
authorization only; rogue DHCP on production is disruptive.

## Quick Workflow

1. Observe normal DHCP: capture the DORA sequence and note the real
   server, pool, and options.
2. Review switch config for DHCP snooping and rate limiting.
3. In the lab, run a rogue server and confirm clients take its
   gateway and DNS.
4. Demonstrate the MITM: traffic flows through your lab host.
5. Test starvation: exhaust the pool and watch new clients fail.
6. Check option injection: WPAD, DNS, and boot options the rogue can
   push.
7. Tear down the rogue and confirm the network recovers.
8. Recommend snooping, allowed server lists, and 802.1X.

## 1. Observation and rogue server (lab)

```bash
# Capture the normal DHCP exchange
sudo tshark -i eth0 -Y "dhcp" -a duration:60 | head -20
# Note: server IP, offered gateway, DNS, lease time, pool hints
```

```bash
# Lab: rogue DHCP server with your host as gateway (authorized lab net)
# dnsmasq as tooling:
sudo dnsmasq --interface=eth0 --bind-interfaces \
  --dhcp-range=192.168.99.50,192.168.99.150,12h \
  --dhcp-option=3,192.168.99.1 \
  --dhcp-option=6,192.168.99.1 \
  --port=0
# From a lab client: dhclient -r; dhclient; then check gateway and DNS
ip route | grep default
cat /etc/resolv.conf
```

## 2. Starvation test (lab)

```python
#!/usr/bin/env python3
"""DHCP starvation sketch (lab only, scapy as tooling)."""
print("loop: send DHCPDISCOVER with random chaddr (fake MACs)")
print("server leases an address per MAC until the pool is empty")
print("measure: legitimate client gets no offer after exhaustion")
print("stop condition: agreed count or first client failure, then halt")
```

```bash
# Option injection to review: WPAD (252), DNS (6), boot server (66/67)
# A rogue pushing WPAD can redirect browser proxy config: check whether
# clients honor it, and whether the real network even uses WPAD
grep -i wpad /tmp/dhcp_capture.txt | head -5
```

## Edge cases

- DHCP snooping is on and blocks your rogue. That is the control
  working; verify the trusted ports list is correct and move on.
- The network uses DHCPv6. The same attacks apply; test the v6 path
  separately.
- Clients have static IPs. DHCP attacks do not affect them; note
  the mixed environment.

## Escalation

- Rogue works: the finding is the missing snooping; demonstrate the
  traffic interception once, then tear down.
- Starvation works: recommend rate limiting plus snooping; note that
  starvation is also a DoS primitive worth monitoring.

## Detection and defender view

Defenders see DHCP attacks as multiple servers answering discovers,
pool exhaustion, and clients with unexpected gateways. Detect with
DHCP snooping bindings, alerts on new DHCP servers, and monitoring
for gateway changes on clients. The durable fix is DHCP snooping
with trusted ports, dynamic ARP inspection paired with it, and
802.1X so rogue devices never get a port.

## Key references

- CWE-306 (Missing Authentication for Critical Function).
- RFC 2131 (DHCP): no authentication by design.
- DHCP snooping vendor documentation.
