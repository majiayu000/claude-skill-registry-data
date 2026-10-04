---
name: privacy-consent-ops
version: "1.0.0"
description: Privacy, consent, and sanctions operational integrity for mid-2026 — confusable/homoglyph normalization before sanctions screening, integrity-bound and re-validated consent records, evidence-gated and downstream-propagated DSR erasure, and ROPA reconciliation against actual processing
triggers:
  - privacy operations
  - consent integrity
  - sanctions screening
  - ofac screening
  - homoglyph evasion
  - confusable normalization
  - iab tcf
  - mspa
  - consent string
  - dsr
  - right to erasure
  - right to be forgotten
  - gdpr article 17
  - ropa
  - record of processing
  - data subject request
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
  - T1036
  - T1565.001
  - T1070
framework_gaps:
  - NIST-800-53-SI-2
  - NIS2-Art21-network-security
  - UK-CAF-B4
  - AU-ISM-1240
cwe_refs:
  - CWE-807
  - CWE-345
  - CWE-778
  - CWE-672
last_threat_review: "2026-06-02"
---

# Privacy / Consent / Sanctions Operational Integrity

## Threat Context (mid-2026)

Privacy and sanctions controls fail operationally even when they exist on paper. A sanctions screen that compares raw strings is evaded by a listed name spelled with confusable Unicode (Cyrillic/Latin lookalikes, combining marks, zero-width characters) — or simply by an alias or transliteration the screen does not cover. A consent signal (IAB TCF / MSPA or first-party) trusted from the client with no integrity binding to a server-side consent_log is forgeable and stale-by-default, and continuing to process on a cached signal after withdrawal is unlawful. A data-subject erasure marked "completed" without per-store proof, and not propagated to backups, indexes, warehouses, and processors, leaves live personal data behind while the organisation asserts compliance. A ROPA that drifts from actual processing hides flows that escape the consent/retention/DSR analysis entirely.

## Framework Lag Declaration

Organisational privacy and sanctions controls are attested by having the process — a screening vendor, a consent banner, a DSR queue, a ROPA document. NIST 800-53 SI-10 (input validation) does not require Unicode confusable normalization before a sanctions-screening decision. ISO 27001 A.5.34 (privacy / PII) is met by having consent and DSR processes and does not require the consent signal be integrity-bound or the erasure be evidence-backed and propagated. A clean "we screen against OFAC, capture consent, complete DSRs, and maintain a ROPA" audit is therefore NON-EVIDENCE for operational integrity; it confirms the processes exist, not that screening normalizes confusables, consent is server-bound and re-validated, erasure is evidence-gated and propagated, and the ROPA matches reality.

## TTP Mapping

The privacy/sanctions failures map to MITRE ATT&CK: **T1036 (Masquerading)** for a prohibited party spelling a sanctioned name with homoglyphs or an uncovered alias to evade screening; **T1565.001 (Stored Data Manipulation)** for forging or replaying a consent signal with no authoritative record, and for an erasure status falsely marked "completed"; and **T1070 (Indicator Removal)** for claiming erasure that removes the compliance indicator while live copies survive downstream. The weakness classes are CWE-807 (reliance on untrusted inputs in a security decision — unnormalized screening input), CWE-345 (insufficient verification of data authenticity — unbound consent), CWE-778 (insufficient logging — unevidenced erasure / drifted ROPA), and CWE-672 (operation on a resource after expiration — processing on withdrawn/expired consent).

## Exploit Availability Matrix

These are operational-integrity gaps, so the exploit is the absent control, reproduced with trivial means. A homoglyph-spelled sanctioned name is a copy-paste with lookalike code points; an alias variant is in the sanction list's own alias data. A forged consent string is a crafted request when no server record reconciles it. A falsely-completed erasure needs no attacker at all — it surfaces on audit or a re-request. The real-world priority is set by whether a prohibited party can clear screening on a live onboarding/payment path (regulatory + legal exposure) or whether personal data is systemically unlawfully processed or un-erased across the data estate (false compliance at scale).

## Analysis Procedure

1. Inspect the sanctions screen: does it normalize to a confusable-folded skeleton (NFKC + Unicode confusable folding) and apply the list's aliases + transliteration + bounded fuzzy match before deciding? 2. Inspect consent: is the signal integrity-bound to a server-side consent_log and re-validated (purpose, expiry, withdrawal) at processing time, not just capture? 3. Inspect DSR erasure: is "completed" gated on per-store deletion evidence, and is erasure propagated to every downstream copy and processor on a maintained data-map? 4. Inspect the ROPA: is it reconciled against actual data flows / processors on a cadence? Run the `privacy-consent-ops` playbook to execute these as detect indicators with false-positive checks, then score by prohibited-party admission risk and the breadth of unlawful / un-erased processing.

## Output Format

Report per control (sanctions screening, consent, DSR erasure, ROPA), marking each enforced / missing / inconclusive (visibility gap). For every missing control, state whether a prohibited party could clear screening, whether personal data is unlawfully processed or un-erased, and the affected population. Distinguish a control enforced by a dedicated layer (a confusable-folding screen, a consent platform, an evidence-gated workflow) from an absent one. Provide the prioritised remediation (normalize + alias/fuzzy screen, server-bind + re-validate consent, evidence-gate + propagate erasure, reconcile ROPA) and the negative validation tests (homoglyph name screened, forged consent rejected, erasure-completion gated) plus a functional test that legitimate parties, consents, and erasures proceed.

## Compliance Theater Check

The recurring theater is "we screen all parties against OFAC," "we capture user consent," and "erasure requests are completed." The distinguishing tests: submit a Cyrillic-lookalike spelling of a listed name (if it passes, the screen compares raw strings without confusable normalization); ask whether the consent signal is server-bound and re-validated (a client-presented string with no record is forgeable and stale); ask for the per-store erasure evidence and the downstream-propagation map (a "completed" flag with no proof leaves records live in indexes, backups, and processors). If any control reports success while the obligation is unmet, the process is paper and the verdict is theater.

## Defensive Countermeasure Mapping

Map findings to MITRE D3FEND: confusable-folding + alias/fuzzy screening realises Input Normalization and Identifier Reputation Analysis (countering T1036 evasion); server-bound + re-validated consent realises Authentication-Token Verification and Stored-Record Integrity (countering T1565.001 forged/stale consent); evidence-gated + propagated erasure realises Verifiable Deletion and Data-Inventory Mapping (countering T1070 false-erasure claims); ROPA reconciliation realises Asset/Processing Inventory accuracy. The sanctions-normalization control reuses the vendored Unicode confusable / codepoint-class tooling. The residual risk is a novel transliteration the alias list does not cover and a processor retaining data outside the data-map, accepted at the CISO level with periodic re-reconciliation.
