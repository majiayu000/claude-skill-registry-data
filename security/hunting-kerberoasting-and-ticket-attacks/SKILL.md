---
name: hunting-kerberoasting-and-ticket-attacks
description: 'Hunts for Kerberoasting and related ticket attacks by analyzing Kerberos service
  ticket request events (4769) for weak encryption types, abnormal request volume per account, and
  non-machine accounts requesting many SPNs. Activates for requests to hunt Kerberoasting, detect
  RC4 ticket requests, or find SPN-targeting credential attacks.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - kerberoasting
  - kerberos
  - credential-access
  - active-directory
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1558.003
  - T1558
  - T1550.003
d3fend:
  - D3-ANET
  - D3-UA
references:
  - 'MITRE ATT&CK T1558.003 Kerberoasting — https://attack.mitre.org/techniques/T1558/003/'
  - 'Windows Security Event 4769 — https://learn.microsoft.com/windows/security/threat-protection/auditing/event-4769'
---

# Hunting Kerberoasting and Ticket Attacks

## When to Use

- You have Kerberos service ticket request events (Event ID 4769) and want to detect Kerberoasting
  (bulk TGS requests with crackable RC4 encryption against service accounts).
- You are investigating AD credential-access activity.

**Do not use** this for AS-REP roasting (4768 with preauth disabled) — that is a related but
separate hunt; this focuses on 4769 TGS requests.

## Prerequisites

- Event ID 4769 records with account name, service name (SPN), ticket encryption type, and client
  address.

## Workflow

### Step 1: Flag weak-encryption ticket requests

```bash
python scripts/analyst.py hunt 4769_events.csv
```

Flags tickets with encryption type `0x17` (RC4-HMAC) — the crackable type Kerberoasting prefers —
and computes per-account SPN request volume.

### Step 2: Detect bulk SPN targeting

Surface accounts requesting tickets for many distinct SPNs in a short window (a single user
enumerating service accounts).

### Step 3: Confirm

Correlate with the requesting host and whether the account legitimately needs those services.

### Step 4: Operationalize

Write a detection for RC4 4769 requests from non-machine accounts above a volume threshold.

## Validation

- RC4 (`0x17`) requests are distinguished from AES (`0x11`/`0x12`).
- Per-account distinct-SPN counts identify bulk targeting.
- Findings map to ATT&CK T1558.003.

## Pitfalls

- Legacy applications legitimately using RC4 — baseline before alerting.
- Failure code 0x0 (success) only; some logs include failures that skew counts.
- Service accounts with many SPNs producing benign volume — combine with encryption-type weakness.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the hunter.
- ATT&CK T1558.003 and Event 4769 docs (linked in frontmatter).
