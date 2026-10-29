---
name: plc-basics
description: Use when you need working knowledge of programmable logic
  controllers for an OT assessment or lab. Covers PLC architecture,
  scan cycle, ladder logic reading, common vendors and protocols, and
  how PLCs fit into the Purdue model. Also use when OT findings need
  translation into physical impact for the report.
version: 1.0.0
domain: ics-scada
lifecycle: stable
last_verified: '2026-10-23'
requires: []
extends: []
relates: [modbus-security, scada-network-seg, ics-incident-response]
tools:
  - name: Python
    version: '3.12'
  - name: Wireshark
    version: '4.4'
---

A PLC is a rugged computer that runs one program in a loop: read
inputs, run logic, write outputs. Everything in OT security comes back
to this loop and to the fact that stopping or changing it has physical
consequences. This skill gives the foundations: architecture, scan
cycle, ladder logic, vendors, and where PLCs sit in the network. It is
prerequisite knowledge for the protocol and incident skills.

## Quick Workflow

1. Learn the architecture: CPU, I/O modules, comms modules, and the
   engineering workstation that programs it.
2. Understand the scan cycle: input scan, logic solve, output scan,
   housekeeping, repeat.
3. Read basic ladder logic: contacts, coils, timers, and counters.
4. Map the common vendors to their protocols and software.
5. Place the PLC in the Purdue model: Level 1 controller, Level 2
   supervisory.
6. Learn the operating modes: RUN, PROGRAM, and REMOTE, and what each
   allows over the network.
7. Understand why availability beats confidentiality in OT priorities.
8. Use this model to translate technical findings into physical impact.

## 1. Scan cycle and ladder logic

The scan cycle is the heartbeat. Logic that takes too long or faults
stops the process.

```bash
# Conceptual scan cycle (what the PLC does every few milliseconds):
# 1. INPUT SCAN: copy physical inputs to the input image table
# 2. LOGIC SOLVE: run the program top to bottom, left to right
# 3. OUTPUT SCAN: copy the output image table to physical outputs
# 4. HOUSEKEEPING: comms, diagnostics, watchdog
echo "scan time matters: logic must finish before the watchdog trips"
```

Ladder logic reads like relay schematics. Learn the symbols:

```text
--| |--  normally open contact (true when the input is on)
--|/|--  normally closed contact (true when the input is off)
--( )--  coil / output (energized when the rung is true)
--(S)--  set (latch on), --(R)-- reset (latch off)
--TON--  timer on delay, --CTU-- count up

Example rung: motor runs when START is pressed and STOP is not pressed
  START   STOP    MOTOR
--| |---|/|-------( )--
```

```bash
# When reviewing exported PLC programs, search for safety critical rungs
grep -ai -E "estop|emergency|interlock|safety" /tmp/plc_export.txt | head -20
# Rungs that can be forced or bypassed remotely are high impact findings
```

## 2. Vendors, protocols, and modes

```bash
# Common vendor to protocol map (know what you are looking at)
python3 - << 'PY'
vendors = {
    "Siemens S7": "S7comm (port 102), TIA Portal software",
    "Rockwell/Allen-Bradley": "EtherNet/IP (port 44818), Studio 5000",
    "Schneider Modicon": "Modbus TCP (port 502), EcoStruxure",
    "Mitsubishi": "MELSEC protocol, GX Works",
    "Omron": "FINS (port 9600), CX-One",
}
for v, p in vendors.items():
    print(f"{v}: {p}")
PY
```

Operating modes control what the network can do:

```text
RUN:     program executes; logic writes may be blocked or allowed
PROGRAM: CPU halted; full program upload/download allowed
REMOTE:  mode can be changed over the network (risky if unauthenticated)
```

A PLC in REMOTE with no authentication lets anyone on the segment stop
the process. That single fact drives much of OT network design.

## Edge cases

- The PLC program is password protected. Note it; do not crack OT
  passwords without explicit authorization and a maintenance window.
- Redundant PLC pairs: changing one may trigger failover behavior you
  did not expect; coordinate with operations.
- Safety PLCs are separate from process PLCs. Never test safety
  systems; they protect people, not production.
- Old PLCs have no authentication at all. The finding is the network
  architecture, not the PLC.

## Escalation

- Need deeper protocol testing: move to the protocol skills
  (modbus-security, opc-ua-security) for the specific device.
- Need the network picture: use scada-network-seg for Purdue mapping.
- Incident in progress: switch to ics-incident-response immediately.

## Detection and defender view

Defenders protect PLCs with network segmentation, mode control (key
switches out of REMOTE), program change detection (hash the logic and
alert on change), and engineering workstation hardening. They detect
attacks through unexpected program downloads, mode changes, and
traffic from unknown hosts to PLC ports. The durable principle: the
PLC trusts the network, so the network must be trustworthy.

## Key references

- MITRE ATT&CK for ICS: full technique matrix.
- NIST SP 800-82r3: Guide to OT Security.
- IEC 62443: industrial automation security standard series.
