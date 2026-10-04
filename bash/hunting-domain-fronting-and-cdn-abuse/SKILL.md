---
name: hunting-domain-fronting-and-cdn-abuse
description: 'Hunts for domain fronting and CDN abuse by detecting TLS SNI versus HTTP Host header
  mismatches and high-reputation CDN domains carrying anomalous traffic in network telemetry.
  Activates for requests to hunt domain fronting, detect SNI/Host mismatch, or find CDN abuse used
  to mask C2.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - domain-fronting
  - cdn
  - tls
  - c2
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1090.004
  - T1071.001
  - T1573
d3fend:
  - D3-NTA
  - D3-NTPM
references:
  - 'MITRE ATT&CK T1090.004 Domain Fronting — https://attack.mitre.org/techniques/T1090/004/'
  - 'TLS SNI (RFC 6066) — https://datatracker.ietf.org/doc/html/rfc6066'
---

# Hunting Domain Fronting and CDN Abuse

## When to Use

- You have TLS/HTTP telemetry (Zeek ssl.log + http.log, proxy logs) and want to detect domain
  fronting, where the TLS SNI shows a benign CDN domain but the inner HTTP Host differs.
- You are hunting C2 hidden behind high-reputation CDNs.

**Do not use** SNI/Host mismatch as definitive — some legitimate setups differ. Corroborate with
destination behavior and reputation.

## Prerequisites

- Telemetry pairing TLS SNI with the inner HTTP Host (or proxy logs exposing both).

## Workflow

### Step 1: Detect SNI/Host mismatch

```bash
python scripts/analyst.py hunt flows.csv
```

Flags connections where the TLS SNI and HTTP Host headers resolve to different registered domains,
especially when the SNI is a known CDN/fronting-capable domain.

### Step 2: Surface CDN-hosted anomalies

Highlight high-reputation CDN SNIs carrying long-lived or beaconing flows.

### Step 3: Confirm

Corroborate with beacon periodicity, JA3, and destination reputation; many CDN mismatches are
benign.

### Step 4: Operationalize

Write a detection for SNI/Host registered-domain mismatch on fronting-capable CDNs.

## Validation

- Mismatch is computed on the registered domain, not the full hostname.
- Known CDN SNIs are recognized to prioritize fronting-capable cases.
- Findings are presented with corroboration needs, not as proof.

## Pitfalls

- Legitimate multi-tenant CDN/edge configs producing benign mismatches.
- Encrypted SNI (ECH) hiding the SNI entirely — different hunt required.
- Treating any CDN traffic as suspicious (high false-positive rate).

## References

- See [`references/api-reference.md`](references/api-reference.md) for the hunter.
- ATT&CK T1090.004 and the TLS SNI RFC (linked in frontmatter).
