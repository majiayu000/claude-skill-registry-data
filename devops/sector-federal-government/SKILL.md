---
name: sector-federal-government
version: "1.0.0"
description: Federal government + defense contractor cybersecurity for mid-2026 — FedRAMP Rev5, CMMC 2.0, EO 14028, NIST 800-171/172 CUI, FISMA, M-22-09 federal Zero Trust, OMB M-24-04 AI risk, CISA BOD/ED; cross-jurisdiction NCSC UK, ENISA EUCC, AU PSPF, IL government cyber methodology
triggers:
  - federal cyber
  - government cybersecurity
  - fedramp
  - cmmc
  - eo 14028
  - nist 800-171
  - nist 800-172
  - cui
  - fisma
  - federal zero trust
  - m-22-09
  - omb m-24-04
  - jab authorization
  - cisa bod
  - cisa ed
  - stateramp
data_deps:
  - cve-catalog.json
  - cwe-catalog.json
  - d3fend-catalog.json
  - exploit-availability.json
  - framework-control-gaps.json
atlas_refs: []
attack_refs:
  - T1190
  - T1195.001
  - T1554
framework_gaps:
  - FedRAMP-Rev5-Moderate
  - CMMC-2.0-Level-2
  - NIST-800-218-SSDF
  - SLSA-v1.0-Build-L3
  - NIS2-Art21-incident-handling
  - UK-CAF-A1
  - AU-Essential-8-App-Hardening
rfc_refs:
  - RFC-8032
  - RFC-8446
cwe_refs:
  - CWE-1357
  - CWE-1395
  - CWE-829
d3fend_refs:
  - D3-EAL
  - D3-EHB
  - D3-CBAN
forward_watch:
  - CMMC 2.0 phased rollout milestones through 2028 — Phase 1 (self-assessment) effective Dec 2024, Phase 2 (C3PAO assessments) ramping in 2025-2026, Phase 3 (DIBCAC-level assessments) and Phase 4 (full enforcement in all contracts) push into 2028
  - NIST SP 800-171 Rev 3 (May 2024) replacing Rev 2 in contracts — three-year transition; track which DoD / civilian agency contracts have crossed the Rev 3 boundary
  - NIST SP 800-172 Rev 3 (forthcoming) for the CMMC Level 3 "enhanced security requirements" baseline against APT
  - OMB M-24-04 federal AI risk-management implementation deadlines through 2025-2026 — agency CAIO appointments, AI use-case inventories, generative AI policies
  - FedRAMP 20x program (modernization effort, 2024-2026) — moving toward continuous authorization, machine-readable controls, OSCAL native, automated significant-change review
  - CISA Secure by Design and Secure by Default pledges — federal procurement leverage on commercial vendors, expanding through 2026
  - Cyber Incident Reporting for Critical Infrastructure Act (CIRCIA) final rule from CISA — 72-hour incident / 24-hour ransomware payment reporting, expected effective late 2026 / 2027 for federal contractors in covered CI sectors
  - UK GovAssure replacing the legacy IT Health Check (ITHC) scheme — phased rollout for departments and ALBs through 2026
  - EU Cybersecurity Certification Scheme on Common Criteria (EUCC) operational — first certificates issued 2024; high-assurance level for government use cases ramping
  - Australia PSPF 2024 revision and ISM quarterly updates — track for Essential Eight Maturity Level requirements for federal entities
last_threat_review: "2026-09-28"
discovery_mode: "standalone"  # operator-reached via `exceptd brief sector-federal-government` or `exceptd ask`; not chained into any playbook's direct.skill_chain by design
---

# Federal Government and Defense Contractor Cybersecurity

## Threat Context (mid-2026)

Federal government and defense industrial base (DIB) cybersecurity in mid-2026 is defined by five overlapping transformations driven by Executive Order 14028 (May 2021) and its successor directives:

- **Federal Zero Trust mandate operational, not aspirational.** OMB M-22-09 (January 2022) set agency deadlines for FY 2024 against the five federal Zero Trust pillars (identity, devices, networks, applications and workloads, data) and the cross-cutting CISA Zero Trust Maturity Model (ZTMM v2.0, April 2023). In mid-2026 the question is not "do you have a ZT strategy" but "which pillar is at Optimal vs. Advanced vs. Initial, what is the evidence, and where are the agency-specific gaps." Most federal agencies sit between Initial and Advanced on most pillars; the identity pillar (phishing-resistant MFA per M-22-09 §C.1.ii) is the most consistently mature, the data pillar the least.

- **FedRAMP Rev 5 baseline displaced Rev 4 in January 2024.** Cloud Service Providers (CSPs) pursuing or holding ATOs operate against the NIST SP 800-53 Rev 5 control set with FedRAMP Moderate (323 controls) or High (410 controls) baselines. JAB authorization remains the high-bar centralized path (P-ATO via the FedRAMP PMO + DoD + DHS + GSA Joint Authorization Board); Agency ATOs are the more common path. FedRAMP 20x is the in-progress modernization (continuous authorization, OSCAL machine-readable controls, automated significant-change review). StateRAMP (mid-2024 maturation) extends the model to US state and local procurement.

- **CMMC 2.0 final rule effective December 16, 2024; contractual flow-down via DFARS rule (32 CFR Part 170 + 48 CFR rule, published October 2024) enforced in phased rollout through 2028.** Levels are: Level 1 (Foundational, 15 practices aligned to FAR 52.204-21, annual self-assessment), Level 2 (Advanced, 110 practices aligned to NIST SP 800-171 Rev 2 — moving to Rev 3 over three-year transition, C3PAO third-party assessment every three years for prioritized contracts), Level 3 (Expert, Level 2 plus 24 enhanced practices from NIST SP 800-172, DIBCAC government-led assessment). The phased rollout (Phase 1 in effect, Phase 4 = full enforcement scheduled by 2028) means most contractors are mid-implementation. A contractor "working toward Level 2" without a target C3PAO assessment date and without an SPRS-submitted self-assessment score is behind the rollout curve, not on it.

- **EO 14028 Section 4 Software Supply Chain Security drove NIST SP 800-218 SSDF v1.1 (February 2022) into federal procurement.** OMB M-22-18 (September 2022) and M-23-16 (June 2023) require federal agencies to obtain self-attestation (CISA Secure Software Development Attestation Form, opened June 2024) from software producers for any software the government uses. The attestation references SSDF practices; SBOM submission is producer-determined format and is required when specifically requested. The supply chain compromise vectors (T1195.001 dependency compromise, the SolarWinds 2020 template, the XZ Utils 2024 maintainer-position long game) remain the dominant DIB threat class; SSDF attestation alone does not detect them — see the `supply-chain-integrity` skill.

- **OMB M-24-04 (March 2024) operationalized federal AI risk management.** Required agency Chief AI Officer (CAIO) appointment, public AI use-case inventory (per EO 14110, October 2023), generative AI policies, and minimum risk-management practices for safety-impacting and rights-impacting AI use cases. EO 14179 (January 2025) revoked EO 14110 and shifted federal AI policy emphasis; M-24-04 remains in force as OMB guidance and is the operational hook for federal AI program governance. NIST AI RMF (AI 100-1, January 2023) and the Generative AI Profile (NIST AI 600-1, July 2024) are the technical reference. See the `ai-attack-surface` skill for the AI-specific TTP layer.

State-sponsored adversary activity continues against federal targets. Volt Typhoon (PRC-linked) pre-positioning against US critical infrastructure (CISA + FBI + NSA + allied advisories, ongoing since the May 2023 joint advisory) and Salt Typhoon (PRC-linked) intrusions into US telecommunications providers (publicly disclosed late 2024) are the dominant nation-state context. Both campaigns explicitly target the contractor supply chain and managed-service-provider relationships that surround federal networks.

Allied governments are running parallel transformations. The UK NCSC GOV.UK Zero Trust target architecture and Cyber Essentials Plus for departments, the EU ENISA EUCC scheme (operational from 2024) for certified products in government use cases, the Australian PSPF 2024 revision and ISM continuous update with Essential Eight Maturity Level 3 for non-corporate Commonwealth entities, the Japan NISC Common Standards for Information Security Measures for Government Agencies, the Singapore GovTech / CSA Government Information Security Policy, and the Israel INCD Cyber Defense Methodology v2.1 (one of the most rigorous national methodologies, mandatory for government and CII) are the operational baselines outside the US. None map one-to-one to NIST 800-53; cross-jurisdiction assessments require explicit reconciliation rather than assumed equivalence.

---

## Framework Lag Declaration

| Framework | Control / Baseline | Why It Fails for mid-2026 Federal Threats |
|---|---|---|
| FedRAMP Rev 5 Moderate | NIST 800-53 Rev 5 Moderate baseline (323 controls) inherited via FedRAMP PMO | Authorization cycle (12-18 months JAB; 6-12 months agency) lags adversary capability. ConMon (continuous monitoring) deliverables can devolve into monthly POA&M checkbox updates without active threat-driven control re-validation. SA-12 / SR family supply-chain controls are process-level — do not require SLSA L3 provenance, in-toto attestation, or Sigstore signing (see `data/framework-control-gaps.json` `FedRAMP-Rev5-Moderate` entry). FedRAMP 20x modernization is in-progress, not in-force. |
| FedRAMP Rev 5 High | NIST 800-53 Rev 5 High baseline (410 controls) | Same lag profile as Moderate with broader control coverage. The marginal controls (PE physical-environment, additional CP contingency-planning, additional IR incident-response) do not address AI-coding-assistant, MCP server, or model-weight integrity vectors. |
| CMMC 2.0 Level 1 | 15 FAR 52.204-21 basic safeguarding practices, annual self-assessment | Floor-level. Designed for Federal Contract Information (FCI), not CUI. Self-attestation alone does not survive an adversary with Volt Typhoon-class persistence. Does not address AI, MCP, or supply-chain provenance. |
| CMMC 2.0 Level 2 | 110 practices = NIST SP 800-171 Rev 2 (moving to Rev 3); C3PAO triennial assessment for prioritized contracts; self-assessment with annual affirmation otherwise | 800-171 Rev 2 (2020) is the canonical CUI baseline; Rev 3 (May 2024) tightens and adds practices but enters contracts through a three-year transition. CMMC Level 2 does not require SLSA L3, Sigstore signing, AI-codegen provenance, or formal post-quantum cryptography roadmap. C3PAO assessment scope and depth varies; assessment-result-as-security is a known gap. |
| CMMC 2.0 Level 3 | Level 2 + 24 selected enhanced practices from NIST SP 800-172; DIBCAC government-led assessment | Targeted at APT-relevant programs. Still does not require federal Zero Trust pillar evidence beyond what 800-172 references; AI-system controls per NIST AI RMF are not built in. |
| NIST SP 800-171 Rev 2 | 110 security requirements across 14 families for protecting CUI in non-federal systems | Baseline-of-record for current contracts but predates: federal Zero Trust (M-22-09), SSDF attestation (M-22-18 / M-23-16), federal AI risk management (M-24-04), MCP / agentic AI attack surface, post-quantum cryptography migration. |
| NIST SP 800-171 Rev 3 | 800-171 update May 2024 — restructured families, expanded requirements, tighter alignment with 800-53 Rev 5 | Rev 3 enters contracts through three-year transition. Many contractors are still implementing Rev 2; some have not started Rev 3 gap analysis. Rev 3 does not include SLSA-level supply-chain requirements or AI-system-specific controls. |
| NIST SP 800-172 (Rev 2 current, Rev 3 forthcoming) | Enhanced security requirements for protecting CUI from APTs — the CMMC Level 3 source | The 800-172 controls (penetration-resistant architecture, damage-limiting operations, designed-for-cyber-resiliency) are strong on paper. Implementation evidence at most DIB contractors is sparse. |
| EO 14028 + OMB M-22-18 / M-23-16 + CISA Secure Software Development Attestation Form | Producer self-attestation against SSDF v1.1 practices for federal software procurement | Self-attestation. No third-party audit of SSDF practice implementation; the attestation form is producer-signed under penalty of false claims, which is real legal exposure but is not technical verification. SBOM submission is required only when specifically requested by the agency. AI-generated code provenance is not addressed. |
| FISMA (Federal Information Security Modernization Act of 2014) | Annual agency reporting to OMB and Congress via CIO Council, IG independent evaluation per OIG, CyberScope FISMA metrics | FISMA metric-set lags emerging threats by ~18-24 months. Annual reporting cadence is insufficient for nation-state-grade threats; episodic reporting via CISA BOD / ED partially compensates. |
| OMB M-22-09 Federal Zero Trust Strategy | Five pillars (identity, devices, networks, applications and workloads, data) with FY 2024 target outcomes; aligned to CISA ZTMM v2.0 | Strategy document, not a control catalog. Agency implementation is uneven across pillars. Data pillar (data tagging, encryption-in-use, DRM, DLP at the data layer) is the slowest-moving pillar across federal. AI-system and agentic-AI ZT extensions are not yet incorporated. |
| OMB M-24-04 Federal AI Risk Management | Agency CAIO, AI use-case inventory, generative AI policy, minimum practices for safety- and rights-impacting AI | Implementation deadlines through 2025-2026 not uniformly met. Generative AI policy at most agencies is restrictive-rather-than-enabling, driving shadow AI use. Does not specify ML-BOM, model-weight signing, or MCP server controls. |
| CISA Binding Operational Directives (BOD) and Emergency Directives (ED) | Mandatory directives to federal civilian executive branch (FCEB) agencies — examples: BOD 22-01 KEV remediation, BOD 23-01 asset discovery / vulnerability detection, BOD 23-02 secure cloud business apps, ED 24-01 Ivanti Connect Secure, ED 24-02 Microsoft midnight blizzard | Mandatory only on FCEB agencies; contractors and DoD do not directly inherit. Directive-by-directive coverage; not a comprehensive control framework. Lag from new threat publication to BOD/ED issuance is days to weeks in active campaigns but routinely months in slower-moving classes. |
| GSA MAS Cyber Schedule (Multiple Award Schedule with cyber-specific SINs) | GSA-issued cyber product/service categories — HACS SINs, IT Schedule 70 cyber | Procurement vehicle, not a security framework. Cyber SIN-listed products are pre-vetted at the category level, not against a uniform technical baseline. |
| UK NCSC for government — Cyber Essentials Plus + GovAssure + CAF for government | Cyber Essentials Plus (technical verification of the five Cyber Essentials controls); GovAssure (replacing legacy IT Health Check) using CAF (Cyber Assessment Framework) as the assessment basis | Cyber Essentials Plus is a baseline floor (firewalls, secure configuration, access control, malware protection, security update management); insufficient against nation-state threats alone. CAF principle-based assessment is more rigorous but interpretation-dependent. GovAssure rollout is phased through 2026. |
| EU institutions — ENISA EUCC + NIS2 transposition for government bodies + EU Cloud Code of Conduct | EUCC certification scheme based on Common Criteria; NIS2 (Directive 2022/2555) applies to public administration entities under national transposition | EUCC operational since 2024; high-assurance level for government use cases ramps slowly. NIS2 transposition into national law completed in most member states by late 2024 / early 2025 but enforcement maturity varies. Does not specify AI-system or MCP controls. |
| Australia PSPF + ISM | Protective Security Policy Framework (PSPF, revised 2024) for non-corporate Commonwealth entities; ISM as the technical baseline; Essential Eight Maturity Level 3 expected for federal entities | PSPF is policy-level; ISM is technical and updated quarterly. Essential Eight ML3 (application control, patch applications, MS Office macro settings, user application hardening, restrict admin privileges, patch operating systems, MFA, regular backups) is comprehensive at the endpoint and identity layer but does not specify AI-system, MCP, or model-weight integrity controls. |
| Japan NISC Common Standards | Common Standards for Information Security Measures for Government Agencies, periodic update cadence | National-government-only; not flowed down to contractors with the rigour of CMMC. AI-specific controls limited. |
| Singapore CSA / GovTech | Government Information Security Policy (Government Instruction Manual on Infocomm Technology and Smart Systems Management), CSA guidelines | Public-sector-specific; AI use governed by GovTech AI Verify-aligned practices, not yet a mandatory technical framework for government use. |
| Israel INCD Cyber Defense Methodology v2.1 | Mandatory for government and CII; layered defense with quantified maturity targets | One of the most rigorous national methodologies. Mid-2026: still does not pin SLSA level or Sigstore as the supply-chain control floor; AI-system extensions in development. |
| Canada Federal Government — CCCS ITSG-33 + Directive on Service and Digital | CCCS (Canadian Centre for Cyber Security) ITSG-33 IT security risk management framework; Treasury Board directives | NIST 800-53-aligned and process-oriented; AI-specific controls limited; supply-chain cryptographic-provenance floor not specified. |

**Fundamental gap:** No current federal framework — FedRAMP Rev 5, CMMC 2.0, NIST 800-171/172, or any allied government baseline — mandates cryptographic provenance verification (SLSA L3 + in-toto + Sigstore) for software entering federal environments, mandates model-weight signing for AI in federal use cases, or specifies MCP / agentic AI tool-trust controls. EO 14028 and SSDF attestation create procurement leverage but stop short of technical mandate. The federal Zero Trust mandate is real but is a strategy document, not a control framework; pillar maturity is uneven across agencies.

---

## TTP Mapping

| ATT&CK ID | Technique | Federal-Government Relevance | Gap |
|---|---|---|---|
| T1190 | Exploit Public-Facing Application | Federal-facing web apps (Login.gov, agency portals, contractor remote-access portals, FedRAMP-authorized SaaS), DIB extranet portals, CMS-class agency websites | CISA BOD 23-01 mandates asset discovery and vulnerability detection on FCEB internet-facing assets; BOD 22-01 mandates KEV remediation. Contractors do not directly inherit. T1190 against contractor portals remains a primary CUI exfil vector and is not consistently controlled at CMMC Level 2. |
| T1195.001 | Supply Chain Compromise: Compromise Software Dependencies and Development Tools | Federal supply chain — SolarWinds 2020 template; XZ Utils 2024 maintainer-position long game; ongoing npm / PyPI / Hugging Face / MCP namespace typosquats targeting DIB development environments | EO 14028 + SSDF attestation address this at the procurement layer (producer self-attestation). FedRAMP SA-12 / SR controls are process-level. No federal framework mandates SLSA L3 provenance, in-toto attestation, or Sigstore signature verification at load time. See `supply-chain-integrity` skill. |
| T1554 | Compromise Host Software Binary | Modification of binaries on federal endpoints, contractor workstations, or build-pipeline hosts; AI-coding-assistant binaries and MCP servers are in scope | NIST 800-53 SI-7 file-integrity monitoring is process-level. D3-EHB hash-based binary allowlisting at execution is the actual technical control and is not specified at CMMC Level 2 or FedRAMP Moderate. |

Cross-walk to CWE (see `data/cwe-catalog.json`):

| CWE | Why It Maps |
|---|---|
| CWE-1357 (Reliance on Insufficiently Trustworthy Component) | Continuous re-evaluation of contractor and supplier trust — XZ-class maintainer compromise, MCP package compromise. SSDF attestation is point-in-time, not continuous. |
| CWE-1395 (Dependency on Vulnerable Third-Party Component) | SBOM + VEX-aware CVE matching for federal procurement. EO 14028 SBOM submission required only on agency request; consumption maturity at federal agencies is uneven. |
| CWE-829 (Inclusion of Functionality from Untrusted Control Sphere) | MCP servers, AI coding assistants, and agentic-AI tooling running inside contractor CUI development environments. CMMC Level 2 does not specify allowlist controls at the MCP / AI-tool layer. |

---

## Exploit Availability Matrix

Sourced from `data/cve-catalog.json`, `data/exploit-availability.json`, and CISA KEV (https://www.cisa.gov/known-exploited-vulnerabilities-catalog) plus public federal incident history as of 2026-05-11. Every CVE reference includes CVSS, KEV status, PoC availability, AI-discovery flag, active-exploitation status, and patch availability (no theoretical-only intel). Technique-class rows are scored as ongoing class risks; CVSS is reported alongside RWEP for compatibility but is never the prioritization signal — RWEP is not assigned because the field is defined for individual CVEs in `data/cve-catalog.json`.

| Incident / Class | CVSS | RWEP | PoC Public? | CISA KEV? | AI-Accelerated? | Patch / Mitigation | FedRAMP-Visible? | CMMC-Visible? | SSDF-Attestable? |
|---|---|---|---|---|---|---|---|---|---|
| CVE-2026-30615 (Windsurf MCP local-vector RCE — DIB development environments) | 8.0 | 35 (see `cve-catalog.json`) | Yes | No (architectural class) | Rides on AI agent tool-call autonomy; AV:L (attacker-controlled HTML processed by the MCP client) | Vendor IDE update + manifest signing + MCP server allowlisting | Limited — developer workstation tooling typically outside FedRAMP boundary | Partially — CMMC Level 2 CM (configuration management) and AC (access control) families touch developer workstations handling CUI; MCP-specific controls absent | SSDF practice PS.2 covers software dependency integrity but does not specify MCP manifest signing |
| Volt Typhoon pre-positioning (PRC nation-state, CISA/FBI/NSA joint advisories ongoing since May 2023) | N/A (campaign) | N/A | Yes — public IOC sets and TTP descriptions | Multiple component CVEs in KEV | Yes — AI-assisted lateral movement reported in adjacent campaigns | Living-off-the-land detection; rigorous identity ZT (M-22-09 pillar 1); network ZT (M-22-09 pillar 3); credential hygiene | Partially — FedRAMP ConMon detects only the cloud-tenant surface | Partially — CMMC AC + AU + IR families address detection but not pre-positioning specifically | No — SSDF is producer-side |
| Salt Typhoon US telco intrusions (PRC nation-state, publicly disclosed late 2024) | N/A (campaign) | N/A | Yes — IOC sets and CISA/FBI joint advisories | Multiple component CVEs in KEV | Yes — large-scale exploitation of edge-device CVEs | Patch + replace EOL edge devices; lawful-intercept-interface hardening; segment carrier management plane | No — telco infrastructure outside FedRAMP scope | No — telco carriers outside CMMC scope | No |
| SolarWinds Orion supply-chain compromise (CVE-2020-10148 + SUNBURST backdoor, historical reference) | 9.8 | not in current `data/cve-catalog.json` — pre-scope incident | Yes — fully post-disclosure | Yes (KEV at time of disclosure) | No — long-game manual TTP | Patch; rotate all credentials handled by affected Orion deployments; rebuild from clean state | Yes — FedRAMP-authorized SolarWinds Orion ATOs were impacted; ConMon did not detect the implanted update | Yes — DIB contractors using Orion were impacted; current 800-171 SI-3 / SI-4 controls would not have detected the implant | Partially — SLSA L3 + in-toto + reproducible builds would have detected the build-time tampering; SSDF self-attestation alone would not |
| XZ Utils backdoor (CVE-2024-3094, 2024) | 10.0 | 45 (see `cve-catalog.json`; not KEV-listed, exploitation suspected, human-discovered) | Yes — fully public post-disclosure | No | No — multi-year human social-engineering long game | Distro rollback to 5.4.x; key revocation in federal build pipelines | Indirectly — federal-procured Linux distros downstream of upstream sshd were exposed | Yes — DIB development environments built against affected distros were in scope | Partially — SSDF PS.1 / PS.2 reference dependency integrity; do not require SLSA L3 detection |
| Typosquat against MCP / `@modelcontextprotocol/*` / Hugging Face namespaces targeting DIB AI developers (AML.T0010 class, ongoing) | N/A (technique class) | N/A | Yes — multiple public incidents | No (technique class) | Yes — AI assistants accelerate convincing tool-description authoring | Pin versions; verify publisher provenance; enforce private registry mirroring for CUI development environments | Limited | Partially — CMMC SC + SI families address some controls but MCP namespace specifically is not covered | Yes — SSDF practice PS.2 (software integrity) applies but does not specify the technique-class control |
| AI-generated code committed to federal / DIB codebases without provenance markers (no CVE — class risk) | N/A | N/A | Pervasive | No | Yes — by definition | Commit-trailer provenance markers; PR-level attestation; in-CI AI-code detector; restricted federal-codebase AI tool allowlist | No — not within FedRAMP control set | No — CMMC Level 2 does not address AI-codegen provenance | No — SSDF does not specify AI-codegen attribution |
| Edge / VPN appliance zero-days driving recent CISA Emergency Directives (ED 24-01 Ivanti Connect Secure class, ED 24-02 Microsoft / Midnight Blizzard, ongoing 2024-2026) | varies — multiple CVEs, most in KEV | varies | Yes — public PoCs typically within days | Yes | Yes — AI-assisted reverse engineering on appliance firmware reported | Vendor patch + agency-specific compensating controls per the ED text; ED-mandated actions within hours-to-days | Yes — affected appliances often within FedRAMP-authorized boundaries or boundary-adjacent | Yes — DIB contractors using affected appliances inherit the threat | Producer-side — appliance vendor SSDF attestations are downstream evidence |

Reference RFCs: **RFC 8032** (Edwards-Curve Digital Signature Algorithm, Ed25519 / Ed448) is the asymmetric signature baseline used by Sigstore keyless and by this project itself; relevant to federal SLSA / SSDF implementation choices. **RFC 8446** (TLS 1.3) is the in-transit-protection baseline; FedRAMP Rev 5 and CMMC Level 2 both reference TLS but allow TLS 1.2 for legacy interoperability — a known lag the `pqc-first` skill tracks for the eventual hybrid-PQC TLS migration (DRAFT-IETF-TLS-HYBRID-DESIGN / DRAFT-IETF-TLS-ECDHE-MLKEM).

---

## Analysis Procedure

The procedure threads three foundational principles. Each is non-negotiable for a federal or DIB environment under nation-state-class threat.

### Defense in depth

Layered controls aligned to the M-22-09 five pillars and the CISA ZTMM v2.0 maturity dimensions.

- **Identity pillar (M-22-09 §C).** Phishing-resistant MFA on every account (PIV/CAC for federal employees, FIDO2/WebAuthn for contractors and external users), enterprise IdP with continuous authentication, conditional access keyed to device posture. The identity pillar is the most-mature pillar across federal — but maturity at "Initial" or "Advanced" still leaves credential-theft gaps that Volt Typhoon-class adversaries exploit.
- **Device pillar (M-22-09 §D).** EDR on every endpoint with telemetry to a CDM-equivalent dashboard, device-attestation-gated network access, endpoint configuration management, application allowlisting (D3-EAL) for high-value asset environments.
- **Network pillar (M-22-09 §E).** Encrypt all DNS / HTTP traffic, isolate workloads with microsegmentation, default-deny east-west, no implicit trust by network location.
- **Applications and workloads pillar (M-22-09 §F).** Application-level access decisions, regular external pentest of internet-facing apps (CISA-recommended via High-Value Asset assessment programs and CDM agency penetration testing), DevSecOps with SAST + DAST + SCA + IAC scanning in CI.
- **Data pillar (M-22-09 §G).** Data inventory + classification + tagging, DLP at egress, encryption in use where feasible (confidential computing for sensitive workloads), data-categorization-driven access control.
- **Supply-chain layer overlay.** SSDF attestation from every software producer; SBOM submission requested for high-impact systems; SLSA L3 / Sigstore / in-toto adopted ahead of mandate where producer-side feasible; private mirrors for federal-code development to control package provenance.

### Least privilege

Federal CUI access is minimum-necessary, time-bounded, and instrumented.

- Personnel security: clearance level matched to data sensitivity, not job title; just-in-time elevation where feasible; periodic reinvestigation per the relevant tier.
- System access: role-based access plus attribute-based access for CUI; privileged access management with session recording for tier-0 systems; ephemeral credentials for build pipelines.
- AI / data-pipeline scope per OMB M-24-04: AI use cases scoped to minimum-necessary data; rights-impacting AI subject to the M-24-04 minimum risk-management practices; generative AI use cases have policy and DLP guardrails preventing CUI ingress to non-authorized models.
- Federal contractor extranet access: short-lived federated credentials; no shared service accounts; bastion-style access to internal systems with full audit.

### Zero trust

Verify-not-assume posture per M-22-09 and CISA ZTMM v2.0.

- Every access request is authenticated and authorized at request time; no implicit trust based on prior session, network position, or VPN connection.
- Continuous validation of identity, device, network, application, and data context — not point-in-time at login.
- Default-deny posture at each ZT pillar layer; explicit allow with logged justification.
- AI / agentic workflows treated as Zero Trust principals: every tool call from an AI agent is authenticated, authorized, and audited; no agentic AI is granted standing privileges to CUI repositories without explicit per-action authorization.

### Step-by-step procedure (10 steps)

1. **Scope determination.** Identify which environments are in scope: federal cloud workloads (FedRAMP), CUI-handling non-federal systems (NIST 800-171 / CMMC), federal-network on-premise systems (FISMA + 800-53 directly), DIB classified or controlled enclaves (DoD-specific), federal AI use cases (M-24-04 + 800-53 + NIST AI RMF), allied-government parallel environments (UK GovAssure, EU NIS2 public administration, AU PSPF, IL CDM v2.1). Map each scope to its controlling baseline.

2. **FedRAMP package scoping.** For cloud workloads pursuing or holding ATO: identify authorization type (JAB P-ATO vs. Agency ATO), baseline (Low / Moderate / High / LI-SaaS), boundary definition, inherited controls vs. customer-responsibility controls. For boundary changes, run significant-change review. Audit System Security Plan (SSP) currency, last 3PAO assessment date, ConMon submission cadence, POA&M aging.

3. **CMMC 2.0 assessment status.** For DoD contractors: confirm target Level (1 / 2 / 3), current SPRS self-assessment score (if Level 1 or self-assessment Level 2 contract), C3PAO assessment date (if assessed Level 2), or DIBCAC engagement (Level 3). Map current SSP / SPRS posture against the NIST 800-171 Rev 2 (or Rev 3, depending on contract) control set. Document phased-rollout phase exposure: Phase 1 (in effect), Phase 2 (ramping), Phase 3, Phase 4 (full enforcement).

4. **SSDF evidence pack for federal procurement.** For software-producer organizations: complete CISA Secure Software Development Attestation Form for each in-scope product; document SSDF v1.1 practice implementation evidence (PO, PS, PW, RV practices); collect SBOM in producer-chosen format (CycloneDX 1.6 or SPDX 3.0); maintain VEX statements per release. Producer false-claims exposure is real — attestation must reflect actual practice, not aspiration. Hand off to `supply-chain-integrity` skill for technical depth.

5. **CISA BOD / ED compliance check (FCEB agencies and federal contractors voluntarily mirroring).** Inventory current binding directives and emergency directives. Confirm KEV remediation per BOD 22-01 timelines (typically 14 days for KEV listings, accelerated for active exploitation). Confirm asset and vulnerability discovery cadence per BOD 23-01. Confirm secure cloud business apps configuration per BOD 23-01 and BOD 25-01 (where applicable). For each active ED, confirm remediation actions complete or documented compensating controls.

6. **AI inventory per OMB M-24-04.** Identify safety-impacting and rights-impacting AI use cases. Confirm CAIO appointment, agency AI use-case inventory publication, generative AI policy in force, minimum risk-management practices per M-24-04 §5 (for safety-impacting / rights-impacting use cases). Cross-walk to NIST AI RMF Generative AI Profile (NIST AI 600-1). Hand off to `ai-attack-surface` and `ai-c2-detection` skills for AI-specific TTP coverage.

7. **Federal Zero Trust scorecard per M-22-09 pillars + CISA ZTMM v2.0.** For each of the five M-22-09 pillars (identity, devices, networks, applications and workloads, data) score against the ZTMM v2.0 maturity dimensions (Traditional, Initial, Advanced, Optimal). Document evidence per dimension. The data pillar typically lags most; flag deltas with timeline.

8. **Allied-jurisdiction cross-walk.** For multi-jurisdiction federal contractors or international government collaborations, map each environment against the local government baseline: UK Cyber Essentials Plus + GovAssure / CAF; EU EUCC + NIS2 transposition for public administration; AU PSPF + ISM with Essential Eight ML3; JP NISC Common Standards; SG GovTech / CSA Government Information Security Policy; IL INCD CDM v2.1; CA CCCS ITSG-33. Identify control-equivalence gaps explicitly rather than assuming reciprocity.

9. **Identity assurance per NIST 800-63 + M-22-09 identity pillar.** Confirm IAL / AAL / FAL levels for each federal user population; verify phishing-resistant authenticator (PIV / CAC / FIDO2 / WebAuthn) on every account at the appropriate AAL; verify FAL aligned with the federation protocol. Hand off to `identity-assurance` skill for technical depth.

10. **Gap remediation roadmap.** For each identified gap (FedRAMP control deficiency, CMMC practice gap, SSDF practice gap, BOD/ED non-compliance, ZT pillar maturity gap, AI inventory gap, allied-jurisdiction gap), document: specific delta, owner, target date, success criterion, and RWEP-driven prioritization for any CVE-driven gaps.

---

## Output Format

The skill produces a Federal Government / DIB Cybersecurity Assessment covering FedRAMP Rev5 Moderate / High coverage, CMMC 2.0 Level 1/2/3 maturity, NIST 800-171 Rev 2/3 + 800-172 enhanced security requirements, M-22-09 zero-trust strategy progress, M-24-04 AI obligations, UK GovAssure, EU NIS2 public administration, AU PSPF / ISM Essential 8, and IL CDM v2.1. The shape below is consumed downstream by `incident-response-playbook` (for federal IR notification clocks), by `compliance-theater` (FedRAMP-vs-deployed comparison), and by `global-grc` (for cross-jurisdictional government rollup). Preserve the per-baseline maturity rows verbatim — they are the auditable evidence for ATO / continuous-ATO renewal.

```
## Federal Government / DIB Cybersecurity Assessment

**Assessment Date:** YYYY-MM-DD
**Scope:** [federal agency / DIB contractor / federal cloud workload / multi-jurisdiction government]
**Baselines in scope:** [FedRAMP Rev5 Moderate | FedRAMP Rev5 High | CMMC 2.0 Level 1/2/3 | NIST 800-171 Rev 2/3 | NIST 800-172 | FISMA | M-22-09 | M-24-04 | UK GovAssure | EU NIS2 public admin | AU PSPF/ISM E8 | IL CDM v2.1]
**Phased rollout exposure (CMMC):** [Phase 1 / 2 / 3 / 4]

### FedRAMP Package Status
| Attribute | Value | Gap |
| Authorization type | JAB P-ATO / Agency ATO | |
| Baseline | Moderate / High / LI-SaaS | |
| Boundary scope | [description] | |
| Last 3PAO assessment | YYYY-MM-DD | |
| ConMon cadence | monthly POA&M / sig change reviews | |
| Open POA&M items (high) | [count and aging] | |

### CMMC 2.0 Assessment Matrix
| NIST 800-171 family | Rev 2 / Rev 3 contract | Current SPRS score | Target Level | C3PAO date | Evidence gaps |

### SSDF Attestation Evidence Pack
| Product | Attestation submitted (CISA form) | SSDF practice gaps | SBOM format | VEX coverage | Producer signing in place |

### BOD / ED Compliance Status (FCEB or voluntary)
| Directive | Issued | Action required | Current status | Open delta |

### Federal Zero Trust Scorecard (M-22-09 + ZTMM v2.0)
| Pillar | Traditional | Initial | Advanced | Optimal | Current | Evidence |
| Identity | | | | | | |
| Devices | | | | | | |
| Networks | | | | | | |
| Applications and Workloads | | | | | | |
| Data | | | | | | |

### Federal AI Inventory (M-24-04)
| Use case | Safety-impacting? | Rights-impacting? | Minimum risk-management practices in place | NIST AI RMF profile alignment | Generative AI policy in force |

### CVE / Incident Exposure
[Per Exploit Availability Matrix — CVE-2026-30615 status, Volt Typhoon / Salt Typhoon detection coverage, active CISA EDs, KEV remediation aging]

### Allied-Jurisdiction Cross-Walk (if applicable)
| Jurisdiction | Baseline | Current posture | Control-equivalence gaps to US baseline |

### Framework Gap Declaration
[Per baseline in scope: which control nominally applies, why current implementation does not close the federal-threat gap, what concrete evidence would close it. Reference `data/framework-control-gaps.json`.]

### Gap Remediation Roadmap
[Prioritized by RWEP for CVE-driven gaps; otherwise by blast radius and phased-rollout exposure. Each item: specific delta, owner, target date, success criterion.]
```

---

## Compliance Theater Check

Concrete tests distinguishing paper compliance from operational federal security. Run all three. Any "we don't" or "we're working on it without a date" answer is theater.

1. **FedRAMP continuous monitoring substance.** Ask: *"Show your last three monthly ConMon submissions and the last significant-change review. Identify one POA&M item that closed in the last 90 days, the artifact that demonstrated closure, and the 3PAO or agency review that accepted it. Identify one POA&M item that aged beyond its remediation milestone and the documented compensating control."* If monthly ConMon is a templated checkbox upload with no aging analysis, no significant-change reviews triggered against actual environment changes, and no closed-with-artifact items, FedRAMP authorization is paper. The control set is real; the evidence pipeline is not.

2. **CMMC Level 2 evidence vs. target date.** Ask: *"What is your current SPRS self-assessment score, what is your target CMMC Level 2 C3PAO assessment date, and which contracts flow down CMMC Level 2 obligations to you under the phased rollout? For the contracts already requiring Level 2, what are you doing right now to remain compliant while the C3PAO assessment is pending?"* If the answer is "we're working toward Level 2" without an SPRS score, without a target C3PAO date, and without an interim compensating-control narrative for the contracts that are already obligated, you are behind the phased rollout, not on it. The DoD has been signaling December 2024 effectiveness since 2021 — contractors without a current SPRS score and a 2025-2026 C3PAO date are exposed to false-claims-act risk on existing contracts and to award denial on new ones.

3. **EO 14028 SBOM and SSDF attestation reality.** Ask: *"Pull your last CISA Secure Software Development Attestation Form submission. For one SSDF practice you attested to (e.g., PS.2 protect software from unauthorized access and tampering), show me the evidence that supports the attestation: the code-signing setup, the secure repository configuration, the dependency-integrity verification mechanism, and the audit trail showing it operated for the past 12 months. If an agency requests your SBOM under M-22-18 / M-23-16, what artifact do you ship, in what format, and what is its time-to-deliver SLO?"* If the SSDF attestation references practices without evidence of operation, the attestation is a legal exposure rather than a security control. If SBOM delivery is "we'd have to generate one," the producer-side SBOM-on-request capability is theater. Both are common.

A genuinely conformant federal program answers all three with concrete artifacts: aged-and-closed POA&Ms with traceable 3PAO acceptance, SPRS scores with C3PAO milestones, and SSDF-attestation evidence packs with current SBOMs and VEX statements on demand.

---

## Defensive Countermeasure Mapping

D3FEND techniques referenced (see `data/d3fend-catalog.json`):

- **D3-EAL (Executable Allowlisting)** — Runtime restriction of executable content on federal endpoints and DIB CUI workstations. Maps to NIST 800-53 SI-7 enhancement, CMMC Level 2 CM family, and AU Essential Eight Maturity Level 3 "Application Control" practice. Defense-in-depth layer: endpoint execution control. Least-privilege scope: per-host allowlist scoped to the role of that host. Zero-trust posture: default-deny on unsigned or non-allowlisted executables. AI-pipeline applicability: D3-EAL applies to AI inference hosts loading model binaries; the same default-deny applies to model weights via D3-EHB.
- **D3-EHB (Executable Hash-based Allowlist)** — SHA-256 hash pinning at the binary / artifact level. For federal procurement: maps to the SLSA / Sigstore-verified hash of signed artifacts at the point of admission. Defense-in-depth layer: runtime active rejection layer that closes the loop on EO 14028 SSDF attestation. Least-privilege scope: scoped per-artifact-publisher allowlist. Zero-trust posture: verify the publisher identity and the artifact hash against transparency-log inclusion before execution. AI-pipeline applicability: D3-EHB is the model-weight integrity control — load-time SHA-256 verification against a pinned publishing identity (Sigstore Fulcio certificate subject + Rekor inclusion proof) is the operational pattern.
- **D3-CBAN (Certificate-Based Authentication)** — Public-key-certificate-based authentication. Maps directly to PIV / CAC issuance under NIST 800-63 for federal employees and contractors; FIDO2 / WebAuthn for external federal users. Defense-in-depth layer: identity pillar of M-22-09 federal Zero Trust. Least-privilege scope: certificate-bound to a specific user identity with attribute-driven authorization decisions. Zero-trust posture: phishing-resistant by construction; verify the certificate chain, the revocation status, and the binding identity continuously, not just at session start. AI-pipeline applicability: D3-CBAN authenticates the human operator of an agentic AI session and authenticates the agentic AI principal itself (workload identity bound to a federation-issued certificate).

Signing baseline reference: RFC 8032 (Ed25519 / Ed448) is the asymmetric algorithm used by Sigstore keyless and by NIST-approved federal signing implementations alongside ECDSA. In-transit-protection baseline: RFC 8446 (TLS 1.3); federal use cases retaining TLS 1.2 for legacy interoperability should track the `pqc-first` skill for the hybrid-PQC TLS migration path.

Forward-watch: CMMC Level 3 (NIST 800-172 enhanced practices) addresses APT-relevant scenarios but does not yet incorporate AI-system controls; SLSA / Sigstore / in-toto adoption ahead of mandate is the supply-chain control track; PQC migration via NIST FIPS 203 / 204 / 205 entering federal signing baselines through the next 800-53 control-update cycle.

---

## Hand-Off

- **`supply-chain-integrity`** — SSDF practice evidence, SLSA L3 attestation, in-toto chain, Sigstore / cosign keyless signing, SBOM (CycloneDX 1.6 / SPDX 3.0), VEX via CSAF 2.0 for federal procurement.
- **`attack-surface-pentest`** — Federal red-team and High-Value Asset assessment scoping; CISA penetration testing program alignment; allied-government red-team baselines.
- **`identity-assurance`** — NIST 800-63 IAL / AAL / FAL; PIV / CAC issuance; FIDO2 / WebAuthn for federal external users; M-22-09 identity pillar evidence.
- **`ai-attack-surface`** — Federal AI use cases under OMB M-24-04; NIST AI RMF Generative AI Profile (NIST AI 600-1); MITRE ATLAS v2026.09 TTP coverage for federal AI threat modeling.
- **`ai-c2-detection`** — Detection of agentic-AI command-and-control inside federal networks.
- **`compliance-theater`** — Distinguishing FedRAMP / CMMC paper compliance from operational federal security; ConMon substance audit; SPRS-score-vs-evidence reconciliation.
- **`framework-gap-analysis`** — Per-control gap analysis when an explicit framework-vs-threat reconciliation is requested by an auditor or AO.
- **`global-grc`** — Cross-jurisdiction reconciliation when a federal contractor also operates under EU NIS2, UK CAF / GovAssure, AU PSPF / ISM, IL CDM v2.1, or similar allied government baselines.
- **`pqc-first`** — Post-quantum cryptography migration roadmap for federal signing and TLS baselines.
