---
name: ransomware-response
version: "1.0.0"
description: Ransomware-specific incident response — OFAC sanctions screening as payment-posture blocker, EU Reg 2014/833 + UK OFSI + AU DFAT + JP MOF cross-jurisdiction sanctions lookups, decryptor availability via No More Ransom + vendor-specific catalogs, cyber-insurance carrier 24h notification, negotiator-engagement legal posture, immutable-backup viability test, PHI exfil-before-encrypt as distinct breach class, parallel jurisdiction clocks (NIS2 24h / DORA 4h / GDPR 72h / SEC 8-K 96h / HIPAA 60d / CIRCIA 72h / NYDFS 500.17 24h ransom-payment)
triggers:
  - ransomware
  - ransomware incident
  - encryption event
  - akira ransomware
  - lockbit
  - alphv
  - blackcat
  - cuba ransomware
  - royal ransomware
  - blacksuit
  - hunters international
  - ransomhub
  - ofac sanctions ransomware
  - ransom payment
  - decryptor availability
  - no more ransom
  - cyber insurance ransomware
  - immutable backup
  - shadow copy deletion
  - exfil before encrypt
  - double extortion
  - data theft before encryption
data_deps:
  - d3fend-catalog.json
  - framework-control-gaps.json
  - zeroday-lessons.json
atlas_refs: []
attack_refs:
  - T1486
  - T1567
  - T1078
  - T1059
framework_gaps:
  - OFAC-SDN-Payment-Block
  - Insurance-Carrier-24h-Notification
  - EU-Sanctions-Reg-2014-833-Cyber
  - Immutable-Backup-Recovery
  - Decryptor-Availability-Pre-Decision
  - PHI-Exfil-Before-Encrypt-Breach-Class
rfc_refs: []
cwe_refs:
  - CWE-287
  - CWE-798
d3fend_refs:
  - D3-RPA
  - D3-NTA
  - D3-IOPR
  - D3-CSPP
forward_watch:
  - OFAC Ransomware Advisory revisions (post-2021 advisory, updated periodically) — track expansions to the SDN list for ransomware affiliates, especially LockBit splinter brands, Cuba, ALPHV/BlackCat successors, and Russia/DPRK/Iran-affiliated clusters
  - EU Cyber Sanctions Regulation 2014/833 — additions and the EU's coordination with US OFAC on attribution
  - UK OFSI cyber listings — post-Operation Cronos (LockBit, February 2024) and Operation Endgame (May 2024) expansions
  - AU DFAT autonomous cyber sanctions — first cyber listing 2024; further listings expected
  - NYDFS 23 NYCRR 500.17 — 2023 amendments operationalization; 24h ransom-payment clock case law
  - SEC 17 CFR 229.106(b) Form 8-K Item 1.05 — materiality determination guidance and SEC enforcement actions through 2025-2026
  - CIRCIA implementation — final rule timeline; covered-entity scope expansion
  - HIPAA Security Rule update (NPRM late 2024 → final rule expected 2026) — explicit ransomware-recovery and encryption-at-rest requirements
  - No More Ransom Project decryptor releases — affiliate-takedown decryptor drops (Operation Cronos LockBit decryptor, BlackCat post-exit-scam decryptors)
  - SCOTUS or circuit-court rulings on ransomware payment, sanctions liability, and insurance-policy enforcement
last_threat_review: "2026-09-18"
---

# Ransomware Response Playbook

Ransomware response is incident response with four ransomware-specific decision properties that no security framework operationalizes as controls and that the parent incident-response playbook (`incident-response-playbook`) does not exhaust. This skill extends — it does not duplicate — the parent. Use `incident-response-playbook` for the PICERL phase scaffolding, the jurisdictional notification matrix (Section "Regulatory Notification Matrix"), the post-incident review template, and the cross-skill hand-off graph. Use this skill for the ransomware sub-flow: encryption-confirmation, OFAC SDN sanctions screening as a blocking gate on payment posture, decryptor availability lookup against No More Ransom + vendor-specific catalogs, cyber-insurance carrier 24h notification with pre-approval requirements, negotiator-engagement legal posture, immutable-backup viability test, and PHI / personal-data exfil-before-encrypt as a distinct breach class triggering HIPAA Breach Notification Rule / GDPR Art.33 independently of the encryption event.

This skill operationalizes the four ransomware-specific decision properties under the parent's mid-2026 PICERL frame: NIST SP 800-61r3 (Preparation, Detection & Analysis, Containment-Eradication-Recovery, Post-Incident Activity), ISO/IEC 27035-1:2023 process model, SANS PICERL phases, plus the regulator clocks tracked by the parent (NIS2 Art.23 24h, DORA Art.19 4h, GDPR Art.33/34 72h, AI Act Art.73 15d/2d, NYDFS 500.17 72h/24h-ransom-payment, CIRCIA 72h, SEC 8-K 4 business days, HIPAA 60d, CCPA 60d, UK GDPR 72h, AU NDB 30d). Where this skill names a clock, it is in the parent's matrix; where it names a decision property (sanctions, decryptor, insurance, immutability, exfil-before-encrypt), it is the property the parent does not enumerate.

---

## Threat Context (mid-2026)

Ransomware is the highest-volume critical-infrastructure incident class and the dominant economic-harm cyber category, and its operational shape changed materially between the 2020-2022 frame and the 2024-2026 frame.

- **Exfiltration-before-encryption is now the dominant attack pattern.** Coveware Q1 2026 reports >82% of named-ransomware incidents include a data-theft component, making the encryption event a secondary leverage rather than the primary blast radius. The change matters for IR because the breach-notification scope is no longer derivative of the encryption event — exfiltration is its own breach trigger under HIPAA Breach Notification Rule 45 CFR 164.402, GDPR Art.33/34, and state breach laws, regardless of whether the encryption is decrypted, recovered from backup, or never recovered. The IR team must classify the exfil scope independently of the encryption scope within hours of awareness.
- **Active families and clusters mid-2026 (non-exhaustive):** Akira (sustained 2024-2026, dominant in healthcare and manufacturing), Hunters International (post-Hive successor, broad-sector), RansomHub (2025-2026 affiliate growth after the ALPHV/BlackCat exit-scam of February 2024), LockBit splinter brands (post-Operation Cronos February 2024 law-enforcement takedown), Cuba (FSB-adjacent, multiple sanctions-list flags), BlackSuit/Royal continuation, Qilin (June 2024 Synnovis/NHS pathology disruption), Black Basta (May 2024 Ascension Health), 8base, Medusa, Play, Inc Ransom. Family lifetimes are short; affiliate ecosystems persist post-takedown via rebrand, so attribution-by-family is necessary but not sufficient for sanctions screening.
- **Operational exemplars (2023-2026):** Change Healthcare / UnitedHealth Group (ALPHV/BlackCat, February 2024, ~$1.5B financial impact, 6-week pre-encryption dwell, ~190M individuals affected by PHI exfiltration); MGM Resorts (Scattered Spider initial access → ALPHV affiliate ransomware, September 2023, vishing-driven IT helpdesk credential reset); Synnovis / NHS pathology services (Qilin, June 2024); Ascension Health (Black Basta, May 2024); Colonial Pipeline (DarkSide, May 2021, still the canonical OT/IT segmentation lesson); CDK Global (BlackSuit, June 2024, US auto-dealership systemic outage).
- **Initial-access vector distribution 2024-2026:** ~45% phishing-derived including vishing/MFA-fatigue chains a la Scattered Spider; ~25% exposed-VPN-appliance or management-plane exploitation (Citrix CVE-2023-3519, Fortinet CVE-2024-21762, ScreenConnect CVE-2024-1709, Ivanti Connect Secure 2024 cluster); ~20% credential reuse from infostealer markets (RedLine, LummaC2, StealC); ~10% supply-chain or vendor compromise (CVE-2024-3094 xz-utils as a recent class exemplar, CVE-2024-21626 runc as cloud-runtime supply-chain).
- **Living-off-the-land is universal across families.** PsExec, WMI, PowerShell, AnyDesk, ScreenConnect, Cobalt Strike Beacon, Sliver, Brute Ratel, AdFind, BloodHound/SharpHound, Mimikatz, LaZagne, NetScan. Shadow Copy deletion (vssadmin / wmic shadowcopy / wbadmin delete catalog) precedes encryption in ~95% of Windows attacks; AD reconnaissance (BloodHound-class) precedes encryption by days-to-weeks in domain-wide attacks.
- **Decryptor reliability remains poor even with payment.** Coveware quarterly reports across 2023-2026 show ~65% of paid victims recovered all data; ~35% experienced partial decryption, corrupt files, or no working decryptor. Specific family failure modes (Conti, LockBit, ALPHV) are publicly documented. The decryptor-as-recovery posture is therefore not a backup substitute, and treating it as one is a documented compliance-theater pattern.
- **Sanctions exposure on payment is the single highest legal-risk dimension.** OFAC's 2020 advisory (updated 2021) made clear that payment to a sanctioned threat actor is a federal-law violation in the US; the EU Cyber Sanctions Regulation 2014/833, UK OFSI Consolidated List, AU DFAT autonomous sanctions, and JP MOF Foreign Exchange and Foreign Trade Act sanctions impose parallel obligations in their jurisdictions. The IR team that does not pre-rehearse a sanctions-screening workflow with named legal counsel will, under real time-pressure, either skip the screening (federal-law violation risk) or stall the decision past the carrier-notification window (insurance denial risk). Both are operational failures.
- **Cyber insurance is the dominant economic-exposure failure mode.** Post-2021 cyber-insurance policies typically exclude payments to OFAC-sanctioned actors, require pre-payment carrier approval, require named IR firms from a panel, and require 24h initial notification with non-compliance grounds for policy voiding. Carrier denial post-incident is more common than insufficient policy limits as the harm-amplification mechanism. The IR playbook that does not bake the carrier interaction into the 24h-clock band leaves the insurance posture to chance.

Mid-2026 reality: ransomware is not "malware-on-host plus regulator-clock" — it is a multi-decision problem (sanctions, decryptor, insurance, immutability, exfil-class) that runs in parallel with the regulator clocks tracked by the parent playbook. The org that runs only the parent playbook will miss at least one decision property per incident; the four below are the gaps.

---

## Framework Lag Declaration

The four ransomware-specific decision properties — sanctions screening, decryptor availability, insurance-carrier interaction, exfil-before-encrypt classification — are not operationalized as controls in any security framework. They live in adjacent regulatory trees (Treasury / Finance for sanctions, contract law for insurance, breach-notification statutes for exfil) that the security-framework owner does not maintain. The operator carries the cross-walk.

| Framework / Source | Control | What It Says | Why It Fails as a Ransomware Playbook Spec |
|---|---|---|---|
| NIST SP 800-53 rev 5 | IR-4 Incident Handling; IR-5 Incident Monitoring; IR-6 Incident Reporting; IR-8 Incident Response Plan | Method-neutral incident response capability with preparation, detection-and-analysis, containment-eradication-recovery, post-incident activity. | Does not name sanctions screening as a blocking gate, decryptor availability lookup as a precondition, insurance-carrier interaction as a control, immutable-backup viability test as a Layer-1 backup property, or exfil-before-encrypt as a distinct breach class. IR-4 satisfies an audit by procedure-document existence. |
| NIST SP 800-61r3 (2025) | Computer Security Incident Handling Guide | Integrates MITRE ATT&CK + Cyber Kill Chain into the four-phase handling lifecycle. | Does not operationalize ransomware-specific decision properties. Does not name the OFAC sanctions advisory, No More Ransom Project, or the cyber-insurance carrier-notification clock. |
| ISO/IEC 27001:2022 | A.5.26 Response to information security incidents; A.5.30 ICT readiness for business continuity; A.8.13 Information backup | Process-shaped response, outcome-shaped backup. | Treats "backup" as a single class; auditor accepts tape-vault offsite as compliant. Immutability (compliance-lock storage policy with no root override) is a sub-property absent from A.8.13 control text. A.5.26 evidence is procedure-document existence. |
| ISO/IEC 27035-1:2023 | Information security incident management — Principles and process | Process model: plan & prepare → detect & report → assess & decide → respond → learn lessons. | No ransomware sub-type. No sanctions-screening or decryptor-lookup integration. |
| SOC 2 | CC7.4 Security incident response; CC9.2 Vendor / business partner risk | Trust services criteria for incident response and vendor risk. | Names response capability; does not require evidence of ransomware-specific decision tree. Vendor criterion does not surface cyber-insurance carrier policy as a control. |
| HIPAA (45 CFR 164) | 164.308(a)(7) Contingency Plan; 164.400-414 Breach Notification Rule; 164.402 Breach Risk Assessment | Contingency planning for emergencies damaging ePHI; breach-notification triggers and timelines. | Contingency planning is recovery-shaped; treats the encryption event as the trigger. The dominant 2024-2026 ransomware pattern includes PHI exfiltration before encryption, which is a separate Breach Notification Rule trigger that engages the 164.402 risk assessment independently of the encryption event. The Contingency Plan rule does not naturally surface this parallel obligation, and HIPAA Security Rule NPRM late 2024 → final rule expected 2026 is still pending. |
| AU Essential Eight | Strategy 8 — Regular Backups | Daily backups of important data, software, and configuration with off-network retention. | "Off-network" is the ML2 maturity gate; immutability is not addressed. Replication targets accessible via the same compromised admin credential as production fail the ransomware blast-radius test without failing E8 Backup compliance. |
| AU ISM | ISM-1784 (incident response plan exercised at least annually) + ISM-1819 (plan enacted once an incident is identified) + ISM-1814 (unprivileged accounts cannot modify or delete backups) | Annual exercise of the incident response plan, and backups protected from the accounts ransomware usually runs as. | The exercise frequency is named but its content is not, so an exercise that never rehearses a payment decision or a sanctions check satisfies ISM-1784. ISM-1814 applies at every Essential Eight maturity level but protects backups from unprivileged accounts only; ISM-1705 extends that to privileged accounts other than backup administrators from Maturity Level Two, which still leaves a compromised backup administrator able to delete them. |
| UK NCSC CAF | D1 Response and Recovery Planning | Outcome that the org has plans for responding to and recovering from cyber incidents. | Outcome-shaped at IGP/IGP+ level; tabletop exercise is plan-existence proof. Does not test whether plans address ransomware sub-class with immutable-backup viability check or sanctions screening. |
| US OFAC | 31 CFR 501 + OFAC Ransomware Advisory (2021) | Sanctions list; advisory making clear payment to sanctioned actor is federal-law violation. | Lives in Treasury regulatory tree, not in NIST/ISO/SOC 2 security controls. Cross-walk is operator's responsibility; no security framework names the OFAC SDN list check as a control on the payment posture. |
| EU | Council Regulation 2014/833 — Cyber Sanctions | EU consolidated cyber sanctions list. | Same structural gap as OFAC — lives in EU sanctions tree, not in NIS2 or DORA control text. |
| UK | Sanctions and Anti-Money Laundering Act 2018 + OFSI Consolidated List | UK consolidated sanctions list. | Same structural gap. |
| AU | DFAT Autonomous Sanctions Regulations 2011 — cyber listings | AU autonomous sanctions list. | Same structural gap. |
| JP | MOF Foreign Exchange and Foreign Trade Act sanctions | JP consolidated sanctions list. | Same structural gap. |
| US-NY | NYDFS 23 NYCRR 500.17 | 72h cyber-event notification; **24h ransom-payment notification** (2023 amendment, in force 2023-12). | The ransom-payment 24h clock runs in parallel with OFAC screening and the carrier-notification clock. NYDFS is one of the few regimes that operationalizes ransom payment as a separate event. |
| US-SEC | 17 CFR 229.106(b) Form 8-K Item 1.05 | Public-company material cybersecurity incident disclosure within 4 business days of materiality determination. | Materiality determination is the gate; the 4-business-day clock starts on determination, not on awareness. Determination practice is uneven across companies and is a frequent SEC enforcement target. |
| US-FEDERAL | CIRCIA — Cyber Incident Reporting for Critical Infrastructure Act (final rule pending implementation) | 72h covered cyber incident report; 24h ransom-payment report for covered entities. | Final rule timeline and covered-entity scope still in implementation; the IR team should follow the rulemaking. |

Cross-cutting gap: **no security framework treats the four ransomware-specific decision properties as controls.** Operator workaround: integrate sanctions screening + decryptor lookup + carrier-pre-approval + immutability test + exfil-before-encrypt classification into the IR playbook explicitly; rehearse in tabletop. Framework-level fix is pending the next NIST / ISO / SOC 2 revision cycle; HIPAA Security Rule final rule expected 2026 may close the exfil-before-encrypt gap for healthcare.

---

## TTP Mapping

| TTP ID | Name | Where It Fires in Ransomware Response | PICERL Phase Notes |
|---|---|---|---|
| **T1486** | Data Encrypted for Impact | Confirmation that an encryption event has occurred; bounds the affected-host scope. | Identification: EDR file-encryption telemetry, mass-rename pattern, ransom-note presence. Containment: network-segment isolation, forensic preservation BEFORE remediation. Eradication: clean-media rebuild OR validated immutable-backup restore. Recovery: phased service-level verification. |
| **T1567** | Exfiltration Over Web Service | Exfil-before-encrypt detection in the 24-72h window preceding encryption; bounds the breach-notification scope independently of the encryption event. | Identification: large outbound transfer to non-allowlisted destinations, rclone / MEGAcmd / anon-upload signatures. Containment: egress block, DLP review of exfil scope. Eradication: identify exfiltrated dataset; trigger 164.402 / GDPR Art.33 risk assessment. |
| **T1078** | Valid Accounts | Initial access via credential reuse from infostealer markets; AD privilege chain mapping pre-encryption; lateral movement via valid accounts to broaden encryption scope. | Identification: anomalous sign-in UEBA, impossible-travel, infostealer-market evidence. Containment: account disable + session revocation + MFA re-enrollment. Eradication: krbtgt double-rotation, OAuth-grant audit, AD admin-group review. |
| **T1059** | Command and Scripting Interpreter | Living-off-the-land via PowerShell, WMI, PsExec; Cobalt Strike Beacon / Sliver / Brute Ratel as C2 framework. | Identification: EDR script-block-logging, suspicious WMI invocations, JA3 fingerprints. Containment: EDR quarantine, egress block to C2 destinations. Eradication: artifact removal, persistence-mechanism cleanup. |

Shadow Copy deletion and exfil-staging via Web Service align to the parent IR playbook's `T1486` and `T1567` entries; the parent's `AML.T0096 / AML.T0024 / AML.T0051` entries do not apply to ransomware-as-a-class but may apply if AI-system data is exfiltrated within the ransomware operation.

ATLAS pinned to v2026.09 (September 2026). ATT&CK pinned to v19.2 (August 2026). Both are explicit version pins — never silently upgraded.

---

## Exploit Availability Matrix

For ransomware response, "exploit availability" is the question of which initial-access CVEs are operationally current — the IR playbook must explicitly handle the vectors that mid-2026 ransomware operators are using.

| CVE | Class | Vector | Detection Maturity (mid-2026) | Playbook Implication |
|---|---|---|---|---|
| **CVE-2024-1709** | ScreenConnect authentication bypass | Exposed management-plane appliance | Vendor patch available; signatures public; exploited at scale by multiple ransomware affiliates in 2024 | Patch + rotate any credentials used on the appliance + audit all sessions in the exposure window. |
| **CVE-2023-3519** | Citrix NetScaler ADC / Gateway RCE | Exposed VPN appliance | Patch available; KEV-listed; remained widely exploited through 2024-2025 | Patch + replace appliance certificates + audit session history + memory dump for adversary-implanted credentials. |
| **CVE-2024-3094** | xz-utils malicious upstream maintainer compromise | Supply-chain into Linux distribution | Patched in distros; detection via `xz --version` and SBOM checks | If applicable to the affected environment, SBOM review for xz-utils versions in the vulnerable range; sshd-side mitigations applied. |
| **CVE-2024-21626** | runc file descriptor leak → container escape | Cloud-runtime container escape | Patched in runc, containerd, Docker, Kubernetes runtimes | If ransomware deployed via container escape, SBOM check for vulnerable runc versions; patch and re-deploy from clean images. |

Detection-tool maturity for ransomware mid-2026:
- **EDR/XDR**: high coverage for encryption-impact + mass-rename + shadow-copy-deletion; partial for cloud-workload-only encryption attacks; near-absent for hypervisor-level encryption (ESXi-targeting families).
- **Identity telemetry**: strong for human accounts; weak for service-account abuse and AD krbtgt-class compromise.
- **Egress / network**: strong for known C2-framework signatures (Cobalt Strike, Sliver, Brute Ratel); partial for exfil-to-legitimate-SaaS (MEGA, anonfiles, rclone-to-S3); weak for Tor-egress in environments not explicitly blocking Tor.
- **AD reconnaissance**: emerging — BloodHound / SharpHound / Adalanche have public signatures, but the volume baseline is environment-specific and false positives are common.
- **Sanctions screening + decryptor lookup**: not in any SOC stack by default — the IR team must operationalize the lookups as a workflow with named legal-counsel sign-off (sanctions) and a curated decryptor catalog (No More Ransom + vendor-specific).

---

## Analysis Procedure

Apply the three foundational design principles (defense in depth, least privilege, zero trust), then walk the ransomware-specific decision tree on top of the parent IR playbook's PICERL frame.

**Defense in depth — ransomware-specific layer stack.** The parent IR playbook defines the IR layer stack (Preparation, Identification, Containment, Eradication-Recovery, Lessons). Ransomware response adds five sub-properties:

- **Layer 1.5 — Backup immutability test.** Pre-incident: confirm the production-admin identity cannot delete or modify the most recent backup snapshot via API, storage console, or replication-target manipulation. Test annually as a tabletop drill, not as a paper exercise. Replication, versioning, and "write-protect" labels are not immutability; only storage-side compliance-lock (S3 Object Lock compliance-retention, Azure immutable blob storage with legal hold, Veeam Hardened Repository, Rubrik / Cohesity immutable-by-policy with admin-separation) qualifies.
- **Layer 2.5 — Sanctions screening pre-rehearsal.** Pre-incident: rehearse the OFAC SDN + EU Reg 2014/833 + UK OFSI + AU DFAT + JP MOF lookup workflow with named legal counsel. The lookup must be executed against attribution evidence (ransom note IoCs, leak-site URL, crypto-wallet addresses, family fingerprint) and the result must be signed by counsel with a timestamp that precedes any negotiator engagement. Skipping this lookup is federal-law violation risk in the US.
- **Layer 2.6 — Decryptor availability lookup integration.** Pre-incident: integrate No More Ransom Project Crypto Sheriff family-match + vendor-specific decryptor catalogs (Emsisoft, Kaspersky NoMoreCry, Bitdefender, Avast) into the IR playbook as a precondition to the pay/restore decision. An affirmative decryptor match changes the pay/restore posture materially and the decision must be informed by the lookup result.
- **Layer 2.7 — Insurance-carrier 24h notification with pre-approval.** Pre-incident: rehearse the carrier-notification workflow with the insurance broker, confirm the retained IR firm is on the carrier panel, document the carrier-pre-approval requirements (for ransom payment, for IR firm engagement, for restore-vs-pay decision), and confirm the carrier is reachable in the 24h notice window. Carrier denial post-incident is the dominant economic-exposure failure mode and is the IR team's responsibility to prevent.
- **Layer 3.5 — Exfil-before-encrypt classification as parallel breach trigger.** Pre-incident: integrate exfil-before-encrypt detection (24-72h egress profile preceding the encryption event) into the IR playbook as a distinct breach trigger that engages HIPAA Breach Notification Rule 164.402 risk assessment / GDPR Art.33-34 / state breach laws independently of the encryption event. The encryption may be fully recovered from immutable backup AND the exfiltration still requires regulator notification.

**Least privilege — ransomware containment scope is per-role.** Forensic-acquisition tooling is scoped to a sealed workstation set with chain-of-custody logging. Sanctions-screening lookups are scoped to the legal-counsel role with named sign-off; the IR team does not perform the legal determination, the IR team supplies the attribution evidence to legal. Decryptor-availability lookups are scoped to the IR analyst role with documented catalog access; the lookup result is recorded with timestamp. Carrier-notification interactions are scoped to the legal / risk / executive role; the IR team does not communicate directly with the carrier without legal-counsel involvement. Negotiator engagement is scoped to the legal-counsel + executive-sponsor role; any communication that could be construed as payment-facilitation is legally consequential.

**Zero trust — assume the network and AD are hostile during containment.** During an active ransomware incident: assume the SOC's own tooling may be compromised and validate findings via independent channels; assume the attacker may be reading IR-team communications (use out-of-band comms — Signal / Wickr / dedicated carrier-channel — never the corporate Slack that the attacker may be in); revoke and re-issue identities at the determined blast radius rather than trusting that "this account doesn't show compromise indicators"; verify-not-assume that backup integrity has not been tampered with before restore by running a restore-test on an isolated network with a known-clean admin identity; treat the immutable-backup property as a hypothesis to be tested, not as a certainty.

Then walk the ransomware-specific decision tree.

### Step 1 — Encryption confirmation

Confirm an encryption event has actually occurred (not merely suspected). Evidence: mass file-extension change (>500 files per host renamed within <60 minutes to a family-fingerprinted extension), ransom-note presence (readme*.txt / decrypt*.txt / how_to_recover*), EDR encryption-impact alert. The precondition matters because ransomware-response procedures are heavier than generic IR triage and false-positive ransomware declarations (backup-software encryption mistaken for ransomware, archive-creation batches, BitLocker volume conversion) burn IR-team capacity and trigger insurance-carrier notifications that may complicate policy posture.

### Step 2 — Family fingerprinting + threat-actor attribution

Identify the ransomware family from: encrypted-file extension distribution, ransom-note template, Tor URL / leak-site URL pattern, contact identifier (email / Tox / Session ID), crypto-wallet address, C2 framework JA3 / JA4 signatures, tool reuse (Cobalt Strike Beacon profile, AnyDesk / ScreenConnect remote-management abuse, Mimikatz / LaZagne / NetScan / AdFind / SharpHound). Cross-reference against current-mid-2026 active families. Family fingerprinting feeds Steps 3 (sanctions) and 4 (decryptor).

### Step 3 — OFAC SDN + cross-jurisdiction sanctions screening (BLOCKING gate on payment posture)

Execute sanctions-list screening against the attribution package: US OFAC SDN list + EU Reg 2014/833 consolidated list + UK OFSI Consolidated List + AU DFAT Consolidated List + JP MOF Foreign Exchange and Foreign Trade Act sanctions list. The lookup result is signed by named legal counsel with a timestamp that must precede any negotiator engagement. If the attributed threat actor matches any list, payment posture is FORBIDDEN under the relevant law; any communication that could be construed as payment-facilitation is legally prohibited. This step is BLOCKING — the pay/restore decision cannot be made before it is complete.

### Step 4 — Decryptor availability lookup

Execute the decryptor-availability lookup against No More Ransom Project Crypto Sheriff + Emsisoft + Kaspersky NoMoreCry + Bitdefender + Avast for the identified family + encrypted-file sample. Record the result with timestamp. An affirmative match (a working decryptor exists) substantially changes the pay/restore posture — restore via decryptor is preferable to either pay or rebuild for the affected files. Absence in the snapshot does not equal absence live; live lookup is required at decision time, with the operator confirming via a known-clean workstation.

### Step 5 — Immutable-backup viability test

Test the immutable-backup property end-to-end on an isolated network: restore one critical workload from the most recent backup snapshot; verify integrity hash matches a pre-incident reference hash; verify service behavior matches pre-incident baseline. If the test passes, recovery posture is restore-from-immutable-backup. If the test fails (snapshot tampered, replication target accessible to compromised credential, retention policy modified), recovery posture is rebuild-from-clean-media with data loss back to the last clean backup.

### Step 6 — Cyber-insurance carrier 24h notification + pre-approval

Notify the cyber-insurance carrier within the 24h policy window (most policies require this; non-compliance is grounds for policy voiding). Confirm the retained IR firm is on the carrier panel; if not, engage a panel firm. Confirm carrier-pre-approval for the proposed remediation path (restore vs pay vs rebuild). Document the carrier-pre-approval correspondence as evidence.

### Step 7 — Negotiator-engagement decision under sanctions posture

If sanctions match: negotiator engagement is FORBIDDEN. Do not engage a negotiator; do not communicate with the threat actor in any form that could be construed as payment-facilitation. Document the prohibition with legal-counsel sign-off. If no sanctions match: the negotiator-engagement decision is a risk-benefit analysis under legal-counsel + executive-sponsor authority. Engage a retained negotiator from the carrier panel. The negotiator does not authorize payment — that authority rests with the executive sponsor + legal counsel.

### Step 8 — Exfil-before-encrypt classification + parallel breach-notification scope

Classify the exfil-before-encrypt scope independently of the encryption scope: scope the exfiltrated dataset from the 24-72h pre-encryption egress profile + DLP review + adversary leak-site disclosure (if any). If PHI / personal data / financial data / IP was exfiltrated, trigger the applicable breach-notification clocks per the parent playbook's jurisdiction matrix — HIPAA 164.402 risk assessment + GDPR Art.33/34 + state breach laws + UK GDPR + AU NDB scheme. These clocks run in parallel with the availability clocks (NIS2 24h, DORA 4h, CIRCIA 72h).

### Step 9 — Recovery path execution

Execute the determined recovery path: restore from immutable backup (if Step 5 passed), rebuild from clean media (if Step 5 failed AND sanctions block payment), or decryptor-driven restore (if Step 4 returned an affirmative match). For all paths: rotate credentials at the determined blast radius (domain admin, enterprise admin, privileged service accounts, VPN-appliance admin, ScreenConnect / AnyDesk admin, SSO break-glass, AD krbtgt twice), remediate the initial-access vector (patch the exploited CVE, revoke the compromised credentials, harden the VPN appliance / management plane), confirm lateral-movement scope and rotate any compromised identities within it.

### Step 10 — Post-incident learning + framework-gap filing

Per the parent IR playbook Step 9, run the zero-day learning loop: file a `data/zeroday-lessons.json` entry if a new initial-access vector or family pattern was observed; file `data/framework-control-gaps.json` entries for any of the four ransomware-specific decision properties that failed to operationalize; trigger `framework-gap-analysis` for the control-class gap; schedule a ransomware-specific tabletop exercise within 90 days with sanctions-screening + decryptor-lookup + carrier-notification + immutable-backup viability as exercise injects.

**Ephemeral / cloud-workload ransomware (where some controls are architecturally impossible):** Ransomware against cloud workloads is increasingly hypervisor-level (ESXi-targeting families: Akira ESXi locker, ALPHV/BlackCat ESXi locker) or cloud-storage-API-driven (mass encryption of S3 / Azure Blob / GCS object storage via compromised admin credentials). Forensic preservation against ephemeral compute follows the parent playbook's recommendation: pre-incident continuous forensic-grade telemetry shipping to immutable store; absent the pre-incident pipeline, post-hoc evidence is limited to whatever shipped before workload termination and immutable object-storage versions.

---

## Output Format

The skill produces six ransomware-specific artifacts that augment the parent IR playbook's seven artifacts.

### 1. Encryption Confirmation Record

```
Incident ID: INC-<YYYY>-<NNNN>
Encryption confirmed: <yes/no>
Encrypted-host count: <N>
Family fingerprint: <family + confidence>
Ransom note IoCs:
  - Leak-site URL: <onion address>
  - Contact identifier: <email/Tox/Session>
  - Crypto-wallet addresses: <list>
  - Family signature: <text fingerprint>
Shadow Copy deletion observed: <yes/no + timestamp + invoking process>
Living-off-the-land tools observed: <list — PsExec/WMI/PowerShell/AnyDesk/ScreenConnect/Cobalt Strike/Sliver>
EDR encryption-impact alerts: <count + timestamps>
```

### 2. Sanctions Screening Attestation

```
Threat-actor attribution evidence:
  <evidence package — ransom note IoCs, leak-site URL, crypto-wallet, family fingerprint>
Sanctions lookups executed:
  - US OFAC SDN: <result + timestamp + counsel signature>
  - EU Reg 2014/833: <result + timestamp + counsel signature>
  - UK OFSI Consolidated List: <result + timestamp + counsel signature>
  - AU DFAT: <result + timestamp + counsel signature>
  - JP MOF: <result + timestamp + counsel signature>
Match status: <none/partial/full + jurisdictions>
Legal-counsel signature: <name + timestamp>
Negotiator engagement posture: <permitted/forbidden + reasoning>
```

### 3. Decryptor Availability Record

```
Identified family: <name>
Encrypted-file sample (hash): <SHA256>
Lookups executed:
  - No More Ransom Crypto Sheriff: <result + timestamp>
  - Emsisoft: <result + timestamp>
  - Kaspersky NoMoreCry: <result + timestamp>
  - Bitdefender: <result + timestamp>
  - Avast: <result + timestamp>
Decryptor available: <yes/no + version/URL if yes>
Decryptor known failure modes: <list from family-specific documentation>
Recovery path implication: <decryptor-restore preferred / restore-from-backup / rebuild>
```

### 4. Immutable-Backup Viability Record

```
Backup-system inventory: <vendor + storage layer>
Snapshot retention policy: <text>
Immutability mode: <compliance-lock/governance-retention/replication/write-protect>
Admin-identity separation: <production-admin vs backup-admin separated yes/no>
Restore test on isolated network:
  - Workload tested: <name>
  - Pre-incident reference hash: <SHA256>
  - Restored hash: <SHA256>
  - Service-behavior match: <yes/no>
Viability verdict: <viable/compromised + reasoning>
Recovery path implication: <restore-from-immutable / rebuild-from-clean-media>
```

### 5. Insurance Carrier Notification Record

```
Policy number: <number>
Carrier: <name>
Loss notice timestamp: <ISO timestamp — must be within 24h of detect_confirmed>
Carrier acknowledgment: <yes/no + timestamp>
Retained IR firm: <name>
IR firm on panel: <yes/no>
Carrier-pre-approval for proposed remediation: <yes/no/pending + correspondence reference>
Sanctions exclusion in policy: <yes/no + text reference>
24h compliance: <yes/no — non-compliance is grounds for policy voiding>
```

### 6. Exfil-Before-Encrypt Scope Determination

```
Exfil window: <ISO range — 24-72h preceding encryption event>
Destinations identified: <list — MEGA / anonfiles / Tor-egress / rclone-to-S3 / custom>
Cumulative outbound volume per destination: <table>
Exfiltrated dataset scope:
  - PHI records: <count or "none confirmed">
  - PII records: <count or "none confirmed">
  - Financial records: <count or "none confirmed">
  - IP / trade-secret records: <description or "none confirmed">
HIPAA 164.402 risk assessment: <triggered/not-triggered + result>
GDPR Art.33/34 trigger: <yes/no + scope>
State breach laws triggered: <list>
Adversary leak-site disclosure: <yes/no + URL + timestamp>
Parallel-clock notifications engaged: <list per jurisdiction matrix in parent playbook>
```

---

## Compliance Theater Check

Four concrete tests distinguish a real ransomware-recovery posture from theater. Run them in order — each filters out a tier of paper compliance.

> **Test 1 — Test the backup-immutability property end-to-end with a production-admin-credential adversary simulation.** Pick the most recent backup snapshot. From a system holding the same admin credentials used in production (not from the dedicated backup-admin identity), attempt to: (a) delete the snapshot, (b) modify the retention policy to expire the snapshot, (c) modify the replication topology to make the snapshot unreachable, (d) rotate the storage account key. If any of (a)-(d) succeeds, the backup property is replication or write-protect, not immutability. Compliance-lock storage (S3 Object Lock compliance-retention, Azure immutable blob with legal hold, Veeam Hardened Repository with admin-separation, Rubrik / Cohesity immutable-by-policy with admin-separation) is required for the test to pass. The "immutable backup" marketing label without the test is theater.

> **Test 2 — Walk the OFAC sanctions-screening workflow with named legal counsel, end-to-end, with a worked example.** Given an attribution package (ransom note IoCs, leak-site URL, crypto-wallet addresses, family fingerprint for a current 2024-2026 family — Akira, Hunters International, RansomHub, LockBit splinter, Cuba), produce the sanctions-screening attestation within the time-band that precedes a payment decision in a real incident (typically <24h). Counsel-signature workflow, OFAC + EU + UK + AU + JP list-lookup capability, attribution-evidence package format must all exist. If the workflow has never been rehearsed AND counsel has not pre-agreed the format AND the lookup-tool access is not pre-provisioned, the screening will not happen in time during a real incident — and the org runs federal-law violation risk on the payment posture.

> **Test 3 — Show me the cyber-insurance policy clause on ransom-payment, the carrier-panel IR firms, the pre-approval workflow rehearsal record, and the carrier-notification drill outcome.** Read the policy. Confirm: (a) sanctions-exclusion language present; (b) carrier panel of approved IR firms identified and the retained IR firm is on it; (c) pre-approval workflow rehearsed with the broker (not just present in policy text); (d) 24h notification clock workflow exercised end-to-end (loss-notice form, carrier-reachable channel, broker-contact for after-hours). If any element is missing, carrier denial is the dominant economic-exposure failure mode in a real incident — the policy is theater regardless of policy-limit headline.

> **Test 4 — Produce the integrated ransomware tabletop exercise record from the last 12 months with sanctions / decryptor / carrier / immutability / exfil-before-encrypt as exercise injects.** A generic IR tabletop is insufficient; the ransomware-specific tabletop must exercise the four decision properties under time-pressure. The exercise injects: an attributed family (current 2024-2026), a sanctions-list match (test the screening workflow + counsel sign-off), a decryptor-lookup result (test the lookup integration), a carrier-notification (test the broker workflow), a backup-immutability test (test the restore on isolated network), and an exfil-before-encrypt scope determination (test the parallel breach-notification flow). Action items must have owners and completion-status. If the last 12 months contain no such record, the ransomware-recovery capability is paper.

A program passing all four tests is operating ransomware response as infrastructure. A program failing any one is operating ransomware response as paperwork — and the next ransomware incident will run through the gap publicly.

---

## Defensive Countermeasure Mapping

Map this skill's findings to MITRE D3FEND IDs from `data/d3fend-catalog.json` with defense-in-depth layer position, least-privilege scope, zero-trust posture, and AI-pipeline applicability.

Ransomware response consumes defensive controls across multiple D3FEND categories; the four below are the highest-leverage during active ransomware handling. The parent IR playbook covers the broader IR D3FEND cross-walk; this section names the techniques operationally invoked during ransomware response specifically.

| D3FEND ID | Where It Applies in Ransomware Response | Defense-in-Depth Layer | Least-Privilege Scope | Zero-Trust Posture | AI-Pipeline Applicability |
|---|---|---|---|---|---|
| **D3-RPA** (Remote Process Analysis) | Forensic acquisition before destructive containment (memory dump, disk image, syscall trace from affected hosts and immediately-adjacent hosts). Required for sanctions-screening attribution evidence, insurance-claim documentation, and post-incident root-cause analysis. | Containment / Eradication layer. The acquisition runs before destructive containment so the post-incident review has evidence. | Forensic-acquisition tooling scoped to sealed workstation set with chain-of-custody log restricted to named incident-handler roles. | Treat the affected host as adversarial — its self-reported state cannot be trusted; rely on independent telemetry capture. | Limited — applies if AI-system data was exfiltrated within the ransomware operation. |
| **D3-NTA** (Network Traffic Analysis) | Exfil-before-encrypt detection (24-72h egress profile preceding the encryption event); C2 beacon detection (Cobalt Strike / Sliver / Brute Ratel); ongoing lateral-movement detection during containment. | Identification layer (primary for exfil) and Containment / Eradication layer (residual). | NTA scoped to the IR analyst role; full-take capture sealed and accessed under chain-of-custody for evidentiary use. | Default-suspect for unexpected egress patterns; verify per session against the baseline rather than trusting prior allowlist. | Partial — same as parent IR playbook treatment. |
| **D3-IOPR** (Input/Output Profiling) | Limited direct ransomware applicability; relevant when ransomware operation includes AI-system abuse (rare in current ransomware operations but applicable to AI-pipeline data exfiltration). | Identification layer (limited). | Scoped to the IR analyst role. | Default-suspect for prompt-distribution anomalies if AI systems are within scope. | Applies only when AI systems are within the affected scope. |
| **D3-CSPP** (Client-Server Payload Profiling) | C2 protocol detection — particularly relevant when the C2 channel is HTTPS to a legitimate service (Box / OneDrive / S3 / consumer cloud-storage) used for exfil staging. | Identification layer. | Scoped to detection-engineering and IR analyst roles; payload-content access controlled. | Default-suspect for novel payload shapes against baseline. | Limited. |

**No orphaned controls:** each D3FEND technique above maps to one or more TTPs in the TTP Mapping section (T1486 / T1567 / T1078 / T1059). The defensive cross-walk in `defensive-countermeasure-mapping` covers the broader D3FEND ontology; this section names only the techniques operationally invoked during ransomware response.

**AI-pipeline statement:** Direct AI-pipeline applicability to ransomware response is limited; the parent IR playbook covers AI-class incident response separately. If a ransomware operation includes AI-system data exfiltration, hand off the AI-system-specific containment to the parent IR playbook's AI-class sub-flow.

---

## Hand-Off / Related Skills

Ransomware response is a sub-flow of `incident-response-playbook` with ransomware-specific decision properties. Route to the following on the indicated trigger:

- **`incident-response-playbook`** — *parent IR playbook.* All PICERL phase scaffolding, jurisdictional notification matrix, post-incident review template, evidence preservation, and cross-skill hand-off graph are owned by the parent. This skill extends — does not duplicate — the parent.
- **`cred-stores`** *(playbook chain, not a skill)* — *credential-blast-radius trigger.* When ransomware analysis surfaces lateral movement via valid accounts (T1078) and the blast radius extends to credential stores (AD krbtgt, privileged service accounts, SSO break-glass, OAuth grants, AI-agent service accounts), the `_meta.feeds_into` chain on this playbook routes into the `cred-stores` playbook for credential rotation scope determination and rotation orchestration. Hand-off is via the playbook chain, not a skill load.
- **`framework`** *(playbook chain, not a skill)* — *compliance-theater trigger.* When the four ransomware compliance-theater tests in this skill produce a `theater` verdict for the org's pre-incident posture, the `_meta.feeds_into` chain on this playbook routes into the `framework` playbook for cross-framework gap analysis. Hand-off is via the playbook chain, not a skill load. (The `framework-gap-analysis` skill below is a distinct surface — that one IS a real skill and is loaded directly.)
- **`sector-healthcare`** — *PHI exfil-before-encrypt trigger.* When PHI is in the exfiltrated scope, hand off for HIPAA Breach Notification Rule sequencing (45 CFR 164.400-414), state AG notification matrix, and business-associate cascade. State-specific extensions to the 60-day federal clock are routed through this skill.
- **`sector-financial`** — *financial-entity trigger.* When the affected entity is a DORA-in-scope financial entity, hand off for the 4h initial notification chain to competent authority + ECB / EIOPA / ESMA; for NYDFS 500.17 the 24h ransom-payment notification (if payment is made and sanctions screening cleared) is routed through this skill.
- **`framework-gap-analysis`** — *control-gap filing.* When the ransomware response surfaces that one of the four ransomware-specific decision properties (sanctions / decryptor / insurance / immutability / exfil-before-encrypt) failed to operationalize during the incident, file the gap entry against the relevant framework controls (NIST IR-4, ISO A.5.26, SOC 2 CC7.4, HIPAA 164.308(a)(7), AU E8 Backup, UK CAF D1).
- **`compliance-theater`** — *paper-recovery detection.* The four ransomware-specific theater tests in this skill compose with the broader theater detection across frameworks. Run `compliance-theater` after this skill when the org is claiming SOC 2 / ISO 27001 / NIST CSF maturity that the four ransomware-specific tests contradict.
- **`zeroday-gap-learn`** — *novel-vector trigger.* When the initial-access vector is a novel CVE or attack class, file the learning-loop entry so the lesson lands in the catalog before the change ships.
- **`coordinated-vuln-disclosure`** — *vendor-coordination trigger.* When the initial-access vector involves an exploited CVE in a third-party product (VPN appliance, management plane, supply-chain component), coordinate with the vendor advisory and downstream notification cascade.
- **`threat-model-currency`** — *refresh trigger.* The ransomware incident is a real-world signal that the threat model may be stale; trigger a currency refresh.
- **`skill-update-loop`** — *meta-loop trigger.* When the incident exposes a gap in this skill (a new family with unfamiliar sanctions posture, a decryptor catalog not yet integrated, a carrier-policy clause not yet rehearsed), trigger the loop.
