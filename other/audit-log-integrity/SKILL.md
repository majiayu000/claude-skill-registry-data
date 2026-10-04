---
name: audit-log-integrity
version: "1.0.0"
description: Audit-log integrity for mid-2026 — tamper-evident hash-chaining, off-host signing, compliance-mode WORM immutability, legal-hold-vs-retention enforcement, writer/custodian separation, and deception (honeytoken) coverage that resist the privileged attacker most likely to tamper with the trail
triggers:
  - audit log integrity
  - tamper evident logging
  - hash chain
  - worm
  - object lock
  - immutable storage
  - legal hold
  - retention
  - honeytoken
  - canary token
  - break glass
  - dual control
  - anti forensics
  - log deletion
  - separation of duties
  - audit trail
discovery_mode: standalone
data_deps:
  - cve-catalog.json
  - atlas-ttps.json
  - attack-techniques.json
  - framework-control-gaps.json
  - cwe-catalog.json
  - rfc-references.json
atlas_refs: []
attack_refs:
  - T1070
  - T1565.001
  - T1685.002
framework_gaps:
  - NIST-800-53-SI-2
  - ISO-27001-2022-A.8.15
  - NIS2-Art21-network-security
  - SOC2-CC7-anomaly-detection
cwe_refs:
  - CWE-345
  - CWE-347
  - CWE-284
  - CWE-778
last_threat_review: "2026-06-02"
---

# Audit-Log Integrity (Tamper-Evidence, WORM, Deception)

## Threat Context (mid-2026)

An audit trail is a security control only if it survives the attacker who wants it gone. Anti-forensic tampering (T1070 indicator removal) and stored-data manipulation (T1565.001) target precisely the log that would expose an intrusion, and the most capable adversary is a compromised privileged or insider identity. Logging volume is not integrity: a complete log that a sufficiently privileged credential can rewrite, re-chain, or delete is not a trail. The integrity properties that resist this are a hash chain actually verified on read, entries signed with a key held off the log-writing host, compliance-mode (not governance/override) WORM, legal holds that block the retention purge, separation of the log writer from its custodian, and honeytokens that catch the foraging access in the first place.

## Framework Lag Declaration

Organisational logging controls require that events are recorded, protected, and monitored — and stop there. ISO 27001 A.8.15 (logging) is commonly attested by "we log and protect logs" without verifying hash-chain continuity, independent signing, or immutability against a privileged attacker. SOC 2 CC7 monitoring is satisfied by the presence of logs and alerts. NIS2 Art.21 names monitoring for essential services but not the integrity model. None require the audit trail be immutable to the very identity most likely to tamper with it. A clean "we log and monitor" audit is therefore NON-EVIDENCE for audit-log integrity; it confirms log presence and alerting, not verified-chain continuity, off-host signing, compliance-WORM, or writer/custodian separation.

## TTP Mapping

The audit-log integrity failures map to MITRE ATT&CK: **T1070 (Indicator Removal)** for deleting/rotating/truncating the trail, defeated by compliance-WORM + writer/custodian separation + honeytokens; **T1565.001 (Stored Data Manipulation)** for rewriting entries, defeated by verified hash-chaining + off-host signing; and **T1685.002 (Disable or Modify Cloud Logs / abuse of privileged access)** for break-glass misuse, defeated by dual control + independent alerting. The weakness classes are CWE-345 (insufficient verification of data authenticity — unverified chain), CWE-347 (improper signature verification — co-located/absent signing), CWE-284 (improper access control — governance-WORM, writer-can-delete), and CWE-778 (insufficient logging/detection — absent or untriaged honeytokens).

## Exploit Availability Matrix

These are posture gaps exploited from a privileged or insider position, so the "exploit" is the absent control, not a published CVE. Rewriting a hash chain that is never verified, or recomputing it after editing history, requires only write access. Deleting from governance-mode WORM requires the admin credential the mode explicitly trusts. Purging records under an advisory-only legal hold requires nothing beyond the normal lifecycle job. The real-world priority is set by whether a single compromised identity can rewrite or delete the system-of-record trail without detection, and whether any external anchor or honeytoken would surface the tampering after the fact.

## Analysis Procedure

1. Identify the system-of-record audit trail (not just ephemeral operational logs). 2. Confirm the hash chain is VERIFIED on read/replay/export and fails closed on a break. 3. Confirm entries/checkpoints are signed with a key held off the log-writing host (separate identity / KMS / HSM). 4. Confirm the store is compliance-mode immutable (no role, including root, can delete before expiry) and that legal holds gate the retention purge. 5. Confirm the writing identity is append-only and a separate custodian holds delete rights. 6. Confirm honeytokens are seeded on high-value surfaces and a trip is alerted + triaged, and that break-glass requires dual control + audit. Run the `audit-log-integrity` playbook to execute these as detect indicators with false-positive checks, then score by whether one compromised identity can erase the trail undetected.

## Output Format

Report per integrity property (chain verification, signing, WORM mode, legal-hold gate, writer/custodian separation, deception), marking each enforced / missing / inconclusive (visibility gap). For every missing property, state whether a single compromised privileged or application identity could rewrite or delete the system-of-record trail undetected, and whether any external anchor or honeytoken would catch it. Distinguish a control enforced externally (external WORM/notary, KMS-held key) from an absent one. Provide the prioritised remediation (verify chain + sign off-host, compliance-WORM + hold gate, separate writer from custodian, deploy + triage honeytokens, dual-control break-glass) and the negative validation tests that prove each fix (chain-break detected, privileged delete refused, hold blocks purge) plus a functional test that legitimate writes still chain, sign, and verify.

## Compliance Theater Check

The recurring theater is "we log everything, so we have an audit trail," "our storage is immutable/WORM," and "records under legal hold are preserved." Logging volume is not integrity; "immutable" without naming the mode hides governance-mode reversibility; a hold flag that does not gate the purge preserves nothing. The distinguishing test: verify the chain is checked on read, the signing key is off-host, the WORM mode is compliance (root/admin cannot delete before expiry), and the purge job honors the hold. If a single privileged identity can rewrite or delete the trail undetected, the logging is not an audit trail and the assurance is paper.

## Defensive Countermeasure Mapping

Map findings to MITRE D3FEND: verified hash-chaining and off-host signing realise Message Authentication and Log Integrity (countering T1565.001); compliance-mode WORM and writer/custodian separation realise File Access Pattern Analysis and Access Modeling against deletion (countering T1070); dual-control + alerting on break-glass realises Administrative Account Monitoring (countering T1685.002); honeytokens realise Decoy Object / Connected Honeynet detection (high-fidelity evidence of the foraging access). Pair an external WORM/notary anchor with the on-host chain so even host compromise cannot rewrite history unobserved. The residual risk after these controls is multi-party collusion or compromise of the signing key / WORM authority itself, accepted at the CISO level with key-management oversight.
