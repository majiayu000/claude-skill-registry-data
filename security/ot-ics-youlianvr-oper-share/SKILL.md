---
name: ot-ics
description: Use for authorized OT/ICS security assessment covering Purdue model zoning, PLC/SCADA exposure, industrial protocol discovery, and safe passive-first evaluation.
---

# OT / ICS Security

## Authorization preamble

1. **OT mistakes can cause physical harm** — written authorization is mandatory.
2. Authorization must state: site, network segments, whether active scanning / register writes are allowed.
3. Open a case; **passive-first by default**; no writes to PLCs before `ready_for_act`.
4. Most OT tools are manual installs and need an isolated lab network — verify first.
5. Order: asset and zoning identification → exposure → read-only verification.

## Scope

- ICS/SCADA/DCS security assessment (authorized)
- Purdue model zoning and cross-zone channels
- Modbus / DNP3 / S7 / EtherNet/IP protocol exposure
- Engineering workstations, HMIs, historians, jump hosts
- IT/OT convergence boundary (firewall rules, data diodes)

## Safety iron rules (MUST)

```text
MUST NOT unless explicitly permitted:
- Write coils/registers to PLCs
- Full-network high-rate scans of production OT
- Interrupt paths related to the safety instrumented system (SIS)
Prefer: read-only identification, traffic mirroring, offline firmware/config analysis
```

## Workflow

### Phase 1 — Zoning and assets

```text
□ Purdue L0–L5 sketch: field devices → control → supervisory → site DMZ → enterprise
□ Asset inventory: PLC/RTU/HMI/engineering station/historian/jump host
□ Protocol and port baseline (authorized segments only)
```

### Phase 2 — Passive and read-only

```text
□ SPAN/mirror PCAP → protocol-reverse / Wireshark industrial dissectors
□ Offline audit of configs and engineering files (TIA/RSLogix exports etc.)
□ Default credentials and plaintext protocols (Modbus has no auth) → record as findings, never write values
```

### Phase 3 — Limited active (authorized only)

```text
□ Low-rate identification, maintenance windows
□ Read-only function codes first
□ Evidence at every step; stop and report on any anomaly
```

### Phase 4 — Firmware / patching surface

```text
□ Controller firmware versions → CVE mapping (never blind-flash firmware)
□ Pair with firmware-pentest for offline image analysis
```

## Toolchain

| Tool | Purpose | Note |
|------|---------|------|
| Wireshark industrial dissectors | passive parsing | mirrored traffic |
| Nmap NSE (limited) | identification | rate and time window |
| Claroty / Nozomi etc. | asset discovery | commercial / on-site |
| PLC vendor engineering software | config audit | offline first |
| binwalk / Ghidra | firmware | offline |

## References

- `references/ot-safe-assessment.md`
- `security/parts/firmware-pentest/` `reverse-engineering/parts/protocol-reverse/` (IT network via `pentest-tools`)

## MUST NOT

- Throw ordinary web-scan default profiles at OT.

## Completion self-check

- [ ] Passive/read-only by default, authorization boundary recorded?
- [ ] No writes to control loops unless explicitly permitted?
- [ ] Findings include physical/process impact?
- [ ] Checklist / journal written?
