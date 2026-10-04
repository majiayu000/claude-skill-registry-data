---
name: incident-response-playbook
version: "1.0.0"
description: Incident response playbook design for mid-2026 — NIST 800-61r3, ISO 27035, ATT&CK-driven detection, PICERL phases, AI-class incident handling (prompt injection breach, model exfiltration, AI-API C2), cross-jurisdiction breach notification timing
triggers:
  - incident response
  - ir playbook
  - csirt
  - picerl
  - nist 800-61
  - iso 27035
  - breach notification
  - incident handler
  - blue team
  - soc playbook
  - ai incident
  - prompt injection incident
  - model exfiltration incident
data_deps:
  - d3fend-catalog.json
  - framework-control-gaps.json
  - zeroday-lessons.json
atlas_refs:
  - AML.T0096
  - AML.T0013
  - AML.T0024
  - AML.T0051
attack_refs:
  - T1486
  - T1041
  - T1567
  - T1078
framework_gaps:
  - NIST-800-53-AC-2
  - ISO-27001-2022-A.8.16
  - SOC2-CC7-anomaly-detection
  - NIS2-Art21-incident-handling
  - UK-CAF-D1
  - AU-Essential-8-Backup
rfc_refs:
  - RFC-6545
  - RFC-6546
  - RFC-7970
cwe_refs: []
d3fend_refs:
  - D3-RPA
  - D3-NTA
  - D3-IOPR
  - D3-CSPP
forward_watch:
  - NIST 800-61r3 minor revisions (expected 2026-2027) aligning incident-handling language with the in-force EU CRA Art. 11 24h clock and EU AI Act Art. 73 serious-incident reporting
  - ISO/IEC 27035-3:2026 (technical incident response operations) — final publication expected Q3 2026, expected to formalize AI-class incident sub-types currently absent from 27035-1/-2
  - CSAF 2.1 inclusion of incident-status profile (separate from VEX) for correlated advisory + incident records
  - MITRE ATLAS additions for incident-response-relevant techniques: AI-agent-initiated unauthorized action, training-data exfiltration via inference-time prompts
  - ENISA single-reporting-platform expansion: CRA Art. 11 channel goes operational 2026-09, NIS2 Art. 23 incident-reporting overlap to be reconciled
  - AU SOCI Act expanded sector coverage (data-storage and processing entities added 2024; further mandatory-reporting tiers under review)
  - IL INCD Incident Response Process v4 (slated for 2026-2027) consolidating AI-incident sub-class
  - NYDFS 23 NYCRR 500.17 amendments tightening ransom-payment 24h disclosure operationalization
last_threat_review: "2026-09-18"
---

# Incident Response Playbook

Incident response (IR) is the operational closure of every other skill in this catalog. A vulnerability becomes a CVE through `coordinated-vuln-disclosure`; a CVE becomes a lesson through `zeroday-gap-learn`; a lesson becomes a control through `framework-gap-analysis`; an attack on that control becomes an incident — and the incident handler runs the playbook this skill defines. If the playbook is wrong, every preceding investment leaks at the last yard.

This skill operationalizes NIST SP 800-61r3 (Computer Security Incident Handling Guide, 2025 update integrating ATT&CK and Cyber Kill Chain), ISO/IEC 27035-1:2023 (principles and process) + ISO/IEC 27035-2:2023 (guidelines for incident response planning), and the SANS PICERL phases (Preparation, Identification, Containment, Eradication, Recovery, Lessons learned). It threads the Diamond Model and the MITRE Unified Kill Chain for adversary-narrative reconstruction, anchors detection engineering to MITRE ATT&CK v19.2 (May 2026), and treats three incident classes that the legacy IR literature predates: AI-class incidents (prompt-injection breach, model exfiltration, AI-API as C2 channel, AI-agent-initiated unauthorized action), AI-generated supply-chain compromise, and regulator-mandated notification under cross-jurisdiction clocks running in parallel.

---

## Threat Context (mid-2026)

The incident-response landscape in mid-2026 is materially different from the regime the legacy guides describe.

- **Dwell time has compressed, but the window for regulator-clock compliance has compressed faster.** Mandiant M-Trends 2026 reports a global median dwell time of 7 days, down from 16 days in 2022. The classical IR cycle (detect → triage → contain → eradicate → recover → lessons) assumed quarters of engineering capacity. EU CRA Art. 11 (24h early warning for actively exploited vulnerabilities) and EU NIS2 Art. 23 (24h early warning for significant incidents at essential/important entities) collapse the time between "we have telemetry" and "we have a regulator notification due" to less than a day. NYDFS 23 NYCRR 500.17 requires 72h notification of cybersecurity events and 24h notification of ransom payment. CERT-In's 2022 direction requires 6h reporting for in-scope incidents in India. AU SOCI requires 12h notification for significant cyber incidents at critical infrastructure entities. The IR playbook that does not bake these clocks in is non-compliant by clock arithmetic alone.
- **Ransomware continues to dominate the critical-infrastructure incident class.** Healthcare (Change Healthcare 2024, NHS via Synnovis 2024), energy (Colonial Pipeline 2021 echoes through 2026 OT-IT segmentation requirements), manufacturing, and water utilities take the volume. Cl0p's MOVEit campaign (2023) demonstrated mass-exploit incident shape; LockBit-style affiliate ecosystems persist post-takedown via fork brands. Initial-access brokers monetize valid-account compromise (T1078) faster than the credential-rotation cycle.
- **AI-class incidents are operational reality, not a thought experiment.** Three sub-classes show up in 2024-2026 incident telemetry: (1) **prompt-injection breach** — indirect prompt injection via web content, RAG corpus, email signatures, or document metadata achieves unauthorized action against enterprise AI assistants and agentic systems (see `ai-attack-surface`, `rag-pipeline-security`); (2) **model exfiltration** (AML.T0024) — adversary extracts model weights, training data, or system prompts via inference-side attacks (membership inference, training-data extraction, prompt leaking); (3) **AI-API as C2 channel** (AML.T0096) — SesameOp-pattern operations where the adversary uses legitimate AI provider APIs (Claude, ChatGPT, Gemini) as a covert command-and-control channel, blending into legitimate enterprise AI usage. Detection coverage for these classes lags conventional incident classes by 12-24 months in most enterprise SOC stacks.
- **AI-generated code is a new supply-chain incident vector.** GitHub Copilot, Claude Code, Cursor, and Cline produce code that ships to production without the human-author guarantee SLSA Level 3 assumes. Compromise of an AI coding assistant's training data, system prompt, or runtime pipeline (the IDE plugin, the MCP server, the model endpoint) creates a class of supply-chain incident where the artifact in the SBOM has no human author to interview. The Anthropic / OpenAI / Microsoft / Google AI bug-bounty programs are the upstream pipeline; the downstream incident response is largely undocumented at most orgs.
- **Identity is the perimeter, and identity compromise is the dominant initial-access vector.** Snowflake 2024 (credentials harvested from infostealers used to authenticate to multi-tenant cloud without MFA), Microsoft Midnight Blizzard 2024 (legacy non-production tenant compromised via password-spray), and the broader infostealer market collectively make T1078 (Valid Accounts) the most common precursor to subsequent stages.
- **Cloud-ephemeral evidence preservation is the new hard problem.** When the compromised workload is a serverless function (Lambda, Cloud Run, Azure Functions) that scaled to zero before triage starts, or a Kubernetes pod that the scheduler killed and replaced, the chain of custody assumed by NIST 800-86 (Guide to Integrating Forensic Techniques into Incident Response) breaks. Memory, ephemeral disk, and stdout are gone. The mid-2026 fix is pre-incident: continuous forensic-grade telemetry shipping (process trees, syscall traces, network flows, container layer diffs) to an external store before the workload terminates. Most orgs have not configured this; their first incident in an ephemeral environment becomes their lessons-learned moment.

The mid-2026 reality: IR is no longer a quarterly tabletop, an after-hours pager rotation, and a Word-document playbook. It is a real-time pipeline that has to run multiple parallel regulator clocks while preserving ephemeral evidence in environments designed to destroy it, against adversary classes (AI-API C2, prompt-injection breach, agent-initiated unauthorized action) for which the SOC's existing detection stack has limited coverage.

---

## Framework Lag Declaration

IR obligations span four layers — methodology (NIST 800-61r3, ISO 27035, SANS PICERL), governance (NIST 800-53 IR family, ISO 27001 A.5.24/A.5.26, SOC 2 CC7), regulator-mandated reporting (EU CRA, NIS2, AI Act, NYDFS, CERT-In, SOCI), and sectoral (HIPAA breach notification, PSD2 incident reporting, NERC CIP-008). Each layer is partially covered; none is sufficient alone.

| Framework / Jurisdiction | Control | What It Says | Why It Fails as an IR Playbook Spec |
|---|---|---|---|
| NIST SP 800-61r3 (2025) | Computer Security Incident Handling Guide | Integrates MITRE ATT&CK + Cyber Kill Chain into the four-phase handling lifecycle (Preparation; Detection & Analysis; Containment, Eradication & Recovery; Post-Incident Activity). | Does not operationalize AI-class incidents (prompt-injection breach, model exfiltration, AI-API C2). Does not name the EU CRA 24h or NIS2 24h clocks. Ephemeral / serverless evidence preservation receives one paragraph; the operational detail required (continuous telemetry shipping, container layer snapshots) is absent. |
| ISO/IEC 27035-1:2023 | Information security incident management — Principles and process | Process model: plan & prepare → detect & report → assess & decide → respond → learn lessons. | Process-shaped, not playbook-shaped. No AI-class sub-types. No regulator-clock matrix. Conformance does not imply playbook completeness. |
| ISO/IEC 27035-2:2023 | Guidelines to plan and prepare for incident response | Planning, team structure, communication. | Same process orientation. Mentions "external reporting obligations" without operationalizing EU CRA / NIS2 / AI Act / NYDFS clocks. |
| NIST SP 800-53 rev 5 | IR-4 Incident Handling; IR-5 Incident Monitoring; IR-6 Incident Reporting; IR-8 Incident Response Plan | Method-neutral control objectives. | Per `framework-control-gaps.json` NIST-800-53-AC-2: AC-2 (Account Management) does not require AI-agent identity lifecycle management; identity-compromise (T1078) detection feeds IR but the underlying control gap leaves AI-agent service accounts under-instrumented. IR-4 says "implement an incident handling capability" without specifying AI-class handling. |
| ISO/IEC 27001:2022 | A.5.24 Information security incident management planning and preparation; A.5.26 Response to information security incidents; A.8.16 Monitoring activities | Process-level requirements for incident response and monitoring. | Per `framework-control-gaps.json` ISO-27001-2022-A.8.16: monitoring requirements are technology-neutral but AI-system telemetry (prompt logs, embedding-store access, model-output classification) is not addressed. An ISO 27001-certified org with no AI-system monitoring is formally compliant and operationally blind to AML.T0051 / AML.T0096 / AML.T0024. |
| SOC 2 | CC7 (System operations — security event detection, incident response) | Trust services criteria for anomaly detection and incident response. | Per `framework-control-gaps.json` SOC2-CC7-anomaly-detection: CC7 requires anomaly detection without specifying coverage for AI-API C2 (AML.T0096), training-data exfiltration (AML.T0024), or prompt-injection incident triggers (AML.T0051). Auditors test for "an anomaly detection system" without testing whether it covers AI traffic shape. Theater-prone. |
| EU NIS2 Directive (2022/2555) | Art. 23 — incident notification | 24h early warning, 72h initial notification, 1-month final report to national CSIRT for significant incidents at essential/important entities. | Clocks are explicit; significance criteria are partly Member-State-defined; cross-border coordination via ENISA CSIRTs Network. The IR playbook must run the clocks; the directive does not define playbook content. |
| EU DORA (Regulation 2022/2554) | Art. 17 (ICT incident management); Art. 19 (major ICT-related incident reporting); Art. 18 (classification) | Financial-entity-specific: 4h initial notification for major ICT incidents, 72h intermediate, 1-month final, all to competent authority (national + ECB/EIOPA/ESMA depending on entity). | DORA 4h is tighter than NIS2 24h; an entity in scope of both runs whichever is shorter. DORA RTS on classification (2024) defines "major" but the operational determination at the 4h mark requires triage maturity most entities lack. |
| EU AI Act (Regulation 2024/1689) | Art. 73 — serious incident reporting (high-risk AI systems) | High-risk AI providers must report serious incidents to market surveillance authorities within 15 days; 2 days for "widespread infringement" or breaches of fundamental rights. | Clock is longer than CRA/NIS2/DORA but the determination ("serious incident" in an AI system) is novel. Overlap with CRA Art. 11 unresolved — same event may trigger both. |
| EU Cyber Resilience Act (2024/2847) | Art. 11 — vulnerability and incident reporting | 24h early warning to ENISA + national CSIRT for actively exploited vulnerabilities and severe incidents; 72h intermediate; 14d final. | The IR playbook must distinguish "vulnerability exploited" (CRA Art. 11) from "significant incident" (NIS2 Art. 23) — the same event often triggers both, on slightly different definitions, to overlapping but non-identical authorities. |
| UK NCSC Incident Management Process (IMP) | Guidance | Practical IR process guidance; NIS Regulations 2018 (UK NIS post-Brexit) for OES/RDSP reporting. | Guidance not requirement at the IMP level. UK NIS reporting timing similar to pre-Brexit NIS1 (72h). UK GDPR Art. 33 retains 72h personal-data-breach notification. |
| AU ACSC Incident Response Guidance + AU SOCI Act 2018 (as amended) | Critical infrastructure incident reporting | 12h notification of a "significant" cyber incident; 72h for "relevant" incidents at SoNS (Systems of National Significance). | 12h is among the tightest cyber clocks globally for designated CI. SOCI sector coverage expanded 2024 to include data-storage/processing — many entities discover scope mid-incident. |
| JP NISC Incident Response Manual + METI Cybersecurity Management Guidelines v3.0 | National incident response process | National coordination via NISC, sectoral CSIRTs (e.g., JPCERT/CC). | Method-neutral. JP Personal Information Protection Act (APPI) requires personal-data-breach notification to PPC "promptly" — operationally ~3-5 days; tighter for "high-risk" breaches. |
| IL INCD Incident Response Process v3 | National incident response process | Mature national framework with sectoral CERT structure (Finance, Energy, Health). | Among the most operationally detailed national IR frameworks. v4 expected to add AI-incident sub-class. Israel Privacy Protection Authority enforces breach notification under Privacy Protection Regulations (Data Security) 2017 — "without delay." |
| SG CSA Cybersecurity Code of Practice for Critical Information Infrastructure (CCoP2.0) | Critical Information Infrastructure incident reporting | 2h notification of cybersecurity incidents for CII; 24h for others. | 2h is the tightest cyber-incident clock in this matrix; applies only to designated CII. PDPA breach notification: "soon as practicable" and within 3 calendar days for notifiable breaches. |
| IN CERT-In (2022 Directions, effective 2022-06-28) | Reporting of cyber incidents | 6h reporting requirement for in-scope cyber incidents to CERT-In; comprehensive log-retention obligations. | 6h is among the tightest in this matrix; scope is broad (essentially all body-corporates, data centers, service providers). Most enterprises run an internal compliance gap here. |
| BR LGPD (Law 13.709/2018) Art. 48 | Data security incident notification | ANPD notification "in a reasonable time period"; ANPD Resolution CD/ANPD No. 15/2024 operationalized to 3 business days for incidents likely to cause significant risk. | Personal-data-shaped; the cyber-incident-only event without personal-data impact is out of scope. |
| CN MLPS 2.0 (GB/T 22239-2019) + Cybersecurity Law Art. 25 + Data Security Law Art. 29 + PIPL Art. 57 | Multi-level cyber incident reporting | MLPS-level-specific reporting to public security organs; PIPL personal-information-breach notification "immediately." | Multi-track: MLPS (cyber), CSL (network operator), DSL (data handler), PIPL (personal info). Cross-jurisdictional entities run all four. CAC additionally regulates cross-border data flow incidents. |
| NYDFS 23 NYCRR 500.17 | Cybersecurity event notification | 72h notification to NYDFS for covered cybersecurity events; **24h notification of ransom payment** (added by 2023 amendments, in force 2023-12). | Tighter than HIPAA / state breach laws for in-scope entities. Ransom-payment 24h clock is operationally novel — runs in parallel with FBI / OFAC engagement. |
| AE TDRA + UAE Cybersecurity Council Standards | Cyber incident reporting | TDRA reporting for telecom-sector incidents; UAE Information Assurance Standards (IAS) for federal entities; aeCERT national coordination. | Sector-specific clocks. DIFC Data Protection Law 2020 separately requires "without undue delay" personal-data-breach notification. |
| US HIPAA (45 CFR 164.400-414) | Breach Notification Rule | 60d notification to affected individuals + HHS for breaches of unsecured PHI; immediate for >500 individuals to HHS + media. | Health-sector-specific. Slower than cyber-event clocks above. Intersection with cyber-incident reporting (NYDFS for NY health insurers, state laws) creates parallel timers. |
| NERC CIP-008-6 | Cyber security — Incident reporting and response planning | Reportable Cyber Security Incident notification to E-ISAC within 1h of determination. | Electric-sector. 1h is among the tightest sector-specific clocks. CIP-008-7 (in queue) extends to "attempts to compromise." |

Cross-cutting gap: **no IR framework treats AI-class incidents as a first-class category with concrete handling steps.** NIST 800-61r3 (2025) integrates ATT&CK but does not enumerate AML TTPs. ISO 27035 series is process-shaped. Regulator regimes specify clocks but not playbook content. The org-level workaround: extend the playbook library to cover AI-class incidents explicitly. The framework-level fix is pending the next revision cycle.

---

## TTP Mapping

This skill is response-shaped — the TTPs below name the incident classes the playbook library must cover. Each maps to PICERL-phase response procedures (Section 5 / Step 4) and to detection coverage requirements (Section 5 / Step 1).

| TTP ID | Name | Incident Class | PICERL Phase Notes | Gap Flag |
|---|---|---|---|---|
| **T1486** | Data Encrypted for Impact | Ransomware | Identification: EDR file-encryption telemetry, share-mass-write pattern. Containment: network-segment isolation, identity revocation. Eradication: backup-validation-before-restore. Recovery: validated-restore + service-level verification. Lessons: feed to `zeroday-gap-learn` if initial access was a known CVE. | Detection coverage strong; identity-rotation maturity weak. NYDFS 24h ransom-payment clock and OFAC sanctions screening intersect at decision-to-pay. |
| **T1041** | Exfiltration Over C2 Channel | Data exfiltration via established C2 | Identification: DLP egress, anomalous outbound bandwidth, beaconing patterns. Containment: egress filtering, certificate-pinned proxy. Eradication: C2 artifact removal. Recovery: identity + secrets rotation. Lessons: detection-engineering gap analysis. | EDR coverage variable; encrypted exfiltration to legitimate services (Box, OneDrive, S3) often missed by signature-based DLP. |
| **T1567** | Exfiltration Over Web Service | Exfiltration via legitimate web/SaaS services including AI-API | Identification: web-egress to anomalous services or anomalous-volume to legitimate services; for AI-API channel pair with `ai-c2-detection`. Containment: egress block of identified channel, AI-API key revocation, MCP-server scope reduction. Eradication: identify exfiltrated dataset, follow data-incident sub-playbook. Recovery: re-key + re-issue access. | AI-API exfiltration (sub-technique T1567.<sub-technique-id> pattern; ATLAS overlap with AML.T0024) typically blends with legitimate traffic — see `ai-c2-detection` for content-layer detection. |
| **T1078** | Valid Accounts | Identity compromise as initial access | Identification: anomalous-sign-in UEBA, impossible-travel, MFA-fatigue patterns. Containment: account disable + session revocation + re-authentication for affected blast radius. Eradication: credential rotation, token revocation, OAuth-grant audit, AI-agent service-account rotation. Recovery: re-issue under zero-trust posture. Lessons: identity-control gap analysis. | Dominant initial-access vector mid-2026; coverage strong for human accounts, weak for AI-agent / service-account / OAuth-app identities. |
| **AML.T0096** | AI Service API (LLM API as C2) | AI-API as command-and-control channel (SesameOp pattern) | Identification: see `ai-c2-detection` skill — content-layer detection at the AI API egress boundary, prompt-and-response correlation, anomalous AI-API usage shape. Containment: AI-API egress block or proxy-mediated allowlist. Eradication: identify the agent or workload abusing the channel. Recovery: re-issue AI-API keys under scoped least-privilege. | Detection coverage near-absent in legacy SOC stacks; the AI traffic shape is novel and signatures do not exist for most enterprise SIEMs. |
| **AML.T0013** | Discover AI Model Ontology | Adversary mapping of deployed model family, system-prompt structure, guardrails, and training-data signal — precursor to extraction and adversarial-input crafting | Identification: anomalous inference-API usage patterns (high-volume queries, structured probing, membership-inference signatures, repeated training-data extraction prompts). Containment: rate-limit + API-key revocation + IP block. Eradication: identify attacker access surface; assess what model-ontology data was exposed. Recovery: re-key, consider model-rotation if proprietary weights are at risk; for training-data exfiltration consider differential-privacy retraining. | No standardized detection signatures; org must build custom telemetry over AI inference APIs. |
| **AML.T0051** | LLM Prompt Injection | Prompt-injection breach as incident trigger | Identification: AI-assistant or agentic-system anomalous action (unauthorized data access, anomalous tool invocation, identity-context confusion). Containment: revoke AI-system tool scopes, disable agent autonomy, isolate affected RAG corpus. Eradication: identify injection vector (web content, email signature, document metadata, RAG corpus poisoning) and remove. Recovery: re-deploy with hardened system prompt + tool-scoping per `mcp-agent-trust`. | Detection lags; most orgs discover the incident from downstream effect (unauthorized action) rather than detection at the prompt boundary. |

ATLAS pinned to v2026.09 (September 2026). ATT&CK pinned to v19.2 (August 2026); the Defense Evasion (TA0005) split into Stealth (TA0005) and Defense Impairment (TA0112) is traced via `tactic_moved_from` on affected `data/attack-techniques.json` entries and does not introduce breaking changes for the T-IDs cited above.

---

## Exploit Availability Matrix

For IR, "exploit availability" is the question of which incident exemplars are operationally current — i.e., which recent incidents the playbook library must explicitly handle because their TTPs are in active use and their detection patterns are public.

| Incident Exemplar | Year | Class | TTPs | Detection Maturity (mid-2026) | Playbook Implication |
|---|---|---|---|---|---|
| Change Healthcare ransomware | 2024 | Healthcare ransomware + data exfiltration | T1486, T1041, T1078 | Strong for ransomware encryption; weak for the 6-week pre-encryption dwell | Healthcare-sector playbook (`sector-healthcare`) requires HIPAA breach-notification + state AG notification + business-associate cascade. |
| Snowflake customer-tenant compromise | 2024 | Cloud-tenant identity compromise (no MFA) | T1078 | Strong for sign-in anomalies; weak for legacy MFA-not-enforced tenants | Identity-incident playbook requires MFA-status audit + service-account inventory + OAuth-grant review per `identity-assurance`. |
| MOVEit / Cl0p mass exploitation | 2023 | Mass-exploit of file-transfer software | T1190 + T1041 | Vendor-specific signatures available; broader file-transfer-class detection variable | Mass-incident playbook variant: parallel customer notification + supply-chain advisory hand-off to `coordinated-vuln-disclosure`. |
| SolarWinds Sunburst | 2020 | Supply-chain compromise (vendor-shipped malware) | T1195.002, T1041 | Detection capability significantly improved post-incident; SBOM/SLSA adoption | Supply-chain-incident playbook hand-off to `supply-chain-integrity` for VEX response. |
| Volt Typhoon / Salt Typhoon (telecom) | 2023-2024 | Nation-state telecom infrastructure compromise (CCP-attributed by USG) | T1078, T1133, T1556 | Improved post-CISA advisories; living-off-the-land patterns hard to detect | Telecom-sector playbook + national-security coordination. |
| Microsoft Midnight Blizzard | 2024 | Nation-state cloud-tenant compromise via legacy test tenant | T1078 (password spray on legacy account) | Strong for password-spray; weak for legacy-tenant inventory | Identity-hygiene playbook requires legacy-account inventory and decommissioning audit. |
| Anthropic / OpenAI / Microsoft AI bug bounty disclosures (multiple, 2024-2026) | 2024-2026 | Prompt-injection class, jailbreak class, training-data extraction | AML.T0051, AML.T0024 | Detection coverage near-absent in customer SOCs; vendors handle in serving infrastructure | AI-class incident playbook required; the customer-side IR playbook for AI-system anomalies is the gap. |
| Public agentic-system unauthorized-action incidents (research disclosures + named enterprise cases 2024-2026) | 2024-2026 | AI-agent-initiated unauthorized action via indirect prompt injection | AML.T0051 → unauthorized T-action | Detection at the agent-tool boundary, not the prompt boundary | Hand-off to `mcp-agent-trust` for tool-scope hardening; playbook covers agent-disable + scope-revoke + log-replay. |

Detection-tool maturity (mid-2026):
- **SIEM rules for ATT&CK**: high coverage for T1486, T1078, T1041; partial for T1567 (especially T1567 to legitimate AI/cloud SaaS).
- **EDR/XDR**: high coverage for encryption-impact and process-tree anomalies; partial for cloud-workload-only incidents; near-absent for AI-agent process behavior.
- **AI-incident detection**: emerging in 2025-2026; near-absent in legacy SOC stacks. See `ai-c2-detection` for the detection-engineering gap.
- **Identity telemetry**: strong for human accounts (sign-in logs, conditional access, UEBA); weak for AI-agent / service-account / OAuth-app identities.
- **Ephemeral-compute forensic capture**: per Section 1, pre-incident telemetry shipping is the only viable approach; the average enterprise has not configured it.

---

## Analysis Procedure

Before stepping through the IR program assessment, thread the three foundational design principles.

**Defense in depth — IR as a multi-layer pipeline.** A real IR program is not the playbook document; it is the stack that produces the conditions for the playbook to fire and the conditions for it to succeed:
- **Layer 1 — Preparation.** Playbook library (by ATT&CK technique + incident class + sector + jurisdiction), tabletop exercises (at least quarterly, scenarios drawn from current threat-intel feed), runbook tooling (SOAR + ticketing + comms), redundant logging (SIEM + DLP + identity + EDR + AI-system telemetry shipped to immutable store), legal and PR alignment, executive and board awareness, retainer with external IR firm.
- **Layer 2 — Identification.** SIEM correlation rules mapped to ATT&CK; EDR / XDR on every endpoint and workload; UEBA for identity-anomaly detection; AI-incident detectors per `ai-c2-detection` for AML.T0096 / AML.T0024 / AML.T0051; threat-intel feed integration; honeypot / canary telemetry.
- **Layer 3 — Containment.** Network-segment isolation capability (SDN, microsegmentation, firewall policy push); identity revocation capability (Conditional Access, OAuth-grant revocation, service-account rotation); endpoint isolation (EDR-driven network quarantine); AI-API egress block; cloud-workload pause/snapshot.
- **Layer 4 — Eradication and recovery.** Artifact removal (file, registry, scheduled task, persistence mechanism); credential rotation at scope (privileged, service, AI-agent, OAuth app, API key); validated backup restore; AI-system rollback (model version, system prompt, RAG corpus state); service-level verification before declaring recovery.
- **Layer 5 — Lessons learned.** Post-incident review (root-cause analysis using the Diamond Model and the Unified Kill Chain for adversary-narrative reconstruction); playbook update; detection-engineering refinement; control-gap filing per `framework-gap-analysis`; zero-day learning per `zeroday-gap-learn`; threat-model refresh per `threat-model-currency`; skill-update propagation per `skill-update-loop`.

An org that runs only the document layer is brittle. The brittleness pattern: playbook exists but never tabletop-tested (the runbook is fiction); tabletop run but no SIEM correlation rules to fire identification (the runbook is fire-drill-only); identification but no containment capability (alert-fatigue without intervention); containment but no eradication maturity (re-compromise within days); eradication but no lessons-learned pipeline (same incident class repeats).

**Least privilege — IR scope is per-role, not org-wide.** The IR team has read-everywhere, write-narrow access: incident-handler accounts can read SIEM, EDR, identity, DLP, and AI-system telemetry across the org but write only to ticketing, incident-comms, and the IR-team workspace. Containment actions (network isolation, identity disable, service-account rotation) are performed via SOAR with audit trail, not direct admin access. Break-glass accounts are vaulted with dual-control retrieval and post-use rotation. AI-incident specialists are scoped to the AI tool inventory (model endpoints, MCP servers, agent runtimes, RAG corpora) and do not get blanket admin to non-AI infrastructure. Forensic-acquisition tooling is scoped to a sealed workstation set with chain-of-custody logging. External counsel and external IR firm receive scoped access per engagement.

**Zero trust — assume the network is hostile during containment; identity is not trusted until re-verified after compromise.** During an active incident: assume the SOC's own tooling may be compromised and validate findings via an independent channel where critical; assume the attacker may be reading the IR team's communications (use out-of-band comms — Signal, dedicated incident-bridge with separate identity, never the corporate Slack the attacker may be in); revoke and re-issue identities rather than trusting that "this account doesn't show compromise indicators"; revoke AI-system tool scopes and re-issue under the post-incident scoping policy, not the pre-incident one; verify-not-assume that backup integrity has not been tampered with before restore.

Then run the 10 program-assessment / live-incident steps.

### Step 1 — Detection coverage audit (the "would we identify this" check)

Before any incident fires, audit detection coverage against the ATT&CK + ATLAS techniques the playbook library is supposed to cover:
- Map each playbook in the library to one or more ATT&CK / ATLAS techniques.
- For each technique, identify the detection rule, the log source, the false-positive baseline, and the tested-fire status.
- Identify coverage gaps: techniques with no rule, rules with no log source, rules with no recent test fire.
- Specifically audit AI-class detection: AML.T0096 (AI-API egress shape — hand off to `ai-c2-detection`), AML.T0024 (anomalous inference-API usage), AML.T0051 (downstream-action anomaly).
- Specifically audit identity detection: T1078 sub-technique coverage (cloud accounts, default accounts, domain accounts, local accounts) and service-account / AI-agent variants.

### Step 2 — Incident classification taxonomy (the "what is this" check)

When an incident fires, classify before responding. Classification dimensions:
- **ATT&CK technique(s)** — primary and secondary. Tactic chain for adversary-narrative.
- **ATLAS technique(s)** — for AI-class incidents.
- **Incident class** — ransomware, data exfiltration, identity compromise, supply-chain, AI-system breach, business-email-compromise, DoS, insider, other.
- **Impact severity** — confidentiality / integrity / availability per the org's incident-severity matrix.
- **Jurisdictional notification clock** — per the matrix in Section 7. Which clocks start, when did they start (awareness moment), who is the named officer per clock.
- **AI-class flag** — does the incident involve an AI system as victim, vector, or attacker? AI-as-victim: AML.T0051/AML.T0024. AI-as-vector: AML.T0096. AI-as-attacker: agent-initiated unauthorized action.
- **Sector flag** — does a sectoral framework apply (`sector-healthcare`, `sector-financial`, `sector-energy`, `sector-federal-government`)?

### Step 3 — Declaration and runbook activation

Once classified:
- Declare the incident at the appropriate severity (incident commander assignment, comms-bridge stand-up, executive notification per matrix).
- Activate the playbook from the library matching the classification.
- Start the regulator-clock timers — each applicable jurisdiction's clock runs in parallel from the awareness moment.
- Assign named owners per regulator-notification channel.
- Brief the IR firm retainer if scope warrants.

### Step 4 — Containment per playbook class (PICERL: Containment)

Apply containment matching the class. Common patterns:
- **Ransomware (T1486)**: network-segment isolation for affected hosts; identity revocation for compromised accounts; **do not pay yet** — preserve optionality; backup-integrity verification before recovery decisions.
- **Data exfiltration (T1041 / T1567)**: egress block at the identified channel; certificate-pinned proxy enforcement; identify what was exfiltrated (scope determination drives notification scope).
- **Identity compromise (T1078)**: account disable, session revocation, MFA re-enrollment, OAuth-grant audit; for service / AI-agent accounts, scope-reduce + rotate.
- **AI-API C2 (AML.T0096)**: AI-API egress block or proxy-mediated allowlist; identify the workload abusing the channel; AI-API key revocation.
- **Model ontology discovery (AML.T0013)**: rate-limit the inference API; revoke the abusing API key; IP-block as supplemental; assess what model-ontology data (system prompt, guardrail surface, model family signal) was exposed and tighten the inference-API rate + shape baseline before re-issue.
- **Prompt-injection breach (AML.T0051)**: disable the affected agent autonomy or revoke its tool scopes; isolate the RAG corpus suspected as injection vector; capture the injected content for forensics.
- **Supply-chain (T1195)**: identify affected component versions via SBOM; coordinate with vendor (hand off to `coordinated-vuln-disclosure` reverse-direction — receiving vendor advisory); VEX-driven inventory of affected workloads.

For all classes: **preserve evidence before destructive containment.** In ephemeral environments, that means triggering pre-configured forensic-grade telemetry capture (memory snapshot, container layer diff, syscall trace) before scaling the workload to zero or killing the pod. Where the telemetry pipeline was not pre-configured, the lessons-learned phase produces a Section 10 action item to configure it.

### Step 5 — Eradication and recovery (PICERL: Eradication, Recovery)

Eradication:
- Remove malicious artifacts (files, registry, scheduled tasks, services, container images, malicious model weights or system prompts).
- Rotate credentials at the determined blast-radius scope.
- Patch the exploited vulnerability (hand off to `zeroday-gap-learn` if zero-day; coordinate with vendor advisory per `coordinated-vuln-disclosure`).
- For AI-system incidents: rollback model version, re-deploy system prompt under hardened scope, scrub RAG corpus, re-validate tool-scoping per `mcp-agent-trust`.

Recovery:
- Validated backup restore (integrity verified, restore-test in isolated environment before production).
- Service-level verification — does the restored service exhibit the pre-incident behavior profile?
- Phased re-introduction — restore in stages with telemetry watching for re-compromise indicators.
- Identity re-verification for users affected by mass revocation — re-enroll MFA, re-issue tokens.

### Step 6 — Regulator notification per jurisdiction matrix (PICERL: spans Containment / Eradication / Recovery / Lessons)

Run each jurisdiction's clock in parallel from the awareness moment. The notification template per jurisdiction is in Section 7 (Output Format). Verify the named officer per clock is engaged within the first hour of declaration. Reconcile overlapping reports (CRA Art. 11 + NIS2 Art. 23 + DORA Art. 19 + AI Act Art. 73 may all trigger for one event; the org files four reports on four clocks to overlapping authorities).

### Step 7 — Evidence preservation and chain of custody

Per NIST 800-86:
- Acquire memory, disk, network capture, and log copies via documented forensic procedures.
- Hash artifacts at acquisition; chain-of-custody log maintained throughout.
- Store in evidence-management system with sealed access (least-privilege scope per Section 5 / least-privilege thread).
- For ephemeral compute: rely on the pre-incident telemetry pipeline (continuous forensic-grade capture to immutable store). If the pipeline was not configured pre-incident, document the gap as a Section 10 action item and acquire whatever post-hoc evidence is recoverable (logs that shipped before workload termination, immutable object-storage versions, audit trails).
- For AI-system evidence: prompt logs, response logs, embedding-store access logs, model-version metadata, system-prompt revision history, tool-invocation logs, RAG corpus state at incident time.

### Step 8 — Post-incident review (PICERL: Lessons learned)

Within 14 days of recovery (or sooner for severe incidents):
- Adversary-narrative reconstruction using the Diamond Model (adversary, infrastructure, capability, victim) and the MITRE Unified Kill Chain (extended kill chain stages).
- Root-cause analysis: what control failed at which kill-chain stage? Was it a control gap (no control existed), a control failure (control existed but didn't fire), a control bypass (control fired but was evaded), or a detection gap (control fired but the signal was missed)?
- Detection-engineering refinement: new SIEM rules, EDR queries, AI-system telemetry hooks.
- Playbook refinement: did the playbook match the incident? Update where it didn't.
- Action items with owners and dates.

### Step 9 — Learning-loop feedback (cross-skill hand-offs)

Per the zero-day learning loop and the skill graph:
- File `data/zeroday-lessons.json` entry per `zeroday-gap-learn` if a zero-day or new attack class was involved.
- File `data/framework-control-gaps.json` entry per `framework-gap-analysis` if a control-class gap was exposed.
- Trigger `threat-model-currency` refresh — the incident is a real-world signal that the threat model may be stale.
- Trigger `skill-update-loop` if the incident exposes a gap in the skill library itself (a class of incident with no playbook, a TTP with no skill, a jurisdiction with no notification matrix entry).
- For AI-class incidents, feed `ai-attack-surface`, `rag-pipeline-security`, `mcp-agent-trust`, and `ai-c2-detection` with the observed attack pattern.

### Step 10 — Continuous improvement metrics

Per ISO 27035-1:2023 §6 and NIST 800-61r3 post-incident activity:
- Mean time to detect (MTTD), mean time to acknowledge, mean time to contain, mean time to recover — by incident class.
- Regulator-clock on-time rate per jurisdiction.
- Tabletop exercise frequency and follow-up-completion rate.
- Detection coverage percentage (ATT&CK / ATLAS techniques covered vs. total in scope).
- Playbook coverage percentage (incident classes with playbook vs. total observed in 24-month window).
- AI-class incident detection latency vs. conventional-class incident detection latency — the operationally-relevant gap metric for mid-2026.

**Ephemeral / serverless / AI-pipeline reality:** Evidence preservation in serverless and container environments is the new hard problem of mid-2026 IR. NIST 800-86 forensic procedures assume the workload still exists at acquisition time. For Lambda / Cloud Run / Azure Functions / Knative / Kubernetes pods scaled to zero, the workload is gone before the SOC opens the ticket. The architecturally honest recommendation: configure continuous forensic-grade telemetry shipping pre-incident (process trees, syscall traces, network flows, container-layer diffs, AI-system prompt / response / tool-invocation logs) to an external immutable store. Treat the absence of this pipeline as a precondition for incident-evidence-loss and document it as a control gap per `framework-gap-analysis` before the first incident, not after.

---

## Output Format

The skill produces seven artifacts per IR program assessment or live incident.

### 1. Incident Classification Record

```
Incident ID: INC-<YYYY>-<NNNN>
Awareness timestamp: <ISO timestamp — the regulator-clock anchor>
Declared severity: <Sev1/2/3>
Incident commander: <named>
Classification:
  ATT&CK techniques: <T-IDs with sub-techniques>
  ATLAS techniques: <AML.T-IDs, if applicable>
  Incident class: <ransomware/exfiltration/identity/supply-chain/AI-system/BEC/DoS/insider/other>
  Sector flag: <healthcare/financial/energy/federal/none>
  AI-class flag: <victim/vector/attacker/none>
  Cross-skill hand-offs triggered: <coordinated-vuln-disclosure / zeroday-gap-learn / ai-c2-detection / ...>
Jurisdictional clocks started:
  EU CRA Art. 11: <ISO timestamp + 24h> — officer <name>
  EU NIS2 Art. 23: <ISO timestamp + 24h> — officer <name>
  EU DORA Art. 19 (if financial): <ISO timestamp + 4h> — officer <name>
  EU AI Act Art. 73 (if high-risk AI): <ISO timestamp + 15d / 2d> — officer <name>
  NYDFS 500.17 (if NY): <ISO timestamp + 72h; +24h if ransom paid> — officer <name>
  CERT-In (if IN): <ISO timestamp + 6h> — officer <name>
  AU SOCI (if AU CI): <ISO timestamp + 12h> — officer <name>
  SG CSA CCoP2.0 (if SG CII): <ISO timestamp + 2h> — officer <name>
  UK NIS / UK GDPR (if UK): <ISO timestamp + 72h> — officer <name>
  JP NISC / APPI (if JP): <ISO timestamp + 3-5d> — officer <name>
  IL INCD / Privacy Protection Regulations (if IL): <ISO timestamp + "without delay"> — officer <name>
  BR LGPD (if BR personal data): <3 business days> — officer <name>
  CN MLPS + CSL + DSL + PIPL (if CN): <multi-track per scope> — officer <name>
  AE TDRA (if AE): <sector-specific> — officer <name>
  HIPAA / NERC CIP-008 / sector-specific (as applicable): <per matrix> — officer <name>
```

### 2. Runbook Library Structure

```
runbooks/
  by-attack-technique/
    T1486-ransomware.md
    T1041-c2-exfil.md
    T1567-web-service-exfil.md
    T1078-valid-accounts.md
    T1195-supply-chain.md
    T1190-public-facing-app.md
    ...
  by-atlas-technique/
    AML-T0051-prompt-injection.md
    AML-T0024-model-exfiltration.md
    AML-T0096-llm-api-c2.md
    ...
  by-incident-class/
    ransomware.md
    data-breach.md
    business-email-compromise.md
    ai-system-breach.md
    agent-unauthorized-action.md
    ddos.md
    insider-data-loss.md
  by-sector/
    healthcare-hipaa.md
    financial-dora-nydfs.md
    energy-nerc-cip-008.md
    federal-fisma.md
  by-jurisdiction/
    eu-cra-nis2-aiact.md
    uk-nis-gdpr.md
    au-soci-acsc.md
    jp-nisc-appi.md
    il-incd.md
    sg-csa-ccop.md
    in-cert-in.md
    br-lgpd.md
    cn-mlps-csl-dsl-pipl.md
    nydfs-500-17.md
    ae-tdra.md
```

Each runbook contains: classification triggers, identification signals, containment steps (with named SOAR action), eradication checklist, recovery validation, communication template, regulator-notification references, hand-off triggers.

### 3. Containment Script Catalog (SOAR Actions)

```
containment/
  network/
    isolate-host.yaml          # EDR-driven; rollback time-boxed
    block-egress.yaml          # firewall + proxy
    segment-quarantine.yaml    # SDN microsegmentation push
    ai-api-egress-block.yaml   # AI-provider domain block + proxy enforcement
  identity/
    disable-account.yaml       # IdP + AD + cloud-IAM
    revoke-sessions.yaml       # all SSO + OAuth grants
    rotate-service-account.yaml
    rotate-ai-agent-identity.yaml
    revoke-api-keys.yaml       # incl. AI provider keys
    revoke-oauth-grants.yaml
  endpoint/
    edr-quarantine.yaml
    memory-snapshot.yaml
    forensic-acquisition.yaml
  cloud-workload/
    snapshot-and-pause.yaml
    ephemeral-evidence-capture.yaml  # for serverless / container ephemeral environments
  ai-system/
    disable-agent-autonomy.yaml
    revoke-tool-scopes.yaml
    rollback-model-version.yaml
    isolate-rag-corpus.yaml
    rate-limit-inference-api.yaml
```

### 4. Regulatory Notification Matrix

The matrix maps jurisdiction × incident class × clock × authority × named officer. The shape:

| Jurisdiction | Authority | Clock | Triggering Incident Classes | Notification Channel | Named Officer |
|---|---|---|---|---|---|
| EU (CRA Art. 11) | ENISA + national CSIRT | 24h early / 72h intermediate / 14d final | actively exploited vulnerability + severe incident in product with digital elements | ENISA single reporting platform (operational 2026-09) | <name> |
| EU (NIS2 Art. 23) | national CSIRT | 24h early / 72h initial / 1m final | significant incident at essential/important entity | per Member State | <name> |
| EU (DORA Art. 19) | competent authority (national + ECB/EIOPA/ESMA) | 4h initial / 72h intermediate / 1m final | major ICT-related incident at financial entity | per RTS | <name> |
| EU (AI Act Art. 73) | market surveillance authority | 15d / 2d (fundamental rights / widespread infringement) | serious incident in high-risk AI system | per Member State | <name> |
| UK (NIS Regulations + UK GDPR) | NCSC + ICO | 72h | OES/RDSP significant incident; personal-data breach | per regulator | <name> |
| AU (SOCI Act) | ASD ACSC | 12h significant / 72h relevant | designated CI cyber incident | ReportCyber / direct | <name> |
| JP (NISC + APPI) | NISC + PPC | "promptly" (~3-5d operational) | designated CI / personal-data breach | per regulator | <name> |
| IL (INCD + PPA) | INCD + Privacy Protection Authority | "without delay" | national-significance / personal-data breach | per regulator | <name> |
| SG (CSA CCoP2.0 + PDPC) | CSA + PDPC | 2h CII / 24h others / 3d notifiable PDPA | CII cyber incident; notifiable personal-data breach | per regulator | <name> |
| IN (CERT-In 2022 Directions) | CERT-In | 6h | broad cyber-incident scope | CERT-In portal | <name> |
| BR (LGPD Art. 48) | ANPD | 3 business days for significant-risk events | personal-data security incident | ANPD portal | <name> |
| CN (MLPS + CSL + DSL + PIPL) | public security organs + CAC | per-track | network operator / data handler / personal info | per regulator | <name> |
| US-NYDFS (23 NYCRR 500.17) | NYDFS | 72h event / 24h ransom payment | covered cybersecurity event; ransom payment | NYDFS portal | <name> |
| US-HIPAA (45 CFR 164.400) | HHS OCR + state AGs | 60d individuals + HHS; immediate for >500 | unsecured-PHI breach | per regulator | <name> |
| US-NERC (CIP-008-6) | E-ISAC | 1h | Reportable Cyber Security Incident | E-ISAC portal | <name> |
| AE (TDRA + IAS + DIFC DP) | TDRA + UAE CSC + DIFC Commissioner | per sector | telecom / federal / DIFC personal-data | per regulator | <name> |

The org instantiates the matrix per its scope; multi-jurisdictional entities run multiple rows concurrently for a single event.

### 5. Post-Incident Review Template

```
# Post-Incident Review — INC-<YYYY>-<NNNN>

## Executive Summary
<2-3 paragraphs: what happened, what was impacted, what was contained, what's next>

## Timeline
| Timestamp | Event | Source |
|---|---|---|
| ... | ... | ... |

## Adversary Narrative (Diamond Model)
- Adversary: <attribution confidence + indicators>
- Infrastructure: <C2, hosting, identity>
- Capability: <tools, techniques, exploits>
- Victim: <scope of impact>

## Adversary Narrative (Unified Kill Chain)
For each stage (reconnaissance, weaponization, delivery, exploitation, persistence, defense evasion, command-and-control, action-on-objective):
- Observed: <evidence>
- Detected: <which control fired, when>
- Missed: <which control should have fired and didn't>

## Root Cause Analysis
- Control gaps: <controls that did not exist>
- Control failures: <controls that existed and did not fire>
- Control bypasses: <controls that fired and were evaded>
- Detection gaps: <signals present but not surfaced>

## Action Items
| Item | Owner | Due | Status |
|---|---|---|---|
| ... | ... | ... | ... |

## Cross-Skill Hand-Offs
- zeroday-gap-learn entry: <reference>
- framework-gap-analysis entry: <reference>
- threat-model-currency refresh: <reference>
- skill-update-loop changes: <reference>
- ai-c2-detection / ai-attack-surface / mcp-agent-trust feedback (if AI-class): <reference>

## Metrics
- MTTD: <time>
- MTTC: <time>
- MTTR: <time>
- Regulator-clock on-time per jurisdiction: <table>
```

### 6. Tabletop Exercise Record

```
Exercise: <name>
Date: <ISO date>
Scenario: <one-paragraph; map to ATT&CK / ATLAS techniques>
Participants: <roles, not names — but record names internally>
Injects: <numbered list>
Observations: <gaps, friction, ambiguity>
Action items: <list with owners and dates>
Next exercise: <ISO date>
```

A program with no tabletop record in the last 12 months fails the Compliance Theater Check Test 1.

### 7. Lessons-Learned Feedback Record (for skill-update-loop)

```
Source incident: INC-<YYYY>-<NNNN>
Date: <ISO date>
Feedback target: <skill-update-loop / threat-model-currency / framework-gap-analysis / specific skill>
Change required: <specific edit to a specific skill or data file>
Rationale: <one paragraph linking the incident observation to the change>
Filed by: <role>
```

---

## Compliance Theater Check

Four concrete tests distinguish a real IR program from IR theater. Run them in order — each filters out a tier of paper compliance.

> **Test 1 — Show me your last tabletop exercise outcome and the assigned follow-ups, with completion status.** If the answer is "we don't run tabletops" or "the last one was more than 12 months ago" or "we ran one but didn't track follow-ups," the program is paper IR. ISO 27035-1:2023 §5 and NIST 800-61r3 both require tested incident-handling capability; an untested playbook is a hypothesis. If follow-ups were assigned but not completed, the tabletop was a compliance artifact, not an improvement loop. Particular smell: tabletops only at the IT level (no executive participation, no legal, no PR, no external counsel rehearsal) — these will miss the realities of decision-making at 3am during a regulator-clock event.

> **Test 2 — Walk me through your EU DORA 4-hour initial-notification process, named officer included.** Substitute the tightest jurisdictional clock that applies to the org (DORA 4h for in-scope financial entities; SG CSA CCoP2.0 2h for SG CII; NERC CIP-008 1h for North American electric utilities; CERT-In 6h for India-operating entities; AU SOCI 12h; CRA Art. 11 24h for EU manufacturers). If the answer is "we'll figure it out when it happens" or "legal will handle it," the program will miss the clock during a real incident. The named officer must be identifiable, reachable on a documented out-of-band channel, and trained on the determination criteria for the relevant "significance" or "major" or "actively exploited" thresholds. If the org cannot produce the named officer's contact card and the decision tree they will use at 03:00 on a Saturday, the regulator-notification capability is theater.

> **Test 3 — Do you have an AI-class incident playbook, and when was it last exercised?** Three failure modes signal theater: (a) "AI is just IT — we use our normal playbook" — the org has not engaged with AML.T0096 / AML.T0024 / AML.T0051 detection and containment specifics; (b) "we don't run AI systems" — verify against actual product surface (Copilot, Claude, ChatGPT, Gemini, AI features embedded in SaaS, internal agentic systems, RAG features); (c) "we have a draft playbook but never tested it" — untested AI-class playbooks fail at the same rate as untested conventional playbooks, but the failure modes are unfamiliar to the SOC. Particular smell: the AI-class playbook exists in the security team's shared drive but the AI-platform team and the data-science team have never seen it. AI-incident response requires cross-team rehearsal; AML.T0024 forensics requires data-science skills the SOC does not have.

> **Test 4 — Enumerate every jurisdictional notification clock that applies to your operations, name the officer for each, and produce the last drill record per clock.** If the org cannot enumerate clocks — clocks are discovered mid-incident, while running them late — the program will miss at least one in a real cross-jurisdictional event. The minimum enumeration for a multinational organization: EU (CRA Art. 11 + NIS2 Art. 23 + DORA Art. 19 if financial + AI Act Art. 73 if high-risk AI), UK (NIS + UK GDPR), AU (SOCI), JP (NISC + APPI), IL (INCD + PPA), SG (CSA CCoP2.0 + PDPC), IN (CERT-In), BR (LGPD), CN (MLPS + CSL + DSL + PIPL), US-NYDFS, US-HIPAA (if in scope), US-NERC (if in scope), AE (TDRA + DIFC DP). For each: clock, authority, channel, named officer, last drill. If the clocks live in a regulatory-comms team's binder rather than the IR runbook library, the program will run them out of sequence with the technical response and burn one of them.

A program passing all four tests is operating IR as infrastructure. A program failing any one is operating IR as paperwork — and the next regulator clock will run through the gap publicly.

---

## Defensive Countermeasure Mapping

This section maps this skill's findings to MITRE D3FEND IDs from `data/d3fend-catalog.json` with explicit defense-in-depth layer position, least-privilege scope, zero-trust posture, and AI-pipeline applicability.

IR consumes defensive controls across multiple D3FEND categories; the four cited below are the highest-leverage during active incident handling.

| D3FEND ID | Where It Applies in IR | Defense-in-Depth Layer | Least-Privilege Scope | Zero-Trust Posture | AI-Pipeline Applicability |
|---|---|---|---|---|---|
| **D3-RPA** (Remote Process Analysis) | Forensic acquisition during containment and eradication. Memory, syscall trace, container layer diff acquired from compromised hosts and from suspected-but-not-confirmed lateral-spread hosts. For ephemeral compute, applies to the immutable telemetry pipeline that captured the process state before workload termination. | Containment / Eradication layer. The acquisition runs *before* destructive containment so the post-incident review has evidence. | Forensic-acquisition tooling scoped to a sealed workstation set; chain-of-custody log restricts access to named incident-handler roles. | Treat the host as adversarial — its self-reported state cannot be trusted; rely on independent telemetry capture. | Applies — AI-system process analysis includes inference-runtime telemetry (prompt logs, response logs, tool-invocation logs), agent process trees, and MCP-server interaction logs. The AI-pipeline equivalent of memory capture is the prompt-and-response state at the incident time. |
| **D3-NTA** (Network Traffic Analysis) | Egress detection during identification; lateral-movement detection during containment; post-incident hunt for residual adversary infrastructure. For data-exfiltration incidents (T1041 / T1567), NTA is the primary identification surface. For AI-API C2 (AML.T0096) NTA alone is insufficient because the egress is to legitimate AI provider domains — pair with D3-CSPP for content-layer detection. | Identification layer (primary) and Containment / Eradication layer (residual). | NTA scoped to the IR analyst role; full-take capture is sealed and accessed under chain-of-custody for evidentiary use. | Default-suspect for unexpected egress patterns; verify per session against the baseline rather than trusting prior allowlist. | Partial — AI-API egress traffic shape is novel and most NTA stacks do not have signatures for AML.T0096. Pair with `ai-c2-detection` skill recommendations. |
| **D3-IOPR** (Input/Output Profiling) | AI-API egress correlation and SaaS-egress anomaly detection. For AI-system incidents, profiling the input (prompt) and output (response) distribution is the defensive surface that can detect AML.T0051 (anomalous prompt patterns), AML.T0024 (extraction-pattern queries), and AML.T0096 (C2-channel encoded payloads). | Identification layer (primary for AI-system incidents). | Scoped to the AI-incident specialist role; raw prompts and responses may contain confidential data and must be access-controlled per data-classification policy. | Default-suspect for prompt distributions outside the baseline; do not whitelist by source identity alone — verify per request. | High applicability — D3-IOPR is the highest-leverage D3FEND technique for AI-system incident detection and is the operational complement to D3-NTA when the egress is to a legitimate AI provider. |
| **D3-CSPP** (Client-Server Payload Profiling) | C2 protocol detection during identification; AI-API content-layer detection for AML.T0096. Where the C2 channel is HTTPS to a legitimate service (Box, OneDrive, S3, AI provider), CSPP is the content-shape detection surface that catches the abuse pattern. | Identification layer. | Scoped to the detection-engineering and IR analyst roles; payload-content access controlled. | Default-suspect for novel payload shapes against baseline; verify-not-assume that previously-good clients have not been compromised. | Applies — particularly for AI-API C2 detection where TLS termination at an enterprise proxy enables payload-shape analysis of prompts and responses. |

**No orphaned controls**: each D3FEND technique above maps to one or more incident classes in the TTP Mapping section (T1486 / T1041 / T1567 / T1078, AML.T0096 / AML.T0024 / AML.T0051). The defensive cross-walk in `defensive-countermeasure-mapping` covers the broader D3FEND ontology; this section names only the techniques operationally invoked during IR.

**AI-pipeline statement**: D3FEND coverage of AI-incident defense is concentrated in D3-IOPR (input/output profiling) and the content-layer subset of D3-CSPP. The ephemeral-compute evidence-preservation problem is largely outside the D3FEND ontology as of mid-2026; the operational fix (continuous forensic-grade telemetry shipping to immutable store) is documented in `attack-surface-pentest` and `defensive-countermeasure-mapping` as a control gap pending ontology coverage.

---

## Hand-Off / Related Skills

IR sits downstream of detection and upstream of organizational learning. Route to the following on the indicated trigger:

- **`coordinated-vuln-disclosure`** — *upstream input.* When IR identification surfaces a vulnerability against an org product (received via researcher report, bug-bounty queue, or customer escalation), hand off to the CVD intake pipeline. Conversely, when CVD output identifies a vulnerability that is being actively exploited, the resulting EU CRA Art. 11 24h clock is run by the IR team using this skill's regulator-notification matrix.
- **`zeroday-gap-learn`** — *downstream learning loop.* Every incident with a novel attack class or a zero-day vector triggers a learning-loop entry. If IR is operating but `data/zeroday-lessons.json` entries are not being filed, the hand-off is broken.
- **`threat-model-currency`** — *downstream refresh trigger.* An incident is the strongest real-world signal that the threat model may be stale; trigger the currency refresh routine.
- **`compliance-theater`** — *paper-IR detection.* The four compliance theater tests in this skill compose with the broader theater detection across frameworks; run `compliance-theater` after this skill when the org is claiming SOC 2 / ISO 27001 / NIST CSF / HIPAA maturity that the IR test results contradict.
- **`framework-gap-analysis`** — *control-gap filing.* When an incident exposes that an existing control was insufficient to detect, prevent, or contain, file the gap under the appropriate framework entry per `data/framework-control-gaps.json`.
- **`dlp-gap-analysis`** — *data exfiltration incident class.* T1041 / T1567 / AML.T0024 incidents hand off to DLP gap analysis for the egress-control assessment.
- **`ai-c2-detection`** — *AML.T0096 incident trigger.* AI-API as C2 channel detection feeds IR identification; this skill consumes those detections.
- **`ai-attack-surface`**, **`rag-pipeline-security`**, **`mcp-agent-trust`** — *AI-class incident depth.* AML.T0051 and AI-agent-initiated unauthorized action route through these skills for vector identification and containment depth.
- **`defensive-countermeasure-mapping`** — *full D3FEND cross-walk* beyond the four IDs cited in the Defensive Countermeasure Mapping section above.
- **`sector-healthcare`** — *HIPAA Breach Notification Rule sequencing* for health-sector incidents.
- **`sector-financial`** — *DORA Art. 19 4h clock + NYDFS 500.17 + PSD2 incident reporting + SWIFT CSCF* for financial-sector incidents.
- **`sector-federal-government`** — *FISMA / CISA BOD / OMB M-22-09 zero-trust* reporting overlap for federal entities.
- **`sector-energy`** — *NERC CIP-008-6 1h E-ISAC reporting + TSA pipeline directives + AESCSF + NCCS-G* for energy-sector incidents.
- **`skill-update-loop`** — *meta-loop trigger.* When an incident exposes a skill-library gap (incident class with no playbook, TTP with no skill, jurisdiction with no notification matrix entry), trigger the loop.
- **`global-grc`** — *cross-jurisdiction routing* when the incident intersects multiple regulator regimes (the common case for multinational organizations).
