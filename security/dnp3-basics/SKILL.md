---
name: dnp3-basics
description: Use when you need working knowledge of DNP3 for an OT
  assessment or lab. Covers DNP3 architecture (master and outstation),
  addressing, function codes, Secure Authentication basics, and where
  DNP3 appears in electric utility and water networks. Also use when
  assessing serial or TCP DNP3 links on an authorized engagement.
version: 1.0.0
domain: ics-scada
lifecycle: stable
last_verified: '2026-10-23'
requires: []
extends: []
relates: [modbus-security, scada-network-seg, plc-basics]
tools:
  - name: Wireshark
    version: '4.4'
  - name: Python
    version: '3.12'
  - name: nmap
    version: '7.98'
---

DNP3 is the workhorse protocol of electric utilities and water systems:
masters poll outstations for measurements and send control commands.
Like Modbus it was built without security, though Secure Authentication
adds a challenge response layer many deployments skip. This skill gives
the working knowledge and authorized assessment basics: architecture,
addressing, what to look for on the wire, and how to test safely.

## Quick Workflow

1. Learn the roles: masters (control center) poll outstations (field
   devices) by address.
2. Identify DNP3 on the network: TCP port 20000, or serial links via
   converters.
3. Capture traffic passively first and decode it in Wireshark.
4. Map master to outstation addresses and the poll patterns.
5. Check whether Secure Authentication is actually enabled.
6. Review what function codes are in use, especially direct operate
   commands.
7. Only with authorization, test read functions; treat controls as
   sensitive as Modbus writes.
8. Report exposure with the same care as any OT protocol.

## 1. Architecture and addressing

```text
Master (address e.g. 1) ----polls----> Outstation (address e.g. 10)
  - integrity poll: read all static points periodically
  - event poll: read only changed points (fast, efficient)
  - unsolicited responses: outstation reports urgent events itself
  - controls: SELECT then OPERATE (two step), or DIRECT OPERATE
```

```bash
# Find DNP3 over TCP on the authorized segment (gentle scan)
sudo nmap -sS -p 20000 --open -T2 --max-retries 1 \
  192.168.10.0/24 -oN /tmp/dnp3_disc.txt
grep -B2 open /tmp/dnp3_disc.txt | head
```

```bash
# Capture and decode DNP3 in Wireshark (it has a full dissector)
sudo tshark -i eth0 -f "tcp port 20000" -w /tmp/dnp3.pcap &
sleep 120; kill %1
tshark -r /tmp/dnp3.pcap -T fields \
  -e dnp3.al.ctrl -e dnp3.hdr.src -e dnp3.hdr.dst -e dnp3.al.func \
  | sort | uniq -c | sort -rn | head -20
```

## 2. Secure Authentication check

DNP3 Secure Authentication (SAv5/SAv6) adds challenge response between
master and outstation. Check whether it is on:

```bash
# In the capture, look for authentication objects (group 120)
tshark -r /tmp/dnp3.pcap -Y "dnp3.al.obj == 120" | head -10
# No group 120 traffic during session start = no Secure Authentication
```

```bash
# Also check the device config with operations: which DNP3 security
# mode is configured, and are the pre shared keys managed or default
echo "ask: SAv version, key change procedure, key storage"
```

Without Secure Authentication, DNP3 has no integrity or
authentication: injected packets are trusted. With it, review key
management, since shared keys that never rotate are barely better.

## Edge cases

- DNP3 over serial through a terminal server. The TCP endpoint is the
  converter; the serial side needs physical access to tap.
- Encrypted with TLS wrappers or a VPN. Assess the wrapper's config;
  the protocol inside is still unauthenticated.
- Unsolicited responses flood during events. Do not mistake an event
  storm for an attack; correlate with operations first.
- Address 65535 is broadcast. Never send broadcast controls.

## Escalation

- Need active testing: limit to read function codes (1, 129) during
  the agreed window, and only with operations watching.
- Controls in scope: treat like OT writes, one at a time, announced,
  on lab or maintenance window hardware.
- Serial only access: use a serial tap and decode offline; do not
  insert yourself in the serial path of a live process.

## Detection and defender view

Defenders monitor DNP3 for new masters, function codes outside the
baseline (especially controls), and outstation address scans. With
Secure Authentication, they watch for authentication failures that
signal spoofing attempts. The durable defense is network isolation of
the SCADA segment, Secure Authentication with managed keys where the
devices support it, and an allowlist IDS that knows the normal poll
patterns.

## Key references

- MITRE ATT&CK ICS T0855 (Unauthorized Command Message).
- IEEE 1815: DNP3 protocol standard.
- DNP3 Secure Authentication (IEEE 1815-1): SAv5/SAv6.
