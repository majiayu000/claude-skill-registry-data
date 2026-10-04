---
name: global-grc
version: "1.0.0"
description: Multi-jurisdiction GRC mapping — EU (GDPR/NIS2/DORA/EU AI Act/CRA), UK, AU, SG, JP, IN, CA, ISO 27001:2022, CSA CCM v4
triggers:
  - global grc
  - international compliance
  - gdpr security
  - nis2
  - dora compliance
  - eu ai act
  - cyber resilience act
  - mas trm
  - cert-in
  - essential 8
  - apra cps 234
  - multi-jurisdiction
  - global compliance
data_deps:
  - atlas-ttps.json
  - d3fend-catalog.json
  - exploit-availability.json
  - framework-control-gaps.json
  - global-frameworks.json
atlas_refs: []
attack_refs: []
framework_gaps: []
d3fend_refs:
  - D3-EAL
  - D3-EFA
  - D3-FAPA
  - D3-FE
  - D3-IOPR
  - D3-KBPI
  - D3-MENCR
  - D3-MFA
  - D3-NI
  - D3-NTA
  - D3-OTF
  - D3-SCA
  - D3-CSPP
last_threat_review: "2026-09-09"
---

# Global GRC Assessment

This skill provides multi-jurisdiction GRC analysis. It maps current security threats against frameworks from 14 jurisdictions and two global standards bodies, identifies universal control gaps that no jurisdiction's framework covers, and surfaces jurisdiction-specific notification and compliance requirements.

## Frontmatter Scope

The `atlas_refs` and `attack_refs` arrays are intentionally empty. This skill is a jurisdiction/framework registry and gap-correlation layer — its subject is regulatory coverage, not a native set of attacker techniques. The TTPs referenced in the body come from the domain skills whose threats each framework is measured against; that downstream skill carries the authoritative technique attachment.

---

## Framework Registry (mid-2026 currency)

### European Union

#### GDPR — General Data Protection Regulation (2016/679)

**Relevant Articles:**
- **Art. 32** — Security of processing: "Appropriate technical and organisational measures" including: pseudonymisation/encryption, ongoing confidentiality/integrity/availability/resilience, ability to restore availability after incidents, regular testing/assessing/evaluating.
- **Art. 33** — Breach notification to supervisory authority within 72 hours
- **Art. 34** — Communication to data subjects when breach likely to result in high risk

**What "appropriate measures" means in 2026 context:**
Art. 32 is intentionally technology-neutral. For 2026 threat reality, DPAs (particularly EDPB, CNIL, BfDI, ICO) have signaled:
- Post-quantum cryptography migration planning is an "appropriate measure" given the quantum threat horizon
- AI processing of personal data requires specific security measures (no settled guidance yet — EU AI Act supplements)
- Prompt injection in AI systems processing personal data is an Art. 32 security concern (if successful, it is an unauthorized disclosure)

**Breach notification:** 72 hours from awareness to supervisory authority. Note: this is faster than many US frameworks. An AI-mediated data breach (prompt injection exfiltrating personal data) must be reported even if the AI service account was the "authorized" accessor.

**Currency assessment:** GDPR Art. 32 is reasonably current because "appropriate measures" evolves with technology. The gap is in interpretive guidance — there is no settled EDPB guidance on AI-specific security measures, MCP trust, or prompt injection as an Art. 32 failure.

---

#### NIS2 Directive (2022/2555) — Effective October 2024

**Classification:** Essential entities (energy, transport, banking, health, digital infrastructure) and Important entities (postal, waste, chemicals, food, manufacturing, digital providers, research).

**Key requirements (Art. 21):**
1. Risk analysis and information system security policies
2. Incident handling
3. Business continuity and crisis management
4. Supply chain security (including security in supplier/provider relationships)
5. Security in network/information systems acquisition, development, maintenance
6. Policies/procedures for assessing vulnerability handling measures
7. Cybersecurity hygiene and training
8. Policies on cryptography and, where appropriate, encryption
9. Human resources security, access control, asset management
10. Multi-factor authentication or continuous authentication

**Incident notification:** Significant incidents to national CSIRT within 24 hours (early warning), 72 hours (notification), 1 month (final report).

**Key gaps for 2026 threats:**
- Art. 21(2)(e) covers supply chain security but has no specific guidance for AI/MCP supply chain attacks
- Art. 21(2)(h) mentions "policies on cryptography and encryption" — post-quantum migration is implied but not mandated
- No specific Art. 21 measure for AI pipeline integrity, prompt injection, or AI-as-C2
- "Appropriate measures" language parallels GDPR — same gap in AI-specific interpretation

**Enforcement:** National competent authorities can impose fines up to €10M or 2% of global turnover for essential entities; €7M or 1.4% for important entities.

---

#### DORA — Digital Operational Resilience Act (2022/2554) — Effective January 2025

**Scope:** Financial entities (banks, investment firms, payment institutions, e-money, insurance, crypto-asset service providers) and their critical ICT third-party service providers.

**Five pillars:**
1. ICT risk management framework (Arts. 5–16)
2. ICT incident classification and reporting (Arts. 17–23)
3. Digital operational resilience testing (Arts. 24–27, including TLPT — Threat-Led Penetration Testing)
4. ICT third-party risk management (Arts. 28–44)
5. Information and intelligence sharing (Arts. 45–49)

**Key requirements relevant to 2026:**
- Art. 8: Identification of ICT risk — must include AI/ML systems as ICT assets
- Art. 9: Protection and prevention — encryption "in accordance with latest standards," access policies, monitoring
- Art. 16: Simplified ICT risk management framework for smaller entities
- Art. 26: TLPT (red team testing for significant institutions) — must use threat intelligence, should cover AI attack surfaces
- Art. 28: Third-party ICT risk — critical third-party providers (CTPs) are subject to direct oversight. LLM API providers may qualify as CTPs for financial entities heavily dependent on them.

**DORA gaps for 2026:**
- No specific AI/LLM risk category in ICT risk taxonomy
- TLPT scope guidance doesn't explicitly include prompt injection or AI-as-C2
- CTP designation process for AI/LLM providers is still being clarified by ESAs

---

#### EU AI Act (2024/1689, amended by Regulation (EU) 2026/1744) — staged application through 2028

**Application timeline** (Art. 113 as amended by the Digital Omnibus on AI, in force 2026-07-27):
- 2025-02-02 — Chapters I–II: prohibitions (Art. 5) and AI literacy
- 2025-08-02 — GPAI model obligations (Chapter V), governance, penalties regime
- 2026-08-02 — general application date: Art. 50 transparency obligations bind, and the Commission / AI Office holds supervision and enforcement powers over GPAI model providers
- 2026-12-02 — new Art. 5(1)(ba)/(bb) prohibitions; Art. 50(2) compliance deadline for systems placed on the market before 2026-08-02
- **2027-12-02 — Chapter III Sections 1–3 (high-risk requirements, including Art. 9 risk management and Art. 15 cybersecurity) for Annex III / Art. 6(2) systems**
- **2028-08-02 — Chapter III Sections 1–3 for Annex I / Art. 6(1) product-embedded systems**

The high-risk obligations below are therefore 16 months (Annex III) to 24 months (Annex I) away. Do not scope remediation against an August 2026 high-risk deadline — and do not read the deferral as a withdrawal, because the attack surface those obligations address is live now.

**Risk tiers for AI systems:**
- **Unacceptable risk** (Art. 5): Prohibited (social scoring, real-time remote biometric identification in publicly accessible spaces for law enforcement, etc.). Two prohibitions added by Regulation (EU) 2026/1744 apply from 2026-12-02: Art. 5(1)(ba), AI systems generating or manipulating non-consensual intimate imagery of an identifiable person; Art. 5(1)(bb), AI systems generating or manipulating child sexual abuse material within the meaning of Directive 2011/93/EU. Unlike the Chapter III deferral these are near-term, and they carry Art. 99 penalties.
- **High risk** (Annex III): Critical infrastructure, biometric, employment, education, law enforcement, etc.
- **Limited risk** (Art. 50): Transparency obligations (chatbots must disclose they're AI)
- **Minimal risk**: No specific requirements

**For high-risk AI systems, Art. 9 Risk Management System requires:**
- Continuous iterative risk management process
- Identification and analysis of known/foreseeable risks
- Estimation and evaluation of risks in conditions of intended use
- Evaluation of risks from reasonably foreseeable misuse
- Risk management measures

**What "misuse" means for AI systems in 2026:**
Art. 9 requires identifying reasonably foreseeable misuse. For any high-risk AI system with a language model component, "reasonably foreseeable misuse" includes prompt injection — it is the most documented AI attack pattern in 2026. An Art. 9 risk management system that doesn't address prompt injection is incomplete.

**Interaction with NIS2:** High-risk AI systems operated by NIS2 entities must satisfy both frameworks. The intersection is not fully harmonized — no implementing regulation bridges Art. 9 AI Act risk management and NIS2 Art. 21 measures specifically for AI systems.

---

#### EU Cyber Resilience Act — CRA (2024)

**Scope:** Products with digital elements (hardware and software) placed on EU market.

**Key security requirements (Annex I):**
- No known exploitable vulnerabilities
- Secure by default configuration
- Confidentiality, integrity, and availability protections
- Limited attack surface
- Security updates for the support lifetime

**Manufacturer reporting obligations (Art. 14) — apply from 2026-09-11:**
- Actively exploited vulnerabilities and severe incidents affecting the security of a product with digital elements must be reported: **24-hour** early warning, **72-hour** full notification, final report within **14 days** of a corrective measure becoming available (actively exploited vulnerability) or **one month** (severe incident).
- Filed once through the CRA Single Reporting Platform to the CSIRT of the manufacturer's main establishment; ENISA receives it simultaneously.
- The statutory trigger is *actively exploited* — Art. 14(1) covers a vulnerability the manufacturer becomes aware of being actively exploited in its product. Test it against `active_exploitation: confirmed` for a version of the product the manufacturer actually ships, not against proof-of-concept availability. A public PoC is exploit *capability*, not exploitation, and does not start the clock; KEV listing is strong evidence of active exploitation but is scoped to CISA's own affected-product determination, so it still needs applicability confirmed against the manufacturer's shipped versions. The catalog tracks `poc_available`, `cisa_kev` and `active_exploitation` as separate fields precisely because collapsing them here would tell a manufacturer a statutory clock is running when it is not. The Annex I product requirements themselves apply from 2027-12-11.

**CRA relevance to 2026 threats:**
- MCP servers distributed as software products fall under CRA if sold to EU market
- "No known exploitable vulnerabilities" requirement means MCP servers must have a coordinated disclosure and patch process
- AI model components integrated into products are covered — model updates constitute "security patches" under CRA
- CRA will be the primary enforcement mechanism for AI tool supply chain security in the EU

---

### United Kingdom

#### Cyber Essentials / Cyber Essentials Plus

**Five controls:**
1. Firewalls (boundary firewalls and internet gateways)
2. Secure configuration
3. User access control
4. Malware protection
5. Patch management (high-risk patches within 14 days)

**Currency assessment for 2026:**
- 14-day patch window is better than NIST's 30-day but still insufficient for CISA KEV class (Copy Fail class should be 4 hours)
- No control for AI/ML attack surface, prompt injection, MCP trust
- Malware protection assumes signature-based or behavioral detection — no coverage for AI-generated evasion (PROMPTFLUX)
- Widely used as a baseline for UK government supplier requirements — creates systematic gap for AI-using suppliers

#### NCSC Cyber Assessment Framework (CAF)

**Four objectives, 14 principles:**
- A: Managing security risk (A1: Governance, A2: Risk Management, A3: Asset Management, A4: Supply Chain)
- B: Protecting against cyberattack (B1–B6 covering identity/access, data security, system security, resilient networks, staff awareness, vulnerability management)
- C: Detecting cyber security events (C1: Security Monitoring, C2: Proactive Security Event Discovery)
- D: Minimising impact (D1: Response/Recovery Planning, D2: Lessons Learned)

**CAF strength vs. 2026:** CAF Principle B6 (Vulnerability Management) and C1 (Security Monitoring) are principle-based, allowing more flexibility than control-based frameworks. An assessor applying CAF B6 can reasonably require CISA KEV-aligned response times. CAF C1 can be interpreted to require AI API behavioral monitoring.

**CAF currency (v4.0):** v4.0 is the current version and closed part of this gap. NCSC added a section on developing and maintaining software used in essential services securely, and improved AI-risk coverage across the framework. Principle B4 System Security now carries assessable automated-decision-making outcomes: B4.a requires designed restrictions preventing actions by automated decision-making technologies that could adversely affect the systems supporting an essential function, and B4.b requires their operation to be well understood and their decisions replicable. B4 cites ETSI *Securing Artificial Intelligence (SAI): Baseline Cyber Security Requirements for AI Models and Systems* as an external resource.

**Residual CAF gap:** the outcomes are framed around "automated decision-making technologies", not around LLM-specific attack surfaces. No contributing outcome names prompt injection, MCP/agent tool trust boundaries, RAG pipeline integrity, or AI-as-C2, and the principle-based approach still leaves currency of interpretation to the individual assessor.

#### Cyber Security and Resilience (Network and Information Systems) Bill — not yet in force

Introduced to the House of Commons on 2025-11-12; through Lords stages during July 2026, with no Royal Assent as of 2026-08-05. It reforms the Network and Information Systems Regulations 2018 and is the UK's answer to the NIS2 divergence created at EU exit. Commencement is phased — some measures on or shortly after Royal Assent, others by secondary legislation.

**Scoping consequence today:** a UK-regulated entity's obligations still flow from NIS 2018 plus sector regulators applying CAF v4.0. Do not model NIS2-equivalent duties into a UK gap analysis until commencement. Watch for the Royal Assent date, the commencement regulations, and whether the resulting incident-reporting clocks displace UK GDPR's 72h as the binding UK timeline.

---

### Australia

#### ASD Information Security Manual (ISM) — Monthly Updates

The Australian ISM is the most frequently updated major framework — monthly updates give it the shortest lag of any national framework. Key controls relevant to 2026:

- **ISM-1876 and ISM-1877**: Patch online services and the operating systems of internet-facing servers and network devices within 48 hours of release when the vendor rates a vulnerability critical or a working exploit exists, at every Essential Eight maturity level. Browsers, office suites, email clients and workstation operating systems get 48 hours only at Maturity Level Three (ISM-1692, ISM-1696).
- **ISM-0843**: Implement application control on workstations (ISM-1490 extends it to internet-facing servers from Maturity Level Two).
- **ISM-1488**: Block Microsoft Office macros in files that originate from the internet (relevant for AI document processing pipelines).

**ISM strength:** 48-hour patching for exploited vulnerabilities is the best standard practice in any national framework. It applies to internet-facing systems at every Essential Eight maturity level, and to workstations at Maturity Level Three.

**ISM gap:** No specific controls for AI pipeline security, MCP trust boundaries, or prompt injection as of mid-2026 monthly updates.

#### ASD Essential 8

**Eight mitigations, Maturity Levels 0–3:**
1. Application control
2. Patch applications
3. Configure Microsoft Office macros
4. User application hardening
5. Restrict administrative privileges
6. Patch operating systems (ML3: within 48h of exploit availability)
7. Multi-factor authentication
8. Regular backups

**ML3 patch requirement (48 hours with exploit availability)** is the most operationally realistic framework requirement for CISA KEV class vulnerabilities. Still does not explicitly require live kernel patching as a capability.

**Essential 8 gap:** No AI-specific mitigations. Essential 8 was designed for Windows-centric enterprise environments; doesn't address Linux LPEs, AI assistant supply chain, or prompt injection.

#### APRA CPS 234 — Financial Sector

Requires financial entities to maintain information security capabilities commensurate with information security vulnerabilities and threats. Annual third-party penetration testing. Incident notification to APRA within 72 hours for material incidents.

**CPS 234 + AI:** No specific guidance for AI/ML systems. "Commensurate with threats" requires current threat awareness — a CPS 234-compliant entity should be assessing AI attack surfaces as part of threat landscape monitoring.

#### SOCI Act — Enhanced Critical Infrastructure Risk Management Program Rules 2026

The Security of Critical Infrastructure Legislation Amendment (Enhanced Critical Infrastructure Risk Management Program) Rules 2026 (F2026L00701) were registered 2026-06-09, amending the CIRMP Rules (LIN 23/006) 2023. Enhanced CIRMP obligations apply to nine critical asset classes (broadcasting, DNS, electricity, energy market operators, freight infrastructure, freight services, gas, liquid fuel, water).

**What is new:** s.10A requires a documented system or process for mapping the supply chain covering major suppliers and critical components — the most specific supply-chain-mapping obligation in this registry. s.8A(2)(b) makes unmitigated legacy, unsupported or obsolete technology an addressed hazard. s.9A addresses personnel hazards and access management.

**Gap:** the instrument does not name artificial intelligence, machine learning, model providers or agent tooling. Australia therefore has a mandatory supplier-mapping obligation an assessor can reasonably extend to AI plugins and MCP servers, but no text requiring it.

---

### Singapore

#### MAS Technology Risk Management Guidelines (TRM, Jan 2021 — updated)

**Scope:** MAS-regulated financial institutions.

**Key requirements:**
- Technology risk governance framework
- IT system resilience (RTO/RPO requirements)
- Cyber surveillance (continuous monitoring)
- Penetration testing (frequency based on risk classification)
- Patch management (critical patches within 1 month — same PCI-era problem)
- Third-party technology risk

**MAS TRM + AI:** MAS published AI governance guidelines separately (Fairness, Ethics, Accountability, Transparency framework). Integration between TRM and AI governance is incomplete — no specific TRM controls for AI attack surfaces. Financial institutions in Singapore are expected to apply TRM principles to AI systems but specific control requirements are not yet codified.

**MAS TRM gap:** 1-month critical patch window; no AI-specific controls; no MCP/agent trust boundary requirements.

#### CSA Cybersecurity Code of Practice (CCoP) — Critical Information Infrastructure

Requirements for 11 CII sectors (energy, water, banking, healthcare, transport, government, InfoComm, media, security & emergency, aviation, maritime).

**Key requirements:** Annual cybersecurity audit, annual penetration testing, incident reporting within 2 hours of confirmed incident, patch management within 14 days for critical systems.

**CCoP strength:** 2-hour incident reporting for CII is the fastest notification requirement in any framework.

---

### Japan

#### METI Cybersecurity Framework / NISC Basic Policy

Japan's national cybersecurity framework closely mirrors NIST CSF with adaptations for Japanese industry structure. NISC (National center of Incident readiness and Strategy for Cybersecurity) publishes the Basic Policy updated annually.

**Key gaps for 2026:** Japanese frameworks lag US equivalents by 12–18 months in AI-specific guidance. The METI AI Governance Guidelines (2023) address AI ethics and governance but not AI attack surfaces. No equivalent to EU AI Act security requirements in Japanese law as of mid-2026.

**Active cyber defence legislation (2025):** the Act on Prevention of Damage Caused by Unauthorised Acts against Critical Electronic Computers (Act No. 42 of 2025) and its implementing Act (No. 43 of 2025) passed the Diet on 2025-05-16 and were promulgated on 2025-05-23; commencement is phased by cabinet order. Relevant for understanding Japan's cyber posture, government access to communications information, and critical-infrastructure incident-response coordination — not a control framework in itself.

**APPI amendment (promulgated 2026-07-17):** the Act partially amending the Act on the Protection of Personal Information passed the Diet on 2026-07-10 and was promulgated on 2026-07-17, commencing on a date set by cabinet order within two years; implementing ordinances and guidelines are pending. Headline changes: PPC power to impose surcharges where unlawful handling produced financial gain, an expanded suspension-of-use right covering personal information containing biometric data, and relaxed consent rules for third-party provision for statistical purposes. Nothing in it addresses AI attack surfaces — Japan's AI-security gap is unchanged — but the enforcement ceiling for a personal-data leak moves from guidance-and-order to monetary penalty once the commencement order is made.

---

### India

#### CERT-In Directions (April 2022)

**Breach notification:** 6 hours from awareness — the shortest breach notification requirement globally.

**Other requirements:**
- Maintain logs of ICT systems for 180 days within India jurisdiction
- VPN service providers must maintain subscriber information for 5 years
- Data center operators, virtual asset service providers: same logging requirements
- Mandatory reporting of 20+ incident types including: targeted scanning/probing, compromise of critical systems, unauthorized access, data breach, attacks on applications, defacement

**CERT-In + AI:** No specific AI security requirements. The 6-hour notification requirement applies if an AI system breach results in a reportable incident (unauthorized access, data breach). An AI-mediated exfiltration via prompt injection that affected Indian citizens' data would trigger 6-hour notification.

#### SEBI Cybersecurity and Cyber Resilience Framework

**Scope:** Market infrastructure institutions, regulated entities.

**Requirements:** Annual VAPT, quarterly vulnerability assessment, incident reporting within 6 hours to SEBI. Aligns with CERT-In timelines for financial sector.

---

### Canada

#### OSFI Guideline B-10 (Technology and Cyber Risk, 2023)

**Scope:** Federally regulated financial institutions.

**Key requirements:**
- Technology and cyber risk management framework
- Incident notification to OSFI within 24 hours of high/critical incidents
- Supply chain due diligence for technology third parties
- Annual penetration testing

**B-10 + AI:** No specific AI guidance as of mid-2026. "Technology risk" is interpreted broadly enough to include AI systems. OSFI published draft AI guidance for consultation in 2025 — final guidance expected late 2026.

#### Bill C-36 — Protecting Privacy and Consumer Data Act (proposed; supersedes the former Bill C-27 / CPPA)

Bill C-27 (44th Parliament) did not pass. The current federal privacy bill is C-36 (45-1), first reading 2026-06-15, at second reading in the House of Commons. Nothing in it is in force. PIPEDA remains the operative federal private-sector privacy statute, with breach notification to the OPC "as soon as feasible" where there is a real risk of significant harm. Verify penalty and notification figures against the C-36 text before relying on them — the former C-27 numbers ($25M or 5%, 72 hours) do not carry over automatically.

#### Critical Cyber Systems Protection Act (CCSPA) — enacted by Bill C-8, Royal Assent 2026-06-15

**Scope:** designated operators of the vital services and vital systems listed in Schedule 1, by operator class in Schedule 2 (regulators include the Minister of Industry, the Minister of Transport, OSFI, the Bank of Canada, the Canadian Nuclear Safety Commission and the Canadian Energy Regulator). Schedules and regulations are set by the Governor in Council.

**Key obligations:** establish and implement a cyber security programme; mitigate supply-chain and third-party product/service risks; report a cyber security incident affecting a critical cyber system to the Communications Security Establishment within a period prescribed by regulation, not to exceed 72 hours, then immediately notify the appropriate regulator and provide a copy; comply with cyber security directions.

**Status:** the CCSPA comes into force by order in council — obligations bind once proclaimed and the regulations and schedules are made.

**CCSPA + AI:** no AI-specific requirement. The supply-chain provision is product/service-generic and does not name AI tooling, model providers or MCP servers.

---

### Global Standards

#### ISO 27001:2022 / ISO 27002:2022

**Reorganized control set:** 93 controls in 4 clauses (Organizational, People, Physical, Technological). Reduced from ISO 27001:2013's 114 controls.

**New in 2022:**
- A.5.7: Threat intelligence (explicit requirement to collect and analyze threat intelligence)
- A.5.23: Information security for use of cloud services
- A.8.8: Management of technical vulnerabilities
- A.8.12: Data leakage prevention
- A.8.16: Monitoring activities

**ISO 27001:2022 gap for 2026:**
- A.5.7 threat intelligence: requires collecting and analyzing threat intel but no guidance on currency requirements — an org can comply with A.5.7 using threat intelligence that is years out of date
- A.8.16 monitoring: no guidance for AI API behavioral monitoring, no AI-as-C2 detection requirement
- No controls specific to AI/ML systems (planned for ISO/IEC 27090, still in development)
- A.8.8 same problem as NIST SI-2: "appropriate timescales" undefined for CISA KEV class

#### CSA Cloud Controls Matrix (CCM) v4

**17 domains, 207 control specifications (CCM v4.1, released 2026-01-27, superseding v4.0.x).** Cloud-specific but applicable to any cloud-native or cloud-using organization. v4.1 adds net-new controls in domains including Logging and Monitoring and Security Incident Management; the AI control surface remains in the separate AI Controls Matrix rather than in CCM core.

**AI relevance:**
- AIS domain (Application & Interface Security) covers some AI risk areas
- SEF (Security Incident Management): breach notification requirements
- STA (Supply Chain Management): cloud service supply chain security

**CCM v4 gap:** No AIS controls specifically for LLM/AI systems, MCP servers, or prompt injection. CSA published "AI Controls" supplement (2025) — worth reviewing alongside CCM v4 for AI-using organizations.

#### CIS Controls v8

**18 controls, three Implementation Groups (IG1/IG2/IG3):**

Controls most relevant to 2026 gaps:
- Control 7 (Continuous Vulnerability Management): IG2/IG3 — automated patching. Doesn't specify CISA KEV-based timelines.
- Control 14 (Security Awareness): IG1+. AI-generated phishing is not in scope for current training content guidance.
- Control 16 (Application Software Security): IG2+. Does not cover AI/LLM application security.
- Control 17 (Incident Response Management): IG1+. No AI-specific playbooks recommended.

**CIS Control v8 strength:** Control 7 IG3 requires continuous vulnerability management with asset tracking — more operationally rigorous than NIST SI-2's "timely" language.

---

## Universal Gaps (No Jurisdiction Covers These)

These gaps exist across all 14 jurisdictions and both global standards:

| Gap | Evidence |
|---|---|
| Prompt injection as access control failure | Zero frameworks have a control for this attack class |
| MCP/agent tool trust boundaries | Zero frameworks address AI tool supply chain at this level |
| AI pipeline integrity (model versioning + behavioral regression) | Zero frameworks have technical control requirements |
| AI-as-C2 detection | Zero frameworks have detection/response requirements |
| Live kernel patching as required capability | Only ASD ISM approaches this (48h with exploit); still doesn't mandate live patching |
| CISA KEV-indexed patch SLAs | Closest: ASD ML3 48h, CCoP 14d. None mandate sub-4h for KEV + public PoC |
| AI-generated phishing detection update requirement | Zero frameworks require updating phishing detection for AI-generated content |
| RAG pipeline security | Zero frameworks have controls |
| Post-quantum cryptography migration mandate | NIST/CISA guidance recommends; no framework mandates timeline |

---

## Defensive Countermeasure Mapping

D3FEND references from `data/d3fend-catalog.json`. This skill produces jurisdictional gap findings, not control prescriptions — its subject is which regulator requires what, and the answer for every row in the Universal Gaps table above is "none". A gap that no framework mandates still has a defensive technique that closes it; the mapping below routes each universal gap to that technique and to the downstream skill that owns the implementation guidance. Operators converting a gap into a remediation plan consume the cited downstream skill rather than reading the D3FEND ID in isolation, because that skill carries the AI-pipeline applicability notes, least-privilege scoping, and deployment posture.

| Universal gap | Offensive TTP class | D3FEND ID | Defensive technique | Owning downstream skill |
|---|---|---|---|---|
| Prompt injection as access-control failure | AML.T0051 (LLM Prompt Injection) | `D3-IOPR` + `D3-CSPP` | Input/Output Profiling + Client-server Payload Profiling | `ai-attack-surface` |
| MCP/agent tool trust boundaries | AML.T0010 (AI Supply Chain Compromise) | `D3-EAL` + `D3-EFA` | Executable Allowlisting + Executable File Analysis | `mcp-agent-trust` |
| AI pipeline integrity (model versioning + behavioural regression) | AML.T0018 (Manipulate AI Model), AML.T0020 (Training Data Poisoning) | `D3-FAPA` + `D3-EFA` | File Access Pattern Analysis + Executable File Analysis | `mlops-security` |
| AI-as-C2 detection | AML.T0096 (AI Service API, C2) | `D3-NTA` + `D3-OTF` | Network Traffic Analysis + Outbound Traffic Filtering | `ai-c2-detection` |
| Live kernel patching as required capability | T1068 (Exploitation for Privilege Escalation) | `D3-KBPI` + `D3-SCA` | Kernel-Based Process Isolation + System Call Analysis | `kernel-lpe-triage` |
| CISA KEV-indexed patch SLAs | T1190 (Exploit Public-Facing Application) | `D3-NI` | Network Isolation for the unpatched window | `exploit-scoring` + `kernel-lpe-triage` |
| AI-generated phishing detection update requirement | T1566 (Phishing), AML.T0016 (Obtain Capabilities) | `D3-MFA` + `D3-CSPP` | Multi-factor Authentication (passkey class) + Client-server Payload Profiling | `email-security-anti-phishing` |
| RAG pipeline security | AML.T0051, AML.T0020 | `D3-IOPR` + `D3-FAPA` | Input/Output Profiling + File Access Pattern Analysis | `rag-pipeline-security` |
| Post-quantum cryptography migration mandate | T1040 (Network Sniffing), T1557 (Adversary-in-the-Middle) — harvest-now-decrypt-later | `D3-MENCR` + `D3-FE` | Message Encryption (PQC-hybrid KEM) + File Encryption (PQC-wrapped envelope) | `pqc-first` |

**Defense-in-depth posture:** a jurisdictional gap finding from this skill closes only when the downstream skill's technique is deployed and tested — never when a policy document cites the regulation. Because no jurisdiction mandates any row above, there is no compliance-driven forcing function for these controls: an org that implements only what a regulator can cite will have none of them. That is the entire operational point of the Universal Gaps table, and the reason each row must carry a routing target.

**Least-privilege scope:** the downstream-skill citation is the boundary. This skill does not re-scope D3FEND techniques per principal class; that scoping is owned by the cited downstream skill's own Defensive Countermeasure Mapping section, which is authoritative for principal-class breakdowns (human operator ≠ agent identity ≠ MCP server ≠ model-serving process).

**Zero-trust posture:** jurisdiction is not a trust boundary. An entity established in a Member State that has not yet notified NIS2 transposition, or operating under a framework whose AI obligations are deferred to 2027–2028, faces the same attacker as one in the strictest jurisdiction. Scope controls to the threat, then map the jurisdictional obligation onto them — never the reverse, which produces a control set shaped by the weakest applicable regulator.

**AI-pipeline applicability:** every row whose TTP class is `AML.*` applies to AI workloads specifically and has no jurisdictional mandate anywhere in this registry until EU AI Act Art. 15 applies (2027-12-02 Annex III, 2028-08-02 Annex I). UK NCSC CAF v4.0 B4.a/B4.b is the only in-force obligation touching any of them, and only for automated decision-making — not for prompt injection, tool trust, RAG integrity, or AI-as-C2.

---

## Notification Timeline Summary

| Jurisdiction | Framework | Notification Trigger | Timeline |
|---|---|---|---|
| EU | GDPR | Personal data breach | 72h to SA |
| EU | NIS2 | Significant incident | 24h early warning, 72h notification |
| EU | DORA | Major ICT-related incident | 4h initial, 72h intermediate, 1 month final |
| EU | CRA (manufacturer reporting, from 2026-09-11) | Actively exploited vulnerability or severe incident in a product with digital elements | 24h early warning, 72h notification, 14 days final |
| UK | GDPR/UK DPA | Personal data breach | 72h to ICO |
| AU | Notifiable Data Breaches | Eligible data breach | ASAP (no fixed window), practicable |
| SG | PDPA | Data breach | 3 days to PDPC |
| SG | CSA CCoP (CII) | Cyber incident | 2 hours |
| JP | APPI | Personal data leak | Without delay |
| IN | CERT-In | 20+ incident types | **6 hours** |
| IN | SEBI | Cyber incident | 6 hours |
| CA | PIPEDA | Real risk of significant harm | Asap to OPC |
| CA | OSFI B-10 | High/critical tech/cyber incident | 24 hours |
| CA | CCSPA (Bill C-8) | Cyber security incident affecting a critical cyber system | ≤72h to CSE (period set by regulation), then immediate notice to the regulator — binds on order in council |
| Global | ISO 27001 | No notification requirement | Framework-only |

---

## Threat Context

US-only GRC posture is structurally incomplete for any organisation operating across EU, UK, AU, SG, IN, JP, or CA in mid-2026. The following regulatory instruments are in force or about to be, and have no direct US-framework equivalent:

- **NIS2 Directive (EU 2022/2555)** — transposition deadline 2024-10-17; transposition is still incomplete. The Commission issued reasoned opinions to 19 Member States on 2025-05-07 and on 2026-07-08 referred Ireland, Spain, France and the Netherlands to the CJEU for failing to notify transposing measures. Scope an entity by its Member State of establishment rather than by the directive text — obligations bite through national law, and in the referred Member States that law is not yet notified. Imposes obligations on essential and important entities that NIST CSF / SOC 2 do not mirror, including: 24-hour early-warning notification, mandatory MFA, supply-chain security including AI-tool plugins, board-level accountability with personal liability for senior management.
- **DORA (EU 2022/2554)** — fully applicable 2025-01-17. Imposes a 4-hour initial incident notification, mandatory Threat-Led Penetration Testing (TLPT) for significant financial entities, and direct ESA oversight of Critical Third-Party Providers (CTPs). LLM API providers used by EU financial entities are candidate CTPs.
- **EU AI Act (Regulation 2024/1689, amended by Regulation (EU) 2026/1744)** — staged application. The general application date passed on 2026-08-02: Art. 50 transparency obligations now bind and the Commission / AI Office now supervises GPAI model providers. The high-risk obligations — Art. 9 risk management, Art. 15 cybersecurity, post-market monitoring — were deferred by the Digital Omnibus on AI to 2027-12-02 for Annex III systems and 2028-08-02 for Annex I product-embedded systems. No NIST or SOC 2 control maps to Art. 15 cybersecurity requirements for AI systems, and the deferral widens that gap rather than closing it: no binding AI-cybersecurity obligation is in force in any jurisdiction until December 2027.
- **EU Cyber Resilience Act (Regulation 2024/2847)** — phased application; reporting obligations apply from 2026-09-11, full obligations from 2027-12-11. "Products with digital elements" placed on the EU market — including MCP servers, AI agent tooling, IoT — must satisfy Annex I essential cybersecurity requirements with vendor liability for the support lifetime.
- **CERT-In Directions (India, 2022)** — 6-hour breach notification, mandatory log retention in-jurisdiction. No US framework imposes a comparable timeline.
- **MAS TRM (Singapore)** and **CSA CCoP (Singapore CII)** — 1-hour critical-incident notification for CCoP CII, 14-day patch SLA. Stricter than any US framework.
- **APRA CPS 234 (Australia)** — third-party penetration testing mandate with personal accountability for boards; APRA enforcement actions in 2024–2025 demonstrate this is operationally enforced, not aspirational.

A US-only compliance posture in 2026 has no controls mapped to four of the most consequential regulatory developments of the past 24 months (NIS2, DORA, EU AI Act, CRA). Compliance theatre at the global level is the default state for orgs that have not run a jurisdiction-specific gap analysis since 2024.

---

## Framework Lag Declaration

Every applicable framework has at least one structural gap against mid-2026 threats. The lag is per-jurisdiction and per-control.

| Framework | Control | What it misses (mid-2026) |
|---|---|---|
| EU | GDPR Art. 32 ("appropriate technical and organisational measures") | Principle-based, intentionally technology-neutral. No mapped controls for prompt injection as an Art. 32 failure, no settled EDPB guidance on AI-system security, no PQC migration mandate. |
| EU | NIS2 Art. 21(2)(d) (supply chain) | Expanded scope to "supplier and provider relationships" but does not name AI tool plugins, MCP servers, or model providers. National-CSIRT enforcement timing varies — some Member States are still operationalising the 24h early-warning channel. |
| EU | DORA Art. 28–30 (ICT third-party risk) | Register of information for ICT third-party arrangements is mandated but there is no unified attestation regime yet; CTP designation for LLM/AI API providers is being clarified through ESA Joint Committee guidance. |
| EU | EU AI Act Art. 9 / Art. 15 (high-risk AI risk management and cybersecurity) | Transparency-obligation enforcement is left to Member-State competent authorities. As of mid-2026 the operational test of "appropriate level of accuracy, robustness, and cybersecurity" is being interpreted differently in DE, FR, IT, NL — uniform enforcement is not yet observed. |
| EU | EU CRA Annex I | "No known exploitable vulnerabilities" is a strict obligation but the conformity-assessment regime is new; market-surveillance authorities have limited tooling to test against ATLAS or KEV catalogs. |
| UK | NCSC CAF v4.0 Principles A–D | Principle-based, deliberately not prescriptive; currency of interpretation depends on the individual assessor. v4.0 added secure software development/maintenance coverage and automated-decision-making outcomes under B4.a/B4.b, plus an ETSI Securing AI reference — the first AI-relevant content in any UK regulatory assessment framework. Still no contributing outcome naming prompt injection, MCP/agent tool trust, RAG pipeline integrity, or AI-as-C2. |
| UK | Cyber Essentials Plus | 14-day high-risk patch SLA — better than NIST but still insufficient for KEV-class deterministic LPE. No AI-tool coverage. |
| AU | ASD ISM-1877 and ISM-1696 / Essential 8 | 48-hour patch window for known-exploit vulnerabilities is the best operational standard in any national framework — but does not mandate live-patching capability and has no AI-pipeline controls. |
| AU | APRA CPS 234 | "Commensurate with vulnerabilities and threats" — requires the regulated entity to keep its own threat catalog current. No CPS 234 controls mention AI surfaces explicitly. |
| SG | MAS TRM (2021, updates) | 1-month critical patch SLA still in force; AI governance handled in a parallel document (FEAT) with incomplete bridge to TRM technical controls. |
| IN | CERT-In Directions | 6-hour notification is fastest globally for the trigger set listed, but the trigger set predates the AI-mediated attack patterns now common — categorisation of an AI-mediated breach against the listed 20+ trigger types is interpretive. |
| JP | METI Cybersecurity / NISC Basic Policy | Lags US frameworks by 12–18 months on AI guidance. No equivalent to EU AI Act Art. 15 cybersecurity obligations for AI in Japanese law as of mid-2026. |
| Global | ISO 27001:2022 A.5.7 (Threat intelligence) | Requires intelligence collection; defines no currency metric — compliance achievable with stale intel. |
| Global | ISO 27001:2022 A.8.8 (Technical vulnerability management) | "Appropriate timescales" undefined — same SLA gap as NIST SI-2. |
| Global | CSA CCM v4 AIS / STA | AIS controls predate the LLM/MCP attack surface; STA covers supply chain but not AI-plugin trust boundaries. AI Controls supplement (2025) is not yet integrated into CCM v4 core. |
| US (for contrast) | NIST 800-53 SI-2, AC-2, SC-7 | 30-day patch window; no prompt-injection control; perimeter-centric SC-7 boundary protection misses AI-API egress. Cited here only to show parity with the global frameworks — US controls are not adequate either. |

Universal lag: every jurisdiction except Australia (ISM-1877 for internet-facing systems at every maturity level, ISM-1696 for workstations at Maturity Level Three) lacks an operationally testable patch-SLA for KEV-class deterministic LPE. Every jurisdiction lacks AI-pipeline-integrity controls in force as of mid-2026. The EU AI Act will be the first, but not until Art. 15 applies — 2027-12-02 for Annex III systems, 2028-08-02 for Annex I — following the Digital Omnibus deferral. The UK is marginally ahead in practice: NCSC CAF v4.0 B4.a/B4.b carry automated-decision-making outcomes a regulator can assess today, though they are not AI-pipeline-integrity controls in the full sense.

**Expanded jurisdictional coverage (per `data/global-frameworks.json`).** The EU/UK/AU/ISO baseline is no longer sufficient — the catalog tracks 21+ jurisdictions and the cross-border data-flow obligations are where most of the operational lag now lives:

- **China (PIPL Art. 38-42 / DSL / CSL):** Cross-border personal-information transfer requires one of three lawful bases — CAC Security Assessment (mandatory above thresholds), CAC-accredited Certification, or filed Standard Contract. PIPL enforcement against AI-tool prompt data is active (multi-vendor 2025 actions). No EU/UK control maps to the CAC Security Assessment trigger.
- **Vietnam (Cybersecurity Law 2018 + Decree 53/2022/ND-CP, effective 2022-10-01):** Data-localization for "important data" of Vietnamese citizens; in-country storage and a local representative office for foreign providers above defined-user thresholds. Decree 53 is the operational implementation that NIS2 and DORA have no parallel for.
- **Israel (Privacy Protection Law Amendment 13, in force 2024 with the Privacy Protection Authority expanded enforcement powers; INCD Cyber Defense Methodology v2.0):** Expanded sensitive-data definitions and adequacy-equivalent transfer expectations; INCD methodology pins technical baselines that complement (not duplicate) ISO 27001 A.5 controls.
- **Switzerland (revFADP in force 2023-09-01; FINMA Circular 2023/1 Operational risks and resilience – banks):** Transfer rules require recognised adequacy or contractual safeguards equivalent to GDPR Art. 46; FINMA imposes financial-sector operational-resilience expectations distinct from DORA's scope.
- **Hong Kong (PCPD PDPO + HKMA SA-2 / TM-G-1):** PCPD cross-border transfer guidance (Section 33 historically un-commenced, now operationalised via PCPD 2024 guidance); HKMA TM-G-1 / SA-2 imposes banking-sector cyber resilience timelines comparable to MAS TRM.
- **Taiwan (PDPA TW + Cyber Security Management Act 2018):** CSMA classifies CII operators with sector-specific reporting timelines; PDPA TW cross-border restrictions are agency-imposed per data category.
- **Indonesia (UU PDP 2022, in force 2024-10-17):** New personal-data law with 72-hour breach notification, data-protection officer requirements, and cross-border transfer adequacy or BCR-equivalent safeguards.
- **Japan (expanded — APPI / FISC / NISC):** APPI cross-border consent (Art. 28) and anonymized-information leak rules supplement the existing METI/NISC entry; FISC Security Guidelines impose financial-sector requirements analogous to FFIEC.
- **South Korea (PIPA + Network Act):** Cross-border PI transfer requires consent or one of the specified exceptions; PIPC enforcement against AI tools is active.
- **Brazil (LGPD Art. 33-35):** Cross-border transfer requires adequacy decision, SCCs, BCRs, or specific consent; ANPD has signalled AI-tool enforcement interest under LGPD Art. 33.
- **US sub-national — NYDFS 23 NYCRR 500 (amended Nov 2023, phased through Nov 2025):** 72-hour cyber-event notification to DFS, CISO accountability, MFA mandate, annual independent audit for Class A companies, Third-Party Service Provider Security Policy at 500.11. NYDFS is the strictest US sub-national financial-sector regime and operationally exceeds most state-level analogues.

The global-grc analysis must cross-walk against the full catalog above, not just EU/UK/AU/ISO — a global-first rollup covers every applicable jurisdiction, not a US-centric subset. A jurisdictional rollup that omits CN, VN, IL, CH, HK, TW, ID, JP-expanded, KR, BR, or NYDFS for an in-scope org is structurally incomplete.

---

## TTP Mapping

Regulatory frameworks are control-centric, not TTP-centric. This skill maps controls across jurisdictions; the TTP coverage of any one jurisdiction's controls is the union of mappings in `data/atlas-ttps.json` × `data/framework-control-gaps.json`. Use the **framework-gap-analysis** skill to score TTP coverage for a specific jurisdiction's control bundle; use this skill to compare obligations across jurisdictions.

A summary of the multi-jurisdiction control surface vs. the high-priority TTPs from `data/atlas-ttps.json`:

| TTP | ATLAS / ATT&CK ID | Jurisdiction with most specific obligation | Jurisdictions with no mapped control |
|---|---|---|---|
| Prompt injection | AML.T0051 | EU AI Act Art. 15 (interpretive; not applicable until 2027-12-02 Annex III / 2028-08-02 Annex I). UK CAF v4.0 B4.a/B4.b is the only obligation in force today, and only for automated decision-making | US (NIST/SOC2), AU ISM, SG TRM, IN CERT-In, JP, CA — and the EU until the deferred dates |
| ML supply chain (MCP, models) | AML.T0010 | EU CRA Annex I (post 2026-09-11 reporting) | All others — supply-chain controls do not name AI plugins |
| LLM C2 abuse (SesameOp) | AML.T0096 | None | All — no jurisdiction has a control for AI-API as C2 |
| Poison Training Data | AML.T0020 | EU AI Act Art. 10 (data and data governance for high-risk AI) | All others |
| LLM Jailbreak | AML.T0054 | None — same gap as AML.T0051 | All |
| Discover AI Model Ontology | AML.T0013 | None — adversary reconnaissance against deployed models, no mapped control | All |
| Develop Capabilities (AI-assisted weaponization) | AML.T0017 | None — adversary capability, not directly controllable | All |
| Privilege escalation (T1068) | ATT&CK T1068 | AU ISM-1696 / Essential 8 ML3 (48h patch with exploit) | EU (no specific SLA), UK (14d generic), SG (30d), JP, IN, CA |
| Exploit public-facing app (T1190) | ATT&CK T1190 | AU Essential 8 (patching applications) | All — none address AI-mediated T1190 like CVE-2025-53773 |
| Phishing (T1566) | ATT&CK T1566 | None updated for AI-generated content | All — phishing guidance generally pre-AI-baseline |

Use the framework-gap-analysis skill output alongside this skill's jurisdiction matrix to produce a per-jurisdiction TTP-coverage score.

---

## Exploit Availability Matrix

Per-jurisdiction breach- and incident-notification clocks. When a KEV-listed exploit with public PoC is in play, these clocks compress operationally — the regulator's published timeline is the upper bound, not the planning baseline.

| Jurisdiction | Framework | Trigger | Clock starts | Initial / final timeline | Tightening when PoC + KEV |
|---|---|---|---|---|---|
| EU | GDPR Art. 33 | Personal-data breach | Awareness | 72h to SA | Same legal clock; practical detection-to-classification window shrinks with confirmed active exploitation |
| EU | NIS2 Art. 23 | Significant incident | Awareness | 24h early warning / 72h notification / 1 month final | Early-warning trigger fires immediately on confirmed PoC affecting deployed asset |
| EU | DORA Art. 19 | Major ICT-related incident | Classification | 4h initial / 72h intermediate / 1 month final | 4h clock is unforgiving; KEV+PoC events likely auto-classify as major |
| EU | EU AI Act Art. 73 (high-risk providers; applies from 2027-12-02 Annex III / 2028-08-02 Annex I) | Serious incident for high-risk AI | Provider awareness / establishment of a causal link | 2 days for widespread infringement or a serious incident under Art. 3(49)(b) (critical-infrastructure disruption); 10 days for death of a person; 15 days default | KEV-class exploit chain in a high-risk AI deployment triggers the 2/10/15 cascade once the obligation applies |
| EU | EU CRA Art. 14 (manufacturers, from 2026-09-11) | Actively exploited vulnerability / severe incident in a product with digital elements | Manufacturer awareness of active exploitation | 24h early warning / 72h notification / 14 days after a corrective measure (1 month for severe incidents) | Active exploitation is the statutory trigger itself, not an aggravating factor — but it is `active_exploitation: confirmed` against a shipped version, not PoC availability. A public PoC does not start this clock; a KEV listing does once product applicability is confirmed |
| UK | UK GDPR | Personal-data breach | Awareness | 72h to ICO | Same as GDPR |
| AU | Notifiable Data Breaches | Eligible data breach | Awareness | "As soon as practicable" — typically interpreted ≤ 30 days | Active KEV exploitation collapses "practicable" to hours |
| SG | PDPA | Notifiable data breach | Awareness | 3 days to PDPC | Same |
| SG | CSA CCoP (CII) | Cyber incident | Confirmation | **2 hours** | Already among tightest globally |
| SG | MAS Notice 644 (critical incidents) | Severity-1 incident | Detection | **1 hour** | Tightest globally for affected banks |
| IN | CERT-In Directions | 20+ incident types | Awareness | **6 hours** | Tightest sector-agnostic globally |
| IN | SEBI | Cyber incident | Awareness | 6 hours | Same |
| JP | APPI | Personal data leak | Awareness | "Without delay" (interpreted ≤ 5 working days) | Same |
| CA | OSFI B-10 | High/critical tech-or-cyber incident | Classification | 24h to OSFI | Same |
| CA | PIPEDA | Real risk of significant harm | Awareness | As soon as feasible | Same |
| Global | ISO 27001 | n/a — framework only | n/a | Framework imposes no notification obligation | n/a |

Operational implication: an organisation subject to MAS Notice 644, CSA CCoP, CERT-In, and DORA simultaneously has a 1-hour effective notification floor — the tightest applicable clock governs. A single "we notify within 72h" runbook fails three of those four obligations. From 2026-09-11 an org that also manufactures a product with digital elements for the EU market carries a parallel 24-hour product-side vulnerability clock that most IR runbooks do not model at all.

Refer to `data/exploit-availability.json` for per-CVE PoC and KEV state; the matrix above tightens whenever any catalog entry's `active_exploitation` is `confirmed` or `cisa_kev` is `true`.

---

## Compliance Theater Check

The single most reliable test for global-GRC theater:

> "Open your incident-response runbook. For each jurisdiction your organisation is subject to — EU (NIS2, DORA, GDPR, EU AI Act), UK, AU, SG (MAS, CSA), IN (CERT-In, SEBI), JP, CA — show the per-jurisdiction notification clock with the clock-start trigger documented. A single global '72-hour notification' policy fails this test by definition for any org subject to DORA (4h), MAS Notice 644 (1h critical), CSA CCoP (2h), CERT-In (6h), or NIS2 (24h early warning). If your runbook does not list jurisdiction-specific clocks with trigger criteria, the global-GRC compliance claim is theatre — you do not have operational notification capability for at least one jurisdiction you are subject to."

Three follow-up tests:

> "Your DORA Art. 28 register of information for ICT third-party arrangements: does it include the LLM/AI API providers your business lines use? If `provider=openai` or `provider=anthropic` or `provider=google-cloud-vertex-ai` is absent and any business line uses these providers, the register is incomplete. ESA Joint Committee guidance on CTP designation for AI providers is evolving — your register must include them now and be updated as the CTP designation crystallises."

> "Your EU AI Act Art. 50 transparency compliance, live since 2026-08-02: for every deployed system that interacts with humans, generates synthetic audio/image/video/text, or performs emotion recognition or biometric categorisation, show the disclosure to the user and the machine-readable marking of generated content. Systems placed on the market before 2026-08-02 have until 2026-12-02 to meet Art. 50(2). If you cannot produce the marking implementation, the transparency claim is theatre — this obligation is enforceable now, not in 2027."

> "Your EU AI Act high-risk readiness against the deferred deadlines: identify every system in your inventory that would be a high-risk AI system under Annex III (obligations from 2027-12-02) or Annex I (from 2028-08-02). For each, show the Art. 9 risk management documentation and the Art. 15 cybersecurity controls (including resilience to prompt injection per the Commission's Q&A). If the inventory does not exist or shows zero high-risk systems despite the org operating AI in employment, education, law enforcement, critical infrastructure, biometric, or essential-services contexts, the readiness claim is theatre. A deferral is not a withdrawal: an org that stood its AI Act programme down when Regulation (EU) 2026/1744 landed will re-enter the same gap in 2027 with the same absent inventory, while the attack surface stays live throughout."

---

## Analysis Procedure

### Step 1: Determine jurisdiction scope

For the target organization, identify:
- Where is the organization incorporated?
- Where does it operate?
- Where are its customers/users located?
- What sectors does it operate in? (Financial, health, critical infrastructure, etc.)
- Does it offer products with digital elements to the EU? (CRA scope)

### Step 2: Map applicable frameworks

Based on jurisdiction scope, select applicable frameworks from the registry above.

### Step 3: Identify framework requirements per threat class

For each relevant threat (kernel LPE, prompt injection, MCP supply chain, AI C2, etc.):
1. Which jurisdiction's framework has the most specific requirement?
2. Which has the shortest notification timeline?
3. Which has the steepest penalties for non-compliance?
4. Are there gaps in all applicable frameworks (universal gap)?

### Step 4: Generate compliance matrix

Produce a matrix of: threat class × jurisdiction framework × requirement adequacy × notification trigger.

---

## Output Format

The skill produces a structured Global GRC Assessment that rolls compliance findings across the org's jurisdictional footprint — EU (NIS2, DORA, EU AI Act, CRA), UK (CAF, Cyber Essentials), AU (ISM, Essential 8, APRA CPS 234), ISO 27001:2022 / 42001:2023, NIST, and the expanded set tracked in `data/global-frameworks.json`. The shape below is consumed downstream by `framework-gap-analysis` (which produces per-jurisdiction Framework Lag Declarations), by `policy-exception-gen` (for cross-jurisdictional exception language), and by CSAF-style auditor evidence bundles. Preserve the per-jurisdiction control-mapping rows verbatim — they are the load-bearing global-first cross-walk.

```
## Global GRC Assessment

**Date:** YYYY-MM-DD
**Jurisdictions in scope:** [list]
**Sectors:** [list]

### Applicable Framework Matrix
| Framework | Jurisdiction | Trigger | Notification | Penalties | AI Coverage |
|-----------|-------------|---------|--------------|-----------|-------------|

### Fastest Notification Requirement
[Which jurisdiction, which framework, what timeline]

### Strictest AI/Security Requirements
[For current threats: which framework is most demanding]

### Universal Gaps
[Threats that no applicable framework covers adequately]

### Per-Threat Framework Mapping
[For each threat in scope: best available control, gap declaration]

### Recommended Control Additions
[Beyond framework requirements: what current threats require that frameworks don't mandate]
```
