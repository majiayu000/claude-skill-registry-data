---
name: hunting-unusual-outbound-connections
description: 'Hunts for unusual outbound network connections by flagging direct-to-IP traffic,
  uncommon ports, rare destinations, high data-egress ratios, and connections from unexpected
  processes in network telemetry. Activates for requests to hunt unusual outbound traffic, detect
  suspicious egress, or find anomalous external connections.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - network
  - egress
  - exfiltration
  - anomaly-detection
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1071
  - T1048
  - T1571
d3fend:
  - D3-NTA
  - D3-OTF
car:
  - CAR-2013-05-002
references:
  - 'MITRE ATT&CK T1048 Exfiltration Over Alternative Protocol — https://attack.mitre.org/techniques/T1048/'
  - 'MITRE ATT&CK T1571 Non-Standard Port — https://attack.mitre.org/techniques/T1571/'
---

# Hunting Unusual Outbound Connections

## When to Use

- You have connection/flow telemetry (Sysmon EID 3, firewall, Zeek conn) and want to surface
  anomalous egress: direct-to-IP, non-standard ports, rare destinations, and large uploads.
- You are hunting C2 and exfiltration channels.

**Do not use** this to block on raw destination novelty alone — many new destinations are benign.
Combine signals (port + process + egress ratio) before alerting.

## Prerequisites

- Outbound connection telemetry with destination IP/port, process, and (ideally) byte counts.

## Workflow

### Step 1: Score outbound connections

```bash
python scripts/analyst.py hunt conns.csv
```

Flags direct-to-IP (no domain), uncommon ports (not 80/443/53/...), high sent:received byte ratio
(possible exfil), and connections from unexpected processes (e.g., `notepad.exe` egressing).

### Step 2: Rank destinations by rarity

Aggregate per-destination connection counts to surface low-prevalence endpoints.

### Step 3: Confirm

Investigate top-scoring connections; corroborate with reputation and process context.

### Step 4: Operationalize

Tune thresholds and write a detection for the strongest combined signals.

## Validation

- Direct-to-IP and non-standard-port connections are flagged.
- High egress-ratio connections are surfaced for exfil review.
- Unexpected-process egress is identified.

## Pitfalls

- CDNs and cloud services producing many benign direct-IP/new destinations.
- Standard ports (443) used by C2 — port alone is insufficient.
- Asymmetric-but-benign traffic (backups, uploads) inflating egress ratio.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the hunter.
- ATT&CK T1048 and T1571 (linked in frontmatter).
