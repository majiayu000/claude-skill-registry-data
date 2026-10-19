---
name: defense-ad-defense
description: >
  Detect and harden against Active Directory attacks — Kerberoasting, AS-REP roasting, DCSync, ADCS
  abuse, and delegation/relay. Load for "detect kerberoasting", "harden AD", "AD monitoring", "did
  someone DCSync us", or defending a domain. The defensive counterpart to the ad-* offensive skills.
domain: defense
type: technique
stability: learning
modes: [defense]
severity: info
mitre: [T1558.003, T1558.004, T1003.006, T1207, T1649]
tools: [bloodhound, pingcastle, purpleknight, sysmon, windows-eventlog]
schema_version: 1
---

# Active Directory defense

## When it applies
You run an AD domain and need to catch the standard attacker toolkit and close the structural weaknesses
it relies on — before or after a foothold.

## Why it works
Most AD attacks abuse features, not bugs, so they leave predictable event signatures and depend on
specific misconfigurations. Watch the right events and remove the preconditions, and the common
paths (the ones BloodHound finds) simply close.

## Method
1. **Kerberoasting (T1558.003)**: alert on Event `4769` (TGS request) with RC4 (`0x17`) encryption
   or high volume from one account. Harden: strong (25+ char) managed service-account passwords,
   gMSAs, and AES-only where possible.
2. **AS-REP roasting (T1558.004)**: find and fix accounts with "do not require Kerberos
   preauth"; alert on `4768` without preauth.
3. **DCSync (T1003.006)**: alert on `4662` replication GUIDs (DS-Replication-Get-Changes) from a
   principal that is not a DC. Harden: audit who holds replication rights.
4. **ADCS (ESC1-8, T1649)**: audit templates for enrollee-supplied SAN + client-auth EKU (ESC1) and
   dangerous enrollment rights; monitor `4886/4887` (cert requests/issues). Fix the template.
5. **Delegation / relay (T1207)**: inventory unconstrained/RBCD delegation; enable SMB signing +
   LDAP channel binding/signing to kill NTLM relay; monitor for coercion (PetitPotam-style).
6. **Structural hygiene**: run PingCastle/BloodHound *as the defender*, tier admin accounts,
   Protected Users group, LAPS for local admin, and remove the attack-graph edges (see
   `tradecraft-attack-path-mapping`).

## Gotchas
- `4769` fires constantly — key on RC4/volume/odd source, not the raw event.
- Legacy apps may need RC4/unconstrained delegation; document exceptions, don't leave them silent.
- ADCS is often the fastest domain-takeover path and the least monitored — prioritise it.

## Verify success
A controlled roast/DCSync/ESC1 in a lab produces the expected event and alerts, and a BloodHound run
shows the corresponding attack-graph edge removed after hardening.

## References
Microsoft AD security docs; SpecterOps ADCS ("Certified Pre-Owned"); PingCastle; MITRE ATT&CK.
