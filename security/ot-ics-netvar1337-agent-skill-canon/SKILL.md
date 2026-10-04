---
name: ot-ics
description: "Use for authorized OT/ICS security assessment covering Purdue model zoning, PLC/SCADA exposure, industrial protocol discovery, and safe passive-first evaluation."
version: 1.0.0
license: MIT
metadata:
  package: unleash-skills
  author: NetVar1337/unleash
  category: reverse-skill
  upstream: https://github.com/zhaoxuya520/reverse-skill
---

> Bundled with Unleash skills pack. Upstream: https://github.com/zhaoxuya520/reverse-skill

# OT / ICS Security

## ACTION REQUIRED (execute immediately after reading)

1. `NOW`: read `../field-journal/precedent-pentest.md` — **mistakes in OT environments can cause physical harm**
2. `NOW`: written authorization must state clearly: sites, network segments, whether active scanning/register writes are allowed
3. `NOW`: case-init; **passive-first** by default; no PLC write operations before `ready_for_act`
4. `NEXT`: tool-index; most OT tools need manual setup and an isolated lab network
5. `ACT`: asset and zone identification → exposure surface → read-only verification

## Applicable Scenarios

- OT/SCADA/DCS security assessment (authorized)
- Purdue model zoning and cross-zone channels
- Modbus/DNP3/S7/EtherNet/IP protocol exposure
- Engineering stations, HMIs, historians, jump hosts
- IT/OT convergence boundaries (firewall rules, unidirectional gateways)

## Safety Iron Rules (MUST)

```text
MUST NOT, without explicit permission:
- Write coils/registers to PLCs
- High-rate full-network scans of production OT
- Interrupt safety instrumented system (SIS) related paths
Prefer: read-only identification, traffic mirroring, offline firmware/config analysis
```

## Workflow

### Phase 1 — Zones and Assets

```text
□ Sketch Purdue L0–L5: field devices → control → supervisory → site DMZ → enterprise
□ Asset inventory: PLC/RTU/HMI/engineering station/historian/jump host
□ Protocol and port baseline (authorized segments only)
```

### Phase 2 — Passive and Read-Only

```text
□ SPAN/mirrored PCAP → protocol-reverse / Wireshark OT dissectors
□ Offline audit of configuration and project files (TIA/RSLogix exports etc.)
□ Record default passwords and cleartext protocols (Modbus has no auth) as Findings; do not write to disk or change values
```

### Phase 3 — Restricted Active (authorized only)

```text
□ Low-rate identification, during maintenance windows
□ Read-only function codes first
□ Evidence at every step; stop immediately and report on any anomaly
```

### Phase 4 — Firmware/Patch Surface

```text
□ Controller firmware versions → CVE mapping (do not blindly flash firmware)
□ Combine with firmware-pentest for offline image analysis
```

## Toolchain

| Tool | Purpose | Note |
|------|------|------|
| Wireshark OT dissectors | Passive parsing | Mirrored traffic |
| Nmap NSE (restricted) | Identification | Rate and time window |
| Claroty/Nozomi etc. | Asset discovery | Commercial/on-site |
| PLC vendor engineering software | Config auditing | Offline preferred |
| binwalk / Ghidra | Firmware | Offline |

## References

- `references/ot-safe-assessment.md`
- `../firmware-pentest/` `../protocol-reverse/` `../network` via pentest-tools

## Routing Context

**Upstream**: MASTER R28  
**Downstream**: deep firmware digging `firmware-pentest`; protocols `protocol-reverse`; IT lateral movement `windows-ad`/`attack-chain`  
**Peers**: do not hit OT with default web-scan parameters

## Task Completion Self-Check

- [ ] Passive/read-only by default with authorization boundaries recorded?
- [ ] Avoided write operations to control loops (unless explicitly allowed)?
- [ ] Findings include physical/process impact notes?
- [ ] Checklist / journal?
