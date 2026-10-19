---
name: hardware-ot-ics
description: >
  Assess OT/ICS environments — PLC, SCADA, DCS, HMI — safely and passive-first: Purdue-model
  zoning, industrial protocol discovery (Modbus, S7, DNP3, EtherNet/IP), mirrored-traffic analysis,
  and read-only verification. Load for an authorized engagement touching industrial control
  networks, engineering workstations, historians, or IT/OT boundaries. Signals: ports 502, 102,
  44818, 20000; Modbus/S7comm banners; PLC/RTU inventory requests.
domain: hardware
type: methodology
stability: learning
modes: [pentest, defense]
severity: high
mitre: [T0846, T0842]
cwe: [CWE-306]
tools: [wireshark, tshark, nmap, binwalk, ghidra]
schema_version: 1
---

# OT / ICS security assessment (passive-first)

## When it applies
The engagement touches an industrial environment — PLC/RTU controllers, SCADA/DCS, HMIs,
engineering workstations, historians, jump hosts, or the IT/OT boundary (firewall rules, data
diodes). **A misstep here can cause physical harm, not just downtime.** Load `tradecraft-scope-roe`
and require the written authorization to spell out: the site and network segments, whether active
scanning is allowed, and whether writing coils/registers is allowed — **the default for both is
NO**. Work passive-first; nothing touches a PLC's state until the scope explicitly says so.

## Why it works
Industrial protocols (Modbus, S7comm, DNP3, EtherNet/IP) predate hostile networks: they run in
cleartext with no authentication (`CWE-306`), so anyone who can reach the port can read process
state — and usually write it. That's exactly why the assessment itself is the risk: a high-rate
scan or a stray write can trip a control loop or a safety instrumented system (SIS). Mirrored
traffic and offline artifacts reveal the same exposure with zero packets injected.

## Iron rules (MUST)
- **Never write coils/registers** to a PLC unless the authorization explicitly permits it.
- **No high-rate scanning** of production OT segments — low rate, maintenance window only.
- **Never touch SIS paths** or anything in a safety loop.
- Prefer, in order: read-only identification → traffic mirroring → offline firmware/config analysis.
- An anomaly or unexpected device response → **stop immediately and notify** the site contact.

## Method
1. **Zone and inventory (paper-first).** Sketch the Purdue levels L0–L5: field devices → basic
   control → supervisory → site DMZ → enterprise. Build the asset list — PLC/RTU/HMI/engineering
   workstation/historian/jump host — and the expected protocol/port baseline for the authorized
   segments only (identification, not exploitation): Modbus/TCP **502**, S7comm **102**,
   EtherNet/IP **44818**, DNP3 **20000**.
2. **Passive capture.** Take a SPAN/mirror-port PCAP from an authorized tap:
   `tshark -i <iface> -w ot-mirror.pcap`. Dissect it with Wireshark's ICS dissectors (modbus,
   s7comm, enip, dnp3) — you learn the live devices, the masters/slaves, the function codes in use,
   and any cleartext credentials without sending a single packet. A proprietary protocol on the
   wire goes to `reverse-eng-protocol`.
3. **Offline audit.** Review exported controller configuration and engineering projects (TIA
   Portal, RSLogix/Studio 5000 exports) offline. Record default credentials and unauthenticated
   cleartext protocols (Modbus has none) as findings — **observe and document; change nothing**.
4. **Limited active checks — only if the scope says yes.** During the agreed maintenance window,
   at low rate (`nmap -Pn -n --max-rate 20 -p 502,102,44818,20000 <host>`, plus targeted NSE
   identification such as `--script modicon-info,s7-info,enip-info`), prefer read-only function
   codes, capture evidence for every step, and stop + escalate at the first anomaly.
5. **Firmware and patch surface.** Map controller firmware versions to known CVEs (never blind-flash
   firmware). Pull images for offline analysis with `reverse-eng-firmware` and `reverse-eng-binary-triage`
   rather than probing the live controller.
6. **Report with physical consequence.** Every OT finding states its process/physical impact
   (what an attacker could make the plant *do*), and distinguishes remotely exploitable issues from
   ones requiring physical or control-network access. Lateral movement into the IT side follows
   `network-pivoting-tunneling` and the `ad` domain skills as usual.

## Gotchas
- **A port scan is an active act on OT.** Some PLCs fault or reboot under ordinary scan rates —
   mirrored traffic first, always. Don't run default-parameter web/network scanners against OT
   segments; the profiles are wrong and the risk is real.
- **"No response" may mean you hurt something, not that nothing's there** — if a device goes quiet
   mid-test, stop and notify; check with the site before resuming.
- **Most ICS tooling assumes an isolated lab network** — stage and rehearse tools in a lab VLAN or
   on a mirrored feed, not on the production segment.
- **Default creds and no-auth protocols are findings, not invitations** — log them, prove reachability
   minimally, never exercise a write "to demonstrate".
- **Confirm the emergency contact and rollback plan exist before any active phase** — including the
   maintenance window and who can halt the test.

## Verify success
You can produce: the Purdue-zone sketch with a reconciled asset inventory, the observed
protocol/port baseline from passive capture, a findings list with physical-impact framing
(remote vs physical reachability stated per finding), and — for any authorized active step — a
step-by-step evidence trail showing read-only behavior and zero unplanned state changes.

## References
NIST SP 800-82 (ICS security); ATT&CK for ICS; Wireshark ICS dissector docs; `reverse-eng-firmware`.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
