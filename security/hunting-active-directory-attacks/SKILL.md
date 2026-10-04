---
name: hunting-active-directory-attacks
description: 'Hunts for Active Directory credential and replication attacks — DCSync, Golden/Silver
  Ticket, and DCShadow — by analyzing directory-service-access (4662), Kerberos TGS (4769), and
  logon (4624) events for replication abuse and forged-ticket anomalies. Activates for requests to
  hunt DCSync, detect golden/silver tickets, or find Active Directory replication abuse.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - active-directory
  - dcsync
  - golden-ticket
  - credential-access
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1003.006
  - T1558.001
  - T1207
d3fend:
  - D3-UA
  - D3-ANET
car:
  - CAR-2019-04-004
references:
  - 'MITRE ATT&CK T1003.006 DCSync — https://attack.mitre.org/techniques/T1003/006/'
  - 'Windows Security Event 4662 — https://learn.microsoft.com/windows/security/threat-protection/auditing/event-4662'
---

# Hunting Active Directory Attacks

## When to Use

- You have AD/domain-controller telemetry (Event IDs 4662, 4769, 4624) and want to detect DCSync
  replication abuse, Golden/Silver Ticket usage, and DCShadow.
- You are investigating credential-access and domain-persistence activity.

**Do not use** this for Kerberoasting/AS-REP roasting — those have a dedicated hunt. This focuses
on replication abuse and forged-ticket anomalies.

## Prerequisites

- Event ID 4662 (directory service access), 4769 (TGS requests), and 4624 (logons) with account
  and detail fields.

## Workflow

### Step 1: Hunt DCSync replication abuse

```bash
python scripts/analyst.py hunt events.csv
```

Flags 4662 events granting the replication rights GUIDs (`DS-Replication-Get-Changes`
`1131f6aa-…` / `-All` `1131f6ad-…`) to non-DC accounts.

### Step 2: Detect forged-ticket anomalies

Surface 4769 requests with anomalies consistent with Golden/Silver Tickets (RC4 where AES is
expected, missing preceding 4768, or accounts that do not exist), and logons with mismatched
ticket lifetimes.

### Step 3: Confirm

Correlate the flagged account/host with whether it is a legitimate DC or replication service.

### Step 4: Operationalize

Write a detection for replication-rights grants to non-DC principals.

## Validation

- DCSync flags key on the replication GUIDs granted to non-DC accounts.
- Forged-ticket anomalies are based on encryption type / missing-AS-REQ evidence.
- Findings map to ATT&CK T1003.006 / T1558.001.

## Pitfalls

- Legitimate DCs and Azure AD Connect perform replication — allow-list them.
- Golden Tickets can perfectly mimic valid TGS; rely on corroborating anomalies, not one signal.
- Incomplete auditing (4662 object-access auditing must be enabled) causing blind spots.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the hunter.
- ATT&CK T1003.006 and Event 4662 (linked in frontmatter).
