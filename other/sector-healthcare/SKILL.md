---
name: sector-healthcare
version: "1.0.0"
description: Healthcare sector cybersecurity for mid-2026 — HIPAA + HITRUST + HL7 FHIR security, medical device cyber (FDA + EU MDR), AI-in-healthcare under EU AI Act + FDA AI/ML SaMD guidance, patient data flows through LLM clinical tools
triggers:
  - healthcare security
  - hipaa
  - hitrust
  - hl7
  - fhir
  - phi
  - protected health information
  - medical device security
  - samd
  - fda cyber
  - eu mdr
  - clinical decision support
  - ai diagnostic
  - patient data
data_deps:
  - cve-catalog.json
  - d3fend-catalog.json
atlas_refs:
  - AML.T0051
  - AML.T0017
  - AML.T0013
attack_refs:
  - T1078
  - T1530
  - T1567
framework_gaps:
  - HIPAA-Security-Rule-164.312(a)(1)
  - HITRUST-CSF-v11.4-09.l
  - ISO-27001-2022-A.8.30
  - NIST-800-53-AC-2
  - NIS2-Art21-incident-handling
  - UK-CAF-D1
  - AU-Essential-8-Backup
rfc_refs:
  - RFC-7519
  - RFC-9421
cwe_refs:
  - CWE-200
  - CWE-287
  - CWE-862
  - CWE-1426
d3fend_refs:
  - D3-IOPR
  - D3-CSPP
  - D3-MFA
last_threat_review: "2026-09-18"
---

# Healthcare Sector Cybersecurity (mid-2026)

## Threat Context (mid-2026)

Healthcare has been the most targeted sector for ransomware for three consecutive years, and that ranking has not changed entering mid-2026:

- **Change Healthcare (Optum / UnitedHealth Group), Feb 2024** — ALPHV/BlackCat ransomware via a Citrix portal lacking MFA; pharmacy claims processing across the US disrupted for weeks; reported PHI exposure of approximately one-third of the US population; settlements and HHS-OCR enforcement still active in 2026.
- **Ascension Health, May 2024** — Black Basta intrusion via a clinician downloading a malicious file; 140 hospitals impacted; EHR downtime forced paper-record fallback for weeks.
- **NHS Synnovis (UK), June 2024** — Qilin ransomware against the pathology provider serving Guy's, St Thomas', and King's College London hospitals; blood-test backlogs forced multiple critical-incident declarations across south London; ICO and NHS England investigations open into 2026.
- **Kaiser Permanente, April 2024** — partial PHI exposure via third-party tracking pixels (Meta, Google) — a non-ransomware breach class that nevertheless triggered HHS-OCR Bulletin enforcement on online tracking technologies.

**AI-driven clinical decision support is mainstream by mid-2026.** Radiology triage (Aidoc, Viz.ai, Annalise.ai), pathology image classification (Paige, PathAI, Ibex), ED triage copilots (Epic + Microsoft, Oracle Cerner + Anthropic via vendor integrations), and ambient clinical-documentation tools (Abridge, Nuance DAX Copilot, Suki, DeepScribe) are deployed at scale. FDA's AI/ML-enabled medical-device list crossed 1,000 cleared devices in late 2024 and continues compounding.

**PHI in LLM context windows is the new exfiltration channel.** Clinicians paste de-identification-failed patient notes into ChatGPT / Claude / Gemini consumer tiers for differential-diagnosis assistance, drug-interaction lookup, or letter drafting. Shadow-AI usage in clinical workflows is well-documented (multiple 2024–2025 hospital surveys reporting 20–50% of clinicians admitting some PHI exposure to consumer LLMs). The HIPAA Privacy Rule treats this as an unauthorised disclosure; the HHS-OCR Dec 2023 Bulletin on online tracking technologies sets the enforcement tone for non-traditional disclosure channels.

**EU AI Act high-risk classification took binding effect for high-risk AI systems on 2 Aug 2026** for systems placed on the market post that date (transitional rules for pre-existing systems extend further). Annex III, item 5(a) and Annex I (covered medical-device AI under MDR/IVDR) place the bulk of clinical-decision-support AI in the high-risk category — requiring conformity assessment, risk-management system, data-governance, technical documentation, transparency, human oversight, accuracy/robustness/cybersecurity, and post-market monitoring obligations.

**FDA AI/ML SaMD guidance + Predetermined Change Control Plans (PCCP).** FDA finalized its PCCP guidance in Dec 2024, allowing pre-authorized modifications to AI/ML-enabled device software without resubmitting a 510(k) for each retrain — provided the PCCP is part of the original authorization. This reshapes the medical-device-update model from "freeze on clearance" to "evolve within an authorized envelope."

**Medical device cybersecurity is now an FDA pre-market requirement.** Since FDORA section 524B took effect in March 2023, FDA has a Refuse-to-Accept authority for cyber devices lacking SBOM, vulnerability-management plan, secure-by-design evidence, and post-market patching commitments. CISA-FDA joint advisories on medical-device CVEs have continued through 2024-2026 (Medtronic insulin pumps, MicroPort cardiac, Baxter Welch Allyn, BD Alaris, Illumina sequencer firmware, several Medtronic CareLink remote-monitoring CVEs).

**EU MDR + IVDR cybersecurity** is governed by MDCG 2019-16 Rev.1 (July 2020) and MDCG 2022-11 plus the ENISA medical-device threat-landscape work; notified bodies are increasingly demanding evidence of cybersecurity risk management as part of conformity assessment, but the 2017 MDR Annex I General Safety and Performance Requirement 17.2 (cybersecurity) language predates the AI-augmented-device threat class.

---

## Framework Lag Declaration

| Framework | Control | Designed For | Fails Because |
|---|---|---|---|
| HIPAA Security Rule §164.312 (technical safeguards) | Access control, audit controls, integrity, person/entity authentication, transmission security | US covered entities and business associates; ePHI at rest and in transit | Last substantively updated 2003 (with minor adjustments since). 2024 NPRM ("HIPAA Security Rule To Strengthen the Cybersecurity of ePHI") proposes MFA, encryption baseline, network segmentation, vulnerability scanning, but is still under review entering mid-2026 — not yet binding. §164.312(a)(1) "Access Control" does not mention prompt injection as an access-control bypass; does not name LLM context windows as a disclosure surface; "minimum necessary" cannot be enforced against a clinician copy-pasting a full chart into ChatGPT. |
| HIPAA Privacy Rule §164.502(b) (minimum necessary) | Limit PHI uses and disclosures to the minimum necessary | US covered entities | Predates LLM-mediated workflows. HHS-OCR Dec 2023 Bulletin on online tracking pixels extends Privacy Rule reasoning to non-traditional channels but is sub-regulatory; consumer-LLM PHI disclosure is not formally addressed except as an unauthorised disclosure. |
| HIPAA Breach Notification Rule §164.400–414 | Notification timing for breaches (60 days HHS + individuals; 60 days media for breaches >500 individuals; state AGs per state law) | US-side breach response | 60-day clock assumes a discrete breach event; LLM-mediated leakage is continuous and aggregate. The "low probability of compromise" risk-assessment exception is being abused for consumer-AI prompt leakage. |
| HITRUST CSF v11.4 (2024) | Mapped, certifiable framework consolidating HIPAA, HITECH, NIST CSF, ISO 27001, GDPR, PCI DSS, NIST 800-53, CMS, CIS Controls plus AI Risk Management v1 | Healthcare-tilted but multi-industry; certifiable to e1 / i1 / r2 tiers | Voluntary. r2 certification is the meaningful tier; e1/i1 are baseline. HITRUST CSF v11.4 integrated AI risk-management controls (NIST AI RMF mapping, ISO/IEC 42001 alignment) but field adoption is uneven — most r2 reports issued in 2026 still draw from v11.2/v11.3 controls without the AI overlay. |
| HL7 FHIR R5 (2023) + R6 ballot | Healthcare data exchange API (REST/JSON) | EHR-to-EHR, EHR-to-app, payer-provider data exchange | Security is implementation-defined. SMART on FHIR + OAuth 2.0 + OpenID Connect is the de facto auth pattern but HL7 FHIR R5 does not mandate it. FHIR Bulk Data Access ($export) is a documented exfiltration channel where authorization scopes are over-broad. CARIN BB / Da Vinci profiles add semantics but not security. |
| FDA AI/ML SaMD guidance (PCCP final Dec 2024; AI/ML-Enabled Device Software Functions guidance final Jan 2025; Cybersecurity in Medical Devices guidance final Sept 2023 with refresh-cycle) | AI/ML-enabled medical-device software | US pre-market and post-market device review | Principle-based: secure product development framework (SPDF), threat modelling, SBOM, vulnerability management, post-market plan. Does not specifically address AI supply-chain compromise (training-data poisoning, model-weight tampering, dependency confusion in MLOps). PCCP authorizes retrain within envelope but the envelope's security boundary is not standardized. |
| EU MDR 2017/745 Annex I §17.2 + MDCG 2019-16 Rev.1 + MDCG 2022-11 | Cybersecurity requirements for medical devices placed on EU market | EU notified-body conformity assessment | Annex I 17.2 language is general ("state of the art" cybersecurity). MDCG guidance is non-binding but operationally treated as binding. AI-specific cybersecurity for medical devices under MDR is bridged to EU AI Act high-risk obligations from Aug 2026 onward — operators have to satisfy both regimes, often with duplicative-but-non-identical evidence. |
| EU AI Act (Reg. 2024/1689) Annex III + Annex I high-risk classification | Risk-management, data governance, technical documentation, transparency, human oversight, accuracy/robustness/cybersecurity, post-market monitoring for high-risk AI | EU-placed-on-market AI systems | High-risk obligations binding from 2 Aug 2026 onward. Article 15 (accuracy, robustness, cybersecurity) requires "appropriate level" with no concrete healthcare-AI threshold. Article 14 human-oversight obligations conflict in practice with ambient-documentation tools where the entire value proposition is reduced clinician attention. |
| GDPR Article 9 (special category data — health) + Article 35 DPIA | Lawful basis for processing health data; mandatory DPIA for high-risk processing | EU/EEA data subjects | Health-data DPIA scope rarely covers LLM-mediated workflows in practice; SCC + adequacy + Article 28 processor terms with US LLM providers remain operationally fragile (DPF challenges, Schrems-derived case law). |
| UK NHS DSPT (Data Security and Protection Toolkit) v6 | Annual self-assessment for NHS England organizations and suppliers | NHS provider trusts and connected suppliers | Self-assessment with audit sampling; lags actual practice. DSPT v6 added some AI-readiness questions in 2025 but does not bound generative-AI prompt-leakage explicitly. |
| AU My Health Records Act 2012 + Healthcare Identifiers Act 2010 + AESCSF for healthcare extension + Privacy Act 1988 (APP 11 + Notifiable Data Breaches scheme) | My Health Record system + AU-wide privacy | AU CIs and healthcare providers | OAIC notifiable-breach scheme triggers on eligible data breach; My Health Records Act has stricter penalties but narrow scope (the MyHR itself, not the wider provider environment). |
| JP APPI special-care-required personal information ("yō-hairyō kojin jōhō") | Sensitive personal information including medical history | JP entities | Consent requirements stronger; ISMS in healthcare is mostly ISMAP-adjacent + sector METI/MHLW guidance. AI-mediated processing of medical data is being scoped under the JP AI Strategy 2024 but not yet codified. |
| IL Patient Rights Law 5756-1996 + INCD healthcare directives + Privacy Protection Law 5741-1981 | Patient confidentiality + national cyber regulator directives | IL healthcare providers | INCD has issued healthcare-specific cyber directives but they remain advisory; binding force varies by HMO/hospital governance. |
| SG HCSA (Healthcare Services Act 2020, in force progressively 2022-2024) + PDPA + MOH Cybersecurity Guidelines for Healthcare | Healthcare licensing + data protection + sector cyber | SG licensed healthcare providers | HCSA cyber requirements are operational baseline; LLM-mediated PHI not specifically scoped. |
| IN DPDPA 2023 + DISHA (Digital Information Security in Healthcare Act, drafted, not yet enacted) + NDHM / ABDM | National data protection + pending healthcare-specific bill + national digital health mission | IN entities processing personal data including health | DPDPA treats health data as a sensitive category by implication but DISHA's separate sectoral protection remains pending into 2026. ABDM API ecosystem has its own consent-manager architecture but uptake-by-providers is uneven. |
| SA NHIA + POPIA (Protection of Personal Information Act 2013) | National Health Insurance + cross-sector privacy | SA healthcare entities | NHIA implementation phasing slow; POPIA Information Regulator enforcement maturing. |
| BR LGPD sensitive personal data + ANS cybersecurity guidance + CFM telemedicine resolutions | LGPD treats health data as sensitive | BR healthcare and health-insurance entities | ANPD guidance on AI + LGPD released 2024; healthcare-AI specifics still maturing. |
| UAE Federal Law No. 2 of 2019 on Use of ICT in Healthcare + Federal Decree-Law No. 45 of 2021 (PDPL) + DHA / DOH sector rules | Healthcare data residency + privacy + emirate-level sector rules | UAE-licensed healthcare providers | Data-residency obligations are operationally binding; cross-border LLM use cases run directly into these. |
| ISO 27001:2022 + ISO/IEC 27799 (health-sector ISMS) + ISO 81001-5-1 (medical-device cybersecurity lifecycle) + ISO/IEC 42001 (AI management system) | Generic ISMS + health sector + medical-device cyber lifecycle + AIMS | Organisation-level | A.8.30 outsourced development control needs explicit AI-pipeline interpretation. ISO 81001-5-1 is the strongest medical-device cybersecurity lifecycle standard available but adoption among smaller device vendors is partial. |
| NIST 800-53 Rev 5 + NIST 800-66 Rev 2 (HIPAA implementation guidance) + NIST AI RMF 1.0 + NIST GenAI Profile (NIST-AI-600-1) | US federal + HIPAA mapping + voluntary AI risk | US covered entities can opt-in for stronger baseline | AC-2 account management does not specifically address shared clinician credentials, break-glass accounts, or AI-service-principals for clinical copilots — extension required. |

**Cross-jurisdiction posture (global-first, not US-centric):** Any healthcare gap analysis for a multi-jurisdiction operator must explicitly enumerate the regulator and primary instrument for: US (HHS-OCR, FDA), EU (each Member State DPA + ENISA + notified bodies + Commission for AI Act), UK (ICO + NHS England + MHRA), AU (OAIC + Department of Health + TGA), JP (PPC + MHLW + PMDA), IL (PPA + INCD + MoH), SG (PDPC + MOH), IN (DPB + MoHFW + CDSCO), SA (Information Regulator + SAHPRA), BR (ANPD + ANVISA + ANS), UAE (UAE Data Office + DHA / DOH / MOHAP), alongside ISO 27001:2022 + ISO/IEC 27799 + ISO 81001-5-1 + ISO/IEC 42001. US-only (HIPAA, FDA) is insufficient for any multinational provider, payer, device vendor, or digital-health platform.

---

## TTP Mapping

| Surface | TTP | Matrix | Variant in mid-2026 | Gap Flag |
|---|---|---|---|---|
| Clinician credential phishing for EHR / VPN / Citrix access | T1078 — Valid Accounts | ATT&CK Enterprise | Targeted phishing of physicians and nurses using lookalike Epic / Cerner / Workday portals; MFA-fatigue against Duo/Microsoft Authenticator; SIM-swap on on-call physician phones | HIPAA §164.312(d) person/entity authentication does not specify AAL; many CEs accept SMS-OTP MFA — fails NIST 800-63B AAL2 phishing-resistance bar. Hand off to identity-assurance. |
| Bulk EHR / FHIR / data-warehouse exfiltration | T1530 — Data from Cloud Storage Object | ATT&CK Enterprise | FHIR `$export` Bulk Data over-broad scopes; cloud data warehouse (Snowflake / BigQuery / Redshift) credential theft from clinician laptop; AWS S3 misconfiguration on de-identification staging buckets | HIPAA §164.312(c) integrity controls do not address bulk-API exfil semantics; HITRUST CSF 09.l information-transfer-policies treats bulk data flow at a policy layer. CWE-200 (Information Exposure), CWE-862 (Missing Authorization). |
| PHI exfiltration via clinician prompt to consumer LLM | T1567 — Exfiltration Over Web Service | ATT&CK Enterprise | Clinician pastes patient note into ChatGPT / Claude / Gemini for differential diagnosis or letter drafting; ambient-doc tool retains and forwards transcript to vendor cloud outside BAA | No HIPAA control specifically names this channel; HHS-OCR Bulletin reasoning applies. Hand off to dlp-gap-analysis. CWE-200 (Information Exposure). |
| Prompt injection of clinical decision-support copilot | AML.T0051 — LLM Prompt Injection (with .000/.001/.002 sub-techniques) | ATLAS v2026.09 | Indirect prompt injection via referenced lab report PDF, OCR'd intake form, or patient-portal message that exploits an EHR-integrated copilot; instruction to suppress allergy alert, reorder medications, or fabricate trend in vital signs | EU AI Act Art 15 cybersecurity obligation applies but lacks concrete healthcare-AI threshold; HIPAA silent on prompt-injection-as-disclosure-vector. CWE-1426 (Improper Validation of Generative AI Output). |
| Model extraction / membership inference against clinical AI | AML.T0013, Discover AI Model Ontology (inference-API probing for system-prompt, guardrail, training-data signal); AML.T0017, Develop Capabilities (adversarial-ML weaponization) | ATLAS v2026.09 | Adversarial probing of a clinical-decision-support API to determine whether specific patient records were in training set; reconstruction of de-identified training examples from inference behaviour | EU AI Act Art 10 data-governance applies to training-data quality; does not codify membership-inference defence. CWE-1426 covers output-validation gap. |
| Medical-device firmware tamper / exploit | T1190 (IT-side initial access to device-network) chained with vendor-specific device CVEs | ATT&CK Enterprise + ICS where applicable | Insulin pumps, cardiac monitors, infusion pumps (BD Alaris), sequencers (Illumina firmware), patient-monitoring (BD, Philips, GE Healthcare), bedside imaging | FDA 524B PMA/510(k) cyber obligations only apply to devices submitted after March 2023; brownfield fleet pre-dates it. EU MDR Annex I 17.2 silent on AI-augmented devices. Hand off to ot-ics-security for device-network treatment, and coordinated-vuln-disclosure for vendor reporting. |
| FHIR / SMART on FHIR session token theft | T1078 chained with T1530 | ATT&CK Enterprise | Stolen JWT / OAuth2 bearer for SMART-on-FHIR launch; over-broad scopes (`*/*.read`, `patient/*.read`); refresh-token theft persists access; CWE-287 (improper authentication) and CWE-862 (missing authorization) | RFC-7519 JWT validation must enforce `iss`, `aud`, `exp`, signature algorithm, key rotation; RFC-9421 HTTP message signatures for FHIR API integrity in flight; HL7 FHIR R5 does not mandate either. |
| EHR over-privileged break-glass / shared-account access | T1078.002 — Valid Accounts: Domain Accounts | ATT&CK Enterprise | Shared "Nurse" account on med-cart Windows; break-glass clinician account auditing gap; service account for EHR-integrated copilot with patient/* scope rather than encounter-bound | HIPAA §164.312(a)(2)(i) unique user identification is met technically by user-account-per-clinician but break-glass and AI-service-principals are commonly outside that boundary. NIST 800-53 AC-2 account management does not codify AI-service-principal scoping. |

**Note on ATLAS coverage.** AML.T0051 (Prompt Injection) covers the direct, indirect, and jailbreak sub-techniques against clinical-decision-support copilots; AML.T0054 (LLM Jailbreak) covers guardrail-bypass crafting; AML.T0013 (Discover AI Model Ontology) covers adversary reconnaissance of the deployed model — system-prompt extraction, guardrail mapping, training-data signal probing — relevant to clinical-AI confidentiality; AML.T0017 (Develop Capabilities) covers the broader adversarial-ML weaponization pipeline.

---

## Exploit Availability Matrix

| Surface / CVE Class | CVSS | RWEP | CISA KEV | PoC Public | AI-Discovered | Active Exploitation | Patch Available | Live-Patchable | Sector-Aware Detection |
|---|---|---|---|---|---|---|---|---|---|
| Hospital-network ransomware delivery (Citrix, VPN, MFA-fatigue chain) | varies (CVE-2023-3519 Citrix, CVE-2024-1709 ConnectWise, etc.) | high | Multiple KEV entries 2023-2026 | Yes — many with Metasploit modules | Mixed — some classes AI-assisted in 2025 | Confirmed; weekly cadence in 2024-2026 across US, UK, EU, AU healthcare | Yes for in-support products; brownfield is exposed | Mostly no (vendor product patching is reboot-class) | EDR with healthcare-specific carve-outs; SOC visibility into EHR-host hardening typically partial |
| PHI on dark web | n/a | risk-modelled | n/a | n/a — leaked data, not exploit | n/a | Continuous; price per record moderate ($50-$1000 depending on completeness) | n/a | n/a | DLP and dark-web monitoring; hand off to dlp-gap-analysis |
| Medical-device exploits (Medtronic, BD, Philips, GE Healthcare, Illumina, Baxter) | varies | varies | Several KEV listings 2024-2026 | Mixed — vendor disclosure with optional researcher PoC | Increasingly AI-assisted reverse-engineering of device firmware | Targeted (nation-state interest in remote-monitoring and DNA-sequencing) | Vendor-dependent — patch lag often 90-180 days; deploy lag 6-24 months due to clinical-engineering change windows | No — firmware updates require clinical-engineering change windows | ICS-aware IDS where deployed; rare in hospital networks. Hand off to ot-ics-security for device-network treatment. |
| Clinical-AI prompt injection (no CVE-class yet for clinical specifically) | n/a | risk-modelled | n/a | Demonstrated in 2024-2025 research against EHR-integrated copilots (Epic + GPT-4 series, Cerner + various) | n/a (vector is AI conduit) | Suspected in 2025 advanced campaigns against ambient-doc and triage copilots | Mitigation only — design-time controls on AI integration | n/a | Requires LLM-aware telemetry — almost never present in healthcare today |
| FHIR / SMART JWT token theft / replay | varies (CVE-2024-X for various SMART-on-FHIR libraries) | medium-high | Few KEV | Yes for several library-level vulns | n/a | Confirmed in 2024-2025 against patient-app marketplaces | Yes per library | Yes (library hot-swap) | API-gateway telemetry where deployed; many EHR vendors deploy proprietary token-introspection without standardized log schema |
| EHR / patient-portal credential stuffing | n/a | high | n/a | n/a (credential reuse, not CVE) | n/a | Continuous | n/a | n/a | Bot-management and account-takeover detection if deployed; HHS-OCR has flagged inadequate protection as risk-analysis failure |

**Honest gap statement (catalog coverage is not exhaustive).** This project's `data/cve-catalog.json` does not contain an exhaustive inventory of medical-device CVEs (Medtronic, BD, Philips, GE Healthcare, Illumina, Baxter, Welch Allyn, MicroPort, Abbott). The authoritative source is CISA's ICS Medical Advisory feed (https://www.cisa.gov/news-events/cybersecurity-advisories/ics-medical-advisories) and FDA's medical-device safety communications. Captured in `forward_watch` for inclusion in the next data refresh. Do not invent CVE IDs to fill this matrix.

---

## Analysis Procedure

This procedure threads the three foundational design principles — defense in depth, least privilege, zero trust — through every step.

**Defense in depth.** Layer controls across: clinician identity (D3-MFA at phishing-resistant AAL2/AAL3), EHR application (RBAC + minimum-necessary enforcement + break-glass audit), API perimeter (FHIR gateway with JWT validation per RFC-7519 + HTTP message signatures per RFC-9421 where supported), data layer (encryption at rest, field-level encryption for sensitive PHI fields, tokenization for analytics), egress (DLP at LLM boundary D3-IOPR + sanctioned-AI-only egress policy D3-CSPP), endpoint (EDR + browser-isolation on clinician workstations where clipboard-paste-to-LLM is a documented vector), medical-device network (segmentation à la `ot-ics-security`), backups (immutable + air-gap + tested restore).

**Least privilege.** Clinician access enforces the HIPAA "minimum necessary" standard at technical level, not just policy. EHR roles scoped to encounter, department, and time window — not blanket patient/*. AI clinical tools get scoped contexts: ambient-documentation tools get the current encounter only, not the full chart; triage copilots get triage-relevant fields only; differential-diagnosis copilots run against de-identified or tokenized inputs with re-identification at the human-in-the-loop boundary. SMART-on-FHIR scopes restricted to encounter-bound rather than patient-wide where the use case permits. Break-glass accounts heavily audited; AI-service-principals treated as distinct identities with their own AC-2 lifecycle and audit trail.

**Zero trust.** Every EHR query verified through identity-bound session and policy-decision-point, not assumed trustworthy because the device is on the hospital LAN. Medical device-to-EHR / device-to-historian communications mutually authenticated (mTLS with device-provisioned certificates) — not bare TCP on a flat VLAN. AI clinical-tool prompts and completions logged with identity binding (which clinician, which encounter, which patient context, full prompt + completion, model identifier and version, retrieval-augmented sources). Federated authentication (SAML/OIDC) consumes attributes from a single source of truth — preventing the EHR from being its own identity silo.

### Step 1 — HIPAA Security Rule risk analysis per §164.308(a)(1)(ii)(A)

- Is there a current risk analysis (dated within the last 12 months)? Note: HHS-OCR enforcement actions repeatedly cite "outdated or inadequate risk analysis" as the proximate finding — Anthem, Premera, Excellus, NewYork-Presbyterian, Memorial Hermann.
- Does the risk analysis cover the entire ePHI environment — including AI clinical tools, ambient-documentation vendors, third-party developers, and BA subcontractors?
- Does it cover newer threat classes — LLM prompt-leakage, prompt-injection of clinical copilots, FHIR Bulk Data over-scoped exports, medical-device CVEs?

### Step 2 — HITRUST inheritance and scoping (if applicable)

- Is the entity pursuing HITRUST e1, i1, or r2? r2 is the meaningful certification for healthcare.
- What CSF version? v11.4 (2024) is current; v11.5 expected.
- Which AI-overlay controls from CSF v11.4 are in scope? (NIST AI RMF mapping, ISO/IEC 42001 alignment.)
- Inheritance posture: are cloud/EHR vendor (Epic Hosted, Oracle Cerner-as-a-Service, Microsoft Azure for healthcare, AWS HealthLake, Google Cloud Healthcare API) HITRUST certifications inherited via cross-mapping? Document the inherited control IDs and the residual control responsibility.

### Step 3 — Medical-device inventory and MDS2 mapping

- Produce a clinical-engineering inventory: manufacturer, model, firmware, network connectivity, clinical use, criticality.
- Cross-reference with MDS2 forms (Manufacturer Disclosure Statement for Medical Device Security) on file. MDS2 is the de-facto standard (HIMSS / IHE / NEMA) for pre-procurement cybersecurity disclosure.
- For devices subject to FDA section 524B (submitted post March 2023), confirm SBOM available, vulnerability-management plan documented, post-market patching commitment in place.
- For EU MDR / IVDR devices, confirm cybersecurity conformity-assessment evidence: MDCG 2019-16 Rev.1 elements, ISO 81001-5-1 lifecycle evidence where adopted, and EU AI Act high-risk overlap where the device is AI/ML-enabled.
- Hand off to `ot-ics-security` for device-network segmentation treatment; hand off to `coordinated-vuln-disclosure` for vendor advisory handling.

### Step 4 — AI clinical-tool inventory and EU AI Act tier classification

For each AI clinical tool in production or pilot, enumerate:

- Vendor + model + version + deployment topology (vendor SaaS, hyperscaler-hosted, on-prem).
- Clinical use case: triage, diagnostic, decision-support, ambient-documentation, drug-interaction, prior-auth, scheduling, patient-facing chat.
- EU AI Act classification: high-risk (Annex III item 5(a) or Annex I via MDR/IVDR), limited-risk (transparency obligations), minimal-risk.
- FDA classification: AI/ML-enabled SaMD or not; PCCP in place or not.
- BAA / data-processing agreement covering PHI flow into the tool.
- Prompt and completion logging: enabled? retention? identity-binding? accessible for HIPAA audit?
- Human-in-the-loop gate for write actions (order entry, alarm suppression, dosing changes, clinical-note finalization).
- Training-data provenance: was patient data from this entity in training? what de-identification / consent posture?

### Step 5 — PHI-in-LLM channel inventory (hand off to `dlp-gap-analysis`)

- Enumerate every channel where PHI could reach an LLM: sanctioned vendor integration, sanctioned employee-facing copilot (e.g., Microsoft 365 Copilot, Google Workspace Duet/Gemini), shadow-AI via clinician browser, ambient-documentation pilots, patient-facing chat.
- For each sanctioned channel, document the BAA / DPA, the data-flow boundary, the DLP coverage (D3-IOPR at egress), the logging.
- For shadow-AI, document the detection coverage (browser-isolation logging, SWG / SASE telemetry, EDR clipboard-monitoring) and the policy enforcement (web-filter category, conditional-access, awareness training).
- Hand off to `dlp-gap-analysis` for full DLP control mapping.

### Step 6 — FHIR / SMART-on-FHIR API security audit

- Inventory FHIR endpoints (production, staging, partner-facing).
- For each, audit OAuth 2.0 / OpenID Connect configuration: token lifetime, refresh-token rotation, scope granularity, audience binding, JWT signature algorithm (no `none`, no `HS256` with publicly-known key).
- Audit SMART-on-FHIR launch context — is the encounter binding enforced server-side, or only client-asserted?
- FHIR Bulk Data `$export` operation: which clients are authorized? what scopes? what export size limits? what asynchronous-job authorization-revocation handling?
- Validate per RFC-7519 (JWT) — `iss`, `aud`, `exp`, signature, key rotation. Where supported, validate per RFC-9421 (HTTP Message Signatures) for API integrity.

### Step 7 — Identity assurance for clinicians and AI service principals (hand off to `identity-assurance`)

- Clinician auth at AAL2 minimum; AAL3 for privileged access (EHR admin, identity admin, security admin).
- Phishing-resistant factors (FIDO2 / WebAuthn / passkey) required, not just permitted; SMS-OTP retired.
- Break-glass account: distinct identity, time-boxed, alarmed, post-use review.
- AI-service-principals (Epic-to-GPT, Cerner-to-Anthropic, Snowflake-to-LLM, etc.) treated as distinct identities with workload-identity federation where supported; per-encounter scoped tokens, not long-lived service-account keys.

### Step 8 — Breach-notification readiness

- HIPAA Breach Notification Rule: 60 days HHS for breaches >500 individuals, 60 days individual notification, 60 days media for breaches >500 in a state, plus state AGs per state law (CA, NY, MA, TX, IL among the stricter regimes; many states have shorter clocks than HIPAA — 30 to 45 days).
- EU GDPR Article 33: 72 hours to supervisory authority for personal-data breaches.
- UK ICO: 72 hours under UK GDPR.
- AU OAIC: as soon as practicable under the Notifiable Data Breaches scheme.
- Pre-position breach-counsel relationships, draft notification templates, and exercise the multi-jurisdiction notification matrix in tabletops.

### Step 9 — Business Associate Agreement / processor agreement review

- Inventory every BA and sub-BA (cloud vendors, ambient-doc vendors, transcription, ML platform, FHIR aggregator, analytics, dark-web monitoring).
- For each, verify BAA executed, scope of PHI flow documented, sub-BA chain documented, breach-notification timing in BAA matches HIPAA + state requirements.
- For AI vendors specifically: verify training-data use restrictions (does the vendor use PHI to train base models? to fine-tune customer models? does opt-out actually disable training?), model-output retention, vendor's own subprocessors.
- EU-side: SCC + adequacy + Article 28 processor terms; verify data-residency posture.

### Step 10 — AI vendor risk assessment for clinical-decision tools

- For each AI clinical tool, score:
  - Regulatory: FDA AI/ML SaMD clearance status (510(k), De Novo, PMA, enforcement-discretion); EU AI Act high-risk conformity assessment status (CE under MDR + AI Act overlap); MDR notified-body involvement.
  - Cybersecurity: SBOM available; vulnerability-management plan; secure development lifecycle (ISO 81001-5-1 / NIST SSDF aligned); supply-chain attestation (SLSA / in-toto / Sigstore — hand off to `supply-chain-integrity`).
  - AI-specific: training-data governance and provenance; red-team report on prompt-injection and jailbreak resistance (hand off to `ai-attack-surface`); model-card; eval suite for clinical accuracy / robustness / fairness across demographic strata.
  - Operational: incident-response interface; breach-notification interface; logging API; ability to deliver per-customer audit log; ability to revoke specific encounters / tenants on demand.

### Step 11 — Compliance Theater Check (see dedicated section below for concrete tests)

### Step 12 — Cross-jurisdiction output reconciliation

For each jurisdiction the operator is exposed to (US, EU, UK, AU, JP, IL, SG, IN, SA, BR, UAE), produce a single mapping of the same control findings to that jurisdiction's regulatory language. Disparate findings for the same control deficiency across jurisdictions are themselves a finding.

---

## Output Format

The skill produces a Healthcare Sector Security Posture Assessment covering HIPAA Security Rule + 2025 NPRM coverage, HITRUST control maturity, NIS2 essential-entity obligations (where applicable), FDA pre/post-market cybersecurity for medical devices, and ambient-AI documentation-pilot risk. The shape below is consumed downstream by `incident-response-playbook` (for HIPAA Breach Notification timing), by `compliance-theater` (HITRUST-vs-deployed-control comparison), and by `global-grc` (for cross-jurisdictional healthcare rollup). Preserve the per-control HIPAA / HITRUST rows verbatim — they are the auditable evidence for breach-notification timing.

Produce this structure verbatim:

```
## Healthcare Sector Security Posture Assessment

**Assessment Date:** YYYY-MM-DD
**Entity:** [name] (covered entity / business associate / device vendor / digital-health platform)
**Scope:** [e.g., EHR + ambient-doc pilots + 3 device families; HMO national; payer + provider arms]
**Regulatory jurisdictions:** [US HHS-OCR + FDA, EU AI Act + MDR, UK ICO + MHRA, ...]

### HIPAA Technical-Safeguard Scorecard
| §164.312 Control | Implementation | Adequacy vs current TTPs | Theater Risk |
|------------------|----------------|--------------------------|--------------|
| (a)(1) Access control | ... | ... | ... |
| (a)(2)(i) Unique user identification | ... | ... | ... |
| (a)(2)(ii) Emergency access (break-glass) | ... | ... | ... |
| (a)(2)(iii) Automatic logoff | ... | ... | ... |
| (a)(2)(iv) Encryption / decryption | ... | ... | ... |
| (b) Audit controls | ... | ... | ... |
| (c)(1) Integrity | ... | ... | ... |
| (d) Person or entity authentication | ... | ... | ... |
| (e)(1) Transmission security | ... | ... | ... |

### HIPAA Risk Analysis Currency
[Date of last analysis; scope; AI clinical tools and PHI-in-LLM channels covered yes/no; identified deficiencies; remediation plan status]

### HITRUST Inheritance Matrix (if applicable)
| HITRUST Control Ref | Inherited From | Residual Responsibility | Evidence |

### Medical-Device Inventory with MDS2 / FDA 524B / MDR Mapping
| Manufacturer | Model | Firmware | Clinical Use | MDS2 On File | SBOM | 524B-In-Scope | MDR/AI Act Tier | Network Position |

### AI Clinical-Tool Inventory with EU AI Act + FDA SaMD Tier
| Vendor | Model | Use Case | EU AI Act Tier | FDA SaMD Status | PCCP | BAA | Prompt/Completion Logging | Human-in-Loop Write Gate |

### PHI-in-LLM Channel Inventory
| Channel | Sanctioned? | BAA | DLP Coverage (D3-IOPR) | Egress Policy (D3-CSPP) | Logging | Retention |

### FHIR / SMART-on-FHIR Security Audit
| Endpoint | OAuth Config | Token Lifetime | Scope Granularity | JWT Validation (RFC-7519) | Bulk $export Controls |

### Identity Assurance Snapshot
| Population | AAL | Factors | Phishing-Resistant | Break-Glass Posture |

### Breach-Notification Readiness Scorecard
| Jurisdiction | Notification Clock | Counsel Pre-Positioned | Templates Drafted | Last Tabletop Date |

### Business Associate / Processor Posture
| BA | Sub-BAs | BAA Executed | Training-Use Restrictions | Data-Residency |

### Compliance Theater Findings
[Outcome of the four tests in the Compliance Theater Check section]

### Defensive Countermeasure Plan (D3FEND)
[D3-IOPR, D3-CSPP, D3-MFA — concrete control placements by layer]

### Priority Remediation Actions
1. ...
2. ...
3. ...

### RWEP-Prioritised CVE Exposure
[Hospital-network + medical-device + FHIR-library CVEs ranked by RWEP, not CVSS; see `exploit-scoring` skill for recalculation]
```

---

## Compliance Theater Check

Run all four tests. Any "fail" is a theater finding documented with the evidence (or absence thereof).

**Theater Test 1 — HIPAA risk analysis currency.**
Ask: "Show me the HIPAA Security Rule risk analysis dated within the last 12 months, and identify within it the treatment of AI clinical tools and PHI-in-LLM channels."

- If the most recent risk analysis is older than 24 months: §164.308(a)(1)(ii)(A) compliance is theater; HHS-OCR enforcement history shows this is the most frequently cited finding.
- If the analysis exists but does not address AI clinical tools, ambient-documentation vendors, or LLM channels: the analysis covers a network that no longer exists.
- Acceptable: analysis dated within 12 months, AI clinical tools enumerated and scored, PHI-in-LLM channels identified with treatment status, remediation tracker live and current.

**Theater Test 2 — Medical-device MDS2 coverage.**
Ask: "What percentage of medical devices in the environment have MDS2 forms on file, and what percentage of post-March-2023 procurements have FDA section 524B evidence (SBOM, vuln-management plan, post-market patching)?"

- If the answer is "we don't track that" or coverage is below 80%: regulatory device-cyber compliance posture is theater.
- If MDS2s exist but are uncorrelated with the clinical-engineering CMMS / asset inventory: the forms are not operationally used — theater.
- Acceptable: ≥80% MDS2 coverage of in-service devices, 100% MDS2 + 524B evidence for post-March-2023 procurements, clinical-engineering CMMS cross-referenced quarterly with cybersecurity vulnerability tracking.

**Theater Test 3 — PHI-in-LLM disclosure governance.**
Ask: "Show me the PHI flow into each LLM tool in use across the workforce, the BA agreement covering each, and the technical controls preventing unsanctioned LLM use from clinician workstations."

- If the answer is "we have a policy that staff cannot use ChatGPT for PHI": that is policy, not control — theater unless enforced.
- If the answer is "doctors just use ChatGPT for second opinions and we don't have a BAA": active HIPAA Privacy Rule exposure plus Security Rule §164.308(a)(5) workforce-training failure.
- Acceptable: sanctioned AI tools enumerated with BAAs; egress-policy at SWG / SASE blocks consumer-LLM domains from clinical workstations or routes through DLP-inspected proxy; browser-isolation or clipboard-DLP on workstations where complete egress block is operationally infeasible; awareness training tied to acceptable-use policy with documented attestation per workforce member.

**Theater Test 4 — Ransomware tabletop currency.**
Ask: "What's the most recent ransomware tabletop exercise outcome, including the decision tree for clinical-operations continuity (paper downtime, ED diversion, OR scheduling), the notification matrix across HHS-OCR + state AGs + EU/UK regulators where applicable, and the lessons-learned tracker?"

- If no tabletop in the last 12 months: incident-response capability is theater regardless of what the IR plan document says.
- If a tabletop happened but did not include clinical-operations decision-makers (CMO, CNO, ED chief, OR director): the exercise covered IT incident response, not healthcare-operations incident response — partial theater.
- If the lessons-learned tracker from the last tabletop has zero closed items 90+ days later: the exercise is documentation theater.
- Acceptable: tabletop within last 12 months, included clinical leadership, lessons-learned tracker live and being closed.

---

## Defensive Countermeasure Mapping

Maps healthcare-sector offensive findings to MITRE D3FEND IDs from `data/d3fend-catalog.json`, with explicit defense-in-depth layer position, least-privilege scope, zero-trust posture, and AI-pipeline applicability.

| D3FEND ID | Technique | Healthcare Layer Position | Least-Privilege Scope | Zero-Trust Posture | AI-Pipeline Applicability |
|---|---|---|---|---|---|
| D3-IOPR | I/O Prompt Inspection (PHI inspection at the LLM boundary) | Egress proxy / DLP inline with the sanctioned AI-tool data path; browser-isolation / clipboard-DLP on clinician workstations for unsanctioned channels | Per-clinician identity binding; per-encounter context scope; per-tool BAA-coverage validation | Default-deny; every prompt inspected and policy-evaluated before reaching the model endpoint, every completion inspected before reaching the clinician | Required for sanctioned AI integration. For ephemeral / serverless clinical-AI tool architectures, the prompt-inspection point shifts to the API-gateway sidecar — never recommend host-agent-only DLP for ephemeral AI workloads. |
| D3-CSPP | Client-Server Payload Profiling (EHR / FHIR API payload profiling for exfil detection) | At FHIR API gateway, EHR application reverse-proxy, cloud-data-warehouse egress; sampling and signature on bulk-export operations | Per-API-client identity, per-scope, per-resource-type; flag deviations from baseline access pattern | Continuous verification of API-call conformance with declared scope; deviations alert and optionally throttle | Required at every AI-service-principal egress from the EHR — distinguishes legitimate AI workload reads from exfiltration patterns. For serverless AI architectures the profiling point is the API-gateway, not the ephemeral compute. |
| D3-MFA | Multi-Factor Authentication (clinician auth at AAL2+ minimum; AAL3 for privileged access) | Identity provider (Azure AD / Entra, Okta, PingFederate, ForgeRock) federating SAML/OIDC to EHR, FHIR app marketplace, VPN, Citrix, jump hosts | Per-clinician identity; step-up for privileged roles; phishing-resistant factors required, not optional | Every session re-verified at risk-signal change; no standing trust; break-glass identities distinct and alarmed | Applicable to AI-service-principals via workload-identity federation rather than human MFA; for ephemeral AI workloads use short-lived workload-identity tokens (OIDC workload federation, SPIFFE/SPIRE) rather than long-lived service-account keys. |

**Ephemeral and AI-pipeline applicability statement.** Recommendations in this skill are explicit about where the host-agent control assumption fails. Cloud-hosted clinical-AI tools and serverless ambient-documentation pipelines are by definition ephemeral; host-agent DLP and host-EDR controls do not apply. The compensating-control surface is the API-gateway / egress-proxy boundary, plus the workload-identity layer, plus immutable audit logging delivered to a SIEM under the covered entity's control rather than the vendor's. For brownfield deployments on traditional hospital infrastructure, host-agent controls do apply and should be the primary control plane — recommendations must specify which architectural mode the control is being placed in.

---

## Hand-Off / Related Skills

After producing the healthcare sector posture assessment, chain into the following skills.

- **`dlp-gap-analysis`** — for the PHI-in-LLM channel inventory (Step 5). Full DLP control coverage at the LLM egress boundary, clipboard-paste detection, browser-isolation deployment decisions, and sanctioned-AI-only egress policy enforcement live in this skill.
- **`identity-assurance`** — for clinician auth (AAL2/AAL3, phishing-resistant factors), break-glass account governance, and AI-service-principal scoping. The HIPAA §164.312(d) gap of unspecified AAL is closed here.
- **`ot-ics-security`** — medical devices are the healthcare-sector parallel to OT/ICS. The Purdue-style segmentation, signed-firmware enforcement, vendor remote-access ledger, and long-lifecycle compensating-control programme all apply to clinical-engineering fleets.
- **`ai-attack-surface`** — for clinical-AI prompt-injection threat modelling (AML.T0051) and adversarial-ML capability assessment (AML.T0017) against decision-support copilots, triage copilots, and ambient-documentation tools.
- **`coordinated-vuln-disclosure`** — for medical-device vulnerability reporting per FDA's 21 CFR 803/806 + CISA ICS-CERT pathway, plus EU MDR vigilance reporting. CVD on medical devices is operationally distinct from generic enterprise CVD.
- **`compliance-theater`** — extends the four tests above with general-purpose theater detection on the entity's wider GRC posture (HITRUST audit vs actual control evidence; HHS-OCR resolution-agreement currency; multi-jurisdiction reconciliation).
- **`framework-gap-analysis`** — for multi-jurisdiction reconciliation in Step 12 (US + EU + UK + AU + JP + IL + SG + IN + SA + BR + UAE).
- **`global-grc`** — alongside framework-gap-analysis when EU AI Act + MDR + GDPR, UK ICO + MHRA, AU OAIC + TGA, JP PPC + PMDA, and equivalent regulators apply simultaneously.
- **`mcp-agent-trust`** — when clinical copilots are MCP-server-backed (Epic, Cerner, and third-party connector ecosystems are increasingly MCP-fronted); tool-use governance on copilots with write access to orders / alarms / dosing.
- **`supply-chain-integrity`** — for AI-vendor SBOM, SLSA provenance, Sigstore/in-toto verification on training pipelines and model artefacts. The clinical-AI supply chain is one of the least-controlled surfaces in current healthcare deployments.
- **`policy-exception-gen`** — to generate defensible exceptions for brownfield medical devices where corporate IT SLAs are architecturally infeasible (pre-March-2023 device fleet); the exception evidence is the documented compensating-control programme (segmentation, allowlisting, ICS-IDS monitoring, change-window patching).
- **`exploit-scoring`** — to recalculate RWEP for hospital-network, medical-device, and FHIR-library CVEs — particularly KEV-listed Citrix / VPN / fileshare exposures with active healthcare exploitation campaigns.

**Forward watch (per skill-format spec).** HIPAA Security Rule modernization NPRM (2024) — track to final rule; HHS-OCR Bulletin on AI / LLM disclosures in clinical workflows — emerging guidance; FDA AI/ML SaMD action plan iterations and PCCP guidance refinements; EU AI Act high-risk implementing acts and harmonised standards (CEN/CENELEC JTC 21); EU MDR + AI Act conformity-assessment alignment guidance (MDCG); ISO/IEC 42001 + ISO 81001-5-1 + ISO/IEC 27799 revision cycles; HITRUST CSF v11.5 / v12 with expanded AI controls; HL7 FHIR R6 ballot security profile improvements; CISA ICS-Medical Advisory feed for medical-device CVE inclusion in `data/cve-catalog.json`; UK MHRA AI airlock pilot outcomes and post-pilot regulatory framework; AU TGA SaMD essential-principles update; SG MOH cybersecurity guidelines for healthcare refresh; IN DISHA enactment progress; BR ANPD healthcare-AI guidance.
